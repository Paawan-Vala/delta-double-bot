#!/usr/bin/env python3
"""Persisted position state + exchange reconciliation for the live bot.

The bot keeps one position at a time. Its legs are saved to ``live/state/position.json``
so a restart resumes correctly. ``reconcile`` compares the saved legs against the actual
exchange positions and warns on any mismatch (it never silently trades to "fix" things).
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

STATE_DIR = Path(__file__).resolve().parent / "state"
STATE_FILE = STATE_DIR / "position.json"


@dataclass
class LegState:
    """One option leg of the live position."""

    symbol: str
    product_id: int
    strike: float
    expiry: str          # ISO date
    side: int            # +1 long (bought), -1 short (sold)
    entry_price: float
    entry_date: str


@dataclass
class PositionState:
    """The live PMCC/PMCP position (one long + one short)."""

    direction: str       # "bull" (PMCC) or "bear" (PMCP)
    contracts: int
    open_date: str
    long: LegState
    short: LegState
    rolls: int = 0


def save_state(pos: PositionState | None, path: Path = STATE_FILE) -> None:
    """Persist the position (or remove the file when flat)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if pos is None:
        path.unlink(missing_ok=True)
        return
    path.write_text(json.dumps(asdict(pos), indent=2), encoding="utf-8")


def load_state(path: Path = STATE_FILE) -> PositionState | None:
    """Load the persisted position, or None if flat."""
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    data["long"] = LegState(**data["long"])
    data["short"] = LegState(**data["short"])
    return PositionState(**data)


def reconcile(client: Any, pos: PositionState | None) -> dict[str, int | None]:
    """Compare saved legs against live exchange positions.

    Returns ``{"long": size, "short": size}`` where size is the exchange position size
    (0 = leg missing) or None if it could not be read. Empty dict when flat.
    """
    sizes: dict[str, int | None] = {}
    if pos is None:
        logger.info("Reconcile: no saved position (flat).")
        return sizes
    for name, leg in (("long", pos.long), ("short", pos.short)):
        try:
            live = client.get_position(leg.product_id)
            result = live.get("result", live) if isinstance(live, dict) else {}
            size = int(result.get("size") or 0)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Reconcile: could not read %s leg %s: %s", name, leg.symbol, exc)
            sizes[name] = None
            continue
        sizes[name] = size
        if size == 0:
            logger.warning("Reconcile MISMATCH: %s leg %s shows 0 on exchange (expected %+d x %d).",
                           name, leg.symbol, leg.side, pos.contracts)
        else:
            logger.info("Reconcile OK: %s leg %s exchange size=%d.", name, leg.symbol, size)
    return sizes
