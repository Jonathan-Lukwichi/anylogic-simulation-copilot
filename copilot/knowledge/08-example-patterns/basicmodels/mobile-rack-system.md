# Pattern card — Mobile Rack System
- **Source:** AnyLogic example model "Mobile Rack System" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library) with rack agents
- **Problem it solves:** Model mobile (compactus) pallet racking — racks that slide sideways so only one working aisle is open at a time — served by forklifts that must wait for the aisle to open before storing or retrieving.

## Block chain
- **Racks are agents.** Population `dynamicRacks` of type `DynamicRack`; each rack agent draws its own Rack Storage markup, a short network and a Level Gate paired (`connectedLG` parameter) with a gate in Main's network at its aisle mouth. Parameters give its two parking positions (`leftPosition`, `rightPosition`) and `entryNode`.
- **Rack movement flow (on Main):** `Enter` → `MoveTo` (speed 0.5 m/s, destination = the rack's opposite parking position) → `Exit`. The *rack agents themselves* are the entities; `moveRacks(rack)` pushes into `enter` every rack lying between the requested rack and the currently open aisle (`openedRack`).
- **Storing:** `Source` (manual, boxes) → `MoveByTransporter` to the rack entry (keeps the forklift: `releaseTransporter = false`; *On enter* reserves a cell) → `SelectOutput` "aisle unavailable?" → `Delay` (manual) that calls `moveRacks(...)` → `Store` (`useAlreadySeized = true`, `SP_SPECIFIC_SLOT`) → `Exit`.
- **Retrieving:** an `Order` agent is created per request and pushed into `Enter` → `SeizeTransporter` (priority 2, `PP_SEIZE_ANY_RESOURCE`) → same aisle check / manual `Delay` → `ReleaseTransporter` (stays where it is) → `Combine` with the box → `SeizeTransporter` to an `(x, y)` in the aisle (priority 3) → `Retrieve` → `MoveByTransporter` legs → `Sink`.
- When the last rack leaves `moveRack` (the Exit's action), the waiting forklift is released from the manual Delay with `stopDelayForAll()`.

## Resources
`TransporterFleet forklifts` (free-space navigation, minimum distance to obstacles 0.1 m); custom transporter type carries a `rack` parameter set in *On seize transporter*.

## Key settings worth copying
- Build one StorageSystem from storages living inside other agents: at start-up `storageSystem.addStorage(rack.storage)` for each rack (the StorageSystem block's own list is left empty).
- Initial stock without the flowchart: create the item agent, `createAndStart(this)`, then `cell.store(item)` on a `storage.getRandomFreeCell()`.
- Reserve before travelling: pick a rack with `storage.hasSpace()`, take a free cell and `cell.setReservation(agent)`; later store into exactly that slot with `storageSystem.getSlot(storage, rack, bay, shelf)` under `SP_SPECIFIC_SLOT`.
- Drive the forklift to the cell's aisle point with SeizeTransporter `DEST_XYZ` = `storage.getPositionInAisle(rack, bay, …)`; after it arrives move the load into the rack's space with `agent.setSpace(rack)` so it travels with the rack.
- Store *release moving policy* `MP_GO_TO` the rack's entry node, so the forklift backs out of the aisle before the racks can move again.

## KPIs instrumented
Visual only (storing / retrieving / rack-movement areas, 2D/3D views).

## Pitfalls
- The aisle is a shared, single resource modelled by a variable (`openedRack`); two forklifts wanting different aisles will make racks shuttle back and forth. In a real study add an aisle-request queue or batch requests by rack.
- Moving the rack agent moves everything drawn inside it, including stored items — but only if the items were put into the rack's space (`setSpace`); items left in Main's space stay behind.
- A forklift parked inside an aisle blocks the next rack move; the release policy must take it out of the aisle.

## Reusable idea
Anything that physically moves together with its contents (mobile racks, shuttles carrying a storage, a truck body with shelves) can be an agent that owns a storage markup and is itself moved through a small `Enter → MoveTo → Exit` flowchart, with paired level gates connecting its space to the main network.

## When the co-pilot should use this
Compact/mobile shelving, moving-aisle archives or cold stores, or any layout where access to storage depends on another mechanism moving first. See `level-gate.md` for pairing gates between spaces.
