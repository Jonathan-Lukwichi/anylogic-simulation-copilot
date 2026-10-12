# Pattern card — Failure rates that grow with age or overdue maintenance: keeping a Rate transition up to date
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 4 "How to build agent-based models. Field service example" (§4.4) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** A statechart failure transition whose rate depends on elapsed time (age, time since maintenance, time since last contact) silently keeps an old value, so ageing or late maintenance has little or no effect.

## Mechanism
**The book's design** (ch. 4 pp. 22–24):
- Store event times in variables (`TimeLastMaintenance`, `TimeLastReplacement`) and derive `age()` and
  `timeSinceMaintenance()` from `time()`.
- `failureRate()` = base rate × `max(1, timeSinceMaintenance()/MaintenancePeriod)` × `max(1, age()/(3*MaintenancePeriod))`.
- The transition `Working → Failed` is Rate-triggered with `failureRate()`.
- The initial values `uniform(-MaintenancePeriod, 0)` and `uniform(-3*MaintenancePeriod, 0)` spread the fleet's
  starting state.

**What 8.9.10 evaluates** (Help *Transition*, *Agent API*):
- A Rate is computed on entry to the state. It is recomputed only when `onChange()` runs for that agent, and by default
  that happens only when the agent itself originates an event or receives a message. A changed value reschedules the
  transition with a fresh exponential draw.
- A Timeout is computed once, on entry.

**Consequence** *(inferred from the Help and the 8.9.10 model settings; not run-tested)*:
- In *Field Service Phase 5*, a Working unit's only own events are the failure itself and `MaintenanceTimer` (User
  control). When the timer fires, time since maintenance equals the period, so the overdue factor is exactly 1. While
  the unit then waits for a crew, nothing re-reads the rate. The overdue multiplier is therefore never applied. The age
  factor updates only on entry and at timer ticks.
- `models/Field Service` draws `exponential(...)` once, in a Timeout, on entering Working. At that moment the unit is
  never overdue, so the outcome is the same.

**Fix options:**
1. **Refresh event.** Give the agent a Cyclic event, for example daily, with an empty action. Each occurrence triggers
   `onChange()`, so the Rate is re-read. The hazard becomes piecewise constant on that step. Redrawing a fresh
   exponential keeps it statistically sound, because the exponential is memoryless.
2. **Synchronous steps** for large populations (Help *Transition*). Tick *Enable synchronous steps* on the container
   and call `onChange();` in the agent's *On step*.
3. **Targeted refresh.** Call `unit.onChange()` when an input of the formula changes. For example, arm a User-control
   event at the maintenance due date whose firing notifies the unit.
4. **Exact alternative: thinning** (standard non-homogeneous Poisson method):
   - Use a Rate transition at an upper bound `hMax`.
   - Follow it with a branch: fail with probability `failureRate()/hMax`; otherwise take the default exit back into
     `Working`, which redraws.
   - Don't make that test a guard: a false guard disarms a Rate
     (`bigbook/statechart-guards-branches-and-state-reentry.md`).
   - Keep `Working`'s entry and exit actions free of side effects.

## Resources
n/a

## Key settings worth copying
- Refresh event: Cyclic, recurrence on the scale over which the hazard changes by a few per cent (1 day here). Its
  action can stay empty or call `onChange();` explicitly.
- Rate field: `failureRate()` per day. It must stay non-negative, because a negative rate throws (Help).

## KPIs instrumented
- Failures tagged by whether the unit was overdue when it failed. Set the flag in the Failure action.
- Observed failure rate by age band, compared with the formula.

If maintenance backlogs exist but overdue failures stay at their base-rate share, the refresh is missing.

## Pitfalls
- **The refresh must be the unit's own event,** or an explicit `onChange()` on it. Events on Main and population
  statistics notify no unit.
- **A failure time drawn in a Timeout can never react.** Switch to a Rate or a re-armable event.
- **Cost:** one refresh per agent per step. That is trivial for 50 units; for 100,000 agents, use synchronous steps
  with a coarser step.
- **Expect conclusions to move.** With the effect active, fewer crews mean longer maintenance waits and more failures,
  so the book's optimum (3 crews, replace after 7 periods, p. 47) should be re-checked.

## Reusable idea
The engine does not notice time passing inside a rate expression. Any hazard containing `time()`, an age, or another
agent's data needs an explicit refresh path.

## When the co-pilot should use this
- Reliability and maintenance ABMs, patient deterioration, churn that grows with time since last contact.
- Any Rate or Timeout expression that reads the clock or remote data.
- Related: G56 and `videos/statechart-live-controls-trigger-reevaluation.md` (the same mechanism for slider changes),
  `models/field-service.md`, `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`.
