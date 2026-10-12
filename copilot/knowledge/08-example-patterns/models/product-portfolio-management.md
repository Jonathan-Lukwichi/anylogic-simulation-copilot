# Pattern card — Product Portfolio Management
- **Source:** AnyLogic example model "Product Portfolio Management" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Test R&D portfolio policies (share of revenue reinvested, kill threshold, how often new candidates arrive) when projects are funded and killed on **estimates** that differ from what each product really costs and earns.

## Structure
- **Agents:** `Firm` (embedded in Main), a population of `Product` agents inside the firm, and two `ProductType`
  agents that hold distributions and predictability levels.
- **Product lifecycle statechart:** candidate (front end) → *development* (message "Start development") →
  *in market* → *dead* at end of life, with a *killed* exit (message "Kill") from candidate or development.
  Entry actions time-stamp each stage.
- **True vs estimated attributes.** On creation a product draws its **true** values from its type:
  - development time, monthly development cost, market life, monthly sales.

  It then draws an **estimate** of each, uniform within ±(1 − predictability) × true value (floored at 0).
  Predictability 1 = exact; 0.7 = ±30 %. Type A is exact on time and life but ±30 % on cost and sales; Type B is ±30 %
  on everything.
- **Monthly cycle (a cyclic event on the firm):**
  1. Estimate each candidate's and each in-development product's ROI and send "Kill" to those below the threshold.
  2. Collect this month's sales from products in market. Put a fixed share into the R&D budget; the rest counts as
     revenue.
  3. Pay the monthly cost of products already in development, oldest first, while the budget covers it.
  4. Start new developments, highest estimated ROI first, while the budget allows.
- **Candidates** arrive by a second event at a set frequency. A button can inject external R&D money.
- **ROI** is the ratio of discounted inflows to discounted outflows over the product's (estimated) timeline, with a
  per-period discount rate on Main. For a product in development it uses what was really spent plus the estimated
  remainder.

## Resources
n/a — the R&D budget is the constraint.

## Key settings worth copying
- Firm defaults on Main: `fracOfRevenueToRDBudget = 0.3`, `minROINotToBeKilled = 1.4` (discounted inflows at least 1.4×
  discounted outflows), initial budget 0, 5 products already in market at start (pushed through the statechart with
  `fireEvent`).
- Product type distributions (per month): development time `uniform(4, 7)`, development cost
  `uniform(4000, 7000)`, life `uniform(15, 20)`, sales `uniform(3400, 5000)`.
- `Product` lives inside `Firm`, not Main. It keeps its own reference to the top-level agent (a cast of
  `getEngine().getRoot()`). The documented Agent API alternatives are `getRootAgent()` and `getOwner()` (Help 8.9.10
  `anylogic/agentbased/agent-api.html`).
- Time unit months; fixed seed.

## KPIs instrumented
- Counters: developments started, market launches, kills at candidate stage, kills in development, products retired.
- Totals: revenue, R&D spend, external investment. Lagged copies are kept for month-on-month deltas.
- Histograms per product type: estimated NPV of killed products, and lifetime revenue of retired products.
- Bubble charts drawn by code: development (estimated ROI vs start time), market, retired, killed and candidate pools.

## Pitfalls
- **Decisions must read the estimates and outcomes the truths.** If both use the same value, the model cannot show
  the cost of poor forecasting, which is one of its main lessons.
- Uniform noise that is symmetric around the truth yields estimates that are right on average. Real R&D estimates
  are often optimistic; shift the band if you have evidence of bias *(judgement)*.
- Kill rules applied every month to noisy estimates can kill a good project on one bad draw. Here the estimate is
  drawn once per product; if you re-draw it each month, add hysteresis or require several failing reviews.

## Reusable idea
For any stage-gate decision (R&D, capital projects, maintenance deferral, supplier approval), give each agent a
**true** attribute set and an **estimated** one controlled by a predictability parameter. Let the policy act on the
estimates and score outcomes on the truths. Sweeping predictability then puts a value on better information, while
sweeping the reinvestment share and the kill threshold gives the policy frontier.

## When the co-pilot should use this
- R&D or project portfolio questions: funding order, kill thresholds, budget rules, value of better forecasts.
- Any ABM where agents decide on imperfect information and the analyst must separate perceived from actual values.
- As an example of a monthly management cycle written as one cyclic event over a population filtered by statechart
  state.
