# Pattern card — Moving Transporter without Flowchart Block
- **Source:** AnyLogic example model "Moving Transporter without Flowchart Block" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Drive a transporter from code in the gaps between flowchart moves — pre-position it before it is needed, keep moving while its load is being processed, or park it while the load is with a crane — then hand control back to the flowchart.

## Block chain
`Source` (manual; one item at a time, re-injected from the Sink) → `Convey` (to a conveyor station, 30 s process) → `MoveByTransporter` *toStation* (seize at the pickup node, `releaseTransporter = false`) → `Service` *inspection* (static inspection device, 30 s, `restoreEntityLocationOnExit = false`) → `MoveByCrane` *toTank* (`releaseCrane = false`) → `Delay` *dipping* 10 s → `MoveByCrane` *fromTank* (`seizeCrane = false`) → `Delay` *beingTransported* (manual) → `MoveByTransporter` *moveToTarget* (`seizeTransporter = false`) → `Sink`.

## Resources
One free-space AGV (`TransporterFleet`, custom population `AGV`, acceleration 2 m/s², deceleration 0.5 m/s²); one crane; one inspection device.

## Key settings worth copying
- **Pre-position (idle vehicle):** conveyor station *On process started* → `AGV.get(0).move(waitAtConvPoint)` — the AGV is already at the pickup point when the item leaves the station.
- **Move while the load is processed:** Service *On enter delay* → `setMaximumSpeed(0.2, MPS)` so the trip lasts about as long as the process, then `move(node, TransporterState.DELIVERING)` — the item stays attached and rides along; *On exit* restores `setMaximumSpeed(1, MPS)`. Untick *Restore agent location on exit* so the item is not snapped back to where the Service started.
- **Move empty while the load is elsewhere:** dip-tank Delay *On enter* → `move(node, TransporterState.PROCESSING)` — the AGV drives off without its cargo (the crane holds it).
- **Keep the same vehicle across blocks:** `releaseTransporter = false` on one move, `seizeTransporter = false` on the next; same pair for the crane (`releaseCrane` / `seizeCrane`).
- **Manual control window:** while the item sits in the manual `Delay` *beingTransported*, clicking a machine calls `move(<machinePoint>, TransporterState.DELIVERING)`; a button `stopDelayForAll()` returns the item to the flowchart and to automatic routing.

## KPIs instrumented
Visual only.

## Pitfalls
- Only move by code a transporter that is idle or already seized by the item you are handling; moving a unit that a block is also routing gives conflicting commands.
- The `TransporterState` passed to `move(...)` decides whether the cargo travels with it (DELIVERING) and what time-in-state statistics record — pick it deliberately.
- A speed changed in code stays changed; restore it on the matching exit action.

## Reusable idea
Flowchart blocks own the vehicle only between *seize* and *release*; code can use the gaps. `move(target[, state])` + `setMaximumSpeed(...)` give look-ahead positioning and "process while moving" (inspection on board, curing, cooling in transit) without extra blocks.

## When the co-pilot should use this
AGV look-ahead or pre-staging, on-board processing during transport, user-directed (click) routing, or when a user asks how to move a transporter outside MoveByTransporter.
