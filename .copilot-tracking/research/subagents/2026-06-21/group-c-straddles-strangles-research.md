# Group C — Straddles & Strangles Research (macroption.com)

Status: Complete

Source base: https://www.macroption.com/

This document captures structured study notes for 10 option strategies. Construction, max profit/loss, and break-even formulas are extracted from the actual macroption.com pages. The example numbers shown are the worked examples used on each page.

## Research Topics / Questions

- For each of the 10 strategies: name + alternate names, core idea/construction, when to use, market outlook, pros, cons, risk profile, max profit, max loss, break-even(s), important notes/variations/caveats, plain-English explanation.

## Coverage Status

| # | Strategy | URL | Status |
|---|----------|-----|--------|
| 1 | Long Straddle | /long-straddle/ | Captured |
| 2 | Short Straddle | /short-straddle/ | Captured |
| 3 | Strap | /strap/ | Captured |
| 4 | Strip | /strip/ | Captured |
| 5 | Covered Short Straddle | /covered-short-straddle/ | Captured |
| 6 | Long Strangle | /long-strangle/ | Captured |
| 7 | Short Strangle | /short-strangle/ | Captured |
| 8 | Long Guts | /long-guts/ | Captured |
| 9 | Short Guts | /short-guts/ | Captured |
| 10 | Covered Short Strangle | /covered-short-strangle/ | Captured |

Note on Pros/Cons: macroption pages do not contain literal "Pros"/"Cons" bullet lists. The Pros/Cons below are synthesized faithfully from each page's stated risk profile, payoff description, and Greeks (e.g. "main disadvantage", "worst enemy", time decay, volatility exposure). No numbers are invented.

---

## 1. Long Straddle

URL: https://www.macroption.com/long-straddle/

- **Alternate names:** none given (it is the base "straddle" bought).
- **Core idea / construction:** Buy a call and buy a put with the **same strike** and **same expiration**, equal number of contracts. Typically opened **at-the-money** (ATM). If contracts are unequal it becomes a strip (more puts) or strap (more calls).
- **When to use:** When you expect a **big move** in the underlying but are unsure of direction, and/or expect implied volatility to rise.
- **Market outlook:** Long volatility, **non-directional** (no directional bias when ATM, initial delta near zero).
- **Pros:**
  - Profits from a large move in **either** direction.
  - Limited, fully-known maximum loss.
  - Unlimited upside profit; positive gamma (profits accelerate) and positive vega (gains if IV rises).
- **Cons:**
  - Negative theta — loses value with passing time if price stays near strike (time decay accelerates near expiry).
  - Needs a move big enough to cover the cost of **both** options before it profits.
  - Pays two premiums, so it is relatively expensive vs a strangle.
- **Risk profile:** Limited loss, **unlimited** profit. Two legs.
- **Maximum profit:** **Unlimited** on the upside. On the downside, capped because price can't go below zero: `strike price − premium paid`.
- **Maximum loss:** `premium paid` (both options expire worthless if price ends exactly at the strike). Example: 5.73 per share.
- **Break-even points (two):**
  - B/E #1 = `strike price − premium paid`
  - B/E #2 = `strike price + premium paid`
  - Example (strike 45, premium 5.73): 39.27 and 50.73.
- **Greeks:** Delta ≈ 0 (ATM); positive gamma; negative theta; positive vega.
- **Important notes / caveats:** Example used stock 45.17, 45-strike call 2.88 + 45-strike put 2.85 = 5.73 debit. It is a debit strategy. The further price moves from the strike, the more profit; loss is worst exactly at the strike.
- **Plain-English explanation:** You buy both a call and a put at the same strike, betting the stock makes a big move but not caring which way. You lose the premium only if the stock sits still near the strike; you profit once it moves far enough past either break-even. Time decay works against you, so the move needs to be big and reasonably quick.

---

## 2. Short Straddle

URL: https://www.macroption.com/short-straddle/

- **Alternate names:** none given (the inverse of long straddle).
- **Core idea / construction:** Sell a call and sell a put with the **same strike** and **same expiration**, equal number of contracts. Normally ATM. Selling a strike away from the money adds directional exposure.
- **When to use:** When you expect the underlying to **stay near the strike** and/or implied volatility to **fall**; goal is to "defend the premium received."
- **Market outlook:** Short volatility, **non-directional** (delta neutral near the strike).
- **Pros:**
  - Collects premium up front (credit strategy).
  - Positive theta — gains from time decay, highest near the strike and often increasing into expiration.
  - Negative vega — profits if implied volatility drops.
- **Cons:**
  - **Unlimited** loss on the upside (and very large loss on the downside).
  - Negative gamma — losses accelerate as price moves away from the strike either way.
  - Risk/reward is "infinitely bad"; requires margin and active risk management.
- **Risk profile:** **Unlimited** loss, limited profit. Two legs.
- **Maximum profit:** `premium received` (both options expire worthless if price ends exactly at the strike).
- **Maximum loss:** **Infinite** on the upside. On the downside (price to zero): `strike price − premium received`.
- **Break-even points (two)** — identical to long straddle:
  - B/E #1 = `strike price − premium received`
  - B/E #2 = `strike price + premium received`
- **Greeks:** Delta neutral near strike; negative gamma; positive theta; negative vega.
- **Important notes / caveats:** Example mirrors long straddle: stock 45.17, sell 45 call 2.88 + sell 45 put 2.85 = 5.73 credit. Same family as other short-volatility credit trades (short strangle, iron butterfly, iron condor). Equal call and put contract counts required.
- **Plain-English explanation:** You sell both a call and a put at the same strike and pocket the premium, betting the stock barely moves. You keep the most if it lands right at the strike at expiration, but losses grow without limit if it makes a big move, so it is a high-risk income trade that needs the stock to stay calm.

---

## 3. Strap

URL: https://www.macroption.com/strap/

- **Alternate names:** A "variation of long straddle with more calls than puts" (a bullish-biased straddle).
- **Core idea / construction:** Buy calls and puts on the same underlying, **same strike, same expiration**, but with **more call contracts than put contracts** (e.g. 2 calls : 1 put). Any ratio works as long as calls > puts.
- **When to use:** When you expect a **large, fast move, preferably to the upside**, and/or rising implied volatility.
- **Market outlook:** Long volatility with a **bullish bias** (positive delta near the strike).
- **Pros:**
  - Profits from a big move either way, but **more** on the upside (steeper right-side slope, upside break-even reached faster).
  - Limited loss; positive gamma; positive vega (benefits from rising IV).
  - Adjustable bias: more calls = more bullish.
- **Cons:**
  - Negative theta — loses value as time passes if price stays near the strike.
  - Loses if volatility falls; needs a big enough, fast enough move.
  - More expensive than a plain straddle (extra call premium).
- **Risk profile:** Limited loss, **unlimited** profit. Two legs (with a bullish tilt).
- **Maximum profit:** **Unlimited** (greater on the upside due to extra calls). *Explicit formula not stated on page.*
- **Maximum loss:** Limited to the **premium paid** for all options (page header confirms "limited loss"). *Explicit labeled formula not stated on page.*
- **Break-even points (two):** Page states there are two break-evens at **unequal** distance from the strike, with the upside break-even reached much faster than the downside. *Explicit formulas not specified on page.*
- **Greeks:** Positive delta near strike; positive gamma; positive vega; negative theta.
- **Important notes / caveats:** Same V-shaped payoff as long straddle but with asymmetric slopes (profit grows faster on the upside). The closer the call and put sizes (e.g. 5:4), the more it behaves like a long straddle; the more lopsided (e.g. 5:1), the more bullish/asymmetric. Example construction: 1× 45-strike put + 2× 45-strike calls, same expiration.
- **Plain-English explanation:** A strap is a straddle tilted bullish — you buy more calls than puts at the same strike. You still profit from a big move in either direction, but you make more (and break even sooner) if the stock rises. Like any long-option play, time decay and falling volatility hurt you.

---

## 4. Strip

URL: https://www.macroption.com/strip/

- **Alternate names:** A "variation of long straddle with more puts than calls" (a bearish-biased straddle).
- **Core idea / construction:** Buy calls and puts on the same underlying, **same strike, same expiration**, but with **more put contracts than call contracts** (2:1 is most common; 1:3, 2:3, 2:5, etc. all qualify as long as puts > calls).
- **When to use:** When you expect a **large move, with the downside more likely**, and/or rising implied volatility.
- **Market outlook:** Long volatility with a **slight bearish bias** (negative delta near the strike).
- **Pros:**
  - Profits from a big move either way, but **more** on the downside (profit increases faster when underlying falls).
  - Limited loss; long gamma; long vega (benefits from rising IV).
  - Adjustable bias via the put:call ratio.
- **Cons:**
  - Short theta — time decay is "the worst enemy" of the position.
  - Loses if volatility falls while price stays near the strike.
  - Upside break-even is farther from the strike than the downside (needs a bigger up-move to profit).
- **Risk profile:** Limited loss, **unlimited** profit. Two legs (with a bearish tilt).
- **Maximum profit:** **Unlimited** (increases faster on the downside). *Explicit formula not stated on page.*
- **Maximum loss:** Limited to the **premium paid** for all options (page header confirms "limited loss"), worst exactly at the strike. *Explicit labeled formula not stated on page.*
- **Break-even points (two):** V-shaped like a straddle but asymmetric — the upside break-even is farther from the strike than the downside one. *Explicit formulas not specified on page.*
- **Greeks:** Negative delta near strike; positive (long) gamma; long vega; short (negative) theta.
- **Important notes / caveats:** Payoff is V-shaped with maximum loss exactly at the strike, just with different (asymmetric) slopes vs a straddle. The more equal the put/call sizes, the more it resembles a long straddle; the more puts dominate, the more directional/asymmetric it becomes.
- **Plain-English explanation:** A strip is a straddle tilted bearish — you buy more puts than calls at the same strike. You profit from a big move either way, but you gain more (and break even sooner) if the stock drops. As with all bought-option strategies, time decay and falling volatility are the main risks.

---

## 5. Covered Short Straddle

URL: https://www.macroption.com/covered-short-straddle/

- **Alternate names:** "Covered straddle."
- **Core idea / construction (three legs):** Buy the underlying + sell a call + sell a put with the **same strike and same expiration**. Shares must match the contracts (e.g. 100 shares per 1 call + 1 put). It is a short straddle plus a long stock position.
- **When to use:** Mildly **bullish** income view — you own (or want to own) the stock and expect it to stay near or above the strike, collecting option premium.
- **Market outlook:** **Bullish** (a long-stock + short-straddle combination).
- **Pros:**
  - Collects premium from both short options on top of holding the stock.
  - Flat, maximum payoff for any price at or above the strike (long stock offsets the short call above the strike).
  - Strike choice tunes the bias (lower strike = more bullish, higher = bearish).
- **Cons:**
  - "Covered" only protects the **upside** half; **below the strike, losses grow at double speed** (long stock and short put both lose).
  - Large downside loss possible if the stock falls a lot.
  - Capped upside profit (gives up gains above the strike).
- **Risk profile:** Limited loss and limited profit, **but the loss can be very large** if the underlying falls sharply. Three legs.
- **Maximum profit:** `strike − initial cost`, equivalently `strike − initial stock price + total premium received`. Example: 45 − 39.49 = **$5.51/share ($551)**.
- **Maximum loss:** Occurs at zero underlying price: `initial stock price + strike − total premium received`, equivalently `strike + initial cost`. Example: 45 + 39.49 = **$84.49/share ($8,449)**.
- **Break-even point (one, below the strike):** `B/E = 0.5 × (strike + initial stock price − total premium received)`. The 0.5 reflects the doubled pace of loss below the strike. Example: 0.5 × (45 + 45.22 − 5.73) = **42.245**.
- **Cash flow:** Debit strategy. `initial cost = initial stock price − call and put premium received`. Example: 45.22 − 2.88 − 2.85 = **$39.49/share**.
- **Important notes / caveats:** Example: buy 100 shares at 45.22, sell 45 call 2.88, sell 45 put 2.85. ATM strike typical. Payoff = short-straddle P/L plus the upward-sloping long-stock P/L line.
- **Plain-English explanation:** You own the stock and sell both a call and a put against it. Above the strike you make your fixed maximum profit (the stock gains offset the short call); but below the strike you lose on both the stock and the short put, so losses pile up fast. It is a bullish income play that is only "covered" on the upside.

---

## 6. Long Strangle

URL: https://www.macroption.com/long-strangle/

- **Alternate names:** none given.
- **Core idea / construction:** Buy a put and buy a call with a **higher** strike (call strike > put strike), **same expiration**, equal size. Usually both **out-of-the-money**, roughly equal distance from the underlying price.
- **When to use:** When you expect a **big move** (either direction) but want a **cheaper** setup than a straddle and/or expect rising IV.
- **Market outlook:** Long volatility, **non-directional** when strikes are equidistant (delta neutral).
- **Pros:**
  - Cheaper than a long straddle (both options are OTM).
  - Limited loss, unlimited upside; positive gamma and positive vega.
  - Strikes can be skewed to add a bullish or bearish bias.
- **Cons:**
  - Needs a **larger** move than a straddle to become profitable (the "main disadvantage").
  - Negative theta — time decay hurts, worst between the strikes.
  - Wider strikes = lower cost but lower probability of profit.
- **Risk profile:** Limited loss, **unlimited** profit. Two legs.
- **Maximum profit:** **Unlimited** on the upside. Downside: `put strike − premium paid`.
- **Maximum loss:** `premium paid` (both options expire worthless if price stays between the strikes). Example: $389.
- **Break-even points (two):**
  - B/E #1 = `put strike − premium paid` → 45 − 3.89 = **41.11**
  - B/E #2 = `call strike + premium paid` → 50 + 3.89 = **53.89**
- **Greeks:** Delta neutral (equidistant strikes); positive gamma; negative theta; positive vega.
- **Important notes / caveats:** Example: stock 47.67, buy 45 put 1.87 + buy 50 call 2.02 = 3.89 debit. Wider strikes lower cost/max loss but push break-evens out (lower probability of profit); narrower strikes make it resemble a straddle. Choosing the call strike closer = bullish; put strike closer = bearish.
- **Plain-English explanation:** You buy an OTM call and an OTM put with a gap between the strikes, betting on a big move without picking a direction. It is cheaper than a straddle, but because both options start out of the money the stock has to travel farther before you profit. Time decay is the main drag.

---

## 7. Short Strangle

URL: https://www.macroption.com/short-strangle/

- **Alternate names:** none given (the inverse of long strangle).
- **Core idea / construction:** Sell a put and sell a call with a **higher** strike (call strike > put strike), **same expiration**, equal size. Typically both OTM, equidistant from the underlying.
- **When to use:** When you expect the underlying to **stay range-bound** and/or implied volatility to **fall**.
- **Market outlook:** Short volatility, **non-directional** (delta neutral when strikes are equidistant).
- **Pros:**
  - Collects premium; wide profit zone between the two strikes.
  - Positive theta (time decay works for you); negative vega (profits if IV drops).
  - Wider strike gap = higher probability of keeping max profit.
- **Cons:**
  - **Unlimited** loss on the upside (large loss on the downside too).
  - Negative gamma — losses accelerate on a big move either way.
  - Wider gap lowers the max profit collected.
- **Risk profile:** **Unlimited** loss, limited profit. Two legs.
- **Maximum profit:** `initial cash flow = premium received` (price stays between strikes; both expire worthless). Example: $389.
- **Maximum loss:** **Infinite** on the upside. Downside (price to zero): `put strike − premium received for both options`.
- **Break-even points (two):**
  - B/E #1 = `put strike − premium received`
  - B/E #2 = `call strike + premium received`
  - Example (strikes 45/50, premium 3.89): 41.11 and 53.89.
- **Greeks:** Delta neutral; negative gamma; positive theta; negative vega.
- **Important notes / caveats:** Example: stock 47.67, sell 45 put 1.87 + sell 50 call 2.02 = 3.89 credit. Trade-off: wider gap → smaller but more-likely max profit; narrower gap → bigger but less-likely (extreme case = short straddle). Strikes can be skewed (e.g. 50/55 = bullish, 40/45 = bearish). Hedged version = iron condor.
- **Plain-English explanation:** You sell an OTM call and an OTM put and keep the premium as long as the stock stays between the strikes. It has a comfortable profit window, but a big move in either direction brings unlimited risk, so it is a range-bound income trade that must be watched carefully.

---

## 8. Long Guts

URL: https://www.macroption.com/long-guts/

- **Alternate names:** "Guts" (long guts); described as a long strangle with the strike order reversed.
- **Core idea / construction:** Buy a call (lower strike) and buy a put (higher strike) — i.e. **put strike > call strike**, so **both options are in-the-money** when price is between the strikes. Same underlying, expiration, and equal size. Everything else matches a long strangle except the reversed strike order.
- **When to use:** When you expect a **big move** either way (same use case as long strangle), using ITM options.
- **Market outlook:** Long volatility, **non-directional** when strikes are equidistant (delta neutral).
- **Pros:**
  - Same risk/payoff shape as long strangle; limited loss, unlimited upside.
  - Max loss is reduced by the strike distance (often a modest loss for ITM options).
  - Strikes tunable for bullish/bearish bias.
- **Cons:**
  - **More expensive** up front than a strangle (both options are ITM).
  - Time decay and falling volatility hurt (long-option drawbacks).
  - Wider strike gap pushes break-evens out (lower probability of profit).
- **Risk profile:** Limited loss, **unlimited** profit. Two legs.
- **Maximum profit:** **Unlimited** on the upside; downside limited only by price reaching zero.
- **Maximum loss:** `initial cost − strike distance` (occurs between/at the strikes — both options are ITM but not enough to cover cost). Example: 8.87 − 5 = **$3.87/share ($387)**.
- **Break-even points (two):**
  - B/E #1 = `put strike − initial cost` → 50 − 8.87 = **41.13**
  - B/E #2 = `call strike + initial cost` → 45 + 8.87 = **53.87**
- **Cash flow:** Debit. `initial cost = call premium + put premium`. Example: 4.38 + 4.49 = **$8.87/share**.
- **Important notes / caveats:** Example: stock 47.67, buy 45 call 4.38 + buy 50 put 4.49 = 8.87 debit. Payoff diagram is identical to a long strangle. Because both legs are ITM, between the strikes the call's intrinsic gain equals the put's intrinsic loss, so P/L is flat there. Wider strikes raise cost but lower max loss.
- **Plain-English explanation:** Long guts is a long strangle built with in-the-money options (put strike above the call strike). The payoff looks exactly like a strangle, but you pay more up front since both options already have intrinsic value. You profit on a big move either way; the most you can lose is the cost minus the gap between strikes.

---

## 9. Short Guts

URL: https://www.macroption.com/short-guts/

- **Alternate names:** "Guts" (short guts); the inverse of long guts; similar to short strangle.
- **Core idea / construction:** Sell a call (lower strike) and sell a put (higher strike) — i.e. **put strike > call strike**, so **both options are ITM** between the strikes. Same underlying and expiration; two short legs.
- **When to use:** When you expect the underlying to **stay range-bound** / low volatility (same use case as short strangle), using ITM options.
- **Market outlook:** Short volatility, **non-directional**.
- **Pros:**
  - Collects more premium up front than a short strangle/straddle (both legs ITM).
  - Limited (capped) maximum profit between the strikes.
  - Same payoff shape as a short strangle.
- **Cons:**
  - **Unlimited** loss on the upside (large loss on the downside).
  - There is **always a cash outflow at expiration** because at least one leg is always ITM.
  - Net short calls = unlimited upside risk.
- **Risk profile:** **Unlimited** loss, limited profit. Two legs.
- **Maximum profit:** `initial cash flow − strike distance`, equivalently `call premium + put premium + put strike − call strike`. Example: 8.87 − 5 = **$3.87/share ($387)** (equal to long guts max loss).
- **Maximum loss:** **Unlimited** on the upside. Downside (price falls): `put strike − initial cash flow`.
- **Break-even points (two)** — same as long guts:
  - B/E #1 = `put strike − initial premium received` → 50 − 8.87 = **41.13**
  - B/E #2 = `call strike + initial premium received` → 45 + 8.87 = **53.87**
- **Cash flow:** Credit. `initial cash flow = call premium + put premium received`. Example: 4.38 + 4.49 = **$8.87/share**.
- **Important notes / caveats:** Example: stock 47.67, sell 45 call 4.38 + sell 50 put 4.49 = 8.87 credit. Payoff diagram is the inverse of long guts and looks like a short strangle. Because both options are ITM between the strikes, their combined intrinsic value always equals the strike distance, which is why there is always some payout at expiration.
- **Plain-English explanation:** Short guts is a short strangle built with in-the-money options (put strike above the call strike). You take in a large premium but always have to pay something back at expiration since at least one leg finishes in the money. You keep the most when the stock stays between the strikes; a big move brings unlimited risk.

---

## 10. Covered Short Strangle

URL: https://www.macroption.com/covered-short-strangle/

- **Alternate names:** "Covered strangle."
- **Core idea / construction (three legs):** Buy the underlying + sell a put + sell a call with a **higher** strike (call strike > put strike), same expiration. Sizes must match (e.g. 100 shares per contract). It is a short strangle plus long stock.
- **When to use:** Mildly **bullish** income view — own the stock, expect it to hold up or rise modestly, and collect premium from the short strangle.
- **Market outlook:** **Bullish** (long stock + short strangle).
- **Pros:**
  - Collects premium from both short options on top of holding the stock.
  - Flat maximum profit for any price at or above the call strike (stock gains offset the short call).
  - Three payoff zones give a wide profitable region above the break-even.
- **Cons:**
  - "Covered" only hedges the **upside**; **below the put strike losses grow at double speed** ($2 lost per $1 drop — short put + long stock).
  - Large downside loss if the stock falls a lot.
  - Upside profit is capped above the call strike.
- **Risk profile:** Limited loss and limited profit, **but the loss can be very large** if the underlying falls sharply. Three legs.
- **Maximum profit:** `call strike − initial cost` (reached at or above the call strike). Example: 50 − 43.83 = **$6.17/share** (derived from the page's formula and example inputs).
- **Maximum loss:** At zero underlying price: `put strike + initial cost`. Example: 45 + 43.83 = **$88.83/share**.
- **Break-even point (one):** Conditional on inputs —
  - If `put strike > initial stock price + total premium received`: `B/E = initial stock price − total premium received`.
  - If `put strike < initial stock price + total premium received`: `B/E = 0.5 × (initial stock price + put strike − total premium received)`. Example (45 < 47.72 + 3.89): 0.5 × (47.72 + 45 − 3.89) = **44.415**.
- **Cash flow:** Debit. `initial cost = underlying price − call and put premium received`. Example: 47.72 − 1.87 − 2.02 = **$43.83/share**.
- **Important notes / caveats:** Example: buy 100 shares at 47.72, sell 45 put 1.87, sell 50 call 2.02. Three payoff zones: double-slope below the put strike (short put + long stock), single-slope between strikes (long stock only), constant profit above the call strike (long stock offsets short call).
- **Plain-English explanation:** You own the stock and sell both an OTM put and a higher-strike OTM call against it. Above the call strike you earn a fixed maximum profit; between the strikes the stock keeps gaining; but below the put strike you lose on both the stock and the short put, so losses double up. It is a bullish income trade that is only protected on the upside.

---

## Cross-Strategy Summary (quick-reference)

| Strategy | Direction / Vol view | Risk | Reward | Construction key |
|----------|---------------------|------|--------|------------------|
| Long Straddle | Long vol, neutral | Limited | Unlimited | Long call + long put, same strike |
| Short Straddle | Short vol, neutral | Unlimited | Limited | Short call + short put, same strike |
| Strap | Long vol, bullish | Limited | Unlimited | Long straddle, more calls than puts |
| Strip | Long vol, bearish | Limited | Unlimited | Long straddle, more puts than calls |
| Covered Short Straddle | Bullish | Limited (very large) | Limited | Long stock + short call + short put, same strike |
| Long Strangle | Long vol, neutral | Limited | Unlimited | Long put + long higher-strike call (OTM) |
| Short Strangle | Short vol, neutral | Unlimited | Limited | Short put + short higher-strike call (OTM) |
| Long Guts | Long vol, neutral | Limited | Unlimited | Long call + long higher-strike put (ITM) |
| Short Guts | Short vol, neutral | Unlimited | Limited | Short call + short higher-strike put (ITM) |
| Covered Short Strangle | Bullish | Limited (very large) | Limited | Long stock + short put + short higher-strike call |

Key patterns:

- **Straddles** use one shared strike; **strangles/guts** use two strikes (strangle = call strike higher, OTM; guts = put strike higher, ITM).
- **Strap = bullish** straddle (more calls); **Strip = bearish** straddle (more puts).
- **Long** versions = bought options = limited loss / unlimited(ish) profit, long vega, negative theta.
- **Short** versions = sold options = unlimited loss / limited profit, negative vega, positive theta.
- **Covered** versions add long stock, turn the trade **bullish**, cap profit, and **double** the downside loss rate below the put/strike.

## Fields Not Specified on Source Pages

- **Strap** and **Strip**: macroption does not give explicit labeled formulas for maximum profit, maximum loss, or break-even points (only qualitative payoff descriptions — V-shaped, asymmetric, limited loss = premium paid, unlimited profit). Noted inline above as "not specified on page."
- No page contains literal "Pros"/"Cons" lists; those sections are synthesized from each page's stated risk profile, payoff, and Greeks (no numbers invented).
- **Covered Short Strangle** max profit numeric value ($6.17) is derived by applying the page's own formula (`call strike − initial cost`) to its example inputs; the page states the formula but does not print the numeric result.
