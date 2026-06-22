<!-- markdownlint-disable-file -->
# Group B Research: Vertical Spreads & Ladders (macroption.com)

## Research Scope

Extract structured option-strategy content from macroption.com for 8 strategies:

1. Bull Call Spread — https://www.macroption.com/bull-call-spread/
2. Bull Put Spread — https://www.macroption.com/bull-put-spread/
3. Bear Call Spread — https://www.macroption.com/bear-call-spread/
4. Bear Put Spread — https://www.macroption.com/bear-put-spread/
5. Bull Call Ladder — https://www.macroption.com/bull-call-ladder/
6. Bull Put Ladder — https://www.macroption.com/bull-put-ladder/
7. Bear Call Ladder — https://www.macroption.com/bear-call-ladder/
8. Bear Put Ladder — https://www.macroption.com/bear-put-ladder/

### Fields to capture per strategy

- Strategy name (and alternate names)
- Core idea / construction (legs, strikes, net debit/credit)
- When to use
- Market outlook
- Pros
- Cons
- Risk profile (limited vs unlimited)
- Maximum profit
- Maximum loss
- Break-even point(s)
- Important notes / variations / caveats
- Short plain-English explanation

### Status: Complete — all 8 strategies captured

### Source-quality note (important)

- The **four vertical spread pages** (bull call, bull put, bear call, bear put) are full articles with text sections (Setup, Cash Flow, Payoff, When to Trade, Strike Selection). All fields below come directly from page text.
- The **four ladder pages** (bull call, bull put, bear call, bear put) are **short stub pages**. Each contains only a one-line classification sentence plus a single payoff-diagram image and site navigation. There is **no Setup / Pros / Cons / When-to-Trade text** on the ladder pages.
  - The ladder construction, max profit, max loss, and both break-even points were read from the **payoff-calculator screenshot image** embedded on each ladder page (a worked example using strikes 45 / 50 / 55, underlying 50.17). General formulas below are derived from those worked examples and labeled as such.
  - Fields with no page text (Pros, Cons, When to Use as prose) are marked "not specified on page (stub page)."

---

# Vertical Spreads (4)

## 1. Bull Call Spread

- **Strategy name / alternate names:** Bull Call Spread. Also called **long call spread** or **debit call spread**.
- **Core idea / construction:** Two calls, same expiration and underlying. **Buy** a lower-strike call and **sell** a higher-strike call. It is a **debit** strategy (net cost to open).
  - Initial cash flow = short (higher-strike) call price − long (lower-strike) call price → always **negative** (a debit), because the higher-strike call is cheaper than the lower-strike call. Selling the higher call reduces the cost of the long call but never fully pays for it.
- **When to use:** When you expect the underlying to **moderately increase**. Profit above the higher strike is capped, so if you expect a large move, a plain long call may be better.
- **Market outlook:** Bullish (directional up). Volatility exposure depends on strike placement (positive vega if both strikes above price; negative vega if both below; ~neutral if price is mid-way).
- **Pros:**
  - Limited, known risk (the net debit).
  - Cheaper than buying the call outright (the short call offsets cost).
  - Flexible risk/reward via strike selection.
- **Cons:**
  - Profit is capped above the higher strike.
  - Still a net debit (you pay to enter; time decay can work against you if both strikes are above price).
- **Risk profile:** **Limited risk, limited reward.**
- **Maximum profit:** **Strike difference − net initial cost.** Occurs when underlying ends at or above the higher strike (both calls in the money).
- **Maximum loss:** **Net initial cost** (the debit paid). Occurs when underlying ends at or below the lower strike (both calls expire worthless).
- **Break-even:** **Lower strike + long call price − short call price** (i.e., lower strike + net debit per share). Above B/E = profit, below = loss.
- **Notes / variations:** Strike selection drives Greeks. Both strikes above price = positive vega / negative theta (want a move + volatility). Both strikes below price = positive theta / negative vega (want price to sit still). Strikes straddling price with equal distance = roughly vega/theta neutral (pure directional play). Wider strikes = more cost, more risk, more profit potential.
- **Plain English:** You buy a call and sell a higher-strike call to cheapen it. You profit if the stock rises, but your gain stops once it passes the higher strike. Your most you can lose is what you paid. Good for a measured, moderately bullish view rather than a moonshot.

## 2. Bull Put Spread

- **Strategy name / alternate names:** Bull Put Spread. Also called **short put spread** or **credit put spread**. ("Short" refers to being short the more valuable higher-strike put, not to direction — direction is bullish.) It is the inverse (other side) of the bear put spread.
- **Core idea / construction:** Two puts, same expiration. **Sell** a higher-strike put and **buy** a lower-strike put (as a hedge). It is a **credit** strategy (you receive cash to open).
  - Initial cash flow = short (higher-strike) put price − long (lower-strike) put price → **positive** (a credit), because the higher-strike put sold is more expensive than the lower-strike put bought.
- **When to use:** When you expect the underlying to **moderately rise, or at least not fall** (stay flat or up). Can be built with long, short, or neutral volatility exposure via strikes. **Source caveat:** the page's "When to Trade" sentence literally reads "moderately *decrease*, or at least not rise," which contradicts the same page's own bullish framing, its break-even note ("profitable above the break-even"), and its Summary ("if you expect price to rise … choose higher strikes"). Treated here as a wording slip on the page; the bullish reading above is the correct one.
- **Market outlook:** Bullish (profits when underlying rises or holds). Volatility view set by strikes.
- **Pros:**
  - Receive premium up front (credit).
  - Limited, known risk (capped by the long put).
  - Can profit from time decay / from the underlying simply not falling (when strikes are below price).
- **Cons:**
  - Profit is capped at the premium received.
  - Max loss (strike difference − credit) is usually larger than the credit collected.
- **Risk profile:** **Limited risk, limited reward.**
- **Maximum profit:** **Net premium received** (the credit). Occurs when underlying ends at or above the higher strike (both puts expire worthless).
- **Maximum loss:** **Strike difference − net premium received.** Occurs when underlying ends at or below the lower strike.
- **Break-even:** **Higher strike − net premium received.** Profitable **above** the break-even, loses **below** it.
- **Notes / variations:** Same as other verticals — strike placement sets theta/vega. Both strikes below price (OTM) = positive theta, negative vega (you want it to sit still). Both above price (ITM) = needs a rise, positive vega/negative theta. Straddling strikes with equal distance ≈ vega/theta neutral. Wider strikes = more risk and more profit potential.
- **Plain English:** You collect cash by selling a put, and buy a cheaper lower put for protection. You keep the full credit as long as the stock stays above the higher strike. Your loss is capped, but it can be bigger than the credit if the stock drops through both strikes. A way to earn premium with a "won't fall much" view.

## 3. Bear Call Spread

- **Strategy name / alternate names:** Bear Call Spread. Also called **short call spread** or **credit call spread**. It is the inverse (other side) of the bull call spread.
- **Core idea / construction:** Two calls, same expiration. **Sell** a lower-strike call and **buy** a higher-strike call (protection against the otherwise unlimited short-call loss). It is a **credit** strategy.
  - Initial cash flow = short (lower-strike) call price − long (higher-strike) call price → **positive** (a credit), because the lower-strike call sold is more expensive than the higher-strike call bought.
- **When to use:** When you expect the underlying to **moderately decline, or at least not rise**. Like a short call, but hedged by the long higher-strike call.
- **Market outlook:** Bearish (profits when underlying falls or holds). Volatility view set by strikes.
- **Pros:**
  - Receive premium up front (credit).
  - Limited, known risk (capped by the long higher call) — unlike a naked short call.
  - Profits from time decay / the underlying simply not rising (when strikes are above price — the most common build).
- **Cons:**
  - Profit capped at the premium received.
  - Max loss (strike difference − credit) usually larger than the credit.
- **Risk profile:** **Limited risk, limited reward.**
- **Maximum profit:** **Initial cash inflow** (the credit). Occurs when underlying ends at or below both strikes (both calls expire worthless).
- **Maximum loss:** **Strike difference − initial cash inflow.** Occurs when underlying ends at or above the higher strike.
- **Break-even:** **Lower strike + short call price − long call price** (i.e., lower strike + net credit per share). Identical to the bull call spread break-even, but profitable **below** it and loses **above** it.
- **Notes / variations:** Most common build is both strikes above price (positive theta, negative vega — you profit if price just sits or drifts down). Both strikes below price = needs a move, positive vega/negative theta. Straddling strikes equal distance ≈ vega/theta neutral. Wider strikes = more risk and more profit potential.
- **Plain English:** You collect cash by selling a call and buy a higher call to cap the risk. You keep the credit as long as the stock stays below the lower strike. It's a hedged way to bet the stock won't rally. Loss is limited but can exceed the credit if the stock climbs past the higher strike.

## 4. Bear Put Spread

- **Strategy name / alternate names:** Bear Put Spread. Also called **long put spread** or **debit put spread**. ("Long" refers to being long the more valuable higher-strike put.) Inverse of the bull put spread.
- **Core idea / construction:** Two puts, same expiration. **Buy** a higher-strike put and **sell** a lower-strike put. It is a **debit** strategy (net cost to open).
  - Initial cash flow = short (lower-strike) put price − long (higher-strike) put price → **negative** (a debit), because the higher-strike put bought is more expensive than the lower-strike put sold.
- **When to use:** When you expect a **moderate decrease** in the underlying. Profit on a further fall is capped by the short lower-strike put. For a bigger expected drop, choose lower/wider strikes or just buy a put.
- **Market outlook:** Bearish (directional down). Volatility view set by strikes.
- **Pros:**
  - Limited, known risk (the net debit).
  - Cheaper than buying the put outright (the short put offsets cost).
  - Flexible risk/reward via strike selection.
- **Cons:**
  - Profit capped below the lower strike.
  - Net debit to enter; time decay can work against you when both strikes are below price.
- **Risk profile:** **Limited risk, limited reward.**
- **Maximum profit:** **Strike difference − net initial cost.** Occurs when underlying ends at or below the lower strike (both puts in the money).
- **Maximum loss:** **Net initial cost** (the debit). Occurs when underlying ends at or above the higher strike (both puts expire worthless).
- **Break-even:** **Higher strike − long put price + short put price** (i.e., higher strike − net debit per share). Below B/E = profit, above = loss.
- **Notes / variations:** Mirror of bull call spread (direction reversed). Both strikes below price = positive vega/negative theta (want a move down). Both above price = positive theta/negative vega (already ITM, want it to sit). Most popular build = long put ITM (higher strike above price), short put OTM (lower strike below price). Wider strikes = more cost, risk, and profit potential.
- **Plain English:** You buy a put and sell a lower-strike put to cheapen it. You profit as the stock falls, but your gain stops once it drops below the lower strike. The most you can lose is what you paid. Good for a measured, moderately bearish view.

---

# Ladders (4) — 3-leg extensions of vertical spreads

> macroption ladder pages are stub pages. Construction + numbers below are read from each page's payoff-calculator screenshot (worked example: strikes **45 / 50 / 55**, underlying **50.17**; call prices 6.18 / 3.19 / 1.42; put prices 1.21 / 3.17 / 6.37). "S1/S2/S3" = lowest / middle / highest strike.

## 5. Bull Call Ladder

- **Strategy name / alternate names:** Bull Call Ladder. (Page classifies it as **non-directional**, three legs.) No alternate name given on page.
- **Core idea / construction (from diagram):** Three calls, same expiration:
  - **+1 long call @ S1 (45)**, **−1 short call @ S2 (50)**, **−1 short call @ S3 (55)**.
  - = a **bull call spread (long 45 / short 50) plus one EXTRA short call @ 55** (the "ladder" rung). The extra naked short call is what creates unlimited upside risk.
  - Example net cash flow = **−157** (a small net **debit** here; can be debit or credit depending on strikes/prices).
- **When to use:** Not specified on page (stub). Practically: a refinement of a bull call spread where you sell an extra higher call to lower cost / raise max profit, when you do **not** expect a strong rally above the top strike. Page tag "non-directional."
- **Market outlook:** Page label = **non-directional** / short-volatility-leaning on the upside. You want the underlying to finish in the mid zone (between S2 and S3); a big rally hurts badly.
- **Pros:** Not specified on page. (Derived: cheaper / higher max profit than the equivalent bull call spread because of the extra premium collected from the second short call.)
- **Cons:** Not specified on page. (Derived: **unlimited loss** if the underlying rises sharply above the upper break-even.)
- **Risk profile:** **Unlimited loss, limited profit** (stated on page). Downside loss is limited; **upside loss is unlimited** due to the extra short call.
- **Maximum profit (example = 343):** Realized when underlying finishes **between S2 and S3 (50–55)**. Formula ≈ **(S2 − S1) − net debit** = (50−45)×100 − 157 = 500 − 157 = **343**.
- **Maximum loss:** **Unlimited on the upside** (labeled "Inf Loss" above the upper break-even). On the **downside** (underlying at/below S1), loss is limited to the **net debit (≈157)**.
- **Break-even points (two):**
  - **Lower B/E = 46.57** ≈ S1 + net debit per share (45 + 1.57).
  - **Upper B/E = 58.43** ≈ S3 + max-profit per share (55 + 3.43). Above this, position goes into unlimited loss.
- **Notes / caveats:** The extra short call beyond the bull call spread turns capped risk into **unlimited upside risk** — the key danger. Profit plateaus between the two upper strikes.
- **Plain English:** Take a bull call spread, then sell one more higher-strike call to collect extra premium. You make the most if the stock lands in the middle zone, but selling that extra naked call means a strong rally can cause unlimited losses. A "moderate move, definitely no breakout" trade.

## 6. Bull Put Ladder

- **Strategy name / alternate names:** Bull Put Ladder. (Page classifies it as **long volatility**, three legs.) No alternate name given.
- **Core idea / construction (from diagram):** Three puts, same expiration:
  - **+1 long put @ S1 (45)**, **+1 long put @ S2 (50)**, **−1 short put @ S3 (55)**.
  - = a **bull put spread (short 55 / long 50) plus one EXTRA long put @ 45** (the rung). The extra long put gives big downside profit potential.
  - Example net cash flow = **+199** (a net **credit** here).
- **When to use:** Not specified on page (stub). Practically: when you lean bullish/neutral (keep the credit if it rises) but want a cheap hedge that pays off big if the underlying crashes.
- **Market outlook:** Page label = **long volatility**. Profits most on a large **down** move; also keeps a small credit if it rises. Worst outcome is a mild drift down into the middle.
- **Pros:** Not specified on page. (Derived: limited risk; very large profit if the underlying falls hard; still collects a credit on the upside.)
- **Cons:** Not specified on page. (Derived: loses the most on a small/moderate decline into the S1–S2 zone; needs a real move to shine.)
- **Risk profile:** **Limited loss, limited profit** (page), **"although potential profit can be very large if underlying falls a lot."**
- **Maximum profit (example = 4,199):** Realized as the underlying **falls toward zero**. Formula ≈ **(S1 + S2 − S3) − net credit-adjusted** → (45+50−55)×100 + 199 = 4000 + 199 = **4,199**. (Bounded only because the underlying cannot go below 0.)
- **Maximum loss (example = −301):** Realized when underlying finishes **between S1 and S2 (45–50)**. Formula ≈ **(S3 − S2) − net credit** = (55−50)×100 − 199 = 500 − 199 = **301**.
- **Break-even points (two):**
  - **Lower B/E = 41.99** ≈ S1 − max-loss per share (45 − 3.01).
  - **Upper B/E = 53.01** ≈ S2 + max-loss per share (50 + 3.01). Above S3, position keeps the **net credit (+199)** = limited upside profit.
- **Notes / caveats:** Above the top strike you simply keep the credit (small win). The big payoff requires a substantial fall. It is the **inverse of the bear put ladder**.
- **Plain English:** Start with a bull put spread (collect a credit) and buy one more lower put. If the stock collapses you profit a lot; if it rises you keep a small credit; the only real pain is a modest slide into the middle. A bullish-leaning trade with a built-in crash hedge.

## 7. Bear Call Ladder

- **Strategy name / alternate names:** Bear Call Ladder. (Page classifies it as **long volatility**, three legs.) No alternate name given.
- **Core idea / construction (from diagram):** Three calls, same expiration:
  - **−1 short call @ S1 (45)**, **+1 long call @ S2 (50)**, **+1 long call @ S3 (55)**.
  - = a **bear call spread (short 45 / long 50) plus one EXTRA long call @ 55** (the rung). The extra long call gives unlimited upside profit.
  - Example net cash flow = **+157** (a net **credit** here).
- **When to use:** Not specified on page (stub). Practically: when you lean bearish/neutral (keep the credit if it falls) but want a cheap upside breakout play if the underlying rallies hard.
- **Market outlook:** Page label = **long volatility**. Profits most on a large **up** move; keeps a small credit if it falls. Worst outcome is a mild rise into the middle.
- **Pros:** Not specified on page. (Derived: limited risk; **unlimited profit** on a strong rally; still collects a credit on the downside.)
- **Cons:** Not specified on page. (Derived: loses the most on a small/moderate rise into the S2–S3 zone; needs a real move up to pay off.)
- **Risk profile:** **Limited loss, unlimited profit** (stated on page). The extra long call makes upside profit unlimited.
- **Maximum profit:** **Unlimited on the upside** (labeled "Inf Profit" above the upper break-even), thanks to the extra long call. On the **downside**, "profit" is capped at the **net credit (≈157)**.
- **Maximum loss (example = −343):** Realized when underlying finishes **between S2 and S3 (50–55)**. Formula ≈ **(S2 − S1) − net credit** = (50−45)×100 − 157 = 500 − 157 = **343**.
- **Break-even points (two):**
  - **Lower B/E = 46.57** ≈ S1 + net credit per share (45 + 1.57). Below this, position keeps the net credit (+157).
  - **Upper B/E = 58.43** ≈ S3 + max-loss per share (55 + 3.43). Above this, unlimited profit.
- **Notes / caveats:** It is the **inverse of the bull call ladder** (same strikes/prices, opposite positions, P/L sign flipped). Needs a sizable rally for the big payoff; a mild rise into the middle is the worst case.
- **Plain English:** Start with a bear call spread (collect a credit) and buy one more higher call. If the stock rockets up you profit without limit; if it falls you keep a small credit; the only real pain is a modest rise into the middle. A bearish-leaning trade with a built-in breakout hedge.

## 8. Bear Put Ladder

- **Strategy name / alternate names:** Bear Put Ladder. (Page classifies it as **non-directional**, three legs.) No alternate name given.
- **Core idea / construction (from diagram):** Three puts, same expiration:
  - **−1 short put @ S1 (45)**, **−1 short put @ S2 (50)**, **+1 long put @ S3 (55)**.
  - = a **bear put spread (long 55 / short 50) plus one EXTRA short put @ 45** (the rung). The extra naked short put creates a very large downside loss.
  - Example net cash flow = **−199** (a small net **debit** here).
- **When to use:** Not specified on page (stub). Practically: a refinement of a bear put spread where you sell an extra lower put to lower cost / raise max profit, when you do **not** expect a hard crash below the lowest strike. Page tag "non-directional."
- **Market outlook:** Page label = **non-directional**. You want the underlying to finish in the mid zone (between S1 and S2); a deep crash hurts badly.
- **Pros:** Not specified on page. (Derived: cheaper / higher max profit than the equivalent bear put spread because of the extra premium collected from the second short put.)
- **Cons:** Not specified on page. (Derived: **very large loss** if the underlying falls sharply below the lower break-even.)
- **Risk profile:** **Limited loss, limited profit** (page), **"although the loss can be very large if underlying falls a lot."** (Loss is technically bounded only because the underlying cannot fall below 0.)
- **Maximum profit (example = 301):** Realized when underlying finishes **between S1 and S2 (45–50)**. Formula ≈ **(S2 − S1) − net debit** = (50−45)×100 − 199 = 500 − 199 = **301**.
- **Maximum loss (example = −4,199):** Realized as the underlying **falls toward zero**. Formula ≈ **(S1 + S2 − S3) + net debit** = (45+50−55)×100 + 199 = 4000 + 199 = **4,199** loss. On the **upside** (above S3), loss is limited to the **net debit (−199)**.
- **Break-even points (two):**
  - **Lower B/E = 41.99** ≈ S1 − max-profit per share (45 − 3.01). Below this, losses grow rapidly toward the very large max loss.
  - **Upper B/E = 53.01** ≈ S2 + max-profit per share (50 + 3.01). Above S3, position loses only the net debit (−199).
- **Notes / caveats:** The extra short put beyond the bear put spread turns capped risk into a **very large downside loss** — the key danger. It is the **inverse of the bull put ladder**. Profit plateaus between the two lower strikes.
- **Plain English:** Take a bear put spread, then sell one more lower-strike put to collect extra premium. You make the most if the stock lands in the middle zone, but that extra naked put means a deep crash can cause huge losses. A "moderate drop, definitely no collapse" trade.

---

# Cross-Strategy Quick Reference

| Strategy | Legs (example 45/50/55) | Net CF (example) | Direction | Risk profile | Max profit (example) | Max loss (example) | Break-evens (example) |
|---|---|---|---|---|---|---|---|
| Bull Call Spread | +C(low), −C(high) | Debit | Bullish | Limited / Limited | strike diff − debit | net debit | low strike + net debit |
| Bull Put Spread | −P(high), +P(low) | Credit | Bullish | Limited / Limited | net credit | strike diff − credit | high strike − net credit |
| Bear Call Spread | −C(low), +C(high) | Credit | Bearish | Limited / Limited | net credit | strike diff − credit | low strike + net credit |
| Bear Put Spread | +P(high), −P(low) | Debit | Bearish | Limited / Limited | strike diff − debit | net debit | high strike − net debit |
| Bull Call Ladder | +C45, −C50, −C55 | −157 (debit) | Non-directional | **Unlimited loss** / Limited | 343 | **Unlimited** (upside) | 46.57 & 58.43 |
| Bull Put Ladder | +P45, +P50, −P55 | +199 (credit) | Long vol (bull lean) | Limited / Limited (large down) | 4,199 | 301 | 41.99 & 53.01 |
| Bear Call Ladder | −C45, +C50, +C55 | +157 (credit) | Long vol (bear lean) | Limited / **Unlimited profit** | **Unlimited** (upside) | 343 | 46.57 & 58.43 |
| Bear Put Ladder | −P45, −P50, +P55 | −199 (debit) | Non-directional | Limited / Limited (large down loss) | 301 | **4,199** (downside) | 41.99 & 53.01 |

**Ladder pairing:** Bull Call Ladder ↔ Bear Call Ladder are inverses (same call strikes, opposite positions). Bull Put Ladder ↔ Bear Put Ladder are inverses (same put strikes, opposite positions).

**Unlimited-risk side (per task emphasis):**

- **Bull Call Ladder** → unlimited loss if underlying **rises** sharply (extra short call).
- **Bear Put Ladder** → very large loss if underlying **falls** sharply (extra short put; bounded only by underlying ≥ 0).
- **Bear Call Ladder** → unlimited *profit* if underlying rises sharply (extra long call) — risk stays limited.
- **Bull Put Ladder** → very large *profit* if underlying falls sharply (extra long put) — risk stays limited.

---

# Outstanding / Could-Not-Find

- Ladder pages had **no prose** for: alternate names, explicit "When to Use," Pros, Cons. These were marked "not specified on page" and supplemented with clearly-labeled derivations from the worked-example payoff diagram. If the user needs sourced pros/cons/when-to-use for ladders, those would have to come from a different source (macroption does not provide them on these stub pages).
- Vertical-spread pages each link to a companion "Payoff, Break-Even and R/R" page (e.g., /bull-call-spread-payoff/) with numeric examples — not fetched here because the main pages already supplied all requested formula fields. Recommended only if numeric worked examples for the spreads are wanted.
