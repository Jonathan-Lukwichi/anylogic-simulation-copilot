# Pattern card — Air Defense System - Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Simulates autonomous bomber agents attacking a set of defended buildings inside a protected zone, with each bomber guided by an internal statechart that drives spatial movement toward a target and then retreat.

## Block chain
Three custom agent types interact inside a continuous 2-D space (500 x 500 m, scale 1 px = 10 m):

- **Building agents** (population of 10) — passive targets positioned on a protected-area node; they represent structures the defense must protect.
- **Bomber agents** (dynamic population, initially empty) — spawned periodically by a cyclic timed event in Main; each bomber receives a reference to a randomly chosen Building as its `target` parameter.
  - Bomber statechart: `EntryPoint` → **ToTarget** state (entry action calls `moveTo(target.getX(), target.getY(), 80)` at 80 m/s) → on-arrival transition → **Away** state (entry action moves bomber to an exit node) → on-arrival transition → **FinalState** (exit action removes the bomber from the population via `main.remove_bombers(this)`).
- **Main** environment — owns both populations, the `startMission` cyclic event that calls `add_bombers(buildings.random())`, and bidirectional agent-link connections among all agents.

No Process Modeling Library (PML) blocks (Source/Sink/Queue/Service) are used; all logic is pure ABM via statecharts and spatial movement.

## Resources
- No ResourcePool blocks are present.
- Agent populations: `buildings` (fixed count = 10), `bombers` (dynamic, grows and shrinks at runtime as missions are launched and completed).
- Space: continuous 2-D environment; agents move at defined speeds in meters per second.

## Key settings worth copying
- **Mission arrival interval:** `uniform(5, 12)` seconds — stochastic inter-mission gap giving irregular attack waves.
- **Bomber cruise speed:** 80 m/s (set inside the statechart entry action as the third argument to `moveTo`).
- **Building population size:** 10, placed on a named node (`protectedArea`).
- **Time unit:** Second; scale ruler calibrated at 100 m per 100 px (1 px = 1 m internally, displayed at 10 m per px).
- **Cyclic event trigger:** mode = cyclic, period = every 1 minute base with recurrence overridden by `uniform(5,12)` seconds — a useful pattern for mixing a fixed cadence with stochastic jitter.
- **Target selection:** `buildings.random()` — uniform random pick from the live Building population at spawn time.
- **Agent removal:** called explicitly in the FinalState action (`main.remove_bombers(this)`) to keep the population collection consistent.

## KPIs instrumented
- Dataset auto-creation is enabled in Main with a 1-second collection interval, providing a time series of agent counts.
- No explicit chart widgets or statistics blocks are visible in the file; the primary observable is the animated 2-D/3-D scene showing live bomber positions, active missions, and building status.
- Derived metrics a modeler would add: number of buildings reached (hit count), average mission duration, concurrent bombers in flight at any time.

## Reusable idea
**Statechart-driven spatial missions with dynamic agent lifecycle** — the pattern of spawning an agent with a pre-assigned target reference, using a two-state statechart (move-to-target / move-to-exit) triggered by spatial-arrival events, and destroying the agent in the FinalState action is a clean, reusable template for any scenario involving autonomous units that execute a task and then self-terminate (delivery drones, emergency vehicles, adversarial agents, inspection robots). The `uniform(a, b)` recurrence on the cyclic event is the lightweight way to inject randomness into wave-based arrival patterns without a separate Source block.
