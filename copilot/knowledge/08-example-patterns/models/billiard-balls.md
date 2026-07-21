# Pattern card — Billiard Balls
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Demonstrates continuous-space multi-agent physics — elastic collision between autonomous agents and rigid boundaries — as a foundation for any particle-based or crowd/vehicle interaction model.

## Block chain
A population of Ball agents is spawned inside a bounded 2-D rectangular arena. Each ball starts at a random position drawn with `uniform()` and launches in a random direction (`uniform(2*PI)`) at a fixed scalar speed V, decomposed into Cartesian velocity components `vx` and `vy`. A cyclic event (`bounceBall`) fires on a short time step; on each tick the ball checks whether it overlaps any other ball via a `checkHit()` scan over the full agent list in Main. When a hit is detected the two balls exchange velocity components according to elastic-collision equations (Newton's laws, equal masses). Border rebounding is handled separately by reversing the appropriate velocity component when the ball centre reaches within radius `r` of a wall. Gravity can be toggled on/off at run time, adding a constant downward acceleration term to `vy` each step. The model tracks each ball's kinetic energy (`ke = (vx²+vy²)/2`) and potential energy (`pe`), and aggregates them in a time-plot so the user can verify energy conservation (or watch it shift between KE and PE when gravity is on).

## Resources
- Agent population: N Ball agents (user-configurable slider)
- Continuous 2-D space (CONTINUOUS, user-defined layout)
- No service pools or queues — purely physics-driven movement

## Key settings worth copying
- Initial position: `uniform(r, Xmax-r)` for both axes — keeps balls inside bounds from t=0
- Initial heading: `uniform(2*PI)` radians — isotropic launch directions
- Speed unit: MPS (metres per second), set via `SpeedUnits`
- Time unit: Day (model clock), but physics step driven by the bounceBall event interval, not the calendar
- Spectrum colouring: each ball gets a unique hue via `spectrumColor(getIndex(), N)` — useful visual trick for distinguishing agents

## KPIs instrumented
- Per-agent kinetic energy: `ke = (vx² + vy²) / 2`
- Per-agent potential energy: `pe` (height-based when gravity active)
- Aggregate KE + PE time-plot across all balls (energy conservation check)

## Reusable idea
The transferable trick is the **per-step neighbour scan + elastic velocity swap**: iterate over the agent collection in a single function, detect proximity by comparing centre distances to `2r`, then swap velocity vectors. This pattern is directly reusable for any continuous-space collision scenario (pedestrian shoulder-contact avoidance, vehicle near-miss, molecular dynamics toy models) without needing AnyLogic's built-in pedestrian or vehicle libraries.
