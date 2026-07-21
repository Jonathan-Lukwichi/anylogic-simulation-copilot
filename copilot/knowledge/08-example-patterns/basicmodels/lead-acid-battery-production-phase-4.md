# Pattern card — Lead Acid Battery Production Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-stage lead-acid battery assembly line that combines conveyor transport, transporter vehicles, a crane, batching, and final assembly to expose throughput bottlenecks across heterogeneous material-handling equipment.

## Block chain
Individual electrode plates are generated in batches of 200 every 1.5 hours and immediately grouped into a PlatesBatch of 100 via a Batch block. The batch travels on a conveyor (Convey) to a pre-assembly buffer. A transporter fleet (MoveByTransporter) ferries batches from the buffer to a Delay station representing a chemical treatment step (2 minutes). After treatment an Unbatch block splits the lot back into individual plates, which ride a second conveyor to the main assembly area. There, an Assembler block waits for matching battery-block sub-assemblies that arrive via a separate Source; a MoveByCrane block uses a dedicated overhead crane to position heavy blocks before they enter the Assembler. Once the full battery is assembled, a Combine block joins the casing component (arriving on yet another conveyor from a third Source — batterySource), and the finished unit exits through a Sink. A Hold block upstream of the crane acts as a gate, releasing battery blocks only when the crane is free, preventing deadlocks between the transporter and crane paths.

## Resources
- TransporterFleet: one fleet serving the electrode pre-assembly route (seize/release pattern)
- Overhead crane (batteryBlockCrane): single-unit crane, seized/released around MoveByCrane blocks
- Conveyor segments: at least three separate conveyors (plates outbound, plates inbound to assembly, battery casing feed), speed 10 m/s, 1-metre grid spacing
- Assembler: joins electrode batch with battery block sub-assembly
- Combine: merges assembled cell stack with casing

## Key settings worth copying
- Arrival rate: 1 per hour with 200 entities per arrival burst (simulates pallet-level delivery rather than individual-unit trickle)
- Batch size: 100 plates per lot (PlatesBatch agent type)
- Chemical treatment Delay: 2 minutes per batch
- Conveyor speed: 10 MPS; cell size 1 m x 1 m
- Model time unit: seconds (fine-grained enough to capture conveyor travel accurately)
- Hold-before-crane pattern: prevents crane starvation / deadlock without complex logic
- Unbatch after treatment restores individual-entity tracking for assembly matching

## KPIs instrumented
- Conveyor and transporter utilisation (implicit through seize/release statistics)
- Assembler throughput (units completed at Sink)
- Queue length at pre-assembly buffer (preassembleElectrodeBuffer) and assembleArea
- Hold gate wait time (indirect measure of crane contention)

## Reusable idea
The transferable trick is the Batch → process → Unbatch sandwich: batch items into a lot for bulk transport/treatment, then unbatch them so the downstream Assembler can still match individual sub-components by type. This avoids the complexity of tracking every item through a resource-intensive step while preserving entity-level identity where it matters for final assembly.
