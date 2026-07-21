# Pattern card — Labor Learning Curve
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how workforce productivity evolves over time as cumulative experience accumulates and decays, capturing the classic learning-curve effect at an aggregate level.

## Block chain
Two coupled stock-and-flow structures form the core:

1. **Labor stock** — inflow is a hiring rate (baseline replacement plus optional pulse and exponential-growth components); outflow is attrition (a fractional quit rate applied to current headcount).
2. **Total Experience stock (coflow)** — a "shadow" stock that tracks person-weeks of experience across the workforce. It rises as on-the-job learning adds experience proportional to current labor, and as new hires bring their starting experience. It falls when workers quit (taking average experience with them) and through an experience-decay rate that represents forgetting and process/equipment changes.

Average experience per worker = Total Experience / Labor. Productivity is then read off a power-law learning curve: `Productivity = ReferenceProductivity × (AverageExperience / ReferenceExperience) ^ LearningExponent`, where the exponent is derived from the user-specified percentage gain per doubling of experience.

A pink-noise generator (first-order exponential smoothing of white-noise draws via `uniform()`) is wired to a flexible test-input switch that lets the modeller drive the hiring rate or attrition rate with a step, pulse, ramp, sine wave, or random signal — useful for sensitivity testing without rebuilding the model.

## Resources
- No discrete resource pools (pure SD).
- Key parameters acting as "capacity" levers:
  - **InitialLabor** — starting headcount (default 1000 workers).
  - **NormalAttritionRate** — baseline fractional turnover per year.
  - **NormalExperienceDecayRate** — baseline fractional decay of cumulative experience per year.
  - **WeeksPerYear** — converts annual rates to the Day time unit.

## Key settings worth copying
- **Time unit:** Day (rates expressed as fractions per year, converted internally).
- **Learning exponent formula:** `LN(1 + FractionalProductivityGain) / LN(2)` — derive from a single business input (% gain per doubling) rather than hard-coding the exponent.
- **Coflow pattern:** mirror every inflow/outflow on the Labor stock with a corresponding experience flow; attrition outflow carries `AverageExperience` per departing worker.
- **Experience decay:** separate auxiliary allows decay rate to shift at a user-set time (`TimeForDecayChange`) — models product/technology transitions.
- **Pink noise:** `CorrelationTime` and `NoiseSD` parameters let you calibrate autocorrelated randomness; white noise seed is `uniform()` sampled once per time step via an event.
- **Pulse hiring test:** `PulseSize` workers added at `PulseTime` — useful for evaluating recovery dynamics after a sudden hiring surge.

## KPIs instrumented
- **Productivity** (learning-curve output) — primary output chart.
- **AverageExperience** — tracks workforce knowledge capital over time.
- **Labor** — headcount trajectory under different hiring/attrition scenarios.
- **Total Experience** — aggregate person-weeks; area under this curve relates to cumulative output capacity.

## Reusable idea
The **coflow** technique: whenever a stock of entities (workers, machines, customers) carries an attribute that must be tracked in aggregate (experience, quality, loyalty), create a parallel stock for the attribute total and mirror every flow on the main stock with a proportional attribute flow. This cleanly separates headcount dynamics from knowledge/quality dynamics while keeping them tightly coupled — a pattern directly applicable to any IE model where workforce skill, equipment wear, or inventory quality must be modelled alongside quantity.
