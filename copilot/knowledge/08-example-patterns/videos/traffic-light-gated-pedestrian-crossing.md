# Pattern card — Traffic-light-gated pedestrian crossing (Road Traffic + Pedestrian coupling)
- **Source:** AnyLogic video "How to simulate a pedestrian crossing" (https://youtu.be/LHcu91DxE4g) — distilled, original wording
- **Paradigm:** Hybrid (Road Traffic Library + Pedestrian Library)
- **Problem it solves:** Make cars and pedestrians obey the same signal at a crossing, even though the two libraries cannot see each other's agents.

## Mechanism
Two independent layers share `Main`. The traffic light is the only link between them.
- **Cars:** an existing road network. The video reuses the intersection from AnyLogic's Road Traffic tutorial.
  - Add a **Stop Line** just before the crossing.
  - Add a **Traffic Light** that controls that stop line. Where you place its icon does not matter, because it is only a controller.
  - Give the stop line four phases: green, yellow, red, yellow, e.g. 30 / 7 / 30 / 7 s.
- **Pedestrians:**
  - An invisible **Wall** encloses the walkable zone (both kerbs and the crossing).
  - `targetLineA` is where pedestrians appear and `targetLineB` is their goal.
  - The flowchart is `pedSource` → `pedGoTo` (to `targetLineB`) → `pedSink`.
- **Gate:** a Polygonal node, `crossingArea`, covers the crossing. It is invisible, and its Access restriction is set to "restricted by call of close() function".
- **Link:** in the Traffic Light's Actions, set On phase change to `crossingArea.setOpen(currentPhaseIndex == 2);`.
  - `currentPhaseIndex` is the local variable holding the new phase.
  - Phases are numbered from 0 in phase-table order, so with the order above, index 2 is the phase that is red for cars.

## Resources
n/a

## Key settings worth copying
- Pedestrian node API: `open()`, `close()`, `setOpen(boolean)`, `isOpen()`.
- A pedestrian node restricts access in one of three ways: close() calls, capacity or throughput. Only one can be used per node. Speed restriction is set separately.
- *Beyond the video (AnyLogic Help):* for a crossing, leave **Avoid area if closed** unticked. Pedestrians should wait at the kerb, not look for a detour. *(What happens when no detour exists: unverified.)*

## KPIs instrumented
n/a in the video. Useful additions:
- Pedestrian trip time kerb to kerb (TimeMeasureStart/End around `pedGoTo`), compared with the free-walk time, to get the delay the signal causes.
- Vehicle travel time and queue length on the road side.
- To trade the two off, use the phase-duration optimisation pattern in `models/traffic-light-phases-optimization.md`.

## Pitfalls
- **No gate, no interaction.** The libraries ignore each other. Pedestrians walk through moving cars, and cars never yield. There is no built-in handling of car–pedestrian conflicts.
- **Leave no gap.** Draw the node wider than the crossing so that it overlaps the enclosing walls. Any gap between the node's edge and a wall becomes a way around it.
- **Closing only stops new entries.** People already on the crossing keep walking when the cars get green.
  - The yellow phase that follows red-for-cars works as the clearance interval. Size it as crossing length ÷ walking speed.
  - Alternatively, extend the model to hold the cars until the node is empty.
- **Starting state** *(unverified)*. If On phase change does not fire for the first phase, the node starts open (the default) during the first green for cars. If the cycle starts on green, close it in `Main`'s On startup.
- **Hard-coded index.** The literal `== 2` breaks silently if you reorder or insert phases. Check it after every edit to the phase table, or keep the index in a named parameter.

## Reusable idea
To make pedestrians obey any external signal, have the controller's state-change callback call `node.setOpen(condition)`. The same trick works for turnstiles, boarding gates, lift doors and level-crossing barriers.

## When the co-pilot should use this
- Signalised crossings, stadium or campus crowds crossing roads, level crossings, and any model that mixes vehicles with pedestrians.
- A user reports that pedestrians walk through cars, or that cars ignore people on the crossing.

## Additions (8.9.10 review, 2026-10-01)
- *Defines the mode for* has three options (Help 8.9.10 *TrafficLight*): Intersection's stop lines (default), Intersection's lane connectors (lanes of one road in different phases — the one for protected turns), and Specified stop lines (crossings).
- API: `switchToNextPhase()` (for a phase of infinite duration), `getCurrentPhaseIndex()` (0-based, −1 when off), `getPhaseDuration(i)`, `getCurrentPhaseRemainingTime()`, `getCurrentSignal(stopLine)` / `getCurrentSignal(laneConnector)` (null when off or not controlled), and `turnOn()` / `turnOff()`, which also fire *On phase change*. `turnOn(offset)` / `turnOn(offset, units)` starts several junctions with fixed offsets — a simple green wave (8.9.10 *Traffic Light* example).
