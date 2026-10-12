# Pattern card — Crane settings that change results: reach, safe height, component movement mode (overhead and jib/tower cranes)
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Configure overhead and tower (jib) cranes so lifts are feasible, clear obstacles, and take realistic time before you size the crane fleet.

## Block chain
- **Overhead crane loading an AGV (model 3):** `SeizeTransporter` → **`MoveByCrane`** (destination = the node where the seized AGV waits) → `MoveByTransporter`. See `videos/mhl-agv-dispatch-choice-and-cargo-position.md`.
- **Tower crane feeding a building roof (model 4):**
  1. `Source` with arrivals = *calls of inject()*. Main's On startup calls `source.inject(10)` to pre-stock the ground depot.
  2. `Queue`.
  3. **`MoveByCrane`**: jib crane, destination = a node on the roof level, **Safe height** 20 m.
  4. `MoveByTransporter`: free-space forklifts, node = `randomFrom(floorNodes)`.
  5. `Sink`.
- **Levels and logic.** Flowchart blocks, variables and collections are owned by the agent type, never by a level. So one collection can hold nodes from floors 1 and 2, and one MoveByTransporter serves both. Markup, shapes, controls, charts, and the 3D window/camera/lights belong to a level; the scale and view areas do not. At runtime, `level.setVisible(false)` hides a floor for custom navigation.

## Resources
One crane markup element per crane. MoveByCrane seizes and releases the crane itself (*Seize crane* / *Release crane*) unless you split out `SeizeCrane` / `ReleaseCrane`.

## Key settings worth copying
- **Reach is a hard constraint.** The webinar requires the load and its destination to lie within the crane's working area (the jib's circle, or the overhead runway). The highest point a load can reach equals the **Crane height**. The webinar gave a cat-head tower crane 25 m to serve a roof at about 12 m.
- **Safe height** (MoveByCrane; default 1 m; may depend on `agent` and `crane`): the minimum height a load is raised to before it travels. Set it above the tallest obstacle on the way.
- **Component movement mode:**
  - *Step-by-step*: one component moves at a time. This is the safe way real cranes run.
  - *Concurrent*: all components move at once. Much faster.
  - *Independent hoist* (overhead cranes only): bridge and trolley move together, and the hoist moves before or after them.
  - The mode changes cycle time, not just the animation.
- **Speeds are dynamic.**
  - Jib crane: trolley, rotation and hoist speeds.
  - Overhead crane: bridge, trolley and hoist speeds.
  - Each can use the local `isLoaded`, e.g. `isLoaded ? 0.3 : 0.8` (m/s).
- **Use operation time** (MoveByCrane): give a fixed time and AnyLogic rescales the speeds for each load. The time covers loading, the move and unloading only when the block itself seizes and releases the crane.
- **Jib crane:** Jib length, initial jib angle, Crane height, and type *Industrial jib / Cat-head tower / Flat-top tower*. An optional **Blocked zone** is set with `setBlockedZone(start, delta, DEGREE)`.
- **Overhead crane:**
  - *Gantry* vs *Bridge* drawing. Gantry rails stand on the floor and may visually sit on an AGV path.
  - *Number of bridges* for multi-bridge cranes (see `basicmodels/crane-system-with-multiple-bridges.md`).
  - Snap the crane onto a path, conveyor or railway track (it highlights green) to pick and drop there directly.

## KPIs instrumented
The webinar shows none. Suggested:
- `crane.getUtilization()`.
- Crane cycle time, from entering MoveByCrane to exiting it.
- The queue in front of MoveByCrane.
- `mtbf()` / `mttr()` once a Downtime block is attached — for jib cranes and, since 8.9.1, overhead cranes too (corrected 2026-10-01; gotcha G43). Seize a crane explicitly (`SeizeCrane` … `ReleaseCrane`) when it must **hold** the load while people work under the hook; its utilisation then includes the holding time (8.9.10 *SeizeCrane and ReleaseCrane* example).

## Pitfalls
- **Blocked zone:** if the jib's initial angle lies inside the zone when you enable it, the crane cannot move and the run fails (Help 8.9).
- **Load or destination outside the working area:** the move cannot happen; expect a runtime error *(unverified)*. Check the geometry first.
- **Concurrent vs Step-by-step** can swing throughput. Confirm which one the real site uses before optimising the crane count.
- **The default Safe height of 1 m** suits a flat floor, not lifts over walls or storeys.
- **Obstacles:** jib cranes and overhead-crane rails can block free-space transporters and pedestrians (`setObstacle(...)`).

## Reusable idea
Treat a crane as a geometric server:
1. feasibility first: reach, height and the blocked sector;
2. then timing: movement mode, and dynamic speeds or a fixed operation time;
3. only then fleet sizing.

## When the co-pilot should use this
- **Use cases:** press shops, container and steel yards, construction logistics, any MoveByCrane question.
- **Symptoms:** crane-served throughput looks implausibly high (check the movement mode), or the run errors at start (check the blocked zone and reach).
- **Related cards:**
  - `basicmodels/jib-cranes-at-press-shop.md`
  - `basicmodels/lead-acid-battery-production-phase-4.md`
  - `videos/multi-level-facility-lift-landings.md` (the floors, the lift)
