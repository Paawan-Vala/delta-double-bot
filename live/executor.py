#!/usr/bin/env python3
"""Order execution for the live PMCC/PMCP bot.

Atomic primitives only: ``buy`` and ``sell`` a single option leg as an IOC limit order
that crosses the spread (so it fills now or not at all — no resting orders). Composition
(open / roll / close) lives in the runner.

Safety:
* ``dry_run=True`` (default) logs the intended order and places nothing.
* ``max_contracts`` hard-caps the size of any single order.
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_CROSS_SLIPPAGE = 0.02   # if no bid/ask, cross the mark by this fraction


@dataclass
class OrderResult:
    """Outcome of a single leg order."""

    symbol: str
    side: str
    size: int
    limit_price: float
    dry_run: bool
    order_id: int | None = None
    filled_size: int = 0
    status: str = "dry_run"
    raw: dict[str, Any] = field(default_factory=dict)


def round_to_tick(price: float, tick: float) -> float:
    """Round a price to the instrument tick size."""
    if tick <= 0:
        return round(price, 2)
    return round(round(price / tick) * tick, 8)


class Executor:
    """Places single-leg IOC limit orders on Delta Exchange (or simulates them)."""

    def __init__(self, client: Any, dry_run: bool = True, max_contracts: int = 10,
                 leverage: int = 1, margin_mode: str | None = "cross") -> None:
        self.client = client
        self.dry_run = dry_run
        self.max_contracts = max_contracts
        self.leverage = leverage
        self.margin_mode = margin_mode
        self._margin_mode_set = False
        self._user_id: int | None = None

    def _get_user_id(self) -> int | None:
        """Fetch and cache the account user id (required by the margin-mode endpoint)."""
        if self._user_id is None:
            try:
                bals = self.client.get_all_wallet_balances()
                res = bals.get("result", bals) if isinstance(bals, dict) else bals
                if res:
                    self._user_id = int(res[0].get("user_id"))
            except Exception as exc:  # noqa: BLE001
                logger.warning("      could not fetch user id: %s", exc)
        return self._user_id

    def _prepare_margin(self, product_id: int, opening: bool) -> None:
        """Before opening a leg, set low leverage (+ optional cross margin) for a big buffer.

        This is the guard against naked-short liquidation: at low leverage / cross margin a
        1-lot short can't be force-closed by a normal move. Best-effort — failures (e.g. a
        margin-mode change blocked by open positions) are logged, not fatal.
        """
        if not opening:
            return
        if self.dry_run:
            extra = f" + {self.margin_mode} margin" if self.margin_mode else ""
            logger.info("      [DRY] would set leverage=%dx%s on %d", self.leverage, extra, product_id)
            return
        if self.margin_mode and not self._margin_mode_set:
            try:
                self.client.change_margin_mode(self.margin_mode, subaccount_user_id=self._get_user_id())
                logger.info("      account margin mode -> %s", self.margin_mode)
            except Exception as exc:  # noqa: BLE001
                logger.warning("      %s margin not set (needs a flat account): %s", self.margin_mode, exc)
            self._margin_mode_set = True
        try:
            self.client.set_leverage(product_id, self.leverage)
            logger.info("      leverage set %dx on %d", self.leverage, product_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("      could not set leverage %dx on %d: %s", self.leverage, product_id, exc)

    def _limit_price(self, row: pd.Series, side: str) -> float:
        """Cross-the-spread limit: buy at ask, sell at bid (fallback: mark ± slippage)."""
        tick = float(row.get("tick_size", 0.01) or 0.01)
        mark = float(row["mark"])
        bid, ask = row.get("bid"), row.get("ask")
        if side == "buy":
            raw = float(ask) if ask and not math.isnan(ask) else mark * (1 + DEFAULT_CROSS_SLIPPAGE)
        else:
            raw = float(bid) if bid and not math.isnan(bid) else mark * (1 - DEFAULT_CROSS_SLIPPAGE)
        return max(round_to_tick(raw, tick), tick)

    def _order(self, row: pd.Series, side: str, size: int, reduce_only: bool) -> OrderResult:
        if size <= 0:
            raise ValueError("order size must be positive")
        if size > self.max_contracts:
            raise ValueError(f"size {size} exceeds max_contracts {self.max_contracts}")

        price = self._limit_price(row, side)
        sym, product_id = str(row["symbol"]), int(row["product_id"])
        tag = "REDUCE" if reduce_only else "OPEN"
        logger.info("%s %-4s %d x %s @ %.2f  (%s)", "[DRY]" if self.dry_run else "[LIVE]",
                    side.upper(), size, sym, price, tag)
        self._prepare_margin(product_id, opening=not reduce_only)

        if self.dry_run:
            return OrderResult(sym, side, size, price, dry_run=True)

        from delta_rest_client import OrderType, TimeInForce

        resp = self.client.place_order(
            product_id=product_id, size=size, side=side, limit_price=str(price),
            order_type=OrderType.LIMIT, time_in_force=TimeInForce.IOC,
            reduce_only="true" if reduce_only else "false",
        )
        result = resp.get("result", resp) if isinstance(resp, dict) else {}
        filled = int(result.get("size", 0) - result.get("unfilled_size", result.get("size", 0)) or 0)
        out = OrderResult(
            sym, side, size, price, dry_run=False,
            order_id=result.get("id"), filled_size=filled or int(result.get("size", 0)),
            status=str(result.get("state", "unknown")), raw=result if isinstance(result, dict) else {},
        )
        logger.info("      -> order_id=%s state=%s filled≈%s", out.order_id, out.status, out.filled_size)
        return out

    def buy(self, row: pd.Series, size: int, reduce_only: bool = False) -> OrderResult:
        """Buy ``size`` contracts of the leg (open long, or close a short with reduce_only)."""
        return self._order(row, "buy", size, reduce_only)

    def sell(self, row: pd.Series, size: int, reduce_only: bool = False) -> OrderResult:
        """Sell ``size`` contracts of the leg (open short, or close a long with reduce_only)."""
        return self._order(row, "sell", size, reduce_only)
