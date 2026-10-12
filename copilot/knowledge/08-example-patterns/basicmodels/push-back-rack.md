# Pattern card — Push-back Rack
- **Source:** AnyLogic example model "Push-back Rack" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Model a push-back (LIFO flow) pallet rack, where each lane is loaded and emptied from the aisle side only, and move a chosen item to another lane while respecting that only the front item is reachable.

## Block chain
- **Filling:** `Source` (20 per minute, 100 in total, 0.8 m cubes, at `node`) → `Store` (forklift fleet, slotting *random available*) → `Exit`. The items stay in the rack after the Exit.
- **Re-slotting on click:** the item's `moveToSpecifiedSlot()` runs when the user clicks it: if it is stored (`storage.getCell(this) != null`), the chosen lane has room (`storage.nFreeCells(0, section, shelf) > 0`) and it sits in the aisle-side cell (`getCell(this).getDeepPosition() == 0`), it records the target and is pushed into `Enter` → `Retrieve` (the forklift takes it to `DEST_XYZ` = (item x − 30, item y, 0) and stays there afterwards) → `Store` (*specific slot*, `storage.getSlot(0, targetSection, targetShelf)`) → `Exit`. Otherwise an on-screen error is shown.

## Resources
`TransporterFleet` of forklifts, **free-space** navigation (no path network), cargo placed with `setCargoPosition(1, 0, 0.1, METER)` in the forklift type's On startup.

## Key settings worth copying
- **Storage markup:** rack type *LIFO flow* (the file stores push-back, LIFO, a 5° lane angle), one rack, 8 bays, 5 cells per slot. Help 8.9.10 (*Storage*) lists four types: *Selective* and *Drive-in* (LIFO by construction), *FIFO flow* (load one face, pick the other) and *LIFO flow* (one face; a new item pushes the others back). Shared access rules — only the aisle-side cell can be emptied, one agent per bay face at a time, retrieval before storage — are in `basicmodels/slotting-policies-in-drive-in-storage.md`.
- **Reachability checks:** `cell.isAvailableToRetrieve()` (accessible and occupied — cleaner than the demo's `getDeepPosition() == 0`, which is the cell's index in its slot) and, since 8.9.5, `storage.getRandomAccessibleAgent()` (a random item that can be retrieved now, or null).
- **Digging on purpose (8.9.5):** `Retrieve` → *Allow retrieving from deep position* (`set_retrieveFromDeepPosition(...)` at run time). The blocked item is taken anyway and the *Retrieving time* is assumed to include pulling the front items out and putting them back; in FIFO/LIFO flow racks the remaining items then slide into the freed cell; in drive-in racks the vehicle stops before the first occupied cell (Help, *Retrieve*). Without the option, a blocked retrieval is an error.
- **Index conventions:** `getSlot(rack, bay, shelf)` and `nFreeCells(rack, bay, shelf)` are 0-based (the demo's on-screen numbers are shifted by 1).

## KPIs instrumented
None. Useful: moves per retrieved item (re-handling), forklift utilization, share of retrieval requests that found their item blocked.

## Pitfalls
- In FIFO/LIFO flow storages do **not** use `cell.setReservation(agent)` or `storage.getRandomFreeCell()` — the Help rules them out for flow types (the drive-in card's `cell.setReservation` advice does not carry over). Choose at slot level (`getSlot`, *specific slot*) instead (G? in `.ingest/proposals/m-basic-3.md`).
- *Allow retrieving from deep position* hides re-handling inside one retrieving time; set that time to cover the digging, or model the moves explicitly when forklift load matters.
- A LIFO lane buries old stock: date- or batch-sensitive goods need a FIFO-flow rack or a rotation policy.
- The re-slot check happens at the click; if another forklift fills the target lane first, the `Store` finds no room. Re-check `nFreeCells` just before storing in a busy model *(inferred)*.

## Reusable idea
Let the rack type carry the access rule, test reachability before calling an item, and express re-slotting as `Retrieve` → `Store` with a specific slot. Decide consciously between "blocked means error" (default) and "blocked means dig" (deep-position option).

## When the co-pilot should use this
Push-back and pallet- or carton-flow racks, beverage and cold stores, and any "move this pallet to another lane" or "why does Retrieve fail on this pallet" question. Related: `basicmodels/picking-station-with-a-gravity-rack.md` (FIFO/LIFO flow picking; *Take agent from* cell vs aisle), `basicmodels/mobile-rack-system.md` (reservations in selective racks).
