# Pattern card — Stacker Crane Store
- **Source:** AnyLogic example model "Stacker Crane Store" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Model an automated storage and retrieval system (AS/RS) whose aisles are served by stacker cranes, fed and emptied by conveyors or by AGVs, without building the cranes by hand.

This card also covers the sister example "Stacker Crane with Transporter" (basicmodels, 8.9.10).

## Block chain
- **Conveyor-fed (Stacker Crane Store):** `Source` (limited to `storage.capacity()` arrivals, pull protocol, agents that
  cannot leave wait) → `Convey` (main conveyor → the input conveyor of the rack that holds the box's reserved slot) →
  `Store` (*Agents move*: **by SRM**, *Specific slot* = the reserved slot) → `Delay` (dwell `triangular(0.5, 1, 1.5)` min)
  → `Retrieve` (by SRM) → `Convey` (that rack's output conveyor → exit conveyor) → `Sink`.
- **AGV-fed (Stacker Crane with Transporter):** `Source` at the AGV home → `MoveByTransporter` (to the rack's nearest
  crane input **node**) → the same Store / Delay / Retrieve → `Convey` from the conveyor that starts at the crane's output
  node → `Sink`. A `TransporterControl` block is present for one start-up call (below).
- **Reserve first:** in the Source's *On at exit*, `agent.reservedSlot = storage.getRandomAvailableSlot();` then
  `storage.setReservation(agent, agent.reservedSlot);` — the destination rack, and so the right crane input, is known
  before the box moves.

## Resources
- Storage markup: selective racks, back-to-back, 12 bays × 8 shelves, one cell deep, *Storage is served with* =
  **stacker cranes** → one crane per aisle (5 here), created by AnyLogic.
- Stacker Crane System (auxiliary markup, click any crane): single mast; *Input/Output system* = Conveyor (or Point node),
  input front-right, output back-left, with *Create conveyors/nodes* generating the stations.
- AGV variant: `TransporterFleet` of 5, max 2 m/s, one home node; `onNewTransporter` calls
  `unit.setCargoPosition(0, 0, 0.4, METER)`.

## Key settings worth copying
- Rack → station lookups (Help 8.9.10, *Storage*): `getNearestInputConveyor(rack)` / `getNearestOutputConveyor(rack)`,
  `getNearestInputNode(rack)` / `getNearestOutputNode(rack)` (also by `StorageCell`); all return null when nothing is
  reachable. `getInputConveyors()`, `getOutputNodes()` etc. list one station per active crane.
- Output node → conveyor: a `Map` filled on startup (`nodeToConveyor.put(exitNode1, exitConveyor)` …) turns the crane's
  output node into the `Convey` source conveyor.
- Shared AGV home: `transporterControl.disableCollisionAvoidanceInNodes(List.of(homeNode))` — vehicles heading to those
  nodes always enter and stop treating each other as obstacles there (Help, *TransporterControl*; API since 8.5.1).
- Store/Retrieve by SRM (Help, *Store*): *Load/unload mode* = time (Loading / Storing time) or transfer speed;
  *After release, SRM* = return home or stay; action *On seize SRM* (`unit`, `rack`).
- Crane speeds: *Travel*, *Lift*, *Transfer* speed; speed expressions may use `isLoaded` and `agent`.

## KPIs instrumented
Visual only. Per crane (`storage.getStackerCranes()`, Help *Stacker Crane System*): `getUtilization()`,
`averageStorageTime()`, `averagePickingTime()`, `numberOfAgentsHandled()`, `timeInState(state)`; plus the queue on each
input conveyor and box dwell time.

## Pitfalls
- **Version gate:** stacker cranes are a Storage option from **8.9.9** (release notes); 8.9.10 fixes a crane that could
  not store into middle racks with racks on both sides — build on 8.9.10.
- **Working area:** each crane serves only stations inside its working area; an item waiting elsewhere, or no suitable
  output station, raises an error. Only one input station per crane system (Help).
- **Generated stations are detached:** moving or resizing the Storage later does not move the generated conveyors or
  nodes. Conveyors cannot enter a crane aisle (the crane is an obstacle to them).
- Capping arrivals at `storage.capacity()` keeps `getRandomAvailableSlot()` from being asked for a slot that no longer
  exists *(what it returns when full: unverified)*.
- Keep the Source's *Agents which can't exit* on *wait in this block* when pushing is off (G37).

## Reusable idea
Pick the destination slot when the item is created, then route it to the station of the crane that serves that rack;
the Store block only executes a decision already made. The same "reserve, then route to the rack's station" pattern
works for any storage whose access points depend on the rack.

## When the co-pilot should use this
AS/RS, mini-load and unit-load high-bay warehouses, crane-count and throughput questions, and conveyor or AGV
interfaces to automated racks. For manual racks see `slotting-policies-in-drive-in-storage.md` and
`job-shop-phase-3.md`; for AGV dispatch rules see `../videos/mhl-agv-dispatch-choice-and-cargo-position.md`.
