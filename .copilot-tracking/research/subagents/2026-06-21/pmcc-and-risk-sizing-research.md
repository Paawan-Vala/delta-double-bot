<!-- markdownlint-disable-file -->
# Research: Poor Man's Covered Call (PMCC) / Diagonal Spreads & Risk Management + Position Sizing

> EDUCATIONAL RESEARCH ONLY — NOT FINANCIAL ADVICE. Audience: small-capital, beginner-to-intermediate
> options trader seeking directional monthly income with strictly limited (hedged) risk. Any return or
> probability figures are ILLUSTRATIVE and attributed; no return statistics are fabricated.

## Research Topics / Questions

### Part 1 — Poor Man's Covered Call (PMCC = Long Diagonal Call Spread) and bearish twin (Long Diagonal Put Spread)
- Construction: buy deep-ITM longer-dated (LEAPS-style) call, sell near-term OTM call; roll short call monthly.
- Capital efficiency vs real covered call (LEAPS vs 100 shares) — concrete dollar comparison.
- How monthly income is generated (rolling the short call); how max loss is limited (~net debit).
- Capital requirement; ideal long-call delta (0.80+), short-call delta (~0.30), DTE choices.
- Pros, cons, main risks (long call still loses if stock falls; assignment; upside cap; calendar/IV effects).
- When PMCC suits a small account vs when a simple vertical spread is better.
- Put-side equivalent (Long Diagonal Put Spread) for a bearish view.

### Part 2 — Risk Management & Position Sizing for a small defined-risk options account
- Risk-per-trade rules of thumb (1–5% of account; cap % of buying power in one underlying).
- Why defined-risk only (no naked) matters for a small account.
- Underlying selection: liquid, optionable, tight bid/ask (SPY/QQQ/IWM, large-caps); avoid illiquid options; earnings.
- Diversification across underlyings/directions; number of concurrent positions for a small account.
- Realistic monthly return expectations + honest caveats (capped-but-large losses, sequence-of-losses, fees drag, assignment, over-leverage).

## Status: COMPLETE

All Part 1 and Part 2 questions answered with attributed evidence. Primary sources fully captured:
macroption.com (diagonal/calendar definitions), tastylive (PMCC, poor man's covered put, diagonal spread,
position sizing, best stocks/liquidity), and Investopedia (1% rule, 2% rule, position sizing). Fidelity and
OIC/optionseducation.org strategy pages were not extractable (see Open Items) but coverage from the other
reputable sources is complete. Return figures are labeled ILLUSTRATIVE and attributed; none are fabricated.

---

## Part 1 — PMCC / Diagonal Spreads

### 1.1 What a PMCC is (definition)

- A **Poor Man's Covered Call (PMCC) is a long call diagonal debit spread used to replicate a covered call
  position** — verbatim framing from tastylive. (tastylive, Poor Man's Covered Call)
- A traditional covered call uses **long stock** to "cover" the short call; a PMCC substitutes a **long-term
  (LEAPS-style) call** for the stock. That is why it is "a more capital-efficient way to simulate the covered
  call strategy without actually owning the stock." (tastylive)
- Directional assumption: **neutral-to-bullish**. Ideal implied-volatility environment: **low**. (tastylive)
- Definitional backbone (macroption): a **diagonal spread** = two options of the **same type** (both calls or
  both puts), **same underlying**, but **different strikes AND different expirations** — distinct from
  calendar spreads (same strike, different expiration) and vertical spreads (same expiration, different
  strike). A **long** diagonal is long the **longer-dated** option and short the **shorter-dated** option.
  The PMCC is macroption's "Long longer-expiration LOWER strike + short shorter-expiration HIGHER strike"
  call combination. (macroption, Diagonal Spreads)

### 1.2 Construction (legs, deltas, DTE)

- **Leg 1 — Buy** a back-month, **deep in-the-money (ITM) call** (often a LEAP) with an expiration "several
  months to years out … high delta, so that the price of the call will move closely with the underlying."
  (tastylive)
- **Leg 2 — Sell** a near-term **out-of-the-money (OTM) call**, "typically 30 to 60 days out," strike above
  the current price. (tastylive)
- **DTE choices:** short call ~**30–60 DTE** (monthly income cadence); long call **months-to-years** (LEAPS).
  (tastylive)
- **Delta guidance:** tastylive specifies the long call should be **deep ITM with a high delta** (so it tracks
  the stock ~1:1) but does **not** name an exact number. The specific figures in your brief — **long delta
  ≈ 0.80+** and **short delta ≈ 0.30** — are **widely used practitioner conventions**, consistent with
  tastylive's "deep ITM / high delta long, OTM short" principle. **Label these specific deltas as
  illustrative conventions**, not a macroption/tastylive-stated number.

### 1.3 Capital efficiency vs a real covered call — concrete dollar comparison

Built directly from tastylive's own worked example (XYZ at **$100**):

| Item | Traditional Covered Call | Poor Man's Covered Call (PMCC) |
| --- | --- | --- |
| "Coverage" leg | Buy **100 shares** = **$10,000** | Buy **$90 LEAP call @ $15.00** = **$1,500** |
| Income leg | Sell 30-day $105 call @ $2.00 = **+$200** | Sell 30-day $105 call @ $2.00 = **+$200** |
| **Net capital outlay** | **~$9,800** ($10,000 − $200) | **$1,300 net debit** ($1,500 − $200) |
| **Max loss (stock → $0)** | **~$9,800** | **$1,300** (the net debit) |

- The long LEAP costs **$1,500 vs $10,000 for 100 shares — about 85% less capital**; on a net-debit basis the
  PMCC ties up **$1,300 vs ~$9,800 (~87% less)**. (Figures derived from the tastylive example; treat as
  ILLUSTRATIVE.)
- tastylive's summary: the PMCC "mimics the dynamics of the covered call strategy but **at a fraction of the
  capital requirement**." For a small account it can "replicate a covered call position with **much less
  capital and much less risk** than an actual covered call." (tastylive)

### 1.4 How monthly income is generated (rolling the short call)

- Each cycle you **sell a near-term OTM call** and collect **extrinsic (time) premium**. "Ideally, the short
  call option will expire worthless, allowing the … trader to collect and retain the option's premium, while
  the underlying stock's price gradually rises, boosting the value of the long back-month call." (tastylive)
- After the short expires/decays, **sell another near-term call** against the same LEAP → repeatable monthly
  income that **reduces the cost basis** of the long call over time. (tastylive, diagonal spread page:
  "reducing cost basis aggressively by selling a near-term option against … the further-dated long option.")
- **Management when wrong:** if the stock drops, "the short call can be **rolled to a lower strike to collect
  more credit**," reducing overall risk. When the trade works, tastylive closes diagonals at **25–50% of max
  profit**. (tastylive)

### 1.5 Max loss / max profit / breakeven (formulas + worked numbers)

- **Max loss ≈ the net debit.** "Maximum Loss = Cost of Long Call − Premium Received from Short Call." In the
  example: ($15.00 − $2.00) × 100 = **$1,300**. Worst case = the long call value goes to zero. (tastylive)
- **Max profit (estimate) = Width of Call Strikes − Net Debit Paid** (plus any residual extrinsic value left
  in the long call at the short's expiration). Example: (105 − 90 − 15 + 2) × 100 = **$200**, realized if XYZ
  sits right at the $105 short strike at expiration. (tastylive)
- **Breakeven (estimate) = Long Call Strike + Net Debit Paid.** (tastylive)
- Caveat: exact max profit/breakeven **cannot be precisely calculated** because the two legs are in different
  expiration cycles and the long retains extrinsic value. (tastylive)

### 1.6 tastylive setup rules (important risk guardrails)

- **Collect enough premium:** ensure the **near-term short premium ≥ the extrinsic value of the long ITM
  option**. "The deeper ITM our long option is, the easier this setup is to obtain." (tastylive)
- **Debit cap:** "ensure that the total debit paid is **not more than 75% of the width of the strikes**" (the
  diagonal page also states the broader rule: keep total debit **under the spread width** so a deep-ITM move
  still pays out). (tastylive)
- **Avoid volatility products:** "We never route poor man's covered calls in volatility instruments. Each
  expiration acts as its own underlying, so our max loss is not defined." (i.e., it behaves cleanly only on
  normal equities/ETFs.) (tastylive)

### 1.7 Pros, cons, and main risks

- **Pros:** far less capital than a covered call; **defined-risk** debit trade (max loss ≈ net debit);
  repeatable monthly income; LEAP gives a long runway for the thesis to play out. (tastylive)
- **Cons / risks:**
  - **Direction risk:** "The most significant risk … is if the underlying stock declines in value." The
    premium collected "might not be enough to offset a significant drop in the stock … and the long call you
    own." The long call still loses value as the stock falls. (tastylive)
  - **Capped upside (opportunity loss):** gains above the short strike are forfeited; if the stock rallies
    far past the short strike, profit actually **trails off** because the long call sheds extrinsic value as
    it goes deeper ITM. (tastylive, diagonal page)
  - **Assignment / early exercise:** the short call can be assigned early (esp. around dividends). Because you
    don't own shares, you handle it by **exercising the deep-ITM LEAP** to deliver shares, or **buying 100
    shares and selling the long call** to close. (tastylive)
  - **Calendar / IV effects:** each expiration "acts as its own underlying"; a sharp favorable move *too fast*
    with a poor setup can lose money, and IV shifts affect the legs differently (long vega in the back month,
    short vega in the front). (tastylive)

### 1.8 When PMCC suits a small account vs when a simple vertical is better

- A **long diagonal "is nothing more than a vertical spread with a longer-term long option."** Max profit can
  **exceed the strike width** because the short expires first, leaving extrinsic value in the long. (tastylive)
- **PMCC/diagonal is better when:** you want a **longer runway** for a directional thesis and **repeatable
  monthly income** by re-selling the front-month option against one back-month long; you accept a **larger
  upfront debit** in exchange for **more time** and the ability to roll. (tastylive, diagonal vs vertical)
- **A simple vertical (bull call / bear put) debit spread is better when:** you want the **cheapest, simplest,
  fully defined-risk** directional bet for a **single move/timeframe**, with no roll management and no
  early-assignment juggling — both legs expire together, so there's no calendar/extrinsic mismatch. (Vertical
  = same expiration, different strikes — macroption.) For the smallest accounts, a narrow vertical can have a
  **lower absolute dollar risk** than even a PMCC's net debit.

### 1.9 Put-side equivalent (bearish): Long Diagonal Put Spread / "Poor Man's Covered Put"

- **Structure:** **Buy** a longer-dated **ATM/ITM put** (often a LEAPS put) as a substitute for **shorting
  the stock**, and **sell** a near-term **OTM put** against it for income. The long put strike is typically
  **higher** than the short put strike. (tastylive, Poor Man's Covered Put; diagonal page: "Buy ITM/ATM put
  longer-term, sell OTM put near-term — bearish, defined risk.")
- **Why it's efficient:** avoids the capital and margin of **short stock** (a traditional covered put has
  *unlimited* upside risk and heavy margin). The PMCP is **defined-risk: max loss = net debit** (cost of long
  put − premium from short put). (tastylive)
- **Worked example (tastylive):** Buy 1-year **$95 put @ $9.00 = $900**; sell 1-month **$85 put @ $2.00 =
  $200** → **net debit $700 = max loss**. If stock falls below $85, max profit ≥ **$300** + residual extrinsic
  (Width $10 − $7 debit, ×100). **Max profit ≈ Width of Put Strikes − Net Debit;** **Breakeven ≈ Long Put
  Strike − Net Debit.** (tastylive)
- **Use case:** bearish **or** moderately flat/sideways — keep selling near-term puts against the long "anchor"
  put for recurring income while retaining downside exposure. (tastylive)

---

## Part 2 — Risk Management & Position Sizing

### 2.1 Risk-per-trade rules of thumb (attributed)

- **tastylive (Dr. Jim Schultz) — the core sizing rule for this account type:**
  - **Defined-risk strategies: keep each position to 1%–3% of total account value.**
  - Undefined-risk (naked) strategies: 3%–7% of account value.
  - "Nothing can do more damage to your portfolio than trading too large." Position sizing is "non-negotiable."
  - **Small-account nuance:** with **< $20,000**, you'll "likely have to increase the upper end of this range,
    hitting **5%, 6%, 7% or even higher at times**" for defined-risk — because position minimums are lumpy in
    small accounts. With **> $100,000** you can drop **below 1%**. (tastylive, Defined- vs Undefined-Risk
    Position Sizing)
- **Investopedia — the "1% rule":** never **risk** more than **1% of the account on a single trade**. "$10,000
  account → shouldn't **lose** more than $100 on a single trade" (it limits loss, not capital deployed).
  Common for accounts **< $100,000**; some go to **2%**; keep it **below 2%**. (Investopedia, Risk Management
  Techniques)
- **Investopedia — the "2% rule" + sizing math:** "most retail investors risk **no more than 2%** of capital
  on any one trade." Example: **$25,000 account × 2% = $500 max risk per trade**; even **10 consecutive losses
  = only 20%** of capital. **Position size = Account Risk ÷ Trade Risk** (e.g., $500 ÷ $20 per-share stop = 25
  shares). (Investopedia, Position Sizing)
- **Synthesis for a small defined-risk options account:** risk roughly **1–3% of the account per trade** as the
  default; the **net debit of a PMCC/diagonal or vertical *is* the defined max risk**, so size each trade so
  that debit is within your per-trade budget. Accept that a very small account may be forced toward the
  **5–7%** upper bound on individual tickets — which is itself a reason to keep total positions few.

### 2.2 Why DEFINED-RISK only matters for a small account

- **Undefined-risk (naked) requires far more buying power and carries open-ended loss.** tastylive's covered-put
  comparison: a traditional (naked-style) covered put has "**potentially unlimited risk** if the stock price
  rises" and "substantial margin requirements due to … undefined risk." The poor-man's (defined) version caps
  loss at the **net debit**. (tastylive, Poor Man's Covered Put)
- Defined-risk strategies let you **size precisely** (you know max loss before entry) and **let trades be
  managed as intended** without margin calls — tastylive's stated reason small accounts should "**never** put
  yourself in a position where you can't manage the trade … by staying small on order entry." (tastylive)
- A single oversized naked loss can erase many months of income; **sequence-of-losses** math (2% rule example
  above) only works when every trade's loss is **bounded and known**.

### 2.3 Underlying selection (liquidity, tight bid/ask, ETFs vs single stocks, earnings)

- **Trade where the liquidity is.** "Higher liquidity is generally synonymous with a … narrower **bid-ask
  spread** … reduces the cost of trading and allows for smoother executions." Check **volume + open interest**;
  "low, or declining" open interest signals a weak execution environment. (tastylive, Best Stocks for Options
  Trading)
- **Index/large-cap and ETFs first.** tastylive: focusing on well-known index underlyings (S&P 500, Nasdaq,
  Dow) "helps ensure that volume will be robust enough to … enter and exit." ETFs reduce **idiosyncratic
  (single-stock) gap risk**: single stocks "are subject to … stock-specific risks that can trigger
  high-magnitude moves," which hurt short-option legs; an ETF's diversification "theoretically helps buffer it"
  (though both share systematic/market risk). This supports the brief's **SPY / QQQ / IWM** and liquid
  large-caps. (tastylive)
- **Small-account asset selection (tastylive small-account guidance):** for accounts **under $25,000**, prefer
  **cheaper, liquid alternatives — sector ETFs or liquid individual stocks — instead of expensive indices**,
  and **scale via wider strikes rather than more contracts** (illustrative buying-power figure cited for SPY
  ~$9,000). (tastylive, "Small Account Trading: Managing Buying Power Expansion Risk" — episode summary via
  DuckDuckGo result.)
- **Earnings:** options education sources flag earnings as elevated-risk events. Investopedia: before earnings,
  "investors might **halve their position size to cut gap risk**," because stops don't protect against gaps.
  tastylive: diagonals *can* be used to trade earnings deliberately, but only if "comfortable with volatile
  profit or loss numbers." For an income trader, the default is to **avoid holding through earnings unless that
  exposure is intended.** (Investopedia, Position Sizing; tastylive, Diagonal Spread)

### 2.4 Diversification & number of concurrent positions

- **Don't concentrate.** Investopedia: "never putting all your eggs in one basket … diversify across **industry
  sector, market capitalization, and geographic region**." (Investopedia, Risk Management Techniques)
- **Implied position-count math:** if each defined-risk trade is ~1–3% of the account, a diversified book is
  naturally on the order of **a handful of positions** for a small account (the 5–7% small-account bound
  implies even **fewer** concurrent trades). Keep meaningful **cash in reserve** rather than deploying 100%
  (tastylive philosophy emphasizes staying small and keeping dry powder; a commonly cited tastytrade guideline
  is deploying only a **portion** of capital, ~25–50% in premium strategies depending on volatility — attribute
  as a tastytrade guideline summarized via a secondary/community source, not a hard rule).
- **Diversify direction too:** mixing **bullish (call diagonals/PMCC)** and **bearish (put diagonals/PMCP)** and
  different underlyings reduces correlation so one market move doesn't hit every position at once.

### 2.5 Realistic monthly return expectations + honest caveats

- **No reputable source in this research promises a specific monthly return.** Do **not** quote a "X% per month"
  figure as expected. (Honest framing required by the brief.)
- **Illustrative math only (from tastylive's own example):** the PMCC risked **$1,300** to target up to **~$200**
  of *max* profit in one cycle (~**15%** of capital-at-risk) — but **max profit is a single best-case price
  point at expiration, not an expected value.** Most cycles return a **fraction** of that, and losing cycles can
  give back the bulk of the debit. (Derived from tastylive; ILLUSTRATIVE.)
- **Caveats to state plainly:**
  - **Capped-but-occasionally-large losses:** income strategies win often but a bad directional move can cost
    most of the net debit at once; one large loss can wipe out several months of small wins.
  - **Sequence-of-losses risk:** the 2%-rule example (10 losses ≈ 20% drawdown) shows why per-trade risk must
    stay tiny; a clustered losing streak in a small account is survivable only if sizing is disciplined.
  - **Commissions/fees drag:** rolling a short option every month multiplies per-contract fees; on a small
    account this drag is proportionally **large** and erodes net income. (General principle; Investopedia notes
    matching broker to frequent trading.)
  - **Assignment / early exercise:** American-style short calls/puts can be assigned early (esp. around
    dividends), forcing share handling or unwinding the long leg. (tastylive)
  - **Over-leverage danger:** the capital efficiency that makes PMCCs attractive also makes it easy to put on
    **too many** contracts for the account size — the single biggest documented mistake ("nothing can do more
    damage … than trading too large"). (tastylive)
  - **Start small / paper trade first.** "Think carefully, start small, and try simulating some trades on a
    test account before putting your money on the line." (Investopedia)

---

## Small-Account Starter Checklist

1. **Pick liquid underlyings:** index ETFs (SPY/QQQ/IWM) or liquid large-caps; confirm **tight bid/ask + high
   volume/open interest** before entering. (tastylive)
2. **Choose direction & structure:** bullish → **PMCC / long call diagonal**; bearish → **long put diagonal /
   poor man's covered put**; simplest single-move bet → **narrow vertical debit spread**.
3. **Build the PMCC right:** **long = deep-ITM LEAP, high delta (illustrative ≈ 0.80+)**, months-to-years out;
   **short = ~0.30-delta OTM, 30–60 DTE.** (tastylive principle; specific deltas illustrative.)
4. **Apply tastylive guardrails:** **net debit ≤ 75% of strike width**; **short premium ≥ long's extrinsic
   value**; **no volatility products.** (tastylive)
5. **Size it:** risk only **~1–3% of account per trade** (the **net debit is your max loss**); accept that a
   sub-$20k account may be pushed to **5–7%** per ticket — so hold **fewer** positions. (tastylive)
6. **Know max loss = net debit before entry;** know the breakeven (Long Strike + Debit for calls / Long Strike
   − Debit for puts). (tastylive)
7. **Generate income:** roll/re-sell the near-term option monthly; **take profits at 25–50% of max**; roll the
   short toward the money to add credit when wrong. (tastylive)
8. **Diversify** across **sector, market cap, and direction**; keep **cash in reserve** (don't deploy 100%).
   (Investopedia; tastylive)
9. **Avoid holding through earnings** unless intended; consider **halving size** around known events.
   (Investopedia)
10. **Mind the drag & discipline:** account for **per-contract fees** on monthly rolls; **never oversize**;
    **paper trade** the workflow first. (Investopedia; tastylive)

---

## Sources

Primary / definitional:
- macroption.com — Diagonal Spreads: <https://www.macroption.com/diagonal-spreads/> (definition; long vs short;
  four call-diagonal types; "behaves like vertical vs calendar" depending on strike/expiration distance).
- macroption.com — Calendar Spreads: <https://www.macroption.com/calendar-spreads/> (calendar vs vertical vs
  diagonal distinctions).
- macroption.com — Long Diagonal Call Spread: <https://www.macroption.com/long-diagonal-call-spread/> and Long
  Diagonal Put Spread: <https://www.macroption.com/long-diagonal-put-spread/> — NOTE: body content not
  extractable via fetch (nav/chrome only); definitions sourced from the Diagonal Spreads overview page above.

PMCC / diagonal mechanics (tastylive):
- Poor Man's Covered Call: <https://www.tastylive.com/concepts-strategies/poor-man-covered-call> (definition,
  structure, capital efficiency, max profit/loss formulas + worked example, setup rules, assignment, risks).
- Poor Man's Covered Put: <https://www.tastylive.com/concepts-strategies/poor-man-covered-put> (bearish twin;
  structure, net-debit max loss, worked example, breakeven).
- Diagonal Spread: <https://www.tastylive.com/concepts-strategies/diagonal-spread> (long call/put diagonal
  setups, defined-risk, debit ≤ width, management, diagonal vs vertical vs calendar, earnings).
- Best Stocks for Options Trading: <https://www.tastylive.com/concepts-strategies/best-stocks-for-options-trading>
  (liquidity, bid/ask, volume/open interest, ETFs vs single-stock gap risk).
- Position Sizing with Defined-Risk and Undefined-Risk (Dr. Jim Schultz, Jul 15 2024):
  <https://www.tastylive.com/news-insights/Defined-Risk-and-Undefined-Risk-Position-Sizing> (1–3% defined-risk;
  3–7% undefined; small-account upper-bound nuance).
- Small Account Trading: Managing Buying Power Expansion Risk (episode; via DuckDuckGo result):
  <https://www.tastylive.com/shows/tasty-bites/episodes/small-account-trading-managing-buying-power-expansion-risk-06-11-2025>
  (asset selection for < $25k, scale via wider strikes, close at 50%).

Risk management & position sizing (Investopedia):
- Risk Management Techniques for Active Traders:
  <https://www.investopedia.com/articles/trading/09/risk-management.asp> (1% rule; up to 2%; diversify; protective
  puts; start small/simulate).
- Master Position Sizing (term page): <https://www.investopedia.com/terms/p/positionsizing.asp> (2% rule;
  $25k × 2% = $500; 10 losses = 20%; position size = account risk ÷ trade risk; halve size before earnings for
  gap risk).

## Open Items / Clarifying Questions

- **Fidelity / Schwab strategy pages:** the Fidelity diagonal-spread URL redirected to a generic Learning Center
  landing page (no strategy body extracted). If a Fidelity or Schwab citation is specifically required, it
  should be located/confirmed manually (e.g., Fidelity Options Strategy Guide "Diagonal spread with calls").
- **OIC / optionseducation.org:** the OIC diagonal-spread page returned "failed to extract meaningful content"
  (JS-rendered). OIC content was therefore not directly quoted; tastylive + Investopedia + macroption fully
  cover the requested points.
- **Specific deltas (long 0.80+, short ~0.30):** these are presented as **illustrative practitioner
  conventions** consistent with tastylive's qualitative "deep-ITM/high-delta long, OTM short" guidance — no
  fetched source stated those exact delta numbers. Confirm acceptable to label as illustrative.
- **Monthly return %:** intentionally **not** quoted as expected; only an illustrative single-cycle max-profit
  ratio (~15% of capital-at-risk in tastylive's example) is given. Confirm whether a modeled (e.g., backtested)
  return range is wanted — that would require a separate data source, not these education pages.
- **CBOE:** not separately fetched; the requested mechanics/risk conventions were already fully covered. Add CBOE
  only if an exchange-level citation is explicitly needed.
