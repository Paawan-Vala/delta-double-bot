<!-- markdownlint-disable-file -->
# Crypto Options Historical Data Sources Research (BTC/ETH)

## Research Scope

Find the BEST sources of HISTORICAL crypto options data for BTC and ETH, for backtesting an
options diagonal strategy (Poor Man's Covered Call / Put — long-dated long leg, daily/short-dated
short leg rolled over multiple weeks).

Educational research. Verify facts from actual source websites/docs. Do NOT fabricate pricing,
lookback, or feature claims. Where a number cannot be verified, say so explicitly.

## Research Questions

1. Deribit public API for historical options data: which historical endpoints exist
   (get_instruments incl. expired, public/get_last_trades_by_instrument,
   tradingview/get_chart_data, get_book_summary_by_currency), how far back data goes, rate limits,
   whether IV/greeks/mark price are provided, whether a free API key is needed.
2. Tardis.dev: coverage start date, data types, FORMAT (CSV/normalized), free sample availability,
   Python client (tardis-machine / tardis-dev), pricing tiers.
3. Amberdata: crypto options historical data + greeks/IV; coverage and access (API).
4. CoinAPI: does it offer options data? free-tier limits, format.
5. Laevitas / Genesis Volatility (GVol): crypto options analytics/history; free historical or API.
6. Kaggle / public datasets: any usable BTC/ETH options history datasets (name + lookback).
7. Kaiko: institutional options data (paid/enterprise).

### Key Questions To Answer

- BEST FREE way to get BTC/ETH options history (likely Deribit API directly).
- BEST PAID/highest-quality option (likely Tardis.dev).
- Does any source provide ready greeks/IV, or must they be computed (Black-76 / Black-Scholes)?

### Per-Source Fields To Document

- Data available (chains/strikes/expiries, mark price, IV, greeks)
- HISTORY LOOKBACK (start date)
- GRANULARITY (tick/snapshot/daily)
- FORMAT
- ACCESS METHOD (REST API / Python client / CSV download)
- COST (free / free-tier / paid + rough tier)
- SUITABILITY for backtesting a multi-week diagonal with a daily short leg

---

## Source 1: Deribit

Deribit is the dominant BTC/ETH options venue (the large majority of global crypto options open
interest and volume). Its public API is the canonical FREE primary source for BTC/ETH options data.

**Verified from https://docs.deribit.com/ (API v2.1.1):**

- Interfaces: JSON-RPC over WebSocket (preferred), JSON-RPC over HTTP/REST, FIX 4.4.
  - Production HTTP base: `https://www.deribit.com/api/v2`; WS: `wss://www.deribit.com/ws/api/v2`.
- Public market-data methods are usable WITHOUT authentication (doc: "Public methods can be used
  without authentication"). A free API key (OAuth2) is OPTIONAL but recommended — authenticated
  traffic gets higher, per-sub-account credit limits; unauthenticated public calls are rate-limited
  per-IP.

### Data available (verified endpoints)

- `public/get_instruments` (currency, kind=`option`, `expired` bool): full option contract specs —
  `strike`, `option_type` (call/put), `expiration_timestamp`, `creation_timestamp`, `contract_size`,
  `tick_size`, `settlement_currency`, `state`. Set `expired=true` to list **recently expired**
  instruments. NOTE: docs only say "recently expired" — they do NOT state the exact window (commonly
  observed to be only a few days; UNVERIFIED exact number). This is the key gap for the free route.
- `public/ticker` (per instrument) — for options returns: `mark_price`, `last_price`,
  best bid/ask, `open_interest`, `index_price`, `underlying_price`, `interest_rate`,
  `bid_iv`, `ask_iv`, `mark_iv`, and a `greeks` object: `delta`, `gamma`, `vega`, `theta`, `rho`.
  Greeks/IV are computed BY Deribit (standard Black-Scholes; theta = min(1-day, lifetime theta)).
- `public/get_order_book` / `get_order_book_by_instrument_id` — bids/asks + mark price, IV, greeks.
- `public/get_last_trades_by_instrument` and `..._and_time` — historical trade prints (price,
  amount, direction, timestamp, trade_id, and per-trade `iv` for options); time-range queries.
- `public/get_last_trades_by_currency` and `..._and_time` — all-instrument trade history per currency.
- `public/get_book_summary_by_currency` / `..._by_instrument` — per-instrument summary: open interest,
  24h volume, best bid/ask, last price, **mark price** (snapshot, current only).
- `public/get_tradingview_chart_data` — OHLCV candles per instrument over a time range (good for
  per-contract price history at chosen resolutions).
- `public/get_mark_price_history` — **5-minute** historical mark price for an instrument.
- `public/get_historical_volatility` — realized/historical volatility series for a currency.
- `public/get_volatility_index_data` — DVOL volatility-index candles.
- `public/get_delivery_prices`, `public/get_last_settlements_by_currency`/`..._by_instrument` —
  historical expiry settlement / delivery prices.
- Article "Accessing Historical Trades and Orders Using API" — `historical` parameter for older
  trade/order records.

### History lookback (start date)

- Deribit launched BTC options in 2016 and ETH options in 2019; trade-history endpoints can reach
  back toward instrument inception via `..._and_time` queries. However, the API does NOT expose a
  clean full-chain snapshot for an arbitrary PAST date: `get_instruments?expired=true` only returns
  *recently* expired contracts, and ticker/order-book/greeks are CURRENT-state only (no historical
  snapshot of IV/greeks/mark for a past timestamp except the 5-min mark-price history).
- Practical consequence: to build a historical option CHAIN with the free API you must POLL on a
  schedule (e.g., daily) and persist instruments + ticker/quotes yourself going forward; you cannot
  retroactively pull a full historical chain with greeks for dates before you started collecting.
- EXACT earliest retrievable trade timestamps per instrument: UNVERIFIED from docs (would need a
  live API probe). Third-party vendors that recorded Deribit from 2019-03-30 (see Tardis) fill this
  gap for past chains.

### Granularity

- Trades: tick-level. Mark price history: 5-minute. Ticker/order book: on-demand snapshots
  (or real-time via WS subscriptions `ticker.*`, `book.*`, `markprice.options.*`).

### Format

- JSON (JSON-RPC 2.0). No bulk CSV download — you fetch and persist yourself.

### Access method

- REST (HTTP GET/POST) or WebSocket. Many community Python wrappers exist; also raw `requests`/
  `websockets`. No paid key needed for public data.

### Cost

- FREE. Public data requires no payment and no mandatory API key. Optional free API key raises limits.

### Rate limits (verified, articles/rate-limits)

- Credit-based "leaky bucket" per sub-account. Non-matching (market-data) default: 500 credits/req,
  50,000 max pool, refill ~10,000 credits/s → ~20 req/s sustained, ~100 burst (illustrative defaults).
- `public/get_instruments` is specially limited: 1 request/second sustained (cost 10,000, pool
  500,000, burst ~50). Use WS `instrument_state.{kind}.{currency}` to avoid hammering it.
- Unauthenticated PUBLIC calls are limited PER-IP and do not draw from the credit pool; Deribit
  recommends authenticating for higher/clearer limits. Error on exhaustion: `too_many_requests`
  (code 10028).

### Suitability for a multi-week diagonal with a daily short leg

- BEST FREE source IF you collect forward. Going forward you can snapshot the full option chain daily
  (mark price, IV, greeks all included) to evaluate the long-dated long leg and roll a daily/weekly
  short leg. For PAST periods you can reconstruct executable prices from `get_last_trades_*_and_time`
  and 5-min `get_mark_price_history`, but rebuilding a complete historical chain with greeks for old
  dates is laborious — a recorded dataset (Tardis) is far more convenient for historical backtests.

## Source 2: Tardis.dev

Tardis.dev is a specialist tick-level historical crypto market-data vendor (50+ exchanges). It is the
strongest PAID/highest-quality option for ready-to-use historical Deribit options data.

**Verified from https://docs.tardis.dev/ :**

### Data available

- Deribit "Options" data plan covers ALL Deribit options instruments. Data types (normalized CSV):
  `trades`, `incremental_book_L2`, `book_snapshot_25`, `book_snapshot_5`, `quotes`,
  `book_ticker`, `derivative_ticker` (open interest, funding, mark price, index price),
  `liquidations`, and **`options_chain`**.
- `options_chain` includes strikes, expirations, open interest, and **IV (`bid_iv`, `ask_iv`,
  `mark_iv`) and greeks (`delta`, `gamma`, `vega`, `theta`, `rho`)** — i.e., a ready per-snapshot
  options chain with greeks already populated (sourced from Deribit's option ticker stream).
- Underlying option implied-vol / greeks streams (`markprice.options`, options `ticker`) recorded
  since 2019-10-01; full instrument coverage (incl. options) since 2019-03-30.

### History lookback (start date)

- Deribit data available since **2019-03-30** (verified coverage table). Options IV/greeks streams
  since **2019-10-01**.
- IMPORTANT — access window depends on subscription billing interval, NOT just the dataset:
  - Yearly billing: Business = ALL history since 2019-03-30; Academic/Solo/Pro = last 4 years.
  - Quarterly billing: last 12 months. Monthly billing: last 4 months.
  - Access is a fixed start date from purchase, not a rolling window.

### Granularity

- Tick-level (most granular order-book updates and trades). `options_chain` and snapshots are
  produced from the recorded real-time feed. CSV datasets are daily files; Replay API supports
  custom minute-precision windows.

### Format

- Normalized CSV (daily flat files), gzip; also raw exchange-native via HTTP Replay API and
  normalized via client libs / tardis-machine.

### Access method

- Downloadable CSV files (all subscription types) + HTTP Replay API + official **Python** and
  **Node.js** clients + locally runnable **tardis-machine** (npm / Docker) for normalization and
  custom snapshots. Raw replay API + tardis-machine + instruments-metadata API are Pro/Business only.
- A paid API key (from the order form) is required for historical data; the open-source real-time
  streaming libs need no key.

### Cost

- Paid subscription. Dimensions: subscription type (Academic [disabled for new], Solo, Pro,
  Business) x data plan (Perpetuals, Options, Spot, Derivatives, All Exchanges) x billing interval
  (monthly/quarterly/yearly). EXACT prices are NOT published in the docs — shown on the order form
  (https://tardis.dev/#order) / via quotation. Invoicing offered for orders over $6000. Discounts
  via subscription type (solo/academic cheaper). Specific $ figures: UNVERIFIED (not in docs).
- Free samples (VERIFIED): "Historical datasets for the FIRST DAY OF EACH MONTH are available to
  download WITHOUT API key." This includes Deribit options — e.g.
  `https://datasets.tardis.dev/v1/deribit/options_chain/2020/09/01/OPTIONS.csv.gz` and the same for
  `quotes`, `book_snapshot_25`, `trades`. So you can evaluate the exact `options_chain` format for
  free before buying. Additional "generous free trials" available on request (contact them).
- Python client (VERIFIED): `pip install tardis-dev` (Python >=3.9), `download_datasets(...)`; CSV
  URL pattern `https://datasets.tardis.dev/v1/{exchange}/{dataType}/{YYYY}/{MM}/{DD}/{SYMBOL}.csv.gz`.
  Grouped symbol `OPTIONS` downloads ALL option instruments for that day in one file. New daily data
  lands ~06:00 UTC next day.
  NOTE: `options_chain` likely starts ~2019-10-01 (when Deribit option ticker/IV streams began),
  slightly later than the 2019-03-30 overall Deribit start — trades/order book go back to 2019-03-30.

### Suitability for a multi-week diagonal with a daily short leg

- EXCELLENT. `options_chain` with mark price + IV + greeks per snapshot is exactly what a diagonal
  backtest needs: pick the long-dated long leg, roll a daily/weekly short leg, all legs priced from
  the same recorded chain. No need to collect-forward or recompute greeks. The 'Options' data plan
  on a yearly Business (or 4-year Solo/Pro) subscription cleanly covers multi-year backtests.

## Source 3: Amberdata

**Verified from https://www.amberdata.io/ :**

- MAJOR UPDATE: "Kaiko Acquires Amberdata" (2026) — Amberdata is now part of Kaiko (see Source 7).
- Amberdata's options/derivatives offering is "Amberdata Derivatives" (the former **Genesis
  Volatility / GVol** team — the Amberdata footer links the GenesisVol handle and an "Amberdata
  Derivatives" channel; options analytics live at pro.amberdata.io / intelligence.amberdata.com).
- Data available: institutional crypto derivatives data including options with **greeks and IV**,
  volatility surfaces, skew, term structure, options analytics (their research routinely covers
  Deribit BTC/ETH options skew/smile). Real-time and historical, normalized.
- History lookback: marketing claims "13+ years of historical data" for the overall platform; this
  is NOT specifically the options history. Exact options-history start date: UNVERIFIED (not stated
  on the pages reviewed). Crypto options realistically begin ~2019 (Deribit) regardless of vendor.
- Granularity: tick / snapshot / analytics depending on product. Format: REST API + WebSocket + JSON;
  bulk delivery for enterprise. Access method: REST/WebSocket API (key required) + analytics UI.
- Cost: PAID / enterprise. No public pricing; "Request a Demo." Greeks/IV come INCLUDED (computed).
- Suitability: high-quality and greeks/IV are ready-made, but enterprise pricing and demo-gated
  access make it heavier than needed for a solo diagonal backtest vs. Deribit/Tardis.

## Source 4: CoinAPI

**Verified from https://www.coinapi.io/ and /market-data-api/pricing :**

- Positioning: unified market data across "400+ exchanges (spot, derivatives, options)". Core
  DOCUMENTED data types are **trades, quotes, OHLCV, and order books** ("Raw, real-time trading
  data like Trades, Order Books, Quotes and OHLCV"). Products: Market Data API, **Flat Files**
  (bulk historical CSV via S3), Indexes, EMS.
- Options support CAVEAT: the homepage lists "options" among coverage, but NOWHERE in the pricing /
  product copy reviewed are option **chains, implied volatility, or greeks** documented as a data
  type. CoinAPI does NOT appear to compute/serve option greeks or IV. Treat CoinAPI options as, at
  best, raw option-instrument market data (trades/quotes/OHLCV) — chain/greeks/IV depth UNVERIFIED
  and most likely NOT provided. (The docs index redirected/404'd during research.)
- History lookback: marketing claims "a decade of historical data" (spot/derivatives); options
  history specifics UNVERIFIED.
- Granularity: tick-by-tick + OHLCV. Format: REST/JSON, WebSocket, FIX, **Flat Files (CSV/S3)**.
- Cost (VERIFIED): Pay-As-You-Go metered with **$25 free credits** to start; Startup $79/mo
  ($69/mo annual) = 1,000 REST credits/day; Streamer $249/mo = 10k/day; Pro $599/mo = 100k/day;
  Enterprise custom. PAYG REST credits from $5.26/1k (first 1k/day) down to $0.03/1k at huge volume.
  Free tier = $25 credits / no WebSocket on the free plan.
- Suitability: NOT recommended as a primary BTC/ETH options source for a diagonal backtest — no
  documented greeks/IV/option-chain product. Fine for underlying spot/perp prices if needed.

## Source 5: Laevitas / Genesis Volatility (GVol)

**Laevitas — verified from https://www.laevitas.ch/ :**

- Data available: full option chains, trade flows (blocks/strategies), IV-to-**greeks**, options
  strategy builder, **options backtesting** (predefined strangles/straddles/risk reversals vs.
  history), historical order-book snapshots. Exchanges: Deribit, Binance, OKX, Bybit, Hyperliquid.
- REST API v2: historical & real-time OHLCVT candles, funding, open interest, liquidations, and
  **options greeks**; also WebSocket, an MCP server (20+ tools), and x402 pay-per-request (USDC,
  no API key).
- History lookback: site states "5+ Years Historical Data" (platform-wide). Plan-gated (below).
- Granularity: candles/snapshots/analytics (not marketed as full tick options chains like Tardis).
- Format: web app + CSV exports (Premium) + REST/JSON API (Enterprise). Access: dashboards + API.
- Cost (VERIFIED pricing):
  - Free: $0/mo — only **1 week** of historical data, basic charting (app only, no API history).
  - Premium: $50/mo per seat — **1 year** historical data, unlimited charting, **CSV exports**.
  - Enterprise: $500/mo per seat — **API historical data**, all premium features, priority support.
  - Custom Enterprise: custom — high-throughput API.
- Suitability: good for analytics, IV surfaces, and quick strategy backtests via the UI; greeks/IV
  included. For a programmatic multi-year diagonal backtest you'd need the $500/mo Enterprise (API
  history) or export CSVs at $50/mo (1yr). Less granular and less backtest-friendly than Tardis
  `options_chain`, but cheaper than enterprise vendors and partnered with Deribit.

**Genesis Volatility / GVol — https://gvol.io/ (page would not render during research):**

- GVol (Genesis Volatility) is a crypto-options analytics platform with a (paid) **GraphQL API**
  for options data, vol surfaces, and greeks. It has effectively merged into **Amberdata
  Derivatives** (now Kaiko) — see Sources 3 and 7. Some free public charts/social analytics exist;
  the historical API is PAID. Exact current pricing/lookback: UNVERIFIED (site did not render; treat
  GVol as the Amberdata/Kaiko derivatives stack going forward).

## Source 6: Kaggle / Public Datasets

**Verified from https://www.kaggle.com/ (search "deribit options"):**

- Crypto BTC/ETH options datasets on Kaggle are SPARSE and generally NOT suitable for multi-week
  backtests. The most relevant hit, "Deribit BTC options information"
  (kaggle.com/datasets/hsergeyfrolov/deribit-btc-options-information), is a **single point-in-time
  SNAPSHOT** of all BTC option series — 1 file `data.csv` (~446 kB, 27 columns), "Expected update
  frequency: Never," updated ~2 years ago. Columns include `bid_iv`, `ask_iv`, `mark_iv`,
  `underlying_price`, `open_interest`, best bid/ask price+amount, `estimated_delivery_price`.
  Good for learning / building a one-moment IV surface; NO time series, so unusable for a diagonal
  backtest that needs daily rolls over weeks.
- Other hits are equity options (SPY) or generic crypto OHLC, not BTC/ETH options time series.
- History lookback: effectively a single date (UNVERIFIED which exact date); MIT license, free.
- Verdict: free but NOT a viable backtest source for this strategy. Use Deribit API or Tardis.

## Source 7: Kaiko

**Verified from https://www.kaiko.com/ :**

- Institutional digital-asset market-data leader (10+ years, SOC-2 Type II, EU BMR-compliant,
  200+ enterprise clients). **Acquired Amberdata (2026)** — consolidating Amberdata's derivatives /
  options analytics (GVol lineage) under Kaiko.
- Data available: derivatives incl. options; their research explicitly analyzes Deribit BTC options
  volatility surfaces ("Measuring Risk in Crypto Options", "Exploring Options Market Dynamics").
  Products: Data Feeds, Analytics Solutions (fair-value/derivatives), Indices; Developer Hub at
  docs.kaiko.com, Instrument Explorer at instruments.kaiko.com.
- History lookback / options granularity: not published publicly; UNVERIFIED specific options start
  date. Format: REST/streaming feeds + flat files (enterprise delivery).
- Cost: PAID / ENTERPRISE only. No public pricing — "Request a Trial." Greeks/IV available via the
  Amberdata-derived analytics (computed/included).
- Suitability: overkill for a solo diagonal backtest (enterprise sales, compliance-grade). Best for
  regulated institutions needing auditable data + indices. Deribit/Tardis are far more practical.

---

## Best Free vs Best Paid Recommendation

### BEST FREE: Deribit public API (collect-forward) + first-of-month Tardis samples

- **Why:** Deribit is the dominant BTC/ETH options venue and its PUBLIC market-data endpoints are
  free, need no mandatory API key, and already return **mark price, IV (bid/ask/mark), and full
  greeks (delta/gamma/vega/theta/rho)** per option via `public/ticker` / `public/get_order_book`.
- **Lookback:** Trades reach back toward instrument inception via `get_last_trades_by_instrument_
  and_time`; 5-min mark-price history via `get_mark_price_history`. BUT there is NO clean historical
  full-chain snapshot for arbitrary past dates (`get_instruments?expired=true` returns only RECENTLY
  expired contracts; ticker/greeks are current-state). Practical free approach = snapshot the chain
  yourself daily going forward.
- **Format / access:** JSON via REST or WebSocket; free. Rate limits credit-based (~20 req/s
  non-matching default; `get_instruments` capped at 1 req/s). Authenticated free key = higher limits.
- **Free shortcut for PAST data:** Tardis publishes the **first day of each month FREE** (no key),
  including `deribit/options_chain/.../OPTIONS.csv.gz` — enough to prototype a backtest on monthly
  snapshots at zero cost.

### BEST PAID / HIGHEST QUALITY: Tardis.dev — Deribit "Options" data plan

- **Why:** Ready-made historical `options_chain` CSV with strikes, expiries, open interest, and
  **mark/bid/ask IV + full greeks already populated** — exactly what a diagonal backtest needs; no
  collect-forward, no recomputation. Plus tick trades, quotes, and L2/snapshots for fills.
- **Coverage start:** Deribit data since **2019-03-30** (options_chain ~2019-10-01). Access window
  depends on billing: yearly Business = ALL history since 2019-03-30; Academic/Solo/Pro yearly =
  last 4 years; quarterly = 12 months; monthly = 4 months.
- **Format / access:** normalized daily **CSV** (gzip) via datasets API + official **Python**
  (`tardis-dev`) / Node clients; Replay API + tardis-machine for Pro/Business.
- **Cost:** paid subscription; EXACT prices not published (order form / quotation; invoicing >$6000).
  Free first-of-month samples + free trials on request let you validate before buying.
- **Runner-up paid (analytics/cheaper):** Laevitas — greeks/IV + options backtester; CSV export at
  $50/mo (1yr history), programmatic API history at $500/mo. Institutional alternatives (heavier,
  enterprise-priced, demo-gated): Amberdata Derivatives / GVol and Kaiko.

### Do greeks/IV come included or must they be computed?

- **INCLUDED (no Black-Scholes/Black-76 needed):** Deribit (native, Black-Scholes), Tardis
  `options_chain` (from Deribit's streams), Laevitas, Amberdata/GVol, Kaiko. For these you get
  `delta/gamma/vega/theta/rho` and `mark_iv`/`bid_iv`/`ask_iv` directly.
- **MUST COMPUTE yourself:** only if you rely on a source that ships just option price + underlying
  (e.g., CoinAPI raw option trades/OHLCV, or a bare trades-only pull) — then compute IV/greeks with
  Black-76 (futures-settled) or Black-Scholes from option mark + underlying + time-to-expiry + rate.
- Caveat on Deribit's greeks: theta = min(1-day theta, lifetime theta); delta in `ticker.greeks` is
  Black-Scholes delta (account-summary DeltaTotal uses Net Transaction Delta) — fine for backtests.

## Fields Available Summary (IV / Greeks / Mark)

| Source | Option chain (strikes/expiries) | Mark price | IV (bid/ask/mark) | Greeks | Lookback start | Granularity | Format | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Deribit API** | Yes (active; expired = recent only) | Yes | Yes (native) | Yes (BS) | ~2016 BTC / 2019 ETH via trades; chain = collect-forward | tick trades; 5-min mark; snapshots | JSON (REST/WS) | FREE |
| **Tardis.dev** | Yes (`options_chain`, OPTIONS group) | Yes (in chain/derivative_ticker) | Yes (`bid_iv`/`ask_iv`/`mark_iv`) | Yes (delta/gamma/vega/theta/rho) | Deribit 2019-03-30; chain ~2019-10-01 | tick / snapshot (daily files) | normalized CSV + API | PAID (free 1st-of-month + trials) |
| **Amberdata / GVol** | Yes | Yes | Yes | Yes | UNVERIFIED (platform "13+ yrs") | tick/snapshot/analytics | REST/WS/JSON | PAID/enterprise |
| **CoinAPI** | Not documented (likely no) | Underlying/instrument only | No (not documented) | No (not documented) | ~10 yrs spot/deriv; options UNVERIFIED | tick + OHLCV | REST/JSON, WS, FIX, flat files | $25 free credits; $79+/mo |
| **Laevitas** | Yes | Yes | Yes | Yes (options greeks) | "5+ years" (plan-gated) | candles/snapshots/analytics | App + CSV (Premium) + API (Ent.) | Free(1wk)/$50/$500 mo |
| **Kaggle (Deribit BTC opts)** | Yes (one snapshot) | via bid/ask | Yes (`bid_iv`/`ask_iv`/`mark_iv`) | No (compute from IV) | single date (~2yrs ago) | single snapshot | CSV | FREE |
| **Kaiko** | Yes (institutional) | Yes | Yes | Yes (Amberdata-derived) | UNVERIFIED | feeds/flat files | REST/streaming + flat files | PAID/enterprise |

UNVERIFIED items above could not be confirmed from the public pages reviewed and should be checked
with the vendor or via a live API probe before relying on them.

## Sources List

- Deribit API docs: https://docs.deribit.com/ (llms.txt index; market-data methods
  `public/ticker`, `public/get_instruments`, `public/get_last_trades_by_instrument_and_time`,
  `public/get_tradingview_chart_data`, `public/get_mark_price_history`,
  `public/get_book_summary_by_currency`), rate limits: https://docs.deribit.com/articles/rate-limits.md
- Deribit platform: https://www.deribit.com/
- Tardis.dev docs: https://docs.tardis.dev/ ; coverage/data FAQ https://docs.tardis.dev/faq/general.md ;
  billing https://docs.tardis.dev/faq/billing-and-subscriptions.md ; CSV overview + free first-of-month
  https://docs.tardis.dev/downloadable-csv-files/overview.md ; Deribit details
  https://docs.tardis.dev/historical-data-details/deribit.md ; datasets URL pattern
  https://datasets.tardis.dev/v1/deribit/options_chain/2020/09/01/OPTIONS.csv.gz
- Amberdata: https://www.amberdata.io/ (options analytics https://pro.amberdata.io/ ; Kaiko acquisition)
- CoinAPI: https://www.coinapi.io/ ; pricing https://www.coinapi.io/market-data-api/pricing
- Laevitas: https://www.laevitas.ch/ ; API docs https://apiv2.laevitas.ch/redoc ; app https://app.laevitas.ch/
- Genesis Volatility / GVol: https://gvol.io/ (did not render; now Amberdata Derivatives / Kaiko)
- Kaggle: https://www.kaggle.com/datasets?search=deribit%20options ;
  https://www.kaggle.com/datasets/hsergeyfrolov/deribit-btc-options-information
- Kaiko: https://www.kaiko.com/ ; developer hub https://docs.kaiko.com/
