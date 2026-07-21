# Pattern card — Supply Chain Optimizer
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + ABM with Python-driven optimization)
- **Problem it solves:** Find minimum-cost factory-warehouse-customer allocation while simultaneously simulating day-by-day order fulfilment and vehicle logistics.

## Block chain
Three agent types operate in parallel populations — **Customer**, **Warehouse**, and **Factory** — each running its own DES process chain.

- **Factory flow:** Order arrives → `Seize` production slot → `Queue` (buffer until capacity frees) → `Delay` (production time, event-controlled to handle mid-run rate changes) → `MoveTo` (truck travel to warehouse or customer) → `Exit`.
- **Warehouse flow:** Inbound shipment → `Enter` → `Seize` dock resource → `Delay` (unloading: `triangular(0.5, 1, 1.5)` days) → stock held behind a `Hold` block → customer order triggers `Release` → outbound `MoveTo` → `Delay` (last-mile) → `Sink`.
- **Customer demand:** periodic orders with size drawn from `uniform_discr(15, 45)` units; accumulated demand is streamed to the optimizer each cycle.
- A **`PyCommunicator`** (Pypeline add-on) serialises the live simulation state to JSON, calls a Python solver (scipy / linear-programming), receives back the minimum-cost allocation map, and feeds routing decisions back into the agent network.
- A **NetworkGraph** object maintains the physical topology (nodes = facilities, edges = routes with cost weights).

## Resources
- **Vehicle ResourcePool** on Main — trucks shared across factory and warehouse shipment legs.
- Factory production capacity expressed as an adjustable **output rate** (units/day); the controlling event recalculates delay duration whenever the rate slider changes.
- Warehouse dock capacity: implicit through Seize/Release pairs per warehouse agent.

## Key settings worth copying
- Time unit: **Day**.
- Unloading delay: `triangular(0.5, 1, 1.5)` days — easy to swap in your own empirical triangular.
- Customer order size: `uniform_discr(15, 45)` — discrete uniform, good for integer-unit goods.
- Production delay uses an **event-recalculation pattern** rather than a fixed Delay value: on each rate change, remaining time is recomputed and the event is rescheduled. Copy this whenever throughput can shift mid-run.
- Python bridge pattern: serialise agent state → JSON → Python solver → parse result map back in Java/AnyLogic. Requires Pypeline add-on and Python 3 + requirements.txt.

## KPIs instrumented
- **Optimized cost** tracked in a history dataset (`optimizedCostsHD`) — one entry per optimization cycle.
- **Weekly net supply** (`weeklyNetSupplyHD`) = total factory output minus total customer demand that week.
- Implicitly: vehicle utilisation (ResourcePool statistics) and order wait time (Queue/Delay statistics).

## Reusable idea
The standout trick is the **co-simulation bridge**: the running DES/ABM simulation pauses, exports its current state as structured JSON to a Python optimization process, receives a cost-minimizing allocation decision, and then resumes with updated routing — coupling simulation fidelity with mathematical optimization without rebuilding the solver in Java. This pattern applies anywhere you need both stochastic realism and optimal decision-making in the same experiment.
