# Pattern card — FluidEnter and FluidExit
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous)
- **Problem it solves:** Demonstrates how to bridge discrete-event process flows and continuous fluid pipelines using FluidEnter and FluidExit connectors so that bulk material or liquid can move in and out of Tank blocks while interacting with agent-based or event-driven logic.

## Block chain
A FluidSource generates continuous flow (measured in cubic metres per second). That flow feeds into a Tank which stores the bulk volume. FluidExit drains fluid out of the tank into a downstream pipe or disposal point (FluidDispose). In the reverse direction, FluidEnter injects fluid arriving from an external pipe back into a tank. Multiple FluidEnter and FluidExit blocks are demonstrated in parallel, showing that a single tank can have several simultaneous input and output connections operating concurrently.

## Resources
- Tank capacity: 1 000 m³, pre-filled to 1 000 m³ at simulation start
- Maximum drain rate per FluidExit: 10 m³/s
- FluidSource output rate: configurable (rate parameter, units = m³/s); default left open (no explicit constant coded in the base source)

## Key settings worth copying
- **Tank.capacity** = 1000 CUBIC_METER and **Tank.initialAmount** = 1000 CUBIC_METER — start fully loaded
- **Tank.limitRateOut** = true, **Tank.maxRateOut** = 10 CUBIC_METER_PER_SECOND — cap the discharge rate to prevent instantaneous emptying
- **FluidSource.rate** unit set to CUBIC_METER_PER_SECOND — always declare explicit flow-rate units to avoid unit-mismatch errors
- Model time unit: Second — align all rate and duration expressions accordingly
- **customInitialBatch** = true on Tank — allows the initial fill to be treated as a named batch for colour tracking in the flowchart

## KPIs instrumented
- Tank fluid level over time (implicit through Tank.level())
- Effective inflow vs. outflow rates (observable via FluidEnter.flowRate() and FluidExit.flowRate())
- n/a — no explicit dashboard charts defined in the model; KPIs are read directly from block statistics

## Reusable idea
Use FluidEnter / FluidExit as explicit seams between a continuous fluid network and discrete logic: anywhere an agent-triggered event (e.g., a valve opening) must start or stop bulk flow, wire a FluidEnter or FluidExit at that seam and control its rate programmatically from the agent's state-chart or on-action code. This cleanly separates the continuous physics (inside the fluid library) from the discrete decision logic (outside it).
