# Pattern card — FluidSelectInput
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous)
- **Problem it solves:** Merging two independent fluid streams into one combined output using a single junction block.

## Block chain
Two separate FluidSource blocks each emit a continuous flow at a fixed rate. Both feeds connect into a single FluidSelectInput block, which acts as a two-inlet merge junction — it accepts fluid from either or both inlets simultaneously and forwards the combined stream downstream. A FluidDispose block at the end absorbs the merged output, representing a sink or downstream process.

## Resources
No resource pools or agent populations. Capacity is implicitly unlimited at the FluidSelectInput junction; the effective throughput is bounded by the sum of the upstream source rates.

## Key settings worth copying
- Both FluidSource blocks configured at **1 m³/s** each (unit: CUBIC_METER_PER_SECOND), giving a combined merge rate of 2 m³/s.
- Model time unit: **Second**.
- FluidSelectInput parameters include `selectInput1` (inlet selector), `limitRateOut` / `maxRateOut` (optional output rate cap), and callbacks `onNewBatchIn1`, `onNewBatchIn2`, `onRateChange` for monitoring batch arrivals or rate shifts.
- Batch coloring on each source (`batchColor`) lets you visually distinguish which inlet's fluid is flowing through the merged stream.

## KPIs instrumented
n/a — the baseline model demonstrates topology rather than measuring KPIs; instrumentation would be added by connecting a FluidTank or level sensors to track accumulated volume over time.

## Reusable idea
Use **FluidSelectInput** whenever you need to consolidate multiple upstream fluid pipelines into one pipe without writing custom mixing logic — it is the fluid-library equivalent of a traffic merge lane and handles priority, rate-limiting, and batch-tracking at the junction out of the box.
