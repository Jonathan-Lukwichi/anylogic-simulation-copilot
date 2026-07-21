# Pattern card — Interconnected Call Centers
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a network of regional call centers that overflow calls to neighbours when their own queue is full, measuring balk rates and operator/link utilisation.

## Block chain
Each CallCenter agent encapsulates its own process flow: a Source generates inbound calls at an exponential inter-arrival rate derived from a per-center `callsPerHour` parameter. Calls enter a bounded queue; if the queue is not full a Seize grabs an available operator and a Service block handles the call for a duration drawn from `uniform(callDurationMean/skillLevel*2, callDurationMean/skillLevel*3)`. After service a SelectOutput checks whether the caller originated here or was transferred in, then routes to the appropriate Release/Exit path.

When a call arrives and the queue is already at capacity, a routing function (`routeOut`) inspects peer centers via a Link network. It searches for a neighbour whose queue has room AND whose connecting Link (a constrained channel with its own `lines` capacity) is not fully occupied. If such a neighbour exists the call is forwarded via Exit→Enter across the link; otherwise it is discarded through a `routeBalk` Sink. The number of call centers is a top-level parameter, and links between every pair are stored in a triangular list so any two centers can be queried in O(1).

## Resources
- **Operators:** one ResourcePool per CallCenter; capacity initialised to `uniform_discr(5, 25)` at model start.
- **Transfer lines (Links):** each Link holds a ResourcePool of trunk lines; capacity drawn from `uniform_discr(0, 3)` at creation. Lines must be seized before a call is forwarded and released on delivery.

## Key settings worth copying
| Setting | Value / expression |
|---|---|
| Call arrival inter-arrival | `exponential(callsPerHour / 60.0)` (minutes) |
| Calls per hour per center | `uniform_discr(100, 500)` |
| Operator count per center | `(int)uniform(5, 25)` |
| Queue capacity per center | `uniform(1, 5)` (slider-adjustable at runtime) |
| Call service time | `uniform(callDurationMean/skillLevel*2, callDurationMean/skillLevel*3)` |
| Trunk lines per link | `uniform_discr(0, 3)` |
| Time unit | Minute |

All parameters are adjustable via sliders during the run with immediate visual feedback.

## KPIs instrumented
- **Operator utilisation** per center (gauge, colour-coded green→red at 0.2/0.4/0.6/0.8 thresholds)
- **Link (trunk line) utilisation** per pair of centers
- **Calls balked** count (calls discarded when no overflow path is available)
- Queue size vs capacity (runtime slider shows current load)

## Reusable idea
The key transferable trick is the **two-gate overflow check**: before forwarding a call the model simultaneously tests (a) the destination queue has space AND (b) the connecting link has an idle trunk line — both conditions must hold. This prevents overflow from creating a second bottleneck on the transfer channel itself, and the same pattern applies to any network where both the node capacity and the edge capacity are limited (e.g., hospital patient transfers constrained by ambulance availability, or warehouse order handoffs constrained by conveyor slots).
