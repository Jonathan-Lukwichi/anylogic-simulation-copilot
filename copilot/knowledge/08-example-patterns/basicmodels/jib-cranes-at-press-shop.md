# Pattern card — Jib Cranes at Press Shop
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates coordinated crane-conveyor-AGV material handling in a stamping/press shop where two jib cranes, a conveyor line, and autonomous guided vehicles must hand off parts without collision or starvation.

## Block chain
Two separate entry streams feed the system:

1. **Sheet feed line** — Source (metal sheets arrive at uniform(0.7, 1.3) inter-arrival rate) → MoveByCrane (crane 1 lifts sheet onto conveyor) → Convey (sheets travel down the press conveyor) → Hold (wait until a press machine slot is free) → MoveByCrane (crane 2 picks finished car-body part from press) → Convey (exit conveyor) → MoveByCrane (crane 2 stacks part onto AGV trolley) → Sink.

2. **AGV trolley stream** — Source (trolleys arrive periodically) → MoveByTransporter (AGV drives to conveyor end) → Pickup (crane loads parts onto trolley one by one) → MoveByTransporter (full trolley departs to assembly shop) → Sink.

Hold blocks gate flow at each press machine, releasing only when the crane is ready and a trolley slot is available. Pickup blocks accumulate parts on a trolley until the trolley capacity is reached, then release the AGV.

## Resources
- **Crane 1** — CraneFleet / Crane markup element, serves the infeed conveyor
- **Crane 2** — second independent CraneFleet, serves the outfeed stacking station
- **AGV fleet** — TransporterFleet with AGV agents pulling Trolley agents; each trolley has a fixed part capacity
- **Conveyor** — Convey blocks model two physical conveyor segments (infeed and outfeed)

## Key settings worth copying
- Inter-arrival rate on the sheet Source uses `uniform(0.7, 1.3)` — adds natural variability without heavy distribution fitting
- Model time unit is **Second**, appropriate for short-cycle material handling
- Trolley capacity drives the Pickup accumulation threshold; changing this one parameter stress-tests crane utilisation vs. AGV cycle time
- Hold blocks are used as synchronisation gates rather than queues — a clean way to model resource-gated press machines without a separate Seize/Release pair
- Two independent MoveByCrane sequences share the same physical space, making crane interference the key bottleneck to observe

## KPIs instrumented
- Crane utilisation (fraction of time each crane is moving vs. idle)
- AGV/trolley cycle time (pickup-to-drop-off round trip)
- Conveyor throughput (parts per hour exiting the press section)
- Hold queue length at each press machine (proxy for press starvation or overload)
- Trolley fill latency (time to accumulate a full load)

## Reusable idea
Use a **Pickup block as a batch-accumulator gate**: instead of batching parts into a single entity and then splitting them, keep parts as individuals and let the Pickup block hold the transporter in place until the required count arrives. This preserves per-part identity for downstream tracking while naturally synchronising crane stacking with AGV departure — no custom Java logic needed.
