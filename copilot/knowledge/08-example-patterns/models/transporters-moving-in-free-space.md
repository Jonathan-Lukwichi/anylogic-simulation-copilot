# Pattern card — Transporters Moving in Free Space
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model autonomous mobile robots (AGVs) navigating an open factory floor without fixed guide paths, while routing parts through conveyors, racks, and workstation buffers.

## Block chain
Two independent AGV fleets operate in parallel. The first fleet shuttles work-in-progress items across three workshops: entities exit a Source (pre-loaded with 20 items at startup), ride Convey segments between workstations, and are handed off via MoveByTransporter blocks that claim a vehicle, carry the item to the next conveyor or buffer, then release it. SelectOutput blocks at branch points decide which downstream station receives each item; Delay blocks model processing time at each workstation. A Sink terminates completed items. The second fleet handles parts replenishment: parts are retrieved from a rack-based Store via Retrieve blocks, moved by a dedicated TransporterFleet to workstation 3 sub-stations, and placed into local buffers (Store/Convey). SeizeTransporter / release pairs appear wherever fine-grained manual control of vehicle allocation is needed (e.g., picking up a pallet from a rack). Split blocks divide a batch into sub-items; Enter re-injects sub-items into a sub-flow.

## Resources
- **TransporterFleet "AGVs"** — assembly-line AGV pool; fleet size and maximum speed (agvSpeed, m/s) are slider-controlled at runtime.
- **TransporterFleet "partsStorageAGVs"** — dedicated parts-storage fleet; separate speed slider (partsStorageAGVSpeed, m/s).
- Individual conveyor segments each expose their own speed parameter (ws1_conveyorSpeed, ws2_conveyorSpeed, ws3_conveyorSpeed, m/s).
- No human-resource pools; all capacity is vehicle-count and conveyor-speed.

## Key settings worth copying
- **Model time unit:** Second (MPS speed units align naturally).
- **Startup injection:** `source.inject(20)` pre-loads 20 entities at time 0 instead of relying on a stochastic arrival rate — useful for warm-starting a system with known WIP.
- **Free-space navigation:** transporters use shortest-path + collision-avoidance automatically; no path network nodes required.
- **Runtime sliders:** fleet speed and conveyor speed are exposed as adjustable parameters so users can observe throughput sensitivity without restarting the simulation.
- **3D view activated on startup:** `navigate(view3D)` gives an immediate spatial overview; a density map is hidden by default and can be toggled.
- **Click-to-inspect:** clicking an AGV in the animation sets `selectedAGV`, enabling a panel that shows per-vehicle statistics.

## KPIs instrumented
- **AGV fleet utilization:** `AGVs.utilization()` — fraction of time the assembly-line fleet is busy carrying items.
- **Parts-storage AGV utilization:** `partsStorageAGVs.utilization()` — same metric for the replenishment fleet.
- **Item waiting time for vehicles:** time entities spend in queue waiting for a free transporter, displayed as running statistics.
- Per-AGV personal statistics (trip count, idle time) accessible via the click-to-select panel.

## Reusable idea
Expose fleet speed (and conveyor speed) as interactive sliders rather than fixed parameters, then display utilization live — this lets a practitioner instantly see the tipping point where adding one more AGV (or increasing speed) stops improving throughput, making fleet-sizing decisions transparent without running a formal experiment.
