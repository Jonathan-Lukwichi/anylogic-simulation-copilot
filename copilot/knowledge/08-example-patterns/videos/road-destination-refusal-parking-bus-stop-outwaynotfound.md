# Pattern card — Road destinations that can refuse a car: full parking lots, occupied bus stops and `outWayNotFound`
- **Source:** AnyLogic 8.9.10 Help tutorial "Intersection (Road Traffic Library)" — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Send some cars to a roadside parking lot and buses to a stop without the run crashing, or the lane silently blocking, when the destination has no room.

## Block chain
- Parking share: `CarSource` → `SelectOutput` (10 % to parking) → `CarMoveTo` (*Moves to*: Parking lot) → `Delay`
  (parking time `triangular(5, 15, 45)` min, capacity 5 = spaces) → `CarMoveTo` (onward road) → `CarDispose`.
  The lower port **`outWayNotFound`** of the parking `CarMoveTo` is wired to the onward `CarMoveTo`: a car that cannot
  park simply drives on.
- Buses: a second `CarSource` (20 per hour, car length 10 m, initial speed 40 km/h, custom `Bus` type) → `CarMoveTo`
  (*Moves to*: Bus stop) → `Delay` (dwell `triangular(15, 30, 90)` s) → `CarMoveTo` (onward).

## Resources
Parking Lot markup (5 spaces) and Bus Stop markup beside the road. No resource pools: space on the markup is the capacity.

## Key settings worth copying
- **Always wire `outWayNotFound`.** Per the 8.9.10 Help (*CarMoveTo*), a car sent to a lot reserves a space only as it
  approaches, and leaves through `outWayNotFound` if none is free. The same Help page also says, under *Parking lot*,
  that an error is generated when the lot is full. The tutorial's model stopped with an error in virtual time until
  the port was wired. Treat an unwired `outWayNotFound` as a crash waiting to happen.
- The port also catches cars that have **no route** to the destination (road, stop line, bus stop or lot in the same
  network). The *On way not found* action runs for them; count them there.
- **A pre-check helps but is not enough.** `parkingLot.nFree() > 0` at the decision point avoids most refusals. Because
  the reservation happens on approach, two cars can still aim for the last space, so keep the port wired as well.
- **Dormant condition in the shipped model.** *Road Traffic Tutorial - Phase 6* (8.9.10) holds the SelectOutput
  condition `randomTrue(0.10) && parkingLot.nFree() > 0`, but it leaves the block in its default probability mode
  (Help: `conditionIsProbabilistic` = true), so that condition never runs. If you switch to condition mode, also tick
  *Condition is stochastic or volatile*, because `randomTrue` differs between the two evaluations (G6).
- Parking Lot (Help 8.9.10): *Parallel*, *Perpendicular* or *Diagonal*; 5 spaces of 6 m by default; one row only (draw
  another road for a second row); space width = the network's lane width (3.5 m default). API: `nFree()`,
  `getFreeSpaceIndexes()`, `randomFreeSpaceIndex()`. The Help recommends following the `CarMoveTo` with a `Delay` with
  *Maximum capacity* ticked.

## KPIs instrumented
Not in the tutorial. Add: refused cars (counter in *On way not found*), lot occupancy over time (`nFree()` in a time
plot), and bus dwell plus the queue that builds behind a waiting bus.

## Pitfalls
- **A bus that finds its stop occupied waits in the traffic lane** next to the stop (Help *CarMoveTo*), blocking cars
  behind it. The stop's length (20 m by default) sets how many vehicles fit at once *(inferred from "reserve a place")*.
- **Mean ≠ middle value.** The parking time averages 21.7 min and the bus dwell 45 s, not 15 min and 30 s (G55).
- Connect only the side ports when chaining blocks; the lower port of `CarMoveTo` is the refusal exit, not a second output.

## Reusable idea
Any destination that can say "no" (lot, stop, bay, dock) needs a wired exit for "no" and a counter on it. The refusal
count is a result, not an error.

## When the co-pilot should use this
- Road Traffic models with parking search, kiss-and-ride, taxi or bus stands, loading bays or delivery stops.
- Symptoms: the run stops when a lot fills, cars vanish from the statistics, or buses cause unexplained jams.
- Related: G6, G55; `videos/road-network-descriptor-callbacks-speed-map-deadlocks.md`; `models/traffic-light-phases-optimization.md`.
