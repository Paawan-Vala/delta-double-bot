#!/usr/bin/env python3
"""Variant 3 — the "double diagonal" income strategy from the reference videos.

This is the merged Poor Man's Covered Call + Covered Put taught in the source videos:
**non-directional and always-on**. It continuously holds FOUR legs and harvests premium
on both sides every day:

* long monthly ITM **call**  (delta ~+target)   — hedge for the short call
* short daily **call**       (premium target)   — income
* long monthly ITM **put**   (delta ~-target)   — hedge for the short put
* short daily **put**        (premium target)   — income

There is NO trend filter (unlike the other two strategies): it opens the full 4-leg
structure as soon as the chain allows and then rolls the daily shorts and the monthly
longs continuously. Reuses ``PriceBookDelta`` selection and ``BacktestEngine`` fills, so
the original two strategies are untouched.

Usage:
    python -m backtest.engine_double
    python -m backtest.engine_double -v
"""
from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass

import pandas as pd

from backtest import config, indicators
from backtest.engine import BacktestEngine
from backtest.strategy import Leg
from backtest.strategy_delta import PriceBookDelta

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
LOT = config.LOT_SIZE_BTC


@dataclass
class DoubleParams:
    """Tunable parameters for the continuous double-diagonal strategy."""

    contracts: int = 1000                       # per leg (1000 * 0.001 BTC = 1 BTC notional)
    short_dte_min: int = 1
    short_dte_max: int = 3
    long_dte_min: int = 21
    long_dte_max: int = 45
    long_dte_target: int = 30
    long_roll_min_dte: int = 7
    long_delta_target: float = 0.70             # |delta| of each long ITM leg (videos: 0.67-0.84)
    short_premium_target: float = 550.0         # USD/BTC premium for each daily short
    taker_fee: float = config.DEFAULT_TAKER_FEE
    slippage: float = config.DEFAULT_SLIPPAGE
    start_cash: float = 100_000.0
    risk_free: float = 0.0
    default_iv: float = 0.6


class DoubleEngine(BacktestEngine):
    """Continuous, non-directional 4-leg (call + put diagonal) backtester."""

    def __init__(self, book: PriceBookDelta, params: DoubleParams, dates: pd.DatetimeIndex) -> None:
        self.book = book
        self.p = params
        self.cash = params.start_cash
        self._pos_cashflow = 0.0
        self.dates = dates
        self.lc: Leg | None = None   # long call
        self.sc: Leg | None = None   # short call
        self.lp: Leg | None = None   # long put
        self.sp: Leg | None = None   # short put
        self.trades: list[dict] = []
        self.records: list[dict] = []

    # --- structure management -----------------------------------------------
    def _open_all(self, date: pd.Timestamp) -> bool:
        lc = self.book.select_by_delta(date, True, self.p.long_dte_min, self.p.long_dte_max,
                                       self.p.long_delta_target, self.p.long_dte_target)
        sc = self.book.select_by_premium(date, True, self.p.short_dte_min, self.p.short_dte_max,
                                         self.p.short_premium_target)
        lp = self.book.select_by_delta(date, False, self.p.long_dte_min, self.p.long_dte_max,
                                       self.p.long_delta_target, self.p.long_dte_target)
        sp = self.book.select_by_premium(date, False, self.p.short_dte_min, self.p.short_dte_max,
                                         self.p.short_premium_target)
        if not (lc and sc and lp and sp):
            return False
        self.lc = self._make_leg(date, lc, side=+1)
        self.sc = self._make_leg(date, sc, side=-1)
        self.lp = self._make_leg(date, lp, side=+1)
        self.sp = self._make_leg(date, sp, side=-1)
        self.trades.append({"event": "open", "date": date, "long_call": lc, "short_call": sc,
                            "long_put": lp, "short_put": sp, "cash": self.cash})
        return True

    def _close_all(self, date: pd.Timestamp, reason: str = "reset") -> None:
        for attr in ("lc", "sc", "lp", "sp"):
            leg = getattr(self, attr)
            if leg is not None:
                self._close_leg(date, leg)
                setattr(self, attr, None)
        self.trades.append({"event": "close", "date": date, "reason": reason, "cash": self.cash})

    def _roll(self, date: pd.Timestamp, which: str) -> None:
        leg = getattr(self, which)
        if leg is None:
            return
        self._close_leg(date, leg)
        is_call = which in ("lc", "sc")
        if which in ("sc", "sp"):
            new_sym = self.book.select_by_premium(date, is_call, self.p.short_dte_min,
                                                  self.p.short_dte_max, self.p.short_premium_target)
            side = -1
        else:
            new_sym = self.book.select_by_delta(date, is_call, self.p.long_dte_min, self.p.long_dte_max,
                                                self.p.long_delta_target, self.p.long_dte_target)
            side = +1
        if not new_sym:
            setattr(self, which, None)
            return
        setattr(self, which, self._make_leg(date, new_sym, side=side))
        self.trades.append({"event": f"roll_{which}", "date": date, "sym": new_sym, "cash": self.cash})

    def _mtm(self, date: pd.Timestamp) -> float:
        """Mark-to-market of the 4-leg portfolio (longs +, shorts -)."""
        value = 0.0
        for leg in (self.lc, self.lp):
            if leg is not None:
                value += self.book.price(date, leg.product_symbol, self.p.default_iv) * LOT * self.p.contracts
        for leg in (self.sc, self.sp):
            if leg is not None:
                value -= self.book.price(date, leg.product_symbol, self.p.default_iv) * LOT * self.p.contracts
        return value

    # --- main loop -----------------------------------------------------------
    def run(self) -> dict[str, pd.DataFrame]:
        dates = list(self.dates)
        for date in dates:
            legs = (self.lc, self.sc, self.lp, self.sp)
            present = sum(leg is not None for leg in legs)
            if 0 < present < 4:                       # incomplete structure -> reset cleanly
                self._close_all(date, reason="incomplete")

            if all(leg is None for leg in (self.lc, self.sc, self.lp, self.sp)):
                self._open_all(date)
            else:
                if (self.sc.expiry - date).days <= self.p.short_dte_min:
                    self._roll(date, "sc")
                if self.sp is not None and (self.sp.expiry - date).days <= self.p.short_dte_min:
                    self._roll(date, "sp")
                if self.lc is not None and (self.lc.expiry - date).days < self.p.long_roll_min_dte:
                    self._roll(date, "lc")
                if self.lp is not None and (self.lp.expiry - date).days < self.p.long_roll_min_dte:
                    self._roll(date, "lp")

            pos_val = self._mtm(date)
            self.records.append({
                "date": date, "spot": float(self.book.spot.get(date, float("nan"))),
                "direction": "double", "cash": self.cash, "position_value": pos_val,
                "equity": self.cash + pos_val, "in_position": self.lc is not None,
            })

        if any(getattr(self, a) is not None for a in ("lc", "sc", "lp", "sp")):
            self._close_all(dates[-1], reason="end")

        equity = pd.DataFrame(self.records).set_index("date")
        trades = pd.DataFrame(self.trades)
        return {"equity": equity, "trades": trades}


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run the continuous double-diagonal (PMCC+PMCP) backtest.")
    parser.add_argument("--start-cash", type=float, default=100_000.0)
    parser.add_argument("--contracts", type=int, default=1000)
    parser.add_argument("--long-delta", type=float, default=0.70)
    parser.add_argument("--short-premium", type=float, default=550.0)
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def load_inputs() -> tuple[PriceBookDelta, pd.DataFrame]:
    """Build the delta price book and load the futures candles (date axis)."""
    options_df = pd.read_parquet(config.OPTIONS_DAILY_DELTA_PARQUET)
    futures_df = indicators.load_daily()
    return PriceBookDelta(options_df, futures_df), futures_df


def run(args: argparse.Namespace) -> int:
    """Run the double-diagonal backtest end-to-end and save equity + trades."""
    config.ensure_dirs()
    book, futures_df = load_inputs()
    params = DoubleParams(start_cash=args.start_cash, contracts=args.contracts,
                          long_delta_target=args.long_delta, short_premium_target=args.short_premium)
    engine = DoubleEngine(book, params, futures_df.index)
    out = engine.run()

    out["equity"].to_parquet(config.EQUITY_DOUBLE_PARQUET)
    out["trades"].to_csv(config.TRADES_DOUBLE_CSV, index=False)
    final_eq = out["equity"]["equity"].iloc[-1]
    logger.info("Double backtest done: final equity %.2f (start %.0f), %d trade events",
                final_eq, params.start_cash, len(out["trades"]))
    return EXIT_SUCCESS


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
