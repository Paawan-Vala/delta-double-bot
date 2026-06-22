<!-- markdownlint-disable-file -->
# Group I — Synthetic Straddles, Strangles & Covered Strangle Research

Source base: https://www.macroption.com/

Status: Complete

## Research Topics / Questions

Extract for each of 9 synthetic positions:
- Strategy name + alternate names
- Core idea / construction legs (stock + options replicating a straddle/strangle)
- When to use
- Market outlook (volatility view)
- Pros
- Cons
- Risk profile (limited vs unlimited)
- Maximum profit
- Maximum loss
- Break-even point(s)
- Important notes / which standard straddle/strangle it replicates
- Plain-English explanation

Pages:
1. Long Call Synthetic Straddle — /long-call-synthetic-straddle/
2. Long Put Synthetic Straddle — /long-put-synthetic-straddle/
3. Short Call Synthetic Straddle — /short-call-synthetic-straddle/
4. Short Put Synthetic Straddle — /short-put-synthetic-straddle/
5. Long Call Synthetic Strangle — /long-call-synthetic-strangle/
6. Long Put Synthetic Strangle — /long-put-synthetic-strangle/
7. Short Call Synthetic Strangle — /short-call-synthetic-strangle/
8. Short Put Synthetic Strangle — /short-put-synthetic-strangle/
9. Synthetic Covered Strangle — /synthetic-covered-strangle/

---

## Page Status Summary (sourcing)

| # | Strategy | Page type | Macroption states P/L & break-even? |
|---|----------|-----------|--------------------------------------|
| 1 | Long Call Synthetic Straddle | Partial (intro + Setup/construction) | No — used standard reference |
| 2 | Long Put Synthetic Straddle | Partial (intro + Setup + Differences) | No — used standard reference |
| 3 | Short Call Synthetic Straddle | Partial (intro + Setup + Example) | No — used standard reference |
| 4 | Short Put Synthetic Straddle | Partial (intro + Setup + Example + Differences) | No — used standard reference |
| 5 | Long Call Synthetic Strangle | Partial (intro + Example) | No — used standard reference |
| 6 | Long Put Synthetic Strangle | Partial (intro + Example) | No — used standard reference |
| 7 | Short Call Synthetic Strangle | Partial (intro + Example) | No — used standard reference |
| 8 | Short Put Synthetic Strangle | Partial (intro + Example) | No — used standard reference |
| 9 | Synthetic Covered Strangle | FULL (Setup + Example + Cash Flow + Payoff + Max Profit + Max Loss) | Yes — formulas taken directly from page |

Note: none of the pages are true one-line stubs, but 8 of 9 give only the construction/classification (and an example for most) without an explicit payoff section. For those, max profit / max loss / break-even are filled from the standard straddle/strangle the position replicates and are labeled "standard reference (not stated on macroption page)." Pros/Cons and "When to use" are not given as dedicated sections on any page; where the page's "Differences" section supplies trade-offs they are quoted, otherwise items are labeled "derived / general."

---

## 1. Long Call Synthetic Straddle

- **Strategy name / alternates:** Long Call Synthetic Straddle. Call variant of the synthetic long straddle.
- **Core idea / construction (per macroption):** Replicates a long straddle but replaces the long put leg with a synthetic put (short underlying + long call). Math given on page: Long straddle = long call + long put; Synthetic put = short underlying + long call; therefore **Long call synthetic straddle = short underlying + 2× long call**. Setup: buy 2 call contracts and sell short 100 shares (short shares = half the shares represented by the long calls). Two legs.
- **When to use:** Not stated on page. Derived/general: when you expect a large move in either direction (same use case as a long straddle) and prefer to build the put side synthetically — e.g., you are already short the stock, or calls are relatively more attractively priced than puts.
- **Market outlook (volatility view):** Long volatility / non-directional — page explicitly classifies it as "long volatility." Profits from a big move up or down.
- **Pros (derived / general):** Same unlimited-upside, limited-loss payoff as a long straddle; lets you assemble a straddle from calls + a short stock position; useful via put-call parity when one option type is cheaper.
- **Cons (derived / general):** Requires short-selling the underlying (may be restricted/impossible, borrow costs); short-stock holder pays dividends; more legs/commissions than a plain straddle.
- **Risk profile:** Limited loss, unlimited potential profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): effectively unlimited as the underlying rises far above the strike (large but capped on the downside since price can't go below zero). Mirrors a long straddle.
- **Maximum loss:** Standard reference (not stated on page): limited to the net cost (net debit) built into the position; for a long straddle this is the total premium paid, realized when the underlying finishes at the strike.
- **Break-even point(s):** Standard reference (not stated on page): strike ± net debit (two break-evens, one above and one below the strike).
- **Replicates:** Long straddle (single strike).
- **Plain-English:** This is just a long straddle wearing a disguise. Instead of buying a put, you short the stock and buy a second call at the same strike, which together behave like that put. You win if the stock makes a big move either way, and the most you can lose is what you paid to set it up.

---

## 2. Long Put Synthetic Straddle

- **Strategy name / alternates:** Long Put Synthetic Straddle. Put variant of the synthetic long straddle.
- **Core idea / construction (per macroption):** Replicates a long straddle but replaces the call leg with a synthetic call (long underlying + long put). Math given on page: Long straddle = long call + long put; Synthetic long call = long underlying + long put; therefore **Long put synthetic straddle = long underlying + 2× long put**. Setup: buy 2 put contracts and buy 100 shares (put size double the underlying share count). Two legs.
- **When to use:** Not stated on page. Derived/general: when you expect a large move either way and prefer the long-stock construction (e.g., you already own the shares, or short selling is unavailable).
- **Market outlook (volatility view):** Long volatility / non-directional (page: "long volatility").
- **Pros (from page's "Differences" section):** Often easier to trade because there is no short selling of the underlying; the holder receives dividends. (Same limited-loss / unlimited-profit payoff as a long straddle.)
- **Cons (from page's "Differences" section):** Requires high initial cash outflow (you must buy the underlying). General: more legs/commissions than a plain straddle. (Page notes dividend/interest effects are normally already reflected in option prices, so they shouldn't change profitability by themselves.)
- **Risk profile:** Limited loss, unlimited potential profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): effectively unlimited on a large up-move (large but capped on the downside). Mirrors a long straddle.
- **Maximum loss:** Standard reference (not stated on page): limited to the net debit paid, realized at the strike.
- **Break-even point(s):** Standard reference (not stated on page): strike ± net debit.
- **Replicates:** Long straddle (single strike). It is the inverse of the short put synthetic straddle and an alternative to the long call synthetic straddle (the page notes that, with fairly priced options, call vs put variant shouldn't differ in profitability).
- **Plain-English:** Same as a long straddle, but built by holding the stock and buying two puts at the strike instead of a call+put pair. The long stock plus one put acts like a call. You profit from a big move in either direction, risk only the upfront cost, and it avoids short selling.

---

## 3. Short Call Synthetic Straddle

- **Strategy name / alternates:** Short Call Synthetic Straddle. Call variant of the synthetic short straddle; inverse of the long call synthetic straddle.
- **Core idea / construction (per macroption):** Replicates a short straddle but replaces the short put with a synthetic short put (long underlying + short call). Math given on page: Short straddle = short call + short put; Synthetic short put = long underlying + short call; therefore **Short call synthetic straddle = long underlying + 2× short call**. Setup: long underlying + short call at double size. Page example: stock, buy 100 shares, sell 2 contracts of 65-strike calls (replicates a 65-strike short straddle). Two legs.
- **When to use:** Not stated on page. Derived/general: when you expect the underlying to stay range-bound near the strike (premium-collection view) and want to build the short straddle from stock + short calls (e.g., against existing long stock — resembles an over-written covered position).
- **Market outlook (volatility view):** Non-directional / short volatility — page classifies it as "non-directional." Best if the underlying sits near the strike at expiration.
- **Pros (derived / general):** Collects option premium; same limited-profit payoff as a short straddle; can be layered onto a long-stock holding.
- **Cons (derived / general):** Unlimited risk on a large up-move and very large risk on a down-move; assignment risk; requires margin.
- **Risk profile:** Unlimited risk, limited profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): limited to the net credit received, realized when the underlying finishes at the strike. Mirrors a short straddle.
- **Maximum loss:** Standard reference (not stated on page): unlimited as the underlying rises far above the strike (large but capped on the downside).
- **Break-even point(s):** Standard reference (not stated on page): strike ± net credit.
- **Replicates:** Short straddle (single strike).
- **Plain-English:** A short straddle in disguise: you hold the stock and sell two calls at the same strike, which behaves like selling a call and a put. You keep the premium if the stock stays put, but you face heavy losses if it moves sharply, especially upward.

---

## 4. Short Put Synthetic Straddle

- **Strategy name / alternates:** Short Put Synthetic Straddle. Put variant of the synthetic short straddle; inverse of the long put synthetic straddle.
- **Core idea / construction (per macroption):** Replicates a short straddle but replaces the short call with a synthetic short call (short underlying + short put). Math given on page: Short straddle = short call + short put; Synthetic short call = short underlying + short put; therefore **Short put synthetic straddle = short underlying + 2× short put**. Page example: sell short 100 shares + sell 2 contracts of 75-strike puts (replicates a 75-strike short straddle). Two legs.
- **When to use:** Not stated on page. Derived/general: when you expect range-bound, low-volatility behavior near the strike and prefer the short-stock construction.
- **Market outlook (volatility view):** Non-directional / short volatility (page: "non-directional").
- **Pros (from page's "Differences" section + general):** Neither put nor call variant is inherently better in profit/risk when options are fairly priced; collects premium; short-stock side produces initial cash inflow.
- **Cons (from page's "Differences" section + general):** Requires short selling the underlying (may be restricted/impossible); short-stock holder pays dividends; unlimited/large risk; margin and assignment risk.
- **Risk profile:** Unlimited risk, limited profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): limited to the net credit received, realized at the strike. Mirrors a short straddle.
- **Maximum loss:** Standard reference (not stated on page): unlimited on a large up-move (large but capped on a down-move).
- **Break-even point(s):** Standard reference (not stated on page): strike ± net credit.
- **Replicates:** Short straddle (single strike). Page notes it is the opposite (inverse) of the synthetic long straddle and the mirror of the short call variant.
- **Plain-English:** Another way to build a short straddle — short the stock and sell two puts at one strike, which together act like a short call plus short put. You pocket the premium if the stock barely moves, but a big move (especially down) can produce large losses.

---

## 5. Long Call Synthetic Strangle

- **Strategy name / alternates:** Long Call Synthetic Strangle. Call variant of the synthetic long strangle.
- **Core idea / construction (per macroption):** Replicates a long strangle using a short underlying position plus two calls at different strikes. The lower-strike put of a normal strangle is replaced by its synthetic equivalent (short stock + long lower-strike call). Page example: stock at $67.55 — sell short the stock, buy the 65-strike call ($4.93), buy the 70-strike call ($2.55); similar to a 65–70 long strangle (long 65 put + long 70 call). Three legs.
- **When to use:** Not stated on page. Derived/general: when you expect a big move either way but want cheaper entry than a straddle (out-of-the-money strikes), built from calls + short stock.
- **Market outlook (volatility view):** Long volatility / non-directional (page: "long volatility"). Needs a large move beyond either strike.
- **Pros (derived / general):** Lower cost than a straddle (wider strikes); unlimited upside, limited loss; lets you create the strangle from calls when puts are less attractive.
- **Cons (derived / general):** Requires short selling the underlying; needs a larger move than a straddle to profit; three legs = more commissions.
- **Risk profile:** Limited loss, unlimited potential profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): effectively unlimited on a large up-move (large but capped on the downside). Mirrors a long strangle.
- **Maximum loss:** Standard reference (not stated on page): limited to the net debit paid; occurs when the underlying finishes between the two strikes.
- **Break-even point(s):** Standard reference (not stated on page): lower strike − net debit and upper strike + net debit.
- **Replicates:** Long strangle (two strikes). If the two calls share the same strike it becomes a long call synthetic straddle.
- **Plain-English:** A long strangle made from two calls at different strikes plus a short stock position, where the short stock + lower call mimic the strangle's put. It costs less than a straddle but needs a bigger move; losses are capped at the amount paid, and the upside is open-ended.

---

## 6. Long Put Synthetic Strangle

- **Strategy name / alternates:** Long Put Synthetic Strangle. Put variant of the synthetic long strangle.
- **Core idea / construction (per macroption):** Replicates a long strangle using a long underlying position plus two puts at different strikes. The higher-strike call of a normal strangle is replaced by a synthetic long call (long stock + long higher-strike put). Page example: stock at $81.25 — buy 100 shares, buy the 80-strike put ($3.72), buy the 85-strike put ($6.57); similar to an 80–85 long strangle (long 80 put + long 85 call). Three legs.
- **When to use:** Not stated on page. Derived/general: when you expect a large move either way, want the wider/cheaper strikes of a strangle, and prefer the long-stock construction (no short selling).
- **Market outlook (volatility view):** Long volatility / non-directional (page: "long volatility").
- **Pros (derived / general):** Avoids short selling (long stock); receives dividends; lower cost than a straddle; limited loss with unlimited upside.
- **Cons (derived / general):** High initial cash outflow to buy the stock; needs a larger move to profit; three legs.
- **Risk profile:** Limited loss, unlimited potential profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): effectively unlimited on a large up-move (large but capped on the downside). Mirrors a long strangle.
- **Maximum loss:** Standard reference (not stated on page): limited to the net debit paid; occurs between the strikes.
- **Break-even point(s):** Standard reference (not stated on page): lower strike − net debit and upper strike + net debit.
- **Replicates:** Long strangle (two strikes). If the two puts share the same strike it becomes a long put synthetic straddle.
- **Plain-English:** A long strangle assembled from owning the stock and buying two puts at different strikes, where the stock + higher-strike put act like the strangle's call. It profits from a big move either way, risks only the premium paid, and skips short selling.

---

## 7. Short Call Synthetic Strangle

- **Strategy name / alternates:** Short Call Synthetic Strangle. Call variant of the synthetic short strangle; inverse of the long call synthetic strangle.
- **Core idea / construction (per macroption):** Replicates a short strangle using a long underlying position plus two short calls at different strikes. The lower-strike put of a normal short strangle is replaced by a synthetic short put (long stock + short lower-strike call). Page example: stock at $74.17 — buy 100 shares, sell the 70-strike call ($6.29), sell the 75-strike call ($3.59); risk profile similar to a 70–75 short strangle (short 70 put + short 75 call). Three legs.
- **When to use:** Not stated on page. Derived/general: when you expect range-bound, low-volatility behavior between the strikes and want to collect premium, built from stock + short calls.
- **Market outlook (volatility view):** Non-directional / short volatility (page: "non-directional"). Best if the underlying stays between the strikes.
- **Pros (derived / general):** Collects premium; wider profit zone than a short straddle (range between strikes); can be layered on long stock.
- **Cons (derived / general):** Unlimited risk on a large up-move, very large risk on a down-move; margin and assignment risk; three legs.
- **Risk profile:** Unlimited risk, limited profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): limited to the net credit received; realized when the underlying finishes between the two strikes. Mirrors a short strangle.
- **Maximum loss:** Standard reference (not stated on page): unlimited on a large up-move (large but capped on the downside).
- **Break-even point(s):** Standard reference (not stated on page): lower strike − net credit and upper strike + net credit.
- **Replicates:** Short strangle (two strikes). If the two calls share the same strike it becomes a short call synthetic straddle.
- **Plain-English:** A short strangle built from holding stock and selling two calls at different strikes, where the stock + lower call mimic the strangle's short put. You keep the premium if the stock stays in a range, but a strong move (up especially) can cause large losses.

---

## 8. Short Put Synthetic Strangle

- **Strategy name / alternates:** Short Put Synthetic Strangle. Put variant of the synthetic short strangle; inverse of the long put synthetic strangle.
- **Core idea / construction (per macroption):** Replicates a short strangle using a short underlying position plus two short puts at different strikes. The higher-strike call of a normal short strangle is replaced by a synthetic short call (short stock + short higher-strike put). Page example: stock at $68.95 — sell short 100 shares, sell the 65-strike put ($1.95), sell the 70-strike put ($4.26); replicates a short strangle with a 65-strike put (unchanged) and a 70-strike call (replaced synthetically). Three legs.
- **When to use:** Not stated on page. Derived/general: when you expect range-bound behavior between the strikes and prefer the short-stock construction for premium collection.
- **Market outlook (volatility view):** Non-directional / short volatility (page: "non-directional").
- **Pros (derived / general):** Collects premium; wider profit range than a short straddle; short-stock side gives initial cash inflow.
- **Cons (derived / general):** Requires short selling the underlying; pays dividends on short stock; unlimited/large risk; margin and assignment risk; three legs.
- **Risk profile:** Unlimited risk, limited profit (stated on page).
- **Maximum profit:** Standard reference (not stated on page): limited to the net credit received; realized between the strikes. Mirrors a short strangle.
- **Maximum loss:** Standard reference (not stated on page): unlimited on a large up-move (large but capped on the downside).
- **Break-even point(s):** Standard reference (not stated on page): lower strike − net credit and upper strike + net credit.
- **Replicates:** Short strangle (two strikes). If the two puts share the same strike it becomes a short put synthetic straddle.
- **Plain-English:** A short strangle created by shorting the stock and selling two puts at different strikes, where the short stock + higher put act like the strangle's short call. You earn the premium while the stock stays in range, but a big move (down especially) can lead to large losses.

---

## 9. Synthetic Covered Strangle

- **Strategy name / alternates:** Synthetic Covered Strangle. Synthetic version of the covered short strangle.
- **Core idea / construction (per macroption):** Replicates a covered short strangle (a short strangle partially hedged by long stock) using **two short put options at different strikes, same expiration**. Reasoning given on page: long underlying + short call = synthetic short put, so the long-stock + short-call portion is collapsed into a short put, leaving two short puts. Page example: stock at $74.53 — sell the 70-strike put ($2.01) and sell the 75-strike put ($4.24). Two legs.
- **When to use:** Not stated as a dedicated section. Derived/general: moderately bullish, income-oriented view — you want premium and are willing to own (be assigned) the stock if it falls. Synthetic form is chosen for the positive initial cash flow.
- **Market outlook (volatility view):** Bullish (page explicitly: "bullish option strategy"). Makes maximum, constant profit above the higher strike.
- **Pros (per page + general):** Positive initial cash flow — you only sell options and don't have to buy the underlying (page: "one advantage … is positive initial cash flow"); simpler than holding stock + multiple options; limited (defined) maximum loss.
- **Cons (per page + general):** Profit is limited; although loss is technically limited it "can be very large if underlying falls a lot"; below the lower strike losses grow at double the rate (both short puts in the money); assignment risk.
- **Risk profile:** Limited loss and limited profit (page), but the maximum loss can be very large on a deep decline.
- **Maximum profit (stated on page):** Equals the initial premium received; reached above the higher strike (both puts expire out of the money). In the example, premium = 2.01 + 4.24 = **$6.25 per share ($625 per contract)**.
- **Maximum loss (stated on page):** `lower strike + higher strike − premium received`. In the example: 70 + 75 − 6.25 = **$138.75 per share** (at zero underlying price). Below the lower strike, losses increase at double rate.
- **Break-even point(s):** Not given explicitly on page. Standard reference (covered short strangle payoff): break-even sits in the declining region around the higher strike where accumulated short-put losses cancel the premium received (roughly `higher strike − premium received` before the lower put goes in the money, steepening once price drops below the lower strike). Labeled standard reference — not stated on macroption page.
- **Important notes / replicates:** Payoff at expiration is identical to the covered short strangle. Profit is constant above the higher strike; between the strikes profit declines as price falls; below the lower strike losses accelerate (double rate) because both short puts are in the money. Page also relates it to synthetic covered call (replicates covered call with a short put) and synthetic covered put.
- **Plain-English:** This turns a "own the stock and sell a strangle" income trade into just selling two puts at different strikes, because owning stock plus a short call is the same as a single short put. You collect premium up front and keep it all if the stock stays high, but if the stock drops a lot you can lose heavily, with losses piling up twice as fast below the lower strike.

---

## Standard-Reference Payoff Cheat Sheet (used for the 8 non-covered pages)

These mirror the classic positions each synthetic replicates; not quoted from the macroption pages.

- **Long straddle (strike K):** max loss = net debit (at K); max profit unlimited up / large down; break-evens K ± net debit.
- **Short straddle (strike K):** max profit = net credit (at K); max loss unlimited up / large down; break-evens K ± net credit.
- **Long strangle (Kput < Kcall):** max loss = net debit (between strikes); max profit unlimited up / large down; break-evens Kput − debit and Kcall + debit.
- **Short strangle (Kput < Kcall):** max profit = net credit (between strikes); max loss unlimited up / large down; break-evens Kput − credit and Kcall + credit.

---

## Open / Clarifying Items

- None of the eight straddle/strangle pages publish explicit max-profit, max-loss, or break-even figures; those fields are standard references. If exact figures are required, they must be computed from the chosen strikes and the net debit/credit of the specific position.
- "When to use" and dedicated "Pros/Cons" sections do not exist on any of the nine pages; items labeled "derived / general" are reasoning-based, not macroption quotes. The long-put and short-put straddle pages' "Differences" sections are the only place macroption supplies explicit trade-offs (short-selling, dividends, cash flow).
- Synthetic covered strangle is the only page with a full payoff section; its break-even is the one payoff field that page does not state explicitly.
