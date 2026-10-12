# Pattern card — Transporter Charging System
- **Source:** AnyLogic example model "Transporter Charging System" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (DES Material Handling + Fluid Library battery inside each vehicle)
- **Problem it solves:** Model how battery charging steals capacity from an AGV and forklift fleet: opportunity charging between jobs, forced charging below a critical level, and technician-served battery swaps.

## Block chain
- **AGV flow:** `Source` (2 per min; `new Production(randomFrom(stationPoints), randomFrom(deliveryPoints))`) →
  `MoveByTransporter` (fleet `agvFleet`, to the item's delivery point; *On downtime* = *transporter finishes its task*)
  → `SelectOutput5` (by delivery point) → three permanent `Batch`es of `nItemsOnPallet` at buffer nodes.
- **Forklift flow:** pallets → `Store` (fleet `forkliftFleet`, random slot, at downtime `TPP_NO_PREEMPTION`) → `Delay`
  `triangular(6, 10, 15)` h → `Retrieve` → `Sink`.
- **Battery inside each AGV:** `FluidSource` (charger, 5 L/s) → `Valve` accumulate (closed at start) → `Tank` battery
  (1,000 L) → `Valve` consume (1 L/s, open) → `FluidDispose`. `startCharging()` opens accumulate and closes consume;
  `stopCharging()` does the reverse.

## Resources
- `agvFleet`: 5 AGVs, each home node is a charger; `downtimes = { criticalLevelCharging, opportunityCharging }`.
- `forkliftFleet`: 2 free-space forklifts, 0.7 m/s; `downtimes = { forkliftBatterySwap }`.
- `technician`: ResourcePool of 1 at the technician's location.

## Key settings worth copying
- **Opportunity charging** (Downtime): trigger *Working time between occurrences* 15 s; *Task type* = *Delay until
  stopTask() is called* (`TASK_WAIT_CALLBACK`); *At downtime equipment* = returns home (`MBD_RETURN_HOME`); usage counted as
  **idle**; priority **−1**; preemption policy **Terminate**; On start / On finish / On terminate → start / stop charging.
  Priority −1 means it only starts when no job waits, and any job (priority 0) ends it.
- **Critical charging** (Downtime, no triggers): the battery Tank's *On below* (level = capacity × 0.2) calls
  `main.criticalLevelCharging.startTask(this)`; duration `unit.timeToCharge()` = (capacity × 0.3 − amount) / charge
  rate; priority 1, *May preempt*; On finish stops charging and calls `opportunityCharging.startTask(unit)` so the AGV
  keeps charging if idle.
- **Battery swap** (Downtime on forklifts): every 3 h of working time, first one after `triangular(0.1, 0.5)` h of work
  (staggered); *Delay with resources* `triangular(7, 10, 15)` min with the technician sent over; the forklift goes to the
  charging room (`MBD_GO_TO`); priority 1.
- A job already under way decides what downtime does to it (Help 8.9.10, *MoveByTransporter* → *On downtime*):
  `PP_WAIT_FOR_ORIGINAL` (default), `PP_SEIZE_ANY_RESOURCE`, `PP_NO_PREEMPTION` (finish first), `PP_TERMINATE` (+ an
  Enter for terminated agents).

## KPIs instrumented
Battery gauge per AGV (colour by level, six bars). For a study add: time per vehicle in downtime states, number of
critical-charge events, battery level distribution, job waiting time, technician utilization.

## Pitfalls
- **Energy drains on a clock.** The consume valve is open whenever the AGV is not charging, so an idle AGV uses as much
  as a loaded one. Tie the consume rate to the vehicle's activity when energy matters.
- **An empty battery does not stop the vehicle.** The tank is bookkeeping; with *finish its task* on the job, an AGV
  can keep driving below critical and even at zero. Enforce a hard floor yourself if needed *(inferred from the model
  structure)*.
- `TASK_WAIT_CALLBACK` ignores the Task duration field (the demo's `100 //TODO` is a leftover); the task ends only by
  `stopTask(unit)`, by preemption (Terminate), or never. `stopTask` is ignored while the unit is still driving to the
  downtime location (Help).
- `startTask(unit)` exists in 8.9.10 (`javap`) but is missing from the Help's Downtime function table.
- *Usage statistics are* defaults to *not collected*; decide whether charging counts as idle, busy or excluded before
  reporting utilization. Fleet downtimes need **8.9.4+** (release notes).

## Reusable idea
Give each vehicle its own small fluid "battery" (source → valves → tank) and drive the charging policy with Downtime
blocks: a low-priority, terminable, callback-ended downtime for opportunity charging, and a level-triggered,
preempting one for mandatory charging. Swap the downtime set to compare charging strategies on the same job stream.

## When the co-pilot should use this
AGV and forklift fleets with batteries, charger-count and charging-strategy questions (opportunity vs threshold vs
swap), and any equipment whose availability depends on a consumable level. Related:
`maintenance-of-a-coffee-machine.md` (Downtime types), `station-and-crane-maintenance.md`, `tank.md`, `valve.md`.
