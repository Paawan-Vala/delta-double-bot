#!/usr/bin/env python3
"""Phase 2 — direction indicators on the resampled BTCUSD daily candles.

Computes the full direction stack described in the plan and reduces it to a single
daily label ``direction ∈ {bull, bear, none}`` used by the PMCC/PMCP engine:

* EMA(n) with k = 2/(n+1): EMA20, EMA50, EMA200.
* Regime  = close vs EMA200 (the 200-EMA needs ~200 bars of warm-up).
* Trigger = EMA20 vs EMA50.
* Strength = ADX(14) Wilder with +DI / -DI.
* Weekly agreement = weekly close vs a weekly EMA, forward-filled onto daily dates.

A day is ``bull`` only when regime, trigger, +DI/-DI, weekly all point up AND ADX is
above the threshold (and the 200-EMA warm-up is complete); ``bear`` is the mirror;
otherwise ``none`` (stand aside).

Usage:
    python -m backtest.indicators            # writes data/processed/direction_daily.parquet
    python -m backtest.indicators -v
"""
from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from backtest import config

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


@dataclass(frozen=True)
class DirectionParams:
    """Tunable parameters for the direction signal."""

    ema_fast: int = config.EMA_FAST
    ema_slow: int = config.EMA_SLOW
    ema_regime: int = config.EMA_REGIME
    adx_period: int = config.ADX_PERIOD
    adx_threshold: float = config.ADX_THRESHOLD
    weekly_span: int = 10


def ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential moving average with k = 2/(span+1) (recursive form)."""
    return series.ewm(span=span, adjust=False).mean()


def _wilder(series: pd.Series, period: int) -> pd.Series:
    """Wilder's smoothing (RMA) = EWM with alpha = 1/period."""
    return series.ewm(alpha=1.0 / period, adjust=False).mean()


def compute_adx(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """Return +DI, -DI and ADX (Wilder) for a high/low/close DataFrame."""
    high, low, close = df["high"], df["low"], df["close"]
    up = high.diff()
    down = -low.diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)

    prev_close = close.shift()
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    atr = _wilder(tr, period)

    plus_di = 100.0 * _wilder(plus_dm, period) / atr
    minus_di = 100.0 * _wilder(minus_dm, period) / atr
    dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan)
    adx = _wilder(dx.fillna(0.0), period)
    return pd.DataFrame({"plus_di": plus_di, "minus_di": minus_di, "adx": adx})


def weekly_trend(close: pd.Series, span: int) -> pd.Series:
    """Weekly trend (+1/-1) from weekly close vs weekly EMA, aligned to daily dates."""
    weekly = close.resample("W-FRI").last().dropna()
    weekly_ema = ema(weekly, span)
    wk_dir = np.where(weekly > weekly_ema, 1, -1)
    wk = pd.Series(wk_dir, index=weekly.index)
    # Map each daily date to the most recent completed weekly signal.
    return wk.reindex(close.index, method="ffill")


def load_daily() -> pd.DataFrame:
    """Load the daily BTCUSD OHLC parquet as a date-indexed pandas DataFrame."""
    df = pd.read_parquet(config.FUTURES_1D_PARQUET)
    df = df.rename(columns={"ts": "date"}).set_index("date").sort_index()
    df.index = pd.to_datetime(df.index)
    return df


def compute_direction(df: pd.DataFrame, params: DirectionParams | None = None) -> pd.DataFrame:
    """Attach indicator columns and the daily ``direction`` label to OHLC data."""
    p = params or DirectionParams()
    out = df.copy()
    out["ema_fast"] = ema(out["close"], p.ema_fast)
    out["ema_slow"] = ema(out["close"], p.ema_slow)
    out["ema_regime"] = ema(out["close"], p.ema_regime)
    out = out.join(compute_adx(out, p.adx_period))
    out["weekly_dir"] = weekly_trend(out["close"], p.weekly_span)

    regime = np.where(out["close"] > out["ema_regime"], 1, -1)
    trigger = np.where(out["ema_fast"] > out["ema_slow"], 1, -1)
    di = np.where(out["plus_di"] > out["minus_di"], 1, -1)
    strong = out["adx"] >= p.adx_threshold
    weekly = out["weekly_dir"].to_numpy()

    # 200-EMA warm-up: require enough bars before trusting the regime filter.
    warm = np.arange(len(out)) >= p.ema_regime

    bull = (regime > 0) & (trigger > 0) & (di > 0) & (weekly > 0) & strong.to_numpy() & warm
    bear = (regime < 0) & (trigger < 0) & (di < 0) & (weekly < 0) & strong.to_numpy() & warm

    direction = np.where(bull, "bull", np.where(bear, "bear", "none"))
    out["regime_dir"] = regime
    out["trigger_dir"] = trigger
    out["di_dir"] = di
    out["adx_strong"] = strong
    out["direction"] = direction
    out["dir_code"] = np.where(bull, 1, np.where(bear, -1, 0))
    return out


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Compute the daily direction signal from BTCUSD candles.")
    parser.add_argument("--ema-regime", type=int, default=config.EMA_REGIME, help="Regime EMA period (default 200).")
    parser.add_argument("--adx-threshold", type=float, default=config.ADX_THRESHOLD, help="ADX strong-trend threshold.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run(args: argparse.Namespace) -> int:
    """Compute the direction signal and save it to parquet."""
    config.ensure_dirs()
    params = DirectionParams(ema_regime=args.ema_regime, adx_threshold=args.adx_threshold)
    daily = load_daily()
    out = compute_direction(daily, params)

    counts = out["direction"].value_counts().to_dict()
    first_signal = out.loc[out["direction"] != "none"].index.min()
    logger.info("Direction counts: %s", counts)
    logger.info("First actionable signal: %s", first_signal)

    out_path = config.PROCESSED_DIR / "direction_daily.parquet"
    out.reset_index().to_parquet(out_path)
    logger.info("Wrote %d rows -> %s", len(out), out_path)
    return EXIT_SUCCESS


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
