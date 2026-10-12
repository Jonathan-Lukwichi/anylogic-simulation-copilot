# Pattern card — Agent Network and Layouts Demo
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling in continuous space)
- **Problem it solves:** Illustrates how to generate, visualise, and hot-swap different agent network topologies and spatial layouts at runtime without rebuilding the model.

## Block chain
There is no process-flow chain. The model hosts a single population (`agents`) of custom `MyAgent` instances placed in a continuous 2-D space. Connections between agents are stored in a `connections` network object. On demand, the network is rebuilt using one of six topology generators (User-Defined, Random, All-in-Range, Ring Lattice, Small World, Scale-Free). Separately, the visual arrangement of agents is refreshed with one of four layout algorithms (Random, Arranged, Spring-Mass, Ring). Neither topology nor layout requires a restart — they are recalculated on button click during a live run.

## Resources
- No ResourcePool or service blocks are used.
- Agent population size is controlled by radio buttons (10 / 50 / 100 / 200 / 500 agents); agents are added or removed programmatically during the run via `add_agents()` / `remove_agents()`.
- Two continuous slider parameters drive network shape: **connectionRange** (distance threshold for proximity-based linking) and **connectionsPerAgent** (target degree for random and lattice topologies).
- A third slider, **neighborLinkProbability**, sets p in the Small World topology: the probability that a link goes to a neighbour (a local link), not a rewiring probability (Help 8.9.10 *Agent API*; the *SIR Agent Based Networks* example passes `1 - PercentOfLongLinks`).
- **scaleFreeM** controls the number of edges added per step in the Scale-Free (Barabási–Albert) generator.

## Key settings worth copying
| Setting | Purpose |
|---|---|
| `setNetworkRandom(k)` | Random links, **k on average** per agent (not exactly k) |
| `setNetworkAllInRange(r)` | Links all agents whose spatial distance ≤ *r* |
| `setNetworkRingLattice(k)` | Ordered ring where each node links to its *k* nearest neighbours (k even) |
| `setNetworkSmallWorld(k, p)` | Ring lattice of degree *k* (even) where each link stays local with probability *p* and otherwise goes to a random agent |
| `setNetworkScaleFree(m)` | Preferential-attachment growth adding *m* edges per new node |
| `setLayoutType(LayoutType.*)` | Switches spatial arrangement (RANDOM, ARRANGED, SPRING_MASS, RING) without resetting agent state |
| Time unit | Day (model clock advances but has no effect on agent behaviour here) |

Random networks and layouts draw from the model's random stream, so the topology changes with the seed; `applyNetwork(Random r)` lets you control it (Help 8.9.10, release notes). (An earlier version said no randomness is used — corrected 2026-10-01.)

## KPIs instrumented
n/a — the model is a visual demo; no throughput, wait-time, utilisation, or cost metrics are tracked. The observable output is the rendered network graph itself.

## Reusable idea
**Runtime topology switching:** by separating the network-generation call from agent initialisation, you can let users explore how connectivity structure changes during a live simulation run. This pattern is directly transferable to any ABM where you want to compare how disease spread, information diffusion, or supply-chain resilience behaves under different graph topologies (random vs. scale-free vs. small-world) without running separate experiments — just swap the topology mid-run and observe the immediate structural change.
