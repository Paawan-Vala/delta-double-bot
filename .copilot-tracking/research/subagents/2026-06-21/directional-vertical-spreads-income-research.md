<!-- markdownlint-disable-file -->
# Directional Vertical Spreads for Small-Capital Monthly Income — Research

Status: Complete
Date: 2026-06-21
Purpose: Educational study note (NOT financial advice). Research how a small-capital, beginner-to-intermediate trader uses directional vertical spreads for monthly income with strictly limited (hedged) risk.

> Disclaimer: All figures below are illustrative educational conventions attributed to their sources. Win-rates and returns are not guarantees. Options involve risk of loss.

## Research Topics & Questions

Four strategies to cover (all defined-risk, directional, low capital):

1. Bull Put Spread (bullish credit spread)
2. Bear Call Spread (bearish credit spread)
3. Bull Call Spread (bullish debit spread)
4. Bear Put Spread (bearish debit spread)

For EACH strategy, document:

- [x] Exact capital / buying-power requirement (credit: collateral = width − net credit; debit: cost = net debit) + concrete $ worked example (e.g., $5-wide spread)
- [x] Typical strike selection by delta (e.g., short strike ~0.30 / 0.16 delta) and mapping to probability of profit
- [x] Net credit-to-width ratio realistically expected, and reward vs risk implication
- [x] Typical DTE for monthly income (e.g., 30–45 DTE) and why
- [x] Management rules: profit target (e.g., 50% max profit), stop-loss / exit (e.g., 1–2x credit, short strike breached), time-based exit (e.g., 21 DTE)
- [x] Realistic win-rate vs payoff trade-off (high win rate but losses > wins for credit spreads)
- [x] Pros/cons for a small account

Also:

- [x] Comparison: credit spreads (bull put / bear call) vs debit spreads (bull call / bear put) for a small account — capital efficiency, trending vs range-bound, beginner-friendliness
- [x] Management rules cheat sheet

## Sources (status)

- macroption.com: bull-put-spread, bear-call-spread, bull-call-spread, bear-put-spread — FETCHED OK (payoff / break-even / max P/L definitions)
- macroption.com: option-delta — FETCHED OK (delta ≈ probability of expiring ITM)
- Investopedia: bullputspread, bearcallspread, bullcallspread, bearputspread — FETCHED OK (worked $ examples, max P/L, breakeven, pros/cons)
- tastylive: vertical-spread, bull-put-spread, debit-spreads, managing-winners, delta — FETCHED OK (delta/probability, 50% profit target, 21 DTE, credit-vs-debit, worked examples)
- tastylive: probability-of-profit, standard-deviation, bear-call-spread — BLOCKED (anti-bot redirect to cloudfront iframe this session)
- Options Industry Council (optionseducation.org/strategies/all-strategies/bull-put-spread) — NOT EXTRACTABLE this session (JS-rendered). Recommended as further reading.
- CBOE — cited indirectly via tastylive delta page (cboe.com/insights "Learning the Greeks"). Direct CBOE strategy page not fetched.
- Fidelity / Schwab learning centers — Fidelity options-strategy-guide URL returned a generic landing page (JS-rendered); not extractable this session.

---

## 0. Shared Foundations (apply to all four spreads)

**Defined-risk vertical spread = one long + one short option, same type, same expiration, different strikes.** Trading directionally with max profit AND max loss known at entry (tastylive, "vertical spread"; macroption).

**Capital / buying-power rule of thumb (the single most important small-account fact):**

- Credit spread (bull put, bear call): collateral / buying-power reduction = max loss = (strike width − net credit) × 100. The cash credit is received up front; the broker holds the remaining risk as buying power. (Investopedia max-loss = capital at risk; tastylive defined-risk.)
- Debit spread (bull call, bear put): capital = cost = net debit × 100. You pay it up front; that debit is also the entire max loss. (tastylive debit-spreads; Investopedia.)

**Delta → probability (strike selection):** macroption — "the absolute value [of delta] indicates the approximate probability of the option expiring in the money" (e.g., 0.90-delta call ≈ 90% chance ITM; 0.025-delta ≈ ~unlikely). tastylive delta page lists delta as "Probability of the stock expiring $0.01 beyond the strike … (in-the-money)."
- Therefore a short strike at ~0.30 delta ≈ ~30% chance of finishing ITM ≈ ~70% chance of expiring worthless (baseline probability of keeping the full credit). The credit cushion pushes the breakeven beyond the short strike, so realized probability of profit (POP) is usually a few points HIGHER than (1 − short-strike delta).
- A short strike at ~0.16 delta ≈ ~16% chance ITM ≈ ~84% OTM ≈ the 1-standard-deviation level (standard-normal tail ≈ 16%). Lower delta short strike = higher POP but smaller credit.
- Call + put delta at the same strike ≈ 1.0, consistent with the two mutually exclusive outcomes summing to ~100% (macroption).

**Credit-to-width ratio (what to realistically expect):** From the OTM income-style examples gathered (see each section), net credit on out-of-the-money short verticals tends to land roughly **1/4 to 1/3 of the strike width** (e.g., $1.25 credit on a $5 width = 25%; $1.50 on $5 = 30%; $2.00 on $5 = 40% when the short strike sits closer to the money). Common income-trader heuristic: target ≈ 1/3 of the width in credit. The closer the short strike is to the money (higher delta), the larger the credit but the lower the POP — a direct trade-off.

**DTE for monthly income:** ~30–45 days to expiration is the standard income window (tastylive's well-known "~45 DTE" entry convention). Rationale: time decay (theta) is meaningful but gamma/"whipsaw" risk is still moderate that far out; ~45 DTE also lines up with one trade per monthly cycle. Income traders commonly exit around 21 DTE (tastylive "21 DTE" research/episodes) or roughly 30 days before expiration (Investopedia, bull call spread) to avoid the accelerating gamma risk of the final weeks.

**Management (income-trader conventions):**
- Profit target: close at ~50% of max profit. tastylive (vertical spread page): "All four types of profitable vertical spreads will be closed at a more favorable price than the entry price (goal: 50% of maximum profit)." Example given: credit received $150 → close when it can be bought back for $75. The 50% figure is "a guideline, not a rule."
- Why manage winners: tastylive (managing winners) — taking the trade off early can push the realized win rate ABOVE the entry POP and reduces the time capital is exposed; near max profit, remaining reward is small relative to risk still held.
- Time exit: ~21 DTE regardless of P/L is a common mechanical exit (tastylive).
- Stop-loss on losers: two schools exist and should both be noted:
  1. Many broker/education sources teach a stop at roughly 1.5×–2× the credit received, or exit if the short strike is breached / tested.
  2. tastylive's stated approach for DEFINED-risk spreads is that "losing positions are generally not defended" because the max loss is already known and capped at entry (they may roll for a credit if the short still has more extrinsic value than the long). 
  Both are legitimate; the choice depends on the trader's plan. (Illustrative conventions, not rules.)

**Win-rate vs payoff (the core trade-off):**
- Credit spreads: high probability of profit, but "your maximum loss, while capped, is generally higher than your maximum potential profit" (tastylive, debit-spreads page). → many small wins, occasional larger losses. Risk-management discipline matters because one full loss can erase several wins.
- Debit spreads: lower probability of profit, but reward can exceed risk (R/R > 1 is achievable). → fewer wins, larger payoff per win.

> All percentages (e.g., "70% POP") below are illustrative conventions tied to delta/strike selection, not guarantees of future results.

---

## 1. Bull Put Spread (Bullish Credit Spread)

**Structure (macroption; tastylive):** Sell a higher-strike put (closer to ATM) + buy a lower-strike put, same expiration. Net credit. Also called short put spread / credit put spread. Bullish: profits if the underlying rises or merely stays above the short strike.

**Payoff math (macroption; tastylive):**
- Max profit = net credit received (underlying at/above the short/higher strike at expiration → both puts expire worthless).
- Max loss = strike width − net credit (underlying at/below the long/lower strike).
- Breakeven = short put strike − net credit.

**Capital / buying-power + worked $ example:**
- Buying-power reduction = max loss = (width − credit) × 100.
- Clean OTM "income" example ($5-wide), tastylive bull-put example 2: XYZ at $50; sell the $45 put for $2.00, buy the $40 put for $0.75 → net credit $1.25 ($125). Width $5.
  - Max profit = $125. Max loss = ($5 − $1.25) × 100 = $375 → collateral ≈ $375. Breakeven = $45 − $1.25 = $43.75. Credit/width = 25%.
- Illustrative near-the-money example (Investopedia AAPL, ITM-skewed — shows how a richer credit lowers POP): spot $275; sell $280 put $8.50, buy $270 put $2.00 → credit $6.50 ($650), width $10. Max profit $650; max loss = ($10 − $6.50) × 100 = $350; breakeven $273.50. Credit/width 65% (because the short put is in-the-money — far less likely to expire worthless).

**Strike selection by delta → POP:** Income traders typically sell the short put around ~0.30 delta (~70% baseline chance it expires OTM) for a balanced credit, or ~0.16 delta (~84%, ≈1 SD) for a higher win rate and smaller credit. Lower delta = higher POP, smaller credit/width.

**Credit-to-width realistically:** ~1/4–1/3 of width for OTM short puts (25% in the clean example). Higher only if you sell closer to/through the money (which lowers POP).

**DTE:** ~30–45 DTE entry; manage ~21 DTE / 50% profit.

**Management:** Close at ~50% of max profit (e.g., buy back the $1.25 credit for ~$0.63); time-exit ~21 DTE; optional stop ~1.5–2× credit or if the short put is breached (or, tastylive style, accept the capped max loss / roll for a credit).

**Win-rate vs payoff:** High POP (~70% at 30-delta short), but a full loss ($375) is ~3× a full win ($125) at 25% credit/width — typical credit-spread asymmetry. IV/time decay help (positive theta, short vega): a drop in implied volatility benefits the spread (tastylive).

**Pros (small account):** Income up front; defined risk; profits from up, flat, or even slightly-down moves; positive theta; only ~$375 collateral for a $5-wide. **Cons:** capped profit; max loss > max profit; assignment risk on the short put (esp. near/through the strike or ex-dividend); ties up buying power.

---

## 2. Bear Call Spread (Bearish Credit Spread)

**Structure (macroption; tastylive):** Sell a lower-strike call (closer to ATM) + buy a higher-strike call, same expiration. Net credit. Also called short call spread / credit call spread. Bearish: profits if the underlying falls or merely stays below the short strike. It is the hedged version of a short call (the long higher call caps the otherwise-unlimited risk).

**Payoff math (macroption; tastylive):**
- Max profit = net credit (underlying at/below the short/lower strike → both calls expire worthless).
- Max loss = strike width − net credit (underlying at/above the long/higher strike).
- Breakeven = short call strike + net credit.

**Capital / buying-power + worked $ example (Investopedia):** Stock at $30; sell the $35 call for $2.50, buy the $40 call for $0.50 → net credit $2.00 ($200). Width $5.
- Max profit = $200. Max loss = ($5 − $2.00) × 100 = $300 → collateral ≈ $300. Breakeven = $35 + $2 = $37. Credit/width = 40% (short strike fairly close to spot).
- Buying-power reduction = max loss = (width − credit) × 100.

**Strike selection by delta → POP:** Sell the short call around ~0.30 delta (~70% chance OTM) or ~0.16 delta (~84%, ≈1 SD) for a higher win rate. Both strikes OTM with the short strike closer to the money is "probably the most common" construction (macroption). Lower delta short call = higher POP, smaller credit.

**Credit-to-width realistically:** ~1/4–1/3 of width for clearly-OTM short calls; the 40% above reflects a short strike only ~$5 above a $30 stock (relatively close). Positive theta, short vega (tastylive/macroption: benefits from passing time and IV contraction).

**DTE:** ~30–45 DTE; manage ~21 DTE / 50% profit.

**Management:** Close at ~50% of max profit; time-exit ~21 DTE; optional stop ~1.5–2× credit or if the short call is breached (or accept capped max loss / roll for credit, tastylive style).

**Win-rate vs payoff:** Mirror image of the bull put — high POP, but max loss ($300) > max profit ($200). Many small wins, occasional larger losses.

**Pros (small account):** Income up front; defined risk; "far less risk than shorting the stock" (Investopedia); profits from down/flat/slightly-up; positive theta. **Cons:** capped profit; max loss > max profit; short-call assignment risk (especially around ex-dividend dates); ties up buying power.

---

## 3. Bull Call Spread (Bullish Debit Spread)

**Structure (macroption; tastylive; Investopedia):** Buy a lower-strike call + sell a higher-strike call, same expiration. Net debit. Also called long call spread / debit call spread. Bullish: needs a moderate up-move.

**Payoff math (macroption; tastylive):**
- Max loss = net debit paid (underlying at/below the long/lower strike → both calls worthless).
- Max profit = strike width − net debit (underlying at/above the short/higher strike).
- Breakeven = long call strike + net debit.

**Capital + worked $ example (Investopedia, ABC):** Stock $50; buy the $50 call for $3.00, sell the $55 call for $2.00 → net debit $1.00 ($100). Width $5.
- Capital / max loss = net debit = $100. Max profit = ($5 − $1) × 100 = $400. Breakeven = $50 + $1 = $51. Cost/width = 20% → reward:risk ≈ 4:1.
- tastylive variant (more ITM, lower R/R): buy $50 call $5, sell $55 call $3 → debit $2 ($200), width $5; max profit ($5−$2)×100 = $300, max loss $200, breakeven $52; R/R 1.5:1. (Buying the long leg deeper ITM raises cost/POP but lowers R/R.)

**Strike selection by delta:** Commonly buy a near-ATM/ITM call (≈0.50–0.70 delta long) and sell an OTM call (≈0.30 delta short) to cap cost. Cheaper, lower-probability structures buy/sell further OTM. (Debit spreads are net long premium → you need the directional move; negative theta, positive vega.)

**Cost-to-width realistically:** Net debit typically a substantial fraction of width; the cheaper the spread (further OTM), the higher the R/R but the lower the probability. The $100-on-$5 (20%) example is an attractive 4:1 but requires the stock to clear $55.

**DTE:** ~30–45 DTE for a monthly directional theme; some traders close ~30 days before expiration (Investopedia) since time decay works against a debit spread.

**Management:** tastylive applies the same ~50% of max profit target to debit spreads (e.g., max profit $250 → close at +$125). Losers generally not defended (max loss = debit is known); close before expiration to avoid assignment/fees.

**Win-rate vs payoff:** Lower POP than a credit spread, but reward can exceed risk (4:1 in the clean example). Fewer wins, bigger payoff per win.

**Pros (small account):** Cheapest absolute outlay (often $100–$300 for a $5-wide); max loss = exactly what you pay; cheaper than buying a naked call; no collateral beyond the debit; clean "most I can lose is the ticket price" math. **Cons:** needs the move (and reasonably soon — negative theta); capped upside; forfeits gains above the short strike; lower win rate.

---

## 4. Bear Put Spread (Bearish Debit Spread)

**Structure (macroption; tastylive; Investopedia):** Buy a higher-strike put + sell a lower-strike put, same expiration. Net debit. Also called long put spread / debit put spread. Bearish: needs a moderate down-move.

**Payoff math (macroption; tastylive):**
- Max loss = net debit paid (underlying at/above the long/higher strike → both puts worthless).
- Max profit = strike width − net debit (underlying at/below the short/lower strike).
- Breakeven = long put strike − net debit.

**Capital + worked $ examples (Investopedia):**
- $5-wide: stock $30; buy the $35 put for $4.75, sell the $30 put for $1.75 → net debit $3.00 ($300), width $5. Capital/max loss $300; max profit ($5 − $3) × 100 = $200; breakeven $32. (ITM long put → higher cost, R/R 0.67:1.)
- $10-wide OTM (better R/R) — LEVI: spot $50; buy the $40 put $4, sell the $30 put $1 → net debit $3 ($300), width $10. Max loss $300; max profit ($10 − $3) × 100 = $700; breakeven $37 (= higher strike − net debit). R/R ≈ 2.33:1.
- tastylive variant: buy $50 put $5, sell $45 put $2 → debit $3 ($300), width $5; max profit ($5−$3)×100 = $200, max loss $300, breakeven $47.

**Strike selection by delta:** Buy a near-ATM/ITM put (≈0.50–0.70 delta long), sell a lower-strike OTM put (≈0.30 delta) to reduce cost. Further-OTM structures are cheaper with higher R/R but lower probability. Net long premium → negative theta, positive vega; you want the move (and ideally rising IV).

**Cost-to-width realistically:** Varies widely with how ITM the long leg is — 60% of width in the ITM $5-wide example (low R/R) vs 30% in the OTM $10-wide example (R/R 2.33:1).

**DTE:** ~30–45 DTE for a monthly bearish theme; close before the final weeks to limit time decay.

**Management:** ~50% of max profit target (tastylive); losers generally not defended (capped at the debit); close before expiration.

**Win-rate vs payoff:** Lower POP, but reward can exceed risk (2.33:1 OTM example). Fewer wins, larger payoff.

**Pros (small account):** Defined, modest cost = entire max loss; "less risky than simple short-selling" (Investopedia); cheaper than a naked put; no collateral beyond debit. **Cons:** needs a timely down-move (negative theta); capped profit; lower win rate; early-assignment risk on the short put.

---

## 5. Comparison: Credit vs Debit Spreads for a Small Account

| Dimension | Credit spreads (bull put, bear call) | Debit spreads (bull call, bear put) |
|---|---|---|
| Cash flow at entry | Receive credit | Pay debit |
| Capital tied up ($5-wide) | Collateral = width − credit (≈ $300–$375) | Cost = debit (≈ $100–$300) |
| Max loss | Width − credit (> max profit) | The debit (often < max profit) |
| Probability of profit | High (sell ~0.16–0.30 delta) | Lower |
| Reward : risk | < 1 (small wins, bigger losses) | Can be > 1 (bigger wins, smaller losses) |
| Theta (time) | Positive — time helps | Negative — time hurts |
| Vega (IV) | Short vega — wants IV to fall | Long vega — wants IV to rise |
| Best directional view | Range-bound to mildly directional ("stays above/below the short strike"; tastylive: "price stays within a range / moves only slightly against you") | Trending — "expect the price to go up or down, but not dramatically" (tastylive) |
| Ideal IV environment | High IV (sell rich premium, hope it contracts) — tastylive | Low IV (buy cheaper premium) — tastylive |

**Which is more capital-efficient?** In absolute dollars, a debit spread is usually the smaller ticket (e.g., $100 for a 4:1 $5-wide bull call vs ~$375 collateral for a $5-wide bull put). But the credit spread "earns" its keep through a higher win rate and positive theta; the debit spread risks less cash but must be right on direction (and timing). For the very smallest accounts, debit spreads let you take a defined directional shot for the least cash; credit spreads generate more consistent income but lock up more buying power per position.

**Trending vs range-bound:** Use DEBIT spreads when you expect a real directional move (trend) and especially when IV is low. Use CREDIT spreads when you expect the underlying to drift your way or simply not move against you (range-bound to mildly directional) and IV is elevated — you get paid by time decay even if the stock goes nowhere.

**Beginner-friendliness:** Debit spreads are arguably the easiest to reason about — "the most I can lose is exactly what I paid," no collateral mechanics, and assignment is less of a daily concern. Credit spreads are the classic monthly-income workhorse (high win rate, paid up front) but carry the harder behavioral math — losses are bigger than wins, so one undisciplined loss can wipe out several winners, and there is short-option assignment risk to manage. A common path: learn the mechanics on debit spreads, then graduate to credit spreads with strict 50%-profit / defined-risk management.

---

## 6. Management Rules Cheat Sheet

| Rule | Convention | Source |
|---|---|---|
| Entry DTE | ~30–45 DTE (one monthly cycle) | tastylive (~45 DTE) |
| Short-strike delta (credit) | ~0.30 delta (~70% OTM) balanced; ~0.16 delta (~84%, ≈1 SD) safer | macroption / tastylive (delta ≈ prob ITM) |
| Credit target (credit spreads) | ≈ 1/4 to 1/3 of strike width | Examples gathered (25–40% of width) |
| Profit target | Close at ~50% of max profit (both credit & debit) | tastylive (vertical spread; managing winners) |
| Time exit | ~21 DTE regardless of P/L | tastylive (21 DTE research) |
| Stop / loss exit | School A: ~1.5–2× credit, or short strike breached. School B (tastylive defined-risk): don't defend; accept capped max loss or roll short for a credit | broker/education convention vs tastylive |
| IV filter | Sell credit in high IV; buy debit in low IV | tastylive |
| Capital at risk | Credit: (width − credit) × 100. Debit: net debit × 100 | Investopedia / tastylive |

**Worked profit-target example (credit):** $5-wide bull put, $1.25 credit ($125 max profit). 50% target = close for ~$0.63 → bank ~$62 and free the ~$375 of buying power for the next cycle.

---

## 7. Caveats & Clarifying Questions

**Caveats:**
- Educational only — NOT financial advice. Options can lose money; defined-risk still means you can lose the full max loss.
- All win-rate / POP figures (e.g., "~70%") are illustrative conventions derived from delta≈probability and standard-normal tails, not guarantees. No specific historical performance statistics were fabricated.
- macroption pages define the payoff/break-even/max-P&L precisely but do not give capital/BP, delta targets, DTE, or management rules — those come from Investopedia and tastylive.
- The "sell ~0.30 / ~0.16 delta," "collect ~1/3 of width," and "stop at 1.5–2× credit" figures are widely-used income-trader heuristics; exact numbers vary by source and were partly inferred from the gathered worked examples plus the sourced delta≈probability relationship. The 16-delta ≈ 1 SD link rests on the standard-normal tail (~16%) combined with delta≈prob-ITM.
- tastylive's probability-of-profit, standard-deviation, and bear-call-spread pages, the OIC (optionseducation.org) strategy page, and Fidelity's options-strategy-guide page could NOT be extracted this session (anti-bot redirect / JS rendering). The conventions they would corroborate are sourced elsewhere here, but direct OIC/CBOE/Fidelity/Schwab citations remain a gap to close.
- Assignment / early-exercise risk (especially around ex-dividend) applies to every short option leg and is a real small-account hazard not captured by the payoff diagram.
- Commissions/fees matter disproportionately on small spreads (tastylive managing-winners): don't manage so early that fees eat the edge.

**Clarifying questions for the user:**
1. Underlying universe — single stocks, ETFs (SPY/QQQ/IWM), or index options? (Index options are cash-settled and avoid early assignment, which matters a lot for credit spreads on a small account.)
2. Account size and per-trade risk budget? (Drives strike width, e.g., $1-wide vs $5-wide, and number of contracts.)
3. Cash account vs margin account? (Defined-risk spreads are allowed in many cash accounts, but buying-power treatment differs.)
4. Do you want me to chase down direct OIC/CBOE/Schwab/Fidelity citations to replace the blocked sources, or is the current macroption + Investopedia + tastylive sourcing sufficient for the study note?

---

## 8. References

macroption.com (payoff, break-even, max P&L, delta-as-probability):
- [Bull Put Spread](https://www.macroption.com/bull-put-spread/)
- [Bear Call Spread](https://www.macroption.com/bear-call-spread/)
- [Bull Call Spread](https://www.macroption.com/bull-call-spread/)
- [Bear Put Spread](https://www.macroption.com/bear-put-spread/)
- [Option Delta](https://www.macroption.com/option-delta/) — "the absolute value [of delta] indicates the approximate probability of the option expiring in the money."

Investopedia (worked $ examples, max P&L, breakeven, pros/cons):
- [Bull Put Spread](https://www.investopedia.com/terms/b/bullputspread.asp)
- [Bear Call Spread](https://www.investopedia.com/terms/b/bearcallspread.asp)
- [Bull Call Spread](https://www.investopedia.com/terms/b/bullcallspread.asp)
- [Bear Put Spread](https://www.investopedia.com/terms/b/bearputspread.asp)

tastylive (delta/probability, 50% profit target, 21 DTE, IV regime, credit vs debit, worked examples):
- [Vertical Spreads](https://www.tastylive.com/concepts-strategies/vertical-spread) — "goal: 50% of maximum profit"; max-profit/breakeven formulas; setup conventions.
- [Bull Put Spread](https://www.tastylive.com/concepts-strategies/bull-put-spread) — worked OTM examples.
- [Debit Spreads](https://www.tastylive.com/concepts-strategies/debit-spreads) — credit-vs-debit table logic; "max loss … generally higher than your maximum potential profit."
- [Managing Winners](https://www.tastylive.com/concepts-strategies/managing-winners) — manage at 50%, improved win %, 21 DTE references.
- [Delta](https://www.tastylive.com/concepts-strategies/delta) — delta = probability of expiring ITM; cites [CBOE "Learning the Greeks"](https://www.cboe.com/insights/posts/learning-the-greeks-an-experts-perspective/).

Blocked / not extractable this session (recommended further reading to add direct citations):
- tastylive Probability of Profit, Standard Deviation, Bear Call Spread (anti-bot redirect).
- Options Industry Council — optionseducation.org strategy pages (JS-rendered).
- Fidelity options strategy guide; Schwab learning center (JS-rendered / generic landing returned).
