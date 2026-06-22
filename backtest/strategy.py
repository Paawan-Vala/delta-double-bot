#!/usr/bin/env python3
"""Phase 3b (data layer) — strategy params, instrument selection and option pricing.

`PriceBook` wraps the processed daily option table and futures candles and answers
the two questions the engine needs each day:

* **Selection** — given a date, option type, an expiry window and a target moneyness,
  which Delta instrument should we trade? (nearest available *traded* strike on the
  expiry closest to the target DTE).
* **Pricing** — what is an option worth on a date? Prefer that day's traded VWAP;
  otherwise fall back to a Black-76 reprice using the day's spot and an ATM-IV estimate.

Conventions: option ``price`` is USD per 1 BTC of underlying; cash for ``n`` contracts
is ``price * LOT_SIZE_BTC * n``.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from backtest import config, options_pricing


@dataclass
class StrategyParams:
    """Tunable PMCC/PMCP parameters."""

    contracts: int = 1000               # 1000 * 0.001 BTC = 1 BTC notional per leg
    short_dte_min: int = 1
    short_dte_max: int = 3
    long_dte_min: int = 21
    long_dte_max: int = 45
    long_dte_target: int = 30
    short_otm: float = 0.03             # short strike = spot * (1 ± short_otm)
    long_itm: float = 0.10             # long strike  = spot * (1 ∓ long_itm)
    long_roll_min_dte: int = 7         # roll the long leg when its DTE drops below this
    taker_fee: float = config.DEFAULT_TAKER_FEE
    slippage: float = config.DEFAULT_SLIPPAGE
    start_cash: float = 100_000.0
    risk_free: float = 0.0
    default_iv: float = 0.6


@dataclass
class Leg:
    """One option leg of a position."""

    product_symbol: str
    is_call: bool
    strike: float
    expiry: pd.Timestamp
    contracts: int
    side: int                # +1 long, -1 short
    entry_price: float       # USD per BTC
    entry_date: pd.Timestamp


@dataclass
class Position:
    """An open PMCC/PMCP position (one long + one short leg)."""

    direction: str           # "bull" (PMCC) or "bear" (PMCP)
    open_date: pd.Timestamp
    long_leg: Leg
    short_leg: Leg
    rolls: int = 0
    realized: float = field(default=0.0)  # realized P/L booked from short-leg rolls


class PriceBook:
    """Daily option price lookup, instrument selection, and ATM-IV estimation."""

    def __init__(self, options_df: pd.DataFrame, futures_df: pd.DataFrame, risk_free: float = 0.0) -> None:
        self.r = risk_free
        opts = options_df.copy()
        opts["date"] = pd.to_datetime(opts["date"])
        opts["expiry"] = pd.to_datetime(opts["expiry"])
        self._opts = opts
        self.spot: pd.Series = futures_df["close"]

        self._meta = opts.drop_duplicates("product_symbol").set_index("product_symbol")[
            ["option_type", "strike", "expiry"]
        ]
        self._price = {
            sym: g.set_index("date")["vwap"].sort_index()
            for sym, g in opts.groupby("product_symbol")
        }
        self._by_date = {d: g for d, g in opts.groupby("date")}
        self.atm_iv = self._estimate_atm_iv()

    # --- ATM IV --------------------------------------------------------------
    def _estimate_atm_iv(self) -> pd.Series:
        """Per-date ATM implied vol from the nearest-to-spot option (DTE 5–45)."""
        iv_by_date: dict[pd.Timestamp, float] = {}
        for date, g in self._by_date.items():
            spot = self.spot.get(date)
            if spot is None or np.isnan(spot):
                continue
            dte = (g["expiry"] - date).dt.days
            band = g[(dte >= 5) & (dte <= 45) & (g["volume"] > 0)]
            if band.empty:
                continue
            row = band.iloc[(band["strike"] - spot).abs().argmin()]
            t = max((row["expiry"] - date).days, 1) / 365.0
            iv = options_pricing.black76_implied_vol(
                float(row["vwap"]), float(spot), float(row["strike"]), t, self.r,
                is_call=(row["option_type"] == "C"),
            )
            if not np.isnan(iv):
                iv_by_date[date] = iv
        series = pd.Series(iv_by_date).sort_index()
        return series.reindex(self.spot.index).ffill()

    def iv(self, date: pd.Timestamp, default: float = 0.6) -> float:
        """ATM IV estimate for a date (falls back to ``default``)."""
        v = self.atm_iv.get(date, np.nan)
        return float(v) if v is not None and not np.isnan(v) else default

    # --- Selection -----------------------------------------------------------
    def select_leg(
        self, date: pd.Timestamp, is_call: bool, dte_min: int, dte_max: int,
        target_moneyness: float, dte_target: int | None = None,
    ) -> str | None:
        """Pick a traded instrument: expiry nearest ``dte_target``, strike nearest target."""
        g = self._by_date.get(date)
        spot = self.spot.get(date)
        if g is None or spot is None or np.isnan(spot):
            return None
        typ = "C" if is_call else "P"
        dte = (g["expiry"] - date).dt.days
        cand = g[(g["option_type"] == typ) & (dte >= dte_min) & (dte <= dte_max) & (g["volume"] > 0)]
        if cand.empty:
            return None
        cand_dte = (cand["expiry"] - date).dt.days
        target = dte_target if dte_target is not None else int(cand_dte.median())
        chosen_expiry = cand.loc[(cand_dte - target).abs().idxmin(), "expiry"]
        same = cand[cand["expiry"] == chosen_expiry]
        target_strike = spot * target_moneyness
        return str(same.loc[(same["strike"] - target_strike).abs().idxmin(), "product_symbol"])

    # --- Pricing -------------------------------------------------------------
    def meta(self, sym: str) -> tuple[bool, float, pd.Timestamp]:
        """Return (is_call, strike, expiry) for an instrument."""
        m = self._meta.loc[sym]
        return m["option_type"] == "C", float(m["strike"]), pd.Timestamp(m["expiry"])

    def price(self, date: pd.Timestamp, sym: str, default_iv: float = 0.6) -> float:
        """Price an instrument on a date: traded VWAP, else Black-76 reprice."""
        series = self._price.get(sym)
        if series is not None and date in series.index:
            val = series.loc[date]
            if not np.isnan(val):
                return float(val)
        is_call, strike, expiry = self.meta(sym)
        spot = self.spot.get(date)
        if spot is None or np.isnan(spot):
            # last resort: most recent traded price
            if series is not None:
                asof = series.loc[:date]
                if not asof.empty:
                    return float(asof.iloc[-1])
            return 0.0
        t = max((expiry - date).days, 0) / 365.0
        if t <= 0:
            return options_pricing.intrinsic(float(spot), strike, is_call)
        return options_pricing.black76_price(
            float(spot), strike, t, self.iv(date, default_iv), self.r, is_call,
        )
