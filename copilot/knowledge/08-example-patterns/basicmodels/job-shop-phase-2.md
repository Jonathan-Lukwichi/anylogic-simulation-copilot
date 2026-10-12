# Pattern card — Job Shop - Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a warehouse/manufacturing job shop where pallets move between storage racks and processing stations using forklift trucks as material-handling resources.

> **Verified corrections (2026-10-01).** Checked against the shipped 8.9.10 example `.alp` and the tutorial text (AnyLogic Help tutorials, *AnyLogic in 3 Days*). Where they differ from the text below, these win.
> - There is no second Retrieve and no `StorageDescriptor.cellCapacity` knob. The storage is Storage markup: back-to-back, 2 shelves, bays calculated from dimensions, network made with *Create storage network* (pp. 139–142).

## Block chain
Jobs (pallets) arrive at a Source with a fixed interarrival time of 5 minutes. They are placed into a rack-based Store block. A Retrieve block pulls them out when a forklift becomes available, and a Delay block represents the processing or transport time. A second Retrieve handles the return leg. Processed items exit through a Sink.

## Resources
- **Forklifts:** a ResourcePool named `forklifts` whose agents are of type `ForkliftTruck` (3-D model: forklift.dae). The pool home location is a dedicated `forkliftParking` area node. Forklifts are seized implicitly by the Store/Retrieve blocks for material movement.

## Key settings worth copying
- **Interarrival time:** 5 minutes (constant) — swap for `exponential(5)` to introduce variability.
- **Processing/transport delay:** `triangular(15, 20, 30)` minutes — captures best-case / most-likely / worst-case uncertainty.
- **Time unit:** Minutes throughout.
- **Storage:** `Store` block paired with a `StorageDescriptor` that defines rack cell capacity — set `cellCapacity` to control how many pallets share a rack slot.
- **Forklift home:** assigning a parking `AreaNodeDescriptor` ensures trucks return to a defined spot between tasks, preventing drift in 2-D/3-D animation.

## KPIs instrumented
- Throughput (items reaching Sink per shift)
- Forklift utilisation (ResourcePool busy fraction)
- Storage dwell time (time between Store and Retrieve)
- Queue length at Retrieve blocks (backlog of pending retrieval requests)

## Reusable idea
Pair every **Store** with a matching **Retrieve** and a dedicated **ResourcePool** of mobile agents (forklifts, AGVs, workers) that travel to the rack. This Store→Retrieve sandwich cleanly models any scenario where a physical carrier must pick an item from a fixed location — the carrier pool becomes the bottleneck to tune, not the rack capacity itself.
