# Pattern card — Chronic Treatment Indication Dynamics
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models long-run patient population dynamics for a chronic disease, capturing treatment uptake, discontinuation, re-initiation, and mortality under different medication scenarios.

## Block chain
The model organises the population into four stocks that patients flow through over a lifetime horizon. People start as **notAfflicted**. A true incidence rate moves them into **undiagnosedPatients**. From there a diagnosis rate shifts them to **currentlyTreatedPatients**. Treated patients who stop taking medication fall into **nonPersistentPatients**; a re-initiation rate can pull them back into treatment. Death flows drain both treated and non-persistent pools at separate rates (treatment lowers mortality). A net population growth flow keeps the healthy pool replenished. All rates are expressed per-millisecond (AnyLogic's internal time unit) but are set by slider parameters so analysts can recalibrate to years easily.

## Resources
n/a — pure stock-and-flow SD model; no agents, queues, or resource pools.

## Key settings worth copying
- **Rates exposed as parameters:** trueIncidenceRate, netPopGrowthRate, untreatedDeathRate, diagnosedRate, discontinuingRate, reinitiatingRate, treatmentEffectOnDeathRate — all tunable at run time via sliders.
- **treatmentEffectOnDeathRate** multiplies untreatedDeathRate to derive the treated death rate, making the treatment benefit a single scalar parameter easy to calibrate from clinical data.
- **Time unit:** Millisecond internally; rates should be converted accordingly when parameterising (use AnyLogic's rate unit helpers).
- **Initial stock:** notAfflictedInitial parameter seeds the healthy population; the remaining stocks start at zero or user-defined values.

## KPIs instrumented
- **prevalentPopulation** = diagnosedPatients + undiagnosedPatients (total disease burden)
- **diagnosedPatients** = currentlyTreatedPatients + nonPersistentPatients
- **currentlyTreated** time-series chart (peak tracked via maxTreated)
- **nonPersistent** time-series (peak tracked via maxNonPersistent)
- Separate flow data recorders for reinitiatingTreatment, discontinuingTreatment, treatedDeaths, untreatedDeaths

## Reusable idea
Split the "off-treatment" pool into its own stock (nonPersistentPatients) rather than sending churned patients back to undiagnosed. This creates a bidirectional loop — discontinuing rate drains treated stock, reinitiating rate refills it — which cleanly captures real-world medication adherence churn without adding agent-level complexity. The same two-rate churn loop can be dropped into any market-share or subscription-retention SD model.
