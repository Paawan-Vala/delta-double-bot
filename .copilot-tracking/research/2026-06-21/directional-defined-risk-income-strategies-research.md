<!-- markdownlint-disable-file -->
# Task Research: Directional, Defined-Risk, Low-Capital Income Strategies

Goal: From the 74 macroption strategies already compiled, identify the best strategies for a trader who wants to (a) trade **directionally** (has an up or down view), (b) keep **loss strictly limited / hedged**, (c) use **low capital**, and (d) aim for **steady monthly profit**. Back the shortlist with practical detail: capital/margin needs, strike selection, management rules, realistic return expectations, and risk caveats.

> Educational research only — not financial advice. Options trading can lose money; "good monthly profit" is never guaranteed and high win-rate income strategies still take occasional large (capped) losses.

## Task Implementation Requests

* Recommend which DIRECTIONAL strategies fit: low capital + limited/hedged loss + monthly income.
* Explain why, with capital efficiency, risk/reward, and management.
* Provide a beginner-friendly starting plan.

## Scope and Success Criteria

* Scope: Directional + defined-risk + capital-efficient strategies. Primary candidates: the 4 vertical spreads (bull call, bull put, bear call, bear put), long diagonal call/put (Poor Man's Covered Call/Put), and — with caveats — ratio backspreads. Excludes naked/unlimited-risk and pure neutral-income strategies (iron condor etc. are neutral, not directional).
* Assumptions (stated; to confirm with user):
  * Small account (e.g., a few hundred to a few thousand units of capital).
  * Beginner-to-early-intermediate experience.
  * Access to liquid optionable underlyings (index ETFs / large caps).
  * Wants monthly (~30–45 DTE) cadence.
* Success Criteria:
  * A ranked shortlist with clear "use when bullish / bearish" mapping.
  * Capital + risk-per-trade guidance for a small account.
  * Concrete management rules (entry delta, profit target, stop, DTE, roll).
  * Honest expectation-setting and caveats.

## Candidate Shortlist (from existing study notes)

| Strategy | Direction | Open | Capital | Defined risk? | Income-capable | Difficulty |
|----------|-----------|------|---------|---------------|----------------|------------|
| Bull Put Spread | Bullish | Credit | Low (collateral = width − credit) | Yes | Yes (sell premium) | Intermediate |
| Bear Call Spread | Bearish | Credit | Low | Yes | Yes (sell premium) | Intermediate |
| Bull Call Spread | Bullish | Debit | Low (cost = debit) | Yes | Directional | Intermediate |
| Bear Put Spread | Bearish | Debit | Low | Yes | Directional | Intermediate |
| Long Diagonal Call (PMCC) | Bullish | Debit | Moderate (LEAPS cost) | Yes | Yes (roll short call) | Advanced |
| Long Diagonal Put | Bearish | Debit | Moderate | Yes | Yes (roll short put) | Advanced |
| Call/Put Ratio Backspread | Directional | Credit/debit | Low–moderate | Yes (limited loss) | No (dead-zone loss) | Advanced |

## Outline

1. Vertical credit spreads as the core directional income engine (bull put / bear call)
2. Vertical debit spreads as cheap directional bets (bull call / bear put)
3. Diagonals / PMCC as a monthly-income directional approach for slightly larger small accounts
4. Risk management & position sizing for small accounts
5. Realistic return expectations and caveats
6. Recommended starter plan

## Potential Next Research

* Confirm user's directional bias, capital size, and market/underlying — would sharpen the recommendation.

## Research Executed

* Subagent: directional vertical spreads for income (output: .copilot-tracking/research/subagents/2026-06-21/directional-vertical-spreads-income-research.md)
  * Sourced from macroption (payoff/break-even), Investopedia and tastylive (capital, delta, DTE, management).
* Subagent: PMCC / diagonals + small-account risk sizing (output: .copilot-tracking/research/subagents/2026-06-21/pmcc-and-risk-sizing-research.md)
  * Sourced from macroption (diagonal definitions), tastylive (PMCC mechanics, sizing), Investopedia (1%/2% rules).

## Key Discoveries

### Capital math (the decisive small-account facts)

* Credit spread (Bull Put, Bear Call): buying-power/collateral = max loss = (strike width − net credit) × 100.
  * Example $5-wide bull put: sell 45 put $2.00 / buy 40 put $0.75 → credit $1.25; collateral ≈ $375; max profit $125; B/E 43.75.
  * Example $5-wide bear call: sell 35 call $2.50 / buy 40 call $0.50 → credit $2.00; collateral $300; max profit $200; B/E 37.
* Debit spread (Bull Call, Bear Put): capital = max loss = net debit × 100 (smallest absolute ticket).
  * Example $5-wide bull call: buy 50 call $3 / sell 55 call $2 → debit $1.00 = $100 cost; max profit $400; B/E 51 (~4:1 R/R).
* PMCC (long call diagonal): tastylive example — buy $90 LEAP call $15 ($1,500) vs $10,000 for 100 shares (~85% less); sell 30-day $105 call $2 → net debit $1,300 = max loss; max profit ≈ width − net debit; B/E ≈ long strike + net debit.

### Management conventions (illustrative, sourced)

* Entry ~30–45 DTE; manage/exit ~21 DTE.
* Credit spreads: sell short strike ~0.30 delta (~70% baseline OTM) or ~0.16 delta (~84%, ≈1 SD) for higher win rate; target credit ≈ 1/4–1/3 of width.
* Close at ~50% of max profit (both credit and debit) — tastylive convention.
* Credit-spread asymmetry: high win rate but max loss > max profit, so discipline matters (one full loss ≈ several wins).
* Debit spreads: lower win rate but reward can exceed risk; want low IV / trend. Credit spreads: want high IV / range-bound-to-mild drift.

### Risk sizing (sourced)

* Defined-risk per trade ≈ 1–3% of account (tastylive); small accounts < $20k may be pushed to 5–7% per ticket → hold fewer positions.
* Investopedia 1%/2% rule: risk ≤ 1–2% per trade; 10 straight losses at 2% ≈ 20% drawdown.
* Trade liquid underlyings (SPY/QQQ/IWM, large caps); tight bid/ask; avoid holding through earnings unless intended; defined-risk only; keep cash in reserve; mind per-roll fees on small accounts.

## Technical Scenarios

### Selected approach (ranked for: low capital + limited loss + directional + monthly income)

1. PRIMARY — Vertical credit spreads: Bull Put Spread (bullish) and Bear Call Spread (bearish).
   * Why: lowest practical capital ($300–375 collateral for a $5-wide), defined risk, paid up front, high win rate, positive theta = the cleanest "directional monthly income" engine. Best when you have a directional lean and IV is elevated / market range-bound-to-trending your way.
2. SECONDARY — Vertical debit spreads: Bull Call Spread (bullish) and Bear Put Spread (bearish).
   * Why: smallest absolute cost ($100–300), max loss = the debit, reward can exceed risk; most beginner-friendly to reason about; best for a clear trend / low IV. Less "income," more "cheap directional bet."
3. GRADUATE-TO — PMCC (long call diagonal) / long put diagonal once the account grows.
   * Why: ~85% less capital than a covered call and repeatable monthly income via rolling the short option, but needs more capital than a vertical and adds calendar/IV, rolling, and assignment complexity. Better suited once comfortable.

Rationale: credit verticals are the best direct fit for all four constraints simultaneously; debit verticals are the gentlest on-ramp and the cheapest tickets; PMCC is the capital-efficient "covered-call-style income" upgrade for later. Iron condors and other neutral strategies are excluded because the user explicitly wants a directional approach.

### Recommended starter plan (beginner, small account)

* Underlyings: liquid ETFs (SPY/QQQ/IWM) or liquid large caps; check tight bid/ask + open interest.
* Structure: bullish → Bull Put Spread (income) or Bull Call Spread (cheap bet); bearish → Bear Call Spread (income) or Bear Put Spread (cheap bet).
* Width: start narrow ($1–$5) to keep max loss tiny.
* Entry: ~30–45 DTE; credit spreads sell ~0.16–0.30 delta short strike; target ~1/3 of width credit.
* Size: risk ~1–3% of account per trade (max loss is known up front); few concurrent positions; keep cash reserve.
* Manage: take ~50% of max profit; exit ~21 DTE; avoid earnings unless intended; defined-risk only.

### Considered alternatives (not selected as primary)

* Ratio backspreads (directional, limited risk): defined risk and big-move upside, but they carry a mid-range "dead zone" loss and are advanced — not a steady monthly-income tool.
* Covered call / cash-secured put: directional income but capital-heavy (need 100 shares / full cash) — fails the low-capital constraint; PMCC is the capital-efficient substitute.
* Neutral defined-risk income (iron condor/butterfly): great defined-risk income but NOT directional — excluded by the user's requirement.
