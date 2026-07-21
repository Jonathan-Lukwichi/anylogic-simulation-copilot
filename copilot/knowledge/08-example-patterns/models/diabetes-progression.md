# Pattern card — Diabetes Progression
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Projects how a population moves from prediabetes through undiagnosed and diagnosed disease stages to death over a multi-decade horizon, and tests how detection rates and treatment quality alter that trajectory.

## Block chain

Six stocks capture the disease pipeline in two parallel lanes — an undiagnosed lane and a diagnosed lane — at three clinical stages: Prediabetes, Uncomplicated Diabetes (UCD), and Complicated Diabetes (CD).

Undiagnosed lane: `unDiagnosedPreDiabetes` → `unDiagnosedUncomplicated` → `unDiagnosedComplicated` → Death  
Diagnosed lane: `diagnosedPreDiabetes` → `diagnosedUncomplicated` → `diagnosedComplicated` → Death

New entrants arrive at `unDiagnosedPreDiabetes` via a time-lookup flow (`newCasesPreD`) driven by a table function `IncidenceByYear(time())` anchored at 2004 and projecting to 2044.

People cross from the undiagnosed lane to the diagnosed lane at each stage through detection flows (`preDdiag`, `unCdiag`, `ComplDiag`), each proportional to the stock size multiplied by a stage-specific detection rate.

Progression within a lane is rate-based (stock / years-to-next-stage). Treatment modifiers are multiplicative scalars applied to three clinical outcomes: onset speed (`treatmentImpactOnOnset`), progression speed (`treatmentImpactOnProgression`), and life expectancy (`treatmentImpactOnLifeExpectancy`). A value of 1.0 means no treatment benefit; values below 1.0 slow the disease or extend life.

The model runs in annual time units from 2004 to 2050.

## Resources

n/a — pure population-level stocks and flows; no discrete agents or resource pools.

## Key settings worth copying

- **Time unit:** Year; horizon 2004–2050
- **Incidence inflow:** table function `IncidenceByYear(time())` — decouples new-case arrival from the SD structure, making it easy to swap epidemiological projections without restructuring the diagram
- **Detection rates (slider-driven):** `preDiabDiagRate`, `unDiagUCDDetectionRate`, `CDdetectionRate` — one per clinical stage, letting analysts run what-if on screening policy independently
- **Treatment scalars (slider-driven):** `treatmentImpactOnOnset`, `treatmentImpactOnProgression`, `treatmentImpactOnLifeExpectancy` — dimensionless multipliers that sit inside flow formulas, so treatment improvement is a single parameter change rather than a structural edit
- **Mortality flows:** `undiagCdeaths = stock / lifeExpectancy`, `diagCdeaths = stock / (lifeExpectancy * treatmentImpactOnLifeExpectancy)` — simple first-order drain, easy to replace with age-stratified lookup later

## KPIs instrumented

- Prevalence in each of the six stocks over time (stock-level time plots)
- Cumulative deaths from undiagnosed vs. diagnosed complicated diabetes
- Implied total disease burden (sum of all six stocks at any year)
- Sensitivity of prevalence to detection-rate and treatment sliders (interactive parameter sweep via sliders)

## Reusable idea

Split every disease stage into an undiagnosed and a diagnosed sub-stock, then connect the two lanes with detection-rate flows. This one structural choice lets the model independently vary screening policy (detection rates) and treatment quality (multiplier scalars) without touching the rest of the diagram — making policy comparisons clean and self-documenting.
