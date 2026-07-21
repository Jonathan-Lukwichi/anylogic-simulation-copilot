# Pattern card — Fun City Driving
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Teaches kids (and beginners) basic programming concepts by letting them write a short command sequence that drives a car agent through a procedurally generated city without hitting buildings or borders.

## Block chain
A single `Car` agent moves through a 2-D continuous space (500 × 500 units) representing a city grid. At startup, `createNewLayout()` randomly scatters rectangular buildings using `uniform_discr` for position and size, and `uniform` for height and color. `prepareNewGame()` places the car at its start and marks a target location (blue circle) on the right half of the field. The player writes a program — at most 30 commands chosen from LEFT, RIGHT, FORWARD, SPEEDUP, and SLOWDOWN — which a built-in interpreter executes one command at a time, pausing at least 1 second between steps. After the last command the interpreter loops back to command 1. A `crashed()` check fires on every step; if the car intersects a building polygon or crosses the field border, the run ends. Completing more layouts increases building count, raising difficulty. A 3-D camera attached to the car gives a first-person view via `window3d1.setCamera(car.camera, true)`.

## Resources
- One `Car` agent (the player vehicle); no resource pools or service queues.
- Building obstacles: count grows with each successive layout level.

## Key settings worth copying
- Space: `CONTINUOUS`, 500 × 500, time unit `Minute`.
- Car default velocity: 10 m/s (overridden by SPEEDUP / SLOWDOWN commands).
- Building placement: `uniform_discr(1,7)` for width/height cells; position constrained so buildings stay inside the field and clear of the start zone.
- Building Z-height: `uniform(20, 50)` units — visible in 3-D view.
- Building color: `lerpColor(uniform(), brown, saddleBrown)` — randomised earth tones.
- Target x: `uniform(field.getWidth()/2, field.getWidth()-30)` — always in the right half.
- Command loop cap: 30 instructions; interpreter loops on overflow.
- Minimum step pause: 1 second of simulation time per command.

## KPIs instrumented
- Game outcome: success (reached target) vs. crash (building/border collision).
- Layout level (difficulty proxy): increments on each successful run.
- n/a: no throughput, utilisation, or wait-time metrics — this is a teaching/game model.

## Reusable idea
Embed a tiny interpreted command language inside a simulation: store the player's program as an ordered list, drive a `scheduleTimeout`/step loop that pops one command per tick, and call `crashed()` as a collision guard. This pattern cleanly separates the "engine" (AnyLogic time-stepping) from the "language" (user-defined command list), making it easy to extend with new commands or swap the car for any other moving agent.
