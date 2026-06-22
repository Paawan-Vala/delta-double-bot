#!/usr/bin/env python3
"""Binance Vision futures klines downloader (BTC / ETH USD-M perpetuals).

Bulk-downloads historical candlestick (kline) data for USD(S)-M futures from the
FREE Binance Vision data dumps (https://data.binance.vision) — no API key required —
and merges them into one tidy CSV per symbol+interval for backtesting.

For each symbol/interval it downloads:
    * monthly archives for every completed month from --start onwards, and
    * daily archives for the current (incomplete) month up to today.

Each archive ships with a ``.CHECKSUM`` (SHA-256) which is verified before use.

URL pattern (verified 2026-06-21):
    https://data.binance.vision/data/futures/um/{monthly|daily}/klines/
        {SYMBOL}/{interval}/{SYMBOL}-{interval}-{YYYY-MM[-DD]}.zip

Binance futures kline CSV columns (12):
    open_time(ms), open, high, low, close, volume, close_time(ms),
    quote_volume, trades, taker_buy_base, taker_buy_quote, ignore

Usage:
    python binance_futures_downloader.py                       # BTC+ETH, 1d+1h, since 2020-01
    python binance_futures_downloader.py -s BTCUSDT -i 1d      # one symbol/interval
    python binance_futures_downloader.py --start 2023-01       # shorter history
    python binance_futures_downloader.py -o data/binance_futures -v
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import logging
import sys
import time
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

BASE_URL = "https://data.binance.vision/data/futures/um"

OUTPUT_COLUMNS = [
    "open_time_ms",
    "open_time_iso",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time_ms",
    "quote_volume",
    "trades",
    "taker_buy_base",
    "taker_buy_quote",
]


class DownloadError(RuntimeError):
    """Raised when an archive cannot be downloaded or verified."""


def month_range(start: date, end: date) -> list[str]:
    """Return YYYY-MM strings for every completed month in [start, end)."""
    months: list[str] = []
    year, month = start.year, start.month
    while (year, month) < (end.year, end.month):
        months.append(f"{year:04d}-{month:02d}")
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


def day_range(year: int, month: int, last_day: int) -> list[str]:
    """Return YYYY-MM-DD strings for days 1..last_day of the given month."""
    return [f"{year:04d}-{month:02d}-{day:02d}" for day in range(1, last_day + 1)]


def _download_bytes(session: requests.Session, url: str, timeout: float) -> bytes | None:
    """Download a URL, returning bytes, None on 404, or raising on other errors."""
    resp = session.get(url, timeout=timeout)
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        raise DownloadError(f"HTTP {resp.status_code} for {url}")
    return resp.content


def _verify_checksum(content: bytes, checksum_text: str) -> bool:
    """Verify SHA-256 of content against a Binance .CHECKSUM file body."""
    expected = checksum_text.strip().split()[0].lower()
    actual = hashlib.sha256(content).hexdigest().lower()
    return expected == actual


def _parse_kline_csv(raw: bytes) -> list[list[str]]:
    """Parse kline CSV bytes into rows, skipping an optional header line."""
    text = raw.decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))
    if rows and rows[0] and not rows[0][0].lstrip("-").isdigit():
        rows = rows[1:]  # drop header row (present in some date ranges)
    return [r for r in rows if r and len(r) >= 11]


def _to_output_row(row: list[str]) -> list[str]:
    """Convert a raw 12-column kline row to the tidy output row."""
    open_ms = int(row[0])
    open_iso = datetime.fromtimestamp(open_ms / 1000, tz=timezone.utc).isoformat()
    return [
        str(open_ms), open_iso,
        row[1], row[2], row[3], row[4], row[5],
        row[6], row[7], row[8], row[9], row[10],
    ]


def fetch_archive(
    session: requests.Session,
    symbol: str,
    interval: str,
    period: str,
    label: str,
    *,
    verify: bool,
    timeout: float,
) -> list[list[str]]:
    """Download + verify + parse a single monthly/daily archive. Returns rows."""
    base = f"{BASE_URL}/{period}/klines/{symbol}/{interval}/{symbol}-{interval}-{label}.zip"
    content = _download_bytes(session, base, timeout)
    if content is None:
        logger.debug("Not available (404): %s", base)
        return []

    if verify:
        checksum = _download_bytes(session, base + ".CHECKSUM", timeout)
        if checksum is not None and not _verify_checksum(content, checksum.decode("utf-8")):
            raise DownloadError(f"Checksum mismatch for {base}")

    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        csv_name = archive.namelist()[0]
        raw = archive.read(csv_name)
    rows = _parse_kline_csv(raw)
    logger.debug("%s %s %s: %d rows", symbol, interval, label, len(rows))
    return rows


def download_symbol_interval(
    session: requests.Session,
    symbol: str,
    interval: str,
    start: date,
    today: date,
    output_dir: Path,
    *,
    verify: bool,
    timeout: float,
    pause: float,
) -> Path | None:
    """Download all archives for one symbol+interval and write a merged CSV."""
    labels: list[tuple[str, str]] = [("monthly", m) for m in month_range(start, today)]
    labels += [("daily", d) for d in day_range(today.year, today.month, today.day)]

    by_open_time: dict[int, list[str]] = {}
    for period, label in labels:
        try:
            rows = fetch_archive(session, symbol, interval, period, label, verify=verify, timeout=timeout)
        except DownloadError as exc:
            logger.warning("Skipping %s %s %s: %s", symbol, interval, label, exc)
            continue
        for row in rows:
            try:
                by_open_time[int(row[0])] = _to_output_row(row)
            except (ValueError, IndexError):
                continue
        if pause:
            time.sleep(pause)

    if not by_open_time:
        logger.warning("No data downloaded for %s %s", symbol, interval)
        return None

    out_path = output_dir / f"{symbol}_{interval}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(OUTPUT_COLUMNS)
        for open_ms in sorted(by_open_time):
            writer.writerow(by_open_time[open_ms])

    first_iso = by_open_time[min(by_open_time)][1]
    last_iso = by_open_time[max(by_open_time)][1]
    logger.info(
        "%s %s: %d candles (%s -> %s) -> %s",
        symbol, interval, len(by_open_time), first_iso[:10], last_iso[:10], out_path,
    )
    return out_path


def parse_start(value: str) -> date:
    """Parse a YYYY-MM start string into the first day of that month."""
    parsed = datetime.strptime(value, "%Y-%m")
    return date(parsed.year, parsed.month, 1)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Download Binance USD-M futures klines for backtesting.")
    parser.add_argument("-s", "--symbols", nargs="+", default=["BTCUSDT", "ETHUSDT"], help="Symbols (default: BTCUSDT ETHUSDT).")
    parser.add_argument("-i", "--intervals", nargs="+", default=["1d", "1h"], help="Kline intervals (default: 1d 1h).")
    parser.add_argument("--start", type=parse_start, default=parse_start("2020-01"), help="History start as YYYY-MM (default: 2020-01).")
    parser.add_argument("-o", "--output", type=Path, default=Path("data/binance_futures"), help="Output directory (default: data/binance_futures).")
    parser.add_argument("--no-verify", action="store_true", help="Skip SHA-256 checksum verification.")
    parser.add_argument("--pause", type=float, default=0.1, help="Seconds to pause between archive downloads (default: 0.1).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run(args: argparse.Namespace) -> int:
    """Download all requested symbol/interval combinations."""
    today = datetime.now(timezone.utc).date()
    session = requests.Session()
    session.headers.update({"User-Agent": "pmcc-futures-downloader/1.0"})
    written: list[Path] = []

    for symbol in args.symbols:
        for interval in args.intervals:
            logger.info("Downloading %s %s since %s ...", symbol, interval, args.start.strftime("%Y-%m"))
            path = download_symbol_interval(
                session, symbol, interval, args.start, today, args.output,
                verify=not args.no_verify, timeout=30.0, pause=args.pause,
            )
            if path is not None:
                written.append(path)

    if not written:
        logger.error("No files were written.")
        return EXIT_FAILURE

    logger.info("Done. Wrote %d combined CSV file(s).", len(written))
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
