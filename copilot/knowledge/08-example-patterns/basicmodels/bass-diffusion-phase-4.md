# Pattern card — Bass Diffusion - Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models how a product spreads through a market via two competing channels — advertising and word-of-mouth — while accounting for product obsolescence through a discard delay.

## Block chain
Two stock variables track the population over time: **PotentialAdopters** (starts at TotalPopulation, drains via AdoptionRate) and **Adopters** (fills via AdoptionRate, drains via DiscardRate).

Two auxiliary flows feed into the single **AdoptionRate** flow:
1. **AdoptionFromAd** — advertising-driven adoption: `PotentialAdopters × AdEffectiveness`
2. **AdoptionFromWOM** — word-of-mouth adoption: `Adopters × ContactRate × AdoptionFraction × (PotentialAdopters / TotalPopulation)`

Total `AdoptionRate = AdoptionFromAd + AdoptionFromWOM`.

**DiscardRate** uses a pipeline delay: `delay(AdoptionRate, ProductLifeTime)`, meaning units adopted ProductLifeTime years ago leave the Adopters stock and re-enter the potential pool (or are simply lost — the classic Bass discard extension).

The solver uses the Euler method for differential equations, with time unit = **Year**.

## Resources
n/a — pure SD stock-and-flow; no agent populations or resource pools.

## Key settings worth copying
| Parameter | Role |
|-----------|------|
| `TotalPopulation` | Fixed market size (initial value of PotentialAdopters) |
| `ContactRate` | Contacts per adopter per year (unit: PER_MINUTE internally, scaled to years) |
| `AdEffectiveness` | Fraction of potential adopters reached by advertising each year |
| `AdoptionFraction` | Fraction of contacts that result in adoption (0–1) |
| `ProductLifeTime` | Years before an adopter discards the product (delay pipeline length) |
| Solver | Euler ODE method; mixed equations via RK45_NEWTON |

## KPIs instrumented
- **AdoptionRate** time series (units entering the Adopters stock per year)
- **DiscardRate** time series (units leaving the Adopters stock per year)
- **PotentialAdopters** stock level over time
- Charts display both rates together to visualise peak adoption and the discard echo

## Reusable idea
Split the adoption flow into an **advertising channel** (linear in remaining market) and a **word-of-mouth channel** (proportional to current adopters × remaining market fraction) and sum them — this is the classical Bass decomposition. The `delay()` function on the outflow is a clean SD trick to model a fixed product lifetime without introducing additional stocks, giving a realistic adoption-then-discard lifecycle in just two stock variables.
