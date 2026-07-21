# Pattern card — Air Defense System - Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Simulates an aerial attack scenario where bombers drop bombs on city buildings while radar-guided interceptor missiles attempt to destroy incoming threats before they reach their targets.

## Block chain
Five custom agent types interact spatially on a continuous 2-D/3-D environment:

1. **Bomber** agents spawn at the boundary, select a random surviving Building as their target, and fly toward it at a fixed speed (10 m/s). Each Bomber carries a statechart with states for flying, releasing a bomb, and being shot down.
2. **Bomb** agents are released mid-flight by a Bomber, then descend toward the targeted Building. A statechart governs their fall; on arrival they send a "You are destroyed" message to the Building.
3. **Building** agents are static targets scattered across the environment. Each holds a boolean `destroyed` flag that flips to `true` upon receiving the destruction message; a 3-D fire model replaces the house model visually. The simulation ends when no undestroyed buildings remain.
4. **Radar** agents scan for incoming threats. When a Bomber or Bomb enters range, the Radar spawns a **Missile** and registers it in a guided-missile list (capped at two simultaneous intercepts per radar to reflect limited battery capacity).
5. **Missile** agents home in on their assigned target. Their statechart checks a proximity condition at each tick; on intercept they send the destruction message to the Bomber/Bomb and deregister from the Radar's list, then terminate.

There is no Source→Sink process chain; agent lifecycles are governed entirely by statechart transitions triggered by spatial proximity, timeouts, and message passing.

## Resources
- No formal ResourcePool blocks are used.
- Radar capacity is self-managed: each Radar agent maintains an internal list of active guided missiles and caps simultaneous launches at 2, acting as an implicit resource constraint.
- Bomber arrival is driven by a repeating event at a rate of **1 per minute** with an initial delay of 1 minute.

## Key settings worth copying
- **Time unit:** Second (fine-grained for spatial movement calculations).
- **Bomber arrival:** rate = 1/minute; first arrival delay = 1 minute.
- **Target selection:** `randomWhere(buildings, b -> b.destroyed == false)` — picks a live building uniformly at random, naturally shifting load as buildings are destroyed.
- **Bomb release delay:** `uniform(5, 12)` seconds after Bomber reaches drop position.
- **Missile guidance limit:** `guidedmissiles.size() >= 2` guard prevents over-committing a radar battery.
- **Environment:** 500 × 500 m continuous space; 100 × 100 grid backing; agent speed in m/s.
- **End condition:** checked after each building destruction — if `findFirst(buildings, b -> !b.destroyed) == null`, the simulation stops.
- **3-D assets:** .dae models (bomber, bomb, house, fire, patriot missile rocket) used for visual feedback — swap with 2-D shapes for lightweight runs.

## KPIs instrumented
- **Throughput** counter (named `throughput`) tracks events of interest (likely bomb hits or interceptions).
- **Building survival rate:** proportion of Building agents with `destroyed == false` at simulation end — the primary outcome metric.
- **Implicit intercept rate:** derivable from (bombers/bombs spawned) minus (buildings destroyed) — not surfaced as a dedicated widget but computable from agent counts.

## Reusable idea
**Capacity-capped agent-to-agent engagement:** the pattern of letting a resource agent (Radar) maintain its own active-task list and gate new assignments behind a size check (`size() >= N`) is a clean, reusable way to model limited-capacity responders (emergency vehicles, server threads, fire suppression units) without a formal ResourcePool — the engaging agent simply checks availability before committing, and deregisters itself on completion, keeping concurrency bounded with minimal infrastructure.
