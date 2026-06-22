#!/usr/bin/env python3
"""Persisted state + reconciliation for the 4-leg double-diagonal bot.

Holds one always-on position with four legs. Saved to ``live/state/double_position.json``
(separate from the single-diagonal bot's ``position.json``) so the two bots never collide.
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from live.state import LegState

logger = logging.getLogger(__name__)

STATE_DIR = Path(__file__).resolve().parent / "state"
STATE_FILE = STATE_DIR / "double_position.json"

SLOTS = ("long_call", "short_call", "long_put", "short_put")
SLOT_SIDE = {"long_call": +1, "short_call": -1, "long_put": +1, "short_put": -1}


@dataclass
class DoublePositionState:
    """The live 4-leg double-diagonal position."""

    contracts: int
    open_date: str
    long_call: LegState
    short_call: LegState
    long_put: LegState
    short_put: LegState
    rolls: int = 0


def save_double_state(pos: DoublePositionState | None, path: Path = STATE_FILE) -> None:
    """Persist the 4-leg position (or remove the file when flat)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if pos is None:
        path.unlink(missing_ok=True)
        return
    path.write_text(json.dumps(asdict(pos), indent=2), encoding="utf-8")


def load_double_state(path: Path = STATE_FILE) -> DoublePositionState | None:
    """Load the persisted 4-leg position, or None if flat."""
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    for slot in SLOTS:
        data[slot] = LegState(**data[slot])
    return DoublePositionState(**data)


def reconcile_double(client: Any, pos: DoublePositionState | None) -> dict[str, int | None]:
    """Compare the four saved legs against live exchange positions.

    Returns ``{slot: size}`` where size is the exchange position size (0 = missing) or
    None if it could not be read. Empty dict when flat.
    """
    sizes: dict[str, int | None] = {}
    if pos is None:
        logger.info("Reconcile: no saved double position (flat).")
        return sizes
    for slot in SLOTS:
        leg = getattr(pos, slot)
        try:
            live = client.get_position(leg.product_id)
            result = live.get("result", live) if isinstance(live, dict) else {}
            size = int(result.get("size") or 0)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Reconcile: could not read %s %s: %s", slot, leg.symbol, exc)
            sizes[slot] = None
            continue
        sizes[slot] = size
        if size == 0:
            logger.warning("Reconcile MISMATCH: %s %s shows 0 on exchange (expected %+d x %d).",
                           slot, leg.symbol, leg.side, pos.contracts)
        else:
            logger.info("Reconcile OK: %s %s exchange size=%d.", slot, leg.symbol, size)
    return sizes
