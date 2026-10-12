# Pattern card — Field Service
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Determine the crew fleet size and proactive-replacement age threshold that maximise annual net profit from a geographically dispersed set of revenue-generating equipment units subject to age- and neglect-driven failures.

## Block chain
Two agent types coordinate through message-passing. **EquipmentUnit** agents are placed across a map area and each runs a statechart that cycles through Working, Maintenance, Repair, and Replacement states. While in Working the unit earns daily revenue. Failure is not scheduled at a fixed rate; instead, each unit resamples its next failure time from an exponential distribution whose rate grows with both how long maintenance has been overdue and how old the unit is. When a failure occurs or a maintenance timer fires, the unit sends a service request up to the parent model. The model holds a priority queue — breakdown requests outrank routine maintenance — and dispatches the next available crew member.

**ServiceCrew** agents begin each day at a home depot. Their statechart moves through Idle, DrivingToWork, Working, and DrivingHome. On becoming idle a crew member checks the request queue: if a breakdown is waiting it goes first, otherwise it takes the oldest maintenance request. Repair, replacement, and maintenance durations are all drawn from triangular distributions centred on a typical time, spanning half to 2.5x that value. An optional boolean policy (`ReplaceOldEquipment`) causes any unit past a configurable age threshold to be proactively swapped out instead of merely repaired during its next visit. Crew headcount is adjustable at runtime through a slider, enabling live what-if comparison on the annual profit chart.

## Resources
- **ServiceCrew agent population** — size set by `ServiceCapacity` (integer slider, runtime-adjustable); daily cost per crew member is `ServiceCrewCostPerDay`
- **EquipmentUnit agent population** — fixed fleet scattered across a 2-D map area
- No AnyLogic Process Library blocks (no Source/Queue/Sink); all scheduling and ownership are handled through statechart transitions and direct agent references

## Key settings worth copying
- Time unit: Day
- Failure inter-arrival: `exponential( NormalFailureRate * max(1, timeSinceMtce/MaintenancePeriod) * max(1, age()/(3*MaintenancePeriod)) )` — the formula *intends* the rate to compound with overdue lag and age, but see the correction below
- Repair duration: `triangular( RepairTypicalTime*0.5, RepairTypicalTime, RepairTypicalTime*2.5 )`
- Replacement duration: `triangular( ReplacementMeanTime*0.5, ReplacementMeanTime, ReplacementMeanTime*1.5 )`
- Maintenance duration: `triangular( MaintenanceMeanTime*0.5, MaintenanceMeanTime, MaintenanceMeanTime*1.5 )`
- Initial maintenance phase offset per unit: `uniform( -MaintenancePeriod, 0 )` — spreads out first-due dates so the crew is not swamped at t=0
- Proactive replacement policy: `ReplaceOldEquipment` boolean + `MtcePeriodsToReplace` threshold

## KPIs instrumented
- Annual revenue: mean fraction of fleet in Working state x `DailyRevenuePerUnit` x 365 (collected in `endYearRevenueK`)
- Annual expenditure: mean crew count x `ServiceCrewCostPerDay` x 365 + cumulative per-job costs (`WorkCost`)
- Net annual profit (revenue minus expenditure, plotted in $K for each simulated year)
- Service crew utilisation: ratio of time spent in Working vs Idle/Driving states, reported as rolling annual averages
- Fleet state breakdown: live counts of units in each statechart state (Working / Maintenance / Repair / Replacement / Failed)

## Reusable idea
Encode degradation as a multiplicative rate modifier on each statechart's timeout rather than a separate failure-mode model. Expressing failure rate as `baseRate * f(maintenanceLag) * f(age)` — where each factor is clamped to 1 at minimum — means a well-maintained new unit behaves normally, an overdue unit fails faster, and an aged overdue unit fails fastest. This single expression inside the statechart's self-loop timeout replaces what would otherwise require nested sub-models or separate state-dependent rate tables.

## Correction (8.9.10 review, 2026-10-01)
In the shipped 8.9.10 model the failure time is drawn once, by a Timeout on entering Working, and at that moment the unit is never overdue (maintenance was just done or is not yet due), so the overdue factor is always 1; only the age factor applies, and only at state entry. In the Big Book's *Field Service Phase 5/6* the Rate is re-read only when the unit's maintenance timer fires, again when the overdue factor is 1 *(inferred from Help 8.9.10 trigger semantics and the model settings; not run-tested)*. So "an overdue unit fails faster" is the formula's intent, not the shipped behaviour. To make the effect real, refresh the rate (`bigbook/abm-time-dependent-hazard-rate-refresh.md`, gotcha G70). The repair `triangular(0.5·T, T, 2.5·T)` averages 1.33 T, not T (G55). Related cards: `bigbook/abm-design-recipe-states-messages-and-dispatcher.md` (message design, dispatcher races), `bigbook/abm-runtime-resizing-of-a-busy-agent-population.md` (the crew slider).
