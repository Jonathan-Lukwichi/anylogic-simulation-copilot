# Pattern card — FluidSource
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Demonstrates how a continuous fluid source block generates flow at a fixed rate or injects discrete boluses into a fluid pipeline, illustrating the two operating modes of AnyLogic's Fluid Library.

## Block chain
FluidSource → FluidDispose

A single FluidSource block produces a steady stream of fluid (treated as a continuous quantity rather than discrete agents). The outflow connects directly to a FluidDispose block, which acts as a drain/sink absorbing whatever volume arrives. No intermediate tanks or pipes are included; the chain is intentionally minimal to isolate the source's behaviour.

## Resources
n/a — no resource pools or agent populations; the model works purely with continuous fluid volume.

## Key settings worth copying
- **Rate parameter** on FluidSource controls the continuous flow rate (units of volume per second; model time unit is Second).
- **infiniteCapacity toggle**: when set to true the source produces unlimited flow at the defined rate; when false it operates in finite-capacity mode and can be topped up programmatically.
- **inject(amount) call**: triggers an on-demand bolus injection (e.g., `fluidSource.inject(1000)`) — useful for modelling batch releases or pump strokes on a button press.
- The radio button in the UI switches between the two capacity modes at runtime, making it easy to compare behaviours in a single run.

## KPIs instrumented
- **amountPassed()**: running total of fluid volume that has left the source, displayed live as "Amount passed: \<value\>". No wait-time or utilisation metrics — throughput volume is the single KPI.

## Reusable idea
The inject-vs-rate duality: any fluid or bulk-material model benefits from offering both a continuous rate mode (steady-state flow) and an on-demand injection mode (event-driven pulse). Exposing both via a runtime toggle — rather than two separate models — lets analysts test surge scenarios (e.g., emergency tank fill, demand spike) without rebuilding the model.
