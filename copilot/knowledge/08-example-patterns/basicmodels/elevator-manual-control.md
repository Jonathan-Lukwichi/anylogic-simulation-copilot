# Pattern card — Elevator Manual Control
- **Source:** AnyLogic example model "Elevator Manual Control" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Replace the built-in lift controller with your own logic — which floor to visit next, whom to pick up, where to let people out — for custom dispatch or emergency modes.

## Block chain
`PedSource` (100/h at the first-floor entry) → `PedElevator` (*Pedestrian is transferred: using elevator API*, `TRANSFER_MODE_MANUAL`; no target level) → `PedGoTo` the exit line on the floor where the cabin now is (`findFirst(exitLines, e -> e.getLevel() == elevator.getCurrentLevel())`) → `PedSink`.
Main's *On startup*: `elevator.setManualMode(true)`. Three buttons drive the lift:
- pick up: `elevator.pickUpPeds(elevator.getWaitingPeds(elevator.getCurrentLevel()))`;
- drop off: `elevator.dropOffPeds(elevator.getPeds())`;
- go: `elevator.moveTo(elevator.accessibleLevels()[selectedFloorNumber])`, the index set by radio buttons.

## Resources
One Elevator markup on four levels.

## Key settings worth copying (Help 8.9.10, *Elevator* → *Manual control mode*; *PedElevator*)
- Two independent switches: the **elevator** in manual mode moves only on `moveTo`, and the **block** in *using elevator API* mode lets people board and alight only on `pickUpPeds` / `dropOffPeds`. The demo uses both; *automatically* transfer with a manual-mode lift is the other combination.
- Built-in controller for reference: *Selective Collective Operation* — keep direction while requests lie ahead, then reverse or stop.
- Manual commands outrank automatic ones (Help), so an emergency routine can take over a running lift. `moveTo(level)` switches to manual by itself; `moveTo(level, false)` hands control back after arrival.
- Controller inputs: `getWaitingPeds(level)`, `getPeds()`, `getCalls()`, `getRoute()`, `getTargetLevel()`, `getNearestLevel()`, `getCurrentDirection()`, `getState()`; `accessibleLevels()` is sorted by Z.
- Statistics stay available: `utilization()`, `meanWaitingTime(level, MINUTE)`, `nTransportedPeds()`, `nPickedUpPeds(level)`, `nDroppedOffPeds(level)`.

## KPIs instrumented
None on screen; the statistics above let two controllers be compared on waiting time and utilisation.

## Pitfalls
- `pickUpPeds` accepts only people on the cabin's current level and errors if the cabin is between levels; call it from the arrival moment (e.g. the elevator's *On level arrival*, which also receives `waitingAgents`).
- `dropOffPeds(getPeds())` unloads everyone on the current floor, whatever their destination. A real controller filters by each person's own target (keep it in the pedestrian, e.g. a target line or level) and drops only those bound for this floor.
- In *using elevator API* mode nothing happens without commands: a controller that misses an event leaves people waiting forever, with no error. Drive it from events (*On level arrival*, a cyclic check), not only from buttons.
- `accessibleLevels()` indexes by height, not by name; map floor numbers deliberately.

## Reusable idea
Keep dispatch rules (destination dispatch, zoning, up-peak parking at the lobby, fire-service recall) in a controller function fed by the elevator's queries, and compare it with the built-in controller on the same arrival stream — the lift's statistics work in both modes.

## When the co-pilot should use this
High-rise or hospital lift studies where the dispatch policy is the question; emergency or evacuation modes; any request to "control the elevator from code". Related: `pedestrian-elevator.md`, `elevator-failure.md`.
