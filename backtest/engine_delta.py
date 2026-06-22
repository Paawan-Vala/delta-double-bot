#!/usr/bin/env python3
"""Phase B (delta variant) — PMCC/PMCP engine with delta/premium leg selection.

``DeltaEngine`` subclasses the original ``BacktestEngine`` and overrides only the
three methods that *select* instruments (``_open``, ``_roll_short``, ``_roll_long``).
Everything else — fills, mark-to-market, the daily event loop, closing logic — is
inherited unchanged, so the original engine is left untouched.

* Long monthly leg: chosen by |delta| target (ITM).
* Short daily leg: chosen by traded-premium target (USD per BTC).

Usage:
    python -m backtest.engine_delta
    python -m backtest.engine_delta -v
"""
from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from backtest import config, indicators
from backtest.engine import BacktestEngine
from backtest.strategy import Position
from backtest.strategy_delta import PriceBookDelta, StrategyParamsDelta

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class DeltaEngine(BacktestEngine):
    """PMCC/PMCP backtester that selects the long leg by delta and the short by premium."""

    book: PriceBookDelta
    p: StrategyParamsDelta

    def _open(self, direction: str, date: pd.Timestamp) -> bool:
        is_call = direction == "bull"           # PMCC uses calls, PMCP uses puts
        long_sym = self.book.select_by_delta(
            date, is_call, self.p.long_dte_min, self.p.long_dte_max,
            self.p.long_delta_target, self.p.long_dte_target,
        )
        short_sym = self.book.select_by_premium(
            date, is_call, self.p.short_dte_min, self.p.short_dte_max, self.p.short_premium_target
        )
        if not long_sym or not short_sym:
            return False

        self._pos_cashflow = 0.0
        long_leg = self._make_leg(date, long_sym, side=+1)
        short_leg = self._make_leg(date, short_sym, side=-1)
        self.position = Position(direction, date, long_leg, short_leg)
        self.trades.append({
            "event": "open", "date": date, "direction": direction,
            "long": long_sym, "short": short_sym,
            "long_price": long_leg.entry_price, "short_price": short_leg.entry_price,
            "long_delta": self.book.delta(date, long_sym),
            "short_delta": self.book.delta(date, short_sym),
            "cash": self.cash,
        })
        return True

    def _roll_short(self, date: pd.Timestamp) -> None:
        pos = self.position
        assert pos is not None
        self._close_leg(date, pos.short_leg)
        is_call = pos.direction == "bull"
        new_sym = self.book.select_by_premium(
            date, is_call, self.p.short_dte_min, self.p.short_dte_max, self.p.short_premium_target
        )
        if not new_sym:
            return
        pos.short_leg = self._make_leg(date, new_sym, side=-1)
        pos.rolls += 1
        self.trades.append({"event": "roll_short", "date": date, "short": new_sym,
                            "short_price": pos.short_leg.entry_price,
                            "short_delta": self.book.delta(date, new_sym), "cash": self.cash})

    def _roll_long(self, date: pd.Timestamp) -> None:
        pos = self.position
        assert pos is not None
        self._close_leg(date, pos.long_leg)
        is_call = pos.direction == "bull"
        new_sym = self.book.select_by_delta(
            date, is_call, self.p.long_dte_min, self.p.long_dte_max,
            self.p.long_delta_target, self.p.long_dte_target,
        )
        if not new_sym:
            self.position = None
            return
        pos.long_leg = self._make_leg(date, new_sym, side=+1)
        self.trades.append({"event": "roll_long", "date": date, "long": new_sym,
                            "long_price": pos.long_leg.entry_price,
                            "long_delta": self.book.delta(date, new_sym), "cash": self.cash})


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run the delta/premium PMCC/PMCP backtest.")
    parser.add_argument("--start-cash", type=float, default=100_000.0)
    parser.add_argument("--contracts", type=int, default=1000)
    parser.add_argument("--long-delta", type=float, default=config.LONG_DELTA_TARGET)
    parser.add_argument("--short-premium", type=float, default=config.SHORT_PREMIUM_TARGET)
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def load_inputs() -> tuple[pd.DataFrame, PriceBookDelta]:
    """Load the direction signal and build the delta price book from processed parquet."""
    direction = indicators.compute_direction(indicators.load_daily())
    options_df = pd.read_parquet(config.OPTIONS_DAILY_DELTA_PARQUET)
    futures_df = indicators.load_daily()
    book = PriceBookDelta(options_df, futures_df)
    return direction, book


def run(args: argparse.Namespace) -> int:
    """Run the delta/premium backtest end-to-end and save equity + trades."""
    config.ensure_dirs()
    direction, book = load_inputs()
    params = StrategyParamsDelta(
        start_cash=args.start_cash, contracts=args.contracts,
        long_delta_target=args.long_delta, short_premium_target=args.short_premium,
    )
    engine = DeltaEngine(direction, book, params)
    out = engine.run()

    out["equity"].to_parquet(config.EQUITY_DELTA_PARQUET)
    out["trades"].to_csv(config.TRADES_DELTA_CSV, index=False)
    n_closed = int((out["trades"]["event"] == "close").sum()) if not out["trades"].empty else 0
    final_eq = out["equity"]["equity"].iloc[-1]
    logger.info("Delta backtest done: %d closed trades, final equity %.2f (start %.0f)",
                n_closed, final_eq, params.start_cash)
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
