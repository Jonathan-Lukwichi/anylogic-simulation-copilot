# Pattern card — Robot for Golem Manufacturing
- **Source:** AnyLogic example model "Robot for Golem Manufacturing" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (PML flowchart + a hand-built robot agent driven by statecharts)
- **Problem it solves:** One handling robot moves every part through three timed tanks in a fixed order; a late pick-up over-processes the part, so robot congestion turns directly into scrap.

## Block chain
`Source` (0.07 per s) → `Conveyor` (in-feed) → `RestrictedAreaStart ras1` (cap 1) → custom `UseRobot toTank1` → `Delay inTank1` (On enter: `send("In tank 1", agent)`) → `Queue queue1` (cap 1, the part sits in the tank) → `RestrictedAreaStart ras2` → `UseRobot toTank2` → `RestrictedAreaEnd rae1` → `SelectOutput` (`!agent.inState(agent.Overcooked)`) → tank 2 … tank 3 → `UseRobot toOut` → pedestrian exit (the finished part walks away: `PedEnter` → `PedWait` → `PedGoTo` → `PedSink`).
Scrap branch: `SelectOutput` false → `RestrictedAreaEnd` of the tank it had already claimed (`rae2defect`, `rae3defect`) → `Queue defects` (timeout 1 h) → `Sink`.

**Custom block `UseRobot`** (generic, `T extends Agent`): `Queue waiting` (cap 1; On enter files `robot.request(agent, priority(agent), entityHeight(agent), lift(agent), this)`) → `Hold holdPickUp` (initially blocked) → `Queue moving` (cap 1; On enter runs the block's `onPickUp` action) → `Hold holdMove` (initially blocked). Both Holds call `self.setBlocked(true)` in their On enter. The robot calls back `pickedUp()` → `holdPickUp.setBlocked(false)` and `moved()` → `holdMove.setBlocked(false)`.

**Robot agent:** a request list kept in priority order (inserted with a `ListIterator`), then `Operation.onChange()` wakes the operation statechart, which waits on the condition `!requestQueue.isEmpty()`. Three orthogonal statecharts (rotation, vertical, arm extension) each take "GO"/"CANCEL" messages and a timeout of distance ÷ axis speed. The operation advances when all three report "FINISHED". The drop point is computed when the move to it starts, not when the request was filed.

**Part (`Golem`) statechart:** Raw → InTank1 → Moving12 → InTank2 → Moving23 → InTank3 → Finished, driven by the flowchart's "In tank N" / "Out of Tank N" messages (the "Out" one is sent from `onPickUp`). Each InTankN also has a timeout of `timeInTankN * maxOverCookedPercent` to `Overcooked`. The clock therefore runs from tank entry until the robot lifts the part.

## Resources
One robot, a custom agent rather than a `ResourcePool`. Three tanks are three restricted areas of capacity 1. Defaults: tank times 6 / 7.5 / 8 s; a part overcooks at 1.5× its tank time.

## Key settings worth copying
- **Hand-over-hand claiming.** Claim tank n+1 (`ras(n+1)`) *before* the pick-up from tank n, and release tank n (`rae(n)`) after it. Every tank then holds at most one part, and a part that cannot move on keeps cooking, which is the real cost of congestion.
- **Late-bound target.** `targetLocation = entity.inState(entity.Overcooked) ? pointDefect : pointInTank2`, read at move start. A part that overcooked while waiting goes to the scrap box.
- **One-shot gate.** A Hold that re-blocks itself in On enter, behind a capacity-1 Queue, releases exactly one agent per external `setBlocked(false)`.
- **Carry by re-parenting.** At pick-up, `a.setSpace(placeholder)` and `jumpTo` the hand point, so the part follows the arm's animation. At drop-off, `a.setSpace(target.getSpace())` and `jumpTo(target)`.
- **Outputs.** `golemsCreated = pedSink.in.count()` and `golemsWithDefects = defects.in.count()`.

## KPIs instrumented
Good and scrapped counts (the two Outputs), so scrap rate = defects ÷ (good + defects). Robot request-queue length is shown through `toString()`.

## Pitfalls
- **`setSpace()` (Help 8.9.10) keeps the old coordinates and must not be called on a moving agent.** Always `jumpTo` a point of the new space right after.
- **Bind the target at move start, not at request time.** Otherwise parts that spoil while waiting for the robot still go on to the next tank.
- **Deadlock.** Claiming the next area while holding the current one is deadlock-free here only because the tanks form a strict line. With loops, shared tanks or two-way traffic, check it for deadlock *(general reasoning)*.
- **Built-in alternative.** AnyLogic 8.9 has a Robot markup element with `ProcessByRobot` / `SeizeRobot` blocks (used by `models/solar-panel-production-line.md`). Build a custom device agent only when you need its own kinematics or one priority queue shared by unrelated blocks.
- **Animation.** Colour-by-progress uses `lerpColor` on a timeout's `getRest()`, as in `bigbook/animation-dynamic-properties-and-frame-cost.md`.

## Reusable idea
Put an agent-controlled device into a flowchart as a custom block. The block files a request with the device, then parks the entity at one-shot Hold gates that the device's callbacks open at pick-up and at drop-off. Between capacity-1 stations, add hand-over-hand restricted areas. Give each part a statechart timer per station, so time spent waiting becomes quality loss.

## When the co-pilot should use this
- **Timed-bath lines:** plating or dip lines, heat treatment, curing, and wet benches with a maximum time in the bath, served by one hoist or robot.
- **Custom devices:** a statechart-driven crane, shuttle or robot that must serve PML entities.
- **Related cards:**
  - `bigbook/statechart-message-queue-and-safe-handoff.md` (message protocols)
  - gotcha G56 (`onChange()`)
