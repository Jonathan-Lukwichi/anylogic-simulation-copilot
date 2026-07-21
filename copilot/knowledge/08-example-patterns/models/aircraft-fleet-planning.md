# Pattern card — Aircraft Fleet Planning
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (agent-based, each aircraft is an autonomous agent with its own statechart)
- **Problem it solves:** Determine the optimal weekly rate-of-effort allocation across a mixed fleet so that maintenance cycles do not ground too many aircraft simultaneously and cumulative flying hours targets are met over a multi-year horizon.

## Block chain
Each aircraft is modelled as an independent agent. Its statechart tracks two parallel maintenance triggers: hours flown (`hrsMtce1` through `hrsMtce5`) and calendar weeks elapsed (`wksMtce1` through `wksMtce3`). Whichever threshold is hit first pulls the aircraft out of the `operational` state into a maintenance state. Once maintenance completes the aircraft re-enters `operational` and its counters reset via `uniform_discr()` draws from the configured intervals.

The main model holds a fleet-level `rateOfEffort` parameter (flying hours per week). Each week the model checks whether the fleet actually achieved that rate; any shortfall accumulates in an `hrsToCatchup` variable, which inflates the target for the following week until the deficit is recovered. This catch-up mechanism is the model's core scheduling logic.

An optimisation experiment sweeps individual aircraft rates-of-effort to maximise total hours flown across 550 weeks while respecting maintenance constraints.

## Resources
- Agent population: one `Aircraft` agent per aircraft in the fleet (typically 3-4 aircraft parameterised individually)
- No ResourcePool blocks; capacity is implicitly bounded by how many aircraft are simultaneously in the `operational` state
- Fleet-level `rateOfEffort` (hours/week) is the shared capacity knob

## Key settings worth copying
- `uniform_discr(main.hrsMtceInterval[i])` — randomises the hours-to-next-maintenance for each aircraft at reset, avoiding lockstep maintenance waves
- `uniform_discr(main.wksMtceInterval[i])` — same principle for calendar-driven checks
- `hrsToCatchup` accumulator: `hrsToCatchup += max(0, rateOfEffort - achievedRateOfEffort)` then feeds into next week's plan (`hrsPlan = rateOfEffort + hrsToCatchup`)
- Model time unit: **Week**; simulation horizon: **550 weeks** (~10 years)
- Optimisation experiment targets per-aircraft rates as decision variables

## KPIs instrumented
- Total fleet flying hours accumulated over the simulation horizon
- Achieved rate of effort per week vs. planned rate (shortfall tracking)
- Number of aircraft simultaneously in maintenance (availability snapshot)
- Catch-up hours outstanding at any point in time

## Reusable idea
The **catch-up accumulator pattern**: when a resource-constrained system misses a periodic target, roll the deficit forward and inflate the next period's goal rather than silently dropping it. This single variable (`hrsToCatchup`) enforces long-run throughput fidelity without complex scheduling logic and can be transplanted directly into any ABM or DES model where weekly/monthly production targets must be met over a rolling horizon.
