# Pattern card — Bus Routing
- **Source:** AnyLogic example model "Bus Routing" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** Send vehicles along a fixed line — an ordered list of stops — while forcing or forbidding particular roads on each leg (a scheduled route, a detour around a closure), with one reusable block.

## Block chain
Main: `CarSource` (a bus every minute, length 15 m, 40 km/h) → **`BusRoute`** (custom block) → `CarMoveTo` (end of the line road) → `CarDispose`.
Inside the `BusRoute` agent type (used as a flowchart block, ports in/out): `CarMoveTo` *busNextStop* → `Delay` (15 s dwell) → `SelectOutput` (`agent.routeIndex >= route.length` → leave the block; otherwise loop back to *busNextStop*).
- *busNextStop*: moves to a **bus stop** `route[car.routeIndex]`, *Include roads* `includeRoads[car.routeIndex]`, *Avoid roads* `avoidRoads[car.routeIndex]`; its *On exit* does `car.routeIndex++`.
- The `Bus` type carries `routeIndex` (starts at 0) — the progress along the line travels with the vehicle.
- Block parameters in Main: `route = {busStop, busStop1, busStop2}`; `includeRoads = {{road, road2}, {road2, road7, road3, road8}, {road8, road4}}`; `avoidRoads = {{}, {road6}, {road3}}` — one row per leg.

## Resources
Bus stops are markup elements; no resource pools.

## Key settings worth copying
- CarMoveTo *Include roads* (Java `throughRoads`) and *Avoid roads* (`avoidRoads`), both `Road[]`, added in **8.9.4** (release notes). Included roads are used **in the given order**, so that sequence must be drivable (Help).
- A 2-D array parameter (`Road[][]`) gives each leg its own list; `{ }` means no constraint on that leg.
- Bus-stop behaviour (Help *CarMoveTo*, *Bus stop*): the car reserves a place when it approaches; if the stop is full it waits **on the road next to it** until a place frees; once in, it exits CarMoveTo and stays until the next CarMoveTo or disposal — so the `Delay` right after is the dwell time. Stop length (default 20 m) sets how many buses fit (`nCars()`, `getCars()`).

## KPIs instrumented
None. Natural additions: time per leg (stamp on exit of *busNextStop*), dwell and bunching at each stop (`busStop.nCars()`), headway at the last stop.

## Pitfalls
- `route`, `includeRoads` and `avoidRoads` must have the same length — the index is shared.
- An impossible include/avoid combination sends the bus out through `outWayNotFound`; the demo leaves that port unconnected. Connect it to a fallback and count it.
- A bus waiting for a full stop stands on the road, so it should hold the traffic behind it in that lane *(inferred from Help)* — realistic, but it inflates car travel times near busy stops.
- Before 8.9.4 there are no include/avoid lists: chain one CarMoveTo per intermediate road instead.
- Reset `routeIndex` if a vehicle is to run the line again.

## Reusable idea
A route is data: an ordered stop list plus per-leg road constraints, stored as block parameters, with a counter on the vehicle and a CarMoveTo in a loop. Several lines reuse the same `BusRoute` type with different arrays; detours are a one-row edit.

## When the co-pilot should use this
Public transport lines, shuttle loops, delivery rounds with fixed stops, road-closure and detour scenarios. Related: `carmoveto.md` (destinations, ports, lane policy), `displaying-traffic-jams.md`.
