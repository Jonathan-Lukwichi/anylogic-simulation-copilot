# Pattern card — Lead Acid Battery Production Phase 7
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-stage battery manufacturing line that merges electrode sub-assemblies with battery casings using conveyors, cranes, and transporters, exposing throughput bottlenecks in material handling.

## Block chain
Two parallel `PrepareElectrode` sub-processes (one per electrode type) each run a `Source` → internal delay pipeline at a 1.5-hour cycle, feeding finished electrodes into the main line. The main battery casing `Source` (named `batterySource`) generates casings at a fixed rate per hour. Casings ride a `ConveyorEnter` → `Convey` belt to a `Combine` block that waits for matching electrode sets. Once combined, a `MoveByCrane` block seizes a `CraneFleet` to lift the assembly to the next station. A `MoveByTransporter` block then uses a `TransporterFleet` to carry the unit through an `Assembler` block (final assembly / casing close), followed by another `Convey` segment to the `Sink`. A `Hold` block gates flow between the crane transfer and the assembler, preventing pile-up when the assembler is busy. A second `MoveByCrane` + `Combine` pair handles an intermediate merging step (e.g., acid fill tray docking). Defective items are stochastically routed out via a `randomTrue(0.01)` check (1 % scrap rate) to a secondary `Sink`.

## Resources
- **CraneFleet** — overhead crane pool; at least one crane instance (`batteryBlockCrane`); seize/release wrappers in `MoveByCrane` blocks
- **TransporterFleet** — autonomous ground transporter pool; capacity configured via fleet parameter; used in `MoveByTransporter` for inter-station transfer
- **Assembler** — acts as a multi-input assembly station; capacity drawn from its own queue

## Key settings worth copying
- Model time unit: **Second** (fine-grained for conveyor speed realism)
- `PrepareElectrode` sub-process interarrival: **1.5 hours** per electrode batch
- Electrode sub-process internal steps use **0.5-minute** handling delays
- Conveyor segment speeds: **10.0 m/s** (or model-unit equivalent) as the default; speed-restricted flag per segment allows per-segment tuning
- Scrap routing: `randomTrue(0.01)` — 1 % random defect diversion before the final sink
- `Hold` block used as a pacing gate between crane release and downstream assembler to prevent over-queuing

## KPIs instrumented
- Throughput at the final `Sink` (completed batteries per shift)
- Queue content upstream of `Combine` blocks (electrode starvation indicator)
- Crane and transporter utilisation (seize/release timing)
- Scrap count at secondary `Sink`

## Reusable idea
Use a `Hold` block as a flow-pacing gate between an overhead crane release and a downstream assembly station: the crane releases the unit, the `Hold` checks whether the assembler has free capacity before unblocking, preventing a pile-up of in-transit units when the assembler is the bottleneck. This pattern cleanly decouples material-handling resources from processing resources without needing custom Java logic.
