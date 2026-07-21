# Pattern card — Warehouse conveyor
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
- **Conveyor speed:** 10 m/s (MPS); item spacing: 1 m; item size: 1 m — all set on the shared conveyor network parameters.
- No explicit ResourcePool blocks; robot and worker availability is implicit in the station blocks.

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
