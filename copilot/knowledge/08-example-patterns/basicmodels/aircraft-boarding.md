# Pattern card — Aircraft Boarding
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Pedestrian Library — agent-based pedestrian flow)
- **Problem it solves:** Measure how long it takes a full plane-load of passengers to board an aircraft, accounting for aisle congestion, luggage stowing, and seat-finding behaviour.

## Block chain
PedSource (passengers arrive at gate) -> PedGoTo (walk to aircraft entrance) -> PedWait (queue / aisle congestion at entry) -> PedGoTo (walk down aisle to assigned row) -> PedWait (stow luggage overhead — conditional delay) -> PedGoTo (move to assigned seat pixel) -> PedWait (settle into seat — short random delay) — boarding complete when all Passenger agents are seated.

A second PedSource / PedWait pair handles the pre-boarding waiting area (gate hold) before the door opens.

## Resources
- **Passenger agent type** — custom agent class carrying attributes: seat assignment (row/column), `hasLuggage` boolean, and a `seatPixel` target coordinate derived from the aircraft floor-plan image.
- No explicit ResourcePool blocks; the aisle itself acts as the capacity constraint — pedestrian physics (social-force model) naturally creates queuing when agents block each other.
- Aircraft layout overlaid on a Boeing 757-200 floor-plan image used as the spatial environment.

## Key settings worth copying
- **Luggage stow time:** `uniform(15, 30)` seconds — applied only when `ped.hasLuggage` is true; zero otherwise. Lets you quickly test "carry-on-free" boarding policies.
- **Seat-settling time:** `uniform(5, 15)` seconds — small randomness to avoid perfectly synchronised movements.
- **Arrival rate:** controlled via a `rate` / `rateSchedule` / `rateExpression` trio on PedSource, making it easy to switch between constant-rate and schedule-driven boarding calls (e.g., board by zone).
- **Time unit:** Seconds — natural for human-motion studies; avoids unit-conversion errors in the uniform() calls.
- Boarding order (back-to-front, window-to-aisle, random) is encoded in the order passengers are released from the gate PedWait, not in a separate router block.

## KPIs instrumented
- **Total boarding time** — wall-clock seconds from first passenger entering to last passenger seated.
- **Aisle congestion** — implicitly visible in the 2-D animation; pedestrian density shows bottleneck rows.
- (No explicit throughput or cost statistics objects in this introductory model — extend with a time-plot or statistics collector as needed.)

## Reusable idea
Use a pedestrian agent's custom attribute (e.g., `hasLuggage`) to switch a PedWait delay between zero and a random duration — this is the simplest way to model heterogeneous service times at a spatial waypoint without adding extra conditional routing blocks, and the same pattern applies to any scenario where only a subset of agents need extra processing at a location (security lanes, check-in desks, hospital triage).
