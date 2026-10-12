# Pattern card — Create GIS Network by Code
- **Source:** AnyLogic example model "Create GIS Network by Code" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM / GIS movement
- **Problem it solves:** Add your own routes to a GIS map at start-up — points, a multi-segment route and the network that holds them — so agents travel along a corridor that the map's road/rail data does not provide (a planned rail line, a shipping lane, a pipeline).

## Structure
Main has a GIS `map` and one embedded agent `train`. *On startup* calls `createRoute()` and then `train_presentation.bringAnimationToFront()`. `createRoute()`:
1. three `GISPoint(map, latitude, longitude)` objects, each followed by `initialize()`;
2. two `GISMarkupSegmentLine(lat1, lon1, lat2, lon2)` segments, added in order from the route start to a `Curve`, then `curve.initialize()`;
3. `new GISRoute(map, curve, startPoint, endPoint, true)` (true = bidirectional), then `initialize()`;
4. `new GISNetwork(map, "n", true, point1, point2, point3, route)` — the network takes its elements directly (visible = true);
5. `train.jumpTo(point1)` and `train.moveTo(point3)`.

## Resources
n/a

## Key settings worth copying (Help 8.9.10, *Create GIS network by code*)
- Order: points → initialize each → segments → curve → `curve.initialize()` → route → `route.initialize()` → network. Unlike the space-markup recipes there is no Level.
- `GISMarkupSegmentLine` accepts a fifth argument `isGeodesic`: true (the default) animates movement along the geodesic; false along a straight line on the map.
- Coordinates are latitude first, then longitude, in decimal degrees.

## KPIs instrumented
n/a

## Pitfalls
- **Cannot be changed later.** A network created by code cannot be modified during the run (Help); create every route at start-up.
- **Which routing wins.** The demo's map still has the web route service selected (transport type rail); the train follows the code-built route because it starts on a network point and is sent to another one. Help only says that markup networks influence GIS movement — test that your agents really take your route (compare the travelled distance with the route length) *(precedence rule unverified)*.
- Swapped latitude/longitude silently puts points elsewhere on the globe (compare G51).
- Long geodesic segments bow on the flat map; use `isGeodesic = false` if the drawn corridor must be straight.

## Reusable idea
Keep corridors as coordinate lists (from a CSV or shapefile export) and turn them into GIS routes at start-up; one routine can build many routes and one network. For converting whole shapefiles to rail markup in the editor instead, see `videos/gis-shapefile-to-rail-markup.md`.

## When the co-pilot should use this
Supply-chain or transport models on a GIS map that need planned or private routes, or routes when no routing server is available. Related: `videos/gis-agent-placement-from-table.md`, `create-road-network-by-code.md`.
