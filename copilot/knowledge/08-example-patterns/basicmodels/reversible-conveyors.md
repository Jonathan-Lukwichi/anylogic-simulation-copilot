# Pattern card — Reversible Conveyors
- **Source:** AnyLogic example model "Reversible Conveyors" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Serve dead-end work stations beside a main line through one short reversible conveyor each — the same belt feeds the item in and brings it back out — and keep items from heading to a station that is already busy.

## Block chain
`Source` (10 per minute, 1 m items) → `ConveyorEnter` (main conveyor) → `Convey` "to turntable" (target = the chosen station's main-line conveyor) → `SelectOutput` "can enter?" (`!agent.targetStation.occupied`)
- **false:** *On exit false* calls `agent.reevaluateStation()` (next station, round robin) and the item goes back into "to turntable".
- **true:** `Convey` "to station" (target = the station's reversible conveyor; *On enter*: `occupied = true`) → `MoveTo` (*place to* the station node) → `Delay` (7 s, the process; *On at exit*: recolour the item and `stationConveyor.changeDirection()`) → `Convey` "to exit" (source = the station conveyor, offset from its end; target = exit conveyor; *On enter*: `occupied = false`) → `Sink`.

## Resources
n/a. Three stations, each a turntable on the main line + a reversible stub + a node at its end.

## Key settings worth copying
- **Station descriptors as a population:** `sideStations` (type `SideStation`, parameters `magistralConveyor`, `stationConveyor`, `stationNode`, variable `occupied`) is created with parameters `magistralConveyors.get(index)`, `stationConveyors.get(index)`, `stationNodes.get(index)` — three collections on Main listing the markup in the same order. N identical markup groups get one piece of logic; the item keeps a reference `targetStation` (initially `main.sideStations.get(0)`).
- **Revert only after the item has left:** each stub conveyor's *On trailing edge exit* runs `if (!runsForward) self.changeDirection();` — `runsForward` tells the current direction, and the trailing edge proves the whole item is off the stub.
- **Why a node and a Delay, not a Station:** an MHL Station cannot sit on a reversible conveyor (`videos/mhl-conveyor-station-processing-and-reassembly.md`).
- **What a direction change does (Help 8.9.10, *Reversible conveyor*):** the belt decelerates to 0 (if deceleration > 0), flips, fires *On direction changed*, cancels the movement of the items on it — they leave their `Convey` through `outRedirect` — then accelerates the other way. A stopped or failed belt flips at once. `setDirection(CONVEYOR_FORWARD | CONVEYOR_BACKWARD)`, `getDirection()`, `isChangingDirection()`; calling `changeDirection()` while decelerating cancels the pending flip.
- **Routing with reversible belts (Help):** automatic routing only (not *Sequence of conveyors*); routes use the belts' current directions; a route that must use a belt in the wrong direction waits in front of it. If the **source** belt runs the wrong way the item does not enter `Convey`; a direction change after departure does not reroute — call the item's `conveyTo()`.

## KPIs instrumented
Colour change on processed items only. Add station utilization (time `occupied`), redirect count (items sent round again), and main-line recirculation time.

## Pitfalls
- **Occupancy must be claimed before the trip**, as here (`occupied = true` when entering "to station"); a check alone lets two items head for one dead end.
- **Runtime errors (Help):** an item straddling a conveyor point node between a reversible and a one-way belt when the direction flips, an item long enough to lie on two belts that start moving in opposite directions, or an item on a spur element at the flip.
- Busy stations make items circulate; without a limit they can clog the main line. Cap recirculation or add a buffer spur (`basicmodels/item-flow-control-on-a-reversible-conveyor-spur.md`).
- Release notes 8.8.0 fixed items stuck at spurs leading to reversible belts and items not leaving a reversible belt at the end of their route — avoid older versions for this layout.

## Reusable idea
A reversible stub turns a two-way connection into one belt: flip it when work ends, flip it back from the trailing-edge callback. Bind repeated markup groups to logic through a population of descriptor agents built from ordered collections.

## When the co-pilot should use this
Side workstations, inspection or rework cells off a main conveyor, dead-end lanes in sortation, or buffers that fill and drain through one belt. Direction-change basics and `outRedirect`: `videos/mhl-convey-routing-offsets-leave-on-exit.md`; buffer spur logic: `basicmodels/item-flow-control-on-a-reversible-conveyor-spur.md`.
