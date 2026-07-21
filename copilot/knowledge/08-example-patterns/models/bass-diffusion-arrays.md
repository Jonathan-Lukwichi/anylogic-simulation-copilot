# Pattern card — Bass Diffusion Arrays
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product or innovation spreads through a segmented population driven by advertising and word-of-mouth, with each segment tracked independently via subscript arrays.

## Block chain
The model maintains two stock variables — PotentialAdopters and Adopters — both dimensioned over a Gender enum (MALE, FEMALE). A single adoption flow converts potential adopters into adopters each month through two additive channels:

1. **Advertising effect** — each gender's pool of potential adopters is multiplied by that gender's ad-effectiveness coefficient, producing an adoption rate independent of how many people have already bought.
2. **Word-of-mouth effect** — adopters from both genders make contacts at their own contact rates; combined contacts are scaled by the fraction of potential adopters remaining in the total population, so saturation naturally slows the spread.

The two channels feed one flow, and because every parameter (TotalPopulation, AdEffectiveness, ContactRate, imitation coefficient) is stored as a HyperArray indexed by Gender, the entire logic runs once but produces separate trajectories per segment without duplicating equations.

## Resources
- No queues or servers (pure SD).
- Parameters per gender segment:
  - TotalPopulation: [80, 120] (thousands, male / female)
  - AdEffectiveness: [0.015, 0.032]
  - ContactRate: [0.023, 0.011]

## Key settings worth copying
- **Time unit:** Month (continuous ODE integration).
- **HyperArray initialisation:** `new HyperArray( new double[]{val_m, val_f}, Gender )` — keeps all gender-specific values in one declaration per parameter.
- **WOM adoption formula:** `(Adopters[MALE]*ContactRate[MALE] + Adopters[FEMALE]*ContactRate[FEMALE]) * PotentialAdopters[Gender] / TotalPopulation.sum()` — cross-segment contact with own-segment susceptibility.
- **Ad adoption formula:** `PotentialAdopters[Gender] * AdEffectiveness[Gender]` — purely segment-local.
- Charts plot both `PotentialAdopters` and `Adopters` per gender on the same time series for direct comparison.

## KPIs instrumented
- Potential adopters over time per gender (stock trajectory)
- Adopters over time per gender (stock trajectory)
- Combined male-and-female adopters per month (flow rate chart)

## Reusable idea
Use AnyLogic HyperArrays (subscripts) to add a segmentation dimension to any SD model without rewriting equations. Define an enum for the dimension (Gender, Region, AgeGroup), declare every parameter and stock as a HyperArray over that enum, and write each equation once — AnyLogic evaluates it for every index automatically. This keeps the model compact while producing fully independent trajectories per segment, and it scales cleanly to three or more segments by extending the enum.
