# Pattern card — Oil Terminal
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid)
- **Problem it solves:** Optimising throughput and resource utilisation at a multi-modal bulk-liquid terminal where sea tankers and railway trains must share limited berth, tugboat, and storage infrastructure.

## Block chain
Tankers arrive according to a triangular inter-arrival distribution (min = mode/3, mode = `tankerInterarrivalTime`, max = mode×2). On arrival a tanker agent is routed via **Source → MoveTo (anchorage) → Seize (berth + tugboats) → MoveTo (berth) → Delay (fluid loading) → Release → MoveTo (departure) → Sink**. While berthed, the tanker transitions through a three-state statechart: *TANKER_AT_THE_BERTH_IDLE* (waiting for pipeline connection), *TANKER_AT_THE_BERTH_LOADING* (fluid transfer in progress), and *TANKER_AT_THE_BERTH_LOADED* (ready to depart). Each tanker carries four internal tank compartments; the product type for each compartment is chosen at random from the four grades (Petrol, Diesel, Fuel Oil, Crude Oil). Loading is handled by **FluidDropoff** blocks drawing from the matching **ProductStorage** (tank farm) object for that grade.

Railway trains replenish the tank farm on a separate Rail Library sub-process: trains enter a **RestrictedAreaStart**, move to an unloading position via **TrainMoveTo**, discharge into a **ProductStorage** via another **FluidDropoff**, then exit via **RestrictedAreaEnd** and depart with **TrainDispose**. The two transport modes (sea and rail) share the same fluid storage layer but otherwise run on independent process chains, so a congested berth does not directly block rail unloading.

## Resources
- **Berth:** capacity 1 (single-berth terminal, modelled as a ResourcePool)
- **Tugboats:** ResourcePool seized and released with the tanker; tugboat agents physically move with the tanker through the GIS/2-D layout
- **ProductStorage tanks:** four grade-specific tank farms, each with four tanks; utilisation tracked continuously via `storagePetrol.utilization()` etc.
- **Railcars:** fixed-capacity train consists; number of trains calculated dynamically from demand versus railcar capacity

## Key settings worth copying
- Inter-arrival time: `triangular( tankerInterarrivalTime/3, tankerInterarrivalTime, tankerInterarrivalTime*2 )` — asymmetric triangular captures maritime scheduling variability without requiring historical data
- Rail supply rate: `exponential( 0.025 )` — Poisson-like train arrivals for the replenishment stream
- Time unit: **Minute** — appropriate granularity for fluid-flow rate calculations
- All capacities, flow rates, and inventory thresholds are exposed as top-level parameters so the model can be re-run in experiments without code changes
- Tugboat agents use a `moveTo` callback to stay co-located with the tanker agent throughout the seize/release cycle

## KPIs instrumented
- **tankersLoaded** — cumulative count of tankers fully loaded
- **tankerIdleTimePercent** — ratio of berth-idle time to total berth-occupied time (`zidz(tankerTimeIdle, tankerTimeIdle + tankerTimeLoading)`)
- **tankerTimeIdle / tankerTimeLoading** — absolute time accumulators fed from statechart state statistics
- **Storage utilisation per grade** — average of the four tanks in each ProductStorage (`utilizationTotal()` averaged across compartments)
- **Average utilisation of Storages** — single dashboard gauge combining all four grades

## Reusable idea
Couple a discrete-event agent process (tanker/train arrivals, berth seizure) with a continuous Fluid Library layer (product storage, pipeline flow) using **FluidDropoff** as the bridge: the DES side controls *when* flow starts and stops, while the Fluid side handles *how much* accumulates. This hybrid handshake lets you model inventory depletion and replenishment accurately without discretising fluid quantities into individual batches.
