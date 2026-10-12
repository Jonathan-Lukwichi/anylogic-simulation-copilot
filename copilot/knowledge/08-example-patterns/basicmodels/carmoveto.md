# Pattern card — CarMoveTo
- **Source:** AnyLogic example model "CarMoveTo" (basicmodels), AnyLogic 8.9.10 — distilled, original wording; also covers the sister demos "CarSource", "CarEnter and CarExit" and "Bus Stop"
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** Know exactly what each car-flow block does at its destination and when things go wrong — the semantics behind parking, bus stops, stop lines, lanes and leaving the road network.

## Block chain
- **CarMoveTo demo:** cars (500/h) → `SelectOutput` → either the far end of another road, or a **parking lot** → `Delay` (parked time) → back along the backward lane → `CarDispose`. Buses (200/h, 10 m, 40 km/h) → `SelectOutput` (30 %) → a **bus stop** → `Delay` (dwell) → onward; or a **stop line** (*Stop before stop line*) → onward. The `outWayNotFound` ports of the parking and stop-line moves also lead onward.
- **CarSource demo:** two-way road; one source on the forward lanes with a lane index expression (`randomTrue(0.5) ? 1 : 2`, *random lane* off), one on the backward lanes (`BACKWARD_LANE`) sent to `END_OF_BACKWARD_LANE`.
- **CarEnter and CarExit demo:** `CarMoveTo` → **`CarExit`** (car leaves the road network into a plain PML flow) → **`CarEnter`** onto the backward road → `CarMoveTo` → `CarDispose`.
- **Bus Stop demo:** `CarMoveTo` to the stop → `Delay` uniform(5, 10) s → `CarMoveTo` onward, with through traffic in both directions.

## Resources
n/a — parking spaces and bus-stop places are markup capacity.

## Key settings worth copying (Help 8.9.10)
- **Destinations** (`movesTo`): road (`END_OF_FORWARD_LANE` / `END_OF_BACKWARD_LANE`), parking lot, bus stop, stop line; they must belong to the car's current road network.
- **Parking lot / bus stop:** a place is reserved only on approach; the car parks, exits CarMoveTo and **stays** until another CarMoveTo or disposal — the following `Delay` is the parked or dwell time. A full bus stop makes the car wait on the road beside it. Since 8.9.3: diagonal parking, *Forced exit on timeout*, a parking-space selection policy in CarMoveTo, `getParkingSpaceIndex()`.
- **`outWayNotFound`:** taken when no route exists to the destination.
- **Lanes (8.9.7+):** CarSource/CarEnter *Lane selection policy* — random (default), closest to median, closest to roadside (with a number of lanes), or specified explicitly (lane index). The policy is inherited by later blocks unless a CarMoveTo ticks *Change lane selection policy*; a lane set through the car API (`setPreferredLane`) overrides it until the given offset or the block's end.
- **Entry:** CarSource and CarEnter place a car only when there is enough free distance ahead (more at higher initial speed); cars that cannot enter wait in the block's internal queue. In a parking lot they take a random free space.
- **CarExit / CarEnter:** model part of a trip abstractly (a long stretch, a car wash, a ferry) as PML blocks between them; a car entered by CarEnter starts moving only when a CarMoveTo sends it.

## KPIs instrumented
None; see `displaying-traffic-jams.md` for network-wide hooks.

## Pitfalls
- **Full parking lot.** CarSource/CarEnter into a full lot raises an error; for CarMoveTo, Help says both "leaves via `outWayNotFound`" and "an error is generated". Guard with `parkingLot.nFree() > 0` in a routing condition (as *Create Road Network by Code* does) **and** connect `outWayNotFound`.
- **Hidden entry queues.** A saturated first lane delays arrivals inside CarSource without any visible queue; count cars in *On enter network* of a RoadNetworkDescriptor and compare with the intended demand before trusting results.
- **An explicit lane is inherited downstream,** so the car keeps to it; add a CarMoveTo (or CarEnter) with *Random lane* where it may change lanes again (Help *CarSource*).
- Lane indices start at 0 and count per direction; a backward-lane source on a one-way road is an error.

## Reusable idea
Treat every destination as a reservation with an explicit failure path: check capacity before routing (`nFree()`), wire `outWayNotFound`, and model dwell as a PML `Delay` after arrival. Use CarExit/CarEnter to abstract parts of a trip that need no traffic detail.

## When the co-pilot should use this
Car-park, drop-off, bus-stop, toll or junction models; debugging cars that vanish, stop or raise errors at parking lots; lane-choice questions. Related: `bus-routing.md`, `create-road-network-by-code.md`, `videos/traffic-light-gated-pedestrian-crossing.md`.
