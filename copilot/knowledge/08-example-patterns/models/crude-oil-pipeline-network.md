# Pattern card — Crude Oil Pipeline Network
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid/Continuous)
- **Problem it solves:** Simulate multi-commodity batch flow through a parameterized pipeline network with tank storage, commodity-aware dispatch logic, and random pipeline failures.

## Block chain
Batches (agents) are injected at source terminals (Austin, Houston, Port Arthur) via a DES Source block and immediately converted into fluid volumes using AgentToFluid blocks. Each OilPipeline wraps a Fluid Library Pipeline block that is dynamically reconnected at startup based on DB-defined topology. Batches queue inside OilTank (Fluid Library Tank) blocks at intermediate terminals. A terminal dispatch event fires whenever a batch arrives or finishes pushing out, selecting the best available tank using a commodity-and-destination matching rule, then rewiring FluidExit/FluidEnter connections on the fly. When a pipeline fails (drawn from DB-stored MTTF/MTTR), flow rate drops to zero for the repair duration, causing upstream tanks to queue. Batches exit at destination terminals and delivery time is recorded.

## Resources
- OilPipeline objects: one per network link; capacity and flow rate (m3/day) read from DB
- OilTank objects: multiple per terminal; each holds one commodity type at a time
- Commodities: five types (A–E), tracked by color-coded batch visualization
- Terminal nodes: source terminals (3) and destination terminals (3)

## Key settings worth copying
- Batch inter-arrival: exponential with mean 2 hours, origin chosen with equal probability across 3 source terminals
- Batch size: uniform(10 000, 30 000) cubic meters
- Commodity assignment: uniform discrete over 5 types (A–E)
- Destination: uniform discrete over 3 destinations (Chicago, Minneapolis, Lima)
- MTTF and MTTR: per-pipeline values stored in DB tables, read at startup
- Pipeline failure modeled as rate = 0 for repair duration (no structural disconnect needed)
- Time unit: Day
- Network topology and all capacities fully driven from DB tables — zero hard-coded structure

## KPIs instrumented
- Throughput (volume delivered per time unit, per terminal and network-wide)
- Pipeline utilization (fraction of time at full flow vs. failed/idle)
- Batch delivery time (DES entity lifetime from injection to destination arrival)
- Tank fill levels (continuous fluid quantity, visualized per tank)

## Reusable idea
**DB-driven self-configuration with dynamic fluid reconnection.** The model reads topology, capacities, and failure parameters entirely from database tables at startup, then programmatically creates and wires all network objects. This means adding a new pipeline or terminal requires only a new DB row — no model logic changes. Combining this with on-the-fly FluidExit/FluidEnter rewiring lets a single generic OilPipeline/OilTank component handle any network shape, making the pattern directly portable to water distribution, gas networks, or any flow network where topology changes frequently.
