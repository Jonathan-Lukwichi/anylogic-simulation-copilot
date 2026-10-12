# Pattern card — RoadNetworkDescriptor: network-wide car callbacks, a speed-coloured "density" map, and deadlock auto-resolution that can hide gridlock
- **Source:** AnyLogic 8.9.10 Help tutorial "Intersection (Road Traffic Library)" — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Measure a road network (travel time, stops, jams) without threading every car through extra blocks, and make sure the engine is not quietly dissolving the congestion you are studying.

## Mechanism
The tutorial's last phase adds a Traffic Light on the T-junction (phases 30 s / 20 s) and a `RoadNetworkDescriptor`
with *Enable density map* ticked, then suggests trying other phase splits (30/20 against 30/30) by eye. The
descriptor has no ports; you point it at one road network. Its settings (Help 8.9.10, *RoadNetworkDescriptor*):
- **Road section length**, 50 m by default. Roads are cut into sections for the map and for average-speed reporting.
- **The "density" map colours each section by the average car speed on it**, not by cars per km: green at or above
  *Green speed level* (default 60), red at or below *Red speed level* (default 10). The levels are in **km/h**: each
  carries its own speed-unit selector, the 8.9.10 *Roundabout* example stores `redSpeedLevel` = 10 KPH, and the
  engine's internal unit for `set_greenSpeedLevel` / `set_redSpeedLevel` is km/h (resolved 2026-10-01; gotcha G61). Map transparency defaults to 0.6. The overview page *Displaying traffic jams*
  still speaks of car density, so read red as "slow", not as "crowded".
- **Callbacks** for every car in the network, each with the car as a local variable:
  - *On enter network* / *On exit network*;
  - *On enter road* / *On exit road* (`road`, `isRoadForward`);
  - *On enter intersection* / *On exit intersection*;
  - *On lane change* (`previousLaneIndex`, `currentLaneIndex`);
  - *On stop* (blocked by the car ahead, preferred speed 0, a stop line, or arrival at a bus stop or parking space) and
    *On resume moving*; *On car clicked*.
- **Automatically resolve deadlocks**, **on by default.** When cars block each other for good, AnyLogic detects it and
  temporarily lets them pass through each other so the model keeps running.

## Resources
n/a — one descriptor per road network.

## Key settings worth copying
- **Travel time without TimeMeasure blocks:** in *On enter network* store `time()` in a field of your car type; in
  *On exit network* add `time() - thatField` to a Statistics or Histogram Data element. Cast `car` to your type to
  reach the field *(the Help types the local variable as `T car` and lists no car-type setting)*.
- **Signal delay and stop counts:** count *On stop* events per car; time each stop until *On resume moving*.
- **Weaving:** count *On lane change* events per road.
- **Validation run for capacity studies:** untick *Automatically resolve deadlocks*. If the model then freezes, you have
  a real gridlock or a markup error; find out which before you report travel times.
- API: `size()` (cars in the network), `getCar(i)`, and `set_enableDensityMap(...)` to toggle the map at runtime.

## KPIs instrumented
The tutorial only shows the map. The callbacks above give mean and 95th-percentile network travel time, stops per car,
and time lost at the signal. Compare phase plans on these numbers over replications, not by watching the colours.

## Pitfalls
- **Resolved deadlocks bias results.** In saturated scenarios, cars passing through each other give optimistic travel
  times and no error. The Help documents the switch only as a descriptor property with default true; that the same
  default applies with no descriptor in the model is *(unverified)*. Add a descriptor to control it.
- **Thresholds must fit the road.** With the default levels, a street with a 30 km/h limit shows yellow or red
  even when it flows freely.
- **Phase tuning by eye** at animation speed hides variance. Use the optimization pattern in
  `models/traffic-light-phases-optimization.md`.

## Reusable idea
Instrument the network once, at the descriptor, instead of every flowchart branch. Then prove that the engine is not
dissolving the jams you are trying to measure.

## When the co-pilot should use this
- Any Road Traffic Library model that reports travel times, queues or level of service, and any junction or signal study.
- Symptoms: cars overlap at a congested junction, a saturated network never locks up, the "density" colours disagree
  with the counts.
- Related: G27; `videos/road-destination-refusal-parking-bus-stop-outwaynotfound.md`;
  `videos/traffic-light-gated-pedestrian-crossing.md`.
