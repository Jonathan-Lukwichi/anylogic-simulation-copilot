# Pattern card — Bass Diffusion - Phase 6
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product spreads through a market via advertising and word-of-mouth, tracking the transition of a population from potential adopters to active adopters over time.

## Block chain
Two stock variables drive the model: **PotentialAdopters** (initialized to TotalPopulation) drains into **Adopters** via the **AdoptionRate** flow. AdoptionRate is the sum of two sub-flows:
- **AdoptionFromAd** — advertising-driven adoption: `PotentialAdopters * AdEffectiveness`, where AdEffectiveness scales with monthly marketing spend.
- **AdoptionFromWOM** — word-of-mouth adoption: `Adopters * ContactRate * AdoptionFraction * PotentialAdopters`, creating a reinforcing feedback loop (R loop "Word of Mouth").
A **DiscardRate** flow uses a pipeline delay (`delay(AdoptionRate, ProductLifeTime)`) to drain the Adopters stock back once product lifetime expires, representing product replacement/churn. A balancing loop (B loop "Market Saturation") limits growth as PotentialAdopters deplete.

## Resources
n/a — pure equation-based SD model; no agent pools or capacity constraints.

## Key settings worth copying
- **TotalPopulation:** 100,000 (slider-adjustable)
- **ContactRate:** 100 per minute (controls word-of-mouth spread speed)
- **MonthlyExpenditures:** 1,100 (advertising budget; AdEffectiveness = spend / 10,000)
- **ProductLifeTime:** 2 minutes model-time (used in pipeline delay for discard)
- **SwitchTime:** 3.0 years (used to switch advertising strategy via `adoptFraction(time())`)
- **ModelTimeUnit:** Year
- All parameters exposed as interactive sliders for sensitivity analysis

## KPIs instrumented
- Adopters stock level over time (S-curve adoption trajectory)
- Potential Adopters remaining (market saturation indicator)
- AdoptionRate and DiscardRate flows (net product uptake)
- TotalExpenditures accumulator (cumulative marketing cost)
- AdoptionFraction (tracks the fraction of contacts that convert)

## Reusable idea
The core transferable trick is splitting the adoption flow into two additive components — one proportional to advertising spend and one proportional to the product of current adopters and remaining potential (the classic Bass imitation term) — and then using a **pipeline delay** on the adoption flow to model product retirement without adding a third stock. This cleanly separates innovation effect from imitation effect and lets you tune each driver independently via sliders while watching the emergent S-curve.
