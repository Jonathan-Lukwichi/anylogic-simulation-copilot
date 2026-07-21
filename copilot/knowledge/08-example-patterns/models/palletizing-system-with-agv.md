# Pattern card — Palletizing system with AGV
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Sizing a shared AGV fleet and picking-robot count for a multi-cell palletizing line where boxes arrive at variable rates and must be batched onto pallets before transport.

## Block chain
Boxes arrive at each of several independent palletizing cells via a Source at a configurable rate (boxes per minute). Inside each cell a picking robot places incoming boxes onto a pallet; once the pallet holds a full batch it exits via a Convey segment. The completed pallet then enters a MoveByTransporter block, which claims one of the shared AGVs from a central resource pool. The AGV carries the loaded pallet to the dispatch area, releases back to the pool, and the pallet passes through a final Convey belt before reaching a Sink. Empty pallets and interlayer sheets are pre-stocked in separate queues at startup and are fetched by cells on demand, creating a secondary material-handling loop alongside the main product flow.

## Resources
- **AGV fleet:** single shared ResourcePool (`agvs`), capacity set by slider `AGVnumber` (default 3, range 1–5); AGVs travel at 10 m/s.
- **Picking robots:** one robot per palletizing cell (3 cells by default); each robot is modelled as a dedicated resource inside the PalletizingCell sub-model.
- **Pallet & sheet buffers:** 10 pre-loaded bottom-sheet pallets and 10 interlayer-sheet pallets initialised at model start; cells draw from these queues as needed.

## Key settings worth copying
- **Arrival rates:** per-cell sliders `initialBoxRate1/2/3` (default 3 boxes/min each, range 0–5); rates are hot-swappable at runtime via `source.set_rate(value, PER_MINUTE)`.
- **Batch size:** `palletBatchSize` slider (default 5 boxes per pallet, range 0–100); passed directly to the Batch block inside each cell.
- **Number of cells:** `numberOfCells` slider (default 3, up to 100); cells are instantiated as an agent population.
- **Time unit:** Seconds throughout; production-rate KPI is tallied hourly.
- **AGV speed:** 10 m/s (hardcoded in the transporter network); network cell size 1 m × 1 m, grid 500 × 500 cells.

## KPIs instrumented
- **Throughput:** `productionRate` dataset — pallets completed per hour, sampled every hour via a cyclic event that resets `hourOutput` counter; plotted as a time-series chart.
- **AGV utilisation:** `agvs.resourcePool.utilization()` — displayed as a gauge.
- **Picking-robot utilisation:** `robot.getUtilization()` per cell — three separate gauges showing per-robot load.
- **Cell throughput:** `throughput` statistic inside each PalletizingCell sub-model.

## Reusable idea
Use a single shared AGV ResourcePool claimed inside MoveByTransporter blocks spread across multiple independent process branches — this is cleaner than one AGV pool per cell and automatically creates contention when the fleet is undersized, making fleet-size a first-class experiment parameter without any additional logic.
