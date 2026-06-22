<!-- markdownlint-disable-file -->
# Task Research: Market-Direction Detection for PMCC / PMCP Timing

Goal: The trader uses Poor Man's Covered Call (PMCC, bullish) and Poor Man's Covered Put (PMCP, bearish) — both ~30–60 DTE directional income trades. They want a reliable, accurate way to decide the MARKET DIRECTION (bullish vs bearish) from the futures chart to choose PMCC vs PMCP. They proposed EMA crossovers (9/20 or 9/50). Research the most accurate / robust trend-direction methods, the trade-offs of EMA crossovers, and how to reduce false signals — then recommend a concrete directional framework aligned to a multi-week options horizon.

> Educational research only — NOT financial/trading advice. No indicator predicts direction with guaranteed accuracy; all trend signals lag and fail in ranges. Backtesting and risk management matter more than the signal itself.

## Task Implementation Requests

* Find the "top accurate" strategy for determining market direction from futures.
* Evaluate EMA crossovers (9/20, 9/50, others) and alternatives.
* Recommend a direction framework to pick PMCC (bullish) vs PMCP (bearish).

## Scope and Success Criteria

* Scope: Trend-direction / directional-bias methods on a swing/position timeframe (daily), since PMCC/PMCP are multi-week. Includes EMA crossovers, MA regime filters, Supertrend, ADX/DMI, MACD, Ichimoku, multi-timeframe alignment, and how to combine them.
* Assumptions (stated; to confirm):
  * Instrument is an index future (e.g., Nifty/Bank Nifty or S&P) — method is largely instrument-agnostic.
  * Direction read for a ~30–60 DTE options bias → primary timeframe = DAILY (with weekly regime context), not 1–5 min intraday.
* Success Criteria:
  * Clear verdict on EMA-cross accuracy + how to filter whipsaws.
  * A ranked, combinable framework (regime filter + trigger + strength confirmation).
  * Concrete mapping to PMCC vs PMCP with honest caveats.

## Candidate Methods (to evaluate)

| Method | Role | Strength | Weakness |
|--------|------|----------|----------|
| EMA crossover (9/20, 9/21, 20/50) | Trigger | Simple, clear flips | Whipsaws in ranges, lag |
| 50/200 MA (golden/death cross) | Regime filter | Defines bull/bear regime | Very slow, late |
| 200-day MA (price above/below) | Regime filter | Classic trend gauge | Lagging |
| Supertrend (ATR) | Trigger/trail | Clear directional flips, dynamic stop | Whipsaws in chop |
| ADX / DMI (+DI/−DI) | Strength + direction | Filters trend vs range | Lags; ADX direction-agnostic |
| MACD | Momentum/direction | Momentum confirmation | Lags, false crosses |
| Ichimoku cloud | Trend/regime | All-in-one trend view | Complex |
| Multi-timeframe alignment | Filter | Reduces counter-trend trades | Fewer signals |

## Outline

1. EMA crossover mechanics, which pair/timeframe, accuracy & whipsaw problem
2. Regime filters (200-MA, 50/200) to set the bull/bear backdrop
3. Confirmation tools (ADX/DMI, Supertrend, MACD) to cut false signals
4. Multi-timeframe alignment for a swing/monthly bias
5. Recommended combined framework + PMCC/PMCP mapping
6. Caveats & realistic expectations

## Potential Next Research

* Confirm instrument + timeframe to tailor exact EMA/ADX parameters.

## Research Executed

* Subagent: EMA crossover direction (output: .copilot-tracking/research/subagents/2026-06-21/ema-crossover-direction-research.md)
  * Sources: Investopedia (EMA, golden/death cross, ADX, crossover), StockCharts ChartSchool (moving averages), TradingView, Fidelity.
* Subagent: robust trend-direction methods (output: .copilot-tracking/research/subagents/2026-06-21/robust-trend-direction-methods-research.md)
  * Sources: Investopedia (ADX, Ichimoku, golden/death cross, multiple timeframes), StockCharts (MACD, ADX/DMI), TradingView (Supertrend).
  * SECURITY: both StockCharts pages embedded an "Agent Instructions / ?ask=" block (GitBook feature) — flagged as untrusted, not followed.

## Key Discoveries

### Timeframe verdict

* For a ~30–60 DTE PMCC/PMCP bias, read direction on the DAILY chart with WEEKLY context. 5-minute/intraday crossovers are the wrong tool (noise/whipsaw, irrelevant to a multi-week hold). Moving averages are lagging — they confirm/identify trend, they do not predict it.

### EMA-pair guidance (answering the user's 9/20 vs 9/50)

* 9/20 (and 9/21): short-term/momentum — more signals, more whipsaws; suited to intraday/fast swings.
* 9/50: medium — fewer, smoother signals.
* 20/50 (daily): the practical sweet spot for a swing/multi-week directional bias.
* 50/200 (golden/death cross): used as the REGIME FILTER, not the entry trigger — too slow to initiate a 6–12 week trade, but good as the bull/bear backdrop.
* Length bands (illustrative, source-named): short 5–20, medium 20–60, long 100+.

### The whipsaw problem + filters that cut false signals (all source-backed)

* Bare EMA crossovers fail in sideways/range markets (false signals cluster). They work best in strong trends.
* Filters: (1) longer-term/200-day regime filter (take bullish crosses only above the 200-day); (2) ADX > 20–25 trend-strength gate; (3) slow-MA slope + price location; (4) multi-timeframe agreement (weekly sets bias); (5) wait for candle close / persistence buffer to avoid intra-bar fakeouts.

### Robust direction tools (for the combination)

* ADX/DMI: +DI>−DI = bullish, −DI>+DI = bearish; ADX measures STRENGTH (>25 strong, <20 weak/range). Best used as a trend-vs-range filter. Default ADX 14.
* Supertrend (ATR): flips green/red for up/down; trailing direction signal; whipsaws in chop. Convention ATR 10 × multiplier 3.
* MACD (12/26/9): signal-line / zero-line crosses for momentum/direction confirmation.
* 200-day MA: classic bull/bear regime filter (price above = bull, below = bear); 50/200 cross variant.
* Ichimoku cloud (9/26/52): price above cloud = uptrend, below = downtrend, inside = no-trade.
* Multi-timeframe alignment: trade in the direction of the higher-timeframe (weekly) trend.

### Honest accuracy framing

* No single "most accurate" indicator / no holy grail — every source says combine tools. All trend tools lag and fail in ranges. Backtest per instrument/timeframe (Wilder's defaults were for commodities). Risk management/position sizing matters more than the entry signal.

## Technical Scenarios

### Selected approach — the "top accurate" practical framework (3-layer stack)

The most reliable answer is NOT one magic indicator but a confluence of three complementary layers on the DAILY futures chart; act only when all three agree:

1. REGIME FILTER (which side am I allowed to trade?): price vs 200-day MA (and/or weekly trend / Ichimoku cloud). Above = bullish regime only; below = bearish regime only.
2. TRIGGER (timing the impulse): daily EMA crossover (20/50 primary; 9/20 as a faster early trigger) OR Supertrend flip OR MACD cross.
3. STRENGTH CONFIRMATION (is it a real trend?): ADX > 20–25 with +DI/−DI agreeing with the trigger.

Rationale: each layer fails in different conditions (regime filters lag/can't time; triggers whipsaw in chop; ADX is direction-agnostic). Requiring all three to align only fires when there is an established regime + fresh impulse + measured strength — exactly the condition trend tools are built for — screening out the ranges where crossovers fail. (Pattern independently encoded by StockCharts' published scans and Investopedia's ADX-filter / weekly-bias-daily-signal guidance.)

### Mapping to PMCC vs PMCP

* Bull regime + bullish daily trigger + ADX > 20–25 (+DI > −DI) → PMCC (bullish call diagonal).
* Bear regime + bearish daily trigger + ADX > 20–25 (−DI > +DI) → PMCP (bearish put diagonal).
* STAND ASIDE (don't force a directional 30–60 DTE trade) when ADX < 20, price chops around the MAs, price is inside the Ichimoku cloud, or weekly/daily disagree.

### Concrete daily-chart checklist (starter default)

1. Regime: Is price above (bull) or below (bear) the 200-day MA / 200 EMA?
2. Trigger: Has the 20 EMA crossed the 50 EMA in that same direction (on a closed daily candle)? (Optionally use 9/20 for an earlier read, confirmed by 20/50.)
3. Strength: Is ADX(14) > 20–25 and is the correct DI on top (+DI for bull, −DI for bear)?
4. Higher TF: Does the weekly trend agree?
5. If all yes → take PMCC (bull) or PMCP (bear). If mixed/ADX low → stand aside.

### Considered alternatives (not selected as the sole method)

* Bare EMA crossover alone: rejected as primary — too many whipsaws in ranges without a regime + strength filter.
* Single regime filter (200-MA only): good context but no timing — too slow to initiate a multi-week trade alone.
* Supertrend or MACD alone: usable as the trigger layer but still need the regime + ADX filters to cut chop. Interchangeable within the framework.

## Addendum: Daily-Short / Monthly-Long Diagonal (decisive recommendation)

Source: subagent dual-timeframe diagonal direction (output: .copilot-tracking/research/subagents/2026-06-21/dual-timeframe-diagonal-direction-research.md). New source this round: tastylive Gamma (short options = negative gamma).

### Structure clarified

* PMCC here = buy a ~monthly call (long anchor, carries the directional risk) + sell a very short-dated/DAILY call (theta/income overlay, rolled often). PMCP = mirror with puts.
* Two horizons in one trade: the monthly long leg is the direction bet; the daily short leg is an income overlay.

### Timeframe verdict (decisive)

* The DAILY futures chart sets the PMCC-vs-PMCP bias; the WEEKLY is the regime/context veto above it. The monthly long leg carries the directional risk, so read its bias on the daily and confirm with the weekly.
* The daily short leg is NOT the direction driver. An intraday chart only refines WHEN and at WHAT strike to sell the short call/put — and you only sell in the direction the daily/weekly bias already allows. (Maps to Investopedia's 3-chart model: long-term = trend, intermediate = signal, short-term = refine.)

### The one default stack (run on the DAILY index-futures chart)

* Regime: price vs 200-EMA AND weekly agrees.
* Trigger: 20/50 EMA cross (on a closed daily candle).
* Strength: ADX(14) > 25 (min 20) with +DI/−DI agreeing.
* All bullish + weekly up → PMCC. All bearish + weekly down → PMCP. Anything else → STAND ASIDE.
* Engine = MA/EMA confluence; ADX is the key "is this trend real?" filter that most raises reliability.

### Simplest fallback

* Single Supertrend (ATR 10 × 3) on the daily — green → PMCC, red → PMCP — optionally gated by the 200-EMA.
* Minimalist: price vs the 200-day MA + weekly agreeing.

### Why the daily short leg makes a clean trend MORE important (new mechanics insight)

* A short option is NEGATIVE GAMMA (tastylive). Selling a DAILY call/put means very high short-gamma exposure: in chop or a fast counter-move the short strike gets run over and the daily roll treadmill compounds the whipsaw losses.
* Therefore the trend must be CLEARLY established (high ADX, clean regime) before running this; in low-ADX/chop the safest "direction" call is "no clear direction — don't trade." Stand-aside triggers: ADX < 20, price chopping around the MAs, price inside the Ichimoku cloud, or weekly/daily disagreement.

### Honest caveats

* No method is high-accuracy alone — every source ends with "combine with other tools"; the stack still lags. Thresholds are conventions, not performance claims, and MUST be backtested on the specific index future (fix a daily-close reference, account for overnight gap run-over, use a back-adjusted/front-month series).
* Multi-timeframe alignment (weekly agrees with daily) is the single biggest reliability booster. Sizing/risk management matters more than the signal. No win-rate figure is asserted.

### Open items to tailor (need user input)

* Which index future + account size (settings are instrument-specific, must be backtested).
* Does the short leg literally expire daily (0DTE) or weekly? True 0DTE maximizes negative-gamma run-over risk → use a stricter high-ADX/clean-regime gate.
* Keep 20/50 EMA trigger, or substitute Supertrend / MACD zero-line (engine stays MA confluence).
