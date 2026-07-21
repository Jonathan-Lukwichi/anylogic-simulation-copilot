# Pattern card — Activity Based Costing Analysis
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Computes per-unit cost broken down by activity category (waiting, processing, conveying, idle resource) so engineers can see where money is actually consumed inside a production or service flow.

## Block chain
Entities arrive via a **Source** at a configurable arrival rate and join an auxiliary **Queue** before competing for **Resource A** (Seize → Delay → Release). After release they join a second auxiliary **Queue** for **Resource B** (Seize → Delay → Release). Between and after the resource stages a **Conveyor** moves entities through space; cost accumulates on each entity during conveyor travel. Entities exit at a **Sink** and their lifetime cost contribution is folded into system-wide accumulators. A reset function zeroes all accumulators at the start of each run so experiments are independent.

## Resources
- **Resource A** — parameterised capacity (integer), busy-cost rate ($/hr) and idle-cost rate ($/hr) set via experiment sliders  
- **Resource B** — same structure as Resource A with independent capacity and cost rates  
- **Conveyor** — parameterised speed; cost per unit distance scales with speed squared (quadratic move-cost relationship)

## Key settings worth copying
- `ArrivalRate` — inter-arrival parameter, units = per Day (model time unit is Day)  
- `MeanProcessDelay` — mean service time shared across both resource stages  
- `ConveyorSpeed` — drives both throughput time and move cost simultaneously  
- Per-resource **busy cost/hr** and **idle cost/hr** — split so idle capacity is never hidden  
- **Existence cost/hr** — overhead charge applied regardless of utilisation  
- `RelativeProcessingCost` and `RelativeMoveCost` — dimensionless multipliers that let you weight activity types without changing physical parameters  
- Accumulators reset in an `onStartRun` hook: `accumSeizeAQCost`, `accumSeizeBQCost`, `accumConveyorQCost`, `accumProcessCost`, `accumMoveCost`

## KPIs instrumented
- **Total cost per product** — `totalCostPerProduct()` = (idle cost A + idle cost B + waiting cost + process cost + move cost) / product count  
- **Queue free slots** — `seizeA.queue.capacity - seizeA.queue.size()` displayed live  
- **Per-activity cost buckets** — waiting in queue A, waiting in queue B, conveyor waiting, processing, movement — each tracked in a separate accumulator  
- **Throughput** — implicit via `productCount` used in cost normalisation

## Reusable idea
Attach a **CostType enum and an `UpdateCost()` method on the agent class** so each block (Seize entry, Conveyor entry, Release exit) fires a single call that timestamps and categorises the cost increment. This pattern cleanly separates cost accounting from routing logic and makes it trivial to add a new cost category by extending the enum rather than rewriting flow blocks.
