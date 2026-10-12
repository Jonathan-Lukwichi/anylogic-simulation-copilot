# Pattern card — Station and Crane Maintenance
- **Source:** AnyLogic example model "Station and Crane Maintenance" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library + PML Downtime)
- **Problem it solves:** Give conveyor equipment realistic unavailability — random station failures repaired by a travelling crew, and preventive crane maintenance every N lifts — through the equipment's own *Downtime block(s)* property.

## Block chain
`Source` (every 6 s, pull) → `Convey` (from 1 m on the main conveyor to the station; processing 3 min) → `Split` (the
processed detail yields a scrap piece: *On exit copy* hides one shape and turns the copy 90°, *On exit* hides the other)
- original → `Convey` (from its current position onto the conveyor) → `MoveByCrane` (`crane` → exit node) → `Sink`;
- copy → `MoveByCrane` (`tableCrane` → onto the scrap conveyor) → `Convey` (along the scrap conveyor) → `Sink`.

Both crane moves use *Use operation time* = 3 min.

## Resources
`repairBrigade` ResourcePool (2 units, moving at 0.1 m/s from a home node); two jib cranes; one conveyor simple station.

## Key settings worth copying
- **Station failures** (`stationFailures`, attached via the station's *Downtime block(s)*): *Type* = Failure / repair;
  trigger *Total time between occurrences* `triangular(20, 30, 45)` min; *Task type* = Delay with resources, 15 min,
  units from `repairBrigade`, *Send seized resources* to a repair node; priority 1, *May preempt*.
- **Crane maintenance** (`craneMaintenance`, on `tableCrane`): Maintenance, trigger **Cycles between occurrences = 5**,
  duration 20 min.
- **Trigger families** (Help 8.9.10, *Downtime*): *Total time* (calendar, idle included; countdown from task start or
  finish), *Working time* (busy time incl. travel to the agent), *Cycles* (number of seizures; a job interrupted and
  resumed counts twice). Optional *Custom first occurrence* (time, working time or cycles to first); Maintenance and
  Custom types may use an on/off `Schedule<boolean>` instead.
- **Operation time instead of kinematics:** with *Use operation time*, the crane's speeds are recalculated per item so
  the move takes the given time (loading and unloading included when the block seizes and releases the crane; Help,
  *MoveByCrane*).

## KPIs instrumented
Visual only. Available: `station.mtbf()` / `mttr()`, crane and station state times (FAILED, MAINTENANCE), crew
utilization, good-part vs scrap counts, time items wait at the station.

## Pitfalls
- `triangular(20, 30, 45)` is min 20, mode 30, max 45 (AnyLogic takes the larger of the last two as maximum) — mean
  31.7 min (G55).
- Calendar-time failures keep counting while the station is idle or starved; use *Working time* if failures come from
  use. Cycle counts ignore how long each lift takes.
- Downtime vs running work (Help, jib crane): loading or unloading cut by a downtime is restarted afterwards; a
  higher-priority downtime without *May preempt* waits for the current task; items with a priority above the downtime
  go first. Effective cycle times grow beyond "process time + downtime".
- Overhead cranes also take Downtime blocks (per bridge) in 8.9.10 — see the proposals note on G43.

## Reusable idea
Keep failure and maintenance on the equipment: attach Downtime blocks to the markup element, pick the trigger that
matches the physics (calendar, running hours or cycles), and let a PML pool travel to repair. Swap trigger types to test
maintenance strategies without touching the material flow.

## When the co-pilot should use this
Availability, OEE and maintenance-strategy studies on conveyor lines and crane cells; sizing a repair crew;
"maintenance every N cycles" requirements. Related: `../videos/mhl-conveyor-control-sensors-and-breakdowns.md`,
`maintenance-of-a-coffee-machine.md`, `transporter-charging-system.md`, `../videos/oee-instrumentation-in-des.md`.
