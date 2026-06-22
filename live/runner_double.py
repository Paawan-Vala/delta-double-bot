#!/usr/bin/env python3
"""Live double-diagonal (PMCC + PMCP) runner — one decision cycle, 4 legs, non-directional.

Each run: pull the live chain, reconcile the saved 4-leg position, heal any vanished leg,
then roll the daily shorts (near expiry) and the monthly longs (near expiry). Always-on:
when flat it opens the full structure; it never closes on a signal (there is no signal).

Defaults match ``double_diagonal_ideal_settings.md`` + the user's live choices:
account 2 (demo), 1 contract/leg, 3x leverage, cross margin, next-day shorts (DTE 1).

Safety:
* **Dry-run unless ``--execute``** (logs intended orders, places none).
* **Refuses production** unless ``--allow-prod``.
* **``--max-contracts``** hard-caps order size.

Usage:
    python -m live.runner_double                 # dry-run, one cycle (account 2)
    python -m live.runner_double --execute        # place orders on testnet
    python -m live.runner_double --close --execute   # flatten all four legs
"""
from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from live.config import load_credentials
from live.delta_data import DeltaData
from live.executor import Executor
from live.state import LegState
from live.state_double import (
    SLOT_SIDE, SLOTS, DoublePositionState, load_double_state, reconcile_double, save_double_state,
)
from live.strategy_double_live import DoubleLiveParams, select_four_legs

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


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


def _place(executor: Executor, row: pd.Series, side: int, contracts: int, reduce_only: bool = False) -> None:
    """Buy when side>0, sell when side<0 (or the reverse for reduce_only closes)."""
    if side > 0:
        executor.buy(row, contracts, reduce_only=reduce_only)
    else:
        executor.sell(row, contracts, reduce_only=reduce_only)


def _open_all(executor: Executor, targets: dict, params: DoubleLiveParams) -> DoublePositionState:
    """Open all four legs (buy the two longs, sell the two shorts)."""
    logger.info("OPEN double: LC %s | SC %s | LP %s | SP %s",
                targets["long_call"]["symbol"], targets["short_call"]["symbol"],
                targets["long_put"]["symbol"], targets["short_put"]["symbol"])
    for slot in SLOTS:
        _place(executor, targets[slot], SLOT_SIDE[slot], params.contracts)
    return DoublePositionState(
        contracts=params.contracts, open_date=_today_iso(),
        long_call=_leg_state(targets["long_call"], +1), short_call=_leg_state(targets["short_call"], -1),
        long_put=_leg_state(targets["long_put"], +1), short_put=_leg_state(targets["short_put"], -1),
    )


def _close_all(executor: Executor, pos: DoublePositionState, chain: pd.DataFrame) -> None:
    """Flatten all four legs with reduce-only orders (sell longs, buy back shorts)."""
    for slot in SLOTS:
        leg = getattr(pos, slot)
        row = _leg_row(chain, leg.symbol)
        if row is None:
            logger.warning("%s %s not on chain (settled?) — skipping close order", slot, leg.symbol)
            continue
        _place(executor, row, -SLOT_SIDE[slot], pos.contracts, reduce_only=True)


def _roll(executor: Executor, pos: DoublePositionState, chain: pd.DataFrame,
          targets: dict, slot: str) -> None:
    """Close the old leg in ``slot`` and open the freshly selected replacement."""
    leg = getattr(pos, slot)
    side = SLOT_SIDE[slot]
    new_row = targets[slot]
    logger.info("ROLL %s: %s -> %s", slot, leg.symbol, new_row["symbol"])
    old = _leg_row(chain, leg.symbol)
    if old is not None:
        _place(executor, old, -side, pos.contracts, reduce_only=True)
    _place(executor, new_row, side, pos.contracts)
    setattr(pos, slot, _leg_state(new_row, side))
    pos.rolls += 1


def _repair(executor: Executor, pos: DoublePositionState, targets: dict,
            sizes: dict[str, int | None], execute: bool) -> tuple[DoublePositionState | None, bool]:
    """Re-establish any leg that vanished on the exchange (settled / closed externally).

    Returns ``(pos, repaired)``. If all four are gone, resets to flat and returns
    ``(None, False)``. Legs reading None (API error) are left untouched.
    """
    known = [v for v in sizes.values() if v is not None]
    if len(known) == 4 and all(v == 0 for v in known):
        logger.warning("All four legs missing on exchange — resetting to flat.")
        if execute:
            save_double_state(None)
        return None, False

    repaired = False
    for slot in SLOTS:
        if sizes.get(slot) == 0:
            row = targets[slot]
            logger.warning("%s missing — re-establishing %s.", slot, row["symbol"])
            _place(executor, row, SLOT_SIDE[slot], pos.contracts)
            setattr(pos, slot, _leg_state(row, SLOT_SIDE[slot]))
            repaired = True
    if repaired and execute:
        save_double_state(pos)
    return pos, repaired


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Live double-diagonal (PMCC+PMCP) decision cycle.")
    parser.add_argument("--execute", action="store_true", help="Actually place orders (default: dry-run).")
    parser.add_argument("--close", action="store_true", help="Flatten all four legs and exit.")
    parser.add_argument("--contracts", type=int, default=1, help="Contracts per leg (1 = 0.001 BTC).")
    parser.add_argument("--max-contracts", type=int, default=10, help="Hard cap on any single order size.")
    parser.add_argument("--leverage", type=int, default=3, help="Leverage per leg (default 3x).")
    parser.add_argument("--margin-mode", default="cross", choices=["cross", "isolated", "portfolio", "none"],
                        help="Account margin mode set before trading (default cross).")
    parser.add_argument("--short-dte-min", type=int, default=1, help="Min DTE for the daily shorts.")
    parser.add_argument("--short-dte-max", type=int, default=1, help="Max DTE for the daily shorts.")
    parser.add_argument("--long-delta", type=float, default=0.70, help="|delta| target for the long ITM legs.")
    parser.add_argument("--short-premium", type=float, default=550.0, help="USD/BTC premium target for shorts.")
    parser.add_argument("--account", default="second", choices=["first", "second"],
                        help="Which .ENV credential set to use (default second = demo).")
    parser.add_argument("--allow-prod", action="store_true", help="Permit running against production.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run_cycle_double(*, execute: bool, contracts: int, max_contracts: int, allow_prod: bool,
                     close: bool = False, leverage: int = 3, margin_mode: str | None = "cross",
                     short_dte_min: int = 1, short_dte_max: int = 1, long_delta: float = 0.70,
                     short_premium: float = 550.0, account: str = "second") -> int:
    """Execute one 4-leg decision cycle (open / repair / roll / close). Reused by the scheduler."""
    creds = load_credentials(account=account)
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
    params = DoubleLiveParams(contracts=contracts, short_dte_min=short_dte_min, short_dte_max=short_dte_max,
                              long_delta_target=long_delta, short_premium_target=short_premium)

    spot = data.perp_mark()
    chain = data.option_chain()
    pos = load_double_state()

    logger.info("MODE: %s | venue: %s | acct: %s | spot: %.1f | contracts: %d | lev: %dx %s",
                "LIVE EXECUTION" if execute else "DRY-RUN (no orders)",
                "TESTNET" if creds.is_testnet else "PRODUCTION", account, spot, contracts,
                leverage, margin_mode or "default")

    targets = select_four_legs(chain, params)

    # --- manual close --------------------------------------------------------
    if close:
        if pos is not None:
            _close_all(executor, pos, chain)
            if execute:
                save_double_state(None)
            logger.info("Double position closed (manual).")
        else:
            logger.info("Already flat — nothing to close.")
        return EXIT_SUCCESS

    # --- flat -> open all four ----------------------------------------------
    if pos is None:
        if targets is None:
            logger.warning("Chain can't supply all four legs right now — staying flat.")
            return EXIT_SUCCESS
        pos = _open_all(executor, targets, params)
        if execute:
            save_double_state(pos)
        logger.info("Opened 4-leg double position.")
        return EXIT_SUCCESS

    # --- held: reconcile, repair, roll --------------------------------------
    sizes = reconcile_double(client, pos)
    if targets is not None:
        pos, repaired = _repair(executor, pos, targets, sizes, execute)
        if pos is None:
            return EXIT_SUCCESS
        if repaired:
            logger.info("Leg(s) re-established this cycle; skipping rolls until next cycle.")
            return EXIT_SUCCESS

    acted = False
    if targets is not None:
        for slot in ("short_call", "short_put"):
            if _dte(getattr(pos, slot).expiry) < params.short_dte_min:
                _roll(executor, pos, chain, targets, slot)
                acted = True
        for slot in ("long_call", "long_put"):
            if _dte(getattr(pos, slot).expiry) < params.long_roll_min_dte:
                _roll(executor, pos, chain, targets, slot)
                acted = True
    else:
        logger.warning("Chain incomplete this cycle — holding without rolling.")

    if acted:
        if execute:
            save_double_state(pos)
        logger.info("Double position managed (rolls=%d).", pos.rolls)
    else:
        logger.info("Holding 4 legs | DTE  sc=%d sp=%d lc=%d lp=%d | no action.",
                    _dte(pos.short_call.expiry), _dte(pos.short_put.expiry),
                    _dte(pos.long_call.expiry), _dte(pos.long_put.expiry))
    return EXIT_SUCCESS


def run(args: argparse.Namespace) -> int:
    """Execute one decision cycle from CLI args."""
    mode = None if args.margin_mode == "none" else args.margin_mode
    return run_cycle_double(
        execute=args.execute, contracts=args.contracts, max_contracts=args.max_contracts,
        allow_prod=args.allow_prod, close=args.close, leverage=args.leverage, margin_mode=mode,
        short_dte_min=args.short_dte_min, short_dte_max=args.short_dte_max,
        long_delta=args.long_delta, short_premium=args.short_premium, account=args.account,
    )


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
