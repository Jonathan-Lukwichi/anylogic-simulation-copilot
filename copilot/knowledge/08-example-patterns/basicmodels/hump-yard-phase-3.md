# Pattern card — Hump Yard - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a railway hump yard where inbound trains are decoupled car-by-car, cars are sorted by destination track, and outbound trains are assembled and dispatched — capturing the full shunting lifecycle.

## Block chain
Inbound trains arrive via TrainSource (fixed 15-minute interarrival) → TrainMoveTo to the hump lead track → TrainDecouple splits the consist into individual cars → cars TrainMoveTo their assigned classification track → TrainCouple assembles cars on each departure track into a new consist → Delay (15-second coupling dwell) → TrainMoveTo to the departure lead → TrainDispose exits the assembled outbound train. Multiple parallel classification tracks run concurrently, each fed by the sorting logic after humping.

## Resources
- Classification tracks (multiple parallel holding tracks acting as implicit queues for car groups)
- No explicit ResourcePool blocks; track capacity constrains car accumulation on each bowl track
- Delay block models coupling dwell time (15 seconds per operation)

## Key settings worth copying
- Train interarrival time: 15 minutes (fixed, deterministic — easy to swap for a triangular or exponential distribution to add variability)
- Coupling dwell: 15 seconds (Delay block)
- Time unit: Minutes (fine-grained enough to capture seconds-level shunting moves)
- Accelerate/decelerate conditions on every TrainMoveTo block — essential for realistic hump speed profiles
- TrainDecouple and TrainCouple blocks used in sequence to model full consist manipulation

## KPIs instrumented
- Throughput of outbound trains assembled per shift
- Dwell time of individual cars on classification tracks
- Utilisation of the hump lead (bottleneck identification)
- Queue length on each bowl track (sorting backlog)

## Reusable idea
The key transferable trick is the **decouple → sort → recouple pattern**: use TrainDecouple to atomise a compound entity into its parts, route parts through parallel branches by attribute (destination), then use TrainCouple to re-aggregate matching parts into a new compound entity. This generalises beyond rail — it applies to any system where batches arrive mixed, must be sorted by type, and then re-batched by destination (e.g., parcel sortation, order consolidation in a warehouse).
