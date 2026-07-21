# Pattern card — Air Defense System - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Simulate an aerial attack-and-defense scenario in which autonomous bomber and bomb agents pursue building targets while a defense system attempts to intercept them — modelling spatial movement, message passing, and cascading destruction across a 2D/3D environment.

## Block chain
There are no Process Modeling library blocks (Source/Sink/Queue/Service) in this model. Instead, three custom agent populations interact directly:

- **Bombers** — spawned dynamically via `add_bombers()` triggered by a cyclic `startMission` event (fires every `uniform(5, 12)` seconds). Each bomber holds a `target` reference to a Building and executes a statechart: entry action calls `moveTo(target.x, target.y, altitude)` → on arrival transition fires → bomber spawns a Bomb agent aimed at the same building.
- **Bombs** — each carries its own statechart: entry calls `moveTo(target.x, target.y, target.z)` → on arrival, delivers the message `"You are destroyed"` to the target Building and then exits.
- **Buildings** — passive agents that maintain a boolean `destroyed` flag; when they receive the destruction message their state flips and a fire animation becomes visible. Destroyed buildings are skipped by the mission-assignment loop, preventing double-targeting.

The top-level `Main` agent hosts all three populations and runs the cyclic event that scans unassigned, living buildings and dispatches a bomber to each.

## Resources
No ResourcePool blocks are used. Capacity is implicitly bounded by the building count (finite target set). Agent populations grow dynamically:
- Bombers: one created per unassigned living building each mission cycle
- Bombs: one created per bomber on target arrival
- Buildings: fixed count, placed in the environment at model start

Agent links (bidirectional `COLLECTION_OF_LINKS`) connect Main to Bombers, Bombers to Buildings, and Bombs to Buildings so agents can cross-reference each other by object reference.

## Key settings worth copying
- **Time unit:** Second (environment scale: 100 m per 100 px)
- **Mission interval:** cyclic event with `uniform(5, 12)` second recurrence — introduces stochastic spacing between bomber waves
- **Agent speed:** default 10 m/s for all mobile agents (overridable per agent type)
- **Spatial movement:** `moveTo(x, y, z)` in statechart entry actions drives continuous 3D navigation; arrival triggers the next statechart transition automatically
- **Message passing:** `deliver("You are destroyed", target)` is the sole inter-agent communication mechanism — lightweight, event-driven, no shared queues needed
- **Target assignment guard:** the mission loop checks both `bomber.target == bldg` (already assigned) and `bldg.destroyed` (already hit) before spawning a new bomber — prevents duplicate work
- **3D visuals:** `.dae` mesh files (house, bomber, bomb, fire) attached to each agent type; fire mesh visibility gated on `destroyed` flag

## KPIs instrumented
- Dataset auto-created every 1 second (recurrence = 1 s) for time-series logging
- Implicit KPIs observable at runtime: number of surviving buildings, active bomber count, active bomb count
- No explicit utilisation or wait-time statistics (this is a combat scenario, not a throughput model); the primary outcome metric is building survival rate over simulation time

## Reusable idea
**Statechart-driven spatial pursuit with a target reference.** Give each attacker agent a direct object reference to its target, encode the pursuit-and-action sequence as a two-state statechart (Flying -> Arrived -> [spawn payload / deliver message]), and let AnyLogic's continuous-time movement engine handle the path. This pattern cleanly separates targeting logic (in the parent environment's event loop) from movement and payload logic (in each agent's own statechart), making it straightforward to extend — e.g., adding an interceptor agent type that uses the same `moveTo + deliver` skeleton to shoot down bombers before they release their bombs.
