# Pattern card — Pedestrian Density Map
- **Source:** AnyLogic example model "Pedestrian Density Map" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Show and query crowd density in a small subway station where two trains release and take bursts of passengers, and let the viewer tune the density display at run time.

## Block chain
- **Alighting:** one `PedSource` per train door (replicated, `rate = 0` by default); `startTrainUnload(i)` sets every door source of train *i* to `uniform_discr(2000, 2250) / hour()` with `set_rate(...)`, `stopTrainUnload(i)` sets it back to 0 → `PedSelectOutput` (four equal probabilities) → `PedGoTo` to one of four exits → `PedSink`.
- **Boarding:** street `PedSource`s (2500/h each) → `SelectOutput` → `Exit` whose action pushes each pedestrian into a random door's sub-flowchart, `goToTrain1.get(uniform_discr(0, 31)).enter.take(agent)`. `GoToTrain` is an agent type holding its own flowchart (`Enter` → `PedGoTo` platform → `PedWait` in the door's waiting area → `PedGoTo` door line → back to Main's sink); its parameters are the door line and waiting area; `board()` calls `waitTrain.freeAll()` when the train opens.

## Resources
n/a

## Key settings worth copying
- Density Map element on the ground level: based on *space*, type *pedestrian*, time period *complete run*, displayed value *maximum*, logarithmic colours (settings themselves: `videos/pedestrian-service-occupancy-sizing-and-density-map.md`).
- **Query at a point:** `level.getDensityMap().currentDensity(x, y)` and `maximumDensity(x, y)` (also per level or per network element) — the demo shows both under a movable marker.
- **Run-time control:** `densityMap.show()` / `hide()`, `setColorScheme(LINEAR_COLOR_SCHEME | LOGARITHMIC_COLOR_SCHEME)`, `setEnableAttenuation(bool)`, `setTransparency(0…1)`, `setCriticalDensity(pedPerM2)`; a *Custom* colour scheme takes an expression of the local `density`.
- **Attenuation (Help):** with a *maximum*, complete-run map, attenuation off shows the historical maximum; attenuation on shows recent density and lets colours fade gradually as density drops.
- Burst arrivals from a vehicle: switch replicated sources' rate between a high value and 0 rather than injecting agents one by one.

## KPIs instrumented
Current and maximum density at a chosen point; visual density field.

## Pitfalls
- The model description still names the pre-8.x objects *PedGround* and *PedDensityMapLegend*; in 8.9.10 the settings live on a **Density Map** markup element on the level.
- A maximum-over-the-run map without attenuation never cools down: short peaks (a train unloading) look like permanent hot spots. Use attenuation or a sliding window when judging typical conditions.
- Rate-switched sources keep generating until set back to 0 — pair every start with a stop (here by train events).

## Reusable idea
Pair the density map with point queries (`currentDensity` / `maximumDensity`) at critical spots (doors, stair heads, gates) and log them as KPIs instead of only eyeballing colours; model vehicle unloading as rate-switched per-door sources and boarding as per-door sub-flowcharts released together.

## When the co-pilot should use this
Station platforms, stadium exits, event venues — any study of crowd density peaks, and questions about reading density values in code or tuning the map at run time.
