# Pattern card — Rail shuttle with pedestrian boarding (Ped-to-Rail hand-off)
- **Source:** AnyLogic video "How to simulate a shuttle train" (https://youtu.be/iJYW24Yk170) — distilled, original wording
- **Paradigm:** Hybrid (Rail + Pedestrian + Process Modeling libraries)
- **Problem it solves:** One rail car runs back and forth on a single track between two stations, and walking passengers board or alight only while it is docked.

## Block chain
Two flowcharts on `Main` are coupled through block actions and one Queue.
- **Train loop (Rail + PML):** `trainSource` → `stopA` (Delay) → `pickupA` (Pickup) → `fromAToB` (TrainMoveTo) → `dropoffB` (Dropoff) → `stopB` (Delay) → `fromBToA` (TrainMoveTo, backward) → back into `stopA`. There is no TrainDispose. The closed loop keeps the single car circulating for the whole run.
- **Passengers (Ped + PML):** `pedSource` (at `lineEntryA`) → `pedWaitA` (PedWait in `waitAreaA`) → `goToBoardingA` (PedGoTo to `lineTrainA`, with its `ccl` port wired back into `pedWaitA`) → `pedExit` → `inTrainA` (Queue, connected to `pickupA.inPickup`) … riding … `dropoffB.outDropoff` → `pedEnter` (at `lineTrainB`) → `pedGoTo` (to `lineEntryB`) → `pedSink`.
- The video does not say where the Dropoff sits. This card puts it straight after the arrival move.

## Resources
n/a. There is no ResourcePool. The rail car is the carrier and, as built, has no capacity limit.

## Key settings worth copying
- `trainSource`: Limited number of arrivals, max 1 · Number of cars 1 · `Entry point defined as` = `Offset on the track` (track `railwayTrack`, offset measured from its start) · New rail car = the custom Rail Car Type `PassengerCar` · Car length 10 m.
- Stations: `terminalA` and `terminalB` are **Position on Track** elements at the two ends of the track.
- `fromAToB` / `fromBToA`: `Route is` = `Calculated automatically from current to target track` · `Target is` = `A given position on track` (`terminalB` / `terminalA`) · Finish options = Decelerate and stop. On `fromBToA`, set **Direction = Backward**.
- `stopA` and `stopB`: Delay time 1 min (the dwell).
- `pedWaitA`: Delay ends = **On free() function call**. Pedestrians are held until code releases them, with no timer.
- `stopA` On enter: `pedWaitA.freeAll();`. The car's arrival releases the waiting crowd.
- `stopA` On exit: `goToBoardingA.cancelAll();`. Anyone still walking to the door leaves through `ccl` and rejoins `pedWaitA`.
- `pickupA`: Pickup = All available agents, so it takes everything in `inTrainA`. `dropoffB`: Dropoff = All available agents.
- `pedExit` removes the walker from pedestrian space, but the agent carries on through the flowchart. `pedEnter` puts it back at a target line. This pair is what lets a pedestrian ride inside another agent.

## KPIs instrumented
n/a in the video. Cheap additions:
- Riders per departure: read `inTrainA.size()` in `stopA` On exit.
- Platform wait: TimeMeasureStart before `pedWaitA` and TimeMeasureEnd after `pedExit`. Passengers who miss a train keep their first timestamp, so their extra wait is counted.

## Pitfalls
- **Reversing needs its own block.** *Beyond the video (AnyLogic Big Book, ch. 9):* TrainMoveTo only plans routes that need no change of direction. The return leg on the same track needs a separate block with Direction = Backward. Use one TrainMoveTo per direction change.
- **Extra trains.** TrainSource's default schedule creates a train every 10 min (Big Book). Without the 1-arrival cap, a second train appears on the shuttle's track and the Rail Library flags a collision.
- **The train must fit.** The whole train has to be on one track when it is created, so the entry offset must be at least the train length. Otherwise you get the runtime error "The car being created must fully be on one track" (Big Book).
- **Instant stops.** With the default Finish option (finish at current speed), the car halts and relaunches instantly because its speed stays set during the dwell. Use Decelerate and stop on arrival, and set Start options = Accelerate/decelerate to cruise speed on the next move (Big Book). The video does not show the start option.
- **Late arrivals miss the train.** `freeAll()` only releases pedestrians who are waiting at that moment. Anyone reaching the platform during the dwell waits for the next trip. To change this, set a `trainAtA` flag in `stopA`'s On enter, clear it in On exit, and send arrivals past `pedWaitA` while it is true, for example with a PedSelectOutput *(suggested, unverified)*.
- **Unlimited boarding.** As built, everyone boards. For a capacity cap, call `goToBoardingA.cancelAll()` once `inTrainA.size()` reaches the limit, for example from the Queue's On enter *(suggested, unverified)*.
- **The coupling is purely logical.** A passenger has boarded when they reach `lineTrainA`, wherever the car is. Draw the target lines where the car actually stops.
- **Scale.** Drawing the first track triggers a prompt to switch to a rail-friendly scale (2 px per metre, Big Book). Accept it before drawing the pedestrian markup, because a scale change also changes the real size of everything already drawn.

## Reusable idea
This works for any vehicle that carries walkers: a shuttle, bus, cable car or ferry.
- The vehicle's arrival action releases the platform crowd with `freeAll()`.
- Its departure action recalls stragglers with `cancelAll()` and the `ccl` loop.
- Riders leave pedestrian space for the trip: PedExit → Queue → Pickup … Dropoff → PedEnter.

For two-way service, mirror the passenger branch with a pickup at B and a drop-off at A.

## When the co-pilot should use this
- Airport or campus people-movers, park-and-ride shuttles, and any case where pedestrians ride a Rail Library vehicle (or any vehicle driven by a flowchart).
- "How do I send a train back along the same track?" and "How do I release waiting pedestrians when an event happens?"
- For a full-scale model, see `models/airport-with-two-terminals.md`. For a GIS version, see `basicmodels/agent-moves-between-spaces.md`.
