<!-- markdownlint-disable-file -->
# Group H — Synthetic Option Positions (Part 1): Research Notes

Source site: macroption.com (base = https://www.macroption.com/)
Date captured: 2026-06-21
Status: Complete (all 10 pages fetched and extracted)

These are SYNTHETIC option positions — combinations of options and/or underlying that
replicate the payoff of another position via put-call parity. The single most important
fact for each is the **put-call-parity equivalence** (what it replicates and why).

---

## Put-Call Parity Cheat Sheet (the "synthetic matrix")

Base identity (ignoring interest/dividends), at one shared strike K:

$$S + P = C + K \quad\Longleftrightarrow\quad S = C - P + K$$

Where S = underlying, C = call, P = put, K = strike. The six core single-position
synthetics (each leg at the SAME strike and expiration):

| Real position | Synthetic equivalent (same strike) |
| --- | --- |
| Long stock | long call + short put |
| Short stock | short call + long put |
| Long call | long stock + long put (protective put) |
| Short call | short stock + short put |
| Long put | short stock + long call |
| Short put | long stock + short call (covered call) |

Combos = the two stock synthetics but with a **gap between strikes** (call strike > put strike):

| Strategy | Construction |
| --- | --- |
| Long combo | long call + short put, call strike > put strike (≈ synthetic long stock with a gap) |
| Short combo | long put + short call, call strike > put strike (≈ synthetic short stock with a gap) |

Covered synthetics (macroption stub pages) — single-leg options that reproduce a covered position:

| Strategy | What it replicates | Equals (single leg) |
| --- | --- | --- |
| Synthetic covered call | covered call (long stock + short call) | short put |
| Synthetic covered put | covered put (short stock + short put) | short call |

---

## Page-by-page coverage classification

- **Full articles (7):** Synthetic Long Stock, Synthetic Short Stock, Synthetic Long Call,
  Synthetic Long Put, Synthetic Short Put, Long Combo, Short Combo.
- **Light/partial article (1):** Synthetic Short Call — has Setup + Example + Payoff
  classification, but NO explicit max-profit / break-even formulas.
- **Stub pages (2):** Synthetic Covered Call, Synthetic Covered Put — one-line
  classification + payoff diagram + equivalence only; no Setup / Example / Payoff / formula
  sections.

> IMPORTANT DATA-QUALITY FLAG (direction labels): macroption labels short-put-equivalent
> synthetics as "bearish" and short-call-equivalent synthetics as "bullish" on several of
> these pages, which is REVERSED from standard option theory (a short put is bullish; a
> short call is bearish) and is internally inconsistent with macroption's own Synthetic
> Short Call page. Affected pages: Synthetic Short Put, Synthetic Covered Call, Synthetic
> Covered Put. Each affected section below reports macroption's stated label AND flags the
> standard interpretation.

---

## 1. Synthetic Long Stock

- **Strategy name / alternates:** Synthetic Long Stock (also just "synthetic stock"; the
  same legs with a strike gap = Long Combo).
- **Core idea / construction:** Buy a call + sell a put at the **same strike and same
  expiration**. Replicates owning the underlying (long stock). Put-call parity:
  **long stock = long call + short put** (same strike). As long as strikes are equal, the
  payoff is an upward-sloping straight line identical to long stock.
  - macroption example: buy 70-strike call for $3.95, sell 70-strike put for $3.52.
- **When to use:** Get long exposure with little/no upfront capital (often near-zero cost,
  sometimes a small credit) instead of paying full share price; capital efficiency; express
  a bullish view; put-call-parity / arbitrage construction.
- **Market outlook:** Bullish (matches long stock).
- **Pros:**
  - Very small initial cash outlay vs. buying shares outright (ATM ≈ near zero; can be a
    small credit if put richer than call).
  - Exact linear long-stock payoff (no time-decay drag once strikes match).
  - Capital efficient; flexible strike choice changes only cash flow, not payoff.
- **Cons:**
  - No dividends — synthetic holder does NOT receive dividends, so realized payoff is worse
    than real long stock by the dividend amount when the stock pays dividends.
  - Carries the same large downside as long stock (loss if underlying falls hard).
  - Short-put leg implies margin requirements / assignment risk.
- **Risk profile:** Mirrors long stock — unlimited upside, limited (but potentially very
  large) downside down to zero underlying.
- **Maximum profit:** Unlimited as underlying rises. *(Standard reference — not stated as a
  formula on the macroption page.)*
- **Maximum loss:** Effective entry price falling to zero ≈ strike + net debit (or − net
  credit) per share. *(Standard reference — not stated on page.)*
- **Break-even:** Effective purchase price = strike + (call premium − put premium) = strike
  + net debit per share. *(Standard reference — not stated on page.)*
- **Important notes / parity:** Equivalence **long stock = long call + short put** at equal
  strikes. Initial cash flow (per macroption) = put premium − call premium (≈ 0 at ATM).
  Example net debit 3.52 − 3.95 = −$0.43/share = $43/contract. If the strikes are NOT equal
  it becomes a Long Combo.
- **Plain English:** Buying a call and selling a put at the same strike behaves exactly like
  owning the stock, but ties up almost no cash up front. You get the full up-and-down stock
  P/L without actually holding shares — the trade-off is you miss out on dividends and still
  shoulder the stock's full downside.

---

## 2. Synthetic Short Stock

- **Strategy name / alternates:** Synthetic Short Stock (the inverse of synthetic long
  stock; same legs with a strike gap = Short Combo).
- **Core idea / construction:** Sell a call + buy a put at the **same strike and same
  expiration**. Replicates a short position in the underlying. Put-call parity:
  **short stock = short call + long put** (same strike). Payoff is a downward-sloping
  straight line identical to short stock.
  - macroption example: sell 65-strike call for $3.58, buy 65-strike put for $3.34.
- **When to use:** Get short exposure when direct short-selling is restricted/expensive,
  with little upfront capital; capital efficiency; bearish view; arbitrage construction.
- **Market outlook:** Bearish (matches short stock).
- **Pros:**
  - Replicates short stock without the full short-sale cash mechanics; tiny initial cash
    flow at ATM (≈ 0).
  - Exact linear short-stock payoff.
  - A way to get short exposure where shorting shares is hard or banned.
- **Cons:**
  - Unlimited loss if the underlying rises (same as short stock).
  - Short-call leg ⇒ margin and assignment risk.
  - No short-rebate / behaves differently on dividends and borrow vs. a true short.
- **Risk profile:** Mirrors short stock — limited profit (max when underlying → 0),
  unlimited loss as underlying rises.
- **Maximum profit:** Reached when underlying falls to zero ≈ strike ± net cash flow per
  share. *(macroption states max profit occurs at zero underlying; exact formula is standard
  reference.)*
- **Maximum loss:** Unlimited (underlying can rise without bound).
- **Break-even:** ≈ strike + net credit per share (strike adjusted by call premium − put
  premium). *(Standard reference — not stated on page.)*
- **Important notes / parity:** Equivalence **short stock = short call + long put** at equal
  strikes. Strikes MUST be equal (unequal ⇒ Short Combo). Initial cash flow (per macroption)
  = call premium − put premium (≈ 0 at ATM). Usually set up ATM; strike choice changes only
  cash flow, not payoff.
- **Plain English:** Selling a call and buying a put at the same strike mimics shorting the
  stock, but without borrowing shares. You profit as the price drops and lose as it rises —
  with theoretically unlimited risk on the upside, just like a real short.

---

## 3. Synthetic Long Call

- **Strategy name / alternates:** Synthetic Long Call ("synthetic call"). Functionally a
  **protective put**.
- **Core idea / construction:** Buy the underlying + buy a put (put strike = the strike of
  the call being replicated). Replicates a long call. Put-call parity:
  **long call = long stock + long put**. Payoff looks exactly like a long call at the put's
  strike: constant limited loss below the strike, unlimited profit above.
  - macroption example: buy 100 shares for $76.04, buy 80-strike put for $6.45 → replicates
    an 80-strike long call. (Match sizes: 100 shares per 1 put contract.)
- **When to use:** When you already own (or want to own) the stock but want downside
  protection; to convert a stock holding into a capped-risk bullish position; parity
  construction. Note: requires full stock purchase, so it is NOT a low-capital play.
- **Market outlook:** Bullish.
- **Pros:**
  - Same payoff as a long call: limited loss, unlimited upside.
  - You hold the actual shares, so you DO collect dividends (unlike a plain call).
  - Useful adjustment/insurance on an existing long-stock position.
- **Cons:**
  - High initial cash outlay = underlying price + put premium (example $82.49/share =
    $8,249/contract), far more than a plain long call costs.
  - Dividend "advantage" is usually already priced into relatively more expensive puts, so
    it is not a free lunch.
  - Put premium is a recurring cost if rolled.
- **Risk profile:** Limited loss, unlimited profit (mirrors long call).
- **Maximum profit:** Unlimited as underlying rises. *(Standard reference — not stated as a
  formula on page; page states "theoretically unlimited potential profit".)*
- **Maximum loss:** Limited = (stock purchase price − strike) + put premium per share (the
  constant loss region below the strike). *(Standard reference — not stated as a formula.)*
- **Break-even:** ≈ stock purchase price + put premium (when bought near the strike).
  *(Standard reference — not stated on page.)*
- **Important notes / parity:** Equivalence **long call = long stock + long put** (protective
  put). Payoff identical to a plain long call at the put strike; only the cash-flow TIMING
  differs (synthetic ties up far more cash up front, fully compensated at expiration).
- **Plain English:** Owning the stock and buying a put on it behaves just like holding a
  call: your downside is capped at the put strike while your upside stays open. The catch is
  you pay full price for the shares up front, though you do get any dividends along the way.

---

## 4. Synthetic Long Put

- **Strategy name / alternates:** Synthetic Long Put ("synthetic put").
- **Core idea / construction:** Sell short the underlying + buy a call (call strike = strike
  of the put being replicated). Replicates a long put. Put-call parity:
  **long put = short stock + long call**. Payoff identical to a plain long put: small
  constant loss at/above strike, profit grows as underlying falls, max profit at zero.
  - macroption example: short 100 shares at $66.12, buy 65-strike call for $4.09 →
    replicates a 65-strike long put. (Match sizes: short 100 shares per 1 call contract.)
- **When to use:** Bearish protection / speculation when you are (or want to be) short the
  stock but want capped upside risk; convert a short-stock position into capped-risk bearish
  exposure; parity construction.
- **Market outlook:** Bearish.
- **Pros:**
  - Same payoff as a long put: capped loss, large profit if underlying falls.
  - Positive initial cash flow = underlying price − call premium (cash received up front
    from the short sale exceeds the call cost).
  - Useful as an adjustment on an existing short-stock position.
- **Cons:**
  - Inherits ALL short-selling burdens: margin requirements, short-sale restrictions in
    stressed markets, and the liability to pay dividends on the borrowed shares.
  - Needs significant cash at expiration to buy back the short shares.
  - Borrow availability/cost risk.
- **Risk profile:** macroption classifies it as "limited loss and limited profit" (loss
  capped at/above strike; profit bounded because underlying can only fall to zero, though it
  can still be very large). Mirrors long put.
- **Maximum profit:** Reached at zero underlying ≈ strike − net cost per share. *(macroption
  states max profit is at zero underlying; exact formula is standard reference.)*
- **Maximum loss:** Limited = constant loss at/above the strike ≈ (call strike − short-sale
  price) + call premium per share. *(Standard reference — not stated as a formula on page.)*
- **Break-even:** ≈ short-sale price − call premium (strike adjusted by premium). *(Standard
  reference — not stated on page.)*
- **Important notes / parity:** Equivalence **long put = short stock + long call**. Same
  expiration payoff as a plain long put, but different cash flow and full short-selling
  regulatory exposure.
- **Plain English:** Shorting the stock and buying a call on it reproduces a long put: you
  profit as the price drops, and the call caps your loss if the price rises instead. Because
  there is a real short underneath, you owe any dividends and face all the usual short-sale
  rules and margin.

---

## 5. Synthetic Short Call

- **Strategy name / alternates:** Synthetic Short Call (inverse / other side of synthetic
  long call).
- **Core idea / construction:** Sell short the underlying + sell a put (put strike = strike
  of the call being replicated). Replicates a short call. Put-call parity:
  **short call = short stock + short put**. Risk profile identical to a classic short call:
  constant profit below the strike, profit erodes then turns to loss above the strike.
  - macroption example: stock at $59.06; short 100 shares, sell 60-strike put →
    replicates a short 60-strike call. (Match sizes: short 100 shares per 1 put contract.)
- **When to use:** Bearish/neutral income view; construct short-call exposure via parity;
  adjust an existing short-stock position.
- **Market outlook:** Bearish (matches short call) — stated correctly on this page.
- **Pros:**
  - Reproduces the short-call payoff using stock + a short put.
  - Collects put premium; constant gain region while underlying stays below the strike.
- **Cons:**
  - **Unlimited loss** as the underlying rises (same as a naked short call).
  - Short stock leg ⇒ short-sale restrictions, margin, dividend liability.
  - Assignment risk on the short put.
- **Risk profile:** Unlimited risk, limited profit (mirrors short call) — stated explicitly
  by macroption ("Maximum loss is unlimited").
- **Maximum profit:** Limited — constant profit when underlying ends below the put strike
  (≈ net premium/credit received). *(Standard reference — exact formula not stated on page.)*
- **Maximum loss:** Unlimited (underlying prices can rise without bound) — stated on page.
- **Break-even:** ≈ short-sale price + net credit per share. *(Standard reference — not
  stated on page.)*
- **Important notes / parity:** Equivalence **short call = short stock + short put**.
  This page is a LIGHT/partial article: it gives setup, example and payoff classification but
  no explicit max-profit / break-even formulas.
- **Plain English:** Shorting the stock and selling a put together behave like selling a
  call: you keep the premium while the stock stays low, but you face unlimited losses if it
  rallies. It is the mirror image of the synthetic long call.

---

## 6. Synthetic Short Put

- **Strategy name / alternates:** Synthetic Short Put (inverse / other side of synthetic
  long put). Construction is effectively a **covered call**.
- **Core idea / construction:** Buy (long) the underlying + sell a call (call strike =
  strike of the put being replicated). Replicates a short put. Put-call parity:
  **short put = long stock + short call** (= covered call). Payoff identical to a classic
  short put: profit rises with the underlying up to the strike, then flat (short call caps
  gains).
  - macroption example: stock at $81.37; buy 100 shares at $81.37, sell 80-strike call for
    $5.03 → replicates a short 80-strike put.
- **When to use:** Income / mildly directional view; build short-put exposure when you also
  want to hold the shares (covered-call framing); parity construction.
- **Market outlook:** macroption labels it **"bearish."** ⚠️ FLAG: standard option theory
  treats a short put (and the covered call it equals) as **bullish-to-neutral**; macroption's
  own Synthetic Short Call page (also a short-stock-based bearish strategy) shows the label
  here is inconsistent. Treat macroption's "bearish" as a likely site error.
- **Pros:**
  - Reproduces short-put payoff; you hold actual shares (collect dividends, covered-call
    style).
  - Short call brings in premium and defines the capped upside.
- **Cons:**
  - Large initial cash outlay = stock price − call premium (must buy the shares).
  - Losses can be very large on a big downside move (down to the stock going to zero).
  - Capped profit (short call limits upside).
- **Risk profile:** Limited profit and limited (but potentially very large) risk — mirrors
  short put. Stated by macroption as "limited profit potential and limited risk."
- **Maximum profit:** Limited — reached at/above the call strike (≈ strike − initial cost
  per share, i.e., the premium-equivalent). *(Implied by page; macroption states profit stops
  growing at the strike.)*
- **Maximum loss:** = initial cost (occurs at zero underlying). **macroption: "Maximum loss
  = initial cost."** (initial cost = stock price paid − call premium received).
- **Break-even:** = initial cost per share. **macroption: "Synthetic short put break-even =
  initial cost."**
- **Important notes / parity:** Equivalence **short put = long stock + short call = covered
  call**. This is the same economic position as macroption's "Synthetic Covered Call" (both
  equal a short put). Cash flow differs from a classic short put, which is a pure credit
  trade; the synthetic requires buying the stock.
- **Plain English:** Buying the stock and selling a call against it produces the same payoff
  as selling a put: you earn the premium and gains up to the strike, but take the full
  downside if the stock falls. It is literally a covered call wearing a "short put" label.

---

## 7. Long Combo

- **Strategy name / alternates:** Long Combo (sometimes "long combination"). Some sources use
  "long combo" loosely for ANY long call + short put (which would include synthetic long
  stock).
- **Core idea / construction:** Buy a call + sell a put with **the call strike HIGHER than
  the put strike**, same expiration. It is synthetic long stock with a **gap between
  strikes**. Between the strikes both options are typically OTM and expire worthless, so P/L
  is flat there; above the call strike it acts like a long call (unlimited), below the put
  strike like a short put (loss grows).
  - macroption example: stock $65.39; buy 70 call for $1.77, sell 65 put for $3.28 → net
    credit $1.51/share ($151/contract).
- **When to use:** Bullish, low/zero-cost directional bet with a "dead zone" between strikes;
  capital-efficient alternative to long stock when you accept the flat mid-range; parity-based
  construction.
- **Market outlook:** Bullish.
- **Pros:**
  - Often entered for a net credit (when the put is richer than the call).
  - Unlimited upside above the call strike.
  - Cheaper/flatter-risk variant of synthetic long stock; gap removes some mid-range P/L
    swing.
- **Cons:**
  - Large downside below the put strike (loss grows to a big number toward zero underlying).
  - Flat "no progress" zone between strikes — no gain even if the stock drifts up within the
    gap.
  - Short-put leg ⇒ margin / assignment risk; no dividends.
- **Risk profile:** Unlimited potential profit, limited (but very large) loss — mirrors long
  stock/synthetic long stock.
- **Maximum profit:** Theoretically infinite (behaves like a long call above the call
  strike). *(macroption states "grows to theoretically infinite.")*
- **Maximum loss:** Occurs at zero underlying. **macroption: Long combo max loss = put strike
  − initial cash flow = put strike + call premium paid − put premium received.** Example:
  65 + 1.77 − 3.28 = $63.49/share ($6,349/contract).
- **Break-even (depends on initial cash flow; never between strikes):**
  - If call costs more than put (negative initial cash flow): **B/E = call strike − initial
    cash flow = call strike + net initial cost** (above the call strike).
  - If put costs more than call (positive initial cash flow): **B/E = put strike − initial
    cash flow** (below the put strike). Example: 65 − 1.51 = 63.49 (equals max loss in this
    case, since loss grows dollar-for-dollar below B/E down to zero).
- **Important notes / parity:** Long combo = long call + short put with call strike > put
  strike = **synthetic long stock with a strike gap**. Initial cash flow = put premium
  received − call premium paid.
- **Plain English:** A long combo is a bullish bet built from a higher-strike long call and a
  lower-strike short put, often costing little or nothing to put on. You make money above the
  call strike and lose money below the put strike, with a flat stretch in between where
  nothing changes.

---

## 8. Short Combo

- **Strategy name / alternates:** Short Combo (or "short combination"); the inverse of long
  combo. Some sources use it loosely for any long put + short call.
- **Core idea / construction:** Buy a put + sell a call with **the call strike HIGHER than
  the put strike**, same expiration. It is synthetic short stock with a **gap between
  strikes**. Between strikes both options are OTM ⇒ P/L flat (= initial cash flow); above the
  call strike losses grow (short call), below the put strike profit grows (long put).
  - macroption example: stock $83.15; buy 80 put for $2.97, sell 85 call for $3.63 → net
    credit $0.66/share ($66/contract).
- **When to use:** Bearish, low/zero-cost directional bet with a flat mid-range; capital-
  efficient alternative to shorting stock; parity-based construction.
- **Market outlook:** Bearish.
- **Pros:**
  - Can be entered for a net credit (when the call is richer than the put).
  - Large profit as the underlying falls (profit max at zero underlying).
  - Mirror of long combo; gap dampens mid-range P/L.
- **Cons:**
  - **Unlimited loss** above the call strike (losses grow dollar-for-dollar with rising
    underlying).
  - Flat zone between strikes — no gain if the stock drifts down within the gap.
  - Short-call leg ⇒ margin / assignment / short-side burdens.
- **Risk profile:** Unlimited loss, limited (but very large) profit — mirrors short
  stock/synthetic short stock.
- **Maximum profit:** Reached at zero underlying. **macroption: Short combo max profit = put
  strike + initial cash flow = put strike + call premium received − put premium paid.**
  Example: 80 + 3.63 − 2.97 = $80.66/share ($8,066/contract).
- **Maximum loss:** Theoretically unlimited (above the call strike).
- **Break-even (depends on initial cash flow; never between strikes):**
  - If initial cash flow positive (example): **B/E = call strike + initial cash flow**
    (above the call strike). Example: 85 + 0.66 = 85.66.
  - If initial cash flow negative: **B/E = put strike − net initial cost** (below the put
    strike).
- **Important notes / parity:** Short combo = long put + short call with call strike > put
  strike = **synthetic short stock with a strike gap**. Initial cash flow = call premium
  received − put premium paid (exact inverse of long combo).
- **Plain English:** A short combo is a bearish bet from a lower-strike long put and a
  higher-strike short call, often set up for a small credit. You profit as the stock falls
  and face unlimited losses if it rallies above the call strike, with a flat band between the
  two strikes.

---

## 9. Synthetic Covered Call  (STUB PAGE)

- **Strategy name / alternates:** Synthetic Covered Call.
- **Core idea / construction:** Replicates a **covered call** (long stock + short call) using
  a single **short put** option. Put-call parity: **covered call = short put**. Setup and
  risk profile are stated by macroption to be **identical to the short put strategy** (single
  leg).
- **When to use:** When you want covered-call economics in one leg (a short put) rather than
  buying stock and selling a call; capital/operationally simpler way to express the same
  payoff; parity construction.
- **Market outlook:** macroption labels it **"bearish."** ⚠️ FLAG: a covered call / short put
  is **bullish-to-neutral** in standard option theory. macroption's direction label here
  appears to be an error (and is inconsistent with its own short-call page). Risk-profile
  label ("limited risk and limited profit") is correct for a short put.
- **Pros (standard reference — not enumerated on the stub page):**
  - Single leg ⇒ simpler, lower transaction friction than long stock + short call.
  - Collects premium up front (pure credit), unlike the cash-heavy stock-based version.
- **Cons (standard reference — not enumerated on the stub page):**
  - Large downside if the underlying falls (loss down to strike → 0).
  - Capped profit (limited to premium received).
  - No dividends (no actual shares held), unlike a real covered call.
- **Risk profile:** Single leg, limited risk and limited profit — identical to a short put
  (stated by macroption).
- **Maximum profit:** = net premium received from the short put (occurs at/above the strike).
  *(Standard reference — short put payoff; NOT stated on the macroption stub page.)*
- **Maximum loss:** = strike − premium received per share (at zero underlying). *(Standard
  reference — NOT stated on the macroption stub page.)*
- **Break-even:** = strike − premium received per share. *(Standard reference — NOT stated on
  the macroption stub page.)*
- **Important notes / parity:** Equivalence **synthetic covered call = short put** (because
  covered call = long stock + short call = short put). Economically the same as macroption's
  "Synthetic Short Put." Page is a stub: only the one-line classification, the payoff diagram,
  and the equivalence are given; no setup/example/formula sections.
- **Plain English:** Instead of buying shares and writing a call against them (a covered
  call), you can just sell a put — the payoff is identical. You pocket the premium and are
  willing to be "assigned" stock if it drops, which is exactly the risk a covered call
  carries.

---

## 10. Synthetic Covered Put  (STUB PAGE)

- **Strategy name / alternates:** Synthetic Covered Put.
- **Core idea / construction:** Replicates a **covered put** (short stock + short put) using a
  single **short call** option. Put-call parity: **covered put = short call**. Setup and risk
  profile are stated by macroption to be **identical to the short call strategy** (single
  leg).
- **When to use:** When you want covered-put economics in one leg (a short call) rather than
  shorting stock and selling a put; simpler way to express the same bearish-income payoff;
  parity construction.
- **Market outlook:** macroption labels it **"bullish."** ⚠️ FLAG: a covered put / short call
  is **bearish-to-neutral** in standard option theory. macroption's direction label here
  appears to be an error (and is inconsistent with its own Synthetic Short Call page, which it
  correctly calls bearish). Risk-profile label ("unlimited risk and limited profit") is
  correct for a short call.
- **Pros (standard reference — not enumerated on the stub page):**
  - Single leg ⇒ simpler than short stock + short put.
  - Collects premium up front.
- **Cons (standard reference — not enumerated on the stub page):**
  - **Unlimited loss** if the underlying rises (naked short call).
  - Capped profit (limited to premium received).
  - Assignment / margin risk.
- **Risk profile:** Single leg, unlimited risk and limited profit — identical to a short call
  (stated by macroption).
- **Maximum profit:** = net premium received from the short call (occurs at/below the strike).
  *(Standard reference — short call payoff; NOT stated on the macroption stub page.)*
- **Maximum loss:** Unlimited (underlying can rise without bound). *(Standard reference —
  consistent with macroption's "unlimited risk" label; exact formula NOT on the stub page.)*
- **Break-even:** = strike + premium received per share. *(Standard reference — NOT stated on
  the macroption stub page.)*
- **Important notes / parity:** Equivalence **synthetic covered put = short call** (because
  covered put = short stock + short put = short call). Economically the same as a plain short
  call. Page is a stub: only the one-line classification, the payoff diagram, and the
  equivalence are given; no setup/example/formula sections.
- **Plain English:** Rather than shorting shares and writing a put (a covered put), you can
  simply sell a call — the payoff is the same. You keep the premium if the stock stays down,
  but carry unlimited risk if it rallies, just like any naked short call.

---

## Fields that could not be sourced directly from macroption (gaps)

- **Max profit / max loss / break-even formulas** were NOT explicitly stated on the page for:
  Synthetic Long Stock, Synthetic Short Stock, Synthetic Long Call, Synthetic Long Put,
  Synthetic Short Call, Synthetic Covered Call (stub), Synthetic Covered Put (stub). These
  were filled using the standard payoff of the replicated position and are clearly labeled
  "standard reference (not stated on macroption page)."
- **Pros / Cons bullet lists:** macroption does not present formal pros/cons lists; the
  bullets above are synthesized from the page's cash-flow, dividend, risk and short-selling
  notes (full/light pages) or from the replicated position's standard payoff (stub pages).
- **Synthetic Covered Call / Synthetic Covered Put:** essentially no body content beyond the
  one-line classification + diagram + equivalence; all numeric fields are standard reference.
- **Alternate names:** macroption gives few explicit aliases (only "synthetic stock",
  "long/short combination"); other common-industry aliases were not asserted to avoid
  attributing invented names to the source.

## Data-quality flags to confirm with the user

1. macroption's **direction labels are reversed vs. standard theory** on Synthetic Short Put
   (bearish), Synthetic Covered Call (bearish), and Synthetic Covered Put (bullish). Standard:
   short put = bullish, short call = bearish. Confirm whether the study notes should keep
   macroption's labels (as captured), use the standard labels, or show both. (Document
   currently shows macroption's label + a standard-theory flag.)
2. Synthetic Long Call page contains an internal example inconsistency in macroption's own
   text (it references a "45-strike call" in the payoff description while the worked example
   uses an 80-strike put/call). Captured the example as the 80-strike case; flagging in case
   verbatim fidelity matters.
