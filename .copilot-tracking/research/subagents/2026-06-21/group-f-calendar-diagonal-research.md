<!-- markdownlint-disable-file -->
# Group F — Calendar & Diagonal Spreads Research (macroption.com)

Research date: 2026-06-21
Source base: https://www.macroption.com/

## Research Topics / Questions

Extract structured study-note content for 10 calendar/diagonal option strategies from macroption.com. For each: strategy name + alternate names, core idea/legs, when to use, market outlook, pros, cons, risk profile, max profit, max loss, break-even, important notes/variations, and a plain-English explanation.

Strategies:
1. Long Calendar Call Spread — /long-calendar-call-spread/
2. Long Calendar Put Spread — /long-calendar-put-spread/
3. Short Calendar Call Spread — /short-calendar-call-spread/
4. Short Calendar Put Spread — /short-calendar-put-spread/
5. Double Calendar Spread — /double-calendar-spread/
6. Long Diagonal Call Spread — /long-diagonal-call-spread/
7. Long Diagonal Put Spread — /long-diagonal-put-spread/
8. Short Diagonal Call Spread — /short-diagonal-call-spread/
9. Short Diagonal Put Spread — /short-diagonal-put-spread/
10. Double Diagonal Spread — /double-diagonal-spread/

Status: Complete

---

## Sourcing Note & Stub Status (READ FIRST)

All 10 individual strategy pages fetched are **STUB pages**. Each one renders only:

- the page title (e.g., "Long Calendar Call Spread Option Strategy"),
- a payoff-diagram image (an image, so its numbers/shape are not extractable as text), and
- navigation to sibling strategies plus the standard site footer.

None of the 10 stub pages contained extractable body prose stating *when to use*, *pros*, *cons*, *maximum profit*, *maximum loss*, or *break-even*. Three different targeted queries per page returned only navigation boilerplate, confirming the stubs.

**What IS legitimately macroption-sourced** comes from the two category overview pages, which are full articles:

- Calendar Spreads overview: https://www.macroption.com/calendar-spreads/
- Diagonal Spreads overview: https://www.macroption.com/diagonal-spreads/

These give macroption-attributable definitions of the legs, the long-vs-short rule, alternate names, and how calendars/diagonals differ from vertical spreads. Those facts are labeled **"Macroption-stated"** below.

Everything else (market outlook specifics, pros, cons, max profit, max loss, break-even, plain-English) is **NOT** on the macroption stub pages and is filled using established options theory, labeled **"Standard reference (not stated on macroption page)"**. No invented numbers are attributed to macroption.

### Macroption-stated definitions that apply to ALL entries

From the Calendar Spreads overview page:

- A calendar spread = two options of the **same type** (two calls or two puts), **same strike price**, but **different expirations**.
- Alternate names for calendar spreads: **time spreads** or **horizontal spreads** (vs vertical spreads, which have same expiration, different strikes). The "horizontal" name comes from option quote tables: strikes listed in rows (vertically), expirations in columns (horizontally).
- **Long calendar** = long the **longer**-expiration option, short the **shorter**-expiration option (e.g., long June calls, short March calls, same strike).
- **Short calendar** = short the longer-expiration option, long the shorter-expiration option (the inverse).
- Mnemonic (macroption): "the longer expiration option is the same as the entire spread name/direction."
- Vertical vs calendar: both are two options, one long + one short, same type, same underlying. Vertical = same expiration / different strikes; calendar = same strike / different expirations.
- Calendar vs diagonal: in a diagonal, **both** the strikes **and** the expirations differ.

From the Diagonal Spreads overview page:

- A diagonal spread = two options of the same type, same underlying, but with **different strikes AND different expirations**.
- macroption example: buy a 30-strike call expiring June + sell a 35-strike call expiring April.
- **Long diagonal** = long the longer-expiration option, short the shorter-expiration option (long June, short April in the example). **Short diagonal** = the inverse.
- Diagonals "provide far more possible combinations due to the added variable of different strikes"; they "can be bullish or bearish, and they can be short or long volatility." The exact exposure depends on the specific strike/expiration combination.
- The four basic **call** diagonal combinations macroption lists:
  1. Long longer-expiration lower strike + short shorter-expiration higher strike
  2. Long longer-expiration higher strike + short shorter-expiration lower strike
  3. Short longer-expiration lower strike + long shorter-expiration higher strike
  4. Short longer-expiration higher strike + long shorter-expiration lower strike
  (Four analogous combinations exist for puts.)
- Distance matters (macroption): a diagonal with expirations close together but strikes far apart behaves more like a **vertical** spread; a diagonal with similar strikes but a big expiration gap behaves more like a **calendar** spread. "Even a very small difference in strikes or expirations can have significant effect," so generalizations are hard.

### Why these are hard to express with simple formulas (applies to every entry)

Because two expirations are involved, at the near-term option's expiration the remaining (longer-dated) option still has **time value** whose size depends on implied volatility and time left. So the precise max profit and break-even points of any calendar or diagonal cannot be written as a clean closed-form formula the way a vertical spread can — they must be modeled (macroption points users to its Option Strategy Simulator). This caveat is repeated per strategy below.

---

## 1. Long Calendar Call Spread

- **Page:** https://www.macroption.com/long-calendar-call-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** "Calendar Call Spread"; also generically a **time spread** / **horizontal spread**.

**Core idea / legs**

- *Macroption-stated:* a long calendar = long the longer-dated option, short the shorter-dated option, same strike, both calls.
- *Standard reference (not stated on macroption page):* **Sell** the near-term (shorter expiration) call and **buy** the far-term (longer expiration) call at the **same strike** (commonly at-the-money). Done for a **net debit** (the longer-dated call costs more than the premium taken in on the near-dated call).

**When to use** — *Standard reference (not stated on macroption page):* You expect the underlying to sit **near the strike** and stay range-bound through the near-term expiration, and/or you expect **implied volatility to rise**. Often opened ATM for a neutral view.

**Market outlook** — *Standard reference:* **Neutral on direction**, wanting little movement short-term; **long volatility** (positive vega) and **positive time decay** (the short near-term call decays faster than the long far-term call while price stays near the strike).

**Pros** — *Standard reference:*
- Limited, fully defined risk (the net debit).
- Cheaper than buying the longer-dated call outright (the sold near-term call subsidizes it).
- Profits from near-term time decay (positive theta near the strike).
- Benefits if implied volatility increases (positive vega).
- The short leg can be rolled forward at each near-term expiry to keep collecting premium.

**Cons** — *Standard reference:*
- Profit is limited and the profitable zone is **narrow**, centered on the strike.
- Loses if the underlying moves far in **either** direction.
- Hurt by a drop in implied volatility (vega risk).
- Two expirations make the payoff path-dependent and hard to model precisely.
- Early-assignment risk on the short near-term call (especially around dividends).

**Risk profile** — *Standard reference:* **Limited risk, limited reward.**

**Maximum profit** — *Standard reference (not stated on macroption page):* No clean formula (two expirations). Roughly maximized when the underlying is **at the strike at the near-term expiration** — the short call expires near worthless while the long call retains the most time value. The exact amount depends on the far-term call's value then (driven by IV and remaining time).

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid**. Occurs when the underlying moves far from the strike (both calls end deep ITM and behave alike, or both go worthless), so the spread collapses.

**Break-even** — *Standard reference (not stated on macroption page):* **Two** break-even points, one below and one above the strike, bracketing the profitable region at near-term expiration. Exact locations can't be given by a simple formula because the long call's residual value depends on IV/time.

**Important notes / variations** — *Standard reference:* The engine of profit is the **faster time decay of the near-term short leg**. It is a **long-vega** position, so it likes rising IV and dislikes IV crush. Manage/close at or before the near-term expiration; if the short leg is rolled, it becomes a series of calendars.

**Plain-English explanation:** You sell a soon-to-expire call and buy a longer-dated call at the same strike, paying a small net cost. You're betting the stock basically stands still near that strike for a few weeks — the near option you sold melts away faster than the longer one you own, and you keep the difference. Big moves either way, or a drop in volatility, are what hurt you, and the most you can lose is what you paid.

---

## 2. Long Calendar Put Spread

- **Page:** https://www.macroption.com/long-calendar-put-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** "Calendar Put Spread"; generically a **time spread** / **horizontal spread**.

**Core idea / legs**

- *Macroption-stated:* long the longer-dated option, short the shorter-dated option, same strike, both puts.
- *Standard reference (not stated on macroption page):* **Sell** the near-term put and **buy** the far-term put at the **same strike** (commonly ATM), for a **net debit**.

**When to use** — *Standard reference:* Expect the underlying to stay **near the strike / range-bound** through near-term expiry, and/or expect **IV to rise**. Behaves much like the long calendar call; built from puts (sometimes preferred when the chosen strike is below spot or for assignment/dividend reasons).

**Market outlook** — *Standard reference:* **Neutral** on direction, **long volatility** (positive vega), **positive time decay** near the strike.

**Pros** — *Standard reference:*
- Limited, defined risk (net debit).
- Cheaper than buying the long-dated put outright.
- Profits from near-term time decay.
- Benefits from rising implied volatility.
- Short leg can be rolled for ongoing premium.

**Cons** — *Standard reference:*
- Limited profit; **narrow** profit zone around the strike.
- Loses on a large move in either direction.
- Hurt by falling implied volatility.
- Two-expiration complexity; path dependence.
- Early-assignment risk on the short near-term put.

**Risk profile** — *Standard reference:* **Limited risk, limited reward.**

**Maximum profit** — *Standard reference (not stated on macroption page):* No simple formula; roughly maximized with the underlying **at the strike at near-term expiration**; exact value depends on the far-term put's remaining time value.

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid**; occurs on a large move away from the strike in either direction.

**Break-even** — *Standard reference (not stated on macroption page):* **Two** break-even points bracketing the strike; exact locations depend on IV/time and can't be expressed simply.

**Important notes / variations** — *Standard reference:* Functionally near-identical to the long calendar call (put-call structure differs, profile is the same neutral, long-vega, positive-theta tent). Watch IV (vega risk) and manage around near-term expiry.

**Plain-English explanation:** Same idea as the call calendar but using puts: sell a near-term put, buy a longer-dated put at the same strike for a small debit. You profit if the stock hovers near the strike and/or volatility climbs, because the put you sold decays faster than the one you own. Your loss is capped at the debit, and large moves in either direction are the enemy.

---

## 3. Short Calendar Call Spread

- **Page:** https://www.macroption.com/short-calendar-call-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified beyond "short calendar (call) spread."

**Core idea / legs**

- *Macroption-stated:* short the longer-dated option, long the shorter-dated option, same strike, both calls (the inverse of the long calendar call).
- *Standard reference (not stated on macroption page):* **Buy** the near-term call and **sell** the far-term call at the **same strike**, for a **net credit** (the longer-dated call sold is worth more than the near-dated call bought).

**When to use** — *Standard reference:* You expect a **large move in either direction** and/or a **drop in implied volatility** before the near-term expiration (e.g., positioning for a post-event IV crush or a breakout).

**Market outlook** — *Standard reference:* Direction-neutral but wants **movement** (dislikes a pin at the strike); **short volatility** (negative vega — profits when IV falls).

**Pros** — *Standard reference:*
- Opened for a **net credit**.
- Profits if the underlying moves far from the strike (either side).
- Benefits from **falling** implied volatility.

**Cons** — *Standard reference:*
- Reward is limited (roughly the credit received).
- Loses if the underlying **stays near the strike** (worst case at the strike at near expiry).
- Hurt by **rising** implied volatility.
- After the near-term long call expires, the remaining **short longer-dated call is naked** — open-ended upside risk if held that way.
- Two-expiration complexity.

**Risk profile** — *Standard reference:* **Limited reward**; risk is **limited when the spread is closed at/by the near-term expiration** (worst case occurs at the strike), but becomes **theoretically unlimited** if the short far-term call is left naked after the near-term leg expires.

**Maximum profit** — *Standard reference (not stated on macroption page):* About the **net credit received**, approached when the underlying moves far from the strike so the time-value differential between the two calls collapses.

**Maximum loss** — *Standard reference (not stated on macroption page):* Occurs with the underlying **at the strike at near-term expiration** (the mirror of the long calendar's best case); magnitude depends on the far-term call's value there. Limited if closed by near expiry; uncapped if the far leg is left naked.

**Break-even** — *Standard reference (not stated on macroption page):* **Two** break-even points around the strike; the position is profitable **outside** that band (the opposite of the long calendar). No simple formula.

**Important notes / variations** — *Standard reference:* This is the exact inverse of the long calendar call — a **short-vega**, anti-time-decay bet that wants a big move or an IV collapse. The naked-far-leg caveat makes risk management at near-term expiry essential.

**Plain-English explanation:** You flip the normal calendar: buy the near-term call, sell the longer-dated call at the same strike, and collect a credit. You win if the stock makes a big move (either way) or if volatility falls, because that shrinks the value of the longer call you're short. You lose if the stock just sits on the strike, and you must watch the leftover short long-dated call after the near option expires.

---

## 4. Short Calendar Put Spread

- **Page:** https://www.macroption.com/short-calendar-put-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified beyond "short calendar (put) spread."

**Core idea / legs**

- *Macroption-stated:* short the longer-dated option, long the shorter-dated option, same strike, both puts (inverse of the long calendar put).
- *Standard reference (not stated on macroption page):* **Buy** the near-term put and **sell** the far-term put at the **same strike**, for a **net credit**.

**When to use** — *Standard reference:* Expect a **big move in either direction** and/or a **fall in implied volatility** before near-term expiry.

**Market outlook** — *Standard reference:* Direction-neutral but wants **movement**; **short volatility** (negative vega).

**Pros** — *Standard reference:*
- Net **credit** received.
- Profits on a large move either way.
- Benefits from falling implied volatility.

**Cons** — *Standard reference:*
- Limited reward (about the credit).
- Loses if the underlying pins near the strike.
- Hurt by rising IV.
- After the near-term long put expires, the **short longer-dated put is naked** (large downside risk, though bounded because the underlying can't fall below zero).
- Two-expiration complexity.

**Risk profile** — *Standard reference:* **Limited reward**; risk **limited if closed by near-term expiration** (worst case at the strike), but the leftover naked short far put carries large (strike-bounded, not infinite) risk if held.

**Maximum profit** — *Standard reference (not stated on macroption page):* About the **net credit**, approached when the underlying moves far from the strike.

**Maximum loss** — *Standard reference (not stated on macroption page):* At the **strike at near-term expiration**; magnitude depends on the far-term put's value; limited if managed by near expiry.

**Break-even** — *Standard reference (not stated on macroption page):* **Two** points around the strike; profitable **outside** that band. No simple formula.

**Important notes / variations** — *Standard reference:* Inverse of the long calendar put; a short-vega bet wanting movement or IV decline. Because it's built from puts, the naked far-leg risk is large but capped (strike → 0), unlike the call version's unlimited risk.

**Plain-English explanation:** The put version of the short calendar: buy the near-term put, sell the longer-dated put at the same strike, take in a credit. You profit from a big move or a volatility drop and lose if the stock parks on the strike. After the near put expires you're left short a longer-dated put, so it needs watching.

---

## 5. Double Calendar Spread

- **Page:** https://www.macroption.com/double-calendar-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified (listed under Calendar Spreads).

**Core idea / legs**

- *Macroption framing:* a calendar uses same strike / different expirations; a "double" runs **two** calendars at **two different strikes**.
- *Standard reference (not stated on macroption page):* Typically combine a **long calendar put spread at a lower strike** and a **long calendar call spread at a higher strike** — i.e., for each strike, **sell the near-term** option and **buy the far-term** option. Net result is a **net debit**. Strikes are usually placed straddling the current price to create a wide neutral zone.

**When to use** — *Standard reference:* Expect the underlying to stay **within a range** (around/between the two strikes) through near-term expiry, and/or expect **IV to rise** — but you want a **wider** profit zone than a single calendar gives.

**Market outlook** — *Standard reference:* **Neutral / range-bound**, **long volatility** (positive vega), **positive time decay**.

**Pros** — *Standard reference:*
- **Wider profit range** than a single calendar (two peaks, one near each strike).
- Limited, defined risk (net debit).
- Positive theta and positive vega.
- Flexible: strike spacing tunes the width of the neutral zone.

**Cons** — *Standard reference:*
- **Costs more** than a single calendar (two calendars = larger debit).
- Profit still limited; loses if price breaks well outside the strikes.
- Hurt by falling IV (vega risk).
- Four legs across two expirations and two strikes — complex to model and manage.
- Payoff can **dip between** the two strikes (twin-peak shape).

**Risk profile** — *Standard reference:* **Limited risk, limited reward.**

**Maximum profit** — *Standard reference (not stated on macroption page):* No simple formula; tends to peak with the underlying **near one of the two strikes at near-term expiration**; depends on the far-term options' residual values.

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid**; occurs on a large move beyond the strikes in either direction.

**Break-even** — *Standard reference (not stated on macroption page):* Generally **two outer** break-even points (one below the lower strike region, one above the upper strike region); exact locations depend on IV/time. No simple formula.

**Important notes / variations** — *Standard reference:* A double calendar = two single calendars at different strikes, giving a **broader tent** of profitability for a range-bound, long-vega view. Often built with an OTM put calendar + OTM call calendar bracketing spot. Closely related to the **double diagonal** (which uses different strikes on the long legs too).

**Plain-English explanation:** Run two calendar spreads at once — one at a lower strike, one at a higher strike — so your profitable zone is a wide range instead of a single point. You sell the near-term options and buy longer-dated ones at both strikes, paying a net debit that is also your max loss. You profit if the stock stays in the range and/or volatility rises; a breakout beyond the strikes is what costs you.

---

## 6. Long Diagonal Call Spread

- **Page:** https://www.macroption.com/long-diagonal-call-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** "Diagonal Call Spread."

**Core idea / legs**

- *Macroption-stated:* a diagonal uses **different strikes AND different expirations**, both calls; "long" = long the longer-dated option, short the shorter-dated option.
- *Standard reference (not stated on macroption page):* The common bullish build is **buy a longer-dated, lower-strike (often deeper-ITM) call** and **sell a shorter-dated, higher-strike (OTM) call**, for a **net debit**. (This is the structure behind the "poor man's covered call.") Exposure depends on the exact strikes — macroption stresses the combination drives the result.

**When to use** — *Standard reference:* **Mildly bullish**, expecting a gradual rise toward the short strike; you want long-call exposure **cheaper** than buying the longer-dated call outright, and/or you intend to **roll the short call** for recurring income.

**Market outlook** — *Standard reference:* **Neutral-to-bullish** on direction (depends on strikes); generally **positive time decay** (short near-term call decays) and often **long vega** from the longer-dated long call.

**Pros** — *Standard reference:*
- Limited, defined risk (net debit).
- Cheaper than owning the long-dated call outright.
- Collects near-term time decay via the short call.
- Short call can be rolled monthly for income (PMCC-style).
- Generally benefits from rising IV (long vega).

**Cons** — *Standard reference:*
- Profit is **capped** by the short strike for each cycle.
- Two strikes + two expirations make P/L path-dependent and hard to model.
- Early-assignment risk on the short call (watch dividends).
- Loses if the underlying falls materially (debit at risk) or spikes far above the short strike too quickly.

**Risk profile** — *Standard reference:* **Limited risk (net debit), limited reward** (though more directional than a same-strike calendar).

**Maximum profit** — *Standard reference (not stated on macroption page):* No clean formula (two expirations); roughly maximized with the underlying **near the short strike at near-term expiration**; depends on the longer-dated call's value then.

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid**; occurs if the underlying falls far so both calls lose most value.

**Break-even** — *Standard reference (not stated on macroption page):* Depends on the strikes and on the far-term call's value at near-term expiration; **no simple formula** (unlike a vertical).

**Important notes / variations** — *Standard reference:* A diagonal is a **hybrid of a vertical and a calendar** (macroption: close expirations + wide strikes → acts vertical; similar strikes + wide expirations → acts calendar). The popular **"poor man's covered call"** is a long diagonal call spread using a LEAPS-style long call.

**Plain-English explanation:** You buy a longer-dated call and sell a shorter-dated call at a higher strike, paying a net debit. It's a cheaper, leveraged stand-in for a covered call: you lean mildly bullish, collect decay from the call you sold, and can keep selling new near-term calls against your long one. Your loss is capped at the debit, and your upside is capped by the strike you sold.

---

## 7. Long Diagonal Put Spread

- **Page:** https://www.macroption.com/long-diagonal-put-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** "Diagonal Put Spread."

**Core idea / legs**

- *Macroption-stated:* different strikes AND different expirations, both puts; "long" = long the longer-dated option, short the shorter-dated option.
- *Standard reference (not stated on macroption page):* The common bearish build is **buy a longer-dated, higher-strike (often ITM) put** and **sell a shorter-dated, lower-strike (OTM) put**, for a **net debit** (the put-side "poor man's covered put").

**When to use** — *Standard reference:* **Mildly bearish**, expecting a gradual decline toward the short strike; want long-put exposure **cheaper** than an outright longer-dated put, and/or plan to **roll the short put** for income.

**Market outlook** — *Standard reference:* **Neutral-to-bearish** (depends on strikes); generally **positive time decay** and often **long vega**.

**Pros** — *Standard reference:*
- Limited, defined risk (net debit).
- Cheaper than owning the long-dated put outright.
- Collects near-term time decay via the short put.
- Short put can be rolled for recurring income.
- Generally benefits from rising IV (long vega).

**Cons** — *Standard reference:*
- Profit **capped** by the short strike each cycle.
- Two strikes + two expirations → path-dependent, hard to model.
- Early-assignment risk on the short put.
- Loses if the underlying rises materially or crashes far below the short strike too fast.

**Risk profile** — *Standard reference:* **Limited risk (net debit), limited reward.**

**Maximum profit** — *Standard reference (not stated on macroption page):* No simple formula; roughly maximized with the underlying **near the short strike at near-term expiration**; depends on the longer-dated put's value.

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid**; occurs if the underlying rises far so both puts lose most value.

**Break-even** — *Standard reference (not stated on macroption page):* Depends on strikes and the far-term put's value at near expiry; **no simple formula**.

**Important notes / variations** — *Standard reference:* The mirror image of the long diagonal call, oriented for a mildly bearish/range view. Same hybrid vertical-plus-calendar behavior; same "poor man's covered put" application.

**Plain-English explanation:** The bearish twin of the diagonal call: buy a longer-dated put and sell a shorter-dated put at a lower strike for a net debit. You lean mildly bearish, pocket decay from the put you sold, and can roll it for income against your longer put. Loss is limited to the debit; profit is capped by the strike you sold.

---

## 8. Short Diagonal Call Spread

- **Page:** https://www.macroption.com/short-diagonal-call-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified beyond "short diagonal (call) spread."

**Core idea / legs**

- *Macroption-stated:* different strikes AND different expirations, both calls; "short" = short the longer-dated option, long the shorter-dated option (the inverse of the long diagonal call). macroption explicitly lists "short longer-expiration ... + long shorter-expiration" combinations.
- *Standard reference (not stated on macroption page):* **Sell** the longer-dated call and **buy** the shorter-dated call at a different strike, usually for a **net credit**. Exact directional/vol bias depends on which strikes are chosen (macroption: diagonals can be bullish or bearish, short or long vol).

**When to use** — *Standard reference:* Inverse of the long diagonal call — used when you expect **falling implied volatility** and/or a directional move that **erodes the longer-dated call you are short**.

**Market outlook** — *Standard reference:* Depends on strike selection; broadly a **short-volatility** (negative vega) stance, often with a bearish-to-neutral lean.

**Pros** — *Standard reference:*
- Usually opened for a **net credit**.
- Benefits from **falling** implied volatility.
- Profits if the underlying moves in the anticipated direction relative to the strikes.

**Cons** — *Standard reference:*
- Reward is limited.
- **Short the longer-dated call** → once the near-term long call expires/closes, the far call can be **naked, with open-ended (unlimited) upside risk**.
- Hurt by **rising** IV.
- Complex two-strike/two-expiration position.

**Risk profile** — *Standard reference:* **Limited reward; risk can be large/unlimited** because of the short longer-dated call (especially if the protective near-term long leg is gone). More dangerous than the long diagonal.

**Maximum profit** — *Standard reference (not stated on macroption page):* Roughly bounded by the **net credit** plus favorable spread movement; no simple formula given two expirations.

**Maximum loss** — *Standard reference (not stated on macroption page):* Potentially **large/unlimited** from the short far-dated call if the underlying rallies and the long near leg no longer offsets it; no simple formula.

**Break-even** — *Standard reference (not stated on macroption page):* Depends on strikes and the far-term call's value at near expiry; **no simple formula**.

**Important notes / variations** — *Standard reference:* Inverse of the long diagonal call; a **short-vega** structure. The naked-far-call exposure makes risk control essential — many traders define risk by also limiting the strike distance or closing before the near-term leg expires.

**Plain-English explanation:** This reverses the diagonal call: you sell the longer-dated call and buy a shorter-dated one at a different strike, taking in a credit. You're betting volatility falls and/or the stock moves so the long-dated call you're short loses value. The catch is real risk — once the near-term call you own is gone, you're short a naked longer-dated call, so a rally can hurt badly.

---

## 9. Short Diagonal Put Spread

- **Page:** https://www.macroption.com/short-diagonal-put-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified beyond "short diagonal (put) spread."

**Core idea / legs**

- *Macroption-stated:* different strikes AND different expirations, both puts; "short" = short the longer-dated option, long the shorter-dated option (inverse of the long diagonal put).
- *Standard reference (not stated on macroption page):* **Sell** the longer-dated put and **buy** the shorter-dated put at a different strike, usually for a **net credit**. Bias depends on the chosen strikes.

**When to use** — *Standard reference:* Inverse of the long diagonal put — used when you expect **falling implied volatility** and/or a directional move that **erodes the longer-dated put you are short** (often a bullish-to-neutral lean).

**Market outlook** — *Standard reference:* Depends on strikes; broadly **short volatility** (negative vega), frequently bullish-to-neutral.

**Pros** — *Standard reference:*
- Usually opened for a **net credit**.
- Benefits from **falling** implied volatility.
- Profits if the underlying moves favorably relative to the strikes.

**Cons** — *Standard reference:*
- Limited reward.
- **Short the longer-dated put** → after the near-term long put expires/closes, the far put can be **naked**, carrying **large (strike-bounded) downside risk**.
- Hurt by **rising** IV.
- Two-strike/two-expiration complexity.

**Risk profile** — *Standard reference:* **Limited reward; risk can be large** from the short longer-dated put (bounded because the underlying can't fall below zero, unlike the call version's unlimited risk).

**Maximum profit** — *Standard reference (not stated on macroption page):* Roughly bounded by the **net credit** plus favorable movement; no simple formula.

**Maximum loss** — *Standard reference (not stated on macroption page):* Potentially **large** from the short far-dated put if the underlying drops and the long near leg no longer offsets it; bounded by the strike (→ 0), not infinite. No simple formula.

**Break-even** — *Standard reference (not stated on macroption page):* Depends on strikes and the far-term put's value at near expiry; **no simple formula**.

**Important notes / variations** — *Standard reference:* Mirror of the short diagonal call; a **short-vega** structure with a naked-far-put caveat after the near leg expires. Risk is large but capped (strike to zero).

**Plain-English explanation:** The put version of the short diagonal: sell a longer-dated put, buy a shorter-dated put at a different strike, collect a credit. You profit if volatility falls and/or the stock moves so the long-dated put you're short loses value. After the near-term put you own expires, you're left short a longer-dated put, so a sharp drop is the main danger.

---

## 10. Double Diagonal Spread

- **Page:** https://www.macroption.com/double-diagonal-spread/ — **STUB** (title + payoff diagram image + navigation only).
- **Alternate names (Macroption-stated):** none specified (listed under Diagonal Spreads).

**Core idea / legs**

- *Macroption framing:* diagonals use different strikes AND different expirations; a "double" runs a **call diagonal and a put diagonal together** (two diagonals at different strikes).
- *Standard reference (not stated on macroption page):* The standard build = **sell a near-term out-of-the-money strangle** (sell near-term OTM put + sell near-term OTM call) and **buy a longer-dated, wider strangle** (buy far-term further-OTM put + buy far-term further-OTM call). Usually a **net debit**. It resembles an **iron condor whose long wings are pushed out to a later expiration**, giving it positive vega.

**When to use** — *Standard reference:* Expect the underlying to stay **within a range** through near-term expiry, and/or expect **IV to rise**, while wanting a **wider profit tent** than a single or double calendar.

**Market outlook** — *Standard reference:* **Neutral / range-bound**, **long volatility** (positive vega), **positive time decay** from the short near-term strangle.

**Pros** — *Standard reference:*
- **Wide profit zone** (a plateau between the short strikes).
- Collects near-term theta from the short strangle.
- Positive vega — benefits from rising IV.
- Defined/limited risk (net debit) while both expirations are on, since the longer-dated long wings cap the shorts.
- Flexible: strike and expiration spacing tune the tent's width and cost.

**Cons** — *Standard reference:*
- Complex **four-leg, two-expiration, multi-strike** position.
- Profit limited; loses if the underlying breaks out of the range.
- Hurt by falling IV (vega risk).
- After the near-term shorts expire, you're left holding a **longer-dated long strangle** that must be managed/closed.

**Risk profile** — *Standard reference:* **Limited risk, limited reward** (when structured with the long wings further out in strike *and* later in time).

**Maximum profit** — *Standard reference (not stated on macroption page):* No simple formula (two expirations); tends to peak with the underlying **near the short strikes at near-term expiration**; depends on the longer-dated options' residual values.

**Maximum loss** — *Standard reference (not stated on macroption page):* Limited to the **net debit paid** (with the standard wider-long-wings structure); occurs on a large breakout beyond the strikes.

**Break-even** — *Standard reference (not stated on macroption page):* Generally **two outer** break-even points beyond the short strikes, with a profitable plateau between; exact locations depend on IV/time. No simple formula.

**Important notes / variations** — *Standard reference:* Think **iron condor + calendar**: short near-term strangle for income/decay, long longer-dated strangle for protection and positive vega. Closely related to the **double calendar** (the double diagonal differs by using **different strikes** on the long legs, widening the tent). Exact exposures are construction-dependent — macroption emphasizes modeling the specific strikes/expirations.

**Plain-English explanation:** You sell a near-term strangle and buy a wider, longer-dated strangle around it — basically an iron condor whose protective wings expire later. You profit if the stock stays inside a fairly wide range and/or volatility rises, collecting decay from the near options you sold. Your loss is capped at the net debit, and a big breakout beyond your strikes is the main risk.

---

## Field-Coverage Summary

| # | Strategy | Page type | Macroption-sourced fields | Fields filled by standard reference |
|---|----------|-----------|---------------------------|-------------------------------------|
| 1 | Long Calendar Call Spread | Stub | Legs, long/short rule, alt names | Outlook, pros, cons, max P/L, break-even, notes |
| 2 | Long Calendar Put Spread | Stub | Legs, long/short rule, alt names | Outlook, pros, cons, max P/L, break-even, notes |
| 3 | Short Calendar Call Spread | Stub | Legs, long/short rule | Outlook, pros, cons, max P/L, break-even, notes |
| 4 | Short Calendar Put Spread | Stub | Legs, long/short rule | Outlook, pros, cons, max P/L, break-even, notes |
| 5 | Double Calendar Spread | Stub | Category framing only | Construction, outlook, pros, cons, max P/L, break-even, notes |
| 6 | Long Diagonal Call Spread | Stub | Legs, long/short rule, alt names, 4-combo list | Outlook, pros, cons, max P/L, break-even, notes |
| 7 | Long Diagonal Put Spread | Stub | Legs, long/short rule, alt names | Outlook, pros, cons, max P/L, break-even, notes |
| 8 | Short Diagonal Call Spread | Stub | Legs, long/short rule, 4-combo list | Outlook, pros, cons, max P/L, break-even, notes |
| 9 | Short Diagonal Put Spread | Stub | Legs, long/short rule | Outlook, pros, cons, max P/L, break-even, notes |
| 10 | Double Diagonal Spread | Stub | Category framing only | Construction, outlook, pros, cons, max P/L, break-even, notes |

**Strategies captured:** 10 of 10.

**Pages that were stubs:** all 10 individual strategy pages (title + payoff-diagram image + navigation only).

**Pages that were full articles (used for attribution):** the two category overviews — Calendar Spreads and Diagonal Spreads.

**Fields that could NOT be found on the macroption pages (filled via standard reference, clearly labeled):** market outlook specifics, when-to-use, pros, cons, maximum profit, maximum loss, and break-even for every one of the 10 strategies. The macroption stub pages state none of these in extractable text (the payoff diagrams are images).

**Open caveats / clarifying questions:**

- The payoff-diagram images on each stub page likely encode macroption's own profit/loss shape and break-even positions, but they are images and were not text-readable here. If exact macroption-drawn numbers are required, the diagrams would need to be opened/inspected visually (e.g., via the Option Strategy Simulator macroption links to).
- "Long/short diagonal" directional bias is construction-dependent; this document used the most common textbook constructions and flagged them as standard reference. Confirm the intended strike placement if a specific bias is needed.
