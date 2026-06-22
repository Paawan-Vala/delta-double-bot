#!/usr/bin/env python3
"""Live market data for Delta Exchange.

Two sources, on purpose:

* **Signal candles** come from a *data* endpoint (default Production-India, public) because
  the testnet only has a few synthetic daily candles — too few for the 200-EMA signal.
* **Options chain + futures mark** come from the *trading* endpoint (your testnet), because
  that is where orders are actually placed.

All calls here are public/read-only (no auth, no orders).
"""
from __future__ import annotations

import logging
import time

import pandas as pd
import requests

from live.config import PROD_INDIA

logger = logging.getLogger(__name__)

PERP_SYMBOL = "BTCUSD"
_MAX_RETRIES = 4
_BACKOFF_SECONDS = 1.5


class DeltaData:
    """Read-only market data access for signal candles and the options chain."""

    def __init__(self, trade_base_url: str, data_base_url: str = PROD_INDIA,
                 session: requests.Session | None = None) -> None:
        self.trade_base = trade_base_url.rstrip("/")
        self.data_base = data_base_url.rstrip("/")
        self.s = session or requests.Session()
        self._products: list[dict] | None = None

    def _get(self, base: str, path: str, **params) -> object:
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                resp = self.s.get(f"{base}{path}", params=params or None, timeout=30)
                resp.raise_for_status()
                return resp.json().get("result")
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
                last_exc = exc
                wait = _BACKOFF_SECONDS * attempt
                logger.warning("GET %s%s failed (attempt %d/%d): %s — retrying in %.1fs",
                               base, path, attempt, _MAX_RETRIES, type(exc).__name__, wait)
                time.sleep(wait)
        raise RuntimeError(f"GET {base}{path} failed after {_MAX_RETRIES} attempts") from last_exc

    # --- futures -------------------------------------------------------------
    def perp_mark(self) -> float:
        """Current BTCUSD futures mark price on the trading venue (testnet)."""
        t = self._get(self.trade_base, f"/v2/tickers/{PERP_SYMBOL}") or {}
        return float(t.get("mark_price") or t.get("spot_price"))

    def daily_candles(self, days: int = 400) -> pd.DataFrame:
        """Daily BTCUSD OHLC from the data venue (production), ascending by date."""
        end = int(time.time())
        start = end - days * 86_400
        rows = self._get(self.data_base, "/v2/history/candles",
                         resolution="1d", symbol=PERP_SYMBOL, start=start, end=end) or []
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        df["date"] = pd.to_datetime(df["time"], unit="s")
        df = df.set_index("date").sort_index()
        return df[["open", "high", "low", "close", "volume"]].astype(float)

    # --- options -------------------------------------------------------------
    def btc_option_products(self) -> list[dict]:
        """All live BTC option products on the trading venue (cached)."""
        if self._products is None:
            prods = self._get(self.trade_base, "/v2/products") or []
            self._products = [
                p for p in prods
                if p.get("contract_type") in ("call_options", "put_options")
                and (p.get("underlying_asset") or {}).get("symbol") == "BTC"
            ]
        return self._products

    def option_chain(self) -> pd.DataFrame:
        """BTC options with live greeks, mark, quotes and the order ``product_id``."""
        prods = self.btc_option_products()
        tickers = self._get(self.trade_base, "/v2/tickers",
                            contract_types="call_options,put_options") or []
        tmap = {t.get("symbol"): t for t in tickers}
        today = pd.Timestamp.now(tz="UTC").tz_convert(None).normalize()

        rows: list[dict] = []
        for p in prods:
            sym = p.get("symbol")
            t = tmap.get(sym)
            if not t:
                continue
            greeks = t.get("greeks") or {}
            quotes = t.get("quotes") or {}
            expiry = pd.to_datetime(p["settlement_time"]).tz_convert(None)
            rows.append({
                "symbol": sym,
                "product_id": p.get("id"),
                "option_type": "C" if p["contract_type"] == "call_options" else "P",
                "strike": float(p["strike_price"]),
                "expiry": expiry,
                "dte": int((expiry.normalize() - today).days),
                "delta": float(greeks["delta"]) if greeks.get("delta") is not None else float("nan"),
                "mark": float(t["mark_price"]) if t.get("mark_price") is not None else float("nan"),
                "bid": float(quotes["best_bid"]) if quotes.get("best_bid") is not None else float("nan"),
                "ask": float(quotes["best_ask"]) if quotes.get("best_ask") is not None else float("nan"),
                "oi": float(t.get("oi") or 0.0),
                "state": p.get("state"),
                "status": p.get("trading_status"),
                "contract_value": float(p.get("contract_value") or 0.001),
                "tick_size": float(p.get("tick_size") or 0.01),
            })
        return pd.DataFrame(rows)
