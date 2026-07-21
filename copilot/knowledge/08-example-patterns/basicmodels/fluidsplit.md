# Pattern card — FluidSplit
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous)
- **Problem it solves:** Divides a continuous fluid stream from a single source into two separate output flows according to fixed proportions.

## Block chain
A single **FluidSource** generates flow at a constant rate and feeds into a **FluidSplit** block. The splitter routes the incoming stream to two outlets (out1 and out2), each directed to its own **FluidDispose** sink. The chain is therefore: FluidSource → FluidSplit → [FluidDispose-1, FluidDispose-2].

## Resources
n/a (no resource pools; the model is purely continuous-flow with no capacity constraints)

## Key settings worth copying
- **Time unit:** Second
- **FluidSource rate:** constant value set on the `rate` parameter (units per second)
- **FluidSplit fractions:** `fraction1` and `fraction2` parameters on the FluidSplit block define what share of total inflow goes to each outlet (they should sum to 1.0)
- **Monitoring:** output port flow rates are read via `fluidSplit.out1.rate()` and `fluidSplit.out2.rate()` expressions, useful for live chart displays

## KPIs instrumented
- Flow rate on each output branch (`out1.rate()`, `out2.rate()`)
- (Implicitly) total throughput equals source rate; individual branch throughput equals fraction × source rate

## Reusable idea
The transferable trick is using **FluidSplit fraction parameters** to split any continuous stream proportionally without writing custom logic — simply set fraction1 and fraction2, connect two sinks, and read each branch's live rate for dashboards. This pattern applies directly to supply-chain liquid flows, pipeline networks, or any proportional resource-splitting scenario.
