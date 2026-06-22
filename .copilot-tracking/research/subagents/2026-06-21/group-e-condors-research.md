<!-- markdownlint-disable-file -->
# Group E — Condor Option Strategies Research

**Date:** 2026-06-21
**Source site:** https://www.macroption.com/
**Researcher status:** Complete
**Pages researched:** 6 (1 full article, 5 stub pages)

## Research Scope / Questions

Extract structured study notes for six condor-family option strategies from macroption.com. For each: name + alternate names, core construction (4 strikes, legs bought/sold, debit/credit), when to use, market outlook, pros, cons, risk profile, max profit, max loss, break-even point(s), notes/variations/caveats, and a plain-English explanation.

## Page Status Summary (stub vs full article)

| # | Strategy | URL | Page type | macroption-stated content |
|---|----------|-----|-----------|---------------------------|
| 1 | Long Call Condor | /long-call-condor/ | **Stub** | "non-directional, four legs, limited loss and limited profit" + payoff diagram |
| 2 | Long Put Condor | /long-put-condor/ | **Stub** | "non-directional, four legs, limited loss and limited profit" + payoff diagram |
| 3 | Iron Condor | /iron-condor/ | **Full article** | Setup, Example, Cash Flow, Payoff, all formulas, Greeks, Related Strategies |
| 4 | Short Call Condor | /short-call-condor/ | **Stub** | "long volatility, four legs, limited loss and limited profit" + payoff diagram |
| 5 | Short Put Condor | /short-put-condor/ | **Stub** | "long volatility, four legs, limited loss and limited profit" + payoff diagram |
| 6 | Reverse Iron Condor | /reverse-iron-condor/ | **Stub** | "long volatility, four legs, limited loss and limited profit" + payoff diagram |

**Attribution rule used in this document:** Facts taken directly from a macroption page are marked **(stated on macroption page)**. Standard condor payoff math used to fill gaps on stub pages is marked **(standard reference formula — NOT stated on macroption page)**. No invented numbers are attributed to macroption.

## Strike Notation Used Below

All condors use four strikes, lowest to highest: **K1 < K2 < K3 < K4**, with equal-width "wings" so that `K2 − K1 = K4 − K3` (this equal distance is the **wing width**). K1 and K4 are the **outer** strikes; K2 and K3 are the **inner** strikes. The underlying is normally centered between the two inner strikes (K2 and K3) at entry.

- **Long condors** (long call condor, long put condor) → **net debit**, peak profit when price stays **between** K2 and K3 (neutral).
- **Short condors / reverse iron condor** → **net credit (call/put condor) or net debit (reverse iron condor)**, profit when price moves **outside** K1 or K4 (long volatility).

---

## 1. Long Call Condor

> **Page type:** STUB. The only content macroption states is the single classification line below plus a payoff-diagram image. All construction details and formulas below are standard reference knowledge, not from the macroption page.

- **Strategy name / alternate names:** Long Call Condor. Alternate names (general knowledge, not on page): "Long Condor (calls)", "Call Condor". 
- **Core idea / how it works (standard reference — NOT stated on macroption page):** Four legs, all **call** options, same expiration, equal contract count:
  - Buy 1 call at **K1** (lowest strike)
  - Sell 1 call at **K2**
  - Sell 1 call at **K3**
  - Buy 1 call at **K4** (highest strike)
  - Established for a **net debit** (the two long outer calls cost more than the credit from the two short inner calls net out to a small payment). Equivalent to a long lower call vertical spread + short upper call vertical spread.
- **When to use it:** When you expect the underlying to stay **range-bound between the inner strikes (K2–K3)** through expiration; a low-cost, defined-risk way to express a neutral view with a wide profit zone.
- **Market outlook:** **Neutral / non-directional** *(macroption states: "non-directional")*. Effectively a short-volatility, range-bound view.
- **Pros (general knowledge):**
  - Limited, fully defined risk *(macroption states: "limited loss")*.
  - Cheaper than a single long straddle/strangle to fade volatility; wide flat profit zone between inner strikes.
  - Benefits from time decay (theta) while price sits inside the inner strikes.
- **Cons (general knowledge):**
  - Limited, capped profit *(macroption states: "limited profit")*.
  - Four legs → higher commissions and bid/ask slippage.
  - Profit zone is narrow relative to a butterfly only marginally; large moves lose the full debit.
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (standard reference formula — NOT stated on macroption page):** `Max profit = wing width − net debit = (K2 − K1) − net debit`, achieved when price finishes **between K2 and K3**.
- **Maximum loss (standard reference formula — NOT stated on macroption page):** `Max loss = net debit paid`, occurs when price finishes **below K1 or above K4**.
- **Break-even points (standard reference formula — NOT stated on macroption page):** Two break-evens:
  - Lower B/E = `K1 + net debit`
  - Upper B/E = `K4 − net debit`
- **Important notes / caveats:** Has the **same payoff shape as the long put condor** and the **iron condor** (peak between inner strikes); they differ only in the option types used and debit-vs-credit construction. Equal wing widths keep the profile symmetric (no directional bias).
- **Plain-English explanation:** A long call condor is a bet, built only with call options, that the stock will drift sideways and finish between the two middle strikes. You pay a small net premium up front; if the stock stays in that middle zone you collect the maximum, and if it runs far in either direction you only lose what you paid. It is a defined-risk, defined-reward way to profit from a quiet, range-bound market.

---

## 2. Long Put Condor

> **Page type:** STUB. The only content macroption states is the single classification line below plus a payoff-diagram image. All construction details and formulas below are standard reference knowledge, not from the macroption page.

- **Strategy name / alternate names:** Long Put Condor. Alternate names (general knowledge, not on page): "Long Condor (puts)", "Put Condor".
- **Core idea / how it works (standard reference — NOT stated on macroption page):** Four legs, all **put** options, same expiration, equal contract count:
  - Buy 1 put at **K4** (highest strike)
  - Sell 1 put at **K3**
  - Sell 1 put at **K2**
  - Buy 1 put at **K1** (lowest strike)
  - Established for a **net debit**. Equivalent to a long upper put vertical spread + short lower put vertical spread.
- **When to use it:** When you expect the underlying to remain **range-bound between the inner strikes (K2–K3)** until expiration and want a defined-risk neutral position using puts.
- **Market outlook:** **Neutral / non-directional** *(macroption states: "non-directional")*. Short-volatility, range-bound view.
- **Pros (general knowledge):**
  - Limited, fully defined risk *(macroption states: "limited loss")*.
  - Wide flat profit zone between the inner strikes; benefits from time decay while price stays inside.
  - Same economics as the long call condor — choice of puts vs calls is mostly about pricing/liquidity of the specific strikes.
- **Cons (general knowledge):**
  - Limited, capped profit *(macroption states: "limited profit")*.
  - Four legs → more commissions and slippage.
  - Full debit is lost if the underlying moves beyond either outer strike.
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (standard reference formula — NOT stated on macroption page):** `Max profit = wing width − net debit = (K2 − K1) − net debit`, achieved when price finishes **between K2 and K3**.
- **Maximum loss (standard reference formula — NOT stated on macroption page):** `Max loss = net debit paid`, occurs when price finishes **below K1 or above K4**.
- **Break-even points (standard reference formula — NOT stated on macroption page):** Two break-evens:
  - Lower B/E = `K1 + net debit`
  - Upper B/E = `K4 − net debit`
- **Important notes / caveats:** Payoff is **identical in shape** to the long call condor and iron condor. Because of put-call parity, a long put condor and a long call condor with the same four strikes have effectively the same risk profile; selection depends on strike liquidity and pricing.
- **Plain-English explanation:** A long put condor is the same sideways bet as a long call condor but assembled from put options. You pay a small net premium and profit the most if the stock finishes between the two middle strikes, while your loss is capped at the premium paid if it moves far in either direction. It is a neutral, defined-risk play for a market you expect to stay quiet.

---

## 3. Iron Condor

> **Page type:** FULL ARTICLE. All formulas below are stated directly on the macroption page.

- **Strategy name / alternate names:** Iron Condor. Variation named on page: **Broken Wing Iron Condor** (unequal wing widths → directional bias). Related inverse: **Reverse Iron Condor**.
- **Core idea / how it works (stated on macroption page):** Four legs at four different strikes, lowest to highest:
  - Buy 1 **long put** at the **lowest** strike (K1, outer)
  - Sell 1 **short put** at K2 (inner)
  - Sell 1 **short call** at K3 (inner)
  - Buy 1 **long call** at the **highest** strike (K4, outer)
  - Put strikes are below the call strikes. **Short options sit at the inner strikes (the "body"); long options sit at the outer strikes (the "wings").** Underlying is chosen to be roughly halfway between the two inner strikes at entry.
  - **Wing width** = distance between the two call strikes = distance between the two put strikes; **both wings must be equal** to keep the position symmetric with no directional bias. The distance between the two inner (short) strikes can differ from the wing width.
  - All options share the same expiration and the same contract count.
  - **Cash flow: it is a CREDIT strategy** — initial cash flow is positive because the inner short options are more valuable than the outer long options. `Net premium received = (short call + short put premiums) − (long call + long put premiums)`.
- **Example (stated on macroption page):** Underlying at 52.67:
  - Buy 45 put @ 0.78 ($78)
  - Sell 50 put @ 2.21 ($221)
  - Sell 55 call @ 2.32 ($232)
  - Buy 60 call @ 1.01 ($101)
  - Net premium received = 2.32 + 2.21 − 1.01 − 0.78 = **2.74 per share ($274 per contract)**.
  - *Caveat / apparent page typo:* the page describes the call wing as "(60-65)", but the example's call strikes are 55 and 60, so the call wing width is 60 − 55 = 5, matching the put wing 50 − 45 = 5. Wing width in this example = **5**.
- **When to use it:** When you expect the underlying to **stay between the inner strikes** and want all four options to expire worthless so you keep the premium; a defined-risk income strategy for range-bound, falling-volatility conditions.
- **Market outlook:** **Neutral / non-directional** *(stated)*. **Delta-neutral** at entry when centered; **negative gamma, positive theta, negative vega** — i.e., a short-volatility view that profits from time passing and IV falling while price stays put.
- **Pros (derived from stated page content):**
  - Defined, limited risk capped by the wings *(stated: "limited loss")*.
  - Positive theta — profits from the passage of time when price stays between the inner strikes *(stated)*.
  - Credit received up front; profits if the underlying simply does nothing.
  - Risk-reward ratio improves as wing width is made smaller *(stated)*.
- **Cons (derived from stated page content):**
  - Limited, capped profit = the net premium received *(stated)*.
  - Negative vega — loses value if implied volatility rises *(stated)*.
  - Negative gamma — losses accelerate as price moves toward either inner strike *(stated)*.
  - Four legs → higher transaction costs; max loss (wing width − credit) usually exceeds max profit (credit).
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (stated on macroption page):** `Iron condor maximum profit = net premium received`. Reached between the inner strikes, where all four options expire out of the money. *(Example value derived from the formula: $274.)*
- **Maximum loss (stated on macroption page):** `Iron condor maximum loss = wing width − net premium received`. Occurs when underlying ends **at or above the long call strike (K4)** or **at or below the long put strike (K1)**. *(Example value derived: 5 − 2.74 = 2.26 → $226.)*
- **Break-even points (stated on macroption page):** Two break-evens — one between the put strikes, one between the call strikes:
  - `Iron condor B/E #1 = short put strike − net premium received` *(example derived: 50 − 2.74 = 47.26)*
  - `Iron condor B/E #2 = short call strike + net premium received` *(example derived: 55 + 2.74 = 57.74)*
  - The distance of each break-even from its short strike equals the net premium received; the distance from the long strike equals the maximum loss.
- **Important notes / variations / caveats (stated on macroption page):**
  - **Greeks:** Delta-neutral at entry (when centered); **negative gamma** (gamma turns positive near the outer long strikes where the hedge kicks in); **positive theta**; **negative vega**.
  - **Risk-reward ratio** improves with smaller wing width (smaller wings reduce both max profit and max loss).
  - **Broken wing iron condor** = modified version with unequal wing widths and an intentional directional bias.
  - **Related strategies:** Reverse iron condor (the inverse — long inner strikes, short outer strikes); iron butterfly (short call and short put at the same strike); long call condor (all calls); long put condor (all puts); short strangle (unhedged alternative without the long wings — greater potential profit but unlimited risk).
- **Plain-English explanation:** An iron condor sells an out-of-the-money put spread and an out-of-the-money call spread at the same time, collecting a net credit. You profit if the stock stays in the middle range between the two short strikes so all four options expire worthless and you keep the premium. Your risk is capped by the long "wings," and the most you can lose is the wing width minus the credit you took in. It is a popular, defined-risk income trade for calm, range-bound markets.

---

## 4. Short Call Condor

> **Page type:** STUB. The only content macroption states is the single classification line below plus a payoff-diagram image. All construction details and formulas below are standard reference knowledge, not from the macroption page.

- **Strategy name / alternate names:** Short Call Condor. Alternate name (general knowledge, not on page): the inverse of the long call condor.
- **Core idea / how it works (standard reference — NOT stated on macroption page):** Four legs, all **call** options; the exact inverse of a long call condor:
  - Sell 1 call at **K1** (lowest strike)
  - Buy 1 call at **K2**
  - Buy 1 call at **K3**
  - Sell 1 call at **K4** (highest strike)
  - Established for a **net credit**. Profits when the underlying moves **outside** the outer strikes.
- **When to use it:** When you expect a **large move** in the underlying (in either direction) and want a defined-risk, four-leg way to be long volatility; you profit if price breaks below K1 or above K4.
- **Market outlook:** **Long volatility / non-directional on direction but expecting a big move** *(macroption states: "long volatility")*. You want movement, not a specific direction.
- **Pros (general knowledge):**
  - Limited, fully defined risk *(macroption states: "limited loss")*.
  - Established for a credit; profits from a sharp move either way.
  - Cheaper / defined-risk alternative to a long straddle for a breakout view.
- **Cons (general knowledge):**
  - Limited, capped profit *(macroption states: "limited profit")*.
  - Loses if the underlying stalls between the inner strikes (the maximum-loss zone).
  - Four legs → more commissions and slippage; negative theta (time decay works against it).
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (standard reference formula — NOT stated on macroption page):** `Max profit = net credit received`, achieved when price finishes **below K1 or above K4**.
- **Maximum loss (standard reference formula — NOT stated on macroption page):** `Max loss = wing width − net credit = (K2 − K1) − net credit`, occurs when price finishes **between K2 and K3**.
- **Break-even points (standard reference formula — NOT stated on macroption page):** Two break-evens:
  - Lower B/E = `K1 + net credit`
  - Upper B/E = `K4 − net credit`
- **Important notes / caveats:** Exact mirror image of the long call condor payoff (profit and loss zones are swapped). Same payoff shape as the short put condor and the reverse iron condor — all three are "long volatility" condors that profit from large moves and lose in the middle.
- **Plain-English explanation:** A short call condor is built entirely from calls and is the opposite of a long call condor: you collect a credit and win if the stock makes a big move out of the middle range, either up or down. If the stock instead sits still between the two middle strikes, you take the maximum (still capped) loss. It is a defined-risk way to bet that a quiet market is about to break out.

---

## 5. Short Put Condor

> **Page type:** STUB. The only content macroption states is the single classification line below plus a payoff-diagram image. All construction details and formulas below are standard reference knowledge, not from the macroption page.

- **Strategy name / alternate names:** Short Put Condor. Alternate name (general knowledge, not on page): the inverse of the long put condor.
- **Core idea / how it works (standard reference — NOT stated on macroption page):** Four legs, all **put** options; the exact inverse of a long put condor:
  - Sell 1 put at **K4** (highest strike)
  - Buy 1 put at **K3**
  - Buy 1 put at **K2**
  - Sell 1 put at **K1** (lowest strike)
  - Established for a **net credit**. Profits when the underlying moves **outside** the outer strikes.
- **When to use it:** When you expect a **large move** in either direction and want a defined-risk, long-volatility position built with puts; profit comes if price breaks below K1 or above K4.
- **Market outlook:** **Long volatility** *(macroption states: "long volatility")*. Direction-agnostic; you want a big move.
- **Pros (general knowledge):**
  - Limited, fully defined risk *(macroption states: "limited loss")*.
  - Opened for a credit; profits from a sharp move in either direction.
  - Same economics as the short call condor — choose puts vs calls based on strike pricing/liquidity.
- **Cons (general knowledge):**
  - Limited, capped profit *(macroption states: "limited profit")*.
  - Maximum loss occurs if price stalls between the inner strikes.
  - Four legs → higher costs; negative theta (time decay hurts).
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (standard reference formula — NOT stated on macroption page):** `Max profit = net credit received`, achieved when price finishes **below K1 or above K4**.
- **Maximum loss (standard reference formula — NOT stated on macroption page):** `Max loss = wing width − net credit = (K2 − K1) − net credit`, occurs when price finishes **between K2 and K3**.
- **Break-even points (standard reference formula — NOT stated on macroption page):** Two break-evens:
  - Lower B/E = `K1 + net credit`
  - Upper B/E = `K4 − net credit`
- **Important notes / caveats:** Payoff shape is identical to the short call condor (mirror of the long put condor). By put-call parity, a short put condor and a short call condor at the same four strikes carry the same risk profile.
- **Plain-English explanation:** A short put condor is the put-based twin of the short call condor: you take in a credit and profit if the underlying makes a large move out of its middle range, up or down. If the stock just sits between the two middle strikes, you incur the (capped) maximum loss. It is a defined-risk, long-volatility play for an expected breakout.

---

## 6. Reverse Iron Condor

> **Page type:** STUB. The only content macroption states is the single classification line below plus a payoff-diagram image. All construction details and formulas below are standard reference knowledge, not from the macroption page (though macroption's full Iron Condor article confirms the reverse iron condor is "the inverse position, which is long the inner strikes and short the outer strikes").

- **Strategy name / alternate names:** Reverse Iron Condor. Alternate names (general knowledge, not on page): "Short Iron Condor", "Long Iron Condor" (naming varies by broker). Macroption's Iron Condor page describes it as the **inverse of the iron condor**.
- **Core idea / how it works (standard reference + cross-referenced from macroption Iron Condor page):** Four legs combining a long put spread and a long call spread; **long the inner strikes, short the outer strikes** *(this inner/outer relationship is stated on macroption's Iron Condor page)*:
  - Sell 1 **put** at **K1** (lowest, outer)
  - Buy 1 **put** at **K2** (inner)
  - Buy 1 **call** at **K3** (inner)
  - Sell 1 **call** at **K4** (highest, outer)
  - Established for a **net debit** (you buy the more valuable inner options and sell the cheaper outer options). Profits when the underlying moves **outside** the outer strikes.
- **When to use it:** When you expect a **large move / volatility expansion** in either direction (e.g., ahead of earnings or a binary event) and want a defined-risk, four-leg long-volatility position.
- **Market outlook:** **Long volatility** *(macroption states: "long volatility")*. Direction-agnostic; you want a big breakout.
- **Pros (general knowledge):**
  - Limited, fully defined risk capped at the net debit *(macroption states: "limited loss")*.
  - Profits from a sharp move in either direction; positive vega (gains if implied volatility rises).
  - Lower cost than an outright long strangle covering the same breakout view.
- **Cons (general knowledge):**
  - Limited, capped profit *(macroption states: "limited profit")*.
  - Maximum loss (the full debit) occurs if price stays between the inner strikes.
  - Negative theta — time decay works against the position; four legs raise transaction costs.
- **Risk profile:** **Limited loss and limited profit** *(stated on macroption page)*.
- **Maximum profit (standard reference formula — NOT stated on macroption page):** `Max profit = wing width − net debit = (K2 − K1) − net debit`, achieved when price finishes **below K1 or above K4**.
- **Maximum loss (standard reference formula — NOT stated on macroption page):** `Max loss = net debit paid`, occurs when price finishes **between the inner strikes K2 and K3** (all options expire worthless).
- **Break-even points (standard reference formula — NOT stated on macroption page):** Two break-evens, measured from the **inner (long) strikes** by the net debit (the mirror of the iron condor's break-even rule):
  - Lower B/E = `K2 (long put inner strike) − net debit`
  - Upper B/E = `K3 (long call inner strike) + net debit`
- **Important notes / variations / caveats:** It is the **exact inverse of the iron condor** *(stated on macroption Iron Condor page)* — where the iron condor is a delta-neutral, short-volatility credit trade, the reverse iron condor is a defined-risk, long-volatility debit trade with positive vega and negative theta. Same family/payoff shape as the short call condor and short put condor (all profit from large moves and lose in the middle).
- **Plain-English explanation:** A reverse iron condor buys a put spread and a call spread at the same time, paying a net debit, so it profits when the underlying makes a large move in either direction and finishes beyond one of the outer strikes. If the stock instead stays trapped between the two inner strikes, you lose the premium you paid — which is your maximum, fully defined loss. It is the mirror image of the iron condor and a popular defined-risk way to bet on a volatility breakout.

---

## Cross-Strategy Quick-Reference Matrix

| Strategy | Options used | Debit/Credit | Direction / vol view | Profits when price is... | Max profit | Max loss |
|----------|--------------|--------------|----------------------|--------------------------|------------|----------|
| Long Call Condor | All calls | Debit | Neutral (non-directional) | **Between** inner strikes | wing width − debit* | net debit* |
| Long Put Condor | All puts | Debit | Neutral (non-directional) | **Between** inner strikes | wing width − debit* | net debit* |
| Iron Condor | Puts + calls | **Credit** | Neutral (non-directional) | **Between** inner strikes | **net premium received** (stated) | **wing width − net premium** (stated) |
| Short Call Condor | All calls | Credit | Long volatility | **Outside** outer strikes | net credit* | wing width − credit* |
| Short Put Condor | All puts | Credit | Long volatility | **Outside** outer strikes | net credit* | wing width − credit* |
| Reverse Iron Condor | Puts + calls | Debit | Long volatility | **Outside** outer strikes | wing width − debit* | net debit* |

\* = standard reference formula (NOT stated on the corresponding macroption stub page). Iron Condor figures in bold are stated directly on macroption.

## Fields Not Found on the Pages

- **All five stub pages** (long call condor, long put condor, short call condor, short put condor, reverse iron condor): macroption provides **only** the one-line classification (legs / direction-or-volatility / "limited loss and limited profit") and a payoff-diagram image. It does **not** state construction details, examples, max profit, max loss, break-evens, pros, cons, or Greeks. Those fields here are filled with standard reference formulas and general option knowledge, clearly labeled as such.
- **Alternate names:** macroption does not list alternate names for any of the six strategies (only related-strategy cross-links). Alternate names noted above are general industry knowledge.
- **Iron Condor:** the only field with a minor data issue is the example's call-wing description, which the page prints as "(60-65)" — an apparent typo, since the example's call strikes are 55 and 60 (wing width = 5, matching the put wing). All Iron Condor formulas (max profit, max loss, both break-evens) are fully stated on the page.

## References

- [Long Call Condor — macroption](https://www.macroption.com/long-call-condor/) (stub)
- [Long Put Condor — macroption](https://www.macroption.com/long-put-condor/) (stub)
- [Iron Condor — macroption](https://www.macroption.com/iron-condor/) (full article)
- [Short Call Condor — macroption](https://www.macroption.com/short-call-condor/) (stub)
- [Short Put Condor — macroption](https://www.macroption.com/short-put-condor/) (stub)
- [Reverse Iron Condor — macroption](https://www.macroption.com/reverse-iron-condor/) (stub)
- [Iron Condor Max Loss & Max Profit Calculation — macroption](https://www.macroption.com/iron-condor-max-loss/) (linked sub-article, not separately fetched)
- [Iron Condor Payoff, Break-Even Points and R/R — macroption](https://www.macroption.com/iron-condor-payoff/) (linked sub-article, not separately fetched)
