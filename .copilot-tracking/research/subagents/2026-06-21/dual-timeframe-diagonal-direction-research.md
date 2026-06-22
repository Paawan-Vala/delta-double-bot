<!-- markdownlint-disable-file -->
# Dual-Timeframe Diagonal Direction (Daily-Short / Monthly-Long PMCC vs PMCP) — Research

Status: Complete
Date: 2026-06-21
Purpose: Educational study note (NOT financial advice). For a call/put DIAGONAL whose LONG leg is ~monthly and whose SHORT leg is sold DAILY (rolled often), decide the single highest-reliability way to read MARKET DIRECTION (PMCC vs PMCP) from an index FUTURES chart, and give a DECISIVE recommendation.

> Disclaimer: All thresholds and default settings below are illustrative educational conventions attributed to their sources. No win-rate / accuracy statistic is fabricated; any percentage is labeled illustrative. Trend tools lag and fail in ranges. Not financial advice. Options involve risk of loss.

## Research Topics & Questions

1. [x] TIMEFRAME: which chart timeframe sets the OVERALL bias when the long leg is ~monthly but the short leg is daily? (two-timeframe operating model)
2. [x] MOST RELIABLE SINGLE METHOD: decisive default stack (regime + trigger + ADX strength) with settings; simplest fallback
3. [x] WHY high-accuracy direction is HARDER for a DAILY short leg (gamma / whipsaw / strike run-over); stand-aside rule
4. [x] CONFIRMATION & BACKTESTING: no method high-accuracy alone; multi-timeframe alignment as biggest reliability booster; backtest; sizing > signal
5. [x] SOURCES + reachability notes

## Sources (status)

- [x] Investopedia — **Multiple Time Frames** (`/articles/trading/07/timeframes.asp`): FETCHED OK (prior session). Longer TF = more reliable; weekly=trend / daily=signal; disagreement = pause.
- [x] Investopedia — **ADX** (`/terms/a/adx.asp`): FETCHED OK (prior). Strength vs direction; >25 strong / <20 trendless; +DI/−DI cross; ADX-as-filter.
- [x] Investopedia — **Golden/Death Cross** (`/terms/g/goldencross.asp`): FETCHED OK (prior). 50/200; lag; "reactive not proactive"; risk-management bottom line.
- [x] Investopedia — **Ichimoku Cloud** (`/terms/i/ichimoku-cloud.asp`): FETCHED OK (prior). Above/below/inside cloud; weak in consolidation.
- [x] Investopedia — **EMA** (`/terms/e/ema.asp`): FETCHED OK (prior, EMA note). EMA hugs price; length bands.
- [x] StockCharts ChartSchool — **ADX/DMI**, **Moving Averages**, **MACD**: FETCHED OK (prior). Wilder 14; 20/25 thresholds; whipsaw examples; scans gate on SMA(200)/SMA(50).
- [x] TradingView education — **Supertrend** (`/support/solutions/43000634738`): FETCHED OK (prior). ATR-based green/red flip; false signals in chop; combine with others.
- [x] tastylive — **Gamma** (`/concepts-strategies/gamma`): FETCHED OK (this session). Short options = negative gamma; short-call delta accelerates against you on an adverse move; ATM/ITM options have higher gamma → delta changes faster.
- [x] tastylive — **PMCC / Poor-Man-Covered-Put / Diagonal**: FETCHED OK (prior, PMCC note). Structure = long-dated ITM long + short-dated short = covered-call/put replica.
- [~] Investopedia — **Gamma** (`/terms/g/gamma.asp`) and **Greeks** (`/trading/getting-to-know-the-greeks/`): UNREACHABLE this session (extraction failed — same pattern as other Investopedia `/terms/` pages). Gamma sourced from tastylive instead.
- [ ] BabyPips — **Multiple Time Frame Analysis**: UNREACHABLE (ad-system redirect) this + prior session. Recommended further reading; points fully covered via Investopedia + StockCharts.
- [ ] tastylive — **0DTE Options** (`/concepts-strategies/zero-days-0dte-options-explained`): UNREACHABLE this session (ad/iframe redirect). Near-expiry gamma intensification labeled a standard convention below.

---

## Bottom Line Up Front (the decisive recommendation)

- **Which timeframe sets the bias:** the **DAILY chart sets the PMCC-vs-PMCP bias, with the WEEKLY chart as the regime/context check above it.** The ~monthly LONG leg is what carries the directional risk, so its bias is read on the timeframe that matches a multi-week swing (daily), confirmed by the weekly. The **daily short leg is a theta/income overlay, not the direction driver** — an intraday chart only refines *when* and at *what strike* to sell the short call, and you only sell shorts in the direction the daily/weekly bias already allows.
- **The one default stack (run on the DAILY index-futures chart):** **Regime** = price above the **200-period EMA** (bull-only) / below (bear-only) **and the weekly agrees**; **Trigger** = **20-EMA vs 50-EMA** cross (20>50 bull / 20<50 bear); **Strength** = **ADX(14) > 25** (≥20 minimum) with **+DI > −DI** (bull) / **−DI > +DI** (bear). All three bullish + weekly up → **PMCC**. All three bearish + weekly down → **PMCP**. Anything else → **STAND ASIDE**.
- **Why this engine:** moving-average / EMA confluence is the most robust *directional backbone* (it objectively defines the current trend direction and is what the reputable published scans are built on), and **ADX is the key "is this trend real?" filter** that screens out the chop where EMA crosses whipsaw — the single change that most raises reliability.
- **Simplest fallback (second-best):** a single **Supertrend (ATR 10 × 3)** on the daily — **green = PMCC bias, red = PMCP bias** — optionally gated by price vs the 200-EMA. One unambiguous line; but it whipsaws in chop, so still stand aside when it flips repeatedly in a tight range. Absolute-minimalist version: **price vs the 200-day MA on the daily + weekly agreeing** (regime-only).
- **Stand-aside rule (the safest "direction" is often "no direction"):** if **ADX < 20**, price is **chopping around the MAs**, price is **inside the Ichimoku cloud**, or the **weekly and daily disagree** → do **not** open a diagonal and do **not** sell daily shorts. A daily short leg is **short gamma**: in chop or a fast counter-move the short strike gets *run over* quickly, and the roll treadmill compounds the whipsaw.
- **Honest caveats:** no method is high-accuracy alone; the stack still **lags**; you **must backtest the exact settings on your specific index future and timeframe**; **multi-timeframe alignment (weekly agrees with daily) is the single biggest reliability booster**; and **position sizing / risk management matters more than the signal**.

---

## 1. Timeframe Model for the Daily-Short / Monthly-Long Diagonal

**The structure has two horizons, and only one of them carries directional risk.**

- **Long leg (~monthly):** a deep/ITM long call (PMCC) or long put (PMCP). This is the *directional* position — it profits or bleeds based on where the index future drifts over weeks. Per the sibling note, the PMCC/PMCP is "a long call/put diagonal that replicates a covered call/put" (tastylive) — the long leg is the anchor that must be on the right side of the trend.
- **Short leg (daily / very short-dated, rolled often):** a near-the-money call (PMCC) or put (PMCP) sold against the anchor to harvest theta. This is an **income/theta overlay**, not a directional forecast. Rolling it daily/weekly is a *premium-collection cadence*, not a series of new direction bets.

**Therefore the bias frame must match the leg that carries the risk — the monthly long leg — which lives on the swing/position horizon → the DAILY chart, with the WEEKLY as context.** This follows directly from Investopedia's multiple-time-frame principle: *"the longer the time frame, the more reliable the signals… As you drill down in time frames, the charts become more polluted with false moves and noise. Ideally, traders should use a longer time frame to define the primary trend"* and then act on the next frame down (Investopedia, Multiple Time Frames). A multi-week hold sits on the daily/weekly horizon; **intraday charts are below the trade's horizon and inject noise irrelevant to a multi-week directional anchor.**

**The two-timeframe (really three-chart) operating model — mapped to Investopedia's long/intermediate/short structure:**

| Chart | Investopedia role | Job in this structure | What it decides |
|---|---|---|---|
| **Weekly** | long-term = define the primary trend | **Regime / context** — is the bigger trend up or down? keeps you on the right side | Bull regime vs bear regime (a *veto*) |
| **Daily** | intermediate = the trading signal | **Bias decision** — run the regime + trigger + ADX stack here | **PMCC vs PMCP vs stand aside** |
| **Intraday** (e.g., 60-/15-min) | short-term = refine entry/exit | **Execution of the short leg only** — *when* to sell the daily short and at *what strike* | Timing & strike of each short-call/put roll, **within the daily/weekly direction** |

**The governing rule:** the **higher timeframe (daily, confirmed by weekly) decides WHICH trade and direction**; the **lower/intraday timeframe only refines WHEN and at WHAT strike to sell the short leg** — and you **only sell short calls (PMCC) when the higher-TF bias is bullish, short puts (PMCP) when it is bearish.** You never let an intraday wiggle flip the strategy; intraday is for execution, not direction. Investopedia: read the higher timeframe first to set the bias, act only on lower-timeframe signals that agree, and *"when time frames disagree, it can serve as a warning signal to pause or reassess."*

**Why not set the bias on the intraday (where the short leg lives)?** Because the short leg is not the directional position — it is theta. Letting the daily short's timeframe drive the *strategy* direction would have you flipping PMCC↔PMCP on noise, churning the expensive monthly anchor on intraday false moves. The anchor's direction is a daily/weekly decision; the short leg's *cadence* is the intraday decision.

## 2. The Decisive Best Method + Settings

**There is no single "most accurate" indicator — every reputable source surveyed ends with "combine with other tools."** So the decisive recommendation is a **default stack** built on the most robust directional backbone plus the one filter that most raises reliability.

### 2a. Which method is the most robust *primary engine*, and why

Comparing the leading trend-direction methods for index futures as a *primary directional engine*:

| Method | As a primary engine | Verdict |
|---|---|---|
| **EMA / MA confluence** (price + 20/50 EMA + 200 regime) | Objectively *"defines the current direction of the trend"* (StockCharts); it is the backbone the reputable published scans are built on (StockCharts MACD scan gates on `Close vs SMA(200)`; ADX scan gates on `Close vs SMA(50)`); one universal reading; scales cleanly across weekly+daily. | **Best primary engine** (directional backbone) |
| **Supertrend (ATR-based)** | Single unambiguous green/red line, volatility-adaptive, doubles as a trailing stop — but it is one line that *"generates false signals"* and whipsaws in chop (TradingView). | Best **single-line alternative / fallback** |
| **ADX / DMI** | Measures trend **strength**, not direction by itself ("ADX… regardless of direction"). +DI/−DI give direction but cross *"too frequently."* | **The key filter, not the engine** |
| **MACD** | Good trend+momentum *confirmation*; but standalone it whipsaws — StockCharts' own example shows *"seven centerline crossovers in five months"* with no trend. | Good **confirmation layer** |
| **Ichimoku** | All-in-one trend + S/R + a forward-looking cloud; but steep learning curve, chart clutter, and *"much less effective in periods of sideways consolidation."* | Best **all-in-one regime view** (advanced) |

**Decisive take:** make **moving-average / EMA confluence the primary directional engine** (it is the most robust, most universally-taught backbone), and **layer ADX on top as the reliability filter.** ADX is the key *"is this trend real?"* gate: Investopedia says to *"first use ADX to determine whether prices are trending or non-trending and then choose the appropriate trading strategy for the condition."* ADX answers *"is there a trend worth trading?"* **before** the EMA structure answers *"which way?"* Requiring **ADX > 25** removes the low-ADX chop where EMA crosses whipsaw — the single biggest reliability gain you can bolt onto an MA system.

### 2b. The ONE default stack (run on the DAILY index-futures chart)

| Layer | Tool & setting | Bullish (→ PMCC) | Bearish (→ PMCP) |
|---|---|---|---|
| **1. Regime** (context) | **200-period EMA** on the daily **+ weekly trend** | Price **above** 200-EMA **and** weekly up | Price **below** 200-EMA **and** weekly down |
| **2. Trigger** (direction) | **20-EMA vs 50-EMA** cross on the daily | **20-EMA > 50-EMA** (fresh up-cross/holding) | **20-EMA < 50-EMA** |
| **3. Strength** (is it real?) | **ADX(14)** with +DI/−DI | **ADX > 25** (≥20 min) **and +DI > −DI** | **ADX > 25** (≥20 min) **and −DI > +DI** |

**Decision:** all three bullish **and** weekly agrees → **PMCC**. All three bearish **and** weekly agrees → **PMCP**. **Any layer disagrees, or ADX < 20, or weekly conflicts → STAND ASIDE.**

**Typical settings (illustrative conventions — validate by backtest, Section 4):**

| Parameter | Default | Source / status |
|---|---|---|
| Regime MA | **200-period** EMA (or SMA) on daily | 200 = most popular long MA (StockCharts/Investopedia length bands) |
| Trigger pair | **20-EMA / 50-EMA** (medium-swing band) | medium band 20–60 (StockCharts/TradingView); 20/50 = labeled convention |
| ADX | **period 14**, **>25 strong / ≥20 minimum / <20 stand aside** | Wilder 14; 25/20 thresholds (StockCharts/Investopedia) |
| Weekly context | weekly **50/200** (golden/death) or weekly slope / price vs weekly 50-EMA | 50/200 regime (Investopedia) |

### 2c. The simplest fallback ("second-best")

- **Single Supertrend (ATR period 10, multiplier 3) on the daily** → **green = PMCC bias, red = PMCP bias.** Optionally gate it by price vs the 200-EMA (only take green above the 200-EMA, red below). One line, no ambiguity. *Caveat:* it whipsaws in chop, so still **stand aside when it flips repeatedly in a tight range** or while price is pinned to the 200-EMA. (10/3 is a community/platform default — labeled convention, not a TradingView-stated number.)
- **Absolute-minimalist version:** **price vs the 200-day MA on the daily, with the weekly agreeing** (regime-only). Above = PMCC bias, below = PMCP bias, oscillating right at it = stand aside. Heavily lagging but objective and self-fulfilling at the index level.

## 3. Why High-Accuracy Direction Is *Harder* for a Daily Short Leg (and the stand-aside rule)

Selling a **daily / very short-dated** option repeatedly is what makes a *clearly established* trend non-negotiable. The mechanism is **gamma**:

- A short option is **negative gamma**: *"short options are said to have 'negative gamma'… For a short option, the gamma value is subtracted from the option's delta when the underlying stock's price rises"* (tastylive, Gamma). So a short **call** (the PMCC overlay) gets a **more-negative delta as the index rallies** — its losses **accelerate** as the underlying pushes through the strike.
- That acceleration is largest where you actually sell for premium — **near-the-money**: *"gamma is generally higher for at-the-money (ATM) and in-the-money (ITM) options… Options with higher gamma are therefore more responsive to price changes in the underlying… the deltas of these options can change more quickly"* (tastylive). High gamma = the short strike's exposure can swing from "safely OTM" to "deep ITM" on a relatively small, fast move.
- For **very short-dated** options this sensitivity is most concentrated near expiry (a standard options principle — the tastylive 0DTE page was unreachable this session, so the *time-to-expiry* dimension is labeled a widely-taught convention rather than a fetched quote). The directly-sourced ATM = highest-gamma point already establishes the core risk.

**Consequence for the trader:** because the daily short is short-gamma and you re-establish it constantly, the position is **highly exposed to short-term whipsaw and to the short strike getting *run over* in a fast move** (including overnight gaps on a near-24h index future — see Section 4). In a choppy/low-ADX tape the short leg gets whipsawed both ways: you sell calls and a pop runs them over; you flip your read and the move reverses. The roll treadmill compounds it.

**That is precisely why direction must be CLEARLY established before this structure is appropriate:**

- Require a **clean regime** (price decisively on one side of the 200-EMA, weekly agreeing) and **high ADX (> 25)** so the underlying keeps drifting in your favor and your short strikes stay on the right side.
- **STAND ASIDE — "no clear direction, don't trade" — whenever:** **ADX < 20** (*"it might not be an ideal time to enter a trade,"* Investopedia); price is **chopping around the MAs** (the whipsaw zone where EMA/Supertrend flip); price is **inside the Ichimoku cloud** (consolidating); or the **weekly and daily disagree** (Investopedia: *"a warning signal to pause or reassess"*). For a daily-short structure, **the safest directional call is frequently "none — stand aside."**
- Note the asymmetry: in a *covered* diagonal a short strike run over is partly offset by the long anchor gaining, but the short leg's **income job is defeated** and you inherit roll-up/assignment management; and if the **anchor's own direction** is wrong (e.g., you hold a PMCC into a downtrend) the monthly long leg bleeds. Directional accuracy protects the anchor; gamma is why you must only sell shorts *with* the established trend, never into chop.

## 4. Confirmation & Backtesting (the honest caveats)

- **No method is high-accuracy alone.** Every reputable source surveyed ends with *"combine with other tools."* Investopedia (golden cross): *"no indicator can truly predict the future."* StockCharts (ADX): even the strength filter *"tends to filter as many good signals as bad."* Reliability comes from the **combination + discipline**, not from any one line.
- **Combining regime + trigger + ADX raises reliability but still LAGS.** Every component is built from past prices (EMAs, ATR bands, smoothed directional movement); stacking confirmations adds **more lag and fewer trades** — an accepted cost for screening out the ranges that wreck single-indicator systems. You will enter later and skip many setups by design.
- **Multi-timeframe alignment is the single biggest reliability booster.** Requiring the **weekly to agree with the daily** is the highest-leverage filter: *"the longer the time frame, the more reliable the signals,"* and disagreement is itself a stand-aside signal (Investopedia, Multiple Time Frames). One timeframe sets the bias; the other vetoes it.
- **You MUST backtest the exact settings on the specific index future and timeframe.** Defaults are not universal — StockCharts (ADX): Wilder's parameters were built for commodities/currencies, and *"chartists will likely need to adjust the indicator settings… according to the characteristics of the security."* Validate ADX 20 vs 25, the EMA lengths, and the Supertrend multiplier on **your** contract before trusting them.
- **Index-futures specifics to bake into the backtest:** futures trade nearly around the clock, so (1) fix a consistent **"daily close" reference** (e.g., session settlement) and apply the stack the same way every day; (2) account for **overnight/gap risk** that can run a daily short over before you can roll — another reason to demand a clean, high-ADX trend and to size the short conservatively; (3) backtest on a properly **back-adjusted continuous series or the actual front-month** you trade, since contract rolls create gaps that distort MA/ADX readings.
- **Risk management / position sizing matters more than the signal.** Investopedia (golden-cross bottom line): use *"profit targets, stop loss, and other risk management tools… rather than just following the cross mindlessly."* The direction read only sets the bias; sizing, defined risk, and exits determine survival — see the sibling note .copilot-tracking/research/subagents/2026-06-21/pmcc-and-risk-sizing-research.md (defined-risk ~1–3% of account; debit ≤ width; take profits at ~25–50%).
- **No fabricated statistics.** This note quotes **no** win-rate or accuracy percentage; reputable education publishes no reliable universal hit-rate, and any such figure would be misleading. All thresholds (ADX 20/25, EMA 20/50/200, Supertrend 10/3, MACD 12/26/9, Ichimoku 9/26/52) are **conventions, not performance guarantees.**

## 5. Sources

**Sourced facts (fetched, with the claim each supports):**

- **Investopedia — Multiple Time Frames** (`/articles/trading/07/timeframes.asp`): longer TF = more reliable; drilling down adds noise; long-term=trend / intermediate=signal / short-term=refine; *"when time frames disagree… pause or reassess."* → Sections 1, 4 and the timeframe decision.
- **Investopedia — ADX** (`/terms/a/adx.asp`): ADX = strength, +DI/−DI = direction; >25 strong / <20 trendless; *"first use ADX to determine whether prices are trending or non-trending…"*; DI crosses too frequent. → Sections 2, 3.
- **Investopedia — Golden/Death Cross** (`/terms/g/goldencross.asp`): 50/200 regime; *"reactive rather than proactive"*; *"no indicator can truly predict the future"*; risk-management bottom line. → Sections 2c, 4.
- **Investopedia — Ichimoku Cloud** (`/terms/i/ichimoku-cloud.asp`): above/below/inside cloud; *"much less effective in periods of sideways consolidation."* → stand-aside rule (Section 3).
- **Investopedia — EMA** (`/terms/e/ema.asp`): EMA hugs price; short/medium/long length bands. → Section 2 settings.
- **StockCharts ChartSchool — ADX/DMI, Moving Averages, MACD:** Wilder 14, 20/25 thresholds; MAs *"define the current direction of the trend"*; whipsaw examples; published scans gate on `Close vs SMA(200)` / `SMA(50)`; *"chartists will likely need to adjust the indicator settings."* → Sections 2, 4.
- **TradingView education — Supertrend** (`/support/solutions/43000634738`): ATR-based green/red flip; *"generates false signals"* in chop; combine with others; inputs atrLength & multiplier. → Sections 2a, 2c.
- **tastylive — Gamma** (`/concepts-strategies/gamma`): short options = **negative gamma**; short-call delta moves *more negative* as the underlying rises; **gamma higher for ATM/ITM → delta changes faster / more responsive.** → Section 3 (the core daily-short-leg risk).
- **tastylive — PMCC / Poor-Man-Covered-Put / Diagonal:** the structure = long-dated ITM long + short-dated short replicating a covered call/put. → Section 1 (the two-horizon framing). Detail in .copilot-tracking/research/subagents/2026-06-21/pmcc-and-risk-sizing-research.md.

**Sibling research reused (same folder):** .copilot-tracking/research/subagents/2026-06-21/robust-trend-direction-methods-research.md (the regime+trigger+ADX framework and full per-indicator sourcing), .copilot-tracking/research/subagents/2026-06-21/ema-crossover-direction-research.md (EMA bands, whipsaws, filters), .copilot-tracking/research/subagents/2026-06-21/pmcc-and-risk-sizing-research.md (structure + sizing).

**Unreachable this session (noted, not fabricated):**

- **Investopedia Gamma** (`/terms/g/gamma.asp`) and **Greeks** (`/trading/getting-to-know-the-greeks/`): extraction failed (same pattern as other Investopedia `/terms/` pages); gamma sourced from **tastylive** instead.
- **tastylive 0DTE Options** (`/concepts-strategies/zero-days-0dte-options-explained`): ad/iframe redirect. The *near-expiry gamma intensification* (time-to-expiry dimension) is therefore labeled a **standard, widely-taught convention**, not a fetched quote; the directly-sourced **ATM = highest gamma** point already carries Section 3.
- **BabyPips — Multiple Time Frame Analysis** (`/learn/forex/multiple-time-frame-analysis`): ad-system redirect (both this and the prior session). Recommended further reading; the multi-timeframe points are fully sourced via Investopedia + StockCharts.

**Labeled conventions (NOT source-stated performance claims):** EMA 20/50/200 pair, ADX 20/25 thresholds, Supertrend ATR 10 × 3, MACD 12/26/9, Ichimoku 9/26/52. Validate per instrument (Section 4).

## Open Items / Clarifying Questions

- **Which index future and account size?** Settings (ADX 20 vs 25, EMA lengths, Supertrend multiplier) must be backtested per instrument — Wilder's defaults were built for commodities and *"may not suit all markets."*
- **Does the short leg literally expire daily (0DTE) or weekly?** True daily/0DTE shorts maximize the negative-gamma run-over risk in Section 3; weekly shorts soften it. This changes how strict the "high-ADX / clean-regime only" gate should be.
- **Preferred trigger:** keep the default **20/50 EMA cross**, or substitute **Supertrend** or **MACD zero-line** as the daily trigger? (Engine = MA/EMA confluence regardless.)
- **Should a follow-up specify the exact intraday execution rules** for *when/what-strike* to roll the daily short (e.g., short delta target, roll trigger), constrained to the daily/weekly bias?
- **Gamma/0DTE deep-dive:** if the near-expiry gamma dimension needs an explicit citation, a future session can retry the tastylive 0DTE page or an OIC/CBOE gamma reference (both unreachable/awkward this session).
