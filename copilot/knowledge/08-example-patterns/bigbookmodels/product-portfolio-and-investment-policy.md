# Pattern card — Product Portfolio and Investment Policy
- **Source:** AnyLogic example model "Product Portfolio and Investment Policy" (bigbookmodels/Multimethod), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid
- **Problem it solves:** Test how the share of revenue reinvested in R&D shapes a portfolio of short-lived products, where finance is aggregate (SD) and each product has its own uncertain lifecycle (agents).

## Structure
- **Finance (SD on Main).** `Revenue = portfolio.AnnualRevenue()` (a population *sum* statistic) splits into
  `InvestedRevenue = Revenue * FractionInvested` → stock `InvestmentCapital` and `MainRevenue` → stock `MainCapital`.
  Outflows: `RnDCost = portfolio.AnnualRnDCost()` from `InvestmentCapital`; `InMarketCost = portfolio.AnnualInMarketCost()`
  from `MainCapital`.
- **Policy.** `FractionInvested = InvestmentCapital > RnDCapacity * AverageProjectCost ? 0 : MaxFraction` — stop
  feeding the fund once it could pay for the full R&D capacity.
- **Project start (Condition event on Main, `StartNewProduct`).** Condition
  `portfolio.NinRnD() < RnDCapacity && InvestmentCapital >= (portfolio.NinRnD() + 1) * AverageProjectCost`;
  action `InvestmentCapital -= ProjectStartCost; add_portfolio(); StartNewProduct.restart();`.
- **Product agent statechart.** `Research` → branch (kill if `SuccessFactor < MinExpectedSuccess`) → `Development` →
  branch (same test) → `InMarket` → Condition `time() - TimeLaunched > IntroductionTime && AnnualRevenue() < DiscontinueThreshold`
  → final state, whose action is `get_Main().remove_portfolio(this)` (also for killed projects). The success factor is
  drawn on leaving Research (`uniform()`) and nudged by `uniform(-0.3, 0.3)` at each later stage.
- **Product economics (agent functions).** Revenue `BaseRevenueCurve(time() - TimeLaunched) * SuccessFactor` in
  `InMarket`, else 0 (table over years 0–10, linear, *Extrapolate*); R&D cost by stage; introduction cost during the
  first `IntroductionTime` after launch.

## Resources
`RnDCapacity` (projects in R&D at once) and the investment fund; no Process Modeling blocks.

## Key settings worth copying
- **Self-limiting creation loop.** After `restart()` the event fires again at the same instant while the fund still
  covers one more project, so it starts as many as the money allows. It stops because each start raises the bar
  (`(N + 1) * AverageProjectCost`) and lowers the fund. Always make the action push its own condition towards false
  before `restart()` (`bigbook/event-modes-condition-monitoring-and-lifecycle.md`).
- **State-dependent cost in one function:**
  `switch (statechart.getActiveSimpleState()) { case Research: return AnnualResearchCost; case Development: return AnnualDevelopmentCost; default: return 0; }`.
  A population *sum* statistic of such functions then feeds the SD flow directly.
- **Sensitivity overlay** (Parameter Variation `SensitivityAnalysis`, `MaxFraction` 0.01…0.40 step 0.01):
  - *Before each experiment run:* `chart0.removeAll();`
  - *After simulation run:* `Color c = lerpColor((getCurrentIteration() - 1) / (double)(getMaximumIterations() - 1), blue, red);`
    then `chart0.addDataSet(root.RevenueDS, format(root.MaxFraction), c, true, Chart.INTERPOLATION_LINEAR, 1, Chart.POINT_NONE);`
    (Help *Plot*: `addDataSet(ds, title, color, drawLine, interpolation, lineWidth, pointStyle)`).
  - `RevenueDS` is an auto-updated dataset on Main (every time unit). One run per value, colour from blue (low) to red
    (high), so the whole family of trajectories reads at a glance.
- **Stage animation for free:** bubble radius `TimeLaunched <= 0 ? 3 : AnnualRevenue()`; `moveTo(getX(), getY() - 100)`
  on approval and `- 120` on launch lift a product into the next lane.

## KPIs instrumented
Revenue over time (`RevenueDS`), the two capital stocks, and products per stage. The overlay chart compares revenue
paths across `MaxFraction`.

## Pitfalls
- **Statistics inside SD formulas and conditions run every solver step** (fixed step 0.001 in this model): `Revenue`,
  both cost flows and the event condition each scan the whole portfolio per step. Fine for dozens of products; for
  thousands, sample into *Constant* variables from a cyclic event (`bigbookmodels/multimethod-interface-catalogue.md`).
- **The time-based `Discontinue` condition works only because Main has SD.** The engine re-tests every armed condition
  per solver step once any SD exists; in a purely discrete copy it would be tested only when the product itself has an
  event, i.e. late or never. Add a cyclic check or a timeout there.
- **One run per value.** The overlay shows single stochastic runs (random seed); use replications before ranking values.
- **Table edge:** *Extrapolate* keeps the declining curve going past year 10; it is harmless here only because
  discontinuation happens first (`bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`).

## Reusable idea
Let agents carry the lumpy, uncertain lifecycles and let SD carry the money: population sums of per-agent functions are
the flows, a condition event on the fund creates agents, and a final state removes them.

## When the co-pilot should use this
- Portfolio, pipeline and fleet-renewal questions: R&D and drug pipelines, product lines, capital projects, equipment
  replacement funded from revenue.
- Any Parameter Variation where the answer is a family of time paths rather than one number.
- Related: `bigbookmodels/statechart-for-product-lifecycle.md`, `sdmodels/`, G11 and G16.
