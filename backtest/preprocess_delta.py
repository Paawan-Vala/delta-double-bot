#!/usr/bin/env python3
"""Phase A (delta variant) — derive a Black-76 delta column for the options table.

The raw Delta Exchange data is trades-only (no greeks), so we *derive* a per-row
option delta with Black-76 using each day's futures price (underlying) and the day's
ATM implied-vol estimate. The output augments ``options_daily.parquet`` with ``delta``
and ``atm_iv`` columns and is written to ``options_daily_delta.parquet`` so the
original processed file is left untouched.

Usage:
    python -m backtest.preprocess_delta
    python -m backtest.preprocess_delta -v
"""
from __future__ import annotations

import argparse
import logging
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm

from backtest import config, indicators
from backtest.strategy import PriceBook

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def compute_delta_column(options_df: pd.DataFrame, futures_df: pd.DataFrame) -> pd.DataFrame:
    """Return ``options_df`` with derived ``atm_iv`` and ``delta`` columns.

    Delta is the Black-76 delta (signed: calls 0..+1, puts -1..0) using the day's
    futures close as the underlying and the day's ATM-IV estimate as volatility.
    """
    df = options_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["expiry"] = pd.to_datetime(df["expiry"])

    # Reuse the PriceBook's per-day ATM-IV estimate (date-indexed, forward-filled).
    book = PriceBook(df, futures_df)
    spot_by_date = futures_df["close"]

    df["spot"] = df["date"].map(spot_by_date)
    df["atm_iv"] = df["date"].map(book.atm_iv)

    f = df["spot"].to_numpy(dtype=float)
    k = df["strike"].to_numpy(dtype=float)
    sig = df["atm_iv"].to_numpy(dtype=float)
    t = ((df["expiry"] - df["date"]).dt.days.clip(lower=0).to_numpy(dtype=float)) / 365.0
    is_call = (df["option_type"].to_numpy() == "C")

    with np.errstate(divide="ignore", invalid="ignore"):
        srt = sig * np.sqrt(t)
        d1 = (np.log(f / k) + 0.5 * sig * sig * t) / srt
        call_delta = norm.cdf(d1)
    put_delta = call_delta - 1.0
    delta = np.where(is_call, call_delta, put_delta)

    # Degenerate cases (expired, zero/NaN vol, NaN inputs) -> intrinsic delta.
    intrinsic = np.where(is_call, np.where(f > k, 1.0, 0.0), np.where(f < k, -1.0, 0.0))
    bad = (t <= 0.0) | (sig <= 0.0) | ~np.isfinite(d1)
    delta = np.where(bad, intrinsic, delta)
    delta = np.where(np.isnan(f) | np.isnan(k), np.nan, delta)

    df["delta"] = delta
    return df.drop(columns=["spot"])


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Derive a Black-76 delta column for the options table.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run() -> int:
    """Load processed options + futures, derive delta, write the augmented parquet."""
    config.ensure_dirs()
    options_df = pd.read_parquet(config.OPTIONS_DAILY_PARQUET)
    futures_df = indicators.load_daily()
    out = compute_delta_column(options_df, futures_df)
    out.to_parquet(config.OPTIONS_DAILY_DELTA_PARQUET)

    valid = out["delta"].dropna()
    logger.info("Wrote %s (%d rows)", config.OPTIONS_DAILY_DELTA_PARQUET, len(out))
    logger.info("delta: min=%.3f max=%.3f mean=%.3f | NaN=%d",
                float(valid.min()), float(valid.max()), float(valid.mean()), int(out["delta"].isna().sum()))
    calls = out[out["option_type"] == "C"]["delta"].dropna()
    puts = out[out["option_type"] == "P"]["delta"].dropna()
    logger.info("calls in [0,1]: %.1f%% | puts in [-1,0]: %.1f%%",
                100.0 * ((calls >= 0) & (calls <= 1)).mean() if len(calls) else 0.0,
                100.0 * ((puts >= -1) & (puts <= 0)).mean() if len(puts) else 0.0)
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
