# Pattern card — FluidSelectOutput
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous)
- **Problem it solves:** Demonstrates how to split a continuous fluid stream into two separate output paths using a condition or toggle, mirroring a SelectOutput block but for bulk/fluid flows.

## Block chain
A FluidSource generates a continuous stream at a fixed rate (capacity 100, max rate 10 units/second). That stream feeds into a FluidSelectOutput block, which routes the flow to one of two downstream FluidDispose sinks depending on a Boolean selector. When the selector flag (`selectOutput1`) is true, the flow exits through `out2`; otherwise it exits through `out1`. Each branch terminates at its own FluidDispose, absorbing whatever volume arrives.

## Resources
n/a — no resource pools or agent populations; this is a pure fluid (continuous) model with no capacity constraints beyond the source rate.

## Key settings worth copying
- **Source rate:** 100 units capacity, 10 units/second max rate
- **Time unit:** Seconds
- **Routing condition:** Boolean flag `selectOutput1` on the FluidSelectOutput block; toggling it at runtime redirects 100 % of the flow instantly to the other output
- **Rate limiting on outputs:** Each output port has its own optional max-rate cap (`limitRateOut` / `maxRateOut`) — useful when downstream pipes have different throughput constraints
- **No stochastic distributions** — this model is fully deterministic; all variability is introduced only by changing the selector flag

## KPIs instrumented
- Flow rate through each output branch (implicit via FluidDispose inflow tracking)
- UI controls expose the `selectOutput1` toggle so users can observe the live rerouting effect during simulation runs

## Reusable idea
The key transferable trick is using a **single Boolean parameter as a live routing switch** on a fluid block: because FluidSelectOutput responds immediately to a condition change, you can model valve-like switching, product-grade diversion, or priority-overflow logic in any continuous-flow system (tanks, pipelines, chemical processes) without stopping or restarting the simulation. Pair this with a slider or event-triggered assignment to simulate scheduled changeovers or demand-driven diversion.
