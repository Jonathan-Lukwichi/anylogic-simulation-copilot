# Pattern card — Capital Vintaging Coflow
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Tracks how the average factor intensity (e.g., labour or energy per unit output) of a productive capital stock evolves over time as old capital ages and retires while new capital with different characteristics enters.

## Block chain
Capital flows through a construction pipeline (one stock representing capital under construction) and then ages through three sequential vintage cohorts — each modelled as a stock. A construction-start rate feeds the pipeline; capital advances from cohort 1 → 2 → 3 via first-order ageing flows whose residence time is one-third of the average capital life. A discard flow drains the final cohort. Alongside each capital stock runs a paired "factor requirement" coflow stock that carries the factor units needed to operate that cohort's capital; factor requirements enter with new capital, age in lock-step, and retire together with capital. Dividing total factor requirements by total capital at any moment yields the average factor intensity — the coflow's key output.

## Resources
- No agent pools or queues; all structure is continuous stocks and flows
- Average capital life: parameter governing residence time across all three cohorts
- Average construction delay: parameter for the pipeline stock
- Construction start rate: exogenous test input (step, pulse, ramp, sine wave, or pink/white noise variants)
- Marginal factor intensity of new capital: second exogenous input with the same test-input options

## Key settings worth copying
- **Three-cohort ageing chain:** each flow rate = cohort stock / (averageLife / 3) — dividing life equally gives a realistic gamma-distributed retirement profile without extra stocks
- **Coflow pairing:** every capital stock has a shadow factor-requirement stock; they share identical inflow/outflow rates so the ratio stays meaningful at all times
- **Pink-noise generator:** a first-order smoothing stock filters white noise (uniform()) through a correlation time constant, producing autocorrelated random inputs for stress-testing
- **Test-input selector:** a single dimensionless "Input" auxiliary switches among step, pulse, ramp, sine, and pink-noise modes — copy this pattern to parameterise any exogenous driver cleanly
- **Time unit:** Day (converted from a Vensim weekly model)

## KPIs instrumented
- Average factor intensity of the entire productive stock (ratio of summed factor requirements to summed capital)
- Total capital stock (sum of all three vintage cohorts)
- Total factor requirements (sum across cohorts plus construction pipeline)
- Individual vintage capital levels and their factor requirements over time

## Reusable idea
The **coflow pattern**: whenever you need to track an attribute (cost basis, embodied energy, technology vintage) of a heterogeneous stock, shadow each physical stock with a parallel attribute stock using identical flow equations. Dividing the attribute total by the physical total gives the population-average attribute without needing agent-level tracking — a powerful SD shortcut for quality or intensity averaging in capital, inventory, or workforce models.
