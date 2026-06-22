<!-- markdownlint-disable-file -->
# Group G Research: Ratio Spreads and Box Spreads (macroption.com)

## Research Scope

Extract structured study-note content for six option strategies from macroption.com:

1. Call Ratio Spread — https://www.macroption.com/call-ratio-spread/
2. Put Ratio Spread — https://www.macroption.com/put-ratio-spread/
3. Call Ratio Backspread — https://www.macroption.com/call-ratio-backspread/
4. Put Ratio Backspread — https://www.macroption.com/put-ratio-backspread/
5. Long Box Spread — https://www.macroption.com/long-box-spread/
6. Short Box Spread — https://www.macroption.com/short-box-spread/

## Status

Complete. All six pages fetched.

## Page Type Summary (Stub vs Full Article)

| # | Strategy | Page type | What macroption actually states |
|---|----------|-----------|----------------------------------|
| 1 | Call Ratio Spread | STUB | Intro sentence + payoff image + classification only |
| 2 | Put Ratio Spread | STUB | Intro sentence + payoff image + classification only |
| 3 | Call Ratio Backspread | STUB | Intro sentence + classification only (no image surfaced) |
| 4 | Put Ratio Backspread | STUB | Intro sentence + payoff image + classification only |
| 5 | Long Box Spread | FULL | Setup, Example, Payoff, Order/Distance of Strikes, Cash Flow, "as a Bond", Arbitrage |
| 6 | Short Box Spread | FULL | Setup, Example, Payoff, Cash-Flow, "as Synthetic Loan", Risks |

Notation used in standard-reference formulas below: K1 = lower strike, K2 = higher strike, C = net credit received at entry (>= 0), D = net debit paid at entry. A "1x2" ratio is assumed (buy/sell quantities of 1 and 2) unless noted.

Important sourcing note: For the four stub pages, macroption states only the strategy name, alternate names, the legs concept (via the "ratio spread"/"backspread" links), and a risk/reward classification. It does NOT state formulas, pros/cons, when-to-use, or numeric examples. All formulas and lists in those four sections are labelled "standard reference (not stated on macroption page)" and are well-known textbook results, NOT attributed to macroption.

---

## 1. Call Ratio Spread

### Strategy name and alternate names

- Call Ratio Spread
- Alternate names (stated on page): "ratio call spread", "bull ratio spread"

### Core idea / how it works (legs and ratio)

- A ratio spread sells MORE options than it buys (net short options).
- Standard reference (not stated on macroption page): typical 1x2 construction = buy 1 lower-strike call (K1) and sell 2 higher-strike calls (K2). Net short one extra (naked) call. Usually opened for zero cost or a net credit.

### When to use it

- Standard reference (not stated on macroption page): neutral to mildly bullish view; you expect the underlying to drift up toward the short strike (K2) but not blow past it. Used to finance a long call cheaply (or for a credit) and to profit from time decay / flat-to-falling implied volatility in the target zone.

### Market outlook (direction + volatility)

- Direction: macroption classifies it as non-directional and "often slightly bullish".
- Volatility: standard reference (not stated on macroption page): net short options, so generally short volatility / short vega — benefits when IV stays flat or falls.

### Pros (standard reference — not stated on macroption page)

- Can often be opened for zero cost or a net credit.
- Profits across a range and on a mild up-move into the short strike.
- Time decay (theta) works in your favour in the target zone.
- If opened for a credit, little or no downside risk if the underlying falls.

### Cons (standard reference — not stated on macroption page)

- Unlimited loss on a strong rally (the extra short call is naked).
- Margin-intensive because of the naked short call.
- Losses accelerate quickly once the underlying pushes above the upper break-even.
- Wrong tool if you are strongly bullish.

### Risk profile

- Stated on page: unlimited loss and limited profit.
- This is the classic "net short options, unlimited risk on the naked side" ratio spread.

### Maximum profit (standard reference — not stated on macroption page)

- Occurs at the short strike (K2) at expiration.
- Max profit = (K2 - K1) + C (credit version), or (K2 - K1) - D (debit version).

### Maximum loss (standard reference — not stated on macroption page)

- Unlimited on the upside above the upper break-even (one naked short call, slope -1 per share above K2).

### Break-even point(s) (standard reference — not stated on macroption page)

- Upper break-even = 2*K2 - K1 + C (credit version) = K2 + max profit.
- Lower break-even (only if opened for a net debit) = K1 + D. If opened for a credit, there is no lower break-even (the position is profitable on the downside).

### Important notes / variations / caveats

- The "ratio" (e.g., 1x2, 2x3, 1x3) changes how much naked short exposure you carry; more extra short calls = more upside risk.
- Macroption page is a stub: it provides the payoff diagram image and the classification, but no numbers — do not attribute formulas above to macroption.

### Plain-English explanation

A call ratio spread is buying one call and selling two higher-strike calls, usually for little or no cost. You make your best profit if the stock drifts up to exactly the short strike by expiration, and you keep the credit if it stays low. The danger is a big rally: because you sold one more call than you bought, your loss above the upper break-even is unlimited.

---

## 2. Put Ratio Spread

### Strategy name and alternate names

- Put Ratio Spread
- Alternate names (stated on page): "ratio put spread", "bear ratio spread"

### Core idea / how it works (legs and ratio)

- Sell MORE puts than you buy (net short options).
- Standard reference (not stated on macroption page): typical 1x2 construction = buy 1 higher-strike put (K2) and sell 2 lower-strike puts (K1). Net short one extra (naked) put. Usually opened for zero cost or a net credit.

### When to use it

- Standard reference (not stated on macroption page): neutral to mildly bearish view; you expect the underlying to drift down toward the short strike (K1) but not crash. Used to finance a long put cheaply (or for a credit) and to profit from time decay / flat-to-falling IV in the target zone.

### Market outlook (direction + volatility)

- Direction: macroption classifies it as non-directional and "often slightly bearish".
- Volatility: standard reference (not stated on macroption page): net short options, so generally short volatility / short vega.

### Pros (standard reference — not stated on macroption page)

- Can often be opened for zero cost or a net credit.
- Profits across a range and on a mild down-move into the short strike.
- Time decay works in your favour in the target zone.

### Cons (standard reference — not stated on macroption page)

- Very large (though technically bounded) loss if the underlying drops sharply.
- Naked short puts carry assignment risk and tie up margin.
- Wrong tool if you expect a crash.

### Risk profile

- Stated on page: limited loss and limited profit — but macroption explicitly warns "the loss can be very large if underlying falls a lot."
- Nuance vs the user's "unlimited risk" framing: a put ratio spread's downside is only "limited" because the underlying price cannot fall below zero. In practice the loss can still be very large. This is the key contrast with the call ratio spread, whose upside truly is unlimited.

### Maximum profit (standard reference — not stated on macroption page)

- Occurs at the short strike (K1) at expiration.
- Max profit = (K2 - K1) + C (credit version), or (K2 - K1) - D (debit version).

### Maximum loss (standard reference — not stated on macroption page)

- Occurs at underlying price = 0 (worst case, bounded by the zero floor).
- Max loss = (2*K1 - K2) - C (credit version). Large but finite.

### Break-even point(s) (standard reference — not stated on macroption page)

- Lower break-even = 2*K1 - K2 - C (credit version).
- Upper break-even (only if opened for a net debit) = K2 - D. If opened for a credit, there is no upper break-even (profitable on the upside).

### Important notes / variations / caveats

- Risk is "limited" only in the mathematical sense (underlying floored at zero); treat it as effectively large downside risk.
- Macroption page is a stub: payoff image + classification only, no numbers.

### Plain-English explanation

A put ratio spread is buying one put and selling two lower-strike puts, usually for little or no cost. You profit best if the stock eases down to the short strike by expiration. Unlike the call version your maximum loss is technically capped (a stock can only fall to zero), but that capped loss can still be very large if the market sells off hard.

---

## 3. Call Ratio Backspread

### Strategy name and alternate names

- Call Ratio Backspread
- Alternate names: none stated on page (commonly also "call backspread" or "reverse call ratio spread" — standard reference, not stated on page).

### Core idea / how it works (legs and ratio)

- A backspread BUYS more options than it sells (net long options) — the mirror image of a ratio spread.
- Standard reference (not stated on macroption page): typical 1x2 construction = sell 1 lower-strike call (K1) and buy 2 higher-strike calls (K2). Net long one extra call. Often opened for zero cost or a net credit.

### When to use it

- Standard reference (not stated on macroption page): you expect a large upside move (an upside breakout) combined with rising volatility, and you want limited risk while keeping unlimited upside. Often structured for a credit so a flat or down move still yields a small gain.

### Market outlook (direction + volatility)

- Direction: bullish — wants a big up move.
- Volatility: macroption classifies it as a long volatility strategy (net long options, long vega/gamma — benefits from rising IV and large moves).

### Pros (standard reference — not stated on macroption page)

- Unlimited profit potential on a strong rally.
- Limited, defined risk.
- Often opened for zero cost or a net credit (small gain even if the move never comes).
- Long volatility: benefits from a jump in implied volatility.

### Cons (standard reference — not stated on macroption page)

- Maximum loss occurs if the underlying sits at/near the long strike (K2) at expiration ("dead zone").
- Time decay (theta) works against you while you wait for the move.
- Needs a sizeable move to pay off; a small or stagnant move is the worst outcome.

### Risk profile

- Stated on page: limited loss and unlimited potential profit.
- Classic backspread: net long options, capped downside, uncapped upside — the opposite of the call ratio spread.

### Maximum profit (standard reference — not stated on macroption page)

- Unlimited on the upside above the upper break-even (one extra long call, slope +1 per share above K2).

### Maximum loss (standard reference — not stated on macroption page)

- Occurs at the long strike (K2) at expiration.
- Max loss = (K2 - K1) - C (credit version), or (K2 - K1) + D (debit version).

### Break-even point(s) (standard reference — not stated on macroption page)

- Upper break-even = 2*K2 - K1 - C (credit version).
- Lower break-even = K1 + C (credit version) — below this (down to the credit kept) the position is mildly profitable.

### Important notes / variations / caveats

- Macroption page is a stub: only the one-line intro and classification were present (no payoff image surfaced in the fetch).
- The further out the long strike vs the short strike, the cheaper/credit the entry but the larger the potential dead-zone loss zone.

### Plain-English explanation

A call ratio backspread sells one call and buys two higher-strike calls, often for a small credit. It is a bet on a big upside breakout with rising volatility: your gains are unlimited if the stock soars, and your risk is capped. The worst case is the stock drifting up just to the long strike and stalling, where you take the maximum (but limited) loss.

---

## 4. Put Ratio Backspread

### Strategy name and alternate names

- Put Ratio Backspread
- Alternate names: none stated on page (commonly also "put backspread" or "reverse put ratio spread" — standard reference, not stated on page).

### Core idea / how it works (legs and ratio)

- A backspread BUYS more options than it sells (net long options).
- Standard reference (not stated on macroption page): typical 1x2 construction = sell 1 higher-strike put (K2) and buy 2 lower-strike puts (K1). Net long one extra put. Often opened for zero cost or a net credit.

### When to use it

- Standard reference (not stated on macroption page): you expect a large downside move (a sell-off or crash) combined with rising volatility, and you want limited risk. Often structured for a credit so a flat or up move still yields a small gain.

### Market outlook (direction + volatility)

- Direction: bearish — wants a big down move.
- Volatility: macroption classifies it as a long volatility strategy (net long options, long vega/gamma).

### Pros (standard reference — not stated on macroption page)

- Large profit on a sharp sell-off.
- Limited, defined risk.
- Often opened for zero cost or a net credit.
- Long volatility: benefits from a jump in implied volatility (puts tend to gain IV in sell-offs).

### Cons (standard reference — not stated on macroption page)

- Maximum loss occurs if the underlying sits at/near the long strike (K1) at expiration.
- Time decay works against you while you wait.
- Profit is bounded by the zero floor on the underlying (a stock cannot fall below zero).

### Risk profile

- Stated on page: limited loss and limited profit — but macroption explicitly notes "the profit can be very large if underlying falls a lot."
- Nuance: the profit is "limited" only because the underlying cannot fall below zero. It is the long-volatility mirror of the put ratio spread.

### Maximum profit (standard reference — not stated on macroption page)

- Occurs at underlying price = 0 (bounded by the zero floor).
- Max profit = (2*K1 - K2) + C (credit version). Large but finite.

### Maximum loss (standard reference — not stated on macroption page)

- Occurs at the long strike (K1) at expiration.
- Max loss = (K2 - K1) - C (credit version), or (K2 - K1) + D (debit version).

### Break-even point(s) (standard reference — not stated on macroption page)

- Upper break-even = K2 - C (credit version) — above this (up to the credit kept) the position is mildly profitable.
- Lower break-even = 2*K1 - K2 + C (credit version) — below this the position becomes increasingly profitable toward the zero floor.

### Important notes / variations / caveats

- Macroption page is a stub: payoff image + classification only, no numbers.
- "Limited profit" is a technicality (zero floor); treat the downside payoff as effectively large.

### Plain-English explanation

A put ratio backspread sells one put and buys two lower-strike puts, often for a small credit. It is a bet on a sharp sell-off plus rising volatility, with capped risk. Profits grow large as the stock falls (capped only because a stock cannot go below zero), while the worst case is the stock drifting down just to the long strike and stalling.

---

## 5. Long Box Spread

### Strategy name and alternate names

- Long Box Spread (also just "box spread"; "long box")

### Core idea / how it works (legs and ratio)

- An arbitrage / financing strategy with FOUR legs. It is a combination of two vertical spreads with identical strikes: a bull call spread + a bear put spread (the two DEBIT vertical spreads).
- The four options (stated on page):
  - Long call with lower strike
  - Short call with higher strike
  - Long put with higher strike
  - Short put with lower strike
- Constraint (stated on page): long call strike = short put strike (the lower strike); long put strike = short call strike (the higher strike).
- Example (stated on page): Buy 45 call, Sell 50 call, Buy 50 put, Sell 45 put. The two calls form a 45/50 bull call spread; the two puts form a 50/45 bear put spread.

### When to use it

- Stated on page: the main motivation is arbitrage — making riskless profit when the options are mispriced.
- Stated on page: it behaves like a zero-coupon bond / lending cash; use it to capture a small interest-like return (or to lend at an implied rate).

### Market outlook (direction + volatility)

- Direction: none — the payoff is constant (non-directional) at any underlying price. Stated on page: "the resulting total box spread payoff is constant ... at any underlying price."
- Volatility: effectively neutral; it is a financing/arbitrage position, not a volatility bet.

### Pros (derived from page content)

- Payoff is fixed and known in advance (payoffs of the legs cancel out).
- Near risk-free in payoff terms; behaves like a zero-coupon bond (a way to lend cash at an implied rate).
- Profits with certainty at expiration if entered below fair value (riskless arbitrage when mispriced).

### Cons (stated on page, in the Arbitrage section)

- Transaction costs from the four legs may be too high to make the arbitrage viable.
- The profit may only represent the riskless interest on the capital tied up, and that cash only comes back at expiration — so the time value of money and the trader's cost of financing must be considered.
- If the options are American, there is risk of early assignment.

### Risk profile

- Near risk-free in market-direction terms: the outcome is fixed (a small profit or a small loss) regardless of underlying price.
- Real risks are execution, financing/time-value-of-money, and early assignment (American options) — NOT market direction.

### Maximum profit / Maximum loss / payoff

- The payoff at expiration is constant and (stated on page) "exactly equal to strike distance regardless of underlying price." There is no separate max-profit vs max-loss as a function of price.
- Standard reference (not stated as a formula on macroption page): value at expiration = (K2 - K1), i.e., the distance between the strikes. Net result = (K2 - K1) - net debit paid. If fairly priced the net debit approx. equals the present value of (K2 - K1), so the result is a small positive amount equal to the interest earned.

### Break-even point(s)

- Not applicable in the directional sense: the payoff line is flat across all underlying prices (no price-based break-even). The position is profitable or not based on entry price vs the present value of the strike distance, not on where the underlying lands.

### Important notes / variations / caveats

- Order of strikes matters (stated on page): if the long call/short put strike is the HIGHER one (strikes reversed), the position is instead a short box spread — identical payoff profile but opposite cash flow.
- Distance between strikes does not change the payoff profile (still constant) but affects the cash flow size.
- Cash flow (stated on page): initial cash flow is negative (two debit spreads); at expiration the box has positive value equal to the strike distance. This is the "lending" / zero-coupon-bond profile.
- External practical caveat (not from macroption, widely-known context): box spreads are used as a synthetic financing / interest-rate tool. The well-known 2018 Robinhood "1R0NYMAN" blow-up involved a trader using box spreads (short boxes) as cheap leverage and being wiped out by assignment/margin — a cautionary tale that "risk-free" boxes are not risk-free when using American options and oversized positions.

### Plain-English explanation

A long box spread combines a bull call spread and a bear put spread on the same two strikes, so the four legs lock in a fixed payoff equal to the distance between the strikes no matter where the underlying ends up. You pay cash up front and receive that fixed amount at expiration, so it works just like buying a zero-coupon bond — a way to lend money at an implied interest rate or to arbitrage mispriced options. The catch is that it is only "risk-free" on paper: commissions on four legs, the time value of the cash tied up, and early-assignment risk on American options can all turn the supposed sure profit into a loss.

---

## 6. Short Box Spread

### Strategy name and alternate names

- Short Box Spread (also "short box"); the inverse position of the long box spread.

### Core idea / how it works (legs and ratio)

- An arbitrage / financing strategy with FOUR legs; the inverse of a long box. It combines a bear call spread + a bull put spread (the two CREDIT vertical spreads).
- The four options (stated on page):
  - Short call with lower strike
  - Long call with higher strike
  - Short put with higher strike
  - Long put with lower strike
- Example (stated on page): Sell 45 call, Buy 50 call, Sell 50 put, Buy 45 put. The two calls form a bear call spread (short call strike is lower); the two puts form a bull put spread (short put strike is higher).

### When to use it

- Stated on page: opening a short box is "quite like taking a loan, which will be repaid at expiration" — used as a synthetic loan / financing tool (borrow cash now, repay at expiration at an implied interest rate).
- Also used for arbitrage when the box is mispriced (inverse of the long box).

### Market outlook (direction + volatility)

- Direction: none — payoff is constant at any underlying price (inverse of the long box).
- Volatility: effectively neutral; it is a borrowing/arbitrage position, not a volatility bet.

### Pros (derived from page content)

- Generates positive cash up front (it is a combination of two credit spreads) — like receiving a loan.
- Fixed, known outcome at expiration regardless of underlying price.
- Implied borrowing rate is "not much higher than riskless money market rates" (stated on page) — potentially cheap financing.

### Cons (stated on page)

- If fairly priced, the result is a small loss corresponding to the interest paid on the loan.
- Transaction costs: bid-ask spread and commissions on four legs.
- Possible margin requirements.
- Risks (see risk profile) make it less viable in reality than it first appears.

### Risk profile

- Payoff is fixed at expiration (a small profit or small loss) regardless of underlying price — not a directional risk.
- Real risks (stated on page):
  - Execution risk: a complex four-leg position; things can go wrong placing the trades.
  - Early assignment: if the options are American there is early-assignment risk — "particularly dangerous when a trader, thinking of the strategy as riskless, takes a position that is too large for his available capital."

### Maximum profit / Maximum loss / payoff

- The payoff at expiration is constant (inverse of the long box). Stated on page: it has a fixed outcome (small profit or small loss).
- Standard reference (not stated as a formula on macroption page): obligation at expiration = (K2 - K1), the strike distance (cash paid out). Net result = net credit received up front - (K2 - K1). If fairly priced the credit approx. equals the present value of (K2 - K1), so the result is a small loss equal to the interest paid (cost of the synthetic loan).

### Break-even point(s)

- Not applicable in the directional sense: the payoff is flat across all underlying prices. Profit/loss depends on entry credit vs the present value of the strike distance, not on where the underlying lands.

### Important notes / variations / caveats

- Cash flow (stated on page): initial cash flow is positive; cash flow at expiration is negative — the "borrowing" profile (opposite of the long box).
- Synthetic loan: implied interest rate close to riskless money-market rates, which is why it is marketed as cheap financing — but transaction costs, margin, and assignment risk erode that benefit.
- External practical caveat (not from macroption, widely-known context): the 2018 Robinhood "1R0NYMAN" incident is the canonical example of a short-box blow-up — a retail trader used short box spreads as cheap leverage, treated them as risk-free, and was wiped out when early assignment / margin turned the "riskless" trade into a large loss. Macroption's own warning ("too large for his available capital") describes exactly this failure mode.

### Plain-English explanation

A short box spread is the reverse of the long box: a bear call spread plus a bull put spread on the same two strikes, which brings in cash up front and requires you to pay back the fixed strike distance at expiration. That makes it work like a synthetic loan — you borrow money now at an implied interest rate close to money-market rates and repay it later. It is not truly risk-free, though: four-leg execution problems, margin requirements, and (with American options) early assignment can hurt you, especially if you oversize the position believing it is safe.

---

## Cross-Strategy Comparison (Ratio vs Backspread vs Box)

| Feature | Call Ratio Spread | Put Ratio Spread | Call Ratio Backspread | Put Ratio Backspread | Long Box | Short Box |
|---|---|---|---|---|---|---|
| Net option position | Short (sell more) | Short (sell more) | Long (buy more) | Long (buy more) | Hedged (4 legs cancel) | Hedged (4 legs cancel) |
| Direction bias (macroption) | Non-directional / slightly bullish | Non-directional / slightly bearish | Bullish | Bearish | None | None |
| Volatility | Short vol (std ref) | Short vol (std ref) | Long volatility (stated) | Long volatility (stated) | Neutral | Neutral |
| Risk (macroption wording) | Unlimited loss | Limited loss (can be very large) | Limited loss | Limited loss | Fixed (near risk-free) | Fixed (near risk-free) |
| Reward (macroption wording) | Limited profit | Limited profit | Unlimited profit | Limited profit (can be very large) | Fixed small profit/loss | Fixed small profit/loss |
| Primary purpose | Income / range | Income / range | Bet on big up move + vol | Bet on big down move + vol | Lend cash / arbitrage | Borrow cash / arbitrage |

Key teaching point: ratio spread = SELL more than you buy (net short, the naked side carries the big risk — truly unlimited for calls, "very large" for puts because of the zero floor). Backspread = BUY more than you sell (net long, limited risk, long volatility — the big payoff is on the naked-long side). Box spread = a fully hedged four-leg position (bull call spread + bear put spread for long; bear call + bull put for short) whose payoff is locked to the distance between the strikes and is used as a financing / arbitrage instrument, not a market-direction bet.

## Fields Not Found on Page (gaps)

- Call Ratio Spread (stub): when-to-use, pros, cons, max-profit/loss numbers, break-evens — not specified on page; filled with standard reference.
- Put Ratio Spread (stub): same as above — not specified on page; filled with standard reference.
- Call Ratio Backspread (stub): same as above, and no payoff image surfaced — not specified on page; filled with standard reference.
- Put Ratio Backspread (stub): same as above — not specified on page; filled with standard reference.
- Long Box Spread (full): explicit algebraic max-profit/break-even formulas are not written out as equations on the page (the page describes the constant payoff = strike distance in words); formula form added as standard reference.
- Short Box Spread (full): same as Long Box — payoff described in words (constant), explicit formula added as standard reference.
- Robinhood box-spread blow-up: NOT mentioned anywhere on the macroption pages; added as clearly-labelled external context.

## References

- [Call Ratio Spread — macroption](https://www.macroption.com/call-ratio-spread/) (stub)
- [Put Ratio Spread — macroption](https://www.macroption.com/put-ratio-spread/) (stub)
- [Call Ratio Backspread — macroption](https://www.macroption.com/call-ratio-backspread/) (stub)
- [Put Ratio Backspread — macroption](https://www.macroption.com/put-ratio-backspread/) (stub)
- [Long Box Spread — macroption](https://www.macroption.com/long-box-spread/) (full article)
- [Short Box Spread — macroption](https://www.macroption.com/short-box-spread/) (full article)
- [Ratio Spreads category — macroption](https://www.macroption.com/ratio-spreads/)
- [Box Spreads category — macroption](https://www.macroption.com/box-spreads/)
