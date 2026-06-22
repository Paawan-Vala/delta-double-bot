<!-- markdownlint-disable-file -->
# Group D — Butterfly Option Strategies Research

Source base: https://www.macroption.com/
Date: 2026-06-21
Method: `fetch_webpage` for all 6 pages, plus integrated-browser `read_page` to verify body content on the stub pages (long-call-butterfly, reverse-iron-butterfly).

## Status: Complete (with an important sourcing caveat — read next section first)

---

## CRITICAL SOURCING NOTE — read before using this document

Of the 6 requested macroption pages, **only the Iron Butterfly page is a fully built-out article.** It contains Setup, Example, Cash Flow, Payoff, Maximum Loss, Maximum Profit, Break-Even Points, Greeks, and Related Strategies.

The **other 5 pages are stubs.** Each one's entire body is a single classification sentence plus a payoff-diagram image. They do **not** contain Setup, Example, max profit/loss, or break-even formulas. This was verified two ways: repeated `fetch_webpage` calls returned only the intro line, and a direct browser `read_page` of long-call-butterfly and reverse-iron-butterfly confirmed the `<main>` element holds exactly one paragraph + one image.

Exactly what each stub page states (verified, quotable macroption content):

| Page | Direction/Volatility class (macroption link) | Legs | Loss/Profit class |
|------|----------------------------------------------|------|-------------------|
| Long Call Butterfly | non-directional | three legs | limited loss and limited profit |
| Long Put Butterfly | non-directional | three legs | limited loss and limited profit |
| Iron Butterfly | non-directional | four legs | limited loss and limited profit |
| Short Call Butterfly | long volatility | three legs | limited loss and limited profit |
| Short Put Butterfly | long volatility | three legs | limited loss and limited **potential** profit |
| Reverse Iron Butterfly | long volatility | four legs | limited loss and limited profit |

Additional verified macroption content: the Iron Butterfly page's **Related Strategies** section explicitly describes three of the stubs:
- Long call butterfly = "all legs are calls"
- Long put butterfly = "all legs are puts"
- Reverse iron butterfly = "the inverse of iron butterfly (long the middle strike, short the outer strikes, long volatility)"

To keep this document useful for study while staying honest about sourcing, each stub strategy below is split into:
- **From macroption's page (verified):** only what the page actually states.
- **Standard reference (NOT on macroption's stub page):** widely-documented standard butterfly construction/formulas, clearly labelled so nothing is mis-attributed to macroption.
- **Plain-English (my own words):** the explicitly-requested summary field.

No numbers have been invented and attributed to macroption. Where a requested field is absent from the page, it is marked "Not specified on page."

---

## 1. Iron Butterfly  — FULL macroption content (verified)

URL: https://www.macroption.com/iron-butterfly/

- **Strategy name / alternates:** Iron Butterfly. (No alternate names given on page; related pages: Iron Condor, Short Straddle, Reverse Iron Butterfly.)
- **Core idea / construction (the legs):** Four legs, all same expiration and same size:
  - Short call (middle strike)
  - Short put (same middle strike)
  - Long put (lower strike)
  - Long call (higher strike)
  The short options strike is typically chosen **at the money** (closest strike to current underlying). The distance from middle strike to long call strike (the "wing width") must be **exactly equal** to the distance from middle strike to long put strike, so the position is symmetric with no directional bias.
- **Net debit or credit:** **Credit** strategy. "Cash flow from opening an iron butterfly is positive." Net premium received = (premium from short call + short put) − (premium paid for long call + long put). Because the short options are ATM, their premiums exceed the long options' premiums, so the net is positive.
- **When to use it:** When you expect the underlying to stay near the middle (ATM) strike through expiration. "The objective of an iron butterfly trade is to defend the premium received. Ideally, the underlying price stays at the short options' strike and no options are in the money at expiration." Benefits from time decay and falling implied volatility.
- **Market outlook:** Non-directional / neutral; **short volatility** (profits if price is pinned and IV falls). Delta near zero, Theta positive, Vega negative.
- **Pros:**
  - Credit received up front (positive initial cash flow).
  - Limited, fully hedged risk — losses stop growing beyond the long strikes.
  - Positive theta (gains as time passes).
  - Highest profit of the butterfly family at the exact middle strike, with a better risk-reward as wings are narrowed.
- **Cons:**
  - Maximum profit only at a single point (exactly the middle strike).
  - Profit is capped at the net premium received.
  - Negative vega (loses if implied volatility rises).
  - Negative gamma (vulnerable to large moves up to the wing limit).
  - Four legs = more commissions / execution complexity than a 3-leg butterfly.
- **Risk profile:** Limited loss **and** limited profit (both capped).
- **Maximum profit (page formula):** `Iron butterfly maximum profit = net premium received`. Reached when the underlying is exactly at the middle strike at expiration.
- **Maximum loss (page formula):** `Iron butterfly maximum loss = wing width − net premium received`. Reached at or above the long call strike, or at or below the long put strike. ("Wing width" = distance between long and short strike, equal on both sides.)
- **Break-even points (page formulas):**
  - `B/E #1 = middle strike − net premium received`
  - `B/E #2 = middle strike + net premium received`
- **Greeks (page):** Delta ≈ 0 near middle strike; Gamma negative; Theta positive (gains with time); Vega negative (loses if IV rises).
- **Important notes / variations / caveats (page):**
  - Risk-reward ratio improves as wing width shrinks, but maximum profit shrinks too.
  - An iron butterfly is essentially a **short put spread + short call spread** sharing the same middle (ATM) strike (i.e., a short straddle hedged by long outer wings).
  - Related: Reverse iron butterfly (the inverse, long volatility); Long call butterfly (all calls); Long put butterfly (all puts); Iron condor (short call strike higher than short put strike, so max profit is reached over a *range* not a single point); Short straddle (the unhedged, unlimited-loss version with higher profit potential).
  - **Page example (macroption's own numbers):** Sell 50 call @ 3.19 ($319); Sell 50 put @ 3.17 ($317); Buy 45 put @ 1.12 (page prints "$121" — appears to be a typo for $112); Buy 55 call @ 1.42 ($142). Wing width = 5.
    - Computed from those numbers (arithmetic mine, formulas macroption's): net premium received = 3.19 + 3.17 − 1.12 − 1.42 = **3.82** ($382) → max profit 3.82; max loss = 5 − 3.82 = **1.18** ($118); B/E = 50 ± 3.82 = **46.18 and 53.82**.
- **Plain-English (my own words):** You sell an at-the-money straddle (call + put at the same middle strike) to collect a fat premium, then buy a cheaper call above and a cheaper put below as "insurance" so a big move can't wipe you out. You keep the most money if the stock finishes pinned right at the middle strike; you lose (a capped amount) if it drifts to either wing. It's a bet that the stock sits still and volatility cools off.

---

## 2. Long Call Butterfly — STUB page

URL: https://www.macroption.com/long-call-butterfly/

**From macroption's page (verified):** Long call butterfly is a **non-directional** option strategy with **three legs**, and it has **limited loss and limited profit**. (That single sentence plus a payoff-diagram image is the entire body. Iron Butterfly's Related Strategies page adds that long call butterfly is the butterfly where "all legs are calls.") Setup, example, max profit/loss and break-even formulas are **not specified on page.**

**Standard reference (NOT on macroption's stub page — for study):**
- **Construction (1-2-1, all calls, net debit):** Buy 1 lower-strike call, sell 2 middle-strike calls, buy 1 higher-strike call; strikes equally spaced. Net **debit** strategy.
- **When to use:** Expect the underlying to expire at/near the middle strike; low-volatility / pinning play.
- **Market outlook:** Neutral; short volatility (wants the price to sit still).
- **Pros:** Cheap (small debit); risk limited to the debit; high reward-to-risk if it pins the middle strike; benefits from time decay near the middle.
- **Cons:** Max profit only at the exact middle strike; profit capped; three legs/commissions; loses if the underlying moves far either way (up to the capped loss).
- **Risk profile:** Limited loss and limited profit.
- **Max profit:** `(middle strike − lower strike) − net debit`, at price = middle strike.
- **Max loss:** `net debit paid` (occurs at/below lower strike or at/above upper strike).
- **Break-evens:** `lower strike + net debit` and `upper strike − net debit`.

**Plain-English (my own words):** A cheap, capped bet that the stock finishes right at the middle strike. You pay a small premium; if the stock pins the middle strike at expiry you make the most, and the worst case is just losing what you paid. Profit and loss are both limited, and big moves in either direction are what hurt you.

---

## 3. Long Put Butterfly — STUB page

URL: https://www.macroption.com/long-put-butterfly/

**From macroption's page (verified):** Long put butterfly is a **non-directional** option strategy with **three legs**, with **limited loss and limited profit**. (Single sentence + payoff image only. Iron Butterfly's Related Strategies adds that long put butterfly is the butterfly where "all legs are puts.") Setup/example/formulas **not specified on page.**

**Standard reference (NOT on macroption's stub page — for study):**
- **Construction (1-2-1, all puts, net debit):** Buy 1 higher-strike put, sell 2 middle-strike puts, buy 1 lower-strike put; equally-spaced strikes. Net **debit**. Payoff is essentially identical to the long call butterfly at the same strikes (a long butterfly can be built from all calls or all puts).
- **When to use / outlook:** Same as long call butterfly — neutral, expects pinning at the middle strike; short volatility.
- **Pros / Cons:** Same profile as long call butterfly (cheap, capped risk, peak only at middle strike, hurt by big moves).
- **Risk profile:** Limited loss and limited profit.
- **Max profit:** `(higher strike − middle strike) − net debit`, at price = middle strike.
- **Max loss:** `net debit paid` (at/above higher strike or at/below lower strike).
- **Break-evens:** `lower strike + net debit` and `upper strike − net debit`.

**Plain-English (my own words):** Same neutral "pin the middle strike" bet as a long call butterfly, but built from puts. Pay a small debit, profit most if the stock sits at the centre strike, lose only the debit if it runs away either direction. Calls vs puts is just construction preference — the payoff shape is the same.

---

## 4. Short Call Butterfly — STUB page

URL: https://www.macroption.com/short-call-butterfly/

**From macroption's page (verified):** Short call butterfly is a **long volatility** option strategy with **three legs**, with **limited loss and limited profit**. (Single sentence + payoff image only.) Setup/example/formulas **not specified on page.** Note the classification difference vs the *long* butterflies: macroption files this under **long volatility**, i.e. it profits from movement, not from pinning.

**Standard reference (NOT on macroption's stub page — for study):**
- **Construction (1-2-1, all calls, net credit):** The inverse of a long call butterfly — sell 1 lower-strike call, buy 2 middle-strike calls, sell 1 higher-strike call; equally-spaced strikes. Net **credit** strategy.
- **When to use:** When you expect a **large move** in either direction (or at least for the price to finish away from the middle strike); a long-volatility play.
- **Market outlook:** Non-directional but **long volatility** — wants a big move either way.
- **Pros:** Receives a credit; risk capped; profits if the underlying moves far from the middle strike in either direction; benefits from rising volatility.
- **Cons:** Maximum (capped) loss occurs if the price pins the middle strike; profit is also capped; three legs/commissions; time decay works against you near the middle.
- **Risk profile:** Limited loss and limited profit (mirror image of the long call butterfly).
- **Max profit:** `net credit received` (kept when price finishes at/below the lower strike or at/above the upper strike — i.e., outside the wings).
- **Max loss:** `(middle strike − lower strike) − net credit`, at price = middle strike.
- **Break-evens:** `lower strike + net credit` and `upper strike − net credit`.

**Plain-English (my own words):** The opposite of a long butterfly: you take in a credit and you *want* the stock to move — a big swing up or down lets you keep the credit. The danger zone is the middle strike; if the stock pins it at expiry you take the (capped) maximum loss. Think of it as a cheap, limited-risk bet on a breakout.

---

## 5. Short Put Butterfly — STUB page

URL: https://www.macroption.com/short-put-butterfly/

**From macroption's page (verified):** Short put butterfly is a **long volatility** option strategy with **three legs**, with **limited loss and limited potential profit** (note macroption's slightly different wording, "limited *potential* profit", on this page). Single sentence + payoff image only. Setup/example/formulas **not specified on page.**

**Standard reference (NOT on macroption's stub page — for study):**
- **Construction (1-2-1, all puts, net credit):** The inverse of a long put butterfly — sell 1 higher-strike put, buy 2 middle-strike puts, sell 1 lower-strike put; equally-spaced strikes. Net **credit**. Payoff matches the short call butterfly at the same strikes.
- **When to use / outlook:** Same as short call butterfly — expects a large move; long volatility; profits when the price finishes away from the middle strike.
- **Pros / Cons:** Same mirror-of-long-butterfly profile (credit received, capped risk, max loss at the middle strike, profits on big moves, helped by rising IV).
- **Risk profile:** Limited loss and limited profit.
- **Max profit:** `net credit received` (price finishes outside the wings).
- **Max loss:** `(higher strike − middle strike) − net credit`, at price = middle strike.
- **Break-evens:** `lower strike + net credit` and `upper strike − net credit`.

**Plain-English (my own words):** Same breakout bet as the short call butterfly, just built from puts. You collect a credit and profit if the stock makes a big move either way; you lose the most (a capped amount) if it sits at the middle strike. Calls vs puts is just construction — same payoff shape.

---

## 6. Reverse Iron Butterfly — STUB page

URL: https://www.macroption.com/reverse-iron-butterfly/

**From macroption's page (verified):** Reverse iron butterfly is a **long volatility** option strategy with **four legs**, with **limited loss and limited profit** (single sentence + payoff image). Setup/example/formulas **not specified on this page** — BUT the **Iron Butterfly page's Related Strategies section (verified macroption content)** explicitly defines it: "the inverse of iron butterfly (**long the middle strike, short the outer strikes, long volatility**)."

**Standard reference (NOT on the stub page — for study; consistent with macroption's "inverse of iron butterfly" definition):**
- **Construction (four legs, net debit):** Inverse of the iron butterfly — buy ATM call + buy ATM put at the middle strike (a long straddle), then sell a lower-strike put and sell a higher-strike call (the wings) to cap cost and risk. Equivalently: long call spread + long put spread sharing the middle strike. Net **debit** strategy (opposite of iron butterfly's credit).
- **When to use:** Expect a **large move** in either direction; long-volatility play; pay a debit up front.
- **Market outlook:** Non-directional but **long volatility** (wants a big move; gains if IV rises).
- **Pros:** Limited, defined risk (capped at the debit paid); profits from a large move either way; positive vega (gains if volatility rises); cheaper and lower-risk than a naked long straddle.
- **Cons:** Maximum loss if the price pins the middle strike at expiry; profit capped at the wings; negative theta (time decay hurts while price sits near the middle); four legs/commissions.
- **Risk profile:** Limited loss and limited profit.
- **Max profit (mirror of iron butterfly):** `wing width − net premium paid`, reached at or beyond either wing strike.
- **Max loss (mirror of iron butterfly):** `net premium paid`, at price = middle strike.
- **Break-evens (mirror of iron butterfly):** `middle strike − net premium paid` and `middle strike + net premium paid`.
- **Caveat:** These formulas are the logical mirror of the verified Iron Butterfly formulas and macroption's "inverse of iron butterfly" description; the reverse-iron-butterfly page itself does not print them.

**Plain-English (my own words):** It's the flipped iron butterfly. Instead of selling the ATM straddle for a credit, you *buy* the ATM straddle (long call + long put at the middle strike) and sell outer wings to cut the cost and cap the risk. You pay a debit and profit if the stock makes a big move in either direction; the worst case is the stock pinning the middle strike, where you lose the debit. A defined-risk way to be long volatility.

---

## Quick contrast (the distinction the requester asked for)

- **Long butterfly (call or put):** net **debit**, **neutral / short-vol**, profits when price stays near the **middle strike**, max loss = debit.
- **Short butterfly (call or put):** net **credit**, **long-vol**, profits from a **big move** away from the middle strike, max loss at the middle strike.
- **Iron butterfly:** net **credit** (call spread + put spread / short ATM straddle hedged), **neutral / short-vol**, profits near the **middle strike**, max profit = net credit, max loss = wing width − credit.
- **Reverse iron butterfly:** net **debit** (long ATM straddle hedged by sold wings), **long-vol**, profits from a **big move**, max loss = debit at the middle strike, max profit = wing width − debit.

## Clarifying questions for the user

1. Five of the six macroption pages (all except Iron Butterfly) are stub pages with no Setup/formula content. Is it acceptable that those fields are filled from clearly-labelled standard references rather than macroption, or would you prefer them left strictly as "Not specified on page"?
2. If you need macroption-sourced formulas specifically, macroption does have deeper sub-pages for some strategies (e.g., iron-butterfly-payoff, iron-butterfly-max-profit, iron-butterfly-max-loss). Want me to mine analogous sub-pages if they exist for the other butterflies?

## Recommended next research (not done this session)

- [ ] Check whether macroption has dedicated payoff/max-profit/max-loss sub-pages for the 5 stub strategies (pattern: `/{strategy}-payoff/`, `/{strategy}-max-profit/`, `/{strategy}-max-loss/`) and mine real formulas from them if they exist.
- [ ] Verify the apparent typo in the Iron Butterfly example ("Buy 45 strike put for 1.12 ($121)" — likely $112).
- [ ] If macroption-only sourcing is required for all fields, confirm with the user before relying on standard-reference formulas for the stub strategies.
