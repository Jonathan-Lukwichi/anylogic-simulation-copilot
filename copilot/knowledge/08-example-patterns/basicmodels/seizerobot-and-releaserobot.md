# Pattern card — SeizeRobot and ReleaseRobot
- **Source:** AnyLogic example model "SeizeRobot and ReleaseRobot" (basicmodels), AnyLogic 8.9.10; hand-off comparison with the sister demos "SeizeCrane and ReleaseCrane" and "SeizeTransporter and ReleaseTransporter" — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Keep one robot holding an item across several steps — waiting for equipment to be ready, dipping, lifting out, handing over to an AGV — instead of seizing and releasing it at every move.

## Block chain
`Source` (one bottle at a time: *On startup* injects the first, the `Sink` injects the next) → **`SeizeRobot`** (robot, *Movement time* 5 s, top approach, safe height 1 cm) → `Hold` (mode *block automatically after N agents*, default count) → `ProcessByRobot` "into the tank" (5 s, *Seize robot* and *Release robot* **off**) → `Delay` (20 s washing; bubbles on, then the bottle recoloured and the water turned dirty) → `ProcessByRobot` "out of the tank" (5 s, seize/release off; *On processing end*: restart the event `washingMaintenance`) → **`SeizeTransporter`** (an AGV comes under the robot) → **`ReleaseRobot`** → `MoveByTransporter` (seize off, to the AGV home) → `Sink`.
The event `washingMaintenance` (a user-controlled 30 s timeout, restarted after each wash) cleans the water and calls `hold.unblock()`: the next bottle can go in only after the tank is clean, and the robot keeps holding it meanwhile.

## Resources
One Robot markup element (end effector: vacuum gripper); `TransporterFleet` of one AGV type (2 m/s). No PML resource pools.

## Key settings worth copying
- **SeizeRobot (Help 8.9.10; blocks added in 8.9.5):** *Robot*, *Movement time* (**default 1 minute** — the time for the end effector to reach the destination), *Destination is* (agent, node, attractor, conveyor + offset, position on conveyor, (x, y, z)), approach side, safe height. Requests wait FIFO in the block's queue.
- **In between:** every `ProcessByRobot` with *Seize robot* and *Release robot* unticked reuses the held robot; its *Operation time* still covers the arm move plus the work (`basicmodels/processbyrobot.md`).
- **ReleaseRobot:** zero time; *After operation, robot*: stay, return to the initial position, or move the end effector to a target, with a *Post-process time*, done only if nobody is queued. An agent that holds no robot passes with a warning. Give back every seized robot before the agent leaves the model.
- **Equipment-ready gate:** a self-blocking `Hold` opened by an event (`hold.unblock()`) holds the robot and its load until a machine, tank or fixture is ready.

## KPIs instrumented
Visual only. Add robot busy share including holding and waiting time (it is seized throughout), the time the robot waits at the gate, and the AGV wait for the hand-off.

## Pitfalls
- **Hand-off order: seize the receiver before releasing the giver.** Here `SeizeTransporter` comes before `ReleaseRobot`, so the bottle is never left unattended. The crane-and-AGV demo does the same the other way round: the unloading crane lifts the load clear of the AGV (*Release crane* off) before `ReleaseTransporter`, and only then puts it on the conveyor; the crane demo keeps the crane through operator loading, a joining step and a two-operator detach before `ReleaseCrane` (*returns to initial position if no other tasks*).
- **Holding is capacity.** A robot or crane held through waits and manual work is unavailable to others; that is the point, but size the cell with this busy share, not with motion time alone.
- **Default movement time of 1 minute** on `SeizeRobot` quietly adds a minute per seize; set it.
- **Deadlock risk:** a device held while waiting for a second device that waits for the first stalls the cell; order seizes consistently (all robots before AGVs, say).

## Reusable idea
Use explicit Seize…/Release… around a sequence whenever the device must stay with the load — as a fixture during manual work, while waiting for equipment, or through a hand-off — and always overlap the holds at a hand-off: receiver seized, then giver released.

## When the co-pilot should use this
Robot or crane cells with dip tanks, ovens, test stands or fixtures; robot-to-AGV and crane-to-AGV transfers; any "the device must not let go yet" logic. Single-move robots: `basicmodels/processbyrobot.md`; explicit transporter seize: `videos/mhl-agv-dispatch-choice-and-cargo-position.md`; crane moves and priorities: `basicmodels/movebycrane.md`.
