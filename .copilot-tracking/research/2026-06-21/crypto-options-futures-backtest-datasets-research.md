<!-- markdownlint-disable-file -->
# Task Research: Backtest Datasets for BTC/ETH Options + Futures (PMCC / PMCP)

Goal: Find the best available HISTORICAL datasets to backtest a Poor Man's Covered Call / Poor Man's Covered Put diagonal on crypto (BTC, ETH). Need BOTH (1) options chain history (strikes, expiries, prices, IV, ideally greeks) and (2) the underlying futures/perpetual price history, aligned in time. Identify free vs paid, lookback, granularity, format, and exact download/access method, then recommend a concrete stack and how to download it.

> Educational research only — NOT financial advice. Backtests are only as good as the data (survivorship, snapshot timing, fees, slippage, liquidity). Crypto options liquidity concentrates on Deribit.

## Task Implementation Requests

* Find the best dataset(s) for BTC/ETH FUTURES + OPTIONS history for backtesting.
* Prefer BTC/ETH. Identify free options first, paid as upgrade.
* Provide exact download/access method (URLs, APIs, Python clients, scripts).

## Scope and Success Criteria

* Scope: Historical crypto derivatives data for backtesting an options income/diagonal strategy. Options venues: primarily Deribit (dominant BTC/ETH options). Futures/perps: Binance, Bybit, Deribit, OKX.
* Assumptions (stated; to confirm):
  * Programmatic (Python) workflow is fine (workspace is a trading algo).
  * Daily/hourly granularity is enough for a multi-week diagonal with a daily short leg; tick is optional.
  * Free/cheap preferred; willing to use an API key.
* Success Criteria:
  * Ranked dataset recommendations (free + paid) for options and for futures.
  * Exact access method, lookback, granularity, format for each.
  * A concrete "download this" plan and the data fields needed to backtest PMCC/PMCP.

## Candidate Sources (to evaluate)

| Source | Type | Options? | Futures? | Cost |
|--------|------|----------|----------|------|
| Deribit API | Exchange API | Yes (BTC/ETH) | Yes (perp/futures) | Free (rate-limited) |
| Tardis.dev | Data vendor | Yes (full depth, IV) | Yes | Paid + free samples |
| Amberdata | Data vendor | Yes | Yes | Paid |
| Kaiko | Data vendor | Yes | Yes | Paid |
| CoinAPI | Data vendor | Yes | Yes | Free tier + paid |
| Laevitas / GVol | Analytics | Yes | Yes | Free + paid |
| Binance Vision | Exchange dumps | Limited | Yes (free CSV) | Free |
| Bybit public data | Exchange dumps | Limited | Yes | Free |
| CryptoDataDownload | Aggregator | No/limited | Some | Free |
| Kaggle | Community | Maybe | Yes | Free |

## Outline

1. Best OPTIONS history source(s) for BTC/ETH (free + paid), fields, lookback, access
2. Best FUTURES/perp history source(s), granularity, download
3. Recommended free stack + paid upgrade
4. Exact download plan (links / API / Python)
5. Data fields required to backtest PMCC/PMCP
6. Caveats (snapshot timing, fees, liquidity, survivorship)

## Potential Next Research

* Confirm granularity needed (daily vs intraday) and whether IV/greeks are required or computable.

## Research Executed

* Subagent: crypto options data sources (output: .copilot-tracking/research/subagents/2026-06-21/crypto-options-data-sources-research.md)
* Subagent: crypto futures data sources (output: .copilot-tracking/research/subagents/2026-06-21/crypto-futures-data-sources-research.md)
* All 14 sources fetched live and verified 2026-06-21.

## Key Discoveries

### The core reality

* FUTURES history is easy + free. OPTIONS history is the hard part — getting clean historical option CHAINS for arbitrary past dates is NOT freely available; you either collect-forward (free) or pay a vendor (Tardis/Laevitas).

### Options data (BTC/ETH = Deribit-dominated)

* Deribit public API — FREE, no key needed for public data. IV + greeks INCLUDED (`public/ticker`: mark_price, bid_iv/ask_iv/mark_iv, full greeks delta/gamma/vega/theta/rho, underlying_price, open_interest). BTC options since ~2016, ETH since 2019.
  * CRITICAL LIMIT: `get_instruments?expired=true` returns only RECENTLY expired contracts, and ticker/greeks are current-state — so there is NO clean historical full-chain snapshot for arbitrary past dates. You CAN get historical trades (`get_last_trades_by_instrument_and_time`) and 5-min mark-price history (`get_mark_price_history`) for KNOWN instruments. Practical free route = snapshot the chain yourself daily going forward (collect-forward).
* Tardis.dev — BEST PAID. Ready `options_chain` CSV (gzip) with strikes/expiries/OI + bid/ask/mark IV + full greeks, Deribit data since 2019-03-30 (options_chain ~2019-10-01). Python client `tardis-dev`. FREE samples: the FIRST DAY OF EACH MONTH downloads without an API key (incl. options_chain) — use for format validation and rough monthly backtests. Pricing is quote-based (not public).
* Laevitas — cheap middle: ~$50/mo Premium = 1yr history + CSV export + an options backtester; ~$500/mo API. Greeks/IV included.
* CoinAPI — trades/quotes/OHLCV/order books only; NO greeks/IV/option-chain product. Not for options.
* Amberdata / Kaiko / GVol — paid/enterprise, no public pricing, overkill for a solo backtest. (Amberdata acquired by Kaiko; GVol now "Amberdata Derivatives.")
* Kaggle — only a point-in-time snapshot, no time series → unusable for a multi-week backtest.

### Futures / underlying data

* Binance Vision (data.binance.vision) — BEST FREE bulk download, no API key, static `.zip` (CSV) + SHA256 checksums, MIT license.
  * URL pattern: `https://data.binance.vision/data/futures/um/{daily|monthly}/klines/{SYMBOL}/{interval}/{SYMBOL}-{interval}-{YYYY-MM[-DD]}.zip` (e.g., `.../futures/um/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01.zip`).
  * Intervals 1m…1mo + markPriceKlines, premiumIndexKlines, indexPriceKlines, fundingRate. BTCUSDT USD-M 1m since 2020-01. Binance options NOT on Vision.
* Deribit-native underlying (best for aligning with Deribit options, avoids cross-exchange basis): `public/get_index_chart_data` (btc_usd/eth_usd index — options settle against it) + `public/get_tradingview_chart_data` on BTC-PERPETUAL/ETH-PERPETUAL (resolutions 1..720,1D; public, no auth).
* CCXT (`binanceusdm.fetch_ohlcv`) for incremental top-ups. Bybit public data, CryptoDataDownload as alternates.

### Fields needed to backtest PMCC/PMCP

* Underlying per timestamp: Deribit index (btc_usd) or perp close.
* Option chain per snapshot date: instrument name (e.g., BTC-27JUN25-60000-C), type (C/P), strike, expiry, mark_price (coin terms + USD), mark_iv, delta (for strike selection), bid/ask, open_interest.
* PMCC needs: long ~monthly call ~0.80 delta (deep ITM) + short daily/short-dated call ~0.30 delta. PMCP = puts. Plus Deribit fees (maker/taker), and note Deribit options are priced in the coin (BTC/ETH), settled to the index.

## Technical Scenarios

### Selected approach — recommended dataset stack

* FREE stack (start now): (1) Futures/underlying = Binance Vision bulk zips (BTCUSDT/ETHUSDT 1h+1d) and/or Deribit index/perp via API. (2) Options = run a daily Deribit chain collector going forward (free, includes IV+greeks) + pull Tardis free 1st-of-month samples for historical spot-checks. Best when you can wait to accumulate forward data or only need monthly-granularity historical points.
* PAID upgrade (true history now): Tardis.dev options_chain (Deribit, 2019→now) via `tardis-dev` Python client — cleanest ready-made history with IV/greeks. Cheaper alternative: Laevitas ~$50/mo (1yr history + built-in backtester).
* Underlying alignment: pair Deribit options with the Deribit index/perp (same venue) to avoid basis mismatch; Binance Vision is an acceptable easy proxy for daily/hourly.

### Download plan (exact)

* Futures (free, runnable now): download Binance Vision zips by URL pattern (above); unzip CSVs. Use the monthly files for bulk, daily for recent top-up. No key.
* Options history (paid path): `pip install tardis-dev`; use `datasets.download` for `deribit` `options_chain` over the date range; or grab a free sample at `https://datasets.tardis.dev/v1/deribit/options_chain/2024/01/01/OPTIONS.csv.gz` (1st-of-month, no key) to validate format.
* Options (free path): write a scheduled Python job hitting Deribit `public/get_instruments` (BTC/ETH options) then `public/ticker` per instrument, saving a daily CSV snapshot (mark, IV, greeks, OI). Accumulates a backtestable chain going forward.

### Considered alternatives (not selected)

* CoinAPI / Kaggle for options — rejected (no chain/greeks; or snapshot-only).
* Amberdata/Kaiko/GVol — rejected for a solo backtest (enterprise pricing, overkill).
* Pure Deribit free for historical chains — limited (no arbitrary past-date full chain); good only for collect-forward + known-instrument trades/mark.

### Open items (need user input)

* History span needed (2021→now vs full 2019→now) → decides Tardis tier vs free collect-forward.
* Granularity for the daily short-leg roll: daily snapshot chains enough, or intraday needed?
* Budget: strictly free (Deribit collect-forward + Tardis monthly samples), ~$50/mo (Laevitas), or a Tardis subscription?
