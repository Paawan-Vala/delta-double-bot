#!/usr/bin/env python3
"""Live decision layer: daily signal + Delta+premium leg selection on the live chain.

Reuses the backtested brain unchanged:

* signal  -> ``backtest.indicators.compute_direction`` (200-EMA regime + 20/50 + ADX + weekly)
* selection-> long monthly leg by |delta| target, short daily leg by traded premium

It does not touch the exchange; it only turns *data* into a *target* (which two legs to hold).
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from backtest import indicators


@dataclass
class LiveParams:
    """Live Delta+premium parameters (small size for testnet by default)."""

    long_delta_target: float = 0.70
    short_premium_target: float = 550.0      # USD per BTC
    short_dte_min: int = 1
    short_dte_max: int = 3
    long_dte_min: int = 21
    long_dte_max: int = 45
    long_dte_target: int = 30
    contracts: int = 1                        # 1 contract = 0.001 BTC (testnet-safe default)


def current_signal(candles: pd.DataFrame) -> tuple[str, pd.Series]:
    """Return (direction, last_row) from the daily candles using the backtest signal."""
    enriched = indicators.compute_direction(candles)
    last = enriched.iloc[-1]
    return str(last["direction"]), last


def select_legs(direction: str, chain: pd.DataFrame, params: LiveParams) -> dict | None:
    """Pick the long (by |delta|) and short (by premium) legs for an actionable signal."""
    if direction not in ("bull", "bear"):
        return None
    typ = "C" if direction == "bull" else "P"
    tradable = chain[(chain["option_type"] == typ) & (chain["state"] == "live") & chain["mark"].notna()]
    if tradable.empty:
        return None

    longs = tradable[(tradable["dte"] >= params.long_dte_min) & (tradable["dte"] <= params.long_dte_max)]
    shorts = tradable[(tradable["dte"] >= params.short_dte_min) & (tradable["dte"] <= params.short_dte_max)]
    if longs.empty or shorts.empty:
        return None

    # Long: expiry nearest the DTE target, then |delta| nearest the target.
    longs = longs.assign(_gap=(longs["dte"] - params.long_dte_target).abs())
    chosen_expiry = longs.sort_values("_gap")["expiry"].iloc[0]
    lcand = longs[longs["expiry"] == chosen_expiry].copy()
    lcand["_dgap"] = (lcand["delta"].abs() - params.long_delta_target).abs()
    long_row = lcand.sort_values("_dgap").iloc[0]

    # Short: traded premium (mark, USD/BTC) nearest the target.
    scand = shorts.copy()
    scand["_pgap"] = (scand["mark"] - params.short_premium_target).abs()
    short_row = scand.sort_values("_pgap").iloc[0]

    return {"long": long_row, "short": short_row}


def leg_cash(row: pd.Series, contracts: int) -> float:
    """USD cash for a leg = mark (USD/BTC) * contract_value (BTC) * contracts."""
    return float(row["mark"]) * float(row["contract_value"]) * contracts
