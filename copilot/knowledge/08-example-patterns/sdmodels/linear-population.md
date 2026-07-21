# Pattern card — Linear Population
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models first-order exponential population growth and decline driven by constant fractional birth and death rates, demonstrating the feedback loop that produces linear-to-S-shaped dynamics.

## Block chain
A single Stock (Population) is fed by two Flows: a Birth flow and a Death flow. Births are computed as `FractionalBirthRate × Population`; Deaths as `FractionalDeathRate × Population`. Two auxiliary variables track the net birth rate (`BirthRate − DeathRate`) and the net fractional birth rate (`FractionalBirthRate − FractionalDeathRate`). The initial population is set via a separate auxiliary constant (`InitialPopulation`). The stock therefore evolves as dPopulation/dt = Births − Deaths, which yields exponential growth when the net fractional rate is positive and exponential decay when negative. The model was originally a Vensim MDL file imported into AnyLogic.

## Resources
n/a — pure stock-and-flow structure; no agent populations or resource pools.

## Key settings worth copying
- **Time unit:** Day
- **Fractional birth rate:** constant auxiliary (tune to scenario)
- **Fractional death rate:** constant auxiliary (tune to scenario)
- **Initial population:** auxiliary constant feeding the stock's initial value
- **Formulas:** `Births = FractionalBirthRate * Population`; `Deaths = FractionalDeathRate * Population`
- **Net fractional birth rate auxiliary** is useful for dashboard display and sensitivity analysis without duplicating formulas

## KPIs instrumented
- Population level over time (stock trajectory)
- Net birth rate (flow differential)
- Net fractional birth rate (growth rate indicator)

## Reusable idea
Separating the *fractional* rate (a dimensionless proportion) from the *absolute* flow (rate × stock) keeps the model parameterised in terms that are easy to calibrate from real demographic data — any population-dynamics or inventory-growth model benefits from this same fractional-rate pattern rather than hard-coding absolute inflow/outflow magnitudes.
