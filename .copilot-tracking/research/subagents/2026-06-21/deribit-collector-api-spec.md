<!-- markdownlint-disable-file -->
# Deribit v2 Public API — Daily Options-Chain Snapshot Collector Spec

**Status:** Complete
**Date:** 2026-06-21
**Scope:** Verify Deribit v2 public REST endpoints (no API key) needed to build a DAILY options-chain snapshot collector for BTC and ETH. All fields verified against https://docs.deribit.com/ (OpenAPI spec embedded in the docs) AND cross-checked with LIVE public production calls on 2026-06-21.

**Verification method:** Each endpoint was confirmed two ways — (1) the official OpenAPI schema published at https://docs.deribit.com/api-reference/market-data/* and (2) live `Invoke-RestMethod` GET calls against `https://www.deribit.com/api/v2/...` (public, unauthenticated). Where the published OpenAPI schema disagreed with live responses, the LIVE response is treated as authoritative and the discrepancy is flagged.

## Research Questions

1. Base URL + request format (REST GET, JSON-RPC envelope).
2. `public/get_instruments` — params + exact response fields.
3. `public/ticker` — exact response fields for an OPTION incl. nested `greeks`.
4. `public/get_book_summary_by_currency` — fields; does it include greeks/IV/underlying/OI?
5. `public/get_index_price` / `public/get_index_chart_data` — fetch BTC/ETH index price.
6. Rate limits — public limits, get_instruments cap, safe req/s.

## TL;DR (Answers)

- **Base REST:** `https://www.deribit.com/api/v2/` + `{scope}/{method}`. Public methods work as plain GET with URL query params, e.g. `https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-26JUN26-100000-C`. Envelope: `jsonrpc`, `result`, `usIn`, `usOut`, `usDiff`, `testnet` (+ `id` if you send one; `error` instead of `result` on failure).
- **`get_book_summary_by_currency` does NOT include greeks** (verified live: `has greeks? False`). It DOES include `mark_iv`, `underlying_price`, `open_interest`, `mark_price`, `bid_price`, `ask_price`. It LACKS `delta/gamma/vega/theta/rho`, `bid_iv`, `ask_iv`, and bid/ask sizes.
- **Greeks require `public/ticker` per instrument.** The `ticker` `greeks` object = `delta, gamma, vega, theta, rho`.
- **Option premiums are quoted in the BASE CURRENCY (BTC/ETH).** Verified live: a BTC option returns `quote_currency: "BTC"`, `settlement_currency: "BTC"`, `counter_currency: "USD"`, `contract_size: 1`, and `mark_price`/`last_price` are small BTC fractions (e.g. `0.01989768` BTC). Strike and `underlying_price` are in USD.
- **Live instrument counts (2026-06-21):** BTC = **938** active options, ETH = **748** → ~**1,686** total (order of magnitude ~1k–2k).
- **Recommended algorithm (user wants IV + full greeks):** Hybrid = `get_book_summary_by_currency` (1 call/currency) to get the full chain + prices + IV + OI cheaply, then `public/ticker` per instrument for greeks. Safe polite rate ≈ **5 req/s** (unauthenticated, per-IP). Full both-currency snapshot ≈ **5–6 min** at 5 req/s.

## Q1 — Base URL & Request Format (CONFIRMED)

**Production REST base:** `https://www.deribit.com/api/v2/{method}` (test: `https://test.deribit.com/api/v2/{method}`).

- Both **GET and POST** are supported. For GET, params may be passed as a **URL query string (URL-encoded)** OR as a JSON-RPC body. Named parameters only (case-sensitive); **batch requests are NOT supported**; positional params are NOT supported.
- Confirmed working GET examples (live, 2026-06-21):
  - `https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=option&expired=false`
  - `https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-26JUN26-100000-C`
  - `https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option`
  - `https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd`
- **HTTP connection lifetime:** expires after 15 minutes of inactivity. Max 32 connections per IP. (HTTP cannot do subscriptions / cancel-on-disconnect — those need WebSocket. Not relevant for a daily snapshot collector.)

**JSON-RPC response envelope** (top-level fields, live-verified keys: `jsonrpc, result, usIn, usOut, usDiff, testnet`):

| Field | Type | Notes |
| --- | --- | --- |
| `jsonrpc` | string | Always `"2.0"`. |
| `id` | integer\|string | Echoed back only if you sent one. (Absent in the bare query-string GET test above.) |
| `result` | any | Present on success. Structure depends on method (object or array). |
| `error` | object | Present on failure instead of `result`: `{ code, message, data? }`. Mutually exclusive with `result`. |
| `testnet` | boolean | `false` for production, `true` for test. |
| `usIn` | integer | Request-received timestamp (microseconds since Unix epoch, UTC). |
| `usOut` | integer | Response-sent timestamp (microseconds). |
| `usDiff` | integer | Server processing time (`usOut - usIn`). |

> Note: `usIn`/`usOut`/`usDiff`/`testnet` are Deribit-specific extensions to JSON-RPC 2.0.

## Q2 — public/get_instruments (CONFIRMED + corrections)

**Method:** `GET https://www.deribit.com/api/v2/public/get_instruments`

**Params:**

| Param | Required | Values | Notes |
| --- | --- | --- | --- |
| `currency` | yes | `BTC`, `ETH`, `USDC`, `USDT`, `EURR`, `any` | Use `BTC` / `ETH`. |
| `kind` | no | `future`, `option`, `spot`, `future_combo`, `option_combo` | Use `option`. |
| `expired` | no | `true` / `false` (default `false`) | `false` = active instruments. |

**Result:** array of instrument objects.

**EXACT field set returned for an OPTION** (live-verified, BTC option `BTC-22JUN26-56000-C`, 25 keys — this is the real per-option key set, which is a subset of the union schema):

`state, price_index, kind, instrument_name, maker_commission, taker_commission, instrument_type, expiration_timestamp, is_active, creation_timestamp, instrument_id, tick_size, contract_size, strike, base_currency, quote_currency, settlement_currency, option_type, min_trade_amount, block_trade_commission, block_trade_min_trade_amount, block_trade_tick_size, settlement_period, counter_currency, tick_size_steps`

Field meanings (the fields the collector needs are marked ★):

| Field | Type | Meaning |
| --- | --- | --- |
| ★ `instrument_name` | string | Unique id, e.g. `BTC-22JUN26-56000-C` (`CCY-DMMMYY-STRIKE-K`, K = `C`/`P`). |
| ★ `strike` | number | Strike price **in USD** (options only). |
| ★ `expiration_timestamp` | integer | Expiry, **milliseconds** since Unix epoch. |
| ★ `option_type` | string | `call` or `put` (options only). |
| ★ `contract_size` | number | Contract multiplier. Live = `1.0` for BTC/ETH options (1 contract = 1 underlying coin). |
| ★ `tick_size` | number | Minimal price change (in premium/base-currency units). |
| `tick_size_steps` | array | `[{ above_price, tick_size }]` — larger tick above a price threshold. |
| ★ `settlement_period` | string | **Live values include `day`, `week`, `month`** (see discrepancy note). |
| ★ `quote_currency` | string | **Live = `BTC` for BTC options** (currency the premium is quoted in). See discrepancy. |
| ★ `base_currency` | string | Underlying coin, `BTC` / `ETH`. |
| `settlement_currency` | string | `BTC` / `ETH` (coin-settled / inverse). |
| `counter_currency` | string | `USD` (the strike/quote-of-underlying currency). |
| ★ `is_active` | boolean | Whether the instrument can currently be traded. |
| `state` | string | Book state: `open`, `settlement`, `delivered`, `inactive`, `locked`, `halted`, `archivized`. |
| `kind` | string | `option`. |
| `instrument_id` | integer | Internal numeric id. |
| `instrument_type` | string | `reversed` (inverse) for BTC/ETH options. |
| `price_index` | string | e.g. `btc_usd`. |
| `min_trade_amount` | number | Min order size (in underlying base coin for options). |
| `maker_commission` / `taker_commission` | number | Fees. |
| `block_trade_commission` / `block_trade_min_trade_amount` / `block_trade_tick_size` | number | Block-trade params. |
| `creation_timestamp` | integer | Creation time (ms). |

**Discrepancies between published OpenAPI and LIVE data (IMPORTANT):**

1. **`quote_currency`** — The OpenAPI schema enumerates `quote_currency` as `USD` only, described as "The currency in which the instrument prices are quoted." **Live, a BTC option returns `quote_currency: "BTC"`** (and ETH options return `ETH`). This CONFIRMS option premiums are denominated in the base coin, not USD. Trust the live value.
2. **`settlement_period`** — OpenAPI enum lists only `month`, `week`, `perpetual`. **Live returns `day`** for short-dated daily options. So daily options exist and `settlement_period` can be `day`. Treat the enum as non-exhaustive.
3. Union-schema fields such as `underlying_type`, `base_currency_uuid`, `quote_currency_uuid`, `qty_tick_size`, `index_id`, `product_group`, `future_type`, `max_leverage`, `max_liquidation_commission` were **absent** for the sampled option (they apply to futures or other kinds). Do not assume they exist on option objects.

## Q3 — public/ticker (CONFIRMED — has full greeks)

**Method:** `GET https://www.deribit.com/api/v2/public/ticker?instrument_name=<name>`
**Params:** `instrument_name` (required).
**Result:** single object.

**EXACT result fields for an OPTION** (live-verified, `BTC-26JUN26-100000-C`, 23 keys):

`timestamp, state, stats, greeks, interest_rate, index_price, instrument_name, last_price, settlement_price, min_price, max_price, open_interest, mark_price, best_ask_price, best_bid_price, mark_iv, bid_iv, ask_iv, underlying_price, underlying_index, estimated_delivery_price, best_ask_amount, best_bid_amount`

| Field | Type | Meaning (verified) |
| --- | --- | --- |
| ★ `mark_price` | number | Option mark price, **in base currency (BTC/ETH)**. |
| ★ `mark_iv` | number | Mark implied volatility, **in PERCENT** (live `80.44` = 80.44%). |
| ★ `bid_iv` | number | IV at best bid (percent). |
| ★ `ask_iv` | number | IV at best ask (percent). |
| ★ `underlying_price` | number | Forward/underlying price for IV calc, **in USD** (options only). |
| ★ `underlying_index` | string | Name of underlying future or `index_price` — **e.g. `"BTC-26JUN26"`** (see discrepancy: it is a STRING, not a number). |
| ★ `open_interest` | number | Outstanding contracts; for options, in underlying base coin units. |
| ★ `best_bid_price` | number | Best bid (base ccy); `0`/`null` if none. |
| ★ `best_ask_price` | number | Best ask (base ccy). |
| ★ `best_bid_amount` | number | Size at best bid. |
| ★ `best_ask_amount` | number | Size at best ask. |
| ★ `last_price` | number | Last trade premium (base ccy); `null` if no trades. |
| ★ `interest_rate` | number | Interest rate used in IV calc (options only). |
| ★ `settlement_price` | number | Settlement price; present when `state = open` (optional). |
| ★ `greeks` | object | See below — `delta, gamma, vega, theta, rho`. |
| `index_price` | number | Current index (USD). |
| `estimated_delivery_price` | number | Estimated delivery/expiration price (USD). |
| `min_price` / `max_price` | number | Order price clamps. |
| `state` | string | Book state (`open`, etc.). |
| `timestamp` | integer | ms since Unix epoch. |
| `stats` | object | `{ volume, low, high, price_change, volume_usd }` (`volume` in base ccy). |

**`greeks` object (CONFIRMED, all 5 present and required):**

| Field | Meaning |
| --- | --- |
| `delta` | Black–Scholes delta (per-expiry). |
| `gamma` | Standard Black–Scholes gamma. |
| `vega` | Standard Black–Scholes vega. |
| `theta` | Deribit theta = min(1-day theta, lifetime theta). |
| `rho` | Standard Black–Scholes rho. |

Live sample: `"greeks": { "delta": 0.0, "gamma": 0.0, "vega": 0.00031, "theta": -0.00096, "rho": 1E-05 }`.

**Futures/perpetual-only fields NOT present on options:** `funding_8h`, `current_funding`, `interest_value`, `delivery_price` (only when settled), `volume_usd` lives inside `stats`, and `is_anchor_breached`/`anchor_min_price`/`anchor_max_price` (RWA perpetuals only).

**Option premium currency — ANSWERED:** YES. Option prices (`mark_price`, `best_bid_price`, `best_ask_price`, `last_price`) are quoted in the **base currency (BTC or ETH)**. Evidence: `quote_currency=BTC`, `settlement_currency=BTC`, `contract_size=1`, and the small fractional magnitudes (e.g. `mark_price 0.01989768` BTC ≈ premium of ~0.02 BTC). `strike` and `underlying_price` are in USD. To get USD premium, multiply by `underlying_price` (or `index_price`).

**Discrepancy:** OpenAPI declares `underlying_index` as `type: number`, but live it is a **string** (`"BTC-26JUN26"`). Parse it as a string.

## Q4 — public/get_book_summary_by_currency (EFFICIENCY — lacks greeks)

**Method:** `GET https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option`
**Params:** `currency` (required: BTC/ETH/…), `kind` (optional: use `option`).
**Result:** array — **one element per instrument** (live: 938 BTC option elements in a single call).

**EXACT result fields for an OPTION element** (live-verified, 20 keys):

`high, low, last, interest_rate, instrument_name, bid_price, ask_price, open_interest, mark_price, creation_timestamp, price_change, volume, mark_iv, underlying_price, underlying_index, base_currency, quote_currency, estimated_delivery_price, volume_usd, mid_price`

| Field | Present? | Notes |
| --- | --- | --- |
| `instrument_name` | ✅ | id. |
| `mark_price` | ✅ | base-ccy premium (higher precision than ticker, e.g. `0.01989768`). |
| `bid_price` / `ask_price` / `mid_price` | ✅ | best bid/ask + midpoint (base ccy). |
| `last` | ✅ | last trade premium. |
| `mark_iv` | ✅ | **IV present** (percent). |
| `underlying_price` | ✅ | USD underlying for IV. |
| `underlying_index` | ✅ | string, e.g. `BTC-31JUL26`. |
| `open_interest` | ✅ | OI present. |
| `interest_rate` | ✅ | options IV rate. |
| `volume` / `volume_usd` | ✅ | 24h volume (base ccy / USD). |
| `price_change` | ✅ | 24h % change. |
| `high` / `low` | ✅ | 24h high/low. |
| `base_currency` / `quote_currency` | ✅ | `BTC` / `BTC` for BTC options. |
| `estimated_delivery_price` | ✅ | USD. |
| `creation_timestamp` | ✅ | ms. |
| **`greeks`** | ❌ | **ABSENT** — `has greeks? False` (live). No `delta/gamma/vega/theta/rho`. |
| `bid_iv` / `ask_iv` | ❌ | absent (only `mark_iv`). |
| `best_bid_amount` / `best_ask_amount` | ❌ | no sizes. |
| `timestamp` / `state` | ❌ | only `creation_timestamp`; no live `state`. |

**Answer to the key question:** ONE call to `get_book_summary_by_currency` CAN replace hundreds of per-instrument `ticker` calls **for prices, `mark_iv`, `underlying_price`, and `open_interest`** — but it **LACKS greeks** (and `bid_iv`/`ask_iv` and bid/ask sizes). Since the user wants **full greeks (delta/gamma/vega/theta/rho)**, `book_summary` ALONE is insufficient; greeks still require `ticker` per instrument.

| Need | `book_summary` (1 call) | `ticker` (N calls) |
| --- | --- | --- |
| prices (mark/bid/ask/last) | ✅ | ✅ |
| `mark_iv` | ✅ | ✅ |
| `bid_iv` / `ask_iv` | ❌ | ✅ |
| `underlying_price`, `open_interest` | ✅ | ✅ |
| bid/ask sizes | ❌ | ✅ (`best_bid_amount`/`best_ask_amount`) |
| **greeks (Δ Γ V Θ ρ)** | ❌ | ✅ |

## Q5 — Index price (CONFIRMED)

**Method:** `GET https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd` (or `eth_usd`).
**Params:** `index_name` (required). Enum includes `btc_usd`, `eth_usd` (also many `*_usdc`/`*_usdt` indices). For a USD-denominated BTC/ETH snapshot use `btc_usd` / `eth_usd`.
**Result (live-verified):**

```json
{ "index_price": 64089.74, "estimated_delivery_price": 64089.74 }
```

| Field | Type | Meaning |
| --- | --- | --- |
| `index_price` | number | Current value of the index (USD). |
| `estimated_delivery_price` | number | Estimated delivery/expiration price (USD). |

Notes:
- You can also read `index_price` (and per-expiry `underlying_price`) directly from each `ticker`/`book_summary` element, so a dedicated `get_index_price` call is optional but cleanest for storing one canonical spot value per currency per snapshot.
- `public/get_index_chart_data` (params `index_name`, `start_timestamp`, `end_timestamp`, `resolution`) returns historical index candles (`data`, `ticks`, etc.) — only needed for backfill/history, NOT for a current snapshot. Not required here.

## Q6 — Rate limits (CONFIRMED) & safe collector rate

From https://docs.deribit.com/articles/rate-limits.md (credit/leaky-bucket system):

- **`public/get_instruments` special cap (CONFIRMED):** Cost **10,000** credits, pool **500,000**, **Sustained Rate = 1 request/second**, **Burst = 50 requests**. So yes — get_instruments is throttled to ~1 req/s sustained. (It is server-cached; you only call it ~1×/currency/snapshot, so this is a non-issue.)
- **Non-matching-engine default budget (authenticated baseline):** Cost 500 credits/request, max pool 50,000, refill = **20 requests/second** (10,000 credits/s), burst ~100. `ticker` / `get_book_summary_by_currency` / `get_index_price` are non-matching-engine requests.
- **Public / unauthenticated requests are rate-limited PER IP** and **do NOT draw from the sub-account credit pool**. Deribit does **not publish an exact public per-IP number**; exceeding it leads to temporary rejection or disconnect. Docs explicitly recommend authenticating for "higher and more transparent limits."
- **Error on exhaustion:** `too_many_requests`, code **10028**.

**Recommended safe rate for a polite UNAUTHENTICATED collector:**
- **~5 requests/second (200 ms spacing)** for `ticker` calls — conservative, well under the 20 req/s authenticated default, and tolerant of the unpublished public per-IP cap.
- Keep `get_instruments` at **≤1 req/s** (only ~1 call/currency anyway).
- Implement exponential backoff on HTTP 429 / error code 10028; reuse a keep-alive HTTP connection (mind the 15-min idle expiry).
- Optional but recommended for sustained/daily use: create a **free read-only API key** and authenticate. The user asked for no key; per-IP public limits then apply, so stay conservative (≤5 req/s).

## Efficiency Recommendation

Given the requirement = **IV + full greeks** per option:

- **Option A — `get_book_summary_by_currency` only (1 call/currency):** minimal calls (2 total), gives prices + `mark_iv` + `underlying_price` + `open_interest`, but **NO greeks**. ❌ Insufficient on its own.
- **Option B — `get_instruments` + `ticker` per instrument (N calls):** guaranteed greeks + `bid_iv`/`ask_iv` + bid/ask sizes for every option. ✅ Complete, but ~1,686 calls.
- **Option C — HYBRID (RECOMMENDED):** Use `get_book_summary_by_currency` (1 call/currency) as the cheap base layer for the full chain (instrument list + prices + `mark_iv` + `underlying_price` + `open_interest` + 24h volume), then call `public/ticker` per instrument to enrich with **greeks** (+ `bid_iv`/`ask_iv` + bid/ask sizes). `get_instruments` is still useful once per currency for static contract metadata (`strike`, `option_type`, `expiration_timestamp`, `contract_size`, `tick_size`, `settlement_period`).

**Use the HYBRID.** If you need greeks for EVERY option, the `ticker` fan-out is unavoidable (book_summary has no greeks). The hybrid still pays off because: (1) one `book_summary` call validates the live tradable set and gives you OI/volume to **filter** which strikes are worth a `ticker` call (e.g., skip zero-OI, zero-volume deep wings if acceptable), and (2) it provides a price/IV fallback for any `ticker` call that fails. If you only needed IV (not greeks), Option A alone would suffice.

## Recommended Snapshot Algorithm (pseudocode)

```text
BASE = "https://www.deribit.com/api/v2"
TICKER_RATE = 5            # req/s, polite unauthenticated cap
SLEEP = 1 / TICKER_RATE    # 0.2 s between ticker calls

func get(method, params):           # GET with query string
    resp = HTTP_GET(BASE + "/" + method + "?" + urlencode(params))
    if resp.error or http_429:
        backoff_exponential(); retry()   # handle code 10028 / 429
    return resp.result

snapshot_ts = now_utc_millis()
for currency in ["BTC", "ETH"]:
    # 1) static contract metadata (cap 1 req/s; cheap, ~1 call)
    instruments = get("public/get_instruments",
                      {currency, kind:"option", expired:false})
    meta = { i.instrument_name: i for i in instruments }   # strike, option_type,
            # expiration_timestamp, contract_size, tick_size, settlement_period,
            # base_currency, quote_currency, is_active

    # 2) canonical index spot for the snapshot
    idx = get("public/get_index_price", {index_name: currency.lower()+"_usd"})
    index_price = idx.index_price

    # 3) cheap full-chain prices + IV + OI (1 call)
    summary = get("public/get_book_summary_by_currency",
                  {currency, kind:"option"})
    book = { s.instrument_name: s for s in summary }   # mark_price, bid_price,
            # ask_price, mid_price, last, mark_iv, underlying_price,
            # underlying_index, open_interest, volume, volume_usd

    # 4) (optional) filter which instruments need greeks
    names = [n for n in book.keys()
             if meta[n].is_active]            # optionally also OI/volume filter

    # 5) per-instrument greeks via ticker (rate-limited fan-out)
    rows = []
    for name in names:
        t = get("public/ticker", {instrument_name: name})   # greeks, bid_iv,
                # ask_iv, best_bid_amount, best_ask_amount, settlement_price
        rows.append(merge(snapshot_ts, currency, index_price,
                          meta[name], book[name], t))
        sleep(SLEEP)

    write_parquet_or_csv(currency, snapshot_ts, rows)
```

**Per-row stored fields (suggested):** `snapshot_ts`, `currency`, `index_price`, `instrument_name`, `strike`, `option_type`, `expiration_timestamp`, `contract_size`, `tick_size`, `settlement_period`, `is_active`, `mark_price`, `mark_iv`, `bid_iv`, `ask_iv`, `best_bid_price`, `best_ask_price`, `best_bid_amount`, `best_ask_amount`, `last_price`, `mid_price`, `open_interest`, `volume`, `volume_usd`, `underlying_price`, `underlying_index`, `interest_rate`, `settlement_price`, `greeks.delta`, `greeks.gamma`, `greeks.vega`, `greeks.theta`, `greeks.rho`. (Premiums in base ccy; multiply by `underlying_price` for USD.)

**Instrument-count & timing estimate (2026-06-21 live):**

| Currency | Active options |
| --- | --- |
| BTC | 938 |
| ETH | 748 |
| **Total** | **~1,686** |

- Order of magnitude: ~1,000–2,000 options total across BTC+ETH (varies with listed expiries/strikes).
- Calls per snapshot (Option C): 2× `get_instruments` + 2× `get_index_price` + 2× `book_summary` + ~1,686× `ticker` ≈ **~1,692 calls**, dominated by ticker.
- Wall-clock at **5 req/s**: 1,686 / 5 ≈ **337 s ≈ 5.6 minutes**.
- At **10 req/s** (more aggressive, monitor for 10028): ≈ **2.8 minutes**.
- With an OI/volume filter (e.g., only ~300–400 liquid strikes/currency): ~600–800 ticker calls → **~2–3 min** at 5 req/s.
- `book_summary`-only (Option A, no greeks): **2 calls, <2 s**.

## Unverified / Uncertain Items

- **Exact public per-IP rate limit:** NOT published by Deribit. The 5 req/s recommendation is a conservative heuristic, not a documented number. Authenticating with a free read-only key gives documented, higher limits.
- **`settlement_period` full enum:** Live shows `day` (plus `week`, `month`) for options; the published OpenAPI enum (`month`/`week`/`perpetual`) is non-exhaustive. Treat as an open string set.
- **`quote_currency` for options:** OpenAPI says `USD`; LIVE returns `BTC`/`ETH`. Live value is authoritative (premium currency = base coin). Flagged as a docs/live discrepancy.
- **`underlying_index` type:** OpenAPI says `number`; LIVE returns a string (`"BTC-26JUN26"`). Parse as string.
- **IV units:** Live `mark_iv`/`bid_iv`/`ask_iv` are in PERCENT (e.g. `80.44`), not decimal fractions — confirmed by magnitude; the OpenAPI text does not state units explicitly.
- **Counts are time-varying:** 938 BTC / 748 ETH are the 2026-06-21 live figures; they change as expiries/strikes are listed and expire.
- **`get_book_summary_by_instrument`** (per-instrument variant) was not separately inspected; the by_currency variant is the efficient choice for a full-chain snapshot and is confirmed.
