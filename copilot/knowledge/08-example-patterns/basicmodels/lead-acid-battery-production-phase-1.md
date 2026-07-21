# Pattern card — Lead Acid Battery Production Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a conveyor-based electrode plate manufacturing line where individual plates are produced, transported on a conveyor, and batched into groups before leaving the system.

## Block chain
Electrodes (agent type) are created by a **Source** in bulk arrivals (200 units every 1.5 hours) → placed on a **Conveyor** (Material Handling library `Convey` block) that moves items at 10 m/s along a physical layout path → a **Batch** block collects 100 individual plates into a single `PlatesBatch` agent → the batch exits through a **Sink**. A secondary **Source** feeds a parallel `Batch` that groups plates into a different aggregate, representing a pasting-machine station on the conveyor line.

## Resources
No explicit `ResourcePool`/`Seize`/`Release` blocks. Throughput is governed by conveyor speed and batch accumulation time. The pasting machine is represented as a `ConveyorSimpleStationDescriptor` on the conveyor path rather than a resource pool.

## Key settings worth copying
- **Arrival pattern:** interarrival time = 1.5 hours, 200 entities per arrival (bulk drop onto conveyor)
- **Batch size:** 100 plates per batch
- **Conveyor speed:** 10 m/s; physical scale 1 m per animation unit
- **Time unit:** Seconds (fine-grained for conveyor travel)
- **Agent types:** `Electrode` (individual plate), `PlatesBatch` (assembled group of 100)
- **Layout:** Background image (`lead_acid_battery_production_layout.png`) with area nodes and conveyor path descriptors for realistic floor-plan routing

## KPIs instrumented
- **Throughput:** tracked via the `throughput` parameter on the Batch/Sink blocks
- Conveyor occupancy is observable through the 3D/2D animation; no explicit utilization statistic block found in Phase 1 (likely expanded in later phases)

## Reusable idea
The key transferable trick is the **bulk-arrival + conveyor + batch accumulation** pattern: generate many small items at once (simulating a production run), transport them on a conveyor at physical speed, then re-aggregate them into a higher-level batch agent before downstream processing. This cleanly separates the "individual part" agent from the "assembly lot" agent and lets the conveyor simulation drive realistic cycle times without needing explicit service-time distributions.
