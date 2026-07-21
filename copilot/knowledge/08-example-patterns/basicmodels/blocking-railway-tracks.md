# Pattern card — Blocking Railway Tracks
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Demonstrates how a train navigates a multi-track rail network when one or more tracks are dynamically blocked, choosing between rerouting or waiting at a switch.

## Block chain
A single train agent is injected once at startup via `trainSource.inject()`. The train travels through a network of rail segments connected by ALL_TO_ALL railroad switches. The user can toggle two named tracks (`track1`, `track2`) between blocked and unblocked states at runtime using on-screen buttons. When a track is blocked *before* the journey begins, the routing engine automatically builds a bypass path avoiding that segment. When a track is blocked *mid-journey* (while the train is already moving), the model branches on a `BlockedTrackHandling` parameter: either stop the train at the last safe switch and wait for the track to clear, or immediately recalculate the shortest available route to the destination. The train carries passenger-car and locomotive 3-D assets and moves with configurable cruise speed, acceleration, and deceleration. On arrival (`TrainDispose`), the train is destroyed and a new one is immediately re-injected, creating a continuous loop for interactive experimentation.

## Resources
- One train agent composed of a locomotive + passenger car 3-D models
- Two toggleable track segments (`track1`, `track2`)
- Multiple ALL_TO_ALL railroad switches (`railwaySwitch`, `railwaySwitch1` … `railwaySwitch6`)
- A `TrainMoveTo` block driving movement with a `BlockedTrackHandling` policy

## Key settings worth copying
- **Time unit:** Seconds
- **Speed units:** KPH for train parameters; MPS used internally
- **Train parameters:** `initialSpeed`, `cruiseSpeed`, `acceleration`, `deceleration` (all tunable)
- **BlockedTrackHandling enum:** `STOP_AT_SWITCH` (wait at switch until clear) vs `RECALCULATE_ROUTE` (dynamic reroute)
- **Switch type:** `ALL_TO_ALL` — every incoming track can connect to every outgoing track
- **Routing:** shortest-path, recalculated on demand when blocking state changes
- **Restart loop:** `trainSource.inject()` called in `TrainDispose` exit action

## KPIs instrumented
- Visual track-blocked indicators (highlighted overlays when `track1.isBlocked()` / `track2.isBlocked()` are true)
- n/a (no formal throughput or wait-time statistics collected; model is interactive/demonstrative)

## Reusable idea
The transferable trick is the **two-phase blocking response pattern**: separate the case where an obstacle is known *before* the agent starts (build a clean route around it) from the case where the obstacle appears *during* travel (choose either a graceful wait at the last safe decision point or a live reroute). Encoding this as a single switchable enum parameter (`BlockedTrackHandling`) makes it trivial to let end-users or a policy layer switch strategies without restructuring the model — a pattern applicable to any network-routing simulation (AGVs, road traffic, pipeline flow).
