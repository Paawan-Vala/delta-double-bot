#!/usr/bin/env python3
"""Phase 3b (engine) — PMCC/PMCP diagonal backtest event loop.

Walks the daily direction signal with no look-ahead and manages one position at a
time: open PMCC on a ``bull`` day / PMCP on a ``bear`` day, roll the daily short leg,
roll the monthly long leg as it nears expiry, and close BOTH legs on a flip/exit.

All cash is in USD. An option leg's cash = price(USD/BTC) * LOT_SIZE_BTC * contracts.
Net cash flow over a fully-closed position equals its realized P/L.

Usage:
    python -m backtest.engine            # runs the backtest, writes results parquet/csv
    python -m backtest.engine -v
"""
from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from backtest import config, indicators
from backtest.strategy import Leg, Position, PriceBook, StrategyParams

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
LOT = config.LOT_SIZE_BTC


class BacktestEngine:
    """Stateful PMCC/PMCP backtester."""

    def __init__(self, direction: pd.DataFrame, book: PriceBook, params: StrategyParams) -> None:
        self.direction = direction
        self.book = book
        self.p = params
        self.cash = params.start_cash
        self.position: Position | None = None
        self._pos_cashflow = 0.0
        self.trades: list[dict] = []
        self.records: list[dict] = []

    # --- fills ---------------------------------------------------------------
    def _fill(self, price: float, contracts: int, buy: bool) -> float:
        """Apply slippage + fee, mutate cash, return the signed cash delta."""
        eff = price * (1 + self.p.slippage) if buy else price * (1 - self.p.slippage)
        gross = eff * LOT * contracts
        fee = self.p.taker_fee * abs(price) * LOT * contracts
        delta = (-gross - fee) if buy else (gross - fee)
        self.cash += delta
        self._pos_cashflow += delta
        return delta

    # --- leg helpers ---------------------------------------------------------
    def _make_leg(self, date: pd.Timestamp, sym: str, side: int) -> Leg:
        is_call, strike, expiry = self.book.meta(sym)
        price = self.book.price(date, sym, self.p.default_iv)
        self._fill(price, self.p.contracts, buy=(side > 0))
        return Leg(sym, is_call, strike, expiry, self.p.contracts, side, price, date)

    def _close_leg(self, date: pd.Timestamp, leg: Leg) -> float:
        """Close a leg (sell a long / buy back a short); return its leg P/L."""
        price = self.book.price(date, leg.product_symbol, self.p.default_iv)
        # closing a long => sell; closing a short => buy back
        self._fill(price, leg.contracts, buy=(leg.side < 0))
        return (price - leg.entry_price) * leg.side * LOT * leg.contracts

    # --- position lifecycle --------------------------------------------------
    def _open(self, direction: str, date: pd.Timestamp) -> bool:
        is_call = direction == "bull"           # PMCC uses calls, PMCP uses puts
        long_mny = (1 - self.p.long_itm) if is_call else (1 + self.p.long_itm)
        short_mny = (1 + self.p.short_otm) if is_call else (1 - self.p.short_otm)

        long_sym = self.book.select_leg(
            date, is_call, self.p.long_dte_min, self.p.long_dte_max, long_mny, self.p.long_dte_target
        )
        short_sym = self.book.select_leg(
            date, is_call, self.p.short_dte_min, self.p.short_dte_max, short_mny
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
            "cash": self.cash,
        })
        return True

    def _roll_short(self, date: pd.Timestamp) -> None:
        pos = self.position
        assert pos is not None
        self._close_leg(date, pos.short_leg)
        is_call = pos.direction == "bull"
        short_mny = (1 + self.p.short_otm) if is_call else (1 - self.p.short_otm)
        new_sym = self.book.select_leg(date, is_call, self.p.short_dte_min, self.p.short_dte_max, short_mny)
        if not new_sym:
            return
        pos.short_leg = self._make_leg(date, new_sym, side=-1)
        pos.rolls += 1
        self.trades.append({"event": "roll_short", "date": date, "short": new_sym,
                            "short_price": pos.short_leg.entry_price, "cash": self.cash})

    def _roll_long(self, date: pd.Timestamp) -> None:
        pos = self.position
        assert pos is not None
        self._close_leg(date, pos.long_leg)
        is_call = pos.direction == "bull"
        long_mny = (1 - self.p.long_itm) if is_call else (1 + self.p.long_itm)
        new_sym = self.book.select_leg(
            date, is_call, self.p.long_dte_min, self.p.long_dte_max, long_mny, self.p.long_dte_target
        )
        if not new_sym:
            self.position = None
            return
        pos.long_leg = self._make_leg(date, new_sym, side=+1)
        self.trades.append({"event": "roll_long", "date": date, "long": new_sym,
                            "long_price": pos.long_leg.entry_price, "cash": self.cash})

    def _close(self, date: pd.Timestamp, reason: str) -> None:
        pos = self.position
        assert pos is not None
        self._close_leg(date, pos.long_leg)
        self._close_leg(date, pos.short_leg)
        self.trades.append({
            "event": "close", "date": date, "reason": reason, "direction": pos.direction,
            "rolls": pos.rolls, "pnl": self._pos_cashflow, "cash": self.cash,
        })
        self.position = None

    def _mtm(self, date: pd.Timestamp) -> float:
        """Mark-to-market value (USD) of the open position (long − short)."""
        pos = self.position
        if pos is None:
            return 0.0
        lp = self.book.price(date, pos.long_leg.product_symbol, self.p.default_iv)
        sp = self.book.price(date, pos.short_leg.product_symbol, self.p.default_iv)
        return (lp - sp) * LOT * self.p.contracts

    # --- main loop -----------------------------------------------------------
    def run(self) -> dict[str, pd.DataFrame]:
        for date, row in self.direction.iterrows():
            sig = row["direction"]
            # manage open position
            if self.position is not None:
                if sig != self.position.direction:
                    self._close(date, reason=("flip" if sig in ("bull", "bear") else "exit"))
                else:
                    if (self.position.short_leg.expiry - date).days <= 1:
                        self._roll_short(date)
                    if (self.position.long_leg.expiry - date).days < self.p.long_roll_min_dte:
                        self._roll_long(date)
            # open if flat and signal actionable
            if self.position is None and sig in ("bull", "bear"):
                self._open(sig, date)

            pos_val = self._mtm(date)
            self.records.append({
                "date": date, "spot": float(self.book.spot.get(date, float("nan"))),
                "direction": sig, "cash": self.cash, "position_value": pos_val,
                "equity": self.cash + pos_val, "in_position": self.position is not None,
                "pos_direction": self.position.direction if self.position else "",
            })

        # close any dangling position on the last date
        if self.position is not None:
            self._close(self.direction.index[-1], reason="end")

        equity = pd.DataFrame(self.records).set_index("date")
        trades = pd.DataFrame(self.trades)
        return {"equity": equity, "trades": trades}


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run the PMCC/PMCP backtest.")
    parser.add_argument("--start-cash", type=float, default=100_000.0)
    parser.add_argument("--contracts", type=int, default=1000)
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def load_inputs() -> tuple[pd.DataFrame, PriceBook]:
    """Load the direction signal and build the price book from processed parquet."""
    direction = indicators.compute_direction(indicators.load_daily())
    options_df = pd.read_parquet(config.OPTIONS_DAILY_PARQUET)
    futures_df = indicators.load_daily()
    book = PriceBook(options_df, futures_df)
    return direction, book


def run(args: argparse.Namespace) -> int:
    """Run the backtest end-to-end and save equity + trades."""
    config.ensure_dirs()
    direction, book = load_inputs()
    params = StrategyParams(start_cash=args.start_cash, contracts=args.contracts)
    engine = BacktestEngine(direction, book, params)
    out = engine.run()

    out["equity"].to_parquet(config.RESULTS_DIR / "equity.parquet")
    out["trades"].to_csv(config.RESULTS_DIR / "trades.csv", index=False)
    n_closed = int((out["trades"]["event"] == "close").sum()) if not out["trades"].empty else 0
    final_eq = out["equity"]["equity"].iloc[-1]
    logger.info("Backtest done: %d closed trades, final equity %.2f (start %.0f)",
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
