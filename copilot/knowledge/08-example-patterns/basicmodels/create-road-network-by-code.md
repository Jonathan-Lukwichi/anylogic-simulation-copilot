# Pattern card — Create Road Network by Code
- **Source:** AnyLogic example model "Create Road Network by Code" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** Generate a road network — roads, an intersection with its lane connections, a stop line, a bus stop and a parking lot — from code at start-up, e.g. from coordinates held in data.

## Block chain
Markup is built in Main's *On startup*; the flowchart only refers to Main variables typed `Road`, `ParkingLot`, `BusStop`, `RoadNetwork`.
- Cars: `CarSource` (west road, max 5 cars, 30 km/h) → `SelectOutput` (park if `randomTrue(0.05) && parkingLot.nFree() > 0`) → `CarMoveTo` *parking lot* → `Delay` (triangular 5 / 7 / 10 min) → `SelectOutput5` (50/50: east or south road) → `CarDispose`. The parking CarMoveTo's `outWayNotFound` also leads to the SelectOutput5. A mirror flow starts on the east road's backward lanes.
- Buses: `CarSource` every 7 min → `CarMoveTo` *bus stop* → `CarMoveTo` east road → `CarDispose`.

## Resources
n/a

## Key settings worth copying (Help 8.9.10, *Create road network by code*)
1. **Roads:** `new Road()`, `setOwner(this)` (every markup element needs its owner), `setForwardLanesCount(2)`, `setBackwardLanesCount(2)`, geometry by `addSegment(new MarkupSegmentLine(x1, y1, z1, x2, y2, z2))`. Leave a gap where the intersection will sit.
2. **Intersection:** `addRoad(road, PathEndType.END or BEGIN)` — the end of the road that touches the junction, which depends on the direction the road was drawn. Then one `addConnection(inRoad, inLane, outRoad, outLane)` per allowed movement: for the first road only lanes *entering* the junction are counted, for the second only lanes *leaving* it, indices from 0. A connection from a road to itself is a U-turn.
3. **Stop line / bus stop / parking lot:** `setRoad`, `setOnForwardSide`, `setOffset` (pixels from the road start); stop line `setLaneIndexFrom/To` and `addSpeedLimitSign(10, SpeedUnits.KPH)`; bus stop `setLength(40, METER)`; parking lot `setParkingType(PARKING_LOT_PARALLEL)`, space length and width, `setNSpaces(5)`.
4. **Network:** `new RoadNetwork(this, "roadNetwork", SHAPE_DRAW_2D3D)`, `setDrivingDirection(ROAD_RIGHT_HAND)` and any other network property **before** `addAll(...)` of every element.
5. **Level:** `new Level(this, "myLevel", SHAPE_DRAW_2D3D, 0)`, `add(network)`, `initialize()` — the last step.
6. **Presentation:** `presentation.insert(0, shape)` per element, or in bulk from `level.getRoadNetworks().get(0).getRoads()` (likewise `getParkingLots()`, …).

## KPIs instrumented
n/a

## Pitfalls
- **Frozen after `initialize()`.** A road network created by code cannot be changed at runtime (Help); build every element and connection first.
- **Lane indices are the usual failure.** Wrong in/out indices, or a movement never connected, gives cars that cannot find a way — they leave CarMoveTo through `outWayNotFound` (or stop the run if that port is not handled). Test every turn once; indices also flip with left-hand traffic.
- **Mixed units:** coordinates and `setOffset` are pixels (check the scale); lengths and widths take a unit argument.
- Elements not inserted into `presentation` are not drawn.
- Guard parking with `nFree() > 0` and wire `outWayNotFound` — a full lot can also raise an error (see `carmoveto.md`).

## Reusable idea
Treat the network as data: keep node coordinates, lane counts and allowed turns in a table, and loop over it in *On startup* with the same six steps. For generating markup at **design time** instead (editable afterwards, Professional/University editions), see `videos/layout-candidates-and-design-time-api.md`.

## When the co-pilot should use this
Traffic studies where the junction layout comes from GIS or CAD data or must be varied between scenarios; when a user asks how `addConnection` lane indices work. Related: `create-transporter-network-by-code.md`, `create-conveyor-network-by-code.md`, `create-gis-network-by-code.md`.
