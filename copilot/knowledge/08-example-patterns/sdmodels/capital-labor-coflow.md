# Pattern card — Capital Labor Coflow
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Shows how a coflow structure tracks an attribute (labor requirements) through a stock (capital) so that the attribute ages and exits together with the physical stock rather than lagging behind it.

## Block chain
Two parallel stock-and-flow chains run in lockstep. The first tracks the physical quantity: capital enters via `CapitalAcquisition`, accumulates in `CapitalStock`, and drains through `CapitalDiscards` at a first-order rate (stock ÷ average life). The second chain is the coflow: `LaborRequirements` (a stock) rises with each capital addition — scaled by `LaborRequirementsOfNewCapital` — and falls with each discard, carrying the embedded labor attribute out of the system at the same fractional rate as the capital it belongs to. An auxiliary `AverageLaborRequirements` divides the coflow stock by `CapitalStock` to recover the average attribute per unit at any point in time. A suite of exogenous test inputs (step, ramp, pulse, sine, pink noise) drives `ExogenousCapitalAcquisitionRate` so modelers can stress-test the coflow dynamics.

## Resources
- `CapitalStock` — stock initialized to `CapitalAcquisition × AverageLifeOfCapital` (steady-state)
- `LaborRequirements` — coflow stock initialized to `CapitalStock × LaborRequirementsOfNewCapital`
- `AverageLifeOfCapital` — parameter set to 20 years
- `LaborRequirementsOfNewCapital` — average workers needed per new capital unit (exogenous parameter)

## Key settings worth copying
- Time unit: Day (Vensim-imported model; internal rates expressed per year converted accordingly)
- Discard flow formula: `CapitalStock / AverageLifeOfCapital` — standard first-order decay
- Coflow inflow: `CapitalAcquisition × LaborRequirementsOfNewCapital`
- Coflow outflow mirrors physical outflow fractionally: `LaborRequirements / AverageLifeOfCapital`
- Pink noise generated via first-order exponential smoothing of `uniform()` white noise, with a user-set correlation time constant — reusable for any realistic demand driver
- Multiple switchable test inputs (step, ramp, pulse, sine, pink noise) controlled by a single `Input` multiplier on `InitialCapitalAcquisitionRate`

## KPIs instrumented
- `CapitalStock` over time (physical accumulation)
- `LaborRequirements` over time (attribute accumulation)
- `AverageLaborRequirements` = `LaborRequirements / CapitalStock` (derived average attribute)
- `WorkersNeeded` — total workforce implied by current capital stock

## Reusable idea
The coflow pattern: whenever you need to track an average attribute (age, quality, cost, embodied labor) of a heterogeneous stock, build a parallel stock that accumulates `inflow × attribute_of_new_units` and drains at the same fractional rate as the physical stock. Dividing the attribute stock by the physical stock always gives the current average — no agent-level bookkeeping required.
