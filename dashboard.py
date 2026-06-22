#!/usr/bin/env python3
"""Phase 5 — Streamlit dashboard for the PMCC/PMCP BTC options backtest.

Interactive front-end over the `backtest` package. The heavy preprocessing
(`data/processed/*.parquet`) is done once via the CLI modules; this app re-runs only
the *signal + engine* layer in-memory whenever a sidebar parameter changes, so it
stays responsive.

Run:
    .\\.venv\\Scripts\\streamlit.exe run dashboard.py
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from backtest import config, indicators, metrics as metrics_mod
from backtest.engine import BacktestEngine
from backtest.engine_delta import DeltaEngine
from backtest.engine_double import DoubleEngine, DoubleParams
from backtest.indicators import DirectionParams
from backtest.strategy import PriceBook, StrategyParams
from backtest.strategy_delta import PriceBookDelta, StrategyParamsDelta

REGIME_COLORS = {"bull": "rgba(38, 166, 91, 0.12)", "bear": "rgba(229, 57, 53, 0.12)"}
LINE = {"close": "#e0e0e0", "ema_fast": "#42a5f5", "ema_slow": "#ffa726", "ema_regime": "#ab47bc"}


# --------------------------------------------------------------------------- #
# Cached data + compute layer
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def load_futures() -> pd.DataFrame:
    """Load the daily BTCUSD candles (cached)."""
    return indicators.load_daily()


@st.cache_resource(show_spinner="Building option price book (one-time)…")
def get_book() -> PriceBook:
    """Build the PriceBook from processed parquet once and reuse it."""
    options_df = pd.read_parquet(config.OPTIONS_DAILY_PARQUET)
    return PriceBook(options_df, load_futures())


@st.cache_data(show_spinner="Running backtest…")
def run_backtest(dir_params: dict, strat_params: dict) -> dict:
    """Recompute direction + run the engine for the given params (memoized)."""
    direction = indicators.compute_direction(load_futures(), DirectionParams(**dir_params))
    engine = BacktestEngine(direction, get_book(), StrategyParams(**strat_params))
    out = engine.run()
    m = metrics_mod.compute_metrics(out["equity"], out["trades"])
    return {"direction": direction, "equity": out["equity"], "trades": out["trades"], "metrics": m}


@st.cache_resource(show_spinner="Building delta price book (one-time)…")
def get_book_delta() -> PriceBookDelta:
    """Build the delta-aware PriceBook from the delta-augmented parquet once and reuse it."""
    options_df = pd.read_parquet(config.OPTIONS_DAILY_DELTA_PARQUET)
    return PriceBookDelta(options_df, load_futures())


@st.cache_data(show_spinner="Running delta/premium backtest…")
def run_backtest_delta(dir_params: dict, strat_params: dict) -> dict:
    """Recompute direction + run the delta/premium engine for the given params (memoized)."""
    direction = indicators.compute_direction(load_futures(), DirectionParams(**dir_params))
    engine = DeltaEngine(direction, get_book_delta(), StrategyParamsDelta(**strat_params))
    out = engine.run()
    m = metrics_mod.compute_metrics(out["equity"], out["trades"])
    return {"direction": direction, "equity": out["equity"], "trades": out["trades"], "metrics": m}


@st.cache_data(show_spinner="Running double-diagonal backtest…")
def run_backtest_double(strat_params: dict) -> dict:
    """Run the continuous double-diagonal (PMCC+PMCP) engine — non-directional (memoized).

    Direction is still computed with defaults purely to shade the price chart; the engine
    itself ignores it and holds all four legs continuously.
    """
    futures = load_futures()
    direction = indicators.compute_direction(futures, DirectionParams())
    engine = DoubleEngine(get_book_delta(), DoubleParams(**strat_params), futures.index)
    out = engine.run()
    m = metrics_mod.compute_metrics(out["equity"], out["trades"])
    return {"direction": direction, "equity": out["equity"], "trades": out["trades"], "metrics": m}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def regime_segments(direction: pd.Series) -> list[tuple[pd.Timestamp, pd.Timestamp, str]]:
    """Collapse a per-day direction series into contiguous (start, end, label) runs."""
    segments: list[tuple[pd.Timestamp, pd.Timestamp, str]] = []
    if direction.empty:
        return segments
    idx = direction.index
    cur_label = direction.iloc[0]
    start = idx[0]
    for i in range(1, len(direction)):
        if direction.iloc[i] != cur_label:
            segments.append((start, idx[i], cur_label))
            start, cur_label = idx[i], direction.iloc[i]
    segments.append((start, idx[-1], cur_label))
    return [s for s in segments if s[2] in REGIME_COLORS]


def price_regime_figure(direction: pd.DataFrame, trades: pd.DataFrame) -> go.Figure:
    """Price + EMAs + ADX with shaded bull/bear regime and trade markers."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.04,
        subplot_titles=("BTCUSD price · EMA20/50/200 · regime", "ADX(14) · DI"),
    )
    for col, color in LINE.items():
        if col in direction:
            fig.add_trace(
                go.Scatter(x=direction.index, y=direction[col], name=col, line=dict(color=color, width=1.4)),
                row=1, col=1,
            )
    for start, end, label in regime_segments(direction["direction"]):
        fig.add_vrect(x0=start, x1=end, fillcolor=REGIME_COLORS[label], line_width=0, row=1, col=1)

    if not trades.empty:
        opens = trades[trades["event"] == "open"]
        closes = trades[trades["event"] == "close"]
        spot_at = direction["close"]
        if not opens.empty:
            fig.add_trace(go.Scatter(
                x=opens["date"], y=spot_at.reindex(pd.to_datetime(opens["date"])).to_numpy(),
                mode="markers", name="open", marker=dict(symbol="triangle-up", size=11, color="#26a65b")),
                row=1, col=1)
        if not closes.empty:
            fig.add_trace(go.Scatter(
                x=closes["date"], y=spot_at.reindex(pd.to_datetime(closes["date"])).to_numpy(),
                mode="markers", name="close", marker=dict(symbol="x", size=10, color="#e53935")),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=direction.index, y=direction["adx"], name="ADX", line=dict(color="#fdd835", width=1.4)), row=2, col=1)
    fig.add_trace(go.Scatter(x=direction.index, y=direction["plus_di"], name="+DI", line=dict(color="#26a65b", width=1)), row=2, col=1)
    fig.add_trace(go.Scatter(x=direction.index, y=direction["minus_di"], name="-DI", line=dict(color="#e53935", width=1)), row=2, col=1)
    fig.add_hline(y=config.ADX_THRESHOLD, line=dict(color="#888", dash="dash"), row=2, col=1)
    fig.update_layout(height=620, hovermode="x unified", legend=dict(orientation="h", y=1.04), margin=dict(t=60, b=20))
    return fig


def equity_figure(equity: pd.DataFrame) -> go.Figure:
    """Equity curve over an underwater drawdown panel."""
    eq = equity["equity"].astype(float)
    drawdown = (eq / eq.cummax() - 1.0) * 100
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.68, 0.32], vertical_spacing=0.05,
                        subplot_titles=("Equity (USD)", "Drawdown (%)"))
    fig.add_trace(go.Scatter(x=eq.index, y=eq, name="equity", line=dict(color="#42a5f5", width=1.6)), row=1, col=1)
    fig.add_hline(y=float(eq.iloc[0]), line=dict(color="#888", dash="dot"), row=1, col=1)
    fig.add_trace(go.Scatter(x=drawdown.index, y=drawdown, name="drawdown", fill="tozeroy",
                             line=dict(color="#e53935", width=1)), row=2, col=1)
    fig.update_layout(height=520, hovermode="x unified", showlegend=False, margin=dict(t=50, b=20))
    return fig


def _signal_params() -> dict:
    """Render the shared signal-parameter widgets and return them as a dict."""
    st.sidebar.header("Signal parameters")
    dp = DirectionParams()
    return {
        "ema_fast": st.sidebar.number_input("EMA fast", 2, 100, dp.ema_fast),
        "ema_slow": st.sidebar.number_input("EMA slow", 5, 200, dp.ema_slow),
        "ema_regime": st.sidebar.number_input("EMA regime", 20, 400, dp.ema_regime),
        "adx_period": st.sidebar.number_input("ADX period", 5, 50, dp.adx_period),
        "adx_threshold": st.sidebar.slider("ADX threshold", 10.0, 40.0, float(dp.adx_threshold), 0.5),
        "weekly_span": st.sidebar.number_input("Weekly EMA span", 2, 30, dp.weekly_span),
    }


def sidebar_params() -> tuple[dict, dict]:
    """Render sidebar widgets for the original (moneyness) strategy."""
    dir_params = _signal_params()
    st.sidebar.header("Strategy parameters")
    sp = StrategyParams()
    strat_params = {
        "contracts": st.sidebar.number_input("Contracts (×0.001 BTC)", 1, 100_000, sp.contracts, step=100),
        "short_otm": st.sidebar.slider("Short OTM offset", 0.0, 0.15, float(sp.short_otm), 0.005),
        "long_itm": st.sidebar.slider("Long ITM offset", 0.0, 0.30, float(sp.long_itm), 0.01),
        "short_dte_min": st.sidebar.number_input("Short DTE min", 0, 10, sp.short_dte_min),
        "short_dte_max": st.sidebar.number_input("Short DTE max", 1, 14, sp.short_dte_max),
        "long_dte_min": st.sidebar.number_input("Long DTE min", 7, 60, sp.long_dte_min),
        "long_dte_max": st.sidebar.number_input("Long DTE max", 14, 120, sp.long_dte_max),
        "long_dte_target": st.sidebar.number_input("Long DTE target", 14, 90, sp.long_dte_target),
        "long_roll_min_dte": st.sidebar.number_input("Long roll-at DTE", 1, 30, sp.long_roll_min_dte),
        "taker_fee": st.sidebar.number_input("Taker fee", 0.0, 0.01, float(sp.taker_fee), step=0.0001, format="%.4f"),
        "slippage": st.sidebar.number_input("Slippage", 0.0, 0.05, float(sp.slippage), step=0.001, format="%.3f"),
        "start_cash": st.sidebar.number_input("Start cash (USD)", 1_000.0, 10_000_000.0, float(sp.start_cash), step=1_000.0),
        "default_iv": st.sidebar.slider("Fallback IV", 0.1, 2.0, float(sp.default_iv), 0.05),
    }
    return dir_params, strat_params


def sidebar_params_delta() -> tuple[dict, dict]:
    """Render sidebar widgets for the delta/premium strategy."""
    dir_params = _signal_params()
    st.sidebar.header("Strategy parameters (delta/premium)")
    sp = StrategyParamsDelta()
    strat_params = {
        "contracts": st.sidebar.number_input("Contracts (×0.001 BTC)", 1, 100_000, sp.contracts, step=100),
        "long_delta_target": st.sidebar.slider("Long |delta| target (ITM)", 0.40, 0.95, float(sp.long_delta_target), 0.05),
        "short_premium_target": st.sidebar.number_input("Short premium target (USD/BTC)", 50.0, 5_000.0, float(sp.short_premium_target), step=25.0),
        "short_dte_min": st.sidebar.number_input("Short DTE min", 0, 10, sp.short_dte_min),
        "short_dte_max": st.sidebar.number_input("Short DTE max", 1, 14, sp.short_dte_max),
        "long_dte_min": st.sidebar.number_input("Long DTE min", 7, 60, sp.long_dte_min),
        "long_dte_max": st.sidebar.number_input("Long DTE max", 14, 120, sp.long_dte_max),
        "long_dte_target": st.sidebar.number_input("Long DTE target", 14, 90, sp.long_dte_target),
        "long_roll_min_dte": st.sidebar.number_input("Long roll-at DTE", 1, 30, sp.long_roll_min_dte),
        "taker_fee": st.sidebar.number_input("Taker fee", 0.0, 0.01, float(sp.taker_fee), step=0.0001, format="%.4f"),
        "slippage": st.sidebar.number_input("Slippage", 0.0, 0.05, float(sp.slippage), step=0.001, format="%.3f"),
        "start_cash": st.sidebar.number_input("Start cash (USD)", 1_000.0, 10_000_000.0, float(sp.start_cash), step=1_000.0),
        "default_iv": st.sidebar.slider("Fallback IV", 0.1, 2.0, float(sp.default_iv), 0.05),
    }
    return dir_params, strat_params


def sidebar_params_double() -> dict:
    """Render sidebar widgets for the continuous double-diagonal strategy (no signal layer)."""
    st.sidebar.header("Strategy parameters (double diagonal)")
    st.sidebar.caption("Non-directional: always holds 4 legs (long ITM call+put, short daily call+put).")
    sp = DoubleParams()
    return {
        "contracts": st.sidebar.number_input("Contracts per leg (×0.001 BTC)", 1, 100_000, sp.contracts, step=100),
        "long_delta_target": st.sidebar.slider("Long |delta| target (ITM)", 0.40, 0.95, float(sp.long_delta_target), 0.05),
        "short_premium_target": st.sidebar.number_input("Short premium target (USD/BTC)", 50.0, 5_000.0, float(sp.short_premium_target), step=25.0),
        "short_dte_min": st.sidebar.number_input("Short DTE min", 0, 10, sp.short_dte_min),
        "short_dte_max": st.sidebar.number_input("Short DTE max", 1, 14, sp.short_dte_max),
        "long_dte_min": st.sidebar.number_input("Long DTE min", 7, 60, sp.long_dte_min),
        "long_dte_max": st.sidebar.number_input("Long DTE max", 14, 120, sp.long_dte_max),
        "long_dte_target": st.sidebar.number_input("Long DTE target", 14, 90, sp.long_dte_target),
        "long_roll_min_dte": st.sidebar.number_input("Long roll-at DTE", 1, 30, sp.long_roll_min_dte),
        "taker_fee": st.sidebar.number_input("Taker fee", 0.0, 0.01, float(sp.taker_fee), step=0.0001, format="%.4f"),
        "slippage": st.sidebar.number_input("Slippage", 0.0, 0.05, float(sp.slippage), step=0.001, format="%.3f"),
        "start_cash": st.sidebar.number_input("Start cash (USD)", 1_000.0, 10_000_000.0, float(sp.start_cash), step=1_000.0),
        "default_iv": st.sidebar.slider("Fallback IV", 0.1, 2.0, float(sp.default_iv), 0.05),
    }


# --------------------------------------------------------------------------- #
# Page
# --------------------------------------------------------------------------- #
def main() -> None:
    """Render the dashboard page."""
    st.set_page_config(page_title="PMCC/PMCP BTC Backtest", layout="wide")
    st.title("Poor Man's Covered Call / Put — BTC diagonal backtest")
    st.caption(
        "Direction from a futures indicator stack (200-EMA regime · 20/50-EMA trigger · ADX(14) · "
        "weekly agreement). PMCC (bullish) shorts a daily call against a monthly ITM call; PMCP (bearish) "
        "mirrors with puts. Delta Exchange BTC data, May 2025 – May 2026."
    )
    st.warning(
        "Feasibility build — Delta Exchange **trades-only** data (no order-book greeks), BTC only, ~13 months. "
        "Untraded options are repriced with Black-76 + an ATM-IV estimate. Treat results as illustrative.",
        icon="⚠️",
    )

    strategy = st.sidebar.radio(
        "Strategy", ["Original (moneyness)", "Delta + premium", "Double (PMCC+PMCP)"], index=0,
        help=(
            "Original: strikes by % moneyness. Delta + premium: long leg by |delta| (ITM), short by traded "
            "premium. Double: the videos' non-directional method — long ITM call+put and short daily call+put "
            "held continuously (4 legs, always on)."
        ),
    )
    if strategy.startswith("Double"):
        strat_params = sidebar_params_double()
        result = run_backtest_double(strat_params)
    elif strategy.startswith("Delta"):
        dir_params, strat_params = sidebar_params_delta()
        result = run_backtest_delta(dir_params, strat_params)
    else:
        dir_params, strat_params = sidebar_params()
        result = run_backtest(dir_params, strat_params)
    direction, equity, trades, m = result["direction"], result["equity"], result["trades"], result["metrics"]

    # --- metric cards ---
    r1 = st.columns(4)
    r1[0].metric("Final equity", f"${m['final_equity']:,.0f}", f"{m['total_return_pct']:+.2f}%")
    r1[1].metric("CAGR", f"{m['cagr_pct']:.2f}%")
    r1[2].metric("Sharpe", f"{m['sharpe']:.2f}")
    r1[3].metric("Max drawdown", f"{m['max_drawdown_pct']:.2f}%")
    r2 = st.columns(4)
    r2[0].metric("Trades", f"{m['num_trades']}", f"{m['win_rate_pct']:.0f}% win")
    r2[1].metric("Time in market", f"{m['time_in_market_pct']:.1f}%")
    r2[2].metric("PMCC / PMCP", f"{m['pmcc_trades']} / {m['pmcp_trades']}")
    r2[3].metric("Bull / Bear days", f"{m['bull_days']} / {m['bear_days']}")

    tab_price, tab_equity, tab_trades = st.tabs(["Price & regime", "Equity & drawdown", "Trades"])
    with tab_price:
        st.plotly_chart(price_regime_figure(direction, trades), use_container_width=True)
    with tab_equity:
        st.plotly_chart(equity_figure(equity), use_container_width=True)
    with tab_trades:
        if trades.empty:
            st.info("No trades for these parameters.")
        elif "pnl" in trades.columns:
            t = trades.sort_values("date").reset_index(drop=True)
            t["campaign"] = (t["event"] == "open").cumsum()
            closes = t[t["event"] == "close"][["date", "direction", "reason", "rolls", "pnl"]]
            st.subheader("Closed campaigns")
            st.dataframe(closes, use_container_width=True, hide_index=True)

            st.subheader("Per-campaign drilldown")
            campaigns = [c for c in t["campaign"].unique() if c >= 1]
            if campaigns:
                pick = st.selectbox("Campaign", campaigns, format_func=lambda c: f"#{c}")
                st.dataframe(
                    t[t["campaign"] == pick].drop(columns=["campaign"]).dropna(axis=1, how="all"),
                    use_container_width=True, hide_index=True,
                )
            with st.expander("Full event log"):
                st.dataframe(t.drop(columns=["campaign"]), use_container_width=True, hide_index=True)
        else:
            # Continuous double-diagonal: no discrete campaigns — show an event summary + log.
            t = trades.sort_values("date").reset_index(drop=True)
            st.subheader("Event summary")
            st.dataframe(
                t["event"].value_counts().rename_axis("event").reset_index(name="count"),
                use_container_width=True, hide_index=True,
            )
            with st.expander("Full event log"):
                st.dataframe(t, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
