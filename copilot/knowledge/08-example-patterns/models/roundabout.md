# Pattern card — Roundabout
- **Source:** AnyLogic example model "Roundabout" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** Evaluate a four-arm roundabout with a parking detour: give-way behaviour at entries, an origin–destination mix per arm, and trip KPIs (time, speed, stops per car).

## Block chain
- **Traffic sources:** one `CarSource` per arm. Cars: west 2500/h, east 2000/h, north 1500/h, south 1500/h; `preferredSpeed = uniform(50, 80)` km/h, `LANE_RANDOM`. Bus sources: west 15/h, north 10/h.
- **Routing:** one `SelectOutput5` per origin, holding **relative weights** (e.g. 7 : 2 : 1). Help 8.9.10 says the five probabilities are normalised when they do not sum to 1, so each row of the O-D matrix can be typed as counts.
- **Exits:** each branch is a `CarMoveTo` to an exit road with `destination = END_OF_BACKWARD_LANE`, then `CarDispose`.
- **Parking detour:** `CarMoveTo` (moves to `PARKING_LOT`, `parkingLot`) → `Delay` (uniform 10–15 min, max capacity) → `CarMoveTo` north exit.
- **Fallback chain.** Each `outWayNotFound` port feeds the next-best destination: first parking lot → second lot → north exit; east/west exit → south exit. The last resort is a separate `wayNotFoundDispose`, which is counted. Wiring the port is KNOWN-KB (`basicmodels/carmoveto.md`, `videos/road-destination-refusal-parking-bus-stop-outwaynotfound.md`); the chain to a counted dispose is this model's addition.
- **Geometry (markup, not blocks):**
  - 17 roads and 7 road junctions, with 84 lane connectors that define the allowed turns.
  - 20 stop lines, 6 of them carrying the **Yield** sign, so entering cars give way. That they sit on the ring entries is inferred from the counts.

## Resources
n/a. Capacity comes from lanes, junction conflicts and the two parking lots.

## Key settings worth copying
- **Give way with Yield stop lines** (Help 8.9.10, *Stop line*). A stop line carrying the Yield sign makes cars stop if needed and let traffic on another approach go first. Signs can be combined with a speed limit. API: `addYieldSign()` / `isYieldSign()`, `queueSize()` (total or per lane), `averageSpeed(KPH)`, and the action *On car passed* (`car`, `laneIndex`). The entry stop lines are therefore the natural place to read entry queues and entry speeds.
- **Network-wide hooks** are KNOWN-KB (`basicmodels/displaying-traffic-jams.md`, `videos/road-network-descriptor-callbacks-speed-map-deadlocks.md`). This model uses:
  - *On stop* → `carStopsCounter++`;
  - *On enter / exit network* to make the 3D camera follow the first car (`window3d.setCamera(car.camera, true)`);
  - the speed-coloured map with red at 10 km/h and 30 m sections.
- **Trip clock:** a `Vehicle` base type with `startTime = time()`. Both disposes call `onVehicleArrived(car)`.

## KPIs instrumented
Recorded when each car is disposed:
- time in system;
- trip mean speed, `getDistanceDriven(KILOMETER) / toTimeUnits(timeInSystem, HOUR)` (`getDistanceDriven` counts from car creation or `resetDistanceDriven()`, Help *Car*);
- stops per car, `carStopsCounter / (carDispose.count() + wayNotFoundDispose.count())`.

## Pitfalls
- **Early bias in stops per car.** The stop counter includes cars still in the network, but the divisor counts only cars that left, so the ratio runs high early on. Warm up, or count stops per car and record them at dispose.
- **A non-zero way-not-found count is a markup bug.** Missing lane connectors, a random lane choice or an unreachable exit send cars there. Fix the network rather than reporting those cars as traffic.
- **Speed depends on the trip.** Parking dwell inflates time in system and deflates trip speed, so report parkers separately.
- **Give-way needs markup.** Without Yield signs (or signals) on the entries, entering cars do not defer to circulating ones.
- **Saturated roundabouts can gridlock.** The descriptor's *Automatically resolve deadlocks* is on by default and dissolves the lock silently. Run once with it off before trusting capacity results (see the descriptor card).

## Reusable idea
Build a roundabout as junction-linked ring roads with Yield stop lines on the entries. Encode demand as per-origin weight rows. Chain every `outWayNotFound` to a fallback and finally to a counted dispose. Instrument trips at dispose (time, distance-based speed, stops) and read entry queues from the stop lines.

## When the co-pilot should use this
- **Use cases:** junction design comparisons (roundabout vs signals), parking-access studies, and entry-capacity checks under growing demand.
- **Related cards:** `models/city-square.md`, `models/traffic-light-phases-optimization.md` (signal timing) and `videos/traffic-light-gated-pedestrian-crossing.md`.
