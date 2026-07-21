# Pattern card — Crane System with Multiple Bridges
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Coordinating two overhead crane bridges that share the same runway to load containers onto AGVs without collision or deadlock.

## Block chain
Containers arrive at a Source and pass through a Delay (representing stacking/staging time). A SelectOutput block routes each container to one of two parallel handling sub-chains depending on the active dispatch strategy. Each sub-chain follows: SeizeTransporter (grab an AGV) → MoveByCrane (blue or red bridge picks up the container) → SeizeTransporter (confirm AGV ready at drop point) → MoveByTransporter (AGV carries load away) → MoveByCrane (bridge returns or repositions) → Sink. In the shared-queue variant a third sub-chain uses a single SeizeTransporter named `seizeNearestAGV`; a custom condition checks which bridge is geometrically closer to the waiting container and assigns it dynamically.

## Resources
- Two overhead crane bridges (blue bridge, red bridge) modelled as crane transporters on a shared overhead path network.
- A fleet of AGVs (`AGV` agent population) that serve as ground-level transporters receiving loaded containers from the crane and carrying them to destination nodes.
- Each bridge and AGV fleet has an independent capacity parameter; AGV speed is a configurable parameter.

## Key settings worth copying
- **Load-time distribution:** `triangular(0.5, 1, 1.5)` seconds — used consistently for every crane pick-and-place operation across all sub-chains.
- **Time unit:** Second.
- **Dispatch mode toggle (run-time parameter):** Switch before run-start between (a) shared single queue with nearest-bridge selection and (b) dedicated per-bridge queues; this is the primary experimental factor.
- **Nearest-bridge selection logic:** `container.distanceTo(blueLoadPoint.getX(), blueLoadPoint.getY())` vs. the red load point — pure Euclidean distance at the moment of seize, no look-ahead.
- **Conflict avoidance:** Handled automatically by AnyLogic's crane library (bridges cannot occupy overlapping runway segments simultaneously); no custom collision code is needed.

## KPIs instrumented
- Throughput: containers delivered to Sink per time unit.
- AGV utilisation: fraction of time each AGV is loaded/in-transit vs. idle.
- Bridge utilisation: active lift time vs. idle/travel time for each bridge.
- Container wait time: time spent in queue before a bridge is seized.

## Reusable idea
The transferable trick is the **two-mode dispatch toggle**: model both a centralised nearest-resource rule and a partitioned dedicated-resource rule inside the same model, separated by a SelectOutput conditioned on a pre-run parameter. This lets analysts compare throughput and utilisation under both policies in a single experiment without duplicating the model, and the distance-based nearest-resource selector (`agent.distanceTo(point)`) is a clean, copy-paste-ready pattern for any multi-crane, multi-AGV, or multi-server layout where spatial proximity is the tiebreaker.
