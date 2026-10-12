# Pattern card — Passing an Oncoming Transporter
- **Source:** AnyLogic example model "Passing an Oncoming Transporter" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Two path-guided AGVs meet head-on on a single-lane path; instead of the engine's automatic "drive through each other" resolution, one vehicle is routed into a spur (passing bay) and the other waits at the junction until the spur is occupied.

## Block chain
Two identical test rigs, each `Source` (every 3 min, at the left or right end node) → `MoveByTransporter` (seize at the pickup node, carry to the opposite end, return to nearest home) → `Sink`:
- **auto_…** blocks use fleet `autoRoutingTransporters` (automatic resolution);
- **custom_…** blocks use fleet `customRoutingTransporters`, governed by a `TransporterControl` with **Navigation = Custom** (`automaticNavigation = false`).

## Resources
Two fleets of 2 AGVs each (acceleration/deceleration 0 — constant speed for a clean comparison).

## Key settings worth copying
- **Automatic behaviour (Help 8.9.10):** with *Resolve collisions* on, vehicles meeting head-on stop at a node, wait the *Collision detection timeout* (default 10 s) and then **drive over each other** inside the node; with it off the run stops with an error. *Avoid collisions* only reduces conflicts by reserving contested paths; it does not guarantee avoidance. Only opposite-direction conflicts are resolved; same-direction followers simply queue.
- **Custom route (Route / `findPath`):** the first AGV to enter the corridor (remembered in a variable) gets `findShortestPath(source, target, null, null)`; the second gets a two-leg route built by concatenation — `findShortestPath(source, new LocationNode(spurNode), null, null)` then `.add(findShortestPath(new LocationNode(spurNode), target, null, null))`.
- **Hold at the junction (Can enter node):** return `false` for the first AGV at the node `intersection` while `spurPath.getNumberOfTransporters() == 0`; it proceeds as soon as the other vehicle is in the spur.
- **Release the token (On enter node):** when the first AGV reaches the intersection on its final movement (`unit.getRouteData().getMovements().size() == 1`), clear the variable.
- Other hooks available: *Can enter path*, *Avoid paths/nodes*, *Include paths*, *On enter/exit path*, *Routing policy* Shortest / Fastest / Custom.

## KPIs instrumented
Visual comparison of the two rigs.

## Pitfalls
- Automatic resolution is not physical: vehicles pass through one another after the timeout, so single-lane corridors, narrow aisles and one-way tunnels look fine in the model but are impossible in reality — and delays are understated. Use custom navigation (or one-way paths) for such layouts.
- A *Can enter node* rule that can stay false forever deadlocks the network; always pair it with a condition that the other vehicle's route guarantees (here: it enters the spur).
- Leaving the "first vehicle" token set (e.g. if its route changes) blocks the logic for all later vehicles.

## Reusable idea
Treat a single-lane section as a shared resource with a token: first comes first, the other is routed via a passing bay by concatenating shortest-path legs through a waypoint, and a node-entry guard holds the first vehicle until the bay is occupied.

## When the co-pilot should use this
Single-lane AGV corridors, passing bays, mine haul roads with pull-outs, narrow warehouse aisles — and whenever a user notices AGVs driving through each other. For general custom routing see `custom-routing-for-transporters.md`; for overtaking see `transportercontrol-overtaking` (batch m-basic-4).
