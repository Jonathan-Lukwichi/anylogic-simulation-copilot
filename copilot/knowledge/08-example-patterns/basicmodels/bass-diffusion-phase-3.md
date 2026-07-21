# Pattern card — Bass Diffusion - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product spreads through a market via both advertising-driven and word-of-mouth adoption, while accounting for product obsolescence and replacement demand.

## Block chain
Two stocks drive the model: `PotentialAdopters` and `Adopters`. A single `AdoptionRate` flow moves people from potential to actual adopters; it is the sum of two auxiliary variables — `AdoptionFromAd` (advertising channel: PotentialAdopters × AdEffectiveness) and `AdoptionFromWOM` (word-of-mouth channel: Adopters × ContactRate × AdoptionFraction × PotentialAdopters / TotalPopulation). A `DiscardRate` flow, computed as `delay(AdoptionRate, ProductLifeTime)`, drains the Adopters stock after each unit's useful life expires, creating a recycling pulse of demand back into the system (the Balancing "Market Saturation" feedback loop). The causal diagram also labels a Reinforcing "Word of Mouth" loop linking Adopters back into WOM adoption.

## Resources
n/a (pure equation-based SD model; no agent pools or capacity constraints)

## Key settings worth copying
- **TotalPopulation:** 100,000 (market size parameter, slider-adjustable)
- **ContactRate:** 100 per year (how often an adopter contacts a potential adopter)
- **AdEffectiveness:** 0.011 (fraction of potential adopters converted per year by advertising alone)
- **AdoptionFraction:** 0.015 (probability that a contact between adopter and non-adopter results in adoption)
- **ProductLifeTime:** 2 years (delay before an adopter discards and potentially re-enters market)
- **Simulation horizon:** 8 years, time unit = Year, dt = 0.1 year
- **DiscardRate formula:** `delay(AdoptionRate, ProductLifeTime)` — a material delay, not an information delay

## KPIs instrumented
- Time-series plot of `PotentialAdopters` vs `Adopters` (stock levels over 8 years)
- Time-series plot of `AdoptionRate` vs `DiscardRate` (flow magnitudes over time)
- Both plots auto-scale vertically and share an 8-year time window

## Reusable idea
Split the adoption flow into two additive channels — an exogenous push (advertising, proportional only to remaining potential) and an endogenous pull (word-of-mouth, proportional to the product of current adopters and remaining potential divided by total market). Then feed a delayed echo of that same flow back as a discard/replacement rate using `delay()`. This three-line SD structure captures the classic Bass S-curve with saturation and repeat-purchase dynamics without any agent logic.
