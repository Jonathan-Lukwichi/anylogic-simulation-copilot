# Pattern card — Pedestrian Elevator in Omniverse
- **Source:** AnyLogic example model "Pedestrian Elevator in Omniverse" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (Pedestrian Library + Omniverse Connector code API)
- **Problem it solves:** Keep an NVIDIA Omniverse (USD) scene in step with a pedestrian elevator — cabin movement, cabin door and per-floor landing doors — using code rather than the connector's property UI.

## Structure
Same logic as the plain "Pedestrian Elevator" demo: `PedSource` → `PedElevator` (to `ped.targetShop.getLevel()`) → `PedWait` shopping `triangular(10, 30, 60)` min → `PedElevator` back to the first floor → `PedGoTo` exit → `PedSink`. Main holds an **Omniverse Connector** (scene path `omniverse://localhost/…/ElevatorAssets/scene.usd`, connection password). *On startup* wires the elevator to the USD scene in code.

## Resources
n/a

## Key settings worth copying
- `getUsdContext()` (available from any agent) returns the USD context; `context.createUsdRepresentation(element, "/World/scene/cage")` binds a model element to a prim and, for an elevator, returns an **`ElevatorUsdRepresentation`**.
- Doors are driven through USD **variant sets**: the demo calls `setCabinFrontDoorVarset("door_state")` for the cabin, `setGatePathProvider(i -> "/World/scene/gate_0" + i)` to map floor index → landing-gate prim, and `setGateFrontVarsetProvider(...)` for the landing doors' variant set (these three names come from the 8.9.10 demo).
- General updaters (Help *Omniverse API*): `addUsdRepresentation(rep)`, `addAttrUpdater(attrName, valueFn)` and `addVariantUpdater(varsetName, variantFn)` (both also with a path inside the prim) — push any agent state (colour, load type, open/closed) to the scene.
- **Coordinate mapping:** the connector's *Transform coordinates globally* fields (dX/dY/dZ, rotation, scale) may use the built-in `position` variable; the sibling demo **Overhead Crane in Omniverse** fills dX/dY/dZ with `position.x*9`, `position.y*9`, `position.z*9`. In code: `getUsdContext().setGlobalCoordinateTransform(Position)`.

## KPIs instrumented
n/a — visualisation link; the AnyLogic model keeps its own statistics.

## Pitfalls
- The scene assets must first be copied to an Omniverse **Nucleus** server and the path must start with `omniverse://`; a local file path will not link (model description).
- Help advises applying scaling and coordinate transforms on the AnyLogic side, not in Omniverse, and not scaling/rotating prims that are bound to model elements (group them under an intermediate prim instead).
- Variant names returned by providers must exist in the USD variant set, or nothing changes in the scene.

## Reusable idea
Treat Omniverse as a view: bind each AnyLogic element to a prim with `createUsdRepresentation`, express discrete visual states as USD variant sets, and compute them from model state with variant updaters — the simulation logic stays untouched.

## When the co-pilot should use this
Digital-twin demos that must show elevators, doors or state changes in Omniverse; questions on the Omniverse code API or on coordinate/scale mismatches. For the connector UI with a crane see `jib-crane-in-omniverse.md`.
