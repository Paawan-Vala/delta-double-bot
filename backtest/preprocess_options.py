#!/usr/bin/env python3
"""Phase 1b — reconstruct DAILY option prices from Delta Exchange BTC option trades.

Reads the extracted monthly option-trade files (`BTC_YYYY-MM.csv`), parses each
`product_symbol` into (type, strike, expiry), and aggregates trades to one row per
(instrument, day) with OHLC/VWAP/last price + volume. This gives a usable daily
price series per option for the backtest (trades are sparse, so gaps are expected
and handled later with a Black-76 fallback).

Input columns:  product_symbol, price, size, timestamp, buyer_role
product_symbol: {C|P}-BTC-{strike}-{DDMMYY}, e.g. C-BTC-94600-010525
Output columns: date, product_symbol, option_type, strike, expiry,
                open, high, low, close, vwap, volume, trades

Usage:
    python -m backtest.preprocess_options
    python -m backtest.preprocess_options -v
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


def _aggregate_file(path) -> pl.DataFrame:
    """Parse one monthly option-trade file into per-(instrument, day) price rows."""
    sym = pl.col("product_symbol").str.split("-")
    lf = (
        pl.scan_csv(path)
        .with_columns(
            pl.col("price").cast(pl.Float64),
            pl.col("size").cast(pl.Float64),
            pl.col("timestamp")
            .str.to_datetime(format=config.RAW_TIMESTAMP_FORMAT, strict=False)
            .alias("ts"),
            sym.list.get(0).alias("option_type"),
            sym.list.get(2).cast(pl.Int64, strict=False).alias("strike"),
            sym.list.get(3).str.to_date("%d%m%y", strict=False).alias("expiry"),
        )
        .drop_nulls(["ts", "strike", "expiry"])
        .with_columns(pl.col("ts").dt.date().alias("date"))
        .group_by(["product_symbol", "date"])
        .agg(
            pl.col("option_type").first(),
            pl.col("strike").first(),
            pl.col("expiry").first(),
            pl.col("price").sort_by("ts").first().alias("open"),
            pl.col("price").max().alias("high"),
            pl.col("price").min().alias("low"),
            pl.col("price").sort_by("ts").last().alias("close"),
            ((pl.col("price") * pl.col("size")).sum() / pl.col("size").sum()).alias("vwap"),
            pl.col("size").sum().alias("volume"),
            pl.len().alias("trades"),
        )
    )
    return lf.collect()


def build_options_daily() -> pl.DataFrame:
    """Aggregate all option-trade months into one daily option-price table."""
    files = sorted(config.RAW_DATA_DIR.glob("BTC_*.csv"))
    if not files:
        raise FileNotFoundError(f"No BTC_*.csv option files in {config.RAW_DATA_DIR}")

    parts: list[pl.DataFrame] = []
    for path in files:
        df = _aggregate_file(path)
        logger.info("%s: %d (instrument, day) rows", path.name, df.height)
        parts.append(df)

    combined = (
        pl.concat(parts)
        .unique(["product_symbol", "date"], keep="last")
        .sort(["date", "expiry", "strike", "option_type"])
    )
    return combined


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Reconstruct daily BTC option prices from trades.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run() -> int:
    """Build and write the daily option-price parquet."""
    config.ensure_dirs()
    df = build_options_daily()
    df.write_parquet(config.OPTIONS_DAILY_PARQUET)
    logger.info(
        "Wrote %d rows (%d instruments, %s → %s) -> %s",
        df.height,
        df["product_symbol"].n_unique(),
        df["date"].min(),
        df["date"].max(),
        config.OPTIONS_DAILY_PARQUET,
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
