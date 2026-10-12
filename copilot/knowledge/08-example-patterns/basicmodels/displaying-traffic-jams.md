# Pattern card — Displaying Traffic Jams
- **Source:** AnyLogic example model "Displaying Traffic Jams" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** See where a road network congests, and get one place to hook network-wide measurements, using the RoadNetworkDescriptor block.

## Block chain
Four `CarSource` blocks (north, east, south, west; random lanes) → one `SelectOutput5` (four equal exits) → four `CarMoveTo` (to the far end of each road, backward lane where needed) → `CarDispose`.
A **`RoadNetworkDescriptor`**, connected to nothing, points at `roadNetwork` with *Road section length* 10 m and *Enable density map* ticked.

## Resources
n/a

## Key settings worth copying (Help 8.9.10, *RoadNetworkDescriptor*, *Displaying traffic jams*)
- **What the map shows:** roads are cut into sections of `roadSectionLength` (default 50 m, minimum 1 m); each section is coloured by the **average car speed** on it — green at or above `greenSpeedLevel` (default 60 km/h), red at or below `redSpeedLevel` (default 10 km/h, must stay below green); the one-argument setters take km/h (gotcha G61). `densityMapTransparency` (default 0.6) and `set_enableDensityMap(...)` at runtime.
- **Network-wide hooks** (one place instead of every block): *On enter / exit network*, *On enter / exit road* (`road`, `isRoadForward`), *On enter / exit intersection*, *On lane change*, *On stop*, *On resume moving*, *On car clicked*. Functions `size()` and `getCar(i)`.
- **Automatically resolve deadlocks** (`automaticallyResolveDeadlocks`, **default true**): when cars block each other for good, AnyLogic lets them temporarily pass through each other.
- Since 8.9.9 the density map also covers transporters on paths, conveyor-guided agents and trains, and has `isShown()` (release notes).

## KPIs instrumented
Only the colour map. Easy additions through the hooks: stop count (`carStopsCounter++` in *On stop*, as the City Square and Roundabout examples do), network travel time (stamp in *On enter network*, record in *On exit network*), flow per road (*On enter road*).

## Pitfalls
- **Red means slow, not crowded.** The map encodes speed, so a normal queue at a red light shows red; compare against a signal cycle before calling it a jam.
- **Hidden gridlock.** With deadlock resolution on, cars ghost through each other and throughput stays plausible where the real network would lock up. When congestion is the question, run once with it off, or log long stops via *On stop* / *On resume moving*, and report any resolution.
- Short sections (10 m here) give a finer map but more bookkeeping; match the section length to the question (signal queues vs corridor speeds).
- Help contradicts itself on transparency: *Displaying traffic jams* says 0 = fully transparent, the block reference says 0 = opaque. Test the value you set.

## Reusable idea
Put one descriptor on every road network: it is the natural place for network-level KPIs and the congestion map, and it keeps measurement code out of the routing flowchart.

## When the co-pilot should use this
Any Road Traffic Library model — for congestion pictures, travel-time and stop statistics, and before trusting throughput from a saturated network. Related: `carmoveto.md`, `bus-routing.md`, `videos/traffic-light-gated-pedestrian-crossing.md`.
