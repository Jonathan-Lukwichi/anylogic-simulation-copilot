# Pattern card — Warehouse conveyor (8.9.10 example: Conveyor System at Warehouse)
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models multi-zone warehouse conveyor networks handling inbound pallets, robotic/manual pick-and-place to rack feeders, and outbound order-picking with inline sortation — all timed in seconds.

## Block chain
1. **Inbound docks** — PalletSource blocks generate pallets of three item types (food, beverage, dish) arriving at receiving docks.
2. **Pallet conveyor network** — Convey blocks move loaded pallets from docks into the storage zone; DropOffStation blocks let robots or workers unload goods from the pallet onto infeeding conveyors.
3. **Rack infeeding** — Separate Convey segments carry individual items toward rack storage; a Storing block represents placing goods into rack slots; an Exit block releases the empty carrier back.
4. **Order-picking lines** — Cartons enter via ConveyorEnter / Enter blocks and queue (Queue blocks) at PickingStation blocks where operators insert ordered items into boxes.
5. **Routing decisions** — SelectOutput and SelectOutput5 blocks direct cartons to the next picking line if additional items are needed, or forward them to the packing line when the order is complete.
6. **Sortation & dispatch** — A downstream Convey segment feeds a simple sortation loop; a final Sink block absorbs completed, packed cartons; a MoveTo block repositions agents (workers/robots) between tasks; ConveyorExit blocks handle transitions between conveyor segments.

## Resources
- **Robots** — handle pallet-to-conveyor transfers on the inbound side; trajectory mapping (food → robotTrajectory) set in startup code.
- **Workers / operators** — staff PickingStation blocks on order-picking lines.
- **Conveyor speed:** 10 m/s (MPS); item spacing: 1 m; item size: 1 m — *(not confirmed in the 8.9.10 model)*.
- **Resource pools (corrected 2026-10-01 from the 8.9.10 `.alp`):** PML ResourcePools `pickupRobot`, `worker`, `asrs1..3` (one per AS/RS) and `packager1..3` (one per packing line), plus a Material Handling `TransporterFleet` `forklifts` (capacity 2). An earlier version of this card said there were none.

## Key settings worth copying
- **Time unit:** Second — fine-grained enough for conveyor travel-time accuracy.
- **Item-type enum:** `ItemType {food, beverage, dish}` — use a simple enum to branch routing logic cleanly.
- **Trajectory map at startup:** `trajectoriesToConv.put(food, robotTrajectory)` — maps item types to conveyor paths in a single hash-map lookup rather than hard-coded if/else chains.
- **SelectOutput for conditional re-circulation:** cartons loop back to a subsequent picking line only when more items remain, avoiding a dedicated recirculation conveyor model.
- **ConveyorEnter / ConveyorExit pairs** — explicit entry/exit blocks make it easy to splice queue buffers between conveyor segments without redesigning the network.

## KPIs instrumented
- Throughput of packed cartons reaching the Sink (implied by Sink count).
- Station utilisation at PickingStation blocks (operators).
- Queue length / wait time at inbound Queue blocks before ConveyorEnter.
- (Model focuses on flow demonstration; detailed KPI dashboards would be added on top of these natural measurement points.)

## Reusable idea
Use a startup-code hash-map to bind item-type enum values to named conveyor trajectories — this lets you add new product categories with zero changes to the routing logic, just one new map entry.

## Techniques in the 8.9.10 model (added 2026-10-01)
1. **Admission check before a dead-end lane.** Before a carton turns into a picking lane, compute the lane's free length (lane length minus, for each item on it, item length plus the conveyor's minimum gap — `getAgents()`, `length(METER)`, `getGap(METER)`); if it does not fit, send it round the recirculation loop (SelectOutput5 by conditions). A full lane then never blocks the main loop.
2. **Merge throttling with two watermarks.** A Position on conveyor at the merge acts as a stop: `block()` when this item type's occupancy of the infeed path reaches about 75 % of its length, `unblock()` when a stored item frees space and occupancy is back under 50 %. Occupancy is summed across a chain of conveyors by walking upstream through `getSource().getIncomingPaths()`. The gap between the two marks prevents stop-go chatter.
3. **Least-busy lane as routing input.** Convey's *Include conveyors* is filled per item with the packing line that holds the fewest open cartons (count over `getAgents()`).
4. **Warm-start racks.** StorageSystem *Initial stock* with *New agent* = a factory function that also does the stock bookkeeping, because *On agent storage* does not run for initial items (gotcha G94).
5. **Wait for rack space.** SelectOutput on `rack.hasSpace()`; if false, a Delay *until stopDelay()*; each pick calls `stopDelayForAll()` on it when space exists.
6. **Back-orders.** An order whose items are not all in stock is kept aside; each newly stored item first looks for a waiting order of its type and reserves itself to it; the carton is created only when nothing is missing. Picking uses Pickup *While condition is true* with `agent.order == container.order` (a condition on both the container and the candidate — Help 8.9.10 *Pickup*).
7. **Replenishment trigger.** After each order, a check restarts a pallet source's event when available units fall to a minimum and the rack has room for at least half a pallet.

**When the co-pilot should use this:** conveyor-fed warehouses where lanes, merges or racks can fill up — the reference for admission control, merge throttling and warm-started storage.
