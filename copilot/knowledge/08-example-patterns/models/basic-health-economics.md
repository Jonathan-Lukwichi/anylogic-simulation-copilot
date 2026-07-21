# Pattern card — Basic Health Economics
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Evaluate the lifetime cost and quality-of-life impact of diabetes prevention interventions by combining individual disease progression with aggregate cost accumulation.

## Block chain
A population of Person agents each carry a statechart with five health states: Normoglycemic → Prediabetic → Type2Diabetes → ESRD (end-stage renal disease) → Transplant, plus mortality exits from every state. Transition triggers are rate-based hazards (annual probabilities), with an optional prevention hazard (PrediabeticPreventionHazard) that can push pre-diabetics back to normoglycemic — representing a lifestyle intervention. Each agent holds two scalar attributes: QoL (quality-of-life weight, 0–1) and CostsPerYear (annual health-service cost for their current state). The SD layer polls the agent population every time step through aggregator functions (totalQoL, newCostsPerYear, countOf* per state) and feeds those values into stock-and-flow accumulators for life-years, QALYs, undiscounted costs, and discounted costs. A DiscountFactor auxiliary (exp(−DiscountRate × time())) multiplies the raw cost flow before it enters the discounted stock, producing time-value-adjusted totals automatically. Intervention costs (per-capita screening + lifestyle programme) are modelled as separate SD flows so their incremental cost against the baseline can be read directly off the stocks.

## Resources
- Agent population: configurable cohort of Person agents (no fixed capacity constraint — this is a health-economics cohort model, not a queuing model)
- No ResourcePool or Seize/Release blocks; disease states replace service capacity as the binding constraint

## Key settings worth copying
- Time unit: Year (critical — all rates and costs are annual)
- Discount rate: 0.03 default (adjustable to 0.01 in the comparison experiment); applied as a continuous exponential decay factor
- State transition triggers: `rate` type on each statechart transition; values are annual hazard rates (e.g., pre-diabetic reversion rate 0.25/year with intervention)
- Intervention parameters exposed as sliders: PerNonDiabeticCapitaInterventionScreeningCostsPerYear, CostsPerPrediabeticLifestyleInterventionCostsPerYear
- SD flows read agent aggregates each step: `population.totalQoL()`, `population.newCostsPerYear()`, `population.countOfPrediabetics()`, etc.

## KPIs instrumented
- AccumulatedUndiscountedCosts (stock) — lifetime nominal expenditure
- AccumulatedDiscountedCosts (stock) — net-present-value expenditure
- AccumulatedLifeYears (stock) — total person-years survived
- AccumulatedQALYs (stock) — quality-adjusted life-years
- State headcounts per simulation step (Normoglycemic, Prediabetic, Type2Diabetes, ESRD, Transplant)
- Incremental cost-effectiveness ratio derivable by comparing baseline vs. intervention experiment outputs

## Reusable idea
Attach lightweight scalar attributes (QoL, CostsPerYear) to each agent that reflect the agent's current statechart state, then let the SD layer continuously aggregate those scalars into running stock accumulators — this decouples individual stochastic progression from economic bookkeeping and makes it trivial to add discounting, sensitivity analysis, or new intervention arms without touching the agent logic.
