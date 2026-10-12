# Pattern card — Route Provider
- **Source:** AnyLogic example model "Route Provider" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM / DES in GIS space
- **Problem it solves:** Let different agent types in one GIS model follow different real networks — trucks on roads, trains on railways — instead of the single network the GIS map provides.

## Block chain
`Enter` → `MoveTo` (destination = GIS point `Nice`) → `Sink`. Two buttons push a random agent into the flow: `enter.take(cars.random())` or `enter.take(trains.random())`. Both populations start at the GIS point `Paris`; sent together, the car and the train take visibly different routes to Nice. Model time unit: hour.

## Resources
n/a. Populations `cars` (100, initial speed 85 km/h) and `trains` (100, 120 km/h); speeds are set on the populations, which override the agent types' defaults (Help 8.9.10, *Agent movement speed*).

## Key settings worth copying
- **Two providers, one map:** GIS Map → *Routing* → *Road type* = Car is the default for every agent. A **Route Provider** element (GIS section of the Space Markup palette) with *Road type* = Rail is the alternative. In the `trains` population, *Initial location → Routing* names `routeProvider`; `cars` keep *Default*. Road types: Car (all vehicles), Rail, Bike, Foot.
- **Route Provider properties (Help 8.9.10):** *Routes are* requested from an OSM server, loaded from a **PBF file** (a local routing graph; pathfinding A* bidirectional or Dijkstra bidirectional), or straight lines; *Routing method* Shortest or Fastest (the demo: Fastest); *If route not found* → create a straight route and continue, or show an error dialog (the demo: error dialog).
- **At run time:** `agent.setRouteProvider(provider)` switches an agent's network (it stops the agent if it is moving); `getRouteProvider()` reads it; the map's own default provider is `map.getRouteProvider()`. A population's *Routing* can also point at a hand-drawn GIS network of points and routes.
- **Custom provider:** *Use custom route provider* opens a code template implementing `IGISRouteProvider` with `getPathData(startLat, startLon, endLat, endLon)` (returns a `Curve<GISMarkupSegment>`) and `getDistance(...)`; the template draws a straight line and measures it with `Utilities.getDistanceGIS(...)`.

## KPIs instrumented
None. Add per-mode trip time and distance to compare modes: the map's `getDistanceByRoute(...)` uses the map's default provider (Help, *GIS map*); for the other network ask that provider, e.g. `routeProvider.getDistance(latFrom, lonFrom, latTo, lonTo)` (an `IGISRouteProvider` method).

## Pitfalls
- **Online dependency:** OSM routing needs internet access (AnyLogic's routing server; Private Cloud lists it as an external service). For offline, Cloud or reproducible runs, use a PBF graph (Help: GIS maps and routing can work without internet using a local PBF file).
- **Error vs straight line:** *Show error dialog* stops the run when a rail route does not exist between two points (a station off the network); *Create straight route* keeps running but silently shortens the trip. Log straight-line fallbacks if you choose them.
- **Switching providers mid-trip** stops the agent; switch at a terminal (a transfer point), not while moving.

## Reusable idea
Model multimodal logistics on one map: one provider per mode, the mode chosen per population or per trip with `setRouteProvider`, and transfers as explicit stops where the provider changes.

## When the co-pilot should use this
Intermodal supply chains (road + rail legs), comparing truck vs train lead times, bike or walking couriers next to vans, evacuation on foot next to vehicles. Rail yards and track occupancy need the Rail Library instead (`videos/gis-shapefile-to-rail-markup.md`); placing sites on the map: `videos/gis-agent-placement-from-table.md`.
