#!/usr/bin/env python3
"""Phase B (delta variant) — params and selection for the delta/premium strategy.

This variant keeps the original ``PriceBook`` data layer and engine mechanics, but
changes how the two legs are *selected*:

* **Long monthly leg** — chosen by target |delta| (ITM), e.g. ~0.70, instead of a
  fixed % moneyness. Delta is Black-76 using the day's ATM-IV estimate.
* **Short daily leg** — chosen by target traded *premium* (USD per BTC), e.g. ~$550,
  using each option's real traded VWAP that day.

``PriceBookDelta`` subclasses ``PriceBook`` and only adds selection helpers, so the
original ``strategy.py`` is left untouched.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from backtest import config, options_pricing
from backtest.strategy import PriceBook


@dataclass
class StrategyParamsDelta:
    """Tunable parameters for the delta/premium PMCC/PMCP variant."""

    contracts: int = 1000                       # 1000 * 0.001 BTC = 1 BTC notional per leg
    short_dte_min: int = 1
    short_dte_max: int = 3
    long_dte_min: int = 21
    long_dte_max: int = 45
    long_dte_target: int = 30
    long_roll_min_dte: int = 7                  # roll the long leg when its DTE drops below this
    # New selection targets (replace short_otm / long_itm moneyness):
    long_delta_target: float = config.LONG_DELTA_TARGET    # |delta| target for the long ITM leg
    short_premium_target: float = config.SHORT_PREMIUM_TARGET  # USD/BTC premium target for the short leg
    taker_fee: float = config.DEFAULT_TAKER_FEE
    slippage: float = config.DEFAULT_SLIPPAGE
    start_cash: float = 100_000.0
    risk_free: float = 0.0
    default_iv: float = 0.6


class PriceBookDelta(PriceBook):
    """``PriceBook`` plus delta-based and premium-based instrument selection."""

    def delta(self, date: pd.Timestamp, sym: str) -> float:
        """Black-76 delta (signed) for an instrument on a date, using the day's ATM IV."""
        is_call, strike, expiry = self.meta(sym)
        spot = self.spot.get(date)
        if spot is None or np.isnan(spot):
            return float("nan")
        t = max((expiry - date).days, 0) / 365.0
        if t <= 0.0:
            return options_pricing.black76_delta(float(spot), strike, 0.0, 0.0, self.r, is_call)
        return options_pricing.black76_delta(
            float(spot), strike, t, self.iv(date, self.atm_iv.median()), self.r, is_call
        )

    def _candidates(
        self, date: pd.Timestamp, is_call: bool, dte_min: int, dte_max: int, dte_target: int | None
    ) -> tuple[pd.DataFrame, float] | None:
        """Traded candidates on the expiry nearest ``dte_target`` within the DTE window."""
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
        return cand[cand["expiry"] == chosen_expiry], float(spot)

    def select_by_delta(
        self, date: pd.Timestamp, is_call: bool, dte_min: int, dte_max: int,
        target_delta: float, dte_target: int | None = None,
    ) -> str | None:
        """Pick the traded instrument whose |delta| is nearest ``target_delta``."""
        result = self._candidates(date, is_call, dte_min, dte_max, dte_target)
        if result is None:
            return None
        same, spot = result
        t = max((pd.Timestamp(same["expiry"].iloc[0]) - date).days, 1) / 365.0
        iv = self.iv(date, self.atm_iv.median())
        deltas = same["strike"].apply(
            lambda k: abs(options_pricing.black76_delta(spot, float(k), t, iv, self.r, is_call))
        )
        return str(same.loc[(deltas - target_delta).abs().idxmin(), "product_symbol"])

    def select_by_premium(
        self, date: pd.Timestamp, is_call: bool, dte_min: int, dte_max: int,
        target_premium: float, dte_target: int | None = None,
    ) -> str | None:
        """Pick the traded instrument whose VWAP premium is nearest ``target_premium``."""
        result = self._candidates(date, is_call, dte_min, dte_max, dte_target)
        if result is None:
            return None
        same, _ = result
        return str(same.loc[(same["vwap"] - target_premium).abs().idxmin(), "product_symbol"])
