# Pattern card — Elevator Connecting Floors Defined by Different Agents
- **Source:** AnyLogic example model "Elevator Connecting Floors Defined by Different Agents" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library, modular building)
- **Problem it solves:** Keep each floor of a building as its own agent type (own layout, own flowchart) and still run one lift through all of them.

## Structure
- Main embeds four single agents — `parkingFloor`, `groundFloor`, `restaurantFloor`, `observationDeckFloor` — each with its own level and markup, and one shared population `pedestrians` (`target` = a random destination area from Main's collection `areas`, which lists area nodes owned by the floor agents, e.g. `groundFloor.shop1`, `restaurantFloor.restaurantArea2`).
- **The one Elevator markup lives in `GroundFloor`.** Its *Stops at: selected levels* list mixes its own level with the others, referenced through Main: `main.parkingFloor.level`, `level`, `main.restaurantFloor.level`, `main.observationDeckFloor.level`.
- **GroundFloor flowchart:** `PedSource` (75/h, entrances of this floor, adds to `main.pedestrians`) → `PedElevator` (target level `ped.target.getLevel()`) → `PedWait` in `ped.target` (triangular 5 / 15 / 30 min) → `PedElevator` back to this `level` → `PedGoTo` exit → `PedSink`.
- **ParkingFloor flowchart:** the same shape (25/h), using `main.groundFloor.elevator`, plus a `PedService` pay station before leaving.
- A person started by one floor's flowchart may wait in an area that belongs to another floor agent; the flowchart owner and the level where the person stands are independent.

## Resources
One Elevator; a pay-station service on the parking level.

## Key settings worth copying
- Help 8.9.10 (*Elevator* → *Levels*): normally all levels sit in one agent; for a model decomposed into floor agents, select the served levels explicitly, including levels of other agents.
- Blocks in any floor agent reach the shared lift by path (`main.groundFloor.elevator`).
- One destination list at the top (`areas`) and `target.getLevel()` let every floor's flowchart send people anywhere in the building.
- Each floor agent carries `anim2DX` / `anim2DY` parameters to lay the floors side by side in Main's 2D view.

## KPIs instrumented
Visual only. The single population `main.pedestrians` makes building-wide statistics easy.

## Pitfalls
- The model's own description places the lift in the parking agent; in the 8.9.10 model it is in `GroundFloor`. Check which agent owns the markup before referencing it.
- Every level a person can target must be in the lift's list; a missing one leaves that person unable to be transferred.
- Cross-agent references (`main.x.level`) tie the floor types to Main; keep all floors as single agents of Main so the paths exist.

## Reusable idea
Build large facilities floor by floor as agent types (reusable, testable on their own) and stitch them with shared vertical transport whose level list spans agents. The same split works for multi-building campuses.

## When the co-pilot should use this
Malls, hospitals, stations or offices modelled per floor or per zone by different people; when a user asks how one lift can serve levels defined in different agents. Related: `pedestrian-elevator.md`, `videos/multi-level-facility-lift-landings.md`, `level-gate.md`.
