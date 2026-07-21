# Pattern card — Lead Acid Battery Production Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a conveyor-and-transporter-based battery-plate production line where individual electrodes are batched before being moved by forklifts to downstream processing.

## Block chain
Electrodes arrive at a Source in bursts (200 units every 1.5 hours) and travel along a Conveyor. A Batch block accumulates 100 electrodes into a PlatesBatch entity. Two separate MoveByTransporter stages use a shared forklift fleet to carry batches between stations. A Delay block represents a fixed 2-minute process step. A second MoveByTransporter routes finished batches onward (optionally to a pre-assembly buffer named `preassembleElectrodeBuffer`). The flow terminates at a Sink.

## Resources
- **TransporterFleet `forklifts`** — fleet capacity of 2 forklift agents (type `Forklift`), operating with free-space navigation, home node `forkliftsHomeLocation`, turn radius 1 m.
- **Conveyor** — used to transport individual Electrode entities before batching; speed configured via block parameters.
- No ResourcePool blocks; material handling is handled entirely by the TransporterFleet.

## Key settings worth copying
- **Source arrivals:** interarrival time = 1.5 hours; `entitiesPerArrival = 200` (bulk burst pattern)
- **Batch size:** 100 electrodes per PlatesBatch (entity type substitution on Batch block)
- **Delay time:** 2 minutes (fixed, no distribution — deterministic process step)
- **Forklift fleet size:** 2 units (easy sensitivity-analysis knob)
- **Navigation:** FREE_SPACE_NAVIGATION with 1 m turn radius
- **Time unit:** Seconds (fine-grained for conveyor speed accuracy)
- **Entity hierarchy:** raw `Electrode` agents batched into `PlatesBatch` composite agents — keeps downstream logic clean

## KPIs instrumented
- Throughput at the Sink (PlatesBatch count)
- Forklift utilisation (implicit through TransporterFleet statistics)
- Delay block occupancy (queue build-up before the 2-minute process step)
- Conveyor occupancy upstream of the Batch block

## Reusable idea
Use AnyLogic's Batch block with a custom composite entity type (here `PlatesBatch`) to convert a high-volume stream of small parts into manageable unit-load packets, then hand those packets off to a TransporterFleet — this cleanly separates the "many small parts on a conveyor" phase from the "bulk transport by vehicle" phase and makes fleet-sizing experiments straightforward.
