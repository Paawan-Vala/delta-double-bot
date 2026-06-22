#!/usr/bin/env python3
"""Hourly scheduler for the live PMCC/PMCP bot.

Runs one decision cycle every ``--interval`` seconds (default 3600 = 1 hour). Each cycle
reports the current position, then: manages it (roll/close) if held, or opens one if flat
and the signal is actionable. A failure in one cycle is logged and the loop continues.

Safe by default: cycles are DRY-RUN unless ``--execute`` is passed.

Usage:
    python -m live.scheduler                      # hourly, dry-run (no orders)
    python -m live.scheduler --execute            # hourly, places orders on testnet
    python -m live.scheduler --execute --interval 1800   # every 30 min
    python -m live.scheduler --execute --iterations 1    # one cycle then exit (for Task Scheduler)
"""
from __future__ import annotations

import argparse
import logging
import sys
import time

from live.runner import run_cycle

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Hourly scheduler for the live PMCC/PMCP bot.")
    parser.add_argument("--interval", type=int, default=3600, help="Seconds between cycles (default 3600 = 1h).")
    parser.add_argument("--iterations", type=int, default=0, help="Number of cycles (0 = run forever).")
    parser.add_argument("--execute", action="store_true", help="Place orders (default: dry-run).")
    parser.add_argument("--contracts", type=int, default=1, help="Contracts per leg (1 = 0.001 BTC).")
    parser.add_argument("--max-contracts", type=int, default=10, help="Hard cap on any single order size.")
    parser.add_argument("--leverage", type=int, default=1, help="Leverage per leg (low = safer; default 1x).")
    parser.add_argument("--margin-mode", default="cross", choices=["cross", "isolated", "portfolio", "none"],
                        help="Account margin mode set before trading (default cross).")
    parser.add_argument("--allow-prod", action="store_true", help="Permit running against production.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run(args: argparse.Namespace) -> int:
    """Run decision cycles on a fixed interval until stopped or iteration cap reached."""
    logger.info("Scheduler start: interval=%ds, mode=%s, iterations=%s",
                args.interval, "EXECUTE" if args.execute else "DRY-RUN",
                "forever" if args.iterations == 0 else args.iterations)
    cycle = 0
    while True:
        cycle += 1
        logger.info("================ CYCLE %d ================", cycle)
        try:
            mode = None if args.margin_mode == "none" else args.margin_mode
            run_cycle(execute=args.execute, contracts=args.contracts,
                      max_contracts=args.max_contracts, allow_prod=args.allow_prod,
                      leverage=args.leverage, margin_mode=mode)
        except Exception as exc:  # noqa: BLE001 - keep the loop alive across transient failures
            logger.exception("Cycle %d failed (continuing): %s", cycle, exc)

        if args.iterations and cycle >= args.iterations:
            logger.info("Reached iteration cap (%d). Stopping.", args.iterations)
            return EXIT_SUCCESS
        logger.info("Sleeping %ds until next cycle…", args.interval)
        time.sleep(args.interval)


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
