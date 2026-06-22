#!/usr/bin/env python3
"""Read-only preview: today's signal and the exact two legs Delta+premium WOULD trade.

Places NO orders. Run this to confirm the live data + selection look right before
enabling execution.

Usage:
    python -m live.preview
    python -m live.preview -v
"""
from __future__ import annotations

import argparse
import logging
import sys

from live.config import load_credentials
from live.delta_data import DeltaData
from live.strategy_live import LiveParams, current_signal, leg_cash, select_legs

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Preview today's signal and target legs (no orders).")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def _fmt_leg(name: str, row, contracts: int) -> str:
    return (f"  {name}: {row['symbol']}  strike={row['strike']:.0f}  dte={row['dte']}  "
            f"delta={row['delta']:+.3f}  mark=${row['mark']:.2f}/BTC  "
            f"bid/ask={row['bid']:.0f}/{row['ask']:.0f}  est_cash=${leg_cash(row, contracts):.2f}")


def run() -> int:
    """Fetch data, compute the signal, and print the target legs."""
    creds = load_credentials()
    data = DeltaData(trade_base_url=creds.base_url)
    params = LiveParams()

    candles = data.daily_candles(days=400)
    logger.info("Signal candles: %d daily bars (%s -> %s)",
                len(candles), candles.index.min().date(), candles.index.max().date())
    if len(candles) < 200:
        logger.warning("Only %d candles (<200): 200-EMA regime not warmed up -> signal will be 'none'.", len(candles))

    direction, last = current_signal(candles)
    logger.info("As of %s: close=%.1f ema20=%.1f ema50=%.1f ema200=%.1f adx=%.1f -> DIRECTION = %s",
                last.name.date(), last["close"], last["ema_fast"], last["ema_slow"],
                last["ema_regime"], last["adx"], direction.upper())

    spot = data.perp_mark()
    chain = data.option_chain()
    logger.info("Testnet spot=%.1f | option chain: %d contracts (%d with delta)",
                spot, len(chain), int(chain["delta"].notna().sum()))

    if direction not in ("bull", "bear"):
        logger.info("No actionable setup today (direction=%s) -> bot would stay flat.", direction)
        return EXIT_SUCCESS

    legs = select_legs(direction, chain, params)
    if not legs:
        logger.warning("Signal is %s but no legs matched the DTE/target filters on the chain.", direction)
        return EXIT_SUCCESS

    strat = "PMCC (calls)" if direction == "bull" else "PMCP (puts)"
    logger.info("TARGET %s position (%d contract(s) = %.3f BTC/leg):",
                strat, params.contracts, params.contracts * 0.001)
    logger.info(_fmt_leg("LONG (buy, ~0.70Δ)", legs["long"], params.contracts))
    logger.info(_fmt_leg("SHORT(sell,~$550)  ", legs["short"], params.contracts))
    net = leg_cash(legs["long"], params.contracts) - leg_cash(legs["short"], params.contracts)
    logger.info("  net debit to open ≈ $%.2f (buy long - sell short)", net)
    logger.info("(preview only — no orders placed)")
    return EXIT_SUCCESS


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
