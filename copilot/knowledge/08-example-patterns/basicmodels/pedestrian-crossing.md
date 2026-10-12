# Pattern card — Pedestrian Crossing
- **Source:** AnyLogic example model "Pedestrian Crossing" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (Road Traffic + Pedestrian libraries, car statechart)
- **Problem it solves:** Make cars and pedestrians respect each other at crosswalks — two signalised crossings (one automatic, one switched by a button) and one **unregulated** zebra crossing where cars must slow down and yield.

## Block chain
Cars: `CarSource` (random road from `roadList`, 20 km/h, custom population `cars`) → `CarMoveTo` (end of backward lane) → `CarDispose`. Pedestrians: `PedSource` (1300/h at a random target line, comfortable speed `uniform(0.5, 1.5)` m/s) → `PedGoTo` (target line picked with `triangular(1, 6, 8)` as index) → `PedSink`. Each crosswalk is a pedestrian **area node** whose access can be closed.

## Resources
n/a

## Key settings worth copying
- **Signalised crossings (known pattern):** the traffic light's phase action opens the crosswalk only in the car-red phase (`area.setOpen(currentPhaseIndex == 2)`); a map `zoneToTrafficLight` (area → light) lets shared car code know which areas are signalised.
- **Sensor without a signal:** Stop Lines drawn on each approach lane just before the crossing are used only as detectors — *On car passed* calls `car.yield(area)` (the action has a local `car`).
- **Car yield statechart (unregulated crossing):** `yield(area)` stores the area and, if pedestrians are on it, sends the car the message "CAREFUL" → the car halves its preferred speed and quarters its acceleration (`setPreferredSpeed`, `setMaxAcceleration`) and starts a timeout that later sends "FOLLOW" to restore them. A condition transition stops the car (`setPreferredSpeed(0)`) while pedestrians are in the area, within 2.5 m (`agentsInRange(main.pedestrians, 2.5, METER)`), or when the car has reached the area edge (`getNearestPoint` equals the car's point); another condition resumes it once the area is clear.
- **Lock the crosswalk while the car crosses:** on resuming, the car calls `lastArea.setOpen(false)`; an event `freeZone` re-opens it — restarting itself while pedestrians are still inside, and for signalised areas restoring the light-based state instead.

## KPIs instrumented
Visual only.

## Pitfalls
- The two libraries do not see each other: without the gate/statechart logic, pedestrians walk through cars and cars never yield (see `videos/traffic-light-gated-pedestrian-crossing.md`).
- Speed changes made in a statechart are multiplicative here (½, ×2); if two triggers overlap without the matching restore, the car keeps a wrong speed — restore from stored values, as the stop/resume pair does.
- A crosswalk closed by a car and never re-opened blocks pedestrians forever; always pair `setOpen(false)` with a guaranteed re-open event.

## Reusable idea
Use road markup (stop lines) as event sensors, a small car statechart as driver behaviour (careful / stopped / following) driven by pedestrian presence in the area, and the pedestrian area's open/closed state as the pedestrians' "signal" — unsignalled conflicts become explicit and tunable.

## When the co-pilot should use this
Zebra crossings, shared spaces, parking-lot pedestrian paths, campus roads — any place where cars must yield to pedestrians without a traffic light. For signal-gated crossings use `videos/traffic-light-gated-pedestrian-crossing.md`.
