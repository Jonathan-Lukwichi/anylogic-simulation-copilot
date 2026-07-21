# Pattern card — Lead Acid Battery Production Phase 8
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-stage lead-acid battery assembly line combining electrode preparation, conveyor transport, crane handling, forklift logistics, and final cell assembly to evaluate throughput and equipment utilisation.

## Block chain
Battery components (anodes and cathodes) are generated at a Source and routed through two parallel PrepareElectrode sub-processes — one for each electrode type. Prepared plates travel on Conveyors via ConveyorEnter blocks and are staged in Queues. A MoveByCrane block lifts batches between work areas; Hold blocks gate flow until a matching set of anodes and cathodes is ready. Combine blocks pair the two electrode streams, and Assembler blocks join electrode groups into battery cells. Forklifts (MoveByTransporter) shuttle heavier sub-assemblies between stations. Finished batteries exit through Sink blocks; rejected or overflow paths have their own Sink exits.

## Resources
- **TransporterFleet** — a fleet of Forklift agents for inter-station transport
- **ResourcePool** — Operator agents assigned to assembly stations
- **Cranes** — modelled via MoveByCrane blocks for overhead lifting between conveyor lines
- Capacities and fleet sizes are configured per-block; the model supports dynamic adjustment via set_batchSize()

## Key settings worth copying
- **Time unit:** Seconds (fine-grained production timing)
- **Electrode type enum:** ANODE / CATHODE option list drives parallel branch routing
- **Assembler** blocks configured with multiple input ports to enforce part-count requirements before joining
- **Hold** blocks used as synchronisation gates — release only when both electrode streams are available
- **Combine** merges two streams into one token representing a matched electrode pair before final assembly
- **ConveyorEnter** places items onto a named Conveyor object, decoupling flow logic from physical belt speed

## KPIs instrumented
- Throughput (batteries completed per shift — counted at Sink)
- Queue length and wait time at electrode-staging queues
- Crane and forklift utilisation (fraction of time busy)
- Operator resource utilisation via ResourcePool statistics
- Hold block wait time (synchronisation delay between anode and cathode streams)

## Reusable idea
The key transferable trick is the **dual-stream synchronisation gate**: run two independent preparation pipelines in parallel, buffer each in a Queue, then use a Hold block as a gate that only releases when both streams have a unit available, followed immediately by a Combine to merge them. This pattern cleanly handles any assembly process that requires matched sets of components arriving at different rates, without polling or complex event logic.
