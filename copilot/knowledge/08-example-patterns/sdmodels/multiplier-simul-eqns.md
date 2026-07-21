# Pattern card — Multiplier Simul Eqns
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models the Keynesian multiplier effect in a macroeconomy, showing how GDP responds dynamically to a step change in government expenditure when consumers form expectations gradually.

## Block chain
Two stock-and-flow loops run in tandem:

1. **GDP adjustment loop** — GDP (stock) is pulled toward AggregateDemand through a first-order smoothing flow (ChangeInGDP), with a ProductionAdjustmentTime of 1 day/year representing how quickly output catches up to demand.
2. **Expected-income adjustment loop** — ExpectedIncome (stock) converges toward actual GDP via ChangeInExpectedIncome, smoothed over ExpectationFormationTime (2 periods). This creates an adaptive-expectations sub-loop.

Auxiliary variables wire the loops together:
- AggregateDemand = Consumption + Investment + GovernmentExpenditure
- Consumption = MarginalPropensityToConsume × ExpectedIncome

GovernmentExpenditure is exogenous and delivers a step shock: `90 + step(10, 1)` — baseline 90 units jumping to 100 at time 1.
Investment is a fixed exogenous constant (10 units).

Both stocks are initialized to simultaneous equilibrium values (GDP and ExpectedIncome both start equal to AggregateDemand), illustrating how to resolve circular initial-value dependencies in SD.

## Resources
n/a — pure stock/flow/auxiliary SD model; no agent populations or resource pools.

## Key settings worth copying
- **ModelTimeUnit:** Day
- **ProductionAdjustmentTime:** 1 (first-order delay, output → demand)
- **ExpectationFormationTime:** 2 (first-order delay, expected income → actual GDP)
- **MarginalPropensityToConsume:** 0.8
- **GovernmentExpenditure formula:** `90 + step(10, 1)` — clean way to inject a permanent policy shock at t=1
- **Stock initial values set to AggregateDemand** — both stocks initialized to the same equilibrium value to avoid a transient at t=0; this is the "simultaneous equations" trick referenced in the model title
- Converted from Vensim MULTIPLI.MDL via AnyLogic import; all variable names preserved from the original Sterman textbook example

## KPIs instrumented
- GDP trajectory over time (response to step shock)
- ExpectedIncome trajectory (lagged convergence)
- AggregateDemand (shows multiplier amplification)
- Implied multiplier = 1 / (1 − MarginalPropensityToConsume) = 5 at steady state

## Reusable idea
**Simultaneous stock initialization to break circularity:** when two stocks reference each other in their initial conditions (GDP initializes to AggregateDemand, which depends on ExpectedIncome, which initializes to GDP), set both initial values to a single shared equilibrium expression. AnyLogic resolves the algebraic loop at t=0 automatically, letting you start in steady state and study only the dynamics of the shock — not an artificial start-up transient. This pattern applies to any SD model with mutually-dependent stocks.
