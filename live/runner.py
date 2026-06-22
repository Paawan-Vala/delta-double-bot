#!/usr/bin/env python3
"""Live PMCC/PMCP runner — one decision cycle for the Delta+premium strategy.

Each run: pull the signal + chain, reconcile the saved position, and take the one
required action (open / roll-short / roll-long / close). Safe by default:

* **Dry-run unless ``--execute``** is passed (logs intended orders, places none).
* **Refuses production** unless ``--allow-prod`` (your keys are testnet, so this is moot).
* **``--max-contracts``** hard-caps order size.

Usage:
    python -m live.runner                 # dry-run, one cycle
    python -m live.runner --execute       # place orders on testnet
    python -m live.runner --close --execute   # flatten the position
"""
from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from live.config import load_credentials
from live.delta_data import DeltaData
from live.executor import Executor
from live.state import LegState, PositionState, load_state, reconcile, save_state
from live.strategy_live import LiveParams, current_signal, select_legs

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
LONG_ROLL_MIN_DTE = 7


def _today_iso() -> str:
    return pd.Timestamp.now(tz="UTC").tz_convert(None).date().isoformat()


def _dte(expiry_iso: str) -> int:
    today = pd.Timestamp.now(tz="UTC").tz_convert(None).normalize()
    return int((pd.Timestamp(expiry_iso).normalize() - today).days)


def _leg_row(chain: pd.DataFrame, symbol: str) -> pd.Series | None:
    match = chain[chain["symbol"] == symbol]
    return match.iloc[0] if not match.empty else None


def _leg_state(row: pd.Series, side: int) -> LegState:
    return LegState(
        symbol=str(row["symbol"]), product_id=int(row["product_id"]), strike=float(row["strike"]),
        expiry=pd.Timestamp(row["expiry"]).date().isoformat(), side=side,
        entry_price=float(row["mark"]), entry_date=_today_iso(),
    )


def _open(executor: Executor, direction: str, legs: dict, params: LiveParams) -> PositionState:
    """Buy the long leg and sell the short leg; return the new position state."""
    long_row, short_row = legs["long"], legs["short"]
    logger.info("OPEN %s: long %s / short %s", "PMCC" if direction == "bull" else "PMCP",
                long_row["symbol"], short_row["symbol"])
    executor.buy(long_row, params.contracts)
    executor.sell(short_row, params.contracts)
    return PositionState(
        direction=direction, contracts=params.contracts, open_date=_today_iso(),
        long=_leg_state(long_row, +1), short=_leg_state(short_row, -1),
    )


def _close(executor: Executor, pos: PositionState, chain: pd.DataFrame, reason: str) -> None:
    """Close both legs (sell the long, buy back the short) with reduce-only orders."""
    logger.info("CLOSE (%s): %s + %s", reason, pos.long.symbol, pos.short.symbol)
    long_row = _leg_row(chain, pos.long.symbol)
    short_row = _leg_row(chain, pos.short.symbol)
    if long_row is not None:
        executor.sell(long_row, pos.contracts, reduce_only=True)
    else:
        logger.warning("long leg %s not on chain (settled?) — skipping close order", pos.long.symbol)
    if short_row is not None:
        executor.buy(short_row, pos.contracts, reduce_only=True)
    else:
        logger.warning("short leg %s not on chain (settled?) — skipping close order", pos.short.symbol)


def _roll_short(executor: Executor, pos: PositionState, chain: pd.DataFrame, legs: dict) -> None:
    """Buy back the expiring short and sell a fresh premium-target short."""
    old = _leg_row(chain, pos.short.symbol)
    new_row = legs["short"]
    logger.info("ROLL SHORT: %s -> %s", pos.short.symbol, new_row["symbol"])
    if old is not None:
        executor.buy(old, pos.contracts, reduce_only=True)
    executor.sell(new_row, pos.contracts)
    pos.short = _leg_state(new_row, -1)
    pos.rolls += 1


def _roll_long(executor: Executor, pos: PositionState, chain: pd.DataFrame, legs: dict) -> None:
    """Sell the near-expiry long and buy a fresh delta-target long."""
    old = _leg_row(chain, pos.long.symbol)
    new_row = legs["long"]
    logger.info("ROLL LONG: %s -> %s", pos.long.symbol, new_row["symbol"])
    if old is not None:
        executor.sell(old, pos.contracts, reduce_only=True)
    executor.buy(new_row, pos.contracts)
    pos.long = _leg_state(new_row, +1)


def _repair(executor: Executor, pos: PositionState, legs: dict,
            sizes: dict[str, int | None], execute: bool) -> tuple[PositionState | None, bool]:
    """Heal the position if a leg vanished on the exchange (settled / closed externally).

    Returns ``(pos, reestablished)``. ``reestablished`` is True when a single leg was
    re-opened (caller should then skip rolls this cycle). If BOTH legs are gone, resets to
    flat and returns ``(None, False)``. Legs reading None (API error) are left untouched.
    """
    long_size, short_size = sizes.get("long"), sizes.get("short")
    if long_size == 0 and short_size == 0:
        logger.warning("Both legs missing on exchange — resetting to flat.")
        if execute:
            save_state(None)
        return None, False
    if short_size == 0:
        new_row = legs["short"]
        logger.warning("Short leg missing — re-establishing short %s.", new_row["symbol"])
        executor.sell(new_row, pos.contracts)
        pos.short = _leg_state(new_row, -1)
        if execute:
            save_state(pos)
        return pos, True
    if long_size == 0:
        new_row = legs["long"]
        logger.warning("Long leg missing — re-establishing long %s.", new_row["symbol"])
        executor.buy(new_row, pos.contracts)
        pos.long = _leg_state(new_row, +1)
        if execute:
            save_state(pos)
        return pos, True
    return pos, False


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Live PMCC/PMCP (Delta+premium) decision cycle.")
    parser.add_argument("--execute", action="store_true", help="Actually place orders (default: dry-run).")
    parser.add_argument("--close", action="store_true", help="Flatten the open position and exit.")
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


def run_cycle(*, execute: bool, contracts: int, max_contracts: int,
              allow_prod: bool, close: bool = False,
              leverage: int = 1, margin_mode: str | None = "cross") -> int:
    """Execute one decision cycle (open / roll / close). Reused by the scheduler."""
    creds = load_credentials()
    if not creds.is_testnet and not allow_prod:
        logger.error("Refusing to run on PRODUCTION (%s) without --allow-prod.", creds.base_url)
        return EXIT_FAILURE
    if contracts > max_contracts:
        logger.error("contracts %d exceeds --max-contracts %d.", contracts, max_contracts)
        return EXIT_FAILURE

    from delta_rest_client import DeltaRestClient

    data = DeltaData(trade_base_url=creds.base_url)
    client = DeltaRestClient(base_url=creds.base_url, api_key=creds.api_key, api_secret=creds.api_secret)
    executor = Executor(client, dry_run=not execute, max_contracts=max_contracts,
                        leverage=leverage, margin_mode=margin_mode)
    params = LiveParams(contracts=contracts)

    direction, last = current_signal(data.daily_candles())
    spot = data.perp_mark()
    chain = data.option_chain()
    pos = load_state()

    logger.info("MODE: %s | venue: %s | signal: %s | spot: %.1f | contracts: %d",
                "LIVE EXECUTION" if execute else "DRY-RUN (no orders)",
                "TESTNET" if creds.is_testnet else "PRODUCTION", direction.upper(), spot, contracts)
    reconcile_sizes = reconcile(client, pos)

    legs = select_legs(direction if direction in ("bull", "bear") else (pos.direction if pos else "none"),
                       chain, params) if (pos or direction in ("bull", "bear")) else None

    repaired_leg = False
    if pos is not None and direction == pos.direction and legs is not None:
        pos, repaired_leg = _repair(executor, pos, legs, reconcile_sizes, execute)

    if pos is not None:
        if close or direction != pos.direction:
            reason = "manual-close" if close else ("flip" if direction in ("bull", "bear") else "exit")
            _close(executor, pos, chain, reason)
            if execute:
                save_state(None)
            logger.info("Position closed (%s).", reason)
            return EXIT_SUCCESS

        if repaired_leg:
            logger.info("Leg re-established this cycle; skipping rolls until next cycle.")
            return EXIT_SUCCESS

        acted = False
        if legs is not None:
            if _dte(pos.short.expiry) <= params.short_dte_min:
                _roll_short(executor, pos, chain, legs)
                acted = True
            if _dte(pos.long.expiry) < LONG_ROLL_MIN_DTE:
                _roll_long(executor, pos, chain, legs)
                acted = True
        if acted:
            if execute:
                save_state(pos)
            logger.info("Position managed (rolls=%d).", pos.rolls)
        else:
            logger.info("Holding %s position; short DTE=%d, long DTE=%d; no action.",
                        pos.direction, _dte(pos.short.expiry), _dte(pos.long.expiry))
        return EXIT_SUCCESS

    # Flat
    if direction in ("bull", "bear") and legs is not None:
        new_pos = _open(executor, direction, legs, params)
        if execute:
            save_state(new_pos)
        logger.info("Opened %s position.", direction)
    elif direction in ("bull", "bear"):
        logger.warning("Signal %s but no legs matched the chain filters — staying flat.", direction)
    else:
        logger.info("Flat and signal is 'none' — nothing to do.")
    return EXIT_SUCCESS


def run(args: argparse.Namespace) -> int:
    """Execute one decision cycle from CLI args."""
    mode = None if args.margin_mode == "none" else args.margin_mode
    return run_cycle(execute=args.execute, contracts=args.contracts,
                     max_contracts=args.max_contracts, allow_prod=args.allow_prod, close=args.close,
                     leverage=args.leverage, margin_mode=mode)


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
