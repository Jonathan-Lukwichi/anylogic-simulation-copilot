# Pattern card — Bass Diffusion - Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product spreads through a fixed population via two adoption channels — advertising (innovation) and word-of-mouth (imitation) — producing the classic S-curve of cumulative adopters over time.

## Block chain
Two stock variables hold the population state at any moment:
- **PotentialAdopters** — people who have not yet adopted; initialised to TotalPopulation and drained by AdoptionRate.
- **Adopters** — people who have adopted; filled by the same AdoptionRate flow.

The single outflow/inflow **AdoptionRate** is the sum of two auxiliary rates:
1. **AdoptionFromAd** — advertising-driven adoption: `PotentialAdopters × AdEffectiveness`. Scales linearly with the remaining pool; unaffected by how many adopters already exist.
2. **AdoptionFromWOM** — word-of-mouth adoption: `Adopters × ContactRate × AdoptionFraction × (PotentialAdopters / TotalPopulation)`. Grows as the adopter base grows, then tapers as potential adopters are exhausted — the engine behind the S-curve inflection.

## Resources
n/a — pure SD stock-and-flow; no agent populations or resource pools.

## Key settings worth copying
| Parameter | Default | Role |
|---|---|---|
| `TotalPopulation` | 100 000 | Market size; also sets the initial stock of PotentialAdopters |
| `AdEffectiveness` | 0.011 (dimensionless fraction/year) | Innovation coefficient — controls early-market lift |
| `ContactRate` | 100 per year (stored as per-minute but used annually) | How often an adopter contacts others |
| `AdoptionFraction` | 0.015 | Fraction of contacts that convert — imitation coefficient |
| Model time unit | Year | Ensures rates are interpreted annually |

All four parameters are exposed as interactive sliders in the UI, enabling real-time sensitivity analysis during a run.

## KPIs instrumented
- **Potential adopters** time-series chart — shows the draining reservoir.
- **Adopters** time-series chart — shows cumulative S-curve growth.
- **Adoption rate** time-series — highlights the bell-shaped pulse that peaks at the inflection point of the S-curve.
- A labelled "Market" annotation groups the stocks visually in the SD diagram.

## Reusable idea
Split the adoption flow into two additive sub-rates — one proportional only to the remaining pool (advertising push, never zero) and one proportional to the product of current adopters and remaining pool (word-of-mouth, self-amplifying then self-limiting). This decomposition cleanly separates the two Bass coefficients and makes each independently tunable via a slider, which is the transferable pattern for any two-channel diffusion problem (disease spread, technology uptake, trend propagation).
