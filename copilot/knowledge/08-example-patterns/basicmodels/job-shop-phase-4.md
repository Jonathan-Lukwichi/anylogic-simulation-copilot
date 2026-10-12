# Pattern card — Job Shop - Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a warehouse job-shop where pallets arrive, are stored in rack storage, retrieved by forklift trucks for processing, then dispatched by outbound trucks — capturing material-handling logistics with autonomous vehicle agents.

> **Verified corrections (2026-10-01).** Checked against the shipped 8.9.10 example `.alp` and the tutorial text (AnyLogic Help tutorials, *AnyLogic in 3 Days*). Where they differ from the text below, these win.
> - The trucks are **inbound delivery** trucks, one per hour from t = 0 at 40 km/h: Source → MoveTo dock → Delay `unloading` (*until stopDelay()*, *On enter* `sourcePallets.inject(60)`) → MoveTo exit → Sink — not outbound loading on a schedule.
> - The pallet Source switches to *Calls of inject()*; Store's *On exit* calls `unloading.stopDelayForAll()` when `self.nWaitingForResource() == 0` (pp. 176–179). Beware `stopDelay(null)`, which releases every truck (gotcha G87).
> - "Delay (unloading/processing, triangular 15–30)" is the rack dwell again; `capacityBasedOnAttractors` is an unused option.

## Block chain
Two parallel flows share the same physical space and resource pool:

**Inbound pallet flow:**
Source (pallets arrive every 5 min) → Store (rack storage) → Delay (unloading/processing, triangular 15–30 min) → Sink

**Outbound truck flow:**
Source (trucks arrive on schedule) → MoveTo (dock area) → Delay (loading) → MoveTo (exit) → Sink

A **Retrieve** block pulls pallets out of the Store on demand, and **MoveTo** blocks navigate both forklift trucks and trucks along a 2-D/3-D warehouse layout using defined path nodes and area nodes.

## Resources
- **ResourcePool — ForkliftTruck agents:** capacity = 5 forklift trucks, each modelled as a custom agent type with 3-D geometry (`3d/forklift.dae`). They are dispatched by Retrieve blocks to fetch pallets from rack locations.
- **StorageDescriptor:** defines rack capacity and slot geometry for the Store block.
- **AreaNodeDescriptors:** two zones (storage area, dock area) used by MoveTo for destination routing.

## Key settings worth copying
- **Interarrival time:** fixed 5-minute interval (deterministic arrivals — easy to swap for `exponential(5)`)
- **Processing delay:** `triangular(15, 20, 30)` minutes — min/mode/max captures realistic variability without heavy data requirements
- **ResourcePool capacity:** 5 forklifts; `capacityBasedOnAttractors` flag available for attractor-driven sizing
- **Model time unit:** Minutes
- **3-D assets:** linked via relative paths (`3d/forklift.dae`, `3d/pallet.dae`, `3d/truck.dae`, `3d/box_1_closed.dae`) — drop-in replaceable

## KPIs instrumented
- Throughput of pallets processed and dispatched (Sink statistics)
- Forklift utilisation (ResourcePool built-in utilisation tracker)
- Store occupancy / queue length at the rack
- Cycle time per pallet (time-in-system from Source to Sink)

## Reusable idea
**Pair a Store+Retrieve block set with a ResourcePool of vehicle agents to model any pick-and-deliver operation.** The Store holds items spatially; the Retrieve triggers a forklift (or AGV, or picker) from the pool to travel to a rack slot and bring the item to a workstation — cleanly separating storage logic from transport logic and making fleet-size sensitivity analysis a single parameter change.
