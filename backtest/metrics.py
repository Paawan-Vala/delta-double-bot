#!/usr/bin/env python3
"""Phase 4 — performance metrics from the backtest equity curve and trade log.

Reads `data/results/equity.parquet` and `data/results/trades.csv`, computes the
standard return / risk / trade statistics, and writes `data/results/metrics.json`.
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sys

import numpy as np
import pandas as pd

from backtest import config

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
TRADING_DAYS = 365  # crypto trades every day


def compute_metrics(equity: pd.DataFrame, trades: pd.DataFrame) -> dict[str, float | int]:
    """Compute return, risk and trade metrics from the equity curve and trades."""
    eq = equity["equity"].astype(float)
    start, end = float(eq.iloc[0]), float(eq.iloc[-1])
    n_days = len(eq)
    total_return = end / start - 1.0
    years = max(n_days / TRADING_DAYS, 1e-9)
    cagr = (end / start) ** (1.0 / years) - 1.0 if start > 0 else math.nan

    daily_ret = eq.pct_change().dropna()
    ann_vol = float(daily_ret.std() * math.sqrt(TRADING_DAYS)) if len(daily_ret) > 1 else 0.0
    ann_ret = float(daily_ret.mean() * TRADING_DAYS)
    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0

    drawdown = eq / eq.cummax() - 1.0
    max_dd = float(drawdown.min())

    closes = trades[trades["event"] == "close"] if not trades.empty else pd.DataFrame()
    pnls = closes["pnl"].astype(float) if "pnl" in closes else pd.Series(dtype=float)
    wins = pnls[pnls > 0]
    losses = pnls[pnls <= 0]
    n_trades = int(len(pnls))
    win_rate = float(len(wins) / n_trades) if n_trades else 0.0
    gross_win = float(wins.sum())
    gross_loss = float(losses.sum())
    profit_factor = float(gross_win / abs(gross_loss)) if gross_loss < 0 else math.inf

    in_pos = equity["in_position"].astype(bool)
    time_in_market = float(in_pos.mean())
    n_rolls = int((trades["event"] == "roll_short").sum() + (trades["event"] == "roll_long").sum()) if not trades.empty else 0

    pmcc = int((closes["direction"] == "bull").sum()) if "direction" in closes else 0
    pmcp = int((closes["direction"] == "bear").sum()) if "direction" in closes else 0
    dir_counts = equity["direction"].value_counts().to_dict()

    return {
        "start_equity": round(start, 2),
        "final_equity": round(end, 2),
        "total_return_pct": round(total_return * 100, 2),
        "cagr_pct": round(cagr * 100, 2),
        "ann_vol_pct": round(ann_vol * 100, 2),
        "sharpe": round(sharpe, 2),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "num_trades": n_trades,
        "win_rate_pct": round(win_rate * 100, 1),
        "avg_win": round(float(wins.mean()), 2) if len(wins) else 0.0,
        "avg_loss": round(float(losses.mean()), 2) if len(losses) else 0.0,
        "profit_factor": round(profit_factor, 2) if math.isfinite(profit_factor) else None,
        "time_in_market_pct": round(time_in_market * 100, 1),
        "num_rolls": n_rolls,
        "pmcc_trades": pmcc,
        "pmcp_trades": pmcp,
        "bull_days": int(dir_counts.get("bull", 0)),
        "bear_days": int(dir_counts.get("bear", 0)),
        "none_days": int(dir_counts.get("none", 0)),
        "n_days": n_days,
    }


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Compute backtest performance metrics.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def run() -> int:
    """Load results, compute metrics, and write metrics.json."""
    equity = pd.read_parquet(config.RESULTS_DIR / "equity.parquet")
    trades_path = config.RESULTS_DIR / "trades.csv"
    trades = pd.read_csv(trades_path) if trades_path.exists() else pd.DataFrame()
    metrics = compute_metrics(equity, trades)
    out_path = config.RESULTS_DIR / "metrics.json"
    out_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    logger.info("Metrics -> %s", out_path)
    for key, value in metrics.items():
        logger.info("  %-22s %s", key, value)
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
