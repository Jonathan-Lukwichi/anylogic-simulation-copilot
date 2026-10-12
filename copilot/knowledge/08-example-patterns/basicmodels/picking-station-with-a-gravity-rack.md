# Pattern card — Picking Station with a Gravity Rack
- **Source:** AnyLogic example model "Picking Station with a Gravity Rack" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling + Process Modeling)
- **Problem it solves:** A pick-from-carton station fed by a flow rack: forklifts/AGVs load cartons by SKU lane, a picker takes items out of the cartons in place for each order, emptied cartons go onto a return shelf and are hauled away.

## Block chain
- **Replenishment:** `Source` *boxSource* (manual; a button injects 30) → `SelectOutput` "lane has space?" (`storage.nFreeCells(0, type, shelf)`) → `Store` by AGV into a **specific slot** `storage.getSlot(0, agent.type, getAvailableShelf(agent.type))` (bay = SKU type) → `Exit`; overflow → `Sink`.
- **Orders:** `Source` (every 20 s) → `Convey` to the station → `SelectOutput` "enough stock?" (`sumWhere(storage.getAgents(), capacity, same type)`), else back-order `Sink` → `Delay` *waitForPicking* (manual; *On enter* creates one `Item` agent per order line with `createAndStart(this)` and pushes it into `Enter` at the carton's position) → `Seize` picker (**send + attach** the picker to (x, y, z) beside the carton) → `MoveTo` station → `Release` → `Queue` (wakes the waiting order) → `Pickup` (*all*; *On pickup* updates the order) → `SelectOutput` "order complete?" → `Convey` away, or back to wait for more lines.
- **Empty carton:** when a carton's count hits 0 → `Enter` → `Seize` picker (**priority 5**) → `Retrieve` (no resource) → `Store` on the upper return shelf `storage1.getSlot(0, type, 0)` → `Release` (*wrap-up only if no other tasks*) → `Retrieve` by an AGV **from the aisle**, AGV chosen by `(int)(agent.type / 3) == unit.getIndex()` → `Sink`.

## Resources
`picker` ResourcePool (0.5 m/s, home at the picking station); `AGV` fleet (free-space); two Rack Storages: main flow rack (2 shelves, 0.5 m, *speed inside slot* 0.5 m/s) and the return shelf.

## Key settings worth copying
- Flow racks (Help 8.9.10 rack types: Selective, Drive-in, **FIFO flow**, **LIFO flow**; both flow types model carton/pallet flow and gravity racks). This model's racks are stored as gravity + LIFO; items slide to the deepest free cell at *Speed inside slot*.
- Dedicated lanes: slot chosen by SKU (`getSlot(rack, bay = type, shelf)`), free space tested with `nFreeCells(rack, bay, shelf)`.
- **Split picks across cartons with pre-emption:** the pick `Seize` has *task pre-emption policy* **wait for original resource**; in *On prepare unit* it takes what the current carton holds; if the carton empties it is sent to the priority-5 replacement flow, which pre-empts the picker; *On task resumed* then continues the same line from the next carton of that SKU.
- *Take agent from*: **cell** (slot movement modelled, respects rack type and in-slot speed) vs **aisle** (item jumps to the aisle point; faster, no slot movement) — used for the empty-carton pickup.
- Dedicated vehicles per SKU group via Retrieve *resource choice condition* on `unit.getIndex()`.

## KPIs instrumented
Visual (2D/3D); back-ordered orders leave through a separate sink (countable).

## Pitfalls
- A FIFO or LIFO flow rack gives up its items on one side only — the unloading face for FIFO, the loading face for LIFO — so aisles and pickers must sit on that side (Help, *Retrieve*).
- Pre-empting the picker without *wait for original resource* would lose the partly done pick; the resume callback is what keeps the order line intact.
- Order-line items are created as agents on the fly; remove them (Pickup into the order, then dispose with it) or populations grow without bound.

## Reusable idea
Model piece-picking from cartons as the picker visiting the carton (send/attach resource to XYZ) rather than retrieving cartons; use a higher-priority, pre-empting replacement task for emptied cartons and resume the interrupted pick — a compact, realistic station logic.

## When the co-pilot should use this
Carton/pallet flow racks, pick-to-order stations, kitting with empty-tote returns, and questions about splitting one pick over several containers or resuming a pre-empted resource task. For push-back racks and drive-in slotting see the `push-back-rack` and `slotting-policies-in-drive-in-storage` cards (batches m-basic-3/4).
