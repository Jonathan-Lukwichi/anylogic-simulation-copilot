# Pattern card — Conveyor control and breakdowns: sensor/stop positions, stop()/run(), failures on MHL equipment
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library + PML resources)
- **Problem it solves:** Stop, restart and break down conveyors (and other MHL equipment) from logic, and dispatch a shared technician to repair them.

## Mechanism
1. **Sensors and stops are Positions on conveyor.**
   - **Instant callbacks:** *On leading edge enter* and *On trailing edge exit*, plus *On cell enter/exit* on cell conveyors. Use them for photo-eyes, scanners and counters.
   - **Stop and escapement devices:** `pos.block()`, `pos.unblock()`, `pos.isBlocked()`, and the *Initially blocked* option. `pos.getAgent()` returns the item currently at the position.
2. **Whole-conveyor control.**
   - Functions: `conveyor.stop()`, `conveyor.run()`, `isStopped()`, `setMaxSpeed(v, units)`, `getCurrentSpeed(units)`.
   - Conveyor actions: *On started*, *On stopped*, *On direction changed*, and the four leading/trailing edge enter/exit actions, which receive `runsForward`.
3. **Breakdown, the webinar recipe (any 8.x).** Model the motor as a 1-unit `ResourcePool` named `motor` and borrow the pool's failure engine.
   - **Failure settings:** set Maintenance, failures, shifts, breaks → **Specified by = ResourcePool properties**. Tick **Failures / Repairs**. Give *Initial time to failure* and *Time to next failure* distributions. Set **Usage statistics = counted as busy**, so the pool's "utilization" becomes the share of time the motor is down.
   - **On failure:** `conveyorSouthEntrance.stop(); lamp.setFillColor(red);`
   - **On repair:** `conveyorSouthEntrance.run(); lamp.setFillColor(yellowGreen);`
   - **Repair type = Send to flowchart:** `ResourceTaskStart` → `Service` (engineer, 4 min, *Send seized resources* to a node beside the conveyor) → `ResourceTaskEnd`.
4. **Breakdown, native in 8.9 (beyond the video; Help and Javadoc 8.9).**
   - **Conveyors, stations and jib cranes** have a *Maintenance, failures, breaks → Downtime block(s)* property and report `mtbf(units)` / `mttr(units)`. Attach a PML `Downtime` block directly instead of a proxy pool.
   - **Transfer tables, turntables, turn stations, lifts and overhead cranes** only offer `fail()` / `repair()` / `isFailed()`. Call these from your own failure logic.
   - The conveyor's own transport task has priority 0, so a Downtime's priority decides how the conveyor reacts:
   - **priority < 0:** the downtime waits until the belt is empty;
   - **priority > 0 and may preempt:** the conveyor stops at once;
   - **priority = 0:** no new items are admitted, the loaded items leave, then the conveyor goes down.

## Resources
- `engineer` ResourcePool (1 unit), shared by inspection and repair.
- `motor` proxy pool (1 unit), in the webinar recipe only.

## Key settings worth copying
- **Status lamp:** an oval coloured from On failure / On repair.
- **Repair `Service`:** its task **priority** and **may preempt** settings decide whether repair jumps ahead of inspection.
- **Proxy failure clock:** leave *Count busy time only* **off**. Nothing ever seizes the proxy, so with it on the motor would never fail *(inferred)*. The proxy therefore fails on calendar time, independent of belt load. If wear should depend on use, look at the Downtime block's work-time triggers (Help 8.9); check that they apply to your equipment type *(unverified for markup)*.

## KPIs instrumented
- **Webinar recipe:** the proxy pool's busy fraction equals the downtime share; also track engineer utilization.
- **8.9:** `conveyor.getState() == ConveyorState.FAILED`, `mtbf(HOUR)`, `mttr(MINUTE)`, `getUtilization()`, and the queue at the entrance.
- **Availability:** feed these into availability as in `videos/oee-instrumentation-in-des.md`.

## Pitfalls
- **`stop()` is not a failure.** `isFailed()` stays false, and MTBF/MTTR are not recorded. Use `fail()` / `repair()` or a Downtime block when reliability KPIs matter.
- **Shared technician.** One technician on two task types becomes the bottleneck, as the webinar shows. Make the priority rule explicit and test it.
- **Callbacks are instantaneous.** Put no waiting in edge callbacks. Timed work belongs in a Station (`videos/mhl-conveyor-station-processing-and-reassembly.md`).
- **Version drift.** The proxy-pool trick predates Downtime-on-markup. In 8.9, prefer the native route unless you need custom failure logic.

## Reusable idea
Keep equipment state on the equipment:
- **8.9:** hang Downtime blocks on conveyors, stations and jib cranes, and call `fail()` / `repair()` on the other MHL elements.
- **Older versions:** call `stop()` / `run()` from a failure-capable object's callbacks.

Either way, the repair crew stays an ordinary PML resource task.

## When the co-pilot should use this
- **Use cases:** line reliability and OEE studies, maintenance-crew sizing, e-stop and escapement logic, and sensor-triggered routing.
- **Related cards:**
  - `basicmodels/maintenance-of-a-coffee-machine.md` (Downtime + ResourceTaskStart/End)
  - `basicmodels/item-flow-control-on-a-reversible-conveyor-spur.md` (`block()` / `unblock()` at positions)
