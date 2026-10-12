# Pattern card — GIS road routing: where routes come from, caching and offline runs, and the silent straight-line fallback
- **Source:** AnyLogic 8.9.10 Help tutorial "Supply Chain GIS (Agents)" — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Make vehicles on a GIS map travel real roads the same way on every machine (online, offline, Cloud), and notice when AnyLogic quietly replaces a road route with a straight line.

## Mechanism
- **The tutorial model.** One distributor on a GIS Point, 14 retailers placed by name search (trap G51), 15 trucks with an `AtDistributor → MovingToRetailer → MovingToDistributor` statechart. Each retailer's Rate event (1/day) creates `new ProductOrder(uniform_discr(10,20), this)` and sends it to the idle truck nearest by road. The dispatch weaknesses are covered elsewhere: `null` when every truck is busy, lost orders with no backlog, and same-instant double booking. See Related.
- **Where a GIS trip gets its path.** GIS map → *Routing* (Help 8.9.10, *GIS map*):

  | *Routes are* | Path source | Options |
  |---|---|---|
  | Requested from OSM server | online routing server (choose one) | *Routing method* Shortest / Fastest; *Road type* Road, Rail, Bike, Foot |
  | Loaded from PBF file | local graph built by the routing-graph wizard from a `.pbf` / `.osm` file | Pathfinding: bidirectional A* or bidirectional Dijkstra; Shortest / Fastest |
  | Straight lines | none | — |

  The tutorial's map (8.9.10 `.alp`) uses the online AnyLogic server, car, Fastest.
- **Off-network legs** (Help, *Movement in GIS space*):
  - A start point off the network: the agent first goes to the nearest point on the network, then follows it.
  - A destination the network does not reach: the agent drives to the network point closest to it, then the last leg in a line.
  - Drawn GIS Routes are used by `moveTo(gisPoint)` in place of downloaded routes.
  - Movers that need different networks (rail vs road) each get a *Route provider* element (Help, *Alternative route providers*).
- **Caching.** Tiles and routes fetched during a run are saved in the model folder, so later runs are faster (tutorial; Help *GIS map*, *Defining routes*). A fully offline model needs both parts stored with it: cached tiles and routing data, i.e. a PBF graph (Help *Taking GIS models offline*).
- **If route not found** (Help; not offered for Straight lines):
  - *Create straight route*: approximate the trip with a line and keep running.
  - *Show error dialog*: stop and report.

  In the 8.9.10 example models, 21 of 23 routing settings (GIS maps and Route provider elements) use *Create straight route*, the tutorial's map among them. It is probably the editor default *(inferred from the examples)*.

## Resources
n/a. Vehicles are an ordinary population; for pooled-fleet statistics see `models/product-delivery.md`.

## Key settings worth copying
- **Choosing by road:**
  - `getNearestAgentByRoute(filter(main.vehicles, v -> v.inState(Vehicle.AtDistributor)))`: route-provider distance.
  - `getNearestAgent(...)`: straight line, the GIS analogue of G44.
  - Both skip the caller and return `null` for an empty collection (Help, *Agent API*).
  - `distanceByRoute(other)` gives the road distance itself.
- **Moving without roads** (helicopters, drones, a contracted transit time):
  - `moveToStraight(agent)` ignores network and routes (Help, *Agent API*). The coordinate overloads do too, but the Help's notes for the (x, y) form disagree on which argument is latitude in GIS space; test it on a known point.
  - `moveToInTime(dest, t, HOUR)` fixes the trip time.
  - `moveToNearestAgent(collection)` starts a trip to the closest member (the metric is not stated in Help).
- **GIS units differ from continuous space** (Help, *Agent API*, *Movement in GIS space*):
  - `getX()` / `getY()` return latitude / longitude in degrees.
  - `distanceTo(agent)` returns metres.
  - `getSpeed()` returns m/s.
  - Probe trips with `timeToArrival()`, `isMoving()`, `getTargetLat()` and `getTargetLon()`.
- **Local-graph limits** (Help, *Routing options*, GraphHopper): car-fastest yes, car-shortest no. No turn restrictions, vehicle height or weight limits, manual speeds, avoid-areas or live traffic. Hills and ferries are handled. Local routes are free-flow estimates.

## KPIs instrumented
- Per trip: departure and arrival `time()`, plus `distanceByRoute(dest)` at dispatch.
- **Fallback check** *(suggested)*: on a long leg, a road distance within about 2 % of `distanceTo(dest)` suggests a straight-line substitute. Count these per run.

## Pitfalls
- **Silent straight lines.** A destination with no road link (an island, a point placed at sea by a bad geocode, G51) gets a straight trip, so trips come out shorter and the fleet looks big enough. Whether an unreachable server also triggers the fallback is *(unverified)*.
- **Online routes are live data.** The first run needs internet and is slow. Results may shift if the server's map changes *(inferred)*. Freeze routes with a PBF graph for any published or replicated study (the same rule as G17's frozen inputs).
- **Cloud and standalone deliveries.** Whether Cloud runs reach the routing and search servers is *(unverified)*. Ship a PBF graph and coordinate placement.
- **Cost of choosing by road.** Nearest-by-route has to route to every candidate *(inferred)*. Filter first (idle only, or the k closest by straight line).
- **Ported continuous-space code** that treats `getX()` as pixels or distances as model units fails silently in GIS space.

## Reusable idea
Treat the road network as an input table:
1. record its source, method, road type and no-route behaviour in the spec;
2. verify with errors switched on;
3. run experiments on a frozen local graph.

## When the co-pilot should use this
- Any GIS model with moving vehicles: delivery, field service, emergency response, supply-chain transport.
- Before promising an offline, standalone or Cloud deliverable.
- When travel times look too short, differ between machines, or vehicles cut across country.
- When road, rail and air movers are mixed.
- Related:
  - `videos/gis-agent-placement-from-table.md` (G51)
  - `videos/dispatch-idle-check-then-send-double-booking.md`
  - `models/product-delivery.md`
  - `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`
  - `models/field-service.md`
