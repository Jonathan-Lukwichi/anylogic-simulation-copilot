# Pattern card — Pedestrian Elevator
- **Source:** AnyLogic example model "Pedestrian Elevator" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Move pedestrians between floors of a building by lift, with each pedestrian's destination floor derived from where it wants to go.

## Block chain
`PedSource` (100/h at the ground-floor entry line; custom population `pedestrians` whose parameter `targetShop = randomFrom(shopAreas)`) → `PedElevator` (elevator `elevator`, **target level = `ped.targetShop.getLevel()`**) → `PedWait` *shopping* (in `ped.targetShop`, `triangular(10, 30, 60)` min) → `PedElevator` *toFirstFloor* (target level `first_floor`) → `PedGoTo` exit line → `PedSink`.

## Resources
One **Elevator** space-markup element drawn on the first floor and serving the building's levels; *Minimum stay time* 15 s; doors: front.

## Key settings worth copying
- Elevator markup (Help 8.9.10): *Capacity* (pedestrians per trip); movement by **speed** or **time per level**; *Minimum stay time* — the cabin stays at least this long at a stop, longer if boarding/alighting is not finished; *Stops at* all or selected levels; doors *front* or *front/rear*.
- Put the destination in the agent (an `AreaNode` parameter) and derive the floor from it with `getLevel()` — one PedElevator block then serves every floor.
- If the target level equals the pedestrian's current level, PedElevator lets it straight through without calling the lift (Help) — no special case needed for ground-floor shops.
- Floor-by-floor 2D view: a function that loops over the model's `Level`s and calls `setVisible(l == chosen)`; the 3D view shows all levels.

## KPIs instrumented
Visual only.

## Pitfalls
- The elevator must be configured to serve every level a pedestrian can target; otherwise pedestrians cannot be transferred.
- A generous *Minimum stay time* quietly caps lift throughput (every stop costs at least that long); calibrate it together with capacity and speed before judging queues at the landings.

## Reusable idea
Keep "where to go" as agent data (target area), let the lift block compute the floor from it, and reuse a single PedElevator for all trips; use per-level visibility for readable 2D multi-floor animation.

## When the co-pilot should use this
Shopping centres, offices, hospitals, stations with lifts in pedestrian models. For manual lift control, lifts spanning floors that live in different agents, or lift failures see the `elevator-*` cards (batch m-basic-1); for Omniverse visualisation see `pedestrian-elevator-in-omniverse.md`.
