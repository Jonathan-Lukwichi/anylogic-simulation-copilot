# Pattern card — Order Picking Line
- **Source:** AnyLogic example model "Order Picking Line" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling + Process Modeling) with replicated station agents
- **Problem it solves:** A pick-to-box conveyor line whose number of identical picking zones is a single parameter — no copying of stations, no rewiring when the count changes.

## Block chain
- **Main:** `Source` (20 boxes/min, `newEntity = getBox()` stamps a random zone number and colour) → `Convey` from the infeed conveyor **directly to** `pickingZones.get(agent.pickingZoneNumber).pickingConveyor` → `Exit` (*On exit*: `pickingZones.get(n).enter.take(agent)`). Outbound: the zones' `outPort` → `Convey` from current position to the **last** zone's `takeawayConveyor` → `Sink`.
- **PickingZone (population of `nZones`, placed at x = 180·index):** replenishment `Source` (manual, 100 items injected at start) → `Store` (no resource) → `Wait` → `Retrieve` (picker from the zone's `ResourcePool`) → `Service` (picker, `uniform(3, 5)` s, queue capacity 1; *On exit* injects one replacement item) → `Pickup` (exact quantity). The box from `Enter` is the container; *On pickup* sends `"close"` to it, and the box's statechart swaps its 3D shape from open to closed.

## Resources
One `picker` ResourcePool per zone (home at the zone's workplace).

## Key settings worth copying
- **Chain replicated segments with a port parameter:** each zone has a Network Port whose *paired port* is its parameter `infeedingPort`, set per index by `getInfeedingPort(index)` — zone 0 pairs with the port at the end of Main's infeed conveyor, zone *i* with the outgoing port of zone *i − 1*. All zone conveyors then form one logical conveyor line.
- Because the line is one network, a single `Convey` in Main can route to a conveyor *inside* any zone agent and on to the last zone's takeaway conveyor.
- Population size = parameter `nZones`; per-zone data from index-based collections (`zoneColors.get(index)`).
- `Pickup` *Pick from* = **Specified Queue object** (`queueIsConnectedToPort = false`): the queue can be chosen per container, instead of the block wired to `inPickup`.

## KPIs instrumented
Visual (logic view, per-zone 3D views with next/previous navigation).

## Pitfalls
- The pairing expression must cover every index, including the first zone (it pairs with a Main port, not a zone port); a gap breaks the line and `Convey` finds no route.
- Zone *i*'s parameter reads `pickingZones.get(i - 1).outputPort`, i.e. an earlier member of the same population — it works because members are created in index order. Never point a member at a *later* index (that agent does not exist yet when the parameter is evaluated) *(ordering inferred from the demo)*.
- Layout positions come from the population's initial location (`180 * index`) — keep them consistent with conveyor lengths, or ports end up far apart.

## Reusable idea
For any line of identical cells (picking zones, test benches, packing stations), build one cell agent with its conveyor/path pieces and ports, replicate it N times, and compute each copy's paired port from its index. N becomes an experiment parameter for line-balancing studies.

## When the co-pilot should use this
Line-length or station-count what-ifs, pick-to-box / zone-picking lines, and whenever a user copies the same station by hand. For stitching different sub-models see `models/fulfillment-center-conveyor-system.md`; for dynamic port references see `videos/multi-level-facility-lift-landings.md`.
