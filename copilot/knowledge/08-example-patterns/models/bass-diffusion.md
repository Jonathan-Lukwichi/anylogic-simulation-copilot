# Pattern card — Bass Diffusion
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Forecasts how a new product or innovation spreads through a fixed population over time, separating advertising-driven adoption from word-of-mouth contagion.

## Block chain
The model maintains two stocks: **PotentialAdopters** (people who have not yet adopted) and **Adopters** (people who have). A single flow, **AdoptionRate**, drains PotentialAdopters and fills Adopters each time step. That flow is the sum of two auxiliary rates:

- **AdoptionFromAd** — advertising effect: `PotentialAdopters × AdEffectiveness`. This is a constant pressure independent of how many people have already adopted.
- **AdoptionFromWOM** — word-of-mouth contagion: `Adopters × PotentialAdopters × ContactRate × AdoptionFraction / TotalPopulation`. This term grows as Adopters increases, then shrinks as PotentialAdopters is exhausted, producing the classic S-curve.

Two variant sub-models extend the base:
1. **Discards and Replacements** — adds an outflow from Adopters (product discard after useful life) that feeds back into PotentialAdopters, sustaining long-run sales.
2. **Repeated Purchases** — adds a **RepeatPurchaseRate** auxiliary so SalesRate includes both first-time adoptions and recurring consumption by existing Adopters.

All three model variants run simultaneously in the same simulation, enabling direct visual comparison of their diffusion curves.

## Resources
n/a (pure SD — no discrete agents, queues, or resource pools)

## Key settings worth copying
- **TotalPopulation:** 1,000,000 (slider range 0–100)
- **AdoptionFraction:** 0.011 (slider 0.005–0.05) — probability an contacted non-adopter converts
- **ContactRate:** 100 per day (slider 30–300) — social contacts per adopter per unit time
- **AdEffectiveness:** constant rate of advertising-driven conversion
- **ModelTimeUnit:** Year
- Parameter variation experiment sweeps ContactRate to show sensitivity of peak adoption timing and height

## KPIs instrumented
- Adopters stock over time (S-curve shape)
- AdoptionRate flow over time (bell curve — peak signals market saturation)
- Comparative time-series chart across all three model variants side-by-side

## Reusable idea
Split a single adoption flow into an **advertising term** (proportional only to remaining potential) and a **contagion term** (proportional to the product of adopters and remaining potential, normalised by total population). This two-force decomposition is the transferable core of Bass-style diffusion and can be grafted into any SD model where you need to distinguish externally-driven uptake from socially self-amplifying spread — disease, technology rollout, policy adoption, etc.
