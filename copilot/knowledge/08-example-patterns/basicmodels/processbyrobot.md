# Pattern card — ProcessByRobot
- **Source:** AnyLogic example model "ProcessByRobot" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** A two-robot cell: a pick-up robot moves parts between conveyors and a workbench, a multifunctional robot welds the part in place (tool change) and places a cover on it — pick-and-place and in-place processing with one block type.

## Block chain
- **Part:** `Source` (`triangular(3, 5, 4)` min; *On exit* injects one cover) → `Convey` → `RestrictedAreaStart` (cell capacity 1) → `ProcessByRobot` *toMachine* (pick-up robot carries the part to the workbench node; nearest-side approach; 50 s; afterwards moves its end effector to a parking node, post-process 10 s) → `ProcessByRobot` *weldRight* (multifunctional robot, **changes end effector to the welding gun**, **Pick up agent = false**, moves along a seam from start XYZ to end XYZ given relative to the part, top approach, 30 s) → *weldLeft* (other seam, then returns to initial position) → `Combine` (part = entity 1; *On enter 1* un-blocks the cover gate) → `ProcessByRobot` *toConveyor* (pick-up robot places the assembly on the out-conveyor, 50 s, post-process 15 s) → `RestrictedAreaEnd` → `Convey` → `Sink`.
- **Cover:** `Source` (manual) → `Queue` → `Hold` (initially blocked, blocks itself after one) → `ProcessByRobot` (multifunctional robot with a new end effector carries the cover to 10 units above the workbench, top approach, returns to initial position, post-process 5 s) → `Combine` in2.

## Resources
Two Robot markup elements: `pickupRobot`, `multifunctionalRobot` (safe height 1 m on the carrying moves).

## Key settings worth copying
- **Pick up agent** (`pickupAgent`): true = transport; false = the robot works on the agent where it is (welding, gluing, inspection, screwing).
- **Operation time** includes the arm reaching the agent *and* the processing/transport (Help) — robot timing is an input, not computed from kinematics.
- **Change end effector** + *End effector*: `ROBOT_END_EFFECTOR_GRIPPER`, `…_VACUUM_GRIPPER`, `…_WELDING_GUN`, `…_NONE` — one robot, several tools.
- *Movement type* (Help 8.9.10): **point to point** — from the start location to *Processing ends at* (node, attractor, conveyor, position on conveyor, (x, y, z) or agent); the demo's seams are start/end XYZ computed from the part (`agent.getX() ± …`). **Path controlled** — the end effector follows a Path, which can be drawn inside the agent type and referenced as `agent.path` (the agent's vertical rotation is not applied to it) — the natural way to model a weld or glue bead.
- *End effector approaches*: `ROBOT_APPROACH_TOP_SIDE` or `…_NEAREST_SIDE`; *Safe height* for travel.
- *After operation robot* (only with *Release robot*): `AFTER_OPERATION_STAY`, `…_MOVE_TO_INITIAL_POSITION`, `…_MOVE_TO_TARGET`; *Post-process time* is the time for that move, applied only when no other agent is waiting.
- Cell guard: `RestrictedAreaStart/End` capacity 1 around the robot operations; a self-blocking `Hold` releases exactly one cover per part.

## KPIs instrumented
Visual only (3D).

## Pitfalls
- Because *Operation time* already includes the approach, adding separate delays for "robot movement" double-counts time.
- *Post-process time* is skipped when another agent is queued — robot return moves then cost nothing; do not read it as a fixed cycle element.
- Without the restricted area, a second part could be picked onto an occupied workbench (same deadlock logic as crane cells — see `movebycrane.md`).

## Reusable idea
Use ProcessByRobot twice over: as a mover (pick up agent) and as a processor (no pick-up, tool changed); build robot cells as a restricted-area-guarded chain of these blocks, with a Hold/Combine pair to synchronise secondary parts.

## When the co-pilot should use this
Robotic welding/assembly cells, machine tending, pick-and-place between conveyors; questions about robot cycle time settings, tool changes or robots returning home. For explicit seize/release of robots see `seizerobot-and-releaserobot` (batch m-basic-3); a larger robot application is `models/solar-panel-production-line.md`.

## Additions (8.9.10 review, 2026-10-01)
- The tool can be switched from code in any block action — `robot3.setEndEffector(ROBOT_END_EFFECTOR_VACUUM_GRIPPER)` — to change tools mid-sequence; the robot's rest pose `robot.getInitialEndEffectorX()/Y()/Z()` is a convenient path start; *After operation* → move to a "pause" node keeps the arm clear between passes (8.9.10 *Robot Move Along Path*).
- 8.9.5 added the Robot API `move()`, `attach()`, `detach()` (robots driven from code), a *Priority* property on ProcessByRobot for competing agents, and *Safe height* for empty moves as well (release notes).
