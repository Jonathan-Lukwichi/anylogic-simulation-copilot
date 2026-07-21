# Pattern card — City Square
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model multi-directional vehicle flow through a mixed signalized/unsignalized urban intersection to expose throughput bottlenecks and lane-conflict points.

## Block chain
Five independent vehicle streams (cars, buses, trucks) each start at a CarSource configured with a fixed constant arrival rate. Each stream immediately issues a CarMoveTo that navigates the vehicle along road-network paths into the square. At decision points inside the square, SelectOutput and SelectOutput5 blocks split traffic probabilistically across exit corridors (NW, NE, SW, SE, North-Center). Every exit corridor ends in a CarMoveTo that steers the vehicle out of the square followed by a CarDispose that removes it. The Road Traffic Library handles physical realism — lane assignment, intersection priority rules, and signal phases — without requiring explicit queue or service blocks; contention emerges from the road geometry itself.

## Resources
No explicit ResourcePool or Seize/Release blocks. Road capacity and signal timing embedded in the road network markup; lane capacity is implicitly constrained by vehicle speed and road width defined in the GIS layer.

## Key settings worth copying
- Arrival discipline: constant rate (not stochastic) — isolates intersection geometry as the sole source of variation
- Time unit: Second — necessary for realistic speed/acceleration physics in Road Traffic Library
- Five named CarSource objects (one per entry direction) enable independent rate tuning per approach
- SelectOutput5 (5-port probabilistic split) used where more than two exit options exist; standard SelectOutput used for binary splits
- Vehicle mix (cars / buses / trucks) differentiated by agent type to capture heterogeneous speed and size effects

## KPIs instrumented
- Throughput per exit corridor (vehicles/minute derived from CarDispose counts)
- Travel time through the square (time from CarSource to CarDispose)
- Queue length on approach roads (observable from Road Traffic Library statistics)
- Intersection utilisation implied by vehicle density animations

## Reusable idea
Use a constant-rate multi-source pattern (one CarSource per entry) combined with probabilistic SelectOutput routing to stress-test an intersection layout before committing to signal timing or lane configuration — stochasticity in the arrival process is deliberately removed so that geometric and control-policy effects are cleanly measurable.
