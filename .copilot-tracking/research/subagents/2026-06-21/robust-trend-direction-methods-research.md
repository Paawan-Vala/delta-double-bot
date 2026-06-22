<!-- markdownlint-disable-file -->
# Robust Trend-Direction Methods (PMCC vs PMCP Bias) — Research

Status: Complete
Date: 2026-06-21
Purpose: Educational study note (NOT financial advice). Research the most reliable / robust methods for determining MARKET DIRECTION (trend bias) beyond simple EMA crossovers, and how to COMBINE them, for a trader choosing between a bullish multi-week options trade (Poor Man's Covered Call, ~30–60 DTE) and a bearish one (Poor Man's Covered Put).

> Disclaimer: All figures, thresholds, and default settings below are illustrative educational conventions attributed to their sources. No win-rate or accuracy statistic is fabricated; any percentage is labeled illustrative. Trend tools lag and fail in ranges. This is not financial advice. Options involve risk of loss.

## Research Topics & Questions

Direction/trend tools to cover (for EACH: how it signals direction, strengths, weaknesses, best use, typical default settings):

1. [x] ADX / DMI system (+DI, −DI, ADX line) — direction via +DI/−DI cross; ADX = trend STRENGTH (>25 strong, <20 weak/range); ADX as trend-vs-range FILTER
2. [x] Supertrend (ATR-based) — green/red flip for up/down trend, trailing direction signal; whipsaw in chop; settings (ATR 10, mult 3)
3. [x] MACD — signal-line and zero-line crosses for momentum/direction confirmation
4. [x] 200-day MA as classic BULL/BEAR REGIME filter (price above = bull, below = bear); 50-day vs 200-day (golden/death cross)
5. [x] Ichimoku Cloud — price above cloud = uptrend, below = downtrend (complete trend/regime view)
6. [x] Multi-timeframe trend alignment — weekly sets bias, act on daily ("trade in direction of higher-timeframe trend")

Core deliverables:

7. [x] Best-practice COMBINATION framework: REGIME FILTER (200-day MA / higher-TF) + TRIGGER (EMA cross or Supertrend flip) + STRENGTH CONFIRMATION (ADX > 20–25); why combining reduces false signals
8. [x] Mapping combined signal → directional bias for 30–60 DTE: bullish → PMCC; bearish → PMCP; no clear trend → STAND ASIDE
9. [x] Honest caveats: no holy grail / no single most-accurate indicator; trend tools fail in ranges; all lag; backtest per instrument/timeframe; risk management/sizing > entry signal; use DAILY (weekly context) not intraday for multi-week bias

## Sources (status)

- [x] Investopedia — **ADX** (`/terms/a/adx.asp`): FETCHED OK. Strength vs direction; ADX>25 strong / <20 trendless; +DI/−DI cross signals; ADX-as-filter; combine-with-other-tools caveat.
- [x] Investopedia — **Ichimoku Cloud** (`/terms/i/ichimoku-cloud.asp`): FETCHED OK. Five components (9/26/52); price above/below/inside cloud; cloud color; limitations (poor in consolidation, lag, clutter).
- [x] Investopedia — **Golden Cross / Death Cross** (`/terms/g/goldencross.asp`): FETCHED OK. 50/200 cross; MA becomes support/resistance; lagging / false-signal limitations; risk-management bottom line.
- [x] Investopedia — **Multiple Time Frames** (`/articles/trading/07/timeframes.asp`): FETCHED OK. Longer TF = more reliable; weekly=trend / daily=signal; disagreement = pause. (Note: `/articles/active-trading/052014/...` variant returned HTTP 404.)
- [x] StockCharts ChartSchool — **MACD** (`.../macd-...-oscillator`): FETCHED OK. 12/26/9; signal-line & zero-line crosses; whipsaw example; trend+momentum; sample scans paired with 200-day SMA.
- [x] StockCharts ChartSchool — **ADX/DMI** (`.../average-directional-index-adx`): FETCHED OK. Wilder system; 14-period; 20/25 thresholds + "gray zone"; DI cross system; scans pairing ADX>20 + DI cross + 50-day SMA; "filters as many good signals as bad" caveat.
- [x] TradingView education — **Supertrend** (`/support/solutions/43000634738-supertrend/`): FETCHED OK. ATR-based; green=above/up, red=below/down; flip on close; inputs atrLength & multiplier; false signals in chop; combine with MACD/PSAR/RSI.
- [ ] BabyPips — **ADX** & **Multiple Time Frame Analysis**: UNREACHABLE this session (404 / ad-redirect). Recommended as further reading; points covered via Investopedia + StockCharts.
- [~] Investopedia — **MACD** (`/terms/m/macd.asp`): extraction failed this session; superseded by StockCharts MACD.

---

## 1. ADX / DMI System

Designed by J. Welles Wilder for commodity daily charts; now used across many markets to judge the **strength** of a trend (Investopedia, ADX).

**The three lines (default period = 14):**
- **ADX line** — measures TREND STRENGTH only (direction-agnostic). "The ADX helps investors determine trend strength, while -DI and +DI help determine trend direction" (Investopedia).
- **+DI (positive directional indicator)** — upward directional movement.
- **−DI (negative directional indicator)** — downward directional movement.

**How it signals DIRECTION:**
- **+DI above −DI = bullish** bias; **−DI above +DI = bearish** bias.
- Crossovers generate signals: "if the +DI line crosses above the -DI line and the ADX is above 20, or ideally above 25, then that is a potential signal to buy." Conversely, −DI crossing above +DI with ADX > 20/25 is "an opportunity to enter a potential short trade" (Investopedia).
- Crosses can also exit trades (if long, exit when −DI crosses above +DI).

**How it signals STRENGTH (the filter use — verbatim thresholds, Wilder):**
- **ADX > 25 = strong trend.**
- **ADX < 20 = weak trend or trendless** ("the indicator is signaling that the price is trendless and that it might not be an ideal time to enter a trade").
- The 20–25 band is the transition/uncertain zone.
- **ADX as a trend-vs-range FILTER:** "Investors should first use ADX to determine whether prices are trending or non-trending and then choose the appropriate trading strategy for the condition" (Investopedia). This is the canonical filter pattern: ADX answers *"is there a trend worth trading?"* before +DI/−DI answers *"which way?"*

**Strengths:** Separates strength from direction (most single indicators conflate them); a purpose-built objective filter for trending vs ranging; widely available with one standard setting.

**Weaknesses:** ADX lags (it is a smoothed average of smoothed values). DI "crossovers can occur frequently, sometimes too frequently, resulting in confusion" — these false signals "are more common when ADX values are below 25." ADX can also poke above 25 "only there temporarily and then reverses." ADX rising tells you a trend is strong but NOT its direction (you still need +DI/−DI). Investopedia: "Like any indicator, the ADX should be combined with price analysis and potentially other indicators."

**Best use:** As the **strength-confirmation / regime gate** in a combined system — only act on a directional trigger when ADX confirms a trend is present (>20–25). Investopedia explicitly pairs it with RSI for entry/exit timing: "While the ADX measures the intensity of the trend, the RSI can help with entries and exits."

**Wilder's system & the combination pattern (StockCharts ChartSchool, ADX):** The +DI/−DI/ADX group is a complete trading system from Wilder's 1978 *New Concepts in Technical Trading Systems*. "In general, the bulls have the edge when +DI is greater than −DI, while the bears have the edge when −DI is greater." Strength: "a strong trend is present when ADX is above 25 and no trend is present when ADX is below 20. There appears to be a gray zone between 20 and 25… Many technical analysts use 20 as the key level." Wilder's rule: require **ADX above 25 (many use 20)**, then **buy when +DI crosses above −DI** (sell when −DI crosses above +DI), initial stop at the signal-day low. StockCharts' own published scan encodes the full three-layer stack: `ADX(14) > 20 AND +DI crosses −DI AND Close > 50-day SMA` for longs (mirror for shorts) — and advises "focus on +DI buy signals when the bigger trend is up and −DI sell signals when the bigger trend [is down]."

**Default settings:** Period **14** (Wilder-recommended, per StockCharts; "by default… calculated using 14 periods"); strong-trend threshold **25**, weak/no-trend threshold **20** (Wilder), with **20** widely used as the practical key level.

## 2. Supertrend (ATR-based)

"Supertrend is a trend-following indicator based on Average True Range (ATR). The calculation of its single line combines trend detection and volatility. It can be used to detect changes in trend direction and to position stops." Created by Olivier Seban (TradingView, Supertrend).

**How it signals DIRECTION:** Supertrend is overlaid on price as a single line that flips sides:
- **Price ABOVE the curve → line turns GREEN → uptrend (bullish).**
- **Price BELOW the curve → line turns RED → downtrend (bearish).**
- "After each close above or below Supertrend, a new trend appears" — i.e., each flip is a discrete trend-change signal, and the line trails price as a dynamic stop. It is a **trailing direction signal**: stay long while green, stay short/flat while red.

**Inputs:** `atrLength` (lookback for the ATR calculation) and `multiplier` (what ATR is multiplied by to offset the bands from price). Larger multiplier / longer ATR = less sensitive (fewer flips); smaller = more sensitive (more flips). Bands are built from `hl2 ± multiplier × ATR`.

**Strengths:** Simple, visual, unambiguous (you are either green or red); volatility-adaptive because the band width scales with ATR; doubles as a trailing-stop tool; works on any timeframe/instrument.

**Weaknesses:** "There are times when it generates false signals" (TradingView). In **choppy / sideways markets it whipsaws** — price repeatedly closes just across the band, flipping the trend color back and forth and generating losing reversals. Like all ATR/MA-derived tools it lags the actual turn. TradingView: "it is best to use the right combination of several indicators… such as MACD, Parabolic SAR, or RSI."

**Best use:** As the **directional TRIGGER / trailing-trend layer** in a combined system — take the green/red flip only when a higher-level regime filter and a strength filter agree (so chop-flips are ignored).

**Default settings:** TradingView documents the two inputs but does not fix the numbers in its definition page. The widely cited de-facto defaults are **ATR period 10, multiplier 3** (common platform default / community convention — label as convention, not a TradingView-stated value).

## 3. MACD (Moving Average Convergence/Divergence)

Developed by Gerald Appel (late 1970s); "one of the most popular momentum indicators." The MACD "turns two trend-following indicators (moving averages) into a momentum oscillator by subtracting the longer moving average from the shorter one" — giving "the best of both worlds: trend following and momentum" (StockCharts ChartSchool, MACD).

**Components (default 12, 26, 9):**
- **MACD Line** = 12-period EMA minus 26-period EMA.
- **Signal Line** = 9-period EMA of the MACD line.
- **Histogram** = MACD Line minus Signal Line.

**How it signals DIRECTION / momentum (two key crosses):**
- **Signal-line crossovers (most common):** bullish when the MACD line crosses **above** the signal line; bearish when it crosses **below**. These are momentum-turn triggers and "can last a few days or a few weeks."
- **Centerline / zero-line crossovers (the trend-direction read):** bullish when the MACD line crosses **above zero** (12-EMA moves above 26-EMA, positive = upside momentum); bearish when it crosses **below zero**. Per StockCharts: a centerline cross "can suggest a change in the overall trend." MACD stays positive in a sustained uptrend and negative in a sustained downtrend — so **the zero line is effectively a fast EMA-regime flag**.
- **Divergences:** MACD diverging from price can foreshadow reversals (but see weaknesses).

**Strengths:** Combines trend and momentum in a single tool; applies to daily/weekly/monthly charts; the zero-line cross gives a clean direction confirmation while the signal-line cross gives an earlier momentum trigger — useful as the **confirmation layer** in a combined system.

**Weaknesses:** Lags (built from EMAs). Whipsaws when no strong trend follows the cross — StockCharts' own example (CMI) shows "seven centerline crossovers in five months" that "would have resulted in numerous whipsaws because strong trends did not materialize." Divergences are unreliable: "Bearish divergences are commonplace in a strong uptrend, while bullish divergences occur often in a strong downtrend." Not suited to overbought/oversold (no bounds); raw values are not comparable across securities (use PPO for that).

**Best use:** Direction/momentum **confirmation**, ideally filtered by a higher-level trend gate. Notably, StockCharts' own sample scans pair MACD with the 200-day MA: the bullish signal-line-cross scan requires **price above its 200-day SMA**, and the bearish scan requires **price below its 200-day SMA** — a concrete, citable example of the regime-filter + trigger combination (see Section 7).

**Default settings:** **12, 26, 9** (standard). More sensitive: MACD(5,35,5) ("might be better suited for weekly charts"); lengthening the EMAs reduces sensitivity and crossover frequency (StockCharts).

## 4. 200-Day Moving Average (Regime Filter) + 50/200 Cross

**Price vs the 200-day MA = the classic BULL/BEAR REGIME filter.** The simplest robust regime read is whether price trades **above** its 200-day moving average (bull regime) or **below** it (bear regime). This is not just folklore: StockCharts' own published MACD scans encode it directly — the bullish setup requires "Daily Close > Daily SMA(200)" and the bearish setup requires "Daily Close < Daily SMA(200)" (StockCharts ChartSchool, MACD). The 200-day MA after a cross "is considered a major support level… or resistance level… for the market from that point forward" (Investopedia, Golden Cross).

**50-day vs 200-day (Golden Cross / Death Cross) = the regime *change* signal:**
- **Golden Cross = bullish:** a short-term MA crosses **above** a long-term MA — "such as the 50-day moving average crosses above its 200-day moving average." "The 50-day moving average crossover up through the 200-day moving average on an index like the S&P 500 is one of the most popular bullish market signals" (Investopedia).
- **Death Cross = bearish:** the short-term MA crosses **below** the long-term MA → signals a possible long-term bear market.
- After the cross, the long MA becomes **support** (golden) or **resistance** (death).
- Three stages of a golden cross: (1) prior downtrend bottoms as buyers overpower sellers; (2) short MA crosses above long MA, confirming the reversal; (3) continuing uptrend with the MAs acting as support on pullbacks.
- "The larger the chart time frame, the stronger and more lasting the… breakout."

**Strengths:** Objective, widely watched (self-fulfilling at the index level), and an excellent *slow* regime/context filter — it keeps you on the right side of the dominant trend and out of counter-trend trades.

**Weaknesses:** Heavily lagging. "All indicators are lagging… they indicate past performance so they are reactive rather than proactive… no indicator can truly predict the future. Many times, an observed golden cross produces a false signal" and golden crosses "also regularly fail to manifest" (Investopedia). Because the signal only appears *after* the market has already moved, it is poor for timing entries — it is a **context filter, not a trigger**. Whipsaws badly when price oscillates around the MA in a range.

**Best use:** The **regime gate** of the combined framework — only take bullish triggers when price is above the 200-day MA (and/or 50 > 200), and bearish triggers when below. Investopedia: "use it with other tools… use profit targets, stop loss, and other risk management… time your trade rather than just following the cross mindlessly."

**Default settings:** **200-day** SMA for the regime line; **50-day / 200-day** SMA pair for golden/death cross (Investopedia). Some traders use the 50-day as a faster intermediate regime line.

## 5. Ichimoku Cloud

Developed by Goichi Hosoda (Japanese journalist/technical analyst), refined over decades and released publicly as an all-in-one system in the 1960s. Designed to show "the asset or market in its entirety, including trend direction, momentum, and support and resistance levels" (Investopedia, Ichimoku Cloud).

**Five components (default settings 9 / 26 / 52, displaced 26):**
- **Conversion Line (Tenkan-sen)** = midpoint of highest high & lowest low over **9** periods — short-term trend.
- **Base Line (Kijun-sen)** = midpoint over **26** periods — medium-term trend / equilibrium.
- **Leading Span A (Senkou Span A)** = (Conversion + Base)/2, plotted **26 periods into the future** — faster cloud boundary.
- **Leading Span B (Senkou Span B)** = midpoint over **52** periods, plotted 26 into the future — slower cloud boundary.
- **Lagging Span (Chikou Span)** = current close plotted **26 periods into the past** — trend confirmation.
- The **Cloud (Kumo)** = the shaded area between Leading Span A and B.

**How it signals DIRECTION (a complete trend/regime view):**
- **Price ABOVE the cloud = uptrend / bullish** (cloud acts as support).
- **Price BELOW the cloud = downtrend / bearish** (cloud acts as resistance).
- **Price INSIDE the cloud = consolidating / sideways** — "a breakout above the Cloud would be bullish, while one below it signals a potential downtrend."
- **Cloud color/orientation:** bullish cloud when Span A > Span B; bearish when Span A < Span B. A rising Span B signals an uptrend; falling Span B confirms a downtrend.
- **Secondary triggers:** Conversion crossing above Base = short-term bullish momentum ("Signals are stronger when they occur above or below the Cloud itself"); Lagging Span above past price confirms uptrend. Thicker cloud = stronger trend & stronger S/R; sharper cloud angle = stronger trend.

**Strengths:** One indicator gives trend direction, momentum, and dynamic support/resistance — a complete regime view. "Because it is so comprehensive, the Cloud filters out a lot of noise." Rare **forward-looking** element (projects 26 periods ahead), helping anticipate continuation/reversal. "The Cloud works best in trending markets."

**Weaknesses:** "Much less effective in periods of sideways consolidation." Steep learning curve; "some lag due to its reliance on historical data"; chart clutter from five components; "default parameters may not suit all markets." Investopedia recommends customizing parameters and filtering signals with other indicators (e.g., RSI).

**Best use:** As a standalone **regime/trend filter** (above/below cloud) and trend-following framework on the higher timeframe; combine with a momentum oscillator for entry timing.

**Default settings:** **9, 26, 52** with 26-period displacement (Investopedia / standard convention).

## 6. Multi-Timeframe Trend Alignment

"Markets exist in several time frames simultaneously… there can be conflicting trends within a particular stock depending on the time frame… It is not out of the ordinary for a stock to be in a primary uptrend while being mired in intermediate and short-term downtrends" (Investopedia, Multiple Time Frames).

**Core principle:** "A general rule is that **the longer the time frame, the more reliable the signals**. As you drill down in time frames, the charts become more polluted with false moves and noise. Ideally, traders should use a longer time frame to define the primary trend." Then use the preferred timeframe for the signal and a faster one to refine entry/exit.

**The three-chart structure:** long-term chart = define the **trend/bias**; intermediate chart = provide the **trading signal**; short-term chart = **refine** entry/exit ("used to confirm or dispel a hypothesis from the primary chart"). Example given: a swing trader uses **weekly to define the primary trend, daily for decisions**, 60-minute to refine.

**How it sets DIRECTION:** Read the **higher timeframe first** to set the bias, then act only on lower-timeframe signals that agree with it — "trade in the direction of the higher-timeframe trend." When timeframes **disagree**, that is itself information: "When time frames disagree, it can serve as a warning signal to pause or reassess a trade."

**Strengths:** Filters out lower-timeframe noise; aligns short-term actions with the broader trend; the disagreement case is a built-in stand-aside rule.

**Weaknesses:** Can produce conflicting signals and "the likelihood of overtrading"; demands more screen time; too much drilling-down invites over-analysis ("do not get caught up in the noise of a short-term chart").

**Best use (and why DAILY-with-weekly for a multi-week options trade):** For a ~30–60 DTE PMCC/PMCP, the trade *lives* on the swing/position timescale, so the **weekly chart sets the directional bias and the daily chart provides the trigger/entry timing.** Intraday charts are below the relevant horizon — they add noise and false moves that are irrelevant to a multi-week hold. This maps directly onto Investopedia's swing-trader example (weekly = primary trend, daily = decisions).

**Default "setting":** Use timeframes roughly 4–6× apart (e.g., **weekly → daily**); pick the timeframe that matches your holding period as the *signal* frame and the one above it as the *bias* frame.

## 7. Best-Practice Combination Framework (Regime + Trigger + Strength)

The robust, widely-taught approach is **not** to hunt for one "best" indicator but to **stack three complementary layers that each fail in different conditions**, and act only when they agree. No source surveyed claims a single indicator is reliable alone — every one ends with "combine with other tools."

| Layer | Job | Tools (pick one per layer) | Direction read |
|---|---|---|---|
| **1. Regime filter** (slow, context) | Decide which direction you are *allowed* to trade; keep you on the right side of the dominant trend | **200-day MA** (price above = bull, below = bear) and/or **50/200 golden/death cross**; or **weekly higher-timeframe** trend; or **Ichimoku cloud** position | Bull regime vs bear regime |
| **2. Trigger** (timing) | Provide the actual entry impulse, in the direction Layer 1 allows | **EMA crossover**, **Supertrend green/red flip**, or **MACD** signal-line / zero-line cross (on the daily) | Fresh bullish vs bearish signal |
| **3. Strength confirmation** | Confirm a real trend exists so the trigger isn't a range whipsaw | **ADX > 20–25** with **+DI/−DI** agreeing with the trade side | Trend present & strong enough |

**The rule:** take a **long/PMCC** setup only when Layer 1 = bull **and** Layer 2 fires bullish **and** Layer 3 confirms (ADX > 20–25, +DI > −DI); take a **short/PMCP** setup only when all three line up bearish. If any layer disagrees or Layer 3 is weak, **do nothing**.

**Why stacking reduces false signals (the core logic):**
- A **regime filter alone** lags badly and cannot time an entry (Investopedia: golden cross is "reactive rather than proactive" and "regularly" gives false signals).
- A **trigger alone** whipsaws in sideways markets (StockCharts: MACD "would have resulted in numerous whipsaws because strong trends did not materialize"; TradingView: Supertrend "generates false signals" in chop; ADX page: "+DI and −DI crossovers are quite frequent").
- A **strength gauge alone** gives no direction (ADX measures strength "regardless of direction").
- Requiring all three to align means you only act when there is (a) an established regime, (b) a fresh directional impulse, **and** (c) measured trend strength — precisely the condition trend-following tools are built for, which screens out the ranges where they fail.

**This pattern is independently encoded by reputable sources (evidence, not opinion):**
- **StockCharts MACD scans:** bullish signal-line cross **only when** `Close > 200-day SMA`; bearish **only when** `Close < 200-day SMA`. = regime (200-MA) + trigger (MACD).
- **StockCharts ADX scans / chart example:** `ADX(14) > 20` **and** DI cross **and** `Close > 50-day SMA` for longs (mirror for shorts); "Only buy signals are used when trading above the 50-day moving average." = regime (50-MA) + trigger (DI cross) + strength (ADX).
- **Investopedia ADX:** "first use ADX to determine whether prices are trending or non-trending and then choose the appropriate trading strategy." = strength filter gating strategy choice.
- **Investopedia multi-timeframe:** weekly defines the trend/bias, daily provides the signal. = higher-timeframe regime + lower-timeframe trigger.
- **TradingView Supertrend / Ichimoku (Investopedia):** both explicitly recommend confirming with additional indicators (MACD, RSI, etc.).

**Honest trade-off:** more confirmation = **more lag and fewer trades**. You will enter later and skip many setups; the payoff is avoiding the low-quality, range-bound signals that wreck single-indicator systems. Combining reduces — it does **not** eliminate — false signals.

## 8. Mapping to PMCC vs PMCP (Including When to Stand Aside)

Translate the combined signal into a directional bias for a **~30–60 DTE** options trade. Read the **weekly chart for bias, the daily chart for the trigger** (a multi-week hold lives on the swing/position timescale — intraday signals are below the horizon and add noise).

| Combined read (weekly bias + daily trigger + ADX) | Bias | Trade |
|---|---|---|
| Price **above** 200-day MA / weekly up **and** daily trigger bullish (EMA up-cross / Supertrend green / MACD bullish) **and** ADX > 20–25 with +DI > −DI | **Bullish** | **PMCC** (Poor Man's Covered Call — long-dated ITM call diagonal) |
| Price **below** 200-day MA / weekly down **and** daily trigger bearish (EMA down-cross / Supertrend red / MACD bearish) **and** ADX > 20–25 with −DI > +DI | **Bearish** | **PMCP** (Poor Man's Covered Put — long-dated ITM put diagonal) |
| **No clear trend** — see stand-aside triggers below | **None** | **STAND ASIDE** (don't force a directional trade) |

**STAND ASIDE when any of these is true (don't force PMCC or PMCP):**
- **ADX < 20** — trend is weak/absent; Investopedia: "it might not be an ideal time to enter a trade."
- **Price chopping around the moving averages** — the whipsaw zone where MA/EMA/Supertrend signals flip repeatedly.
- **Price inside the Ichimoku cloud** — "the market is in a sideways trend or consolidating" (wait for a clean break above/below the cloud).
- **Timeframes disagree** — weekly and daily point opposite ways; Investopedia: "When time frames disagree, it can serve as a warning signal to pause or reassess a trade."

**Why standing aside matters here:** PMCC and PMCP are **directional** structures — they need the underlying to drift (or hold) in the chosen direction over weeks to realize the diagonal's edge. In a range, a directional multi-week bias has no edge and the long option bleeds theta while the trend tools whipsaw. "No trade" is the correct output of the framework when the layers don't align.

**Scope note:** This maps only the **directional entry bias**. It does **not** replace the trade-construction and risk rules (strike/delta selection, debit ≤ width, profit-taking at 25–50%, position sizing at ~1–3% defined-risk) covered in the sibling note `.copilot-tracking/research/subagents/2026-06-21/pmcc-and-risk-sizing-research.md`. Per that research and Section 9, **sizing and exits drive the outcome more than the entry signal.**

## 9. Honest Caveats (No Holy Grail)

- **There is no single "most accurate" indicator / no holy grail.** Every reputable source surveyed ends with "combine with other tools." Investopedia (golden cross): "no indicator can truly predict the future." StockCharts (ADX): even adding the ADX strength filter "tends to filter as many good signals as bad." The robustness comes from the *combination and the discipline*, not from any one line on the chart.
- **Trend tools work in trends and fail in ranges.** Ichimoku is "much less effective in periods of sideways consolidation" (Investopedia); Supertrend "generates false signals" in chop (TradingView); MACD whipsaws "because strong trends did not materialize" (StockCharts); ADX < 20 = stand aside. The combined framework's main job is to keep you out of these ranges.
- **All of these tools lag.** They are built from past prices (SMAs, EMAs, ATR bands, smoothed directional movement). Golden cross is "reactive rather than proactive" and "identified only after the market has risen"; ADX has "a fair amount of lag because of all the smoothing." Stacking confirmations adds *more* lag — an accepted cost for fewer false signals.
- **Backtest on the specific instrument and timeframe; defaults are not universal.** StockCharts (ADX): Wilder's parameters were designed for commodities/currencies — "Stocks with low volatility may not generate signals based on Wilder's parameters. Chartists will likely need to adjust the indicator settings… according to the characteristics of the security." Ichimoku: "default parameters may not suit all markets." Validate thresholds (ADX 20 vs 25), MA lengths, and Supertrend multiplier on *your* underlying and timeframe before trusting them.
- **Risk management and position sizing matter more than the entry signal.** Investopedia (golden cross bottom line): the key to using any such signal correctly is "to use profit targets, stop loss, and other risk management tools… maintain a favorable risk-to-reward ratio… rather than just following the cross mindlessly." The direction read only sets the bias; sizing, defined risk, and exits determine survival (see `pmcc-and-risk-sizing-research.md`).
- **Use DAILY signals with WEEKLY context — not intraday — for a multi-week options bias.** A 30–60 DTE PMCC/PMCP is a swing/position-horizon trade; the weekly sets the bias and the daily triggers it. "As you drill down in time frames, the charts become more polluted with false moves and noise" (Investopedia). Intraday charts sit below the trade's horizon and inject noise irrelevant to a multi-week hold.
- **No fabricated statistics.** This note deliberately quotes *no* win-rate or accuracy percentage for any indicator or combination; reputable education does not publish reliable universal hit-rates, and any such figure would be misleading. Default thresholds (ADX 20/25, MACD 12/26/9, Supertrend 10/3, Ichimoku 9/26/52, 50/200 MA) are conventions, not performance guarantees.

## Open Items / Clarifying Questions

- **BabyPips unreachable this session:** both `babypips.com/learn/forex/multiple-time-frame-analysis` (redirected to an ad-system URL) and `babypips.com/learn/forex/trading-with-adx` (HTTP 404) failed to return content. BabyPips' School of Pipsology does cover ADX and multiple-time-frame analysis and is recommended as further reading; the same points are fully sourced here from Investopedia and StockCharts.
- **Investopedia MACD term page** (`/terms/m/macd.asp`) did not extract this session; MACD is instead fully sourced from **StockCharts ChartSchool (MACD)**, which is the more detailed reference anyway.
- **Supertrend default numbers (ATR 10 / multiplier 3):** TradingView's definition page documents the two *inputs* but does not state fixed default numbers in the fetched text; 10/3 is the de-facto platform/community default and is labeled as a convention, not a TradingView-stated value. Confirm the exact default on the user's charting platform.
- **Clarifying questions for the user:** (1) Which underlying(s) and account size — so settings can be backtested per instrument? (2) Preferred regime filter — 200-day MA, weekly trend, or Ichimoku? (3) Preferred trigger — EMA cross, Supertrend, or MACD? (4) Should a follow-up note specify exact ADX/EMA/Supertrend parameters and a written entry checklist for the chosen instrument?
