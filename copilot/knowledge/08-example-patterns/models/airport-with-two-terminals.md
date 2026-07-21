# Pattern card — Airport with Two Terminals
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Pedestrian Library + Rail Library)
- **Problem it solves:** Models the end-to-end passenger journey through a two-terminal airport — from flight schedule through check-in, security, inter-terminal shuttle, boarding, deplaning, and baggage claim — while coordinating three independently scheduled entity streams (passengers, trains, aircraft).

## Block chain
Passengers are generated according to a flight schedule rather than a simple arrival rate. Each flight injects a batch of passengers into Terminal A or B at a scheduled departure minus check-in lead time. Passengers walk (Pedestrian Library) through check-in counters and security lanes. Those whose departure gate lies in the opposite terminal board a shuttle train (Rail Library); the train runs on a fixed circuit between Terminal A and Terminal B, loading and unloading passengers at platform stops. After clearing security (or riding the shuttle), passengers walk to their gate and queue for boarding. Arriving passengers follow the reverse path: they deplane, walk to baggage claim, and exit. The three process chains — passenger flow, train movement, and aircraft turnaround — are linked by shared events and gate assignments rather than direct block connections, keeping each sub-model modular.

## Resources
- Check-in counters: pool of agents per terminal (capacity configurable per desk row)
- Security lanes: parallel service channels, each terminal has its own lane set
- Shuttle train: single train entity cycling Terminal A platform -> Terminal B platform -> return; capacity defines max passengers per trip
- Gate doors: six gates total (A1, A2, A3, B1, B2, B3) referenced by name at routing decision points

## Key settings worth copying
- Time unit: Minute (fine-grained enough for dwell-time fidelity without second-level overhead)
- Flight schedule drives source injection — passengers arrive as bursts tied to scheduled departure times, not a continuous Poisson stream
- Gate assignment stored on each passenger agent and resolved via a helper function (`getTargetDoor(flight)`) that returns one of six door references — clean way to route large crowds to specific spatial targets
- Train circuit modeled with `TrainSource`, `TrainMoveTo`, and `Delay` blocks for dwell time at each platform; the same two-stop loop repeats indefinitely
- 3D / 2D views are toggled at run time by a view variable, enabling both a bird's-eye overview and close-up terminal walkthroughs without duplicating the model

## KPIs instrumented
- Passenger dwell time at each stage (check-in wait, security wait, gate wait)
- Train utilisation and passenger load per trip
- Gate throughput (boarding completion before departure deadline)
- Baggage claim queue length for arriving passengers

## Reusable idea
The key transferable trick is **schedule-driven batch injection combined with named spatial targets**: instead of generating agents continuously, release them in flight-sized cohorts at computed wall-clock times and immediately stamp each agent with its destination gate reference. This pattern eliminates complex routing logic downstream — every MoveTo block just reads the pre-stamped target — and naturally reproduces the bursty, wave-like congestion that real airports experience around departure pushes. It applies directly to any multi-gate or multi-dock facility (bus terminals, cruise ports, warehouse loading docks) where arrivals are event-driven rather than random.
