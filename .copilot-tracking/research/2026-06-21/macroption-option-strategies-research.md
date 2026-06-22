<!-- markdownlint-disable-file -->
# Task Research: Macroption.com Option Strategies Compilation

Research the website https://www.macroption.com/ thoroughly, extract all option strategy content, and compile a complete, structured Markdown study note covering every strategy with consistent fields (idea, when to use, outlook, pros, cons, risk profile, max profit/loss, break-evens, notes, plain-English summary) plus a comparison summary section.

## Task Implementation Requests

* Research https://www.macroption.com/ and extract all option strategy content available on the site.
* Read through every relevant strategy page.
* Compile a single structured Markdown file with, for each strategy: name, core idea/how it works, when to use, market outlook, pros, cons, risk profile, max profit/max loss, break-even points, important notes/variations/caveats, and a short plain-English explanation.
* Organize with headings/subheadings as a long-term study note; keep writing easy to revisit.
* Add a final summary section comparing strategies broadly: bullish vs bearish vs neutral; limited vs unlimited risk; income vs directional; beginner-friendly vs advanced.
* Save as a single .md file in the specified folder.

## Scope and Success Criteria

* Scope: All option strategy pages published on macroption.com (single-leg, covered, vertical spreads, ratio spreads/backspreads, straddles/strangles, butterflies, condors, calendars/diagonals, synthetics, box). Excludes non-strategy content (calculators, blog posts, Excel tutorials, VIX/volatility theory) unless it clarifies a strategy.
* Assumptions:
  * The user wants a self-contained study reference compiled from macroption.com content, written in plain English.
  * The final deliverable is a single Markdown file; this research document doubles as the compiled study note source.
* Success Criteria:
  * Every macroption.com option strategy page is identified and captured.
  * Each strategy has consistent fields populated (idea, when, outlook, pros, cons, risk, max P/L, break-evens, notes, plain-English).
  * A comparison/summary section groups strategies by direction, risk, purpose, and difficulty.
  * Output is neat, complete, and useful as a future reference.

## Outline

1. Site structure map (list of all strategy URLs)
2. Single-leg strategies (long/short call, long/short put)
3. Covered & protective strategies (covered call, covered put, protective put, collar, married put)
4. Vertical spreads (bull call, bull put, bear call, bear put)
5. Ratio spreads & backspreads
6. Volatility strategies (long/short straddle, long/short strangle, guts)
7. Butterflies (long/short call/put butterfly, iron butterfly)
8. Condors (long/short condor, iron condor)
9. Calendar & diagonal spreads
10. Synthetics & box spread
11. Comparison summary section

## Potential Next Research

* Confirm complete list of strategy pages from macroption.com sitemap/navigation
  * Reasoning: Need authoritative page inventory before deep extraction
  * Reference: https://www.macroption.com/option-strategies/

## Research Executed

### External Research

* Researcher Subagent — site structure mapping (output: .copilot-tracking/research/subagents/2026-06-21/site-structure-research.md)
  * Found 74 distinct individual strategy pages, cross-validated against two authoritative on-site indexes that agree exactly:
    * https://www.macroption.com/all-option-strategies/ (A-Z list)
    * https://www.macroption.com/option-strategies-by-category/ (categorized list)
  * Main hub https://www.macroption.com/option-strategies/ links only to 13 category hub pages; individual strategy pages live one level deeper.
  * `option-strategies-list/` is 404; the real list page is `all-option-strategies/`.

### Complete Strategy Inventory (74 pages, macroption native taxonomy)

* Single Option Positions (4): long-call, long-put, short-call, short-put
* With Underlying / covered-protective (5): covered-call, protective-put, protective-call, covered-put, collar
* Straddles (5): long-straddle, short-straddle, strap, strip, covered-short-straddle
* Strangles (5): long-strangle, short-strangle, long-guts, short-guts, covered-short-strangle
* Butterflies (6): long-call-butterfly, long-put-butterfly, iron-butterfly, short-call-butterfly, short-put-butterfly, reverse-iron-butterfly
* Condors (6): long-call-condor, long-put-condor, iron-condor, short-call-condor, short-put-condor, reverse-iron-condor
* Vertical Spreads (4): bull-call-spread, bear-put-spread, bear-call-spread, bull-put-spread
* Calendar Spreads (5): long-calendar-call-spread, long-calendar-put-spread, short-calendar-call-spread, short-calendar-put-spread, double-calendar-spread
* Diagonal Spreads (5): long-diagonal-call-spread, long-diagonal-put-spread, short-diagonal-call-spread, short-diagonal-put-spread, double-diagonal-spread
* Ratio Spreads / backspreads (4): call-ratio-spread, put-ratio-spread, call-ratio-backspread, put-ratio-backspread
* Ladders (4): bull-call-ladder, bear-put-ladder, bear-call-ladder, bull-put-ladder
* Box Spreads (2): long-box-spread, short-box-spread
* Synthetics (19): long-call-synthetic-straddle, long-call-synthetic-strangle, long-combo, long-put-synthetic-straddle, long-put-synthetic-strangle, short-call-synthetic-straddle, short-call-synthetic-strangle, short-combo, short-put-synthetic-straddle, short-put-synthetic-strangle, synthetic-covered-call, synthetic-covered-put, synthetic-covered-strangle, synthetic-long-call, synthetic-long-put, synthetic-long-stock, synthetic-short-call, synthetic-short-put, synthetic-short-stock

### Scope Decisions (answering subagent questions)

* Capture content for all 74 individual strategy pages; exclude ~30 nav/category/index hub pages.
* Ladders are their own category (4 pages) — included.
* Single-leg `*-payoff/` pages folded into single-leg strategy coverage, not separate.
* Alternate names (e.g., Naked Call = Short Call) noted within each strategy, not counted separately.

## Key Discoveries

### Deliverable

* Compiled study note created at: .copilot-tracking/research/2026-06-21/Option-Strategies-Macroption-Study-Notes.md
* Covers all 74 strategies with consistent fields + a final comparison/summary section.

### Page-type pattern on macroption.com (critical for sourcing)

* macroption pages come in two styles:
  * Full articles — contain Setup, Example, Cash Flow, Payoff, Max Profit/Loss, Break-Even, Greeks. These exist for: Covered Call, Covered Put, Protective Put, Protective Call, Collar; all 4 vertical spreads; all straddles/strangles/guts and their covered variants; Iron Butterfly; Iron Condor; Long Box, Short Box; most synthetic single positions (Synthetic Long/Short Stock, Synthetic Long Call/Put, Synthetic Short Put, Long/Short Combo); Synthetic Covered Strangle.
  * Stub/partial pages — only a one-line classification (direction or volatility + leg count + "limited/unlimited loss/profit") plus a payoff-diagram image. These exist for: the 4 single-leg pages (formulas live on linked `*-payoff/` sub-pages); all 4 ladders (numbers read from worked-example screenshots); 5 of 6 butterflies (all except Iron Butterfly); 5 of 6 condors (all except Iron Condor); all 10 calendar/diagonal pages; the 4 ratio/backspread pages; 2 covered-synthetic pages; 8 synthetic straddle/strangle pages.
* Sourcing rule applied throughout: content taken from a macroption page is treated as authoritative; where a stub page omits payoff math, the deterministic standard formula was supplied and clearly labeled as standard reference (not invented, not mis-attributed to macroption).

### Verified macroption formulas (selected)

* Covered Call: max profit = call strike − initial underlying + call premium; break-even = initial underlying − call premium.
* Collar: break-even = stock price + put premium − call premium; max profit = call strike − initial cost; max loss = initial cost − put strike.
* Protective Put: max loss = put strike − initial underlying − put premium; B/E = initial underlying + put premium.
* Vertical spreads: Bull Call B/E = low strike + net debit; Bull Put B/E = high strike − net credit; Bear Call B/E = low strike + net credit; Bear Put B/E = high strike − net debit.
* Iron Butterfly: max profit = net credit; max loss = wing width − net credit; B/E = middle strike ± net credit.
* Iron Condor: max profit = net credit; max loss = wing width − net credit; B/E = short put strike − credit, short call strike + credit.
* Covered Short Straddle B/E = 0.5 × (strike + stock price − total premium); covered variants lose at double rate below the lower strike.
* Box spread payoff is fixed = distance between strikes (financing/arbitrage, not directional).

### Data-quality flags (carried into study note as cautions)

* Bull Put Spread page: the "When to Trade" sentence reads "moderately decrease, or at least not rise," which contradicts the page's own bullish framing/break-even/summary — treated as a page wording slip; correct reading is bullish.
* Synthetic direction labels on macroption appear reversed vs standard theory: Synthetic Short Put labeled "bearish", Synthetic Covered Call "bearish", Synthetic Covered Put "bullish." Standard theory: short put = bullish/neutral, short call = bearish/neutral. Study note uses standard-theory direction and notes the discrepancy.
* Iron Butterfly example: long 45 put printed as "$121" — appears to be a typo for $112.
* Iron Condor example: call wing printed as "(60-65)" though example call strikes are 55/60 (wing width 5).

## Technical Scenarios

### Handling stub pages with missing payoff math

Requirements: Produce a complete study note where every strategy has max profit/loss and break-even, even though ~40 of 74 macroption pages omit the formulas.

Preferred Approach: For stub pages, fill payoff math with the standard, deterministic option formula for that structure and clearly label it as standard reference (distinct from macroption-stated content). Rationale: butterfly/condor/ladder/spread payoff math is universal and deterministic; leaving fields blank would make the note far less useful, while fabricating macroption attribution would be inaccurate. This keeps the note both complete and honest.

Considered Alternatives:
* Leave stub-page fields as "not specified" — rejected: produces an incomplete study note that fails the user's "complete, useful reference" goal.
* Pull every `*-payoff/` sub-page for the stubs — partially viable but high-volume; the deterministic formulas are already known and were used instead, with sub-page pulls noted as optional follow-up.

### Direction-label discrepancies on synthetics

Requirements: Present correct, teachable market-outlook tags for synthetic positions.

Preferred Approach: Use standard option-theory direction (short put = bullish/neutral; short call = bearish/neutral) and add a one-line caution that macroption's pages label some of these differently. Rationale: the study note must teach correct intuition; the discrepancy is documented for transparency.
