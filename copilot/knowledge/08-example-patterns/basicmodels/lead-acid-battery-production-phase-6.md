# Pattern card — Lead Acid Battery Production Phase 6
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-stage lead-acid battery assembly line that coordinates conveyors, forklifts, and overhead cranes to move, batch, combine, and assemble electrode plates and battery blocks through to finished product.

## Block chain
Electrode plates are generated at a Source and conveyed along a belt (Convey) to a batching station (Batch) where a fixed plate count is grouped. Forklift transporters (MoveByTransporter) shuttle batched plates between stations. An Assembler merges plate groups into battery block sub-assemblies. A crane (MoveByCrane) lifts completed blocks while a second conveyor line brings battery cases through a separate Source → ConveyorEnter → Queue path. A Combine block joins the block and case streams; Hold blocks gate flow until both parts are ready. A further Assembler finalises the battery unit, which travels via conveyor to a Sink. Defective or overflow paths use a second Sink. Unbatch blocks split batches back into individual items where needed before downstream processing.

## Resources
- **TransporterFleet** (forklifts): two separate fleets with configurable capacity; each fleet is seized/released around MoveByTransporter steps
- **Crane** resources (overhead): two crane units (batteryBlockCrane and a second instance) seized via MoveByCrane blocks
- **Conveyors**: multiple Convey segments with individual speed parameters

## Key settings worth copying
- `batchSize` parameter on Batch blocks — controls how many plates are grouped before transport, drives throughput balance
- `speed` parameters on Convey, TransporterFleet, and Crane blocks — tune material-handling pace independently per resource type
- `capacity` on TransporterFleet and Hold blocks — limits concurrent jobs and acts as a buffer gate
- `seizeTransporter` / `releaseCrane` flags on move blocks — explicit resource acquisition pattern prevents deadlock
- Time unit: **Second** — fine-grained enough to distinguish conveyor travel time from crane cycle time
- `capacityDefinitionType` + `capacitySchedule` on fleet — allows shift-based capacity variation

## KPIs instrumented
- Throughput at each Sink (finished batteries per unit time)
- Queue length at ConveyorEnter and Queue blocks (buffer fill level)
- Transporter and crane utilisation (fraction of time seized vs. idle)
- Hold block content (how long the gate waits for the slower sub-stream)

## Reusable idea
The transferable trick is the **dual-stream Combine with Hold gating**: two independent production lines (plates and cases) run at different speeds; Hold blocks park the faster stream until the slower one catches up, then Combine merges them. This pattern cleanly handles any assembly scenario where two asynchronous sub-processes must synchronise before a final join, without requiring a shared queue or complex conditional logic.
