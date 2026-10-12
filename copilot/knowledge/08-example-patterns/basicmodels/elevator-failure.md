# Pattern card — Elevator Failure
- **Source:** AnyLogic example model "Elevator Failure" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Break a pedestrian lift at an arbitrary moment and handle everyone affected — people waiting on the landings, people inside the cabin, and people who arrive while it is broken — then repair it.

## Block chain
`PedSource` (custom population; `target` = a random floor entrance other than the first floor) → `PedElevator` (target level `ped.target.getLevel()`; *exit on timeout* with timeout `elevator.isFailed() ? 10 : 600` s) → `PedSelectOutput` (did the cabin stop on the target floor?) → `PedGoTo` target → `PedSink`; otherwise `PedGoTo` the entrance on the lift's current floor → `PedSink`.
- `ccl` (cancelled while waiting) → `PedGoTo` first-floor entrance → `PedSink`.
- `outT` (timed out, i.e. arrived while broken) → `PedGoTo` stairs → `PedSink`.
- **Rescue branch:** PML `Enter` → `Delay` *wait for mechanic* (triangular 1 / 3 / 5 min) → `PedEnter` at a point on `elevator.getCurrentLevel()` → `PedGoTo` nearest exit on that floor → `PedSink`.

## Resources
One Elevator markup serving four levels; its platform colour shows `isFailed()`.

## Key settings worth copying
- **Break button:** `pedElevator.cancelAll()` first (only people not yet aboard can be cancelled); then, if the cabin is not moving, `dropOffPeds(getPeds())` and `fail()`. If it is moving, either `fail()` at once (stuck between floors) or, with the "generator" option, `moveTo(getNearestLevel(), false)` and, in the elevator's *On level arrival* action, drop everyone off and call `fail()`.
- **Rescue button:** copy `elevator.getPeds()` into a new set, then for each person `pedElevator.remove(p)` and `enterToWaitMechanic.take(p)`; `PedEnter` later puts them back into the building on the cabin's level.
- **Repair button** (enabled only when the cabin is empty and nobody is waiting for rescue): `repair()`, then `setManualMode(false)` if manual mode is still on.
- Help 8.9.10 (*Elevator*, *PedElevator*): `fail()` stops the lift, admits nobody and keeps riders inside until `repair()`; *On failed* / *On repaired* callbacks; after repair it continues its direction if requests remain, otherwise a cabin stuck between floors goes to the nearest level. **No automatic removal of pedestrians on failure** — the modeller must do it.
- **`cancel` vs `remove`:** `cancel(ped)` works only for someone not yet in the cabin (error otherwise) and `cancelAll()` releases only those not yet aboard (Javadoc) — both exit through `ccl`; `remove()` works in any phase, also takes them out of the cabin and the space, and needs `PedEnter` to bring them back.

## KPIs instrumented
Visual only. Useful: `elevator.timeInState(ElevatorState.FAILED, MINUTE)`, `countPedsTimeout()` of the PedElevator (people sent to the stairs), rescue waiting time.

## Pitfalls
- **Enum names:** write `ElevatorState.MOVING` / `IDLE` / `LOADING` / `FAILED` (engine Javadoc and this model); the Help tables print `ELEVATOR_STATE_…`, which is not the 8.9.10 constant name.
- **Ghost stops:** a queued call is always served, even if its caller has left through `ccl` (Help, *Elevator control system*); after mass cancellation use `deleteCallsOnLevel(level)`.
- **Manual mode sticks:** `moveTo(level)` switches the lift to manual mode and it stays there unless you pass `false` or call `setManualMode(false)` — a repaired lift in manual mode ignores calls.
- Iterate over a copy of `getPeds()` when removing people — the live set changes under the loop.
- The timeout expression is read per person when they enter *(inferred from the model's description)*: people who came before the failure keep the long timeout — the demo cancels them instead.

## Reusable idea
Treat an equipment failure as three populations to route explicitly — queued, on board, arriving — each with its own exit port or rescue flow; PedElevator gives each group a distinct handle (`ccl`, `remove`, `outT`).

## When the co-pilot should use this
Evacuation and resilience studies with lifts, hospital or station accessibility when a lift is out of service, reliability what-ifs. Related: `pedestrian-elevator.md` (basic set-up), `elevator-manual-control.md`, `elevator-connecting-floors-defined-by-different-agents.md`.
