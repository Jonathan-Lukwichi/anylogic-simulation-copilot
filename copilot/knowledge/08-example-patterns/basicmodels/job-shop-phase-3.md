# Pattern card — Job Shop - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a warehouse/manufacturing job shop where pallets arrive, are stored in a rack, processed at a workstation, then retrieved and dispatched — with forklift trucks handling all material movement.

## Block chain
Pallets enter through a Source with a fixed interarrival time (5 minutes). They are carried by a forklift to a Store block (rack storage). When a job is ready, a Retrieve block pulls the pallet from storage and routes it to a Delay block representing processing time drawn from triangular(15, 20, 30) minutes. After processing a second Retrieve/Delay stage handles outbound movement, and pallets exit through a Sink. Two parallel store-retrieve-delay chains handle inbound and outbound material flows independently.

## Resources
- **ResourcePool: forklifts** — pool of ForkliftTruck agents that seize/release around every Store and Retrieve block, returning to a forkliftParking attractor when idle.
- **StorageDescriptor** — defines rack layout and storage capacity (capacity parameter on the Store blocks, set to 100 slots each).
- **AreaNodeDescriptors** — define spatial zones (receiving dock, processing area, dispatch area) used by forklifts for path routing.

## Key settings worth copying
- Interarrival time: constant 5 minutes (model time unit = Minute); can be overridden via `INTERARRIVAL_TIME` parameter.
- Processing delay: `triangular(15, 20, 30)` minutes — captures variability without requiring historical data.
- Forklift release policy: `afterReleaseGoHome = true`; transporters return to `forkliftParking` node after each task.
- Storage capacity: 100 units per Store block (rack slots).
- Resource pool size exposed as parameter `RESOURCE_PML` so it can be swept in experiments.
- Pallet agent carries `LOCATION_NODE` parameter so it can be directed to the correct storage zone.

## KPIs instrumented
- Throughput: count of pallets reaching the Sink.
- Queue length / waiting: implicit through Store block statistics (items in storage over time).
- Forklift utilisation: tracked via ResourcePool utilisation statistic.
- Delay (processing) time: recorded per-pallet by the Delay block.

## Reusable idea
The key transferable trick is pairing every **Store** block with an explicit **Retrieve** block and a dedicated **ResourcePool** of mobile transporters — rather than treating storage as a passive queue. This makes forklift contention visible and schedulable: you can size the pool, set a home-base parking node, and sweep capacity as a parameter to find the minimum fleet that keeps throughput targets without over-stocking the racks.
