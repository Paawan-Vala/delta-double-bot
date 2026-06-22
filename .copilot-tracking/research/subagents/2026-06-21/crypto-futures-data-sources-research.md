# Research: Free Historical Crypto Futures / Perpetual & Underlying Price Data (BTC/ETH)

Status: Complete
Date: 2026-06-21
Purpose: Identify the BEST free sources of historical BTC/ETH futures/perpetual + underlying price data for backtesting, to pair with options data (Deribit).
Verification: All sources below were fetched live from their official sites/docs on 2026-06-21. Items that could NOT be verified this session are explicitly flagged "UNVERIFIED".

## Research Questions (answered)

- Best free, easiest bulk-download of BTC/ETH futures klines -> Binance Vision direct zip download, no API key. URL pattern and history start verified below.
- Best underlying series to pair with Deribit options -> Deribit's own index/perpetual via its public API (no cross-exchange basis). Details below.
- Simple recommended free approach for daily + hourly BTC/ETH futures history -> Binance Vision `um` monthly klines (1h + 1d) for BTCUSDT/ETHUSDT, topped up with CCXT. Details below.

---

## 1. Binance Vision / data.binance.vision (VERIFIED — recommended)

Sources: [github.com/binance/binance-public-data](https://github.com/binance/binance-public-data), [data.binance.vision](https://data.binance.vision/)

- Cost: FREE, NO API KEY. Plain HTTPS download of static files. License MIT.
- Data: market data aggregated into `daily` and `monthly` zipped-CSV files. New `daily` available next day; new `monthly` on the first Monday of the month. All symbols supported.
- Categories: `spot` and `futures`. Futures split into `um` (USD(S)-M / USDT-margined) and `cm` (COIN-M / coin-margined).
- USD-M futures data types VERIFIED present (S3 listing of `data/futures/um/monthly/`): `aggTrades`, `bookTicker`, `fundingRate`, `indexPriceKlines`, `klines`, `markPriceKlines`, `premiumIndexKlines` (daily listing also shows `aggTrades`, `bookDepth`, `bookTicker`, `indexPriceKlines`, `klines`). `markPriceKlines` and `premiumIndexKlines` each individually verified to exist for BTCUSDT. The repo README confirms USD-M futures `klines`, `aggTrades`, and `trades` (from `/fapi/v1/...`) and COIN-M from `/dapi/v1/...`.
- Kline intervals (Binance set): `1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo` (`1mo` used instead of `1M` for case-insensitive filesystems). Verified that futures `1m` and `1h` exist for BTCUSDT. Note: `1s` is a spot-only interval on Binance.
- HISTORY START (VERIFIED): for `BTCUSDT` USD-M 1m monthly klines, the earliest file is `BTCUSDT-1m-2020-01.zip` (LastModified 2021-06-14). `markPriceKlines` and `premiumIndexKlines` for BTCUSDT also start `2020-01`. (Binance USD-M futures launched Sept 2019; the BTCUSDT archive begins 2020-01.)
- FORMAT: `.zip` containing one `.csv`; each `.zip` ships with a sibling `.CHECKSUM` (SHA256) for integrity. Kline CSV columns = openTime, open, high, low, close, volume, closeTime, quoteAssetVolume, count, takerBuyBaseVol, takerBuyQuoteVol, ignore.

### Verified URL patterns (no key, direct download)

- USD-M futures monthly klines (the core target):
  `https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/1m/BTCUSDT-1m-2020-01.zip`
- USD-M futures daily klines:
  `https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2024-01-15.zip`
- Mark-price klines (VERIFIED file exists):
  `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/BTCUSDT/1h/BTCUSDT-1h-2020-01.zip`
- Premium-index klines (VERIFIED file exists):
  `https://data.binance.vision/data/futures/um/monthly/premiumIndexKlines/BTCUSDT/1h/BTCUSDT-1h-2020-01.zip`
- Funding rate (folder verified): `https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/...`
- Spot example from README: `https://data.binance.vision/data/spot/monthly/klines/ADABKRW/1h/ADABKRW-1h-2020-08.zip`
- Browse/UI listing (the pattern in the prompt is correct):
  `https://data.binance.vision/?prefix=data/futures/um/daily/klines/BTCUSDT/1m/`
- Machine-readable directory listing (S3 XML, used to enumerate files/dates):
  `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/monthly/klines/BTCUSDT/1m/`
- Programmatic download examples in README (curl/wget), plus helper scripts in `python/` and `shell/` folders of the repo; `shell/fetch-all-trading-pairs.sh` lists current spot+futures symbols.

### Binance OPTIONS data

- The repo is tagged `options` but the live archive exposes `spot` + `futures (um/cm)` only. A Binance options (EAPI) historical kline archive was NOT confirmed on data.binance.vision this session. Treat Binance options history as NOT available via Vision (UNVERIFIED / likely absent) — Deribit remains the options venue for this project.

### Ease of use

Easiest of all sources: deterministic URLs, no auth, resumable, checksum-verified. Trade-off: many small monthly files to stitch (one per symbol/interval/month) and 1m files are large.

---

## 2. Bybit public data — public.bybit.com (VERIFIED)

Source: [public.bybit.com](https://public.bybit.com/)

- Cost: FREE, NO KEY, direct download.
- Root directories (verified): `kline_for_metatrader4/`, `premium_index/`, `spot_index/`, `trading/`, `spot/`.
- `trading/<SYMBOL>/` = daily gzipped CSV of EXECUTED TRADES (tick data), not klines. Verified for `BTCUSDT` (linear USDT perpetual):
  `https://public.bybit.com/trading/BTCUSDT/BTCUSDT2020-03-25.csv.gz`
  Files run daily from 2020-03-25 to present (verified the listing spans 2020-03-25 .. 2026-06-20).
- HISTORY START (VERIFIED): BTCUSDT linear perp tick data begins 2020-03-25.
- GRANULARITY: tick (trade-by-trade). To get OHLCV you must aggregate yourself. `kline_for_metatrader4/` holds kline data formatted for MT4.
- FORMAT: `.csv.gz`. Typical columns (NOT re-verified column-by-column this session): timestamp, symbol, side, size, price, tickDirection, trdMatchID, grossValue, homeNotional, foreignNotional.
- Use when: you want Bybit-native fills (e.g., for microstructure) or a Bybit cross-check; otherwise heavier than Binance Vision klines.

---

## 3. Deribit historical price API (VERIFIED — best for Deribit-options alignment)

Sources: [docs.deribit.com](https://docs.deribit.com/), method page `public/get_tradingview_chart_data`.

- Cost: FREE, public, NO AUTH for these market-data methods. JSON-RPC over HTTPS or WebSocket. Production base `https://www.deribit.com/api/v2`.
- Same venue as the options -> avoids cross-exchange basis/timestamp mismatch. This is the key advantage.
- Correct method name: `public/get_tradingview_chart_data` (the prompt's "tradingview/get_chart_data" maps to this). VERIFIED parameters/response:
  - Params: `instrument_name` (required; e.g. `BTC-PERPETUAL`, `ETH-PERPETUAL`), `start_timestamp` (required, ms since epoch), `end_timestamp` (required, ms since epoch), `resolution` (required, enum minutes or `1D`): `1, 3, 5, 10, 15, 30, 60, 120, 180, 360, 720, 1D`.
  - Returns: `status` (`ok`/`no_data`), `ticks[]` (ms), `open[]`, `high[]`, `low[]`, `close[]`, `volume[]` (base ccy), `cost[]` (quote ccy).
- Related public market-data methods (verified to exist via official docs index):
  - `public/get_index_chart_data` — historical price-INDEX OHLC (the reference the options are priced/settled against). Index names `btc_usd`, `eth_usd` (see `public/get_index_price_names` / `public/get_supported_index_names`).
  - `public/get_index_price` — current index value.
  - `public/get_funding_rate_history` — hourly historical funding for a PERPETUAL.
  - `public/get_funding_chart_data` — funding chart points.
  - `public/get_mark_price_history` — 5-minute historical mark price.
- GRANULARITY: 1m..1D (chart data); 5m (mark price); hourly (funding). HISTORY: deep (Deribit BTC perpetual since ~2016); retrieve by paging time windows with start/end timestamps.
- Ease: simple unauthenticated GET/RPC; you page by time window. CCXT id `deribit` also wraps it.

---

## 4. OKX / Binance via CCXT (VERIFIED)

Source: CCXT Manual ([docs.ccxt.com](https://docs.ccxt.com/), [github.com/ccxt/ccxt/wiki/Manual](https://github.com/ccxt/ccxt/wiki/Manual)).

- Cost: FREE library (Python/JS/etc.). Public OHLCV needs NO API key. 100+ exchanges, one unified API.
- Core method: `fetch_ohlcv(symbol, timeframe='1m', since=None, limit=None, params={})`. Capability flag `exchange.has['fetchOHLCV']`; supported intervals in `exchange.timeframes`. Returns `[ [ ts_ms, open, high, low, close, volume ], ... ]` (ascending).
- LIMITS / PAGINATION (verified guidance):
  - Per-request candle cap is exchange-specific. The Manual notes "there's a limit on how far back" and on count. Binance allows up to ~1500 candles/request (default 500); CCXT's own `features` example shows binance spot `fetchOHLCV: { paginate: true, limit: 1000 }`. OKX v5 returns ~100 per page (history endpoint ~300). Always check the venue.
  - Manual mantra: "YOU CANNOT GET ALL OBJECTS ... IN ONE CALL." Paginate by looping with `since` = last candle ts + 1, OR enable built-in pagination `params={'paginate': True}` (`paginationCalls` default 10, optional `maxEntriesPerRequest`, OHLCV uses deterministic concurrent paging).
- Mark/Index/Premium history: pass `params={'price': 'mark'|'index'|'premiumIndex'}` to `fetch_ohlcv`, or use convenience methods `fetchMarkOHLCV` / `fetchIndexOHLCV` / `fetchPremiumIndexOHLCV` (e.g. on `binanceusdm`). Funding via `fetchFundingRateHistory`.
- Relevant exchange IDs: `binance` (spot), `binanceusdm` (USD-M futures), `binancecoinm` (COIN-M), `okx`, `bybit`, `deribit`.
- Use when: convenient programmatic top-ups, exchanges without a bulk dump, or multi-venue normalization. For deep 1m Binance history, the Vision bulk dump (source 1) is faster than thousands of paged calls.

---

## 5. CryptoDataDownload — cryptodatadownload.com (VERIFIED)

Source: [cryptodatadownload.com/data/binance](https://www.cryptodatadownload.com/data/binance/)

- Cost: FREE CSV, with tiers:
  - SPOT DAILY: directly downloadable, no account (1,100+ assets). Example ranges seen: AAVEUSDT 2020-10-15 .. 2026-06-20.
  - SPOT HOURLY / MINUTE: require a FREE account (email registration).
  - FUTURES USDT-M (UM) and COIN-M (CM) OHLC: require a FREE account.
- Coverage start: data since late 2017; updated at end of each day.
- GRANULARITY: Daily, Hourly, Minute. FORMAT: CSV.
- Fields: Unix Timestamp, Date (UTC), Symbol, Open, High, Low, Close, Volume (Crypto), Volume Base Ccy, Trade Count.
- Also offers a free-tier Developer REST API (api.cryptodatadownload.com). Plus+ (paid) adds gap-filled/aggregated files.
- Caveats: CDD CSVs historically prepend a header line containing a source URL (skip first row when parsing); occasional gaps/quirks — validate before use. Easiest for quick daily spot pulls; futures/intraday gated behind free signup.

---

## 6. Kaggle datasets (VERIFIED — one notable)

Source: [kaggle.com/datasets/mczielinski/bitcoin-historical-data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)

- "Bitcoin Historical Data" (mczielinski / Zielak): BTC/USD 1-MINUTE OHLCV from Bitstamp, Jan 2012 -> present.
- File `btcusd_1-min_data.csv` (~385 MB), 6 columns (Timestamp, Open, High, Low, Close, Volume). License CC BY-SA 4.0; updated daily.
- LOOKBACK: 2012-01-01 .. present (longest free 1m BTC series found). BTC ONLY (no ETH in this dataset). Spot (Bitstamp), not futures.
- Access: free, but requires a Kaggle account/login to download.
- Other Kaggle sets exist (full-history Binance dumps, etc.) but vary in upkeep; this is the most-cited and best-maintained.

---

## 7. Underlying daily/hourly APIs (CoinGecko / CryptoCompare-CoinDesk / Coin Metrics)

### CoinGecko (VERIFIED)
Source: [docs.coingecko.com](https://docs.coingecko.com/reference/coins-id-market-chart) `/coins/{id}/market_chart`.
- Endpoint: `GET /coins/{id}/market_chart?vs_currency=usd&days=N[&interval=daily|hourly|5m]`. `id` = `bitcoin` / `ethereum`. `days` accepts any integer or `max`.
- Auto-granularity (no `interval`): 1 day = 5-minutely; 2-90 days = hourly; >90 days = daily (00:00 UTC). Overrides: `daily`; `hourly` (up to past 100 days); `5m` (past 10 days, Enterprise only).
- Returns `prices`, `market_caps`, `total_volumes` as `[timestamp_ms, value]` pairs — PRICE only (NOT OHLC), volume is 24h rolling.
- Cost: FREE Demo tier (rate-limited). Note: CoinGecko has moved the free tier toward a free Demo API key (`x-cg-demo-api-key`); a keyless public call may be more rate-limited — confirm current limits. Good for the underlying spot reference, not for futures klines.

### CryptoCompare -> CoinDesk Data API (VERIFIED)
Source: [developers.coindesk.com](https://developers.coindesk.com/documentation/data-api/index_cc_v1_historical_days) (CryptoCompare is now CoinDesk Data).
- Base: `https://data-api.coindesk.com`. Daily OHLCV+ index endpoint:
  `/index/cc/v1/historical/days?market=cadli&instrument=BTC-USD&limit=...&aggregate=...&to_ts=...&response_format=JSON` (also `/hours`, `/minutes`).
- Params: `market` (e.g. `cadli` index), `instrument` (e.g. `BTC-USD`, `ETH-USD`), `limit` (max 5000, default 30), `to_ts` (seconds; for pagination, subtract 86400/3600/60 to avoid the overlapping boundary), `aggregate`, `fill`, `response_format` JSON/CSV. Returns OPEN/HIGH/LOW/CLOSE/VOLUME (+QUOTE_VOLUME, message-level fields).
- Cost: FREE API key tier available (the console shows a "Free Key"). Legacy `https://min-api.cryptocompare.com/data/v2/histoday|histohour|histominute` endpoints are still widely used and free (histominute ~last 7 days), but the platform is migrating to the CoinDesk Data API.

### Coin Metrics community API (UNVERIFIED this session)
- Intended free option: Coin Metrics community/free tier (commonly `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics` with metrics like `PriceUSD` / `ReferenceRateUSD`, assets `btc`/`eth`, daily frequency, no key). The docs page failed to load this session, so endpoint/params are NOT verified here — confirm at [docs.coinmetrics.io](https://docs.coinmetrics.io/) before relying on it. Provides the underlying reference price (not exchange futures klines).

---

## Best Free Download Method (recommendation)

Binance Vision direct zip download — best free, easiest, no key.

- Access: plain HTTPS GET of static `.zip` (CSV inside) + `.CHECKSUM`. No account, no key, resumable.
- Exact pattern (USD-M futures klines):
  `https://data.binance.vision/data/futures/um/{daily|monthly}/klines/{SYMBOL}/{interval}/{SYMBOL}-{interval}-{YYYY-MM[-DD]}.zip`
  e.g. `.../data/futures/um/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01.zip`.
- Granularity: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo (plus markPriceKlines / premiumIndexKlines / indexPriceKlines / fundingRate folders).
- Format: zipped CSV (OHLCV + quote volume + trade count + taker volumes), SHA256 checksums.
- History (BTCUSDT um): from 2020-01.
- Enumerate available files/dates via the S3 XML listing URL, then bulk-fetch with the helper scripts in `binance/binance-public-data`.

## Aligning the Underlying with Deribit Options

For a strategy whose OPTIONS come from Deribit, prefer a Deribit-native underlying to avoid cross-exchange basis and clock mismatch:

- Best match = Deribit price INDEX via `public/get_index_chart_data` (index `btc_usd` / `eth_usd`). Deribit options are priced and settled against this index, so it is the most consistent "spot/underlying" for pricing, Greeks, and settlement in a backtest.
- For the tradeable hedge instrument, use `public/get_tradingview_chart_data` on `BTC-PERPETUAL` / `ETH-PERPETUAL` (same venue) for perp OHLC; add `public/get_funding_rate_history` if you model carry, and `public/get_mark_price_history` for mark-based PnL/margin.
- Binance `BTCUSDT`/`ETHUSDT` USD-M futures (from Binance Vision) is an acceptable proxy — extremely correlated and far easier to bulk-download — but it carries a small Binance-vs-Deribit basis and timestamping difference. Fine for daily/hourly backtests; less ideal for precise intraday option pricing/settlement. If you use Binance for convenience, still pull the Deribit index for the actual option pricing/settlement leg.

## Simple Recommended Free Approach (daily + hourly BTC/ETH futures)

1. Bulk-download Binance Vision `um` MONTHLY klines for `BTCUSDT` and `ETHUSDT` at `1h` and `1d` (add `1m` only if you need intraday); unzip, verify checksums, concatenate. One-time, no key.
2. Keep recent data current with CCXT `binanceusdm.fetch_ohlcv(symbol, '1h'|'1d', since=...)` (loop/paginate).
3. If the backtest's options are Deribit, additionally pull the Deribit index (`get_index_chart_data`, `btc_usd`/`eth_usd`) and/or `BTC-PERPETUAL`/`ETH-PERPETUAL` (`get_tradingview_chart_data`) to price/settle the option leg on its native venue.

## Unverifiable / flagged claims

- Coin Metrics community API endpoint/params: NOT verified this session (docs failed to load).
- Bybit `trading/*.csv.gz` exact column order: not re-verified column-by-column.
- Binance OPTIONS historical klines on data.binance.vision: not found / treat as unavailable.
- CoinGecko free keyless-vs-demo-key access and current rate limits may have changed; confirm before building on it.
- CryptoCompare legacy `min-api.cryptocompare.com` endpoints still work but are being migrated to `data-api.coindesk.com`.

## Open questions for the user

- Which timeframe(s) do you actually need — 1h/1d only, or 1m? (Determines whether the large 1m bulk pull from Binance Vision is worth it.)
- Are linear USDT perps (BTCUSDT/ETHUSDT) acceptable as the futures series, or do you need COIN-M/inverse, or strictly Deribit-native?
- Do you need funding + mark/index series too (for financing/carry and margin in the backtest), or just price OHLCV?

## Sources List (URLs)

- Binance public data repo: https://github.com/binance/binance-public-data
- Binance Vision site: https://data.binance.vision/
- Binance Vision futures klines (browse): https://data.binance.vision/?prefix=data/futures/um/daily/klines/BTCUSDT/1m/
- Binance Vision S3 listing (example): https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/monthly/klines/BTCUSDT/1m/
- Bybit public data: https://public.bybit.com/ (e.g. https://public.bybit.com/trading/BTCUSDT/)
- Deribit API docs: https://docs.deribit.com/ (method: public/get_tradingview_chart_data, public/get_index_chart_data, public/get_funding_rate_history, public/get_mark_price_history)
- CCXT manual: https://docs.ccxt.com/ and https://github.com/ccxt/ccxt/wiki/Manual
- CryptoDataDownload: https://www.cryptodatadownload.com/data/binance/
- Kaggle BTC 1-min: https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data
- CoinGecko market_chart: https://docs.coingecko.com/reference/coins-id-market-chart
- CoinDesk Data (ex-CryptoCompare): https://developers.coindesk.com/documentation/data-api/index_cc_v1_historical_days
- Coin Metrics docs (verify): https://docs.coinmetrics.io/
