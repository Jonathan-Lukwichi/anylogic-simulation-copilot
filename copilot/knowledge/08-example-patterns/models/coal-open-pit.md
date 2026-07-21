# Pattern card — Coal Open Pit
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid)
- **Problem it solves:** Simulate the full lifecycle of an open-pit coal mine — from initial drilling and blasting through ore enrichment to final backfilling — tracking both discrete vehicle movements and continuous bulk-material flows.

## Block chain
The model unfolds in two interleaved layers. The discrete layer drives agent-based equipment: drillers seize a Delay block to bore holes, then release; chargers load explosives; LHD loaders and miners use SeizeTransporter / ReleaseTransporter pairs to haul blasted rock. Trucks (configurable count) and railroad trains carry product out of the pit. The continuous (fluid) layer models bulk ore as a flowing medium through Pipelines, BulkConveyors, FluidPickup, Dropoff, FluidMerge, and FluidSplit blocks. Inside the beneficiation centre, FluidSplit divides the ore slurry into three streams — useful concentrate, tailings (waste), and an intermediate fraction that loops back for reprocessing — mimicking froth flotation. FluidToAgent converters hand finished concentrate back to the discrete world (trucks/trains) for dispatch to the coal dump. The simulation ends when the pit volume is exhausted; waste from the fluid circuit is then routed back to backfill the pit.

## Resources
- Drillers: configurable count (`drillerAmount` slider), tracked via SeizeTransporter / ReleaseTransporter
- LHD loaders and Miners: separate transporter pools, each seized per haul cycle
- Trucks: `truckAmount` slider; volume capped by `TRUCK_MAX_VOLUME` constant
- Railroad trains: two loading points (`trainLoadingBack1`, `trainLoadingBack2`); weekly train counts tracked
- Flotation unit: rate-controlled by `flotationSpeed` and `effectivenessFlotation` parameters
- Service vehicles: three service stops (`service1Stop`, `service2Stop`, `service3Stop`); `serviceTime` parameter

## Key settings worth copying
- `drillingSpeed` and `maxDrillerDurability` / `workingCyclesDriller` — driller wear-out governs when equipment must be replaced mid-run
- `flotationSpeed` + `effectivenessFlotation` — two-knob control of beneficiation yield; vary together to study concentrate recovery vs. throughput trade-off
- `TRUCK_MAX_VOLUME` — discrete payload cap bridges the fluid-to-agent boundary (FluidToAgent block)
- Time unit: **Minute** — appropriate for equipment-cycle granularity in mining
- Backfilling triggered by a state/timestamp (`backfillingStamp`) rather than a fixed schedule, so it activates automatically when ore is depleted

## KPIs instrumented
- Weekly truck dispatches (`lastWeekTrucks`) and train dispatches (`lastWeekTrains`)
- Cumulative concentrate yield (tracked through fluid exit points)
- Equipment utilisation implied by driller work cycles vs. durability limit
- Pit volume remaining (drives simulation termination and backfill trigger)

## Reusable idea
**Use FluidSplit + a recycle loop to model yield-loss processes.** Whenever a process produces good product, waste, and a rework fraction (flotation, casting, chemical reaction), route three fluid branches: one to the next stage, one to a waste sink, and one back to the inlet merge. The split ratios become tunable parameters (`effectivenessFlotation`), making sensitivity analysis on recovery rate trivial without restructuring the flowchart.
