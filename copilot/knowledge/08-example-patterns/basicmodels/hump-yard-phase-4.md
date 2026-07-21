# Pattern card — Hump Yard - Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates the full operational sequence of a rail hump yard where incoming trains are broken apart, individual cars are sorted by destination, and outbound trains are reassembled — capturing the multi-stage decouple/move/couple choreography in a single model.

## Block chain
Inbound trains arrive via TrainSource at a fixed interarrival interval and enter the yard on a dedicated entry track. A series of TrainMoveTo blocks navigate each train to the hump lead. TrainDecouple blocks split the consist car by car (or in cuts); SelectOutput blocks route individual cars to classification tracks based on destination. Short Delay blocks represent dwell time while cars roll down the hump or wait in a bowl track. On the departure side, TrainCouple blocks reassemble cars into new outbound trains, which then move via additional TrainMoveTo steps to departure tracks and exit through TrainDispose.

## Resources
- No explicit ResourcePool agents; track occupancy is the implicit capacity constraint.
- Two TrainSource instances generate inbound trains (one per entry lead).
- Delay blocks set to 15 seconds model the coupling/uncoupling dwell time.
- Train agent population (class Train) carries per-car destination attributes used for routing decisions.

## Key settings worth copying
- **Interarrival time:** 15 minutes (fixed, deterministic) — straightforward to swap for exponential(15) to add variability.
- **Time unit:** Minutes at model level; individual delay parameters expressed in seconds (unit conversion handled automatically).
- **Hump dwell Delay:** 15 seconds per cut — tune this to match actual retarder/bowl timing.
- **SelectOutput routing:** condition-based (car destination attribute) rather than probabilistic — keeps logic explicit and auditable.
- **TrainSource locationType:** LOCATION_TRACK_OFFSET with a named stop line, making spawn position easy to reposition by moving the stop-line marker.

## KPIs instrumented
- Throughput of outbound trains assembled per shift (count at TrainDispose).
- Bowl track content (number of cars waiting in each classification track).
- Cycle time per car from entry to departure train assembly.
- Delay block statistics expose average and maximum dwell times at each stage.

## Reusable idea
The core transferable trick is the decouple-route-recouple pattern: use TrainDecouple to atomize a multi-unit consist into individual cars, route each car independently through SelectOutput logic, let cars accumulate in staging Delays until a full cut is ready, then fire TrainCouple to rebuild a new consist. This same pattern applies to any domain where composite entities must be disassembled, individually processed, and then re-aggregated (e.g., pallet break-bulk in warehousing, batch splitting in pharma manufacturing).
