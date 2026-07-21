# Pattern card — Leader Election Protocol
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based / Discrete-Event hybrid — statechart-driven agents on a message-passing network)
- **Problem it solves:** Shows how a cluster of machines autonomously elects and maintains a single leader despite node failures and an unreliable network, using randomised timeouts to break ties.

## Block chain
A population of Machine agents are interconnected through a LocalNetwork agent. Each machine runs an identical statechart encoding the three classic roles: Follower, Candidate, and Leader. Followers wait for heartbeat messages from the current leader; if the heartbeat times out (drawn from a uniform window to prevent simultaneous elections), the machine promotes itself to Candidate and broadcasts a vote request. A Candidate that collects a majority of votes transitions to Leader and begins sending periodic heartbeats. If two candidates tie, a second uniform ResolveTimeout staggers their retry so one eventually wins. The LocalNetwork layer independently models message loss, duplication, and latency: every outbound message is either dropped with probability LossRate or forwarded after an exponential(1/MeanLatency) delay. Node reliability is a two-state statechart driven by exponential failure (MTTF) and repair (MTTR) rates, so crashed machines stop sending and receiving until recovered. The combination lets you watch cascading re-elections in real time when you manually crash the current master.

## Resources
- Machine agent population (configurable count, all running the same statechart)
- LocalNetwork agent (one per logical network segment, holds LossRate and MeanLatency parameters)
- No traditional capacity pools — availability is governed by the MTTF/MTTR failure statechart embedded in each Machine

## Key settings worth copying
| Parameter | Distribution / Value | Role |
|---|---|---|
| ElectionTimeout | uniform(ElectionTimeoutLow, ElectionTimeoutHigh) | Randomises when a follower calls an election, avoiding simultaneous triggers |
| ResolveTimeout | uniform(ResolveTimeoutLow, ResolveTimeoutHigh) | Breaks ties when two candidates collide |
| Message latency | exponential(1/MeanLatency) seconds | Per-message delivery delay through LocalNetwork |
| Node failure | exponential(1/MTTF) | Time until next crash |
| Node repair | exponential(1/MTTR) | Time to recover after crash |
| LossRate | scalar [0,1] | Fraction of messages silently dropped |
- Time unit: Seconds

## KPIs instrumented
- Visual colour chart showing which machine currently holds the Leader role at each moment
- Election frequency observable by watching statechart state transitions (no formal KPI variable, but easily added as a counter)
- n/a — no throughput or queue-wait metrics; the focus is protocol correctness under failure, not performance

## Reusable idea
Use a **randomised timeout window** (uniform low/high) inside every competing agent's statechart instead of a fixed timer. This single trick — borrowed directly from Raft consensus — prevents simultaneous state transitions that would cause deadlock or infinite tie-loops, and it translates cleanly to any simulation where multiple autonomous agents must coordinate without a central arbiter (e.g., AGV priority negotiation, auction bidding, resource-contention protocols).
