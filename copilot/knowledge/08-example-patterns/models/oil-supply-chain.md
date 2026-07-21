# Pattern card — Oil Supply Chain
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD fluid dynamics)
- **Problem it solves:** Model the end-to-end flow of crude oil and refined fuel across tankers, pipelines, refineries, terminal storages, and last-mile truck delivery to retailers, with stochastic retail demand.

## Block chain
Crude oil arrives at port storage tanks via sea tankers (agent population). Pipeline networks carry crude to refineries, where it is processed at a configurable refining rate (m³/s) into refined fuel. A fluid-split distributes output across multiple terminal storage sites. From terminals, fuel trucks (agent population) haul product to retailer agents, each holding their own local stock. Demand at the retail tier varies randomly around a mean level that the user controls as a parameter. The model is geospatially embedded — agent nodes sit on a real map and trucks route via GraphHopper; pipelines are modelled as fluid connectors (FluidEnter / FluidExit / FluidSplit / Valve / Tank) rather than discrete queues. Each major node type (Tanker, FuelTruck, Storage, Refinery, Pipeline, PipelineNode, Retailer) is a separate agent class with bidirectional links to its neighbours.

## Resources
- **Tanker fleet** — agent population, transports crude to port
- **Refinery agents** — each has an internal Tank (crude buffer) and a Valve that throttles the refining_rate parameter (m³/s)
- **Pipeline network** — fluid-connector graph linking port → refinery → terminal storage
- **FuelTruck fleet** — agent population dispatched from terminals to retailers
- **Retailer agents** — each maintains a totalStock variable; aggregate tracked as retailers.totalStock()
- **Storage agents** — intermediate buffer nodes on both the crude and product sides

## Key settings worth copying
- **Time unit:** Hour (fine-grained enough to capture truck turnaround and pipeline transit)
- **Flow rate units:** LITER_PER_SECOND (crude side) and CUBIC_METER_PER_SECOND (product side) — use different unit scales per segment to keep numbers readable
- **Refining rate:** exposed as a slider parameter on the Refinery agent so sensitivity runs require no code change
- **Demand:** randomly varied around a user-set mean — wire a uniform or normal draw to the retailer's consumption rate
- **Routing:** GraphHopper engine attached to truck agents for realistic road-distance dispatch decisions
- **Agent links:** COLLECTION_OF_LINKS with bidirectional=true; each node holds up to 2 connections, enabling branching pipeline topology without hardcoding

## KPIs instrumented
- **retailers.totalStock()** — aggregate retail inventory level over time (main supply-security KPI)
- Pipeline fill levels visible per Tank agent
- Refinery throughput (refining_rate × time)
- Truck fleet utilisation implicit in dispatch frequency vs. demand rate

## Reusable idea
Mix fluid-library blocks (Tank, Valve, FluidSplit) for continuous bulk flows with discrete agent populations (Tanker, FuelTruck) for vehicle movements — this hybrid lets you model both the high-volume pipeline segment and the individual trip economics in a single model without approximation on either side.
