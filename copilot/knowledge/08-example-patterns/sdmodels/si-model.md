# Pattern card — SI Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how an infectious disease spreads through a closed population with no recovery, tracking the transition from Susceptible to Infectious over time.

## Block chain
Two stock variables hold the compartment sizes: **SusceptiblePopulationS** and **InfectiousPopulationI**. A single **Flow** called **InfectionRate** drains S and fills I simultaneously. The infection rate formula is:

  InfectionRate = (S × infectivity_i × contact_rate_c × I) / N

where N is the fixed total population. As I grows, the rate accelerates until nearly everyone is infectious — a classic positive-feedback loop with a decelerating brake as S is depleted.

## Resources
n/a — this is a pure SD compartmental model; no agent pools or queues are used.

## Key settings worth copying
- **Time unit:** Day
- **Parameters:** N (total population), ContactRateC (contacts per person per day), InfectivityI (probability of transmission per contact), InitialInfectiousPopulation (seed infections)
- **Stock initial values:** S₀ = N − InitialInfectiousPopulation; I₀ = InitialInfectiousPopulation
- **Flow formula:** `(S * i * c * I) / N` — frequency-dependent (divides by N), keeping the rate bounded
- **Model converted from Vensim** SI_MODEL1.mdl — useful cross-tool reference

## KPIs instrumented
- Time-series chart of **SusceptiblePopulationS** (declining S-curve)
- Time-series chart of **InfectiousPopulationI** (rising S-curve)
- Implicit: epidemic peak timing can be read from the inflection point of I

## Reusable idea
The transferable trick is **frequency-dependent mixing**: dividing the force of infection by total population N (`S * i * c * I / N`) keeps the model well-behaved regardless of population size and is the standard building block for any SIR/SEIR extension — just add more stocks and flows for Recovered, Exposed, or Vaccinated compartments using the same rate formula pattern.
