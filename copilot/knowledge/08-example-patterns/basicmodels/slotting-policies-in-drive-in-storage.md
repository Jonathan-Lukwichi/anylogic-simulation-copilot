# Pattern card — Slotting Policies in Drive-in Storage
- **Source:** AnyLogic example model "Slotting Policies in Drive-in Storage" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Decide where each incoming pallet goes in deep-lane (drive-in) racks — the rack's own filling order, a random lane, or a lane chosen per item — and retrieve only what a forklift can actually reach.

## Block chain
- **Put-away, three variants side by side:** `Source` (arrivals = calls of `inject()`, several SKUs per call, created at
  the unloading node, kept in population `SKUs`) → `Store` (forklift fleet, loading 30 s) → `Exit`.
  - green: slotting *According to storage* (default) — the drive-in rack's own order;
  - blue: *Random available* (`SP_RANDOM_AVAILABLE`);
  - red: *Specific slot* (`SP_SPECIFIC_SLOT`), slot `redStorage.getSlot(0, agent.bay, 0)`. The red Source's *On exit*
    gives each SKU a lane that still has room: `agent.bay = redStorage.getRandomFreeCell().getBay()`.
- **Retrieval:** chosen SKUs are pushed with `enter.take(sku)` → `Retrieve` (same fleet, unloading 30 s, drop at
  `loadArea`) → `Sink`. A click on a stored SKU retrieves it; a button retrieves the last *n* agents of
  `storage.getAgents()`.
- UI guards: the STORE button is enabled only while `storage.nFreeCells() >= n`; RETRIEVE only while no Store block has
  work waiting (`nWaitingForResource()` summed) and the Retrieve queue is empty.

## Resources
`TransporterFleet`: 5 forklifts, free-space navigation, 5 home locations. The forklift type calls
`setCargoPosition(1.3, 0, 0, METER)` on startup so the pallet sits on the forks.

## Key settings worth copying
- **Slotting policies (Help 8.9.10, *Store*, *Storage*):**
  - *According to storage* — next cell by rack type. Drive-in: the deepest position of every bottom lane first, then
    the level above, and only then the next depth. Selective: bay by bay, bottom shelf up, deepest cell first.
  - *Random available* — the deepest free cell of a randomly picked rack and slot.
  - *Specific slot* — you pass a `StorageSlot` from `storage.getSlot(rack, bay, shelf)`; the block takes the deepest
    free cell in it.
- **Drive-in quirk:** with *Specific slot* the shelf argument is ignored; the item goes to the next free shelf of that
  bay. To force a cell, reserve it (`storage.setReservation(agent, rack, bay, shelf)` or `cell.setReservation(agent)`) and
  place it with `store(...)` (Help).
- **Reachability test:** `sku.storage.getCell(sku).isAvailableToRetrieve()`. Keep a `Storage` reference on the item (here a
  `storage` parameter) so any code can find its cell.
- **Lanes shared out among vehicles:** Retrieve → *Customize transporter choice*, condition
  `bay % fleet.size() == unit.getIndex()`, so each forklift owns a set of lanes and two trucks never meet at one lane
  mouth. Built-in alternative: Storage → *Restrict aisle access* (limit transporters per aisle; for drive-in racks the
  trucks inside the lanes count too; transporters only, not resources).
- **Priorities:** put-away Stores have priority −5, so retrieval requests (default 0) are served first; one Store uses
  *Task preemption policy* = `TPP_SEIZE_ANY_RESOURCE`.

## KPIs instrumented
Visual only. For a policy study add: lanes in use, free cells that are unreachable (honeycombing), blocked-retrieval
requests, forklift utilization, and put-away / retrieval cycle times per policy.

## Pitfalls
- **Blocked cells.** Only the cell next to the aisle can be emptied; asking for a deeper one raises an error, unless a
  blocker in front is already being fetched, in which case the request waits (Help, *Storage*). The model checks
  reachability before a click-retrieval instead of failing.
- **One agent per bay side at a time.** Each bay's operating side has an internal queue, and retrieval outranks storing
  (Help). Mixed put-away and picking in the same lanes therefore serialises.
- **Leftover hidden settings.** The red Store still holds `storage = greenStorage` from another policy; under *Specific
  slot* only the slot counts. Clear such values — they mislead the next reader.
- **Help name error:** the Help lists *Specific slot* as `Store.SP_EXPLICIT`; 8.9.10 defines `Store.SP_SPECIFIC_SLOT`
  (checked with `javap`).
- The lane is chosen when the SKU is created; if other flows fill it before the SKU reaches the Store, the outcome is
  *(unverified)* — reserve the cell at creation when it matters.

## Reusable idea
Treat slotting as a policy lever: keep the put-away and picking flowcharts fixed, switch the Store's slotting policy or
slot expression, and compare reach, re-handling and travel. For deep lanes, assign the lane at creation, test
reachability before calling an item, and split lanes among vehicles to avoid congestion at lane mouths.

## When the co-pilot should use this
Drive-in or other deep-lane pallet storage, cold stores, bulk warehouses, "where should this pallet go" questions, and
errors from a Retrieve on a blocked cell. Related: `job-shop-phase-3.md` (Store/Retrieve with forklifts),
`mobile-rack-system.md` (reservations, specific slot in a storage system), `multiload-transportation-at-storage.md`,
`stacker-crane-store.md`.
