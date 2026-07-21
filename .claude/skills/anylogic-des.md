---
name: anylogic-des
description: Build discrete-event (process) models in AnyLogic 8.9 - patient/entity flows, services, queues, priorities, data-driven arrivals, experiments with confidence intervals. Battle-tested idioms from the Steve Biko hospital twin. Use when building or extending any process-flow simulation.
---

# anylogic-des

Field-tested method for AnyLogic DES. Follow the idioms; they encode errors already paid for.
(Companion skills: `anylogic-abm` for agent populations, `anylogic-debug` when something breaks.)

## Model skeleton (always this order)
1. **Time units first** (Model properties → hours is the safe default for service systems).
   Every rate/delay expression inherits this — changing later silently rescales everything.
2. **Flow before detail**: Source → [Service/Delay/SelectOutput chain] → Sinks. Run with toy
   rates until agents traverse end-to-end. Only then add data, resources, statistics.
3. One **Reps experiment** (Parameter Variation, Freeform, N=30) from day one — single runs lie.

## Arrivals — the rules
- **Data-driven arrivals**: load counts into a list; a cyclic **Event** calls `source.inject(n)`
  per period. NEVER pair a rate-field expression with an event calling `set_rate()` — they
  double-drive and flood the model (PLE 50k-agent cap).
- Rate-driven: put the expression in the Source's rate field only, e.g. `lambda(time())`, and give
  the lambda its argument: `double t`.
- **Forced pushing OFF** on Source. "Agent could not leave port" is usually forced pushing, not
  a missing resource.

## Routing — decide UPSTREAM (the #1 silent bug)
SelectOutput evaluates its condition at *preview*, BEFORE the entity's On-enter runs. Setting the
routing field in the deciding block's On enter = decision made on a stale value = everyone takes
one branch (looks fine, results are wrong). **Set routing fields in the PREVIOUS block's On exit.**
Generalises: for any agent field, know its write point vs read point; write must come strictly first.

## Services, queues, priorities
- **Service** = Queue+Seize+Delay+Release in one; prefer it. There is no "Wait" block — use
  **Delay with "Until stopDelay()"** and call `stopDelay(agent)` when ready.
- Priority queueing: Properties → Priorities → **Task priority**, higher value served first, e.g.
  `agent.triage.equals("P1") ? 3 : agent.triage.equals("P2") ? 2 : 1`.
  Default is 0 for all = FIFO — priority silently NOT enforced. Check every queueing block.
- Acuity-dependent service times: ternary chains of `lognormal(mu, sigma, min)` — remember
  lognormal params are on the LOG scale (median = e^mu).
- Live readouts: `block.size()` (in block), `block.queueSize()` (waiting), `pool.utilization()`,
  `sink.count()`.

## Scope rules (compile-error factory)
- Inside Main's own blocks/actions: **bare names** (`forecastDriven`), never `main.`.
- Inside another agent's code: qualify (`main.forecastDriven`).
- "X cannot be resolved to a variable" when X is a function → missing `()`.
- Experiments do NOT read Main's parameter defaults — a Parameter-Variation experiment has its
  OWN parameter values (Freeform expression). Change scenario there, not on Main. Two arms
  producing identical results = this, almost always.

## Statistics & experiments
- Collect per-run outputs in the experiment's **After simulation run**: `statX.add(root.kpi())`.
- PLE `StatisticsDiscrete` has NO `confidence()` — compute CI manually:
  `t * stat.deviation() / sqrt(stat.count())` with t=2.045 for N=30 (df=29, 95%).
- Compare policies with **common structure**: same seeds count, same window, toggle ONE thing.
  Report mean ± CI; overlapping CIs = "no significant difference" — say so honestly.
- Warm-up: either subtract a warm-up window or state that startup transients are included.

## Calendar & run control
- Real dates: set Start date in the Simulation experiment; display with
  `new java.text.SimpleDateFormat("EEE dd MMM yyyy HH:mm").format(date())`.
- User-chosen run length: `getEngine().setStopTime(simDays * 24.0);` in On startup.
- Start paused for scenario setup: a Timeout event at t=0 with
  `viewArea.navigateTo(); getEngine().pause();`. Buttons: `getEngine().run()/pause()/stop()`.

## Dashboard idioms
- Dynamic Text = the `=` button; without it the expression shows as literal code.
- View Areas are named bookmarks; `va.navigateTo();` on buttons = tab navigation. Create the
  View Area BEFORE the button that references it.
- Rectangles behind content: right-click → Order → Send to Back, then Locking → Lock.
- Variables/parameters never render at runtime — organise them in labelled zones for readers.
