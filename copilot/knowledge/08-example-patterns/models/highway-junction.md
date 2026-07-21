# Pattern card — Highway Junction
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models multi-entry highway merges to show how a periodic bottleneck at one exit propagates backwards as a traffic jam across the whole junction.

## Block chain
Multiple CarSource blocks inject vehicles onto separate highway entry ramps at steady constant rates. Each car agent is then routed through a sequence of CarMoveTo blocks that represent road segments and lane changes on the modelled road network. At the merge/junction point a SelectOutput block distributes cars toward their respective exits. One of those exits — the Gardena freeway exit — is set up with periodic congestion events: at regular intervals the exit capacity is artificially restricted, causing vehicles to queue up on the road upstream and spill back into the main carriageway, creating a realistic jam that then clears when the congestion window ends. Vehicles that successfully pass through exit into CarDispose blocks and leave the system.

## Resources
n/a — no staff or machine pools; the capacity constraint is the road network geometry and the periodic exit blockage at Gardena.

## Key settings worth copying
- Time unit: **seconds** (fine-grained enough to capture vehicle-by-vehicle dynamics)
- Arrival pattern: **constant rate** per entry ramp (no randomness in arrivals — isolates the effect of the bottleneck)
- Congestion trigger: **periodic schedule** tied to named road-segment endpoints (`GardenaFwyEStart` / `GardenaFwyEEnd`) — toggled on/off to simulate recurring real-world bottlenecks (e.g., ramp metering, signal failure, incidents)
- Routing: `SelectOutput` with `exitNumber` condition — probabilistic or rule-based exit choice per car

## KPIs instrumented
- Queue length / jam extent upstream of the Gardena exit during congestion windows
- Throughput (cars disposed per time unit) across each exit
- Travel time from entry ramp to disposal (derived from simulation clock difference)

## Reusable idea
**Scheduled capacity collapse as a congestion source.** Instead of randomising arrivals to generate queues, hold arrivals constant and periodically choke a downstream segment. This isolates the bottleneck effect cleanly and makes it straightforward to test mitigation strategies (e.g., ramp metering, diversion routing via SelectOutput logic) without confounding arrival variability.
