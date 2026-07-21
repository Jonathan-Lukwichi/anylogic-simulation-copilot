# Pattern card — Level Gate
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Routing a transporter agent seamlessly across multiple floors or spaces within the same agent using a single MoveByTransporter block.

## Block chain
Source → MoveByTransporter → Convey → Sink

Agents are generated at a Source on one level (bottomLevel). A MoveByTransporter block handles the full cross-level trip: it seizes a transporter from a TransporterFleet, the transporter navigates through paired LevelGate markup elements to cross from one floor to another (bottomLevel ↔ upperLevel, and further through a gate into a separate DestinationSpace agent), delivers the agent, and releases. A Convey block moves the agent along a conveyor path inside the destination space before it reaches the Sink.

## Resources
- **TransporterFleet** — one or more Transporter units (forklift 3-D model) defined within the fleet; transporters travel through level gates automatically when a cross-level route is planned.

## Key settings worth copying
- **Paired LevelGate references:** each LevelGate carries a `pairedGateCode` pointing to its counterpart on the adjacent level (e.g., `levelGate_bottomLevel` ↔ `levelGate_upperLevel`; `levelGate_toDestination` ↔ `destinationSpace.levelGate_atDestination`). Both must be consistent or routing fails.
- **MoveByTransporter destination level fields:** `destinationLevel`, `seizeDestinationLevel`, `canceledDestinationLevel`, and `releaseDestinationLevel` are set individually so the block knows which physical level each phase of the trip targets.
- **Source arrival rate:** configured via a `rate` / `rateSchedule` / `rateExpression` parameter (model time unit = Second).
- **Level visibility:** bottomLevel set to ALWAYS_SHOW; upper and destination levels set to DIM_NON_CURRENT — useful visual convention for multi-floor layouts.

## KPIs instrumented
n/a (demo model; no explicit KPI charts — focus is on routing correctness, not throughput statistics)

## Reusable idea
A single MoveByTransporter block can span multiple floors and even separate sub-agent spaces when LevelGate pairs are correctly linked. There is no need for chained Move blocks per level; the library resolves the full multi-segment route internally, making multi-storey warehouse or building layouts straightforward to model.
