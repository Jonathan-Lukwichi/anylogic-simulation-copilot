# Pattern card — Storage with Initial Stock
- **Source:** AnyLogic example model "Storage with Initial Stock" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling + Process Modeling)
- **Problem it solves:** Start a rack warehouse partly full instead of empty, and stop inbound goods from entering when the rack has no free cell.

## Block chain
`Source` (interarrival `uniform(1, 2)` min, created at the unloading node, pull protocol) → `Hold` (*Conditional*,
blocking condition `!storage.hasSpace()`) → `Store` (*Agents move*: **by resources**, pool `forkLiftTrucks`, into the
`StorageSystem`) → `Delay` (dwell `uniform(30, 40)` min) → `Retrieve` (same pool, to the pickup node) → `Delay` (pickup,
1 min) → `Sink`.
The `StorageSystem` block wraps one selective rack storage (2 racks × 30 bays, one cell deep) and creates the initial
stock at start-up.

## Resources
`ResourcePool forkLiftTrucks`: 5 units, moving at 1.8 km/h, one home node. Store and Retrieve use them as PML resources
(`RESOURCE_PML`) rather than a `TransporterFleet`; Retrieve *Return home* = *if no other tasks*
(`WRAP_UP_IF_NO_TASKS`). Vertical moves are made quick (elevation / lowering speed 10 m/s).

## Key settings worth copying
- **Initial stock (StorageSystem, Help 8.9.10; available since 8.9.5):**
  - *Storage system* = is initially empty / **contains a given number of items** / is fully filled
    (`initialFillingPolicy` = `INITIAL_EMPTY` / `INITIAL_PARTIAL` / `INITIAL_FULL`);
  - *Used capacity is defined* by percentage (`capacityPercent`, default 50) or by exact number (`capacityNumber`,
    default 10) — here the parameter `initialStockSize` = 35;
  - *Slotting policy* for the initial items: according to storage (default) or random;
  - *New agent* (item type, optional new dimensions) and *Add agents to* a custom population.
- **Backpressure gate:** a conditional Hold in front of the Store blocks arrivals while the rack is full (*Blocking
  condition* true = blocked). A Hold stores nothing itself, so the goods wait in the upstream block — here the Source,
  which is on pull protocol.
- Expose the stock level as a parameter so it can be swept (empty vs typical vs near-full start).

## KPIs instrumented
Visual only. Useful additions: occupied cells over time (`storageSystem` / `storage.nFreeCells()`), time products wait
at the Hold, forklift utilization, storage dwell time.

## Pitfalls
- **Initial items are outside every flowchart.** They never pass the Source, so counters, lists or attributes set there
  are missing, and *On agent storage* does not fire for them (Help). Nothing in this demo ever retrieves them: they
  occupy 35 cells for the whole run. To consume them, collect `storageSystem.getAgents()` at start and push them into the
  retrieval flow with `Enter.take(...)` (as in `multiload-transportation-at-storage.md`).
- **A conditional Hold is not re-checked by itself.** The condition is evaluated when an agent arrives; after space frees
  up, call `hold.recalculateConditions()` (Help, *Hold*) — e.g. from the storage's *On agent retrieval* — or a held
  product can wait for ever. The shipped model has no such call; whether it ever blocks depends on sizing *(not tested)*.
- A partial fill with random slotting scatters items over the rack; with "according to storage" they sit together at
  the start of the fill order. The choice changes early travel distances.

## Reusable idea
Start a storage model in a realistic occupancy state (StorageSystem initial filling) rather than empty, and put an
explicit capacity gate before put-away. This shortens the warm-up, makes early travel distances realistic, and turns
"what if we start the week 80 % full?" into a parameter.

## When the co-pilot should use this
Warehouse, buffer-store and cold-store models where the starting inventory matters, warm-up discussions for storage
models, and "store is full" handling. Related: `multiload-transportation-at-storage.md` (initial stock fed to picking),
`mobile-rack-system.md` (initial stock placed by code), `slotting-policies-in-drive-in-storage.md`.
