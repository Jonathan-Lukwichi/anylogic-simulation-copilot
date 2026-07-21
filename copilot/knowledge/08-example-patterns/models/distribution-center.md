# Pattern card — Distribution Center
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates the end-to-end flow of a warehouse distribution center — truck unloading, pallet storage in racks, order assembly by forklifts, and outbound truck loading — to expose bottlenecks in dock counts, forklift allocation, and assembly throughput.

## Block chain

Inbound trucks arrive and compete for a limited number of unloading docks. Once a dock is seized, forklifts (pooled per dock) unload pallets and transfer them to main rack storage. Independently, customer orders are generated at a configurable rate; each order specifies a mix of pallet types and a total capacity requirement. An order scheduler checks whether enough pallets of the right types exist in storage and whether an assembly dock has space before releasing the order into assembly. Forklifts retrieve the required pallets from racks and stage them at the assigned assembly dock. When an order is fully assembled and meets the minimum load threshold (at least half a truck's capacity), an outbound truck is matched to that loading dock, forklifts load the pallets, and the truck departs. The Hold block at the order entry point gates new orders when the pending-orders queue is full, preventing runaway backlog build-up.

## Resources

| Resource | Parameter name | Notes |
|---|---|---|
| Loading docks | `numLoadingDock` | shared between inbound and outbound |
| Unloading docks | `numUnloadingDock` | separate dock bank |
| Total forklifts | `forkliftsNum` | shared pool |
| Forklifts per assembly order | `forkliftsPerOrderAssembling` | sub-allocation |
| Forklifts per unload dock | `forkliftsPerUnloadDock` | sub-allocation |
| Forklifts for pallet re-stowing | `forkliftsPerOrderReMoving` | handles overflow to standby storage |
| Rack storage | `dockStorages` (12 dock nodes) | typed pallet slots per rack zone |
| Truck capacity | `truckCapacity` | minimum half-fill rule for dispatch |
| Max pending orders | `ordersListMaxLength` | caps the order queue length |

## Key settings worth copying

- **Order arrival rate:** `orderRate` (Poisson-driven Source block, time unit = minutes)
- **Order size randomisation:** `uniform_discr(minOrderSize, maxOrderSize)` for total pallet capacity; each pallet-type quantity also drawn with `uniform_discr`, iterated until capacity is consumed — produces realistic mixed-SKU orders without a fixed bill-of-materials
- **Minimum truck fill rule:** outbound truck is only dispatched when assembled order volume >= 0.5 × `truckCapacity`; enforced in the loading-trigger logic, not in a block parameter
- **Restricted-area blocks:** `RestrictedAreaStart` / `RestrictedAreaEnd` pairs gate forklift movement into dock zones, preventing simultaneous collisions in narrow aisles
- **Standby storage overflow:** when a dock lacks space for a newly released order, pallets are temporarily staged in `standByStorage` and re-assigned when dock space opens — modelled via a Wait block with an event-driven free call
- **Model time unit:** Minute

## KPIs instrumented

- Queue lengths tracked via bar charts: `titleQueue` (orders waiting), `titleWaitAssembling`, `titleAssembling`, `titleWaitLoading`
- Dock utilisation (implicit through Seize/Release cycle statistics)
- Forklift utilisation across sub-pools
- Order throughput (assembled and loaded orders over time)
- Truck turnaround time at unloading and loading docks

## Reusable idea

**Hierarchical forklift sub-allocation:** rather than one monolithic resource pool, split a shared forklift fleet into named sub-quotas (`forkliftsPerOrderAssembling`, `forkliftsPerUnloadDock`, `forkliftsPerOrderReMoving`). Each subprocess seizes only its quota, so no single operation can starve the others — a transferable pattern for any facility where the same mobile resource class serves multiple competing process stages simultaneously.
