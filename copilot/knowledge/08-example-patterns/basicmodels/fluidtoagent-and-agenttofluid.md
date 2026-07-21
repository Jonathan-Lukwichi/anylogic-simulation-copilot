# Pattern card — FluidToAgent and AgentToFluid
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid/Continuous)
- **Problem it solves:** Bridging discrete-event agent flows and continuous fluid flows within a single model so that high-volume streams can be modelled cheaply as fluid while individual entities are tracked where detail matters.

## Block chain
Two complementary conversion paths run in parallel:

**Agent → Fluid path:** Discrete agents arrive via a `Source`, pass through a `Queue`, and enter an `AgentToFluid` block that dissolves them into a continuous fluid stream. The stream flows through `Pipeline` segments controlled by `Valve` blocks into a `Tank` that acts as a buffer.

**Fluid → Agent path:** A second `Tank` accumulates fluid. A `FluidToAgent` block watches the tank level and, once a threshold is reached, emits discrete agents at a configured batch rate. Those agents are then routed via `MoveTo` blocks and ultimately consumed by a `Sink`.

Both paths share the same model time unit (seconds) and can be observed side-by-side to verify mass/count conservation across the conversion boundary.

## Resources
- Two `Tank` objects (fluid buffers, each with a configurable capacity)
- Two `Pipeline` segments (fluid transport, with flow-rate capacity)
- Two `Valve` objects (flow gates; one is labelled "outputValve" with a settable maximum rate)
- One `Queue` (discrete agent buffer before dissolution)
- No ResourcePool / Seize / Release blocks — this model is not a staffed-service model

## Key settings worth copying
- **FluidToAgent threshold / batch size:** controls how many fluid units are converted into one agent — tune this to balance granularity vs. performance
- **Valve maximum rate:** caps the fluid throughput; expose as a model parameter to run sensitivity experiments
- **Tank capacity:** prevents overflow; set to match expected peak accumulation between conversion events
- **Model time unit:** Seconds — appropriate for fast-moving fluid processes; change to minutes/hours for slower industrial or supply-chain contexts
- **AgentToFluid rate:** must be consistent with the downstream pipeline capacity to avoid back-pressure artefacts

## KPIs instrumented
- Tank fluid level over time (content / fill percentage)
- Agent count entering and exiting the Fluid→Agent converter (throughput conservation check)
- Valve flow rate vs. maximum rate (utilisation of the valve constraint)
- Queue length before AgentToFluid (indicates back-pressure when fluid pipeline is at capacity)

## Reusable idea
The central transferable trick is **selective resolution switching**: model bulk flow as cheap continuous fluid for the portions of a system where individual identity does not matter, then crystallise discrete agents only at the point where per-entity decisions or attributes become necessary. This avoids the performance cost of tracking millions of individual agents while still producing trackable entities at key decision nodes — directly applicable to supply-chain bulk materials, patient cohort models, or high-volume call-centre traffic.
