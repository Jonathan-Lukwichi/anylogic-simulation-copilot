# Pattern card — Subway Platform
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES (Pedestrian Library + Rail Library hybrid)
- **Problem it solves:** Models bidirectional passenger flow on a subway platform where alighting passengers must fully clear the doors before waiting passengers can board.

## Block chain
Two pedestrian sources (`pedSourceWest`, `pedSourceEast`) generate arriving passengers who walk to the platform and wait. When a train event fires, a Rail Library train agent pulls in and triggers door-zone pedestrian sources (`pedSourceTrainDoors1`, `pedSourceTrainDoors2`) that release alighting passengers at a controlled unload rate. A `SelectOutput` block routes each pedestrian: alighting passengers head straight for the exits (`PedGoTo` → `PedSink`), while waiting passengers are held (`PedWait`) until alighting is complete, then routed via `PedGoTo` through the train doors to their own `PedSink`. Two separate train schedules (`trainSource1`, `trainSource2`) inject train agents on independent timed events, keeping the two platform tracks independent.

## Resources
- Platform capacity: one integer `capacity` parameter controlling pedestrian density limits
- Train unload rate: `uniform_discr(2000, 2250)` passengers per hour per door set, set dynamically on each train arrival via `setTrainUnloadRate()`
- Two groups of door-zone `PedSource` blocks (one per track), each with individually settable rates

## Key settings worth copying
- **Alighting rate:** `uniform_discr(2000, 2250)` pax/hour — gives realistic variability in how quickly a train empties
- **Boarding gate logic:** boarding rate set to 0 until alighting sources stop, enforcing the sequential alighting-before-boarding rule in code rather than a complex connector arrangement
- **Time unit:** Minutes — train headways expressed as per-minute rates on timed event blocks
- **Pedestrian movement time:** `uniform(0.5 * second(), 1.0 * second())` used for short navigation steps inside the station
- **Dual-track injection:** two `trainSource.inject()` calls on separate timed events, each wired to its own door-zone sources

## KPIs instrumented
- Platform crowd level (pedestrian count in wait zone)
- Throughput: passengers alighted and boarded per train visit (tracked via PedSink counts)
- Dwell time implied by how long boarding is blocked while alighting completes

## Reusable idea
**Rate-gated sequential flow:** use a programmatically settable source rate (set to 0 to block, set to a positive value to open) as a lightweight gate between two opposing pedestrian streams. This avoids complex conditional connectors — you simply call `set_rate(0)` to hold one stream until the other finishes, then restore the rate. The same trick applies anywhere two crowds must take turns using a shared corridor, doorway, or bottleneck.
