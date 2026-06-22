# Double Diagonal (PMCC + PMCP) — Ideal Settings

These are the **default / ideal** dashboard settings for the **Double (PMCC+PMCP)** strategy.
They are the baseline used by the backtest. Use this file to reset the sidebar after experimenting.

## Ideal sidebar values

| Sidebar field | Ideal value |
| --- | --- |
| Contracts per leg (×0.001 BTC) | **1000** |
| Long \|delta\| target (ITM) | **0.70** |
| Short premium target (USD/BTC) | **550** |
| Short DTE min | **1** |
| Short DTE max | **1** |
| Long DTE min | **21** |
| Long DTE max | **45** |
| Long DTE target | **30** |
| Long roll-at DTE | **7** |
| Taker fee | **0.0005** |
| Slippage | **0.01** |
| Start cash (USD) | **100000** |
| Fallback IV | **0.60** |

> Note: the `0.40` and `0.95` shown under "Long |delta| target" are the slider's **minimum and maximum bounds**, not the setting. The ideal value to use is **0.70**.

## Result these settings produced

Backtest on Delta Exchange BTC data (May 2025 – May 2026):

| Metric | Value |
| --- | --- |
| Total return | **+113.14%** |
| CAGR | 110.13% |
| Sharpe | 4.02 |
| Max drawdown | −4.05% |
| Annualised volatility | 18.99% |
| Time in market | 100% |
| Total roll/trade events | 768 |

## What each setting means (quick reference)

- **Contracts per leg** — size of each of the 4 legs; 1000 × 0.001 BTC = 1 BTC notional per leg.
- **Long |delta| target** — how deep ITM the bought call/put hedges are (0.70 ≈ moderately ITM).
- **Short premium target** — USD/BTC premium aimed for when selling each daily short.
- **Short DTE min / max** — the daily shorts are picked 1–3 days to expiry (fast decay) and rolled near expiry.
- **Long DTE min / max / target** — the monthly hedges are bought 21–45 days out, aiming for ~30.
- **Long roll-at DTE** — replace a long hedge once it drops below 7 days to expiry.
- **Taker fee / Slippage** — modelled trading costs per fill.
- **Start cash** — starting account balance for the backtest.
- **Fallback IV** — implied vol used to reprice options that did not trade that day.

## Important caveat

This result assumes the 4-leg structure can always be held without a margin call. The backtest does
**not** model leverage, margin, or liquidation — so treat +113% as the strategy ceiling, not a
guaranteed live outcome.
