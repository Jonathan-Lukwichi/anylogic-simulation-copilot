# Pattern card — Hump Yard - Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a railway hump yard where inbound trains are broken apart and their cars sorted and re-assembled into outbound trains, capturing the sequenced decouple-sort-couple workflow under timed movement constraints.

## Block chain
Inbound trains arrive via **TrainSource** (one train every 15 minutes). Each train moves to a receiving track using **TrainMoveTo**, then is split into individual cars or cuts via **TrainDecouple**. The freed cars roll over the hump and are directed to classification tracks by additional **TrainMoveTo** blocks governed by accelerate/decelerate conditions. Cars sit in short **Delay** blocks (15 seconds) representing coupling dwell time before being joined into new outbound trains with **TrainCouple**. The completed outbound train then makes a final **TrainMoveTo** to a departure track and exits through **TrainDispose**.

## Resources
No explicit ResourcePool or Seize/Release blocks. Capacity is implicitly constrained by the number of track segments (rail network topology) and the sequential nature of TrainMoveTo routing. The car agent population is set to a replication of 100 agents at 10 m/s initial speed.

## Key settings worth copying
- **Interarrival time:** 15 minutes (fixed, deterministic) — straightforward to swap for exponential(15) to introduce stochastic arrivals
- **Coupling dwell delay:** 15 seconds per cut — modelled as a Delay block, easy to parameterise
- **Car speed:** 10 m/s initial speed on track segments
- **Time unit:** Minutes (model clock), seconds used for short process delays
- **Accelerate/decelerate conditions:** Boolean flags (`ACCELERATE_YES`) on each TrainMoveTo control realistic speed profiles without hard-coding physics

## KPIs instrumented
Throughput of outbound trains (cars reassembled and dispatched), implied yard dwell time per car (time from decouple to couple exit), and track occupancy patterns visible from the animation. No explicit wait-time or utilisation dashboard shown in the base model, but Delay block statistics expose per-cut dwell automatically.

## Reusable idea
The key transferable trick is the **decouple → route → couple pipeline**: using Rail Library's TrainDecouple and TrainCouple blocks as a pair with intermediate MoveTo routing lets you model any split-process-merge workflow on a rail network (or by analogy, any entity that must be disassembled, sorted, and rebuilt). The accelerate/decelerate condition flag on each MoveTo block is a clean way to inject realistic motion behaviour without building a custom physics model.
