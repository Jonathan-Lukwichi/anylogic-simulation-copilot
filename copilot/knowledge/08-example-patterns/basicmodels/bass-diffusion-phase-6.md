# Pattern card — Bass Diffusion - Phase 6
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product spreads through a market via advertising and word-of-mouth, tracking the transition of a population from potential adopters to active adopters over time.

> **Verified corrections (2026-10-01).** Checked against the shipped 8.9.10 example `.alp` and the tutorial text (AnyLogic Help tutorials, *AnyLogic in 3 Days*). Where they differ from the text below, these win.
> - `SwitchTime` is the Timeout of `with_advertising → without_advertising`, whose entry action sets `MonthlyExpenditures = 0`; `adoptFraction(t)` is the seasonal lookup `demand(getMonth())/200` (with the off-by-one of gotcha G64) — not "SwitchTime … via adoptFraction(time())".
> - Word of mouth is `Adopters*ContactRate*AdoptionFraction*PotentialAdopters/TotalPopulation` (the card dropped `/TotalPopulation`).
> - The phase's point is an **Optimization experiment**: minimise `root.TotalExpenditures`; `MonthlyExpenditures` continuous 0–10,000; `SwitchTime` discrete 0–1.5 in steps of 0.0833; requirement `root.Adopters >= 80000`; stop at 1.5 years; 500 iterations; no replications (so the optimum is one run per plan — gotcha G11).
> - ContactRate (100) and ProductLifeTime (2) carry per-minute / minute tags in the `.alp` while the model runs in years; the tutorial means per year and years (see phase 1 note).

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
