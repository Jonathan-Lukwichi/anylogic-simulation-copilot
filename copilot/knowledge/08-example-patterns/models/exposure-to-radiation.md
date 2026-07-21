# Pattern card — Exposure to Radiation
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Estimate the cumulative radiation dose absorbed by a vehicle agent as it traverses a 2-D environment containing zones of varying radiation intensity.

## Block chain
A single Vehicle agent follows a mission plan — an ordered list of waypoints — using a statechart to sequence movement legs. The statechart starts in a waiting state, receives an "Arrived" message when each leg completes, then triggers a timeout-driven transition to the next waypoint until the route is finished.

While the vehicle moves, a System Dynamics mini-model runs inside the same agent: a **Flow** variable (`CurrentRadiationLevel`) continuously queries a helper function (`radiationLevel(x, y)`) that reads the vehicle's current coordinates, iterates over all drawn radiation-zone shapes on the map, and maps their fill colour to a numeric intensity level. That flow feeds a **Stock** variable (`TotalRadiationExposure`) which integrates dose over time. Because the SD equations run at every simulation step, the accumulated dose rises faster when the vehicle lingers in high-intensity zones and rises slower (or plateaus) in clean zones.

The environment is a raster-style map where coloured polygons represent radiation hot-spots; no GIS import is required — ordinary AnyLogic shape groups serve as the spatial data layer. A slider lets the user adjust vehicle speed (40–150 km/h) at runtime, demonstrating how velocity affects final exposure.

## Resources
- One Vehicle agent instance (singleton, not a population)
- One statechart (`statechart`) governing waypoint-to-waypoint movement
- One SD stock (`TotalRadiationExposure`) and one SD flow (`CurrentRadiationLevel`) embedded in the agent
- Radiation zone group (`groupRadiation`) — coloured shape overlays acting as a spatial intensity map

## Key settings worth copying
- **Model time unit:** Minute
- **Default vehicle speed:** 80 km/h (slider range 40–150 km/h), set via `vehicle.setSpeed(velocity, KPH)` at startup
- **Radiation lookup:** `radiationLevel(double x, double y)` iterates `groupRadiation.getShapes()`, calls `area.contains(x - offsetX, y - offsetY)`, and maps shape colour to an integer level — a lightweight substitute for a real GIS raster
- **SD integration step:** inherits the model step (1 second converted internally); stock initial value = 0
- **Statechart triggers:** "Arrived" message on leg completion, timeout transitions for dwell/next-leg logic
- **Final snapshot:** `finalRadiationExposure` variable captures `TotalRadiationExposure` at mission end for reporting

## KPIs instrumented
- `TotalRadiationExposure` — running integral of radiation dose (stock value over time)
- `finalRadiationExposure` — scalar summary at end of mission
- Implicit: effect of speed on dose (higher speed = less time in hot zones = lower total dose)

## Reusable idea
Embed a tiny SD stock-and-flow inside a moving agent to accumulate any spatially varying quantity (pollution, noise, heat, cost-per-metre) as the agent traverses a colour-coded zone map. The key trick is the `radiationLevel(x, y)` pattern: use the agent's live coordinates plus a shape-group overlay as a zero-infrastructure raster lookup, avoiding any external GIS dependency while still delivering realistic spatial variation.
