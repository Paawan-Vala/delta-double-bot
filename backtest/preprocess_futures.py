#!/usr/bin/env python3
"""Phase 1a — resample Delta Exchange BTCUSD futures TRADES into OHLC candles.

Reads the extracted monthly trade files (`BTCUSD_YYYY-MM.csv`), resamples the tick
trades into 1-day and 1-hour OHLCV bars, and writes compact parquet files used by
the rest of the backtest (indicators, dashboard).

Input columns:  product_symbol, price, size, timestamp, buyer_role
Output columns: ts, open, high, low, close, volume, trades

Usage:
    python -m backtest.preprocess_futures            # all months, 1d + 1h
    python -m backtest.preprocess_futures -v
"""
from __future__ import annotations

import argparse
import logging
import sys

import polars as pl

from backtest import config

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

_AGG = [
    pl.col("price").first().alias("open"),
    pl.col("price").max().alias("high"),
    pl.col("price").min().alias("low"),
    pl.col("price").last().alias("close"),
    pl.col("size").sum().alias("volume"),
    pl.len().alias("trades"),
]


def _load_trades(path) -> pl.DataFrame:
    """Load one monthly trade file into a sorted (price, size, ts) DataFrame."""
    return (
        pl.scan_csv(path)
        .select(
            pl.col("price").cast(pl.Float64),
            pl.col("size").cast(pl.Float64),
            pl.col("timestamp")
            .str.to_datetime(format=config.RAW_TIMESTAMP_FORMAT, strict=False)
            .alias("ts"),
        )
        .drop_nulls("ts")
        .sort("ts")
        .collect()
    )


def _resample(df: pl.DataFrame, every: str) -> pl.DataFrame:
    """Resample a sorted trade DataFrame into OHLCV bars of the given interval."""
    return df.group_by_dynamic("ts", every=every, closed="left", label="left").agg(_AGG)


def build_bars() -> tuple[pl.DataFrame, pl.DataFrame]:
    """Build combined 1d and 1h OHLC bar tables across all BTCUSD month files."""
    files = sorted(config.RAW_DATA_DIR.glob("BTCUSD_*.csv"))
    if not files:
        raise FileNotFoundError(f"No BTCUSD_*.csv files in {config.RAW_DATA_DIR}")

    daily_parts: list[pl.DataFrame] = []
    hourly_parts: list[pl.DataFrame] = []
    for path in files:
        df = _load_trades(path)
        logger.info("%s: %d trades (%s → %s)", path.name, df.height, df["ts"].min(), df["ts"].max())
        daily_parts.append(_resample(df, "1d"))
        hourly_parts.append(_resample(df, "1h"))

    daily = pl.concat(daily_parts).unique("ts", keep="last").sort("ts")
    hourly = pl.concat(hourly_parts).unique("ts", keep="last").sort("ts")
    return daily, hourly


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Resample Delta BTCUSD futures trades to OHLC.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run() -> int:
    """Build and write the 1d and 1h OHLC parquet files."""
    config.ensure_dirs()
    daily, hourly = build_bars()
    daily.write_parquet(config.FUTURES_1D_PARQUET)
    hourly.write_parquet(config.FUTURES_1H_PARQUET)
    logger.info(
        "Wrote %d daily bars (%s → %s) -> %s",
        daily.height, daily["ts"].min(), daily["ts"].max(), config.FUTURES_1D_PARQUET,
    )
    logger.info(
        "Wrote %d hourly bars -> %s", hourly.height, config.FUTURES_1H_PARQUET,
    )
    return EXIT_SUCCESS


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
