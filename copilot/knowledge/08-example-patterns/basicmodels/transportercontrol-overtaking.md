# Pattern card — TransporterControl Overtaking
- **Source:** AnyLogic example model "TransporterControl Overtaking" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Let path-guided AGVs drive around a vehicle that has stopped to unload, instead of queueing behind it, and keep line-side stations supplied by a reorder point.

## Block chain
- **Production line:** `Source` (10 items/min, pull) → `Convey` (round the conveyor loop, 7 simple stations) → `Sink`.
  Each station's *On process started* calls `correctPartsAvailability(station)`.
- **Replenishment:** `Enter` `partsAtStore` → `Queue` → `MoveByTransporter` `toLine` (to the conveyor, load 5 s, keeps
  the AGV) → `MoveByTransporter` `toStation` (destination type **conveyor station**, no seize, unload 15 s) → `Sink`.
- **Stock logic (functions on Main, state in a `StationArea` agent per station):** each process start uses one part; at
  zero the station is stopped with `station.fail()`; when the buffer falls to `reserveStockNumber` (3) and no order is
  open, `partsAtStore.take(new StationOrder(area))` places one. Delivery (*On unloading finished*) adds a batch of
  `uniform_discr(6, 15)` parts and restarts a stopped station with `repair()`.

## Resources
`TransporterFleet AGVs`: 7 path-guided AGVs (0.8 × 0.5 m, 1.3 m/s, 0.5 m minimum distance), 7 home nodes,
`setCargoPosition(0, 0, 0.3, METER)`. One `TransporterControl` block governs routing.

## Key settings worth copying
- **Blocked-path list:** a collection `blockedPaths`; TransporterControl *Avoid paths* =
  `blockedPaths.toArray(new Path[0])` (type `Path[]`, re-evaluated when a route is planned).
- **Detect the stop:** TransporterControl *On enter path* (`unit`, `path`): if `unit.getState() ==
  TransporterState.DELIVERING`, start a zero-delay dynamic event with the path, the AGV and its order
  (`(StationOrder) unit.getServicedEntity()`).
- **Block and reroute:** the event checks that the path is the order's unloading path, adds it to `blockedPaths`, then
  calls `recalculateRoute()` on every other AGV that has a route (`getRouteData() != null`) with more than one movement
  left.
- **Unblock:** `toStation` *On unloading finished* removes the path from the list after topping up the buffer.
- Each station area carries its own unloading path (`agvPath`) as a parameter, so the logic works for any number of
  stations.

## KPIs instrumented
Visual only. Add: time each station stands starved, reroutes per hour, order lead time (order → delivery), AGV utilization.

## Pitfalls
- **Planned routes do not see later changes.** A new avoid entry affects routes planned afterwards; vehicles already on
  their way keep their route unless you call `recalculateRoute()` — which only works while the vehicle is moving
  (DELIVERING, GOING_TO_AGENT, GOING_HOME; Help 8.9.10, *Transporter API*).
- **The layout needs a bypass.** Avoiding the only path to a node makes it unreachable; draw passing lanes where you
  want overtaking *(inferred)*.
- **Starvation is booked as failure.** `fail()`/`repair()` put the station in the failed state and feed its reliability
  statistics (G43). Report starved time separately, or use a counter, if MTBF/MTTR are needed.
- The zero-delay event keeps the rerouting out of the path callback of the moving AGV *(design reading, not stated in
  the model)*.

## Reusable idea
Turn temporary obstacles into routing data: maintain a live list of paths to avoid, feed it to TransporterControl, and
re-plan the vehicles already moving whenever the list changes. The same hook blocks aisles for maintenance, spills or
one-way time windows.

## When the co-pilot should use this
AGV systems with line-side unloading, narrow aisles where a stopped vehicle blocks traffic, temporary closures, and
reorder-point replenishment of conveyor stations. Related: `custom-routing-for-transporters.md` (custom routes),
`../videos/mhl-agv-dispatch-choice-and-cargo-position.md` (dispatch rules), `stacker-crane-store.md`
(`disableCollisionAvoidanceInNodes`).
