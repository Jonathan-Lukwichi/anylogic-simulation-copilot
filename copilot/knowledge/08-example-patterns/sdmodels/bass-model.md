# Pattern card — Bass Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models how a new product spreads through a population via two competing forces — paid advertising and organic word-of-mouth — to predict adoption curves over time.

## Block chain
Two stock variables hold the population split at any point in time: **PotentialAdopters** (not yet adopted) and **Adopters** (already adopted). A single flow, **AdoptionRate**, drains PotentialAdopters into Adopters each time step. AdoptionRate is the sum of two auxiliary pathways: (1) **AdoptionFromAdvertising** — a constant advertising effectiveness coefficient multiplied by the current pool of potential adopters; (2) **AdoptionFromWordOfMouth** — the contact rate between adopters and non-adopters, scaled by the adoption fraction (probability a contact converts). The word-of-mouth term grows non-linearly because it multiplies the Adopters stock, creating a positive feedback loop that drives the classic S-curve.

## Resources
n/a — pure SD; no agent pools, servers, or resource pools.

## Key settings worth copying
- **TotalPopulationN** — fixed scalar parameter defining the market ceiling.
- **AdvertisingEffectivenessA** — constant coefficient; tune to shift the early-adoption ramp.
- **ContactRateC** — frequency at which an adopter encounters a potential adopter (contacts per adopter per day).
- **AdoptionFractionI** — probability a contact results in conversion; multiplied with ContactRateC to give effective word-of-mouth pressure.
- **Time unit:** Day (imported from Vensim BASSMODE.MDL).
- Initial conditions: PotentialAdopters = TotalPopulationN, Adopters = 0 (or a small seed).

## KPIs instrumented
- Adopters stock trajectory over time (the S-curve).
- AdoptionRate flow (bell-shaped peak indicates peak diffusion speed).
- PotentialAdopters depletion rate.

## Reusable idea
Decompose any diffusion/spread flow into an **external-push term** (advertising, broadcast, constant force) and an **internal-pull term** (word-of-mouth, contagion, proportional to current adopters × remaining susceptibles). The two terms together reproduce any S-shaped adoption curve, and tuning their ratio lets you model everything from product launches to epidemic spread to technology adoption.
