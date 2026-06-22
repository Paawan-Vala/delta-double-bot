#!/usr/bin/env python3
"""Live selection for the double-diagonal (PMCC + PMCP) strategy.

Non-directional: it always targets FOUR legs at once on the live chain —

* long  ITM call  (by |delta| target)   + short daily call (by traded premium)
* long  ITM put   (by |delta| target)   + short daily put  (by traded premium)

There is no signal: every cycle it picks the best four legs from the current chain.
Pure data -> target; it never touches the exchange.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class DoubleLiveParams:
    """Live double-diagonal parameters (testnet-safe defaults)."""

    long_delta_target: float = 0.70
    short_premium_target: float = 550.0      # USD per BTC
    short_dte_min: int = 1
    short_dte_max: int = 1                    # next-day-expiry shorts
    long_dte_min: int = 21
    long_dte_max: int = 45
    long_dte_target: int = 30
    long_roll_min_dte: int = 7
    contracts: int = 1                        # 1 contract = 0.001 BTC


def _select_diagonal(chain: pd.DataFrame, option_type: str,
                     params: DoubleLiveParams) -> tuple[pd.Series, pd.Series] | None:
    """Pick (long-by-delta, short-by-premium) for one option type ('C' or 'P')."""
    tradable = chain[(chain["option_type"] == option_type)
                     & (chain["state"] == "live") & chain["mark"].notna()]
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

    return long_row, short_row


def select_four_legs(chain: pd.DataFrame, params: DoubleLiveParams) -> dict | None:
    """Return the four target legs, or None if the chain can't supply all four."""
    call = _select_diagonal(chain, "C", params)
    put = _select_diagonal(chain, "P", params)
    if call is None or put is None:
        return None
    return {
        "long_call": call[0], "short_call": call[1],
        "long_put": put[0], "short_put": put[1],
    }
