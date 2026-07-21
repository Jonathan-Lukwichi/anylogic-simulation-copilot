# Pattern card — Agent per Fluid Batch
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (Fluid / Continuous + DES agent generation)
- **Problem it solves:** Represent a bulk material stream as a continuous fluid and automatically spawn one discrete agent every time a fixed-volume batch completes its journey through the system.

## Block chain
FluidSource (continuous inflow at a configured rate) -> Valve (gate control, opens/closes flow) -> BulkConveyor (carries bulk material along a physical path, visualised as a belt/heap) -> FluidConvert (monitors inflow rate; when rate drops to zero it closes one batch and triggers downstream notification) -> FluidToAgent (converts the completed fluid batch into a single discrete agent) -> Queue (buffers the generated agents) -> Convey (moves agents along a conveyor path) -> Sink (agents exit the system)

Two parallel BulkConveyor + FluidConvert + FluidToAgent branches feed into the same Queue, demonstrating that multiple fluid streams can independently produce agents that then merge into one discrete flow.

## Resources
n/a — no ResourcePool or Seize/Release blocks are used. Material flow is governed by the Valve open/close state and the rate parameter of FluidSource. A Heap 3-D shape provides visual feedback of accumulated bulk material.

## Key settings worth copying
- **Time unit:** Second
- **FluidSource rate:** exposed as a named parameter (`rate`) so it can be varied per experiment without editing the block
- **Batch size (FluidConvert):** set via `uniform_discr(100)` — a randomly drawn integer up to 100 units, assigned each time a new batch begins; this makes every batch a different size
- **Batch colour:** assigned with `randomColor()` at batch-start so each agent carries a visually distinct colour inherited from its parent fluid batch
- **Trigger mechanism:** FluidConvert uses a `rate`-change event in cyclic mode — when inflow rate falls to zero it calls `setBatchOut(...)`, which is the signal FluidToAgent listens for to emit the agent
- **Valve:** acts as an on/off switch upstream of each conveyor; toggling it starts/stops discrete batches

## KPIs instrumented
n/a — the example is illustrative rather than metric-focused; no explicit KPI charts or data sets are wired up. Throughput can be inferred from Sink agent counts; batch volume is implicit in the FluidConvert batch-size setting.

## Reusable idea
Use **FluidConvert + FluidToAgent** as a "batch detector" bridge: let your process run as an efficient continuous fluid for as long as material is flowing, then automatically harvest one agent per completed batch the moment the valve closes or the inflow stops. This avoids modelling every unit as a separate agent during bulk transport while still giving you a discrete, attribute-carrying entity (with colour, size, or any custom data) for downstream DES logic such as quality checks, labelling, or order tracking.
