# Pattern card — Steel Converter Process
- **Source:** AnyLogic example model "Steel Converter Process" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (statechart agents plus a central controller, no process blocks)
- **Problem it solves:** Dispatch several overhead cranes that share one runway (so they cannot pass each other) to move ladles between converter transfer cars, continuous casting machines (CCMs) and outgoing cars. The aim is to keep the casters pouring without interruption.

## Structure
- **Incoming transfer car** (statechart): wait for converter steel (the `converterGenerator` event sets `canPourout`) → fill → go to the IPM station and wait `1 + weight / IPMProcessSpeed` → go to the crane zone. On entering *waitCrane* it calls `cranesController.addTask(TO_CCM, getIndex(), LinePosition, ladle)`; it leaves on "PICKED".
- **CCM** (turret with two ladle seats):
  - rotate (swap seats) → pour for `weight / PouroutSpeed` (adds to `steelProduced`);
  - when a ladle runs out: if the other seat holds a full ladle (`leftLadle != null && leftLadle.full`), rotate again, otherwise **stop**;
  - a stopped caster needs `triangular(5, 7, 10)` min before it can rotate again, then waits for a ladle if none has arrived;
  - on entering *pouring* it asks for the empty ladle to be taken away (`TO_TRANSCAR` task).
- **Crane:** waitTask → on "NEW TASK": two-leg move to the pick-up → *branch* (a pure MOVE task ends here and the crane is released) → load (1 min) → two-leg move to the drop-off → unload (1 min). It then hands over with `statechart.fireEvent(ladle)` to the CCM or car and calls `releaseCrane(this)`.
- **`Mover`:** a small reusable agent for piecewise-linear 2D motion. Its *after move* callback fires `"ARRIVED"` into the owner's statechart.
- **`CranesController`:** lists `tasks`, `freeCranes` and `busyCranes`. `runTaskDistributer()` is called on every change: new task, crane released, caster restarted, car arrived.

## Resources
Cranes (agents with lifting capacity and axis speeds), CCM ladle seats, and incoming/outgoing transfer cars. Task types: `NONE`, `TO_CCM`, `TO_TRANSCAR`, `MOVE`.

## Key settings worth copying
- **Three-way match.** For each waiting task (oldest first), find:
  - a crane that can lift the ladle plus steel, whose runway span is free and whose way can be cleared;
  - a target (a CCM that is not stopped, has a free seat and is not already claimed, or an empty outgoing car) under the same span tests.

  Claim the target (`seized = true`), load the crane's task, move it from free to busy, and fire "NEW TASK".
- **Runway interval reservation.** A busy crane reserves the whole runway interval of its task, from pick-up to drop-off. `isFreeZone(a, b)` rejects any interval that overlaps a busy crane's reservation.
- **Push idle cranes aside.** `clearWayIfPossible(a, b, self)`:
  - takes the idle cranes parked inside [a, b] and moves the nearest one just past b (± `SPACE_BETWEEN_CRANES`);
  - gives it a `MOVE` task, which reserves that interval too;
  - applies the same clearing rule to its own path first, so the check chains down the runway.
- **Simultaneous-axis travel with one mover** (`makeFirstMove`). The first leg moves diagonally until the faster axis is done, and the second leg finishes the other axis. Travel time then equals the maximum of the two axis times, as with independent bridge and trolley drives.
- **Caster continuity as the KPI.** Each CCM's `utilDataset` is a *continuous* Statistics element. It gets `add(1, time())` when rotating or pouring starts and `add(0, time())` when the caster stops or waits. Its `mean()` is therefore the time-weighted share of time casting (Help *Statistics*), shown per CCM and per crane in bar charts.

## KPIs instrumented
Time-weighted utilisation per CCM (continuity) and per crane, and total steel produced.

## Pitfalls
- **The duplicate check does not work.** `addTask` guards with `tasks.contains(newTask)`, but `Task` does not override `equals`. The check compares object identity and never matches a freshly built task (inferred from Java semantics). Compare by code, number and ladle if duplicate requests are possible.
- **The heuristic is greedy.** The model's own description says it is known to be sub-optimal in some configurations. First-fit crane choice, oldest-task-first order and a fixed push distance can leave a caster starving while a crane sits idle behind a reservation. Compare it against at least one alternative rule before concluding anything about crane count.
- **Reservations are coarse.** A busy crane holds its whole pick-up-to-drop-off interval until the task ends, even the part it has already passed, which understates runway capacity. Its approach leg to the pick-up is checked when the task is assigned but is not reserved afterwards.
- **Pushes cost time.** Moving an idle crane creates a `MOVE` task that itself holds a reservation. Count these moves, or crane utilisation will look like productive work.
- **Built-in first.** For material-handling cranes, the MHL overhead crane with several bridges already resolves runway conflicts by priority, pushing lower-priority bridges aside (Help *Overhead crane*; `basicmodels/crane-system-with-multiple-bridges.md`). Hand-code a controller like this one only for custom rules, multi-resource matching (crane × ladle × target) or non-MHL movers.

## Reusable idea
For several movers on one shared track:
- keep free and busy lists plus a task list in one controller;
- make matching a function that is re-run on every state change;
- give each busy mover a reservation interval on the track;
- let a new task proceed only if its interval is free, after pushing idle movers out of the way.

Hand-offs are statechart events, and the KPI that matters is the time-weighted continuity of the bottleneck (the caster), not crane utilisation.

## When the co-pilot should use this
- **Use cases:** steel melt shops and ladle logistics, several gantries or shuttles on one rail (warehouses, container yards, AGVs on a single lane), and any scheduling of non-passing movers.
- **Typical question:** "how many cranes do we need so the casters never stop?"
- **Related cards:** `bigbook/abm-design-recipe-states-messages-and-dispatcher.md` (a dispatcher written as functions) and `bigbook/statechart-message-queue-and-safe-handoff.md`.
