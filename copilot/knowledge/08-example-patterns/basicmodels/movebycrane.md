# Pattern card — MoveByCrane
- **Source:** AnyLogic example model "MoveByCrane" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** One overhead crane serving several stations in sequence (conveyor → dip tank → machine → back to conveyor) without deadlocking itself, using the three kinds of crane destination.

## Block chain
`Source` (5/min, no push) → `Convey` (onto the input conveyor) → `MoveByCrane` *toTank* (destination node `tankNode`, priority 1) → `Delay` *inLiquid* (3 min, capacity 10, agents shown at `tankNode`) → `RestrictedAreaStart` (capacity 1) → `MoveByCrane` *toMachine* (destination type **agent** = the machine resource unit, priority 2) → `Service` *processing* (machine pool, 25 s) → `RestrictedAreaEnd` → `MoveByCrane` *toConveyor* (destination type **position on conveyor**, priority 3) → `Convey` (from current position to the output conveyor) → `Sink`.

## Resources
One Crane markup (`crane`), safe height 3.5 m on the first two moves; a static `ResourcePool` of `Machine` agents placed at `machineNode` (custom population `machine`).

## Key settings worth copying
- Destination types of MoveByCrane: node (`destinationNode`), agent (`DEST_AGENT`, `destinationAgent` — here the machine unit), position on conveyor (`DEST_POSITION_ON_CONVEYOR`, `destinationPositionOnConveyor`); after a drop on a conveyor continue with `Convey` *from current position*.
- **Downstream-first task priorities:** the later the step, the higher the crane task priority (tank 1 < machine 2 < unload machine 3), so the crane always clears the machine before feeding new work.
- **RestrictedArea of capacity 1 around "crane in → process → crane out"**: a part may request the crane for the machine only when the machine cell is free, so the crane never lifts a part it cannot put down.
- Height fix for animation: in the Service, *On enter* sets the part's Z to the machine's table height and *On at exit* lowers it again (`agent.setXYZ(x, y, z)`).

## KPIs instrumented
Visual (2D/3D view areas); no statistics.

## Pitfalls
- A single crane feeding a single-capacity station deadlocks if it can grab a new part while the finished one still occupies the station: nobody can move. Both guards (restricted area + downstream priority) are needed.
- *Priority* (applies only with *Seize crane* ticked) is the rule for choosing which waiting agent the crane serves next — larger value first, ties FIFO (Help 8.9.10). It does not interrupt a move already under way, so a long low-priority move still delays an urgent one.

## Reusable idea
For any shared handler (crane, robot, AGV) that feeds and empties the same stations: give unloading/downstream tasks the higher priority and gate loading with a capacity-limited restricted area equal to station capacity. This "pull from the end" rule is the standard cure for handler deadlock.

## When the co-pilot should use this
Crane or robot cells with sequential stations, dip/plating lines, or whenever a user reports a crane (or transporter) "stuck holding a part". For safe height and movement modes see `videos/mhl-crane-reach-safe-height-movement-mode.md`; for several bridges on one runway see `crane-system-with-multiple-bridges.md`.
