<!-- markdownlint-disable-file -->
# Research: US / Global Historical Data Sources for Backtesting Options Strategies (PMCC / PMCP)

> Educational research only — NOT financial advice. Pricing and terms change frequently. Every dollar figure below is marked **VERIFIED (date)** with the source page, or **verify current pricing/terms** when it could not be confirmed at research time. Do not treat any number as a quote.

## Research Scope and Questions

**Strategy context:** PMCC (Poor Man's Covered Call = long call diagonal) and PMCP (Poor Man's Covered Put = long put diagonal). Mechanics: buy a ~monthly (longer-dated) option as the "stock substitute," sell a daily/weekly (short-dated) option against it, plus a futures trend-direction signal (ES/NQ). US underlyings of interest: SPY, QQQ, SPX, and ES/NQ futures.

**Data implication of the strategy (drives the requirements):**
- Needs **per-strike, per-expiry** historical option prices (bid/ask/close) for BOTH the long monthly and the short daily/weekly legs.
- Needs reliable **short-dated / weekly / 0DTE** expirations (daily short leg) — many cheap datasets only have monthly expiries.
- Wants **IV / Greeks** (delta for strike selection of the long leg; theta for the short leg) — ideally provided, otherwise computed.
- Wants **intraday granularity** if entries/exits are intraday; EOD is enough for a first daily-close backtest.
- Separately needs **ES/NQ futures OHLC** (cheap/free) for the trend signal.

**Questions to answer per source:**
1. Coverage — options and/or futures; which underlyings (SPY/QQQ/SPX/ES/NQ).
2. History depth (years).
3. Granularity — EOD vs 1-min vs tick.
4. Fields — strike, expiry, call/put, bid/ask/close, volume, OI, IV/Greeks?
5. Format — download (CSV/flat file) vs API.
6. Cost — free tier vs paid tiers.
7. Exact access method — API endpoint / client library / download portal.

**Providers to cover:**
- Options: ThetaData, Polygon.io, CBOE DataShop, ORATS, OptionMetrics IvyDB, Databento, Nasdaq Data Link (Quandl), dxFeed, IQFeed, FirstRate Data, Dolthub options dataset, Alpha Vantage, yfinance/Yahoo.
- Futures (ES/NQ): FirstRate Data, Databento, CME DataMine, Yahoo continuous front-month.
- All-in-one (data + backtest engine): QuantConnect (LEAN), optopsy, Option Alpha, OptionStrat, tastytrade/thinkBack.

---

## 1. Options-Data Providers (Free-Tier vs Paid)

_(in progress)_

## 2. Futures Data (ES / NQ)

_(in progress)_

## 3. All-in-One Platforms (Data + Backtest Engine)

_(in progress)_

## 4. Recommended Top Pick for a First US Backtest + Access Method

_(in progress)_

## 5. Caveats and Reality Check

_(in progress)_

## Comparison Table

_(in progress)_

## Clarifying Questions / Unverifiable Items

_(in progress)_
