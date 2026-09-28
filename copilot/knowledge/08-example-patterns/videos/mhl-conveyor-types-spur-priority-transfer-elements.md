# Pattern card — Conveyor behaviour choices: accumulation type, spur merge priority, transfer elements and item orientation
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Choose conveyor type, merge rules and 90°/rotating transfer equipment so blocking, merging and item orientation behave like the real line.

## Mechanism
1. **Accumulation comes from the conveyor's Type** (`ConveyorType`).
   - *Roller* (`CONVEYOR_TYPE_ROLLER`, the default) accumulates. When one item is held, the items behind close up to it (spacing = **Gap**) while the items ahead carry on. With Gap = 0, collisions are unavoidable.
   - *Belt* (`CONVEYOR_TYPE_BELT`) does not accumulate. One held item stops the whole conveyor, so spacing is frozen.
   - *Fixed cell* (`CONVEYOR_TYPE_CELL`) does not accumulate either. It is a chain of cells of **Cell size**, one item per cell, and Gap is the space between cells.
   - **Test rig (webinar).** Put a Position on conveyor with **Initially blocked** near the end, send sparse arrivals, switch the Type, and watch what queues.
2. **A spur is a junction that does not cut the main conveyor.**
   - Ending one conveyor on another, at any angle, auto-creates a Conveyor spur. One spur takes one branch.
   - An item's heading relative to the belt is preserved.
   - Branch items wait for a safe gap and merge at the main line's maximum speed, so the main flow is never disturbed.
3. **Merge priority is set on the incoming conveyors** (the *Priorities* section), not on the spur, and applies per connection, not network-wide.
   - **Maximum priority** ticked: this conveyor always wins.
   - Otherwise, the **higher Priority value** wins when two branches join from left and right at about the same offset.
   - Equal values: first come, first served. A platoon of high-priority items at minimum gap keeps the right of way until it ends.
   - With a single branch, priorities change nothing; the main line dominates.
4. **Transfer elements split the conveyor into two independent conveyors.** They differ in what they do to orientation.
   - **Transfer table:** up to 4 conveyors at right angles. The item keeps its orientation **in space**, so after a 90° transfer it travels sideways. Make the outgoing conveyor at least as wide as the item is long.
   - **Turntable:** any number of conveyors at any angle. The item turns with the table and keeps its orientation **on the conveyor**.
   - **Turn station:** sits between two collinear conveyors and rotates items in multiples of 90°, in mode *Angle* or *Orientation*. The webinar uses a full 360° turn as a timed "final inspection".

## Resources
n/a

## Key settings worth copying
- **Conveyor properties:** Type, Gap, Cell size, Maximum speed and Initial speed, Acceleration/Deceleration, Reversible, Maximum priority / Priority. If both speeds are 0, the belt never starts until you call `setMaxSpeed(v, MPS)`.
- **Item orientation:**
  - Inside the item type, length runs along X and width along Y, and the **front faces +X**. Items enter the first conveyor front-first.
  - To change it, use *Change orientation* + Orientation on `ConveyorEnter`/`Convey` (`AGENT_ORIENTATION_FRONT/REAR/LEFT/RIGHT`). On `Convey` this is only offered when Convey from = Current position.
  - Or call `agent.setOrientationOnConveyor(...)`; read it back with `getOrientationOnConveyor()`.
- **Runtime:** `conveyor.setType(...)`, `isAccumulating()`, `setMaximumPriority(true)`, `transferTable.setSwitchingDelay(t, SECOND)`, and `setRotationSpeed(...)` on turntables and turn stations. All three transfer elements also have `fail()` / `repair()`.

## KPIs instrumented
The webinar shows none. Suggested:
- Waiting time of branch items before each spur.
- Throughput per entrance.
- `conveyor.getUtilization()` before and after a change of Type.

## Pitfalls
- **KB conflict:** `basicmodels/conveyor-singulator.md` puts merge priority on the ConveyorSpur and says *lower* values win. Help 8.9 (Conveyor spur; Conveyor → Priorities) says the opposite on both counts. See the w2-material-handling-webinar proposals.
- **Narrow outgoing conveyor after a transfer table:** sideways items overhang it. Widen the conveyor.
- **Turntable misbehaving after edits:** disconnect and reconnect its conveyors so it recomputes its internal orientations (a webinar tip).
- **Material item type must not change** at stations, turntables or turn stations; the conveyor expects the same type downstream (Help 8.9).

## Reusable idea
Model the equipment, not the effect:
- pick Roller, Belt or Cell to match the real hardware;
- express merge rules as conveyor priorities;
- use the transfer element whose orientation rule matches the machine.

Blocking, singulation and item turning then emerge without custom code.

## When the co-pilot should use this
- **Use cases:** sortation, induction/merge lines (singulators), 90° diverts, and accumulation buffers (roller zones vs indexed belts or cell conveyors).
- **Symptoms:** items "turn sideways" or overlap, or a merge "never lets the branch in".
- **Related cards:**
  - `videos/mhl-convey-routing-offsets-leave-on-exit.md`
  - `basicmodels/conveyor-singulator.md`
  - `basicmodels/item-flow-control-on-a-reversible-conveyor-spur.md`
