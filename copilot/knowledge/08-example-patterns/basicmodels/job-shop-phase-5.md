# Pattern card — Job Shop - Phase 5
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates a multi-machine job shop where pallets travel between workstations via forklifts, capturing both material handling and machining delays in a 3-D warehouse layout.

## Block chain
Two job streams each follow this sequence: Source (pallet or truck arrival) → Store (queue at input buffer) → Retrieve (pull from storage) → Seize (claim forklift or CNC machine resource) → MoveTo (travel to workstation) → Delay (processing time, triangular 15–30 min) → MoveTo (travel to output) → Release (free resource) → Sink. A parallel forklift-only flow handles internal transport between storage areas using Seize / MoveTo / Delay / Release cycles before the main job resumes.

## Resources
- **ForkliftTruck** ResourcePool — handles all internal pallet movements between Store nodes and workstations.
- **CNC** ResourcePool — represents machining stations seized per job during processing.
- Capacity for both pools is defined statically; attractor-based capacity configuration is present but left at defaults.

## Key settings worth copying
- **Interarrival time:** fixed 5-minute interval per Source (deterministic pacing, not stochastic).
- **Processing delay:** `triangular(15, 20, 30)` minutes — minimum 15, most-likely 20, maximum 30; good default for machining variability.
- **Time unit:** Minutes throughout.
- **Store / Retrieve pair:** use AnyLogic Warehouse Library blocks to model physical racking; pallets are physically placed and retrieved rather than just queued abstractly.
- **3-D assets:** forklift.dae, pallet.dae, sittingworker.dae wired to agents for animated walkthroughs.

## KPIs instrumented
- Throughput at each Sink (pallet count exiting each job stream).
- Resource utilisation tracked implicitly via Seize/Release statistics on ForkliftTruck and CNC pools.
- Delay statistics (mean, max wait) collected at each Delay block for processing time distribution verification.

## Reusable idea
Pair a **Store → Retrieve** block sequence around every **Seize → Delay → Release** cluster: this forces the simulation to physically place entities in a buffer rack before a transport resource picks them up, giving you realistic forklift contention and travel-time effects that a plain Queue block cannot capture.
