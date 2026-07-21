# Pattern card — Clinical Process Concepts
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Quantify how a patient cohort progresses through the full clinical cycle — from recognising a health issue to final outcome — so planners can see where backlogs accumulate and how rate or fraction changes ripple across the whole system.

## Block chain
The model organises the clinical journey as a chain of stocks connected by flows, each stock representing a distinct patient state:

1. **InputHealthState** — the pool of people with an unrecognised health issue.  A concern rate drains them into **HealthIssue**.
2. **HealthIssue** → **DemandForInitialContact** — patients decide to seek help (governed by `requestRate` and a `presentFraction` split).
3. **InitialContact** → **InitNeedsAssessPlan** — initial assessment and care planning stage.
4. **InitNeedsAssessPlan** splits: patients either go to **HealthCareInvestigation** (tests) or bypass directly to **CondNeedsAssessPlan** when no investigation is needed.
5. **HealthCareInvestigation** → **DiagnosedHealthCondition** — tests complete at `testCompletionRate`; a `retestFraction` can loop patients back for further testing.
6. **DiagnosedHealthCondition** / **CondNeedsAssessPlan** → **NoNeedForFurtherAction** or **HealthCareTreatment** — branching on `investigateFraction`.
7. **HealthCareTreatment** → **TreatedHealthCondition** — treatment lasts `TreatDuration` days.
8. **TreatedHealthCondition** → **OutputHealthState** → **HealthCareEvaluation** → **ClinicalProcessOutcomeEval** → **OutputHealthStateFinal** — post-treatment evaluation chain.
9. A **recur** flow from **InterEpisodeState** back to **InputHealthState** closes the loop, capturing conditions that relapse after an episode ends.

All flows that are rates (per day) read from auxiliary parameters; fraction-split flows use dimensionless fractions so the two outgoing branches always sum to 1.

## Resources
n/a — pure SD; no individual agents or resource pools. Capacity constraints are implicit in wait-time parameters (`waitTime`, `CondNeedsAsessWaitTime`, `TreatWaitTime`) that lengthen the time patients spend in a stock.

## Key settings worth copying
- **Time unit:** Day — appropriate for clinical pathways where waits range from hours to months.
- **Fraction splits:** `investigateFraction`, `presentFraction`, `retestFraction` — dimensionless auxiliaries controlling branching; keeping them as sliders lets users run live what-if experiments without recompiling.
- **Rate auxiliaries:** `concernRate`, `requestRate`, `assessRate`, `testCompletionRate` — each is 1 / average_time_in_state, so they are easy to calibrate from real data.
- **Recurrence loop:** `timePostEpisode` auxiliary governs how quickly recovered patients re-enter the input pool, capturing chronic or recurring conditions.
- **Scale parameter:** a single `scale` multiplier adjusts the entire cohort size, enabling sensitivity runs without touching individual stock initial values.

## KPIs instrumented
- Stock levels at each stage (prevalence / queue depth at each care step)
- Flow rates between stages (throughput)
- Implied wait times derived from Little's Law (stock / inflow rate)
- Fraction of patients reaching final discharge vs. looping back (recurrence prevalence)

## Reusable idea
Model every patient-pathway branch as a **fraction auxiliary** (0–1) rather than hard-coding two separate flow formulas. This single-number knob instantly makes any binary branch point interactive: drag the slider and watch the system rebalance in real time — a technique directly applicable to any SD model with conditional routing (triage splits, rework loops, yield fractions in manufacturing).
