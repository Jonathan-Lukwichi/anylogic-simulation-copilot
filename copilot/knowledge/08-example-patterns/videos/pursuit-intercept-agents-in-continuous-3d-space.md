# Pattern card — Pursuit and interception in continuous 3D space: spawn at the launcher, re-aim loop, flight corridors, a hit that survives self-destruction
- **Source:** AnyLogic 8.9.10 Help tutorial "Air Defense System (Agents)" — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Model movers that launch from another agent, chase a moving target, fly scripted 3D legs and destroy themselves on impact, without lost hits, frozen events or distance thresholds that break when the scale changes.

## Mechanism
Checked against the 8.9.10 example *Air Defense System - Phase 4*. Main is a continuous 3D space at 100 px = 100 m (1 px = 1 m), time in seconds. Speeds are set on the populations: bombers 600 km/h, bombs 400 km/h, missiles 900 km/h. Two radars are single agents of one `Radar` type, each with `range` 200.
1. **Children are peers, not nested.** Bombs and missiles are populations of Main, in the same space as bombers and buildings. They are created with the generated adders, whose arguments follow the parameter order: `main.add_bombs(target, this)`, `main.add_missiles(this, b)`. Agents that measure distances to one another, or message one another, should share one space (G22).
2. **Spawn at the launcher before the first move.** The statechart entry point's *Action* is `setXYZ(radar.getX(), radar.getY(), radar.getZ())`. It runs as control passes the entry point, before the first state's entry action calls `moveTo(...)`, so the trip starts at the launcher and not at the population's default spot.
3. **Re-aim loop.**
   - State `Flying` has the entry action `moveTo(target.getX(), target.getY(), target.getZ())`.
   - `moveTo` aims at a point frozen at call time, so on its own the missile flies to where the target *was*.
   - An outside self-loop `Adjust` (Timeout 0.05 s) re-enters `Flying` 20 times a second, re-aiming at the target's current position. The result is a curved pursuit path. Re-entry semantics: `bigbook/statechart-guards-branches-and-state-reentry.md`.
4. **The loop is also the sensor clock.**
   - `AtTarget` (Condition `distanceTo(target) < 10`) and `OutOfRange` (Condition `distanceTo(radar) > radar.range`) are re-tested at every re-entry. Movement alone would not wake them (Big Book ch. 8 p. 11).
   - Both lead to the final state `Exploded`, which runs `radar.guidedmissiles.remove(this); main.remove_missiles(this);`, so a radar slot is freed on a hit and on a miss.
   - The radar scans on Main's synchronous steps (*Enable synchronous steps*, 1 s) in its *On step*. For each bomber within `range` that no missile already targets, it launches one, as long as `guidedmissiles.size() < 2`.
5. **A hit message that survives self-destruction.**
   - `AtTarget`'s action is `target.statechart.receiveMessage("You are destroyed")`.
   - Why not `send()`: it delivers in a later zero-time event, and the tutorial states that the delivery is cancelled if the sender has been removed by then, which the missile's final state does. `receiveMessage` acts at once.
   - The bomber catches the message on the border of a composite state drawn around its whole statechart, so the kill works from any state. The target of that transition is a final state that removes the bomber.
6. **Scripted 3D corridor.**
   - The bomber escapes with `moveTo(main.exitNode)` from free flight. `escapeRoute` is a hidden Path in Main with per-point Z (base Z 100; `exitNode` at Z 340). The `main.` prefix is needed because the markup lives in Main.
   - Help rule (*Agents movement inside and outside network*): an agent that starts off the network first moves straight to the closest point of the path, then follows the path to the node. A hidden path with per-point Z therefore works as a flight corridor.
7. **Stop when the job is done.** The bomb's hit action is `target.destroyed = true;`. It then calls `traceln(...)` and `finishSimulation()` once `findFirst(main.buildings, b -> !b.destroyed) == null`.

## Resources
- A radar's engagement capacity is a collection (`guidedmissiles`, at most 2). It works as a counting resource without a ResourcePool.
- The missile population starts empty.

## Key settings worth copying
- **`moveTo(x, y, z)`: the third argument is Z** (altitude), not speed (Help, *Movement in continuous space*). Speed comes from the population's *Initial speed*. The tutorial's `moveTo(target.getX(), target.getY(), 80)` makes the bomber descend to 80 m on the way in.
- **Scale-proof thresholds.** Write `distanceTo(target, METER) < 10`. The plain overload returns model units, i.e. pixels: Help documents pixels for the in-range functions and offers `LengthUnits` overloads *(pixel unit for plain `distanceTo` inferred)*. The tutorial's 10 and 200 are metres only because it set 1 px = 1 m.
- **Animation rotation.** *Rotate animation towards movement* is on by default and turns the shape in the XY plane. For climbing or diving movers, also tick *Rotate vertically (incline on ramps)* (Help, *Agent animation rotation*); the example leaves it off.
- **Visibility.** *Additional scale* of 300–800 % keeps small shapes visible at 1 px = 1 m. It changes only the drawing.

## KPIs instrumented
The tutorial has none beyond its end condition. Add:
- intercept ratio (bombers killed / bombers launched);
- missiles fired per kill;
- misses (exits through `OutOfRange`);
- time from detection to kill;
- buildings intact over time.

## Pitfalls
- **`send()` from an agent that removes itself** is dropped silently (tutorial, Help 8.9.10).
  - Fixes: use `receiveMessage`, or set a field on the target and call `target.onChange()`.
  - Deferring the removal by a zero-time step is not safe: simultaneous events run LIFO by default (G60), so the removal can still come first *(reasoned, not run)*.
- **Re-aim period vs hit radius** *(arithmetic, not run)*. Between checks the gap shrinks by closing speed × period. Head-on at 900 + 600 km/h (about 417 m/s), a 0.05 s period closes about 21 m, more than the 10 m radius, so a missile can pass through the target and turn back. Keep radius ≥ closing speed × period. Each pursuer also adds 1/period events per second.
- **Chasing a removed target.** If the bomber leaves the model first (escape route done), the missile keeps its reference and flies to the last position until `OutOfRange` fires. Guard with `main.bombers.contains(target)` *(suggested)*.
- **Unbounded search loop in an event.** The mission event repeats `randomWhere(...)` inside `do … while (!chosen)` until it finds an intact building with no bomber.
  - If every intact building already has one, the loop never ends and the run freezes inside one event. This comes from reading the 8.9.10 example code: unlikely at the tutorial's speeds, likely if bombers are slowed.
  - Instead, pick once from the filtered set and skip on `null`: `randomWhere(buildings, b -> !b.destroyed && findFirst(bombers, m -> m.target == b) == null)`.
- **Polling vs analytic timing.** The tutorial itself notes that, for straight or piecewise-straight paths at constant speed, computing the intercept and crossing times analytically is more accurate and cheaper. Polling is simpler and works for any kind of movement.

## Reusable idea
For every mover, settle four things:
1. where it starts (set before its first move);
2. what it aims at (and the re-aim period);
3. what wakes its checks (a loop, steps or events);
4. how its last message leaves (synchronously, if the mover destroys itself).

## When the co-pilot should use this
- **Use cases:** interception and air defence; drones or police chasing a moving target; robots tracking a moving part; predator–prey in continuous space.
- **Scripted 3D legs:** approach, escape or climb corridors drawn as paths with per-point Z (compare `videos/spiral-conveyor-per-point-z.md`).
- **Symptoms:**
  - hits that never register;
  - a pursuer that flies to where the target used to be;
  - a run that freezes at a mission time;
  - thresholds that go wrong after a scale change.
- **Related:**
  - `basicmodels/air-defense-system-phase-1.md` … `-phase-4.md`: structure only. Corrections are proposed in `knowledge/.ingest/proposals/tutorials-1.md`.
  - `bigbook/statechart-message-queue-and-safe-handoff.md`
  - `bigbook/event-modes-condition-monitoring-and-lifecycle.md`
