# Pattern card — Pop and Carrying Capacity
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models the co-evolution of a population and its environment by coupling logistic population growth with a degradable, regenerating carrying capacity stock.

## Block chain
Two coupled stock-and-flow loops drive the model. A **Population** stock accumulates Births and loses Deaths. A **Carrying Capacity** stock accumulates Regeneration and loses Degradation (consumption). Aux variables compute the ratio of population to carrying capacity, which feeds logistic and power-function lookup tables to derive fractional birth and death rates. Births scale linearly with population via the fractional birth rate; deaths do the same via the fractional death rate. Degradation of carrying capacity is proportional to per-capita resource consumption multiplied by population, capped so carrying capacity cannot go negative. An optional maturation delay switch routes births through a delay before they enter the population stock, enabling S-shaped growth or overshoot-and-collapse dynamics.

## Resources
- No agent pools or queues (pure SD)
- Two stocks: Population and Carrying Capacity
- Carrying capacity acts as the renewable resource pool subject to depletion and regeneration

## Key settings worth copying
- **Time unit:** Day (converted from a Vensim annual model — rescale rates accordingly)
- **Fractional birth rate:** logistic function of (Population / Carrying Capacity)
- **Fractional death rate:** power function of (Population / Carrying Capacity)
- **Max fractional net birth rate** and **min fractional death rate:** scalar parameters the user tunes
- **Regeneration rate:** exogenous constant set by the user (linear replenishment)
- **Max degradation rate:** derived from carrying capacity magnitude, declining as undamaged capacity shrinks
- **Min degradation time constant:** controls how quickly the environment degrades under pressure
- **Resource consumption per capita:** expressed in people-equivalent carrying-capacity units per person per year
- **Maturation delay switch:** boolean parameter that toggles delayed birth entry

## KPIs instrumented
- Population trajectory over time (exponential growth, S-shaped growth, or overshoot-collapse)
- Carrying capacity trajectory (depletion curve and recovery)
- Ratio of population to carrying capacity (stress indicator)
- Net birth rate and net fractional birth rate (system health signals)

## Reusable idea
Coupling a renewable-resource stock to a population stock via a stress ratio (population / capacity) — and using asymmetric nonlinear functions (logistic for births, power-law for deaths) of that ratio — is the transferable trick: it generates the full family of classical population modes (exponential growth, S-shaped stabilisation, overshoot-and-collapse) from a single model just by adjusting consumption and regeneration parameters.
