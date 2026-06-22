#!/usr/bin/env python3
"""Deribit daily options-chain snapshot collector (BTC / ETH).

Fetches the full *active* options chain from Deribit's free public API and writes a
timestamped CSV snapshot per currency, including implied volatility and full greeks.

This is the "collect-forward" approach. Run it once per day (e.g. via Windows Task
Scheduler) to build your own historical options dataset over time, because Deribit's
free API does NOT expose clean historical chains for arbitrary past dates.

No API key is required (public endpoints only).

Endpoints used (verified against https://docs.deribit.com/ on 2026-06-21):
    public/get_index_price               - current BTC/ETH USD index price
    public/get_instruments               - active option instrument metadata
    public/ticker                        - per-option mark price, IV and greeks
    public/get_book_summary_by_currency  - fast prices/IV/OI (no greeks; --fast mode)

Notes:
    * Option premiums (mark_price, bid/ask) are quoted in the BASE CURRENCY (BTC/ETH),
      not USD. ``mark_price_usd`` below is an approximation = mark_price * underlying_price.
    * Implied volatility fields (mark_iv/bid_iv/ask_iv) are in PERCENT.
    * Greeks (delta/gamma/vega/theta/rho) are only available from ``public/ticker``;
      ``get_book_summary_by_currency`` does not return greeks, hence the hybrid design.

Usage:
    python deribit_options_collector.py                 # BTC + ETH, full greeks
    python deribit_options_collector.py -c BTC          # BTC only
    python deribit_options_collector.py --fast          # no greeks, ~1 call/currency
    python deribit_options_collector.py --min-oi 1      # skip zero-open-interest wings
    python deribit_options_collector.py -o D:/data -v   # custom output dir, verbose
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2

API_BASE = "https://www.deribit.com/api/v2"
INDEX_NAMES: dict[str, str] = {"BTC": "btc_usd", "ETH": "eth_usd"}

CSV_FIELDS: list[str] = [
    "snapshot_time_utc",
    "currency",
    "instrument_name",
    "option_type",
    "strike",
    "expiry_utc",
    "dte_days",
    "index_price",
    "underlying_price",
    "mark_price",        # in coin (BTC/ETH)
    "mark_price_usd",    # approx = mark_price * underlying_price
    "mark_iv",           # percent
    "bid_iv",
    "ask_iv",
    "best_bid_price",
    "best_ask_price",
    "best_bid_amount",
    "best_ask_amount",
    "last_price",
    "open_interest",
    "volume_24h",
    "delta",
    "gamma",
    "vega",
    "theta",
    "rho",
    "contract_size",
    "tick_size",
]


class DeribitError(RuntimeError):
    """Raised when the Deribit API returns an error or cannot be reached."""


@dataclass
class RateLimiter:
    """Minimum-interval rate limiter to stay polite to the public API."""

    rate_per_sec: float
    _last: float = field(default=0.0, repr=False)

    def wait(self) -> None:
        """Block until at least ``1 / rate_per_sec`` seconds have elapsed."""
        if self.rate_per_sec <= 0:
            return
        min_interval = 1.0 / self.rate_per_sec
        elapsed = time.monotonic() - self._last
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last = time.monotonic()


class DeribitClient:
    """Thin client for Deribit public REST endpoints with retry + backoff."""

    def __init__(
        self,
        rate_per_sec: float = 5.0,
        timeout: float = 15.0,
        max_retries: int = 5,
    ) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "pmcc-deribit-collector/1.0"})
        self.limiter = RateLimiter(rate_per_sec)
        self.timeout = timeout
        self.max_retries = max_retries

    def _get(self, method: str, params: dict[str, Any]) -> Any:
        """GET a public method, retrying on HTTP 429/5xx and Deribit code 10028."""
        url = f"{API_BASE}/{method}"
        backoff = 1.0
        for attempt in range(1, self.max_retries + 1):
            self.limiter.wait()
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                logger.warning(
                    "Network error on %s (attempt %d/%d): %s",
                    method, attempt, self.max_retries, exc,
                )
                time.sleep(backoff)
                backoff = min(backoff * 2, 30.0)
                continue

            if resp.status_code == 429 or resp.status_code >= 500:
                logger.warning(
                    "HTTP %d on %s (attempt %d/%d); backing off %.1fs",
                    resp.status_code, method, attempt, self.max_retries, backoff,
                )
                time.sleep(backoff)
                backoff = min(backoff * 2, 30.0)
                continue

            try:
                data = resp.json()
            except ValueError as exc:
                raise DeribitError(f"{method}: invalid JSON response") from exc

            error = data.get("error")
            if error:
                code = error.get("code")
                if code == 10028:  # too_many_requests
                    logger.warning(
                        "Rate limited (10028) on %s; backing off %.1fs", method, backoff,
                    )
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 30.0)
                    continue
                raise DeribitError(f"{method} error {code}: {error.get('message')}")

            return data["result"]

        raise DeribitError(f"{method} failed after {self.max_retries} retries")

    def get_index_price(self, currency: str) -> float:
        """Return the current USD index price for the currency (btc_usd / eth_usd)."""
        result = self._get("public/get_index_price", {"index_name": INDEX_NAMES[currency]})
        return float(result["index_price"])

    def get_option_instruments(self, currency: str) -> list[dict[str, Any]]:
        """Return metadata for all active option instruments of the currency."""
        return self._get(
            "public/get_instruments",
            {"currency": currency, "kind": "option", "expired": "false"},
        )

    def get_ticker(self, instrument_name: str) -> dict[str, Any]:
        """Return full ticker (mark price, IV, greeks) for one option instrument."""
        return self._get("public/ticker", {"instrument_name": instrument_name})

    def get_book_summary(self, currency: str) -> list[dict[str, Any]]:
        """Return one-shot book summaries for all options (no greeks)."""
        return self._get(
            "public/get_book_summary_by_currency",
            {"currency": currency, "kind": "option"},
        )


def _to_float(value: Any) -> float | None:
    """Coerce a value to float, returning None when missing/invalid."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _expiry_and_dte(
    meta: dict[str, Any], snapshot_time: datetime
) -> tuple[str | None, float | None]:
    """Compute ISO expiry and days-to-expiration from instrument metadata."""
    exp_ms = meta.get("expiration_timestamp")
    if not exp_ms:
        return None, None
    expiry = datetime.fromtimestamp(exp_ms / 1000, tz=timezone.utc)
    dte = (expiry - snapshot_time).total_seconds() / 86400.0
    return expiry.isoformat(), round(dte, 4)


def _row_from_ticker(
    currency: str,
    snapshot_time: datetime,
    index_price: float,
    meta: dict[str, Any],
    ticker: dict[str, Any],
) -> dict[str, Any]:
    """Build a CSV row from instrument metadata + a ticker response (with greeks)."""
    expiry_iso, dte = _expiry_and_dte(meta, snapshot_time)
    greeks = ticker.get("greeks") or {}
    stats = ticker.get("stats") or {}
    mark = _to_float(ticker.get("mark_price"))
    underlying = _to_float(ticker.get("underlying_price"))
    mark_usd = mark * underlying if mark is not None and underlying is not None else None
    return {
        "snapshot_time_utc": snapshot_time.isoformat(),
        "currency": currency,
        "instrument_name": ticker.get("instrument_name") or meta.get("instrument_name"),
        "option_type": meta.get("option_type"),
        "strike": _to_float(meta.get("strike")),
        "expiry_utc": expiry_iso,
        "dte_days": dte,
        "index_price": index_price,
        "underlying_price": underlying,
        "mark_price": mark,
        "mark_price_usd": round(mark_usd, 4) if mark_usd is not None else None,
        "mark_iv": _to_float(ticker.get("mark_iv")),
        "bid_iv": _to_float(ticker.get("bid_iv")),
        "ask_iv": _to_float(ticker.get("ask_iv")),
        "best_bid_price": _to_float(ticker.get("best_bid_price")),
        "best_ask_price": _to_float(ticker.get("best_ask_price")),
        "best_bid_amount": _to_float(ticker.get("best_bid_amount")),
        "best_ask_amount": _to_float(ticker.get("best_ask_amount")),
        "last_price": _to_float(ticker.get("last_price")),
        "open_interest": _to_float(ticker.get("open_interest")),
        "volume_24h": _to_float(stats.get("volume")),
        "delta": _to_float(greeks.get("delta")),
        "gamma": _to_float(greeks.get("gamma")),
        "vega": _to_float(greeks.get("vega")),
        "theta": _to_float(greeks.get("theta")),
        "rho": _to_float(greeks.get("rho")),
        "contract_size": _to_float(meta.get("contract_size")),
        "tick_size": _to_float(meta.get("tick_size")),
    }


def _row_from_summary(
    currency: str,
    snapshot_time: datetime,
    index_price: float,
    meta: dict[str, Any],
    summary: dict[str, Any],
) -> dict[str, Any]:
    """Build a CSV row from instrument metadata + a book summary (no greeks)."""
    expiry_iso, dte = _expiry_and_dte(meta, snapshot_time)
    mark = _to_float(summary.get("mark_price"))
    underlying = _to_float(summary.get("underlying_price"))
    mark_usd = mark * underlying if mark is not None and underlying is not None else None
    return {
        "snapshot_time_utc": snapshot_time.isoformat(),
        "currency": currency,
        "instrument_name": summary.get("instrument_name") or meta.get("instrument_name"),
        "option_type": meta.get("option_type"),
        "strike": _to_float(meta.get("strike")),
        "expiry_utc": expiry_iso,
        "dte_days": dte,
        "index_price": index_price,
        "underlying_price": underlying,
        "mark_price": mark,
        "mark_price_usd": round(mark_usd, 4) if mark_usd is not None else None,
        "mark_iv": _to_float(summary.get("mark_iv")),
        "bid_iv": None,
        "ask_iv": None,
        "best_bid_price": _to_float(summary.get("bid_price")),
        "best_ask_price": _to_float(summary.get("ask_price")),
        "best_bid_amount": None,
        "best_ask_amount": None,
        "last_price": _to_float(summary.get("last")),
        "open_interest": _to_float(summary.get("open_interest")),
        "volume_24h": _to_float(summary.get("volume")),
        "delta": None,
        "gamma": None,
        "vega": None,
        "theta": None,
        "rho": None,
        "contract_size": _to_float(meta.get("contract_size")),
        "tick_size": _to_float(meta.get("tick_size")),
    }


def collect_currency(
    client: DeribitClient,
    currency: str,
    snapshot_time: datetime,
    *,
    with_greeks: bool = True,
    min_oi: float = 0.0,
) -> list[dict[str, Any]]:
    """Collect one chain snapshot for a currency and return CSV rows."""
    index_price = client.get_index_price(currency)
    instruments = client.get_option_instruments(currency)
    meta_by_name = {i["instrument_name"]: i for i in instruments}
    logger.info("%s: %d active options (index %.2f)", currency, len(meta_by_name), index_price)

    rows: list[dict[str, Any]] = []
    if with_greeks:
        names = list(meta_by_name)
        total = len(names)
        for idx, name in enumerate(names, start=1):
            try:
                ticker = client.get_ticker(name)
            except DeribitError as exc:
                logger.warning("Skipping %s: %s", name, exc)
                continue
            if (_to_float(ticker.get("open_interest")) or 0.0) < min_oi:
                continue
            rows.append(_row_from_ticker(currency, snapshot_time, index_price, meta_by_name[name], ticker))
            if idx % 100 == 0:
                logger.info("%s: fetched %d/%d", currency, idx, total)
    else:
        for summary in client.get_book_summary(currency):
            name = summary.get("instrument_name")
            meta = meta_by_name.get(name)
            if meta is None:
                continue
            if (_to_float(summary.get("open_interest")) or 0.0) < min_oi:
                continue
            rows.append(_row_from_summary(currency, snapshot_time, index_price, meta, summary))

    logger.info("%s: collected %d rows", currency, len(rows))
    return rows


def write_snapshot(rows: list[dict[str, Any]], output_dir: Path, currency: str, snapshot_time: datetime) -> Path:
    """Write rows to a dated CSV file and return its path."""
    day_dir = output_dir / snapshot_time.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    stamp = snapshot_time.strftime("%Y%m%d_%H%M%S")
    out_path = day_dir / f"{currency}_options_{stamp}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Wrote %d rows -> %s", len(rows), out_path)
    return out_path


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Daily Deribit BTC/ETH options-chain snapshot collector.")
    parser.add_argument(
        "-c", "--currencies", nargs="+", default=["BTC", "ETH"],
        choices=sorted(INDEX_NAMES), help="Currencies to collect (default: BTC ETH).",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("data/deribit_options"),
        help="Output directory (default: data/deribit_options).",
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Skip greeks: 1 book-summary call per currency instead of per-option ticker calls.",
    )
    parser.add_argument(
        "--min-oi", type=float, default=0.0,
        help="Only keep options with open_interest >= this value (default: 0 = keep all).",
    )
    parser.add_argument(
        "--rate", type=float, default=5.0,
        help="Max requests per second to the public API (default: 5).",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run(args: argparse.Namespace) -> int:
    """Collect snapshots for the requested currencies."""
    client = DeribitClient(rate_per_sec=args.rate)
    snapshot_time = datetime.now(timezone.utc)
    written: list[Path] = []

    for currency in args.currencies:
        try:
            rows = collect_currency(
                client, currency, snapshot_time,
                with_greeks=not args.fast, min_oi=args.min_oi,
            )
        except DeribitError as exc:
            logger.error("Failed to collect %s: %s", currency, exc)
            continue
        if rows:
            written.append(write_snapshot(rows, args.output, currency, snapshot_time))

    if not written:
        logger.error("No snapshots were written.")
        return EXIT_FAILURE

    logger.info("Done. Wrote %d snapshot file(s).", len(written))
    return EXIT_SUCCESS


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Unexpected error: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
