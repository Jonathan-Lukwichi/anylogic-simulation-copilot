# Pattern card — Material Handling in Hospital
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model internal hospital logistics — moving supplies and items across multiple floors via lifts — using free-space transporters to size fleets and identify flow bottlenecks.

## Block chain
Items (supply requests) are generated at sources with interarrival times drawn from `uniform_discr(15, 20)` seconds. Each item is seized by a transporter, moved to a target location on the same or different floor, and released after delivery. When a cross-floor trip is required, the transporter navigates to a lift, rides it to the destination floor elevation, then continues in free space. Restricted-area markup gates access to sensitive zones. After delivery, items pass through a Delay representing handling/unloading before being split or sunk. Parallel streams serve different hospital wings independently, each with its own SeizeTransporter → MoveByTransporter → Release chain.

## Resources
- Free-space transporter pools (one pool per wing / zone) with capacity defined per pool
- Two AGV lift shafts (agvlift1, agvlift2, agvlift3 reference points per floor) for vertical movement
- Staff/porter ResourcePools with capacity set via `triangular(18, 20, 24)` and `triangular(5, 10, 15)` for task durations
- Restricted-area start/end markup to enforce zone access rules

## Key settings worth copying
- Interarrival: `uniform_discr(15, 20)` seconds — discrete uniform captures scheduling regularity
- Handling delay: `triangular(5, 10, 15)` seconds; porter task: `triangular(18, 20, 24)` seconds
- Model time unit: **Second**
- Lift defined with `floorElevation` and `liftingSpeed` parameters — set per shaft to reflect real building geometry
- Multiple floors modelled with the Level markup element; transporters autonomously select lifts by proximity

## KPIs instrumented
- Throughput counters on each conveyor/sink segment (items delivered per time window)
- Transporter utilisation (busy vs. idle fraction per pool)
- Queue content at SeizeTransporter blocks (backlog when fleet is undersized)
- Cross-floor trip time implicitly captured via MoveByTransporter statistics

## Reusable idea
The transferable trick is pairing **free-space transporter pools with lift markup** to handle multi-storey logistics: transporters are not confined to fixed paths, so you define only the lift shafts and floor elevations, and AnyLogic routes vehicles vertically as naturally as horizontally. Copy this pattern whenever your facility has more than one floor and you want realistic elevator contention without building explicit path networks between levels.
