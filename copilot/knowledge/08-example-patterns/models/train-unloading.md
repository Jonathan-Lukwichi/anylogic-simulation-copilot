# Pattern card — Train Unloading
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES (Hybrid — Rail Library + Process Modeling Library + Material Handling Library)
- **Problem it solves:** Simulates a small rail yard where incoming trains are selectively unloaded using cranes, coordinating three distinct AnyLogic libraries in one model.

## Block chain

Two parallel flows share the model:

**Train flow (Rail Library):**
TrainSource → SelectOutput (needsUnloading?) → TrainMoveTo (arriveUnloading) → [Hold until unloading complete] → TrainMoveTo (finishedUnloading / bypass) → TrainDispose

**Cargo flow (Process Modeling Library + Material Handling Library):**
Enter → Queue → Delay → MoveTo (crane pickup position) → Pickup → MoveByCrane (unload block) → Dropoff → Queue → Split → MoveTo (storage) → Sink

Hold blocks on the train flow are released by signals from the cargo flow, synchronising the two streams — the train waits at the unloading track until all cargo has been placed in storage.

## Resources

- One or more overhead cranes modelled with the Material Handling Library (MoveByCrane block); crane travels to cargo, lifts, and deposits.
- Rail yard tracks and switches managed by the Rail Library (no explicit ResourcePool; track segments act as capacity constraints).
- No explicit ResourcePool agents; capacity is implicit in crane availability and queue sizing.

## Key settings worth copying

- **Time unit:** Minutes.
- **SelectOutput routing:** Condition `needsUnloading` on the train agent attribute determines whether a train enters the unloading spur or bypasses directly to the exit track.
- **Command-id constants** (`AT_END_OF_ENTRY = 1`, `AT_END_OF_BYPASS = 2`, `AT_UNLOADING = 3`) stored as static ints on Main, used to trigger TrainMoveTo target positions — clean way to parameterise multi-destination rail movements.
- **Startup injection:** `trainSource.inject()` called in startup code to place the first train immediately rather than waiting for an inter-arrival delay.
- **Hold/release synchronisation:** Hold blocks gate train departure; the cargo Dropoff completion triggers the Hold to open — cross-library event handshake pattern.

## KPIs instrumented

- Train cycle time (entry to dispose).
- Crane utilisation (busy time vs. available time).
- Cargo throughput (units unloaded per hour via Sink count).
- Queue length at unloading spur (train waiting for crane).

## Reusable idea

**Cross-library synchronisation via Hold + signal:** When two independent flow streams (here: trains and cargo) must wait on each other, place a Hold block in one stream and programmatically release it from an action in the other stream. This pattern generalises to any scenario where a container vehicle must wait until its contents have been processed before it can depart.
