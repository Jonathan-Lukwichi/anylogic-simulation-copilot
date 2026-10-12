# Pattern card — Palletizing system with AGV (8.9.10 example: Palletizing System with AGV Transportation)
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Sizing a shared AGV fleet and picking-robot count for a multi-cell palletizing line where boxes arrive at variable rates and must be batched onto pallets before transport.

## Block chain
Boxes arrive at each of several independent palletizing cells via a Source at a configurable rate (boxes per minute). Inside each cell a picking robot places incoming boxes onto a pallet; once the pallet holds a full batch it exits via a Convey segment. The completed pallet then enters a MoveByTransporter block, which claims one of the shared AGVs from a central resource pool. The AGV carries the loaded pallet to the dispatch area, releases back to the pool, and the pallet passes through a final Convey belt before reaching a Sink. Empty pallets and interlayer sheets are pre-stocked in separate queues at startup and are fetched by cells on demand, creating a secondary material-handling loop alongside the main product flow.

## Resources
- **AGV fleet:** a Material Handling `TransporterFleet` `agvs` (2 × 1.2 × 2 m vehicles), capacity set by slider `AGVnumber` (default 3, range 1–5) — not a ResourcePool (corrected 2026-10-01 from the 8.9.10 `.alp`); AGV speed *not confirmed*.
- **Picking robots:** one robot per palletizing cell (3 cells by default); each robot is modelled as a dedicated resource inside the PalletizingCell sub-model.
- **Pallet & sheet buffers:** initial stocks are per cell — pallets `index + 3`, bottom sheets `(index + 1) * 2`, interlayer sheets 8 (corrected; not "10 + 10"); cells request more from a shared store.

## Key settings worth copying
- **Arrival rates:** per-cell sliders `initialBoxRate1/2/3` (default 3 boxes/min each, range 0–5); rates are hot-swappable at runtime via `source.set_rate(value, PER_MINUTE)`.
- **Batch size:** `palletBatchSize` slider (default 5, range 0–100) is the number of **empty pallets** requested and delivered per batch, and the capacity of each cell's left/right pallet stack — not boxes per pallet. A pallet is full at the cell parameter `palletCapacity`, loaded 4 boxes per layer (corrected).
- **Number of cells:** `numberOfCells` slider (default 3, up to 100); cells are instantiated as an agent population.
- **Time unit:** Seconds throughout; production-rate KPI is tallied hourly.
- **AGV speed and network grid:** *not confirmed in the 8.9.10 model* (an earlier version said 10 m/s and a 500 × 500 grid).

## KPIs instrumented
- **Throughput:** `productionRate` dataset — pallets completed per hour, sampled every hour via a cyclic event that resets `hourOutput` counter; plotted as a time-series chart.
- **AGV utilisation:** `agvs.resourcePool.utilization()` — displayed as a gauge.
- **Picking-robot utilisation:** `robot.getUtilization()` per cell — three separate gauges showing per-robot load.
- **Cell throughput:** `throughput` statistic inside each PalletizingCell sub-model.

## Reusable idea
Use a single shared AGV fleet (TransporterFleet) claimed inside MoveByTransporter blocks spread across multiple independent process branches — this is cleaner than one AGV pool per cell and automatically creates contention when the fleet is undersized, making fleet-size a first-class experiment parameter without any additional logic.

## Techniques in the 8.9.10 model (added 2026-10-01)
1. **ProcessByRobot for palletizing.** End point (x, y, z) with z from the current stack height (layers and sheets already placed); *End effector approaches* = top side; *Safe height* 2 m (Help 8.9.10 *ProcessByRobot*: an absolute minimum, ignored for path-controlled movement).
2. **One robot, three task types, fixed priorities** — bottom sheet > interlayer sheet > box. A `getPriority()` function returns the code of the most urgent non-empty queue; each task queue feeds a conditional Hold whose blocking condition is "priority is not mine"; every queue change calls a `checkHolds()` that runs `recalculateConditions()` on the three Holds (gotcha G85).
3. **Release exactly one** pallet or sheet pallet per request: Holds in *Block automatically after N agents* with *Initially blocked*, opened by `unblock()`.
4. **Stacks** are LIFO Queues whose *Agent location* is a node, with a stack index stored in On enter that raises each pallet's z.
5. **Starvation downtime.** A cell short of pallets or sheets records when its idle spell starts and ends, feeding a per-cell log and histogram (`downtimeSec`).
6. **Material requests as FIFO lists** of requesting cells; the AGV trip's destination is the head of the list. Returns of empty sheet pallets run at a higher MoveByTransporter *priority* than deliveries.

**When the co-pilot should use this:** end-of-line palletizing, robot cells fed by AGVs, and any case where one robot or operator serves several task types with a strict priority.
