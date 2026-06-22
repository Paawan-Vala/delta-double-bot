<!-- markdownlint-disable-file -->
# Group A Research: Single-Leg and Covered Option Strategies (macroption.com)

Status: Complete

## Research Topics / Questions

Extract structured study-note content for 9 option strategies from macroption.com. For each strategy capture: name + alternate names, core idea / construction (legs), when to use, market outlook, pros, cons, risk profile, maximum profit, maximum loss, break-even point(s), important notes / variations / caveats, and a short plain-English explanation.

Strategies (base = https://www.macroption.com/):
1. Long Call — /long-call/
2. Long Put — /long-put/
3. Short Call (Naked Call) — /short-call/
4. Short Put (Naked Put) — /short-put/
5. Covered Call — /covered-call/
6. Protective Put (Married Put) — /protective-put/
7. Protective Call — /protective-call/
8. Covered Put — /covered-put/
9. Collar — /collar/

## Source-Structure Finding (important)

macroption.com organizes these in two different page styles:

- The four single-option pages (/long-call/, /long-put/, /short-call/, /short-put/) are very short "hub" pages. Their body text is only a one-sentence summary (direction, number of legs, risk profile) plus a payoff diagram image and a link to a dedicated payoff page. The actual maximum profit / maximum loss / break-even formulas live on the linked payoff pages:
  - Long Call formulas: /call-option-payoff/
  - Long Put formulas: /put-option-payoff/
  - Short Call formulas: /short-call-payoff/
  - Short Put formulas: /short-put-payoff/
- The five with-underlying pages (/covered-call/, /protective-put/, /protective-call/, /covered-put/, /collar/) are long, self-contained articles that include setup, payoff, max profit/loss, break-even, strike/expiration selection, and Greeks.

For single-leg strategies the formula fields below are taken from the linked payoff pages (URLs cited per strategy) because the overview page itself does not state them. Where a requested field is genuinely absent, it is marked "not specified on page."

A note on Pros/Cons: macroption's pages generally do not present literal "Pros"/"Cons" lists. The pros/cons below are concise points derived directly from each page's stated risk/reward, payoff, and caveats. Volatility view is only listed where the page explicitly states it; otherwise it is marked "not specified on page."

---

## 1. Long Call

- Source pages: /long-call/ (overview) and /call-option-payoff/ (formulas)
- Strategy name / alternate names: Long Call (a.k.a. simply "buying a call"). The overview page calls it a single-leg bullish strategy.
- Core idea / construction: Buy 1 call option (single leg). A call gives the right, but not the obligation, to buy the underlying at the strike price. Payoff at expiration depends on where the underlying is relative to the strike.
- When to use: Bullish view — you expect the underlying to rise above the break-even (strike + premium) by expiration. (Overview page has no explicit "when to trade" section; outlook is stated as bullish.)
- Market outlook: Bullish. Volatility view: not specified on page.
- Pros (derived from page facts):
  - Loss is strictly limited to the premium paid — you can never lose more, even if the underlying falls to zero.
  - Unlimited upside; payoff rises in proportion with the underlying above the strike.
  - Much smaller cash outlay than buying the underlying outright.
- Cons (derived from page facts):
  - If the underlying ends at or below the strike, the option expires worthless and you lose the entire premium.
  - The underlying must climb above the break-even just to start profiting.
- Risk profile: Limited loss, unlimited profit.
- Maximum profit: Unlimited (rises in proportion with underlying price above the strike).
- Maximum loss: Equal to the initial cost of the option (premium paid); applies for underlying price at or below the strike.
- Break-even point: B/E = strike price + initial option price.
- Important notes / formula: P/L per share = MAX(underlying price − strike price, 0) − initial option price. Below/at strike the payoff is a flat line at the loss equal to premium; above strike it slopes up 1:1 with the underlying.
- Plain-English explanation: You pay a premium for the right to buy the stock at a fixed price. If the stock rises well above that price you profit dollar-for-dollar with no ceiling; if it doesn't, the most you can lose is the premium you paid. It's a capped-risk, uncapped-reward way to bet on a price increase.

---

## 2. Long Put

- Source pages: /long-put/ (overview) and /put-option-payoff/ (formulas)
- Strategy name / alternate names: Long Put (a.k.a. "buying a put"). Single-leg bearish strategy.
- Core idea / construction: Buy 1 put option (single leg). A put gives the right, but not the obligation, to sell the underlying at the strike price. It gains value as the underlying falls below the strike.
- When to use: Bearish view — you expect the underlying to fall below the break-even (strike − premium) by expiration.
- Market outlook: Bearish. Volatility view: not specified on page.
- Pros (derived from page facts):
  - Loss is strictly limited to the premium paid.
  - Profit can be very large (per-share profit grows as the underlying falls toward zero).
  - A defined-risk way to profit from, or hedge against, a decline.
- Cons (derived from page facts):
  - If the underlying ends at or above the strike, the put expires worthless and you lose the entire premium.
  - Profit is ultimately capped because the underlying cannot fall below zero.
- Risk profile: Limited loss, limited profit (but the profit "can be very large if underlying falls a lot").
- Maximum profit: Limited but usually very high. Maximum theoretical profit (if the underlying dropped to zero) per share equals the break-even price (strike − premium).
- Maximum loss: Equal to the initial cost of the option (premium paid); applies for underlying price at or above the strike.
- Break-even point: B/E = strike price − initial option price.
- Important notes / formula: P/L per share = MAX(strike price − underlying price, 0) − initial option price.
- Plain-English explanation: You pay a premium for the right to sell the stock at a fixed price, so you profit as the stock drops. Your loss is capped at the premium, while your gain grows the further the stock falls (maxing out if it hits zero). It's the bearish mirror image of a long call.

---

## 3. Short Call (Naked Call)

- Source pages: /short-call/ (overview) and /short-call-payoff/ (formulas)
- Strategy name / alternate names: Short Call, also "naked call" or "uncovered call." Single-leg bearish strategy.
- Core idea / construction: Sell (write) 1 call option (single leg) and receive premium up front. You either buy it back later or let it expire. It is the opposite side of a long call.
- When to use: You expect the underlying to NOT go up (or not move at all), ideally ending below the strike (often an out-of-the-money call is sold) so the call expires worthless and you keep the premium.
- Market outlook: Bearish (directional). Volatility view: short volatility — the position gains as volatility falls (a call loses value when volatility decreases).
- Pros (derived from page facts):
  - Immediate premium income; profitable if the underlying stays flat or falls.
  - Benefits from both time decay and falling volatility.
- Cons (derived from page facts):
  - Unlimited risk — losses grow proportionally with the underlying, which can rise without limit.
  - Upside is capped at the premium received, so risk/reward is highly asymmetric.
- Risk profile: Unlimited loss, limited profit.
- Maximum profit: The premium (cash) received when selling the call. This is the most you can gain.
- Maximum loss: Unlimited (total loss rises proportionally with the underlying, which can theoretically rise infinitely).
- Break-even point: B/E = strike price + initial option price (same formula as the long call). Profitable below this point; loses above it.
- Important notes / formula: Short call payoff per share = initial option price − MAX(0, underlying price − strike price).
- Plain-English explanation: You collect a premium for promising to deliver the stock at the strike. As long as the stock stays below the strike you keep the premium, but if it rallies hard your losses are theoretically unlimited. High-probability small gains, but a dangerous tail risk.

---

## 4. Short Put (Naked Put)

- Source pages: /short-put/ (overview) and /short-put-payoff/ (formulas)
- Strategy name / alternate names: Short Put, also "naked put" or "uncovered put." Single-leg bullish strategy.
- Core idea / construction: Sell (write) 1 put option (single leg) and receive premium up front. You either buy it back at a lower price or wait for it to expire out of the money. It is the opposite side of a long put.
- When to use: You expect the underlying to NOT go down (or not move at all), ideally ending above the strike (often an out-of-the-money put is sold) so the put expires worthless and you keep the premium.
- Market outlook: Bullish (directional). Volatility view: short volatility — the position gains as volatility falls (a put loses value when volatility decreases).
- Pros (derived from page facts):
  - Immediate premium income; profitable if the underlying stays flat or rises.
  - Benefits from time decay and falling volatility; risk is technically limited (unlike a short call).
- Cons (derived from page facts):
  - Loss can be very large — up to (strike − premium) per share if the underlying collapses to zero.
  - Risk/reward is usually unfavorable: the page's example shows risk ($4,215) nearly 15x the potential gain ($285).
- Risk profile: Limited loss, limited profit — but "the loss can be very large if underlying falls a lot."
- Maximum profit: The premium (cash) received when selling the put; reached when the underlying ends at or above the strike.
- Maximum loss: Strike price − initial option price (occurs when the underlying drops to zero).
- Break-even point: B/E = strike price − initial option price (same formula as the long put). Profitable above this point; loses below it.
- Important notes / formula: Short put payoff per share = initial option price − MAX(0, strike price − underlying price). Risk-reward ratio is typically unfavorable because the option premium is usually much smaller than the strike.
- Plain-English explanation: You collect a premium for promising to buy the stock at the strike. If the stock stays at or above the strike you keep the premium; if it crashes you are forced to buy high, so the downside is large (though not infinite). Comparable risk profile to a covered call.

---

## 5. Covered Call

- Source page: /covered-call/ (self-contained, detailed)
- Strategy name / alternate names: Covered Call; the special case where the underlying and the short call are opened at the same time is called buy-write (a subtype).
- Core idea / construction: Two legs (only one is an option): Long position in the underlying asset + Short call option on that underlying. The long underlying "covers" the otherwise-unlimited risk of the short call.
- When to use: When you hold (or want to hold) the underlying and think it will stay flat or rise only moderately in the short term — you don't expect it to fall and don't want to sell, but see limited near-term upside, so you write calls for extra income. (Two motivations: long-term holder earning income, or a deliberate buy-write for income.)
- Market outlook: Neutral to moderately bullish (want the underlying at or near the call strike, not falling, not rising far above it). Volatility view: short volatility — covered call vega is negative.
- Pros (derived from page facts):
  - Generates premium income and enhances returns on a holding.
  - Premium received lowers the break-even and cushions moderate declines.
  - Caps and offsets the short call's risk because you own the underlying (no naked-call assignment problem).
- Cons (derived from page facts):
  - Upside is capped above the call strike (you may be assigned and must deliver the underlying).
  - Still exposed to large downside on the underlying (max loss only realized if it falls to zero).
- Risk profile: Effectively limited but large downside (down to the underlying going to zero), capped upside.
- Maximum profit: Max profit = call strike − initial underlying price + call premium received (occurs at or above the call strike). P/L below the strike = underlying price at expiration − initial underlying price + call premium received.
- Maximum loss: Max loss = call premium received − initial underlying price (i.e., when the underlying falls to zero).
- Break-even point: B/E = initial underlying price − call premium received. (Notably, the formula does not directly include the strike; strike affects it only indirectly via the premium. B/E is numerically the same as the max loss, opposite sign.)
- Important notes / variations:
  - Buy-write = same strategy with both legs opened simultaneously.
  - Strike selection: a higher strike means smaller premium → higher break-even and greater max loss (worse downside) but greater max profit; the best strike is the one closest to your expected underlying price at expiration.
  - Expiration selection: shorter expirations maximize premium income per unit of time if all goes well; longer expirations are more conservative (more premium up front, lower break-even). Liquidity falls for very long expirations.
  - Greeks: positive delta (between 0 and +1; ≈ +0.5 at the money), negative gamma, negative vega, positive theta.
- Plain-English explanation: You own the stock and sell a call against it to collect premium. The premium gives you income and a small downside cushion, but in exchange you give up gains above the strike (you may be forced to sell at the strike). Best when you expect the stock to drift sideways or rise slightly.

---

## 6. Protective Put (Married Put)

- Source page: /protective-put/ (self-contained, detailed)
- Strategy name / alternate names: Protective Put, also called Married Put.
- Core idea / construction: Two legs: Long underlying + Long put option. The put works like insurance on the long underlying position; the premium is a non-refundable cost that buys downside protection.
- When to use: When you hold a long underlying position and still expect it to rise, but want protection against a possible fall; or when you fear a near-term drop but don't want to sell the underlying (e.g., long-run bullishness, dividends, or tax reasons).
- Market outlook: Bullish (with downside insurance). Volatility view: not explicitly stated; the page notes negative rho.
- Pros (derived from page facts):
  - Caps downside loss to a known, limited amount while keeping unlimited upside.
  - Lets you keep the underlying (and its dividends) instead of selling to avoid risk.
- Cons (derived from page facts):
  - The put premium is a non-refundable cost that reduces total profit and raises the break-even.
  - Below the strike the position simply sits at the (limited) max loss — protection has a price.
- Risk profile: Limited loss, unlimited profit.
- Maximum profit: Infinite (behaves like the long underlying, just reduced by the fixed put premium paid).
- Maximum loss: Max loss = put strike − initial underlying price − put premium paid (constant for any underlying price at or below the put strike).
- Break-even point: B/E = initial underlying price + put premium paid (always above the put strike).
- Important notes / variations:
  - Works like insurance; premium is the cost of protection.
  - If you bought the underlying earlier and it rose before you bought the put, the sum (initial underlying price + premium) can be below the strike — then the position cannot lose and the "max loss" is actually a minimum profit (no break-even).
  - Strike selection: usually at-the-money or out-of-the-money (lower) strikes; a lower strike is cheaper but protection kicks in later.
  - Protective put resembles a long call (put-call parity), but differs in cash flow (much higher initial cost because you buy the underlying), negative rho, and dividends (you own the underlying and receive them).
- Plain-English explanation: You own the stock and buy a put as an insurance policy. If the stock drops, the put limits your loss; if it rises, you keep the gains minus the small insurance cost. You sacrifice a bit of profit for peace of mind on the downside.

---

## 7. Protective Call

- Source page: /protective-call/ (self-contained, detailed)
- Strategy name / alternate names: Protective Call (no alternate name given on page).
- Core idea / construction: Two legs: Short underlying + Long call option. The call insures a short underlying position against an adverse (upward) price move — the mirror image of a protective put.
- When to use: When you are bearish and want to profit from a falling underlying via a short position, but also want protection against an unexpected price increase (a naked short has infinite risk; the call caps it).
- Market outlook: Bearish (with upside insurance). Volatility view: not specified on page.
- Pros (derived from page facts):
  - Caps the otherwise-infinite risk of a short underlying position.
  - Keeps full profit potential as the underlying falls (toward zero), minus the call cost.
- Cons (derived from page facts):
  - The call premium reduces profit if the trade works.
  - Above the call strike the position sits at its (limited) max loss.
- Risk profile: Limited loss, limited (but large) profit.
- Initial cash flow: Initial CF = initial underlying price − call premium paid.
- Maximum profit: Equals the initial cash flow = initial underlying price − call premium paid (occurs when the underlying goes to zero).
- Maximum loss: Max loss = initial underlying price − call premium paid − call strike (constant at or above the call strike).
- Break-even point: B/E = initial underlying price − call premium paid (below the strike). Profitable below B/E, loses above it.
- Important notes / variations:
  - If the short underlying is already profitable when you buy the call (initial underlying price − call premium > call strike), there is no break-even and the "max loss" becomes a minimum profit.
  - Strike selection: a lower call strike means protection kicks in sooner and lower max risk, but it is more expensive (call premiums rise as strike falls).
  - Protective call has a similar payoff to a long put (put-call parity); differences are mainly in cash flow and dividends, depending on the underlying.
- Plain-English explanation: You short the stock and buy a call as insurance against a surprise rally. You profit as the stock falls, your loss is capped if it instead spikes up, and the cost of that protection is the call premium. It's the bearish counterpart of a protective put.

---

## 8. Covered Put

- Source page: /covered-put/ (self-contained)
- Strategy name / alternate names: Covered Put (no alternate name given on page).
- Core idea / construction: Two legs: Short underlying + Short put option. A short put "covered" by a short underlying position. It is a credit strategy (you receive cash up front from both legs). Position sizes must match (e.g., 5 put contracts ↔ 500 short shares).
- When to use: A bearish income strategy — you profit if the underlying stays at or below the put strike. (The page has no explicit "when to trade" section; it frames the strategy as bearish with a payoff similar to a short call.) Note the "covered" label only covers downside, not upside.
- Market outlook: Bearish. Volatility view: not specified on page.
- Pros (derived from page facts):
  - Positive (credit) initial cash flow from selling both the put and the underlying.
  - Profitable across the whole range at or below the put strike.
- Cons (derived from page facts):
  - Theoretically unlimited loss if the underlying rises (the short underlying drives losses).
  - The "covered" name is misleading — there is no upside protection.
- Risk profile: Unlimited loss, limited profit.
- Initial cash flow (credit): initial stock price received + put premium received.
- Maximum profit: Max profit = initial cash flow − put strike = initial stock price received + put premium received − put strike (occurs at and below the put strike).
- Maximum loss: Unlimited (when the underlying rises above the strike, the put is worthless and the short underlying produces theoretically infinite loss).
- Break-even point: B/E = initial cash flow = initial stock price received + put premium received.
- Important notes / related strategies: Payoff resembles a short call. Related: protective put (the inverse — long underlying + long put), covered call (long underlying + short call), and collar (long underlying + short call + long put).
- Plain-English explanation: You short the stock and also sell a put against it for extra premium. You keep the maximum profit as long as the stock stays at or below the strike, but because you're short the stock, a rally produces unlimited losses. It is the bearish, income-oriented counterpart to the covered call.

---

## 9. Collar

- Source page: /collar/ (self-contained, detailed)
- Strategy name / alternate names: Collar (no alternate name given on page).
- Core idea / construction: Three legs — the only common strategy using all three instrument types: Long underlying + Long put (lower strike, downside protection) + Short call (higher strike, helps pay for the put / earn income). It combines a covered call (short call) with a protective put (long put).
- When to use: To protect a long underlying position at low or even zero net option cost, accepting a capped upside in return. (No explicit "when to trade" heading; outlook is stated as bullish with limited loss and limited profit — a cautious, hedged long.)
- Market outlook: Bullish but cautious / range-bound. Volatility view: not specified on page.
- Pros (derived from page facts):
  - Downside is strictly limited by the long put.
  - The short call premium offsets (sometimes fully) the cost of the put — protection can be nearly free.
- Cons (derived from page facts):
  - Upside is capped above the call strike.
  - Both profit and loss are confined to a narrow band between the two strikes.
- Risk profile: Limited loss, limited profit.
- Construction rules (from page): the call and put must share the same expiration; the call strike must be higher than the put strike; position sizes must match.
- Initial cost: Collar initial cost = initial stock price + put premium − call premium (the two option legs net to either a credit or a debit depending on their relative prices).
- Maximum profit: Max profit = call strike − initial cost (applies at or above the higher/call strike).
- Maximum loss: Max loss = initial cost − put strike (applies at or below the lower/put strike).
- Break-even point: One break-even, between the strikes: B/E = initial cost = initial stock price paid + put premium paid − call premium received.
- Important notes / variations:
  - Risk/reward is roughly 1:1 when the underlying starts about halfway between the two strikes.
  - Strike selection: a higher call strike raises net cost (smaller premium received) but extends the profit window; a lower put strike lowers cost but delays downside protection.
  - Related strategies (similar payoff): bull call spread and bull put spread (without the underlying); covered call (collar without the downside protection); protective put (collar without the short call).
- Plain-English explanation: You own the stock, buy a put below the current price for protection, and sell a call above it to pay for that protection. Your outcome is "collared" into a band: you can't lose much below the put strike and can't gain above the call strike, often for little or no net option cost.

---

## Capture Summary

- Strategies captured: 9 of 9.
- Pages that failed to load: none.
- Fields explicitly present on the requested 9 pages vs. supplemented:
  - The four single-leg pages (/long-call/, /long-put/, /short-call/, /short-put/) contain only a one-line summary (direction, legs, risk profile) plus a payoff-page link; their max profit / max loss / break-even formulas were taken from the linked payoff pages (/call-option-payoff/, /put-option-payoff/, /short-call-payoff/, /short-put-payoff/), which are cited per strategy.
  - The five with-underlying pages are self-contained and supplied all formula fields directly.
- Fields marked "not specified on page":
  - Volatility view for Long Call, Long Put, Protective Put, Protective Call, Covered Put, and Collar (those pages do not state a volatility/vega view; short call, short put, and covered call explicitly state a short-volatility view).
  - Explicit "When to Trade" sections are absent from the Covered Put and Collar pages (outlook inferred from the page's stated direction and payoff); Covered Call frames timing via its two use-cases rather than a dedicated heading.
  - Pros/Cons are not given as literal lists on any page; the lists above are derived from each page's stated risk/reward and caveats.

