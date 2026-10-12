# Pattern card — Tugger Train Operating on a Predefined Route
- **Source:** AnyLogic example model "Tugger Train Operating on a Predefined Route" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Run a tow train as a fixed milk run — it calls at every station in a set order and drops whatever is for that station — instead of letting the library pick the nearest destination.

## Block chain
`Source` (6 items every `uniform(6, 7)` min, each with a random `targetStation`) → `Queue` → `Hold` (*block automatically
after 6 agents*) → `SeizeTransporter` (fleet `tuggerTrain`; *On seize transporter* → `tugger.setRoute()`) →
**`MoveByTransporter` `toNextStation`** (destination = `tugger.getTargetStation()`; *Seize transporter* off, *Release
transporter* off) → `SelectOutput` (is `agent.targetStation` the train's current stop?)
- yes → `Delay` unload 10 s → `ReleaseTransporter` (*stays where it is*) → `Sink`;
- no → `Delay` `waitOtherForUnload` (*until stopDelay() is called*) → back into `toNextStation`.

## Resources
`TransporterFleet tuggerTrain`: tugger with 6 trailers, one home area, trailers in a custom population; tugger type holds
the route state (below).

## Key settings worth copying
- **Route state on the tugger agent:** a list `stationsToVisit` (filled from `main.stationsList` when the first item
  seizes an empty route), a counter `nUncheckedItems` (items on board still to be sorted at this stop), a flag
  `movesEmptyThroughStations`.
- **The destination is the route, not the cargo.** Every item on board uses the train's current stop as its destination,
  so all of them leave `toNextStation` together at each stop (with *Release transporter* off they exit at once and keep
  the train — Help 8.9.10, *Tugger trains*).
- **Sort, then move on:** both Delays call `tugger.checkIfReady()`; when the last item at a stop has been sorted and some
  are still on board, it drops the stop from the list, resets the counter and `waitOtherForUnload.stopDelayForAll()`
  sends the rest to the next stop.
- **Finish the loop empty:** when the last item releases the train, *On release transporter* raises the flag and starts a
  dynamic event 1 s later; the event pops the stop and calls `move(nextStop, TransporterState.GOING_HOME)`. The fleet's
  *On destination reached* repeats this while the flag is set. After the last stop: `move(home, …)`, clear the flag,
  `main.hold.unblock()` so the next 6 items can board.
- The dynamic event is there on purpose: it keeps the `move()` command out of the same event as the ReleaseTransporter
  command (comment in the model).

## KPIs instrumented
Visual only. Add: loop time, items per loop, time each item waits for its stop, empty-running share of the loop.

## Pitfalls
- The empty legs run in state `GOING_HOME`, so time-in-state statistics book them as return trips; choose the state
  passed to `move()` deliberately (`MOVING_IDLE` is the default for `move(node)`).
- Every item's target must be on the route list. An item whose station is not listed never gets off, and the list
  eventually runs empty under it *(inferred; the demo draws targets from the same list, so it cannot happen there)*.
- The Hold admits exactly one train-load per loop; with more items than trailers per cycle, the queue grows. With
  several tuggers, keep one route state per train and one Hold per train (or a smarter admission rule).
- `SeizeTransporter` seats the item but the train only starts once the item enters `MoveByTransporter` or `move()` is
  called (Help); do not put timed blocks between them unless the train should wait.

## Reusable idea
When the visiting order is a business rule (fixed milk run, one-way loop, delivery sequence), keep the vehicle seized,
drive it stop by stop with a route list on the vehicle, and let each load decide at every stop whether it gets off. The
library's nearest-destination rule then never applies.

## When the co-pilot should use this
Line-side milk runs with fixed stops, hospital or campus delivery loops, one-way aisles where "nearest first" is
physically impossible, and any user who says the tugger "visits stations in the wrong order". Related: `tugger-train.md`,
`moving-transporter-without-flowchart-block.md` (`move()` from code).
