# Pattern card — Bass Diffusion - Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product spreads through a fixed population via two channels — advertising pressure and word-of-mouth — capturing the classic S-curve of market adoption.

## Block chain
Two stock variables partition the population at all times:
- **PotentialAdopters** (stock) — starts at TotalPopulation; drains at AdoptionRate.
- **Adopters** (stock) — starts at zero; fills at AdoptionRate.

The single flow **AdoptionRate** is the sum of two auxiliary variables:
- **AdoptionFromAd** = PotentialAdopters × AdEffectiveness  (advertising-driven; linear in the remaining pool)
- **AdoptionFromWOM** = Adopters × ContactRate × AdoptionFraction × (PotentialAdopters / TotalPopulation)  (word-of-mouth; proportional to both current adopters and the fraction of population still reachable)

The WOM term creates the positive feedback loop responsible for the S-shaped diffusion curve.

## Resources
n/a — pure stock-and-flow model; no agents, queues, or resource pools.

## Key settings worth copying
| Parameter | Default | Unit | Role |
|---|---|---|---|
| TotalPopulation | 100 000 | — | Market size ceiling |
| ContactRate | 100 | per minute (treated as per year in model time) | Social contact frequency |
| AdEffectiveness | (slider) | — | Coefficient of innovation (p) |
| AdoptionFraction | (slider) | — | Coefficient of imitation (q) |
| ModelTimeUnit | Year | — | All rates interpreted annually |

Slider controls are wired to all four parameters, enabling live what-if exploration without re-running.

## KPIs instrumented
- Time-path of **Adopters** stock (S-curve shape)
- Time-path of **PotentialAdopters** stock (mirror decline)
- **AdoptionRate** flow over time (bell curve peak shows inflection point)

## Reusable idea
Split a fixed population into exactly two complementary stocks (Potential + Adopted) with one flow governed by two additive terms — a constant-coefficient "push" term (advertising) and a nonlinear "pull" term (social contagion proportional to adopter × remaining-fraction). This two-term AdoptionRate formula is the transferable core of Bass diffusion and can be dropped into any SD model where an innovation competes for a saturating market.
