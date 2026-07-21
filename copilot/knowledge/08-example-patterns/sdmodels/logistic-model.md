# Pattern card — Logistic Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models bounded population growth where a carrying capacity progressively limits an otherwise exponential net birth rate, producing the classic S-shaped logistic curve.

## Block chain
Single stock (`Population`) accumulates a single flow (`NetBirthRate`). The flow is determined by multiplying the current population by a `FractionalNetBirthRate`, which itself declines linearly as population approaches the environment's `CarryingCapacity`. The feedback loop: more population → higher birth rate → higher population → lower fractional rate → growth slows and saturates.

Formula summary:
- `FractionalNetBirthRate = MaximumFractionalNetBirthRate × (1 − Population / CarryingCapacity)`
- `NetBirthRate = FractionalNetBirthRate × Population`
- `Population(t=0) = InitialPopulationFraction × CarryingCapacity`

## Resources
n/a — pure SD with no agent populations or resource pools.

## Key settings worth copying
- **CarryingCapacity** set to 1.0 (normalised units) so all results are expressed as fractions; rescale by multiplying outputs for real populations.
- **MaximumFractionalNetBirthRate** set to 1.0, which scales time so that 1 time unit equals 1/g* — making the model dimensionless and directly comparable to the textbook logistic equation.
- **InitialPopulationFraction** (typically small, e.g. 0.01) seeds the stock far below carrying capacity to observe the full S-curve.
- **Time unit:** Day (easily changed to Year or any planning horizon).
- Converted from Vensim LOGISTIC.MDL — shows AnyLogic's SD import capability.

## KPIs instrumented
- `Population` over time (S-curve chart) — the primary output.
- Implicit: time to reach 50 % of carrying capacity (inflection point) and asymptotic saturation level.

## Reusable idea
Normalise carrying capacity to 1 and maximum growth rate to 1 when building any bounded-growth SD model; this makes the model unit-agnostic and lets you overlay multiple scenarios on the same 0–1 chart before re-scaling to real units for reporting.
