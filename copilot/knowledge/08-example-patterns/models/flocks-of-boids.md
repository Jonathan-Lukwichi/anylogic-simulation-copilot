# Pattern card — Flocks of Boids
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Show how realistic collective motion — flocking, faction attack, and retreat — emerges from each agent independently applying three simple local steering rules, with no central coordinator.

## Block chain
Each Boid agent owns a heading, speed, and faction colour (four colours represent rival groups). The main clock drives a single cyclic event every second that iterates the whole `boids` collection and calls `step()` on every agent in sequence.

Inside `step()` each Boid first calls `senseFlock()`, which loops through all agents in the population to find the nearest neighbour and records that neighbour's position and heading. Using that information the agent computes a heading correction from three layered rules applied in priority order:

1. Separation — steer away if a neighbour is closer than a personal-space threshold, to prevent crowding.
2. Alignment — rotate own heading a small increment toward the neighbour's heading to match local direction.
3. Cohesion — drift gently toward the spatial midpoint of perceived flockmates to maintain group compactness.

A fourth override layer handles faction rivalry: when the sensed nearest neighbour belongs to a different colour group and is ahead of the current Boid (dot-product of displacement vs. heading is positive), the Boid accelerates to chase; when that rival is behind, it retreats. A wall-avoidance rule fires whenever a Boid nears a canvas boundary and steers it back inward before the normal steering logic runs. If a Boid somehow leaves the arena anyway, a boundary handler removes it from the population. New Boids can arrive at runtime via a separate injection event timed by an exponential interval; up to four colour groups are injected from different edges, each with a heading biased toward the opposite side plus a narrow random spread.

Agent-to-agent links are modelled as a bidirectional collection overlay (95 % neighbour-link fraction, ~2 connections per agent) used purely for visual display of the network; the steering logic reads directly from the global boids list, not from the link topology.

## Resources
- Agent population: `boids` collection on Main, type `Boid`; size grows dynamically at runtime up to a hard cap of 4 000
- Four faction colour groups — colour is a per-Boid parameter, not a separate resource pool
- Bounded 2-D continuous arena; no GIS layer or grid

## Key settings worth copying
- Initial heading: `uniform() * 2 * Math.PI` — fully random orientation at first spawn
- Initial speed: `uniform(minimumSpeed, maximumSpeed)` — band-limited to keep motion visually coherent
- Injection heading: `meanHeading + uniform(-Math.PI/8, Math.PI/8)` — directed reinforcements with a 22.5-degree spread
- Injection position: `uniform(minX, minX + w)` / `uniform(minY, minY + h)` — random placement within an edge-aligned rectangle
- Injection inter-arrival: `exponential(0.01)` seconds — Poisson-rate arrivals of new agents
- Population ceiling: 4 000 agents; injection event skips if `boids.size() >= 4000`
- Time unit: Second; master step event period = 1 s

## KPIs instrumented
- No numeric KPI widgets — the primary output is the animated emergence of flocking and battle patterns
- Population size (`boids.size()`) is evaluated at each injection event as an operational guard

## Reusable idea
Drive all agent behaviour from a single top-level cyclic event that calls a `step()` method on each agent rather than giving every agent its own independent scheduler. This batch-step pattern keeps thousands of agents in sync at near-zero scheduling overhead, and the three-rule steering architecture (separation / alignment / cohesion as a base layer, state-based override on top) transfers directly to any ABM requiring emergent crowd, swarm, or competitive-group dynamics.
