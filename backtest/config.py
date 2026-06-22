"""Shared paths and constants for the PMCC/PMCP backtest.

All file locations and a few domain constants live here so every module agrees on
where the data is and how the Delta Exchange BTC instruments are sized/priced.
"""
from __future__ import annotations

from pathlib import Path

# --- Paths -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "delta_exchgange_options_data" / "extracted"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "data" / "results"

# Processed (parquet) outputs produced by Phase 1.
FUTURES_1D_PARQUET = PROCESSED_DIR / "BTCUSD_1d.parquet"
FUTURES_1H_PARQUET = PROCESSED_DIR / "BTCUSD_1h.parquet"
OPTIONS_DAILY_PARQUET = PROCESSED_DIR / "options_daily.parquet"
# Options table augmented with a derived Black-76 delta column (delta-strategy variant).
OPTIONS_DAILY_DELTA_PARQUET = PROCESSED_DIR / "options_daily_delta.parquet"

# Result files. The original strategy writes equity.parquet / trades.csv; the
# delta/premium variant writes to its own files so both can coexist.
EQUITY_PARQUET = RESULTS_DIR / "equity.parquet"
TRADES_CSV = RESULTS_DIR / "trades.csv"
EQUITY_DELTA_PARQUET = RESULTS_DIR / "equity_delta.parquet"
TRADES_DELTA_CSV = RESULTS_DIR / "trades_delta.csv"
METRICS_DELTA_JSON = RESULTS_DIR / "metrics_delta.json"
# Continuous double-diagonal variant (PMCC + PMCP together, non-directional).
EQUITY_DOUBLE_PARQUET = RESULTS_DIR / "equity_double.parquet"
TRADES_DOUBLE_CSV = RESULTS_DIR / "trades_double.csv"

# --- Instrument / market constants (Delta Exchange BTC) ----------------------
# 1 Delta BTC option/future contract represents this much BTC.
LOT_SIZE_BTC = 0.001
# Option premiums and futures prices in the raw data are quoted in USD.

# --- Default fees / slippage (configurable in the engine) --------------------
# Delta Exchange option fee ~0.03% of premium (taker); modelled as a fraction of
# premium notional. Slippage is half the typical bid/ask as a fraction of premium.
DEFAULT_TAKER_FEE = 0.0005   # fraction of premium notional
DEFAULT_MAKER_FEE = 0.0002
DEFAULT_SLIPPAGE = 0.01      # fraction of premium applied on each fill

# --- Default direction-signal parameters (Phase 2) ---------------------------
EMA_FAST = 20
EMA_SLOW = 50
EMA_REGIME = 200
ADX_PERIOD = 14
ADX_THRESHOLD = 25.0

# Raw timestamp format in the Delta CSVs, e.g. "2026-01-01 00:00:00.322462".
RAW_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S%.f"

# --- Delta/premium strategy variant defaults ---------------------------------
# Long monthly leg is chosen by |delta| near this target (ITM); short daily leg is
# chosen by traded premium (USD per BTC) near this target.
LONG_DELTA_TARGET = 0.70
LONG_DELTA_MIN = 0.60
LONG_DELTA_MAX = 0.80
SHORT_PREMIUM_TARGET = 550.0
SHORT_PREMIUM_MIN = 500.0
SHORT_PREMIUM_MAX = 600.0

# --- Live margin safety (prevents naked-short liquidation) --------------------
# Low leverage allocates a large margin buffer per leg; cross margin lets the whole
# wallet back the position. Both are applied before each opening order.
DEFAULT_LEVERAGE = 1
DEFAULT_MARGIN_MODE = "cross"   # "cross" | "isolated" | "portfolio" | None


def ensure_dirs() -> None:
    """Create the processed/results output directories if missing."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
