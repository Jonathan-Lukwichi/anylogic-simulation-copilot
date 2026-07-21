# Pattern card — Traffic Light Phases Optimization
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES (Agent-Based road traffic / pedestrian library)
- **Problem it solves:** Find the green-phase durations for each direction at three signalised intersections that minimise average vehicle travel time through the network.

## Block chain
Six independent vehicle streams enter the road network via **CarSource** blocks (one per approach lane / direction). Each car agent navigates a road topology through **CarMoveTo** blocks that advance the vehicle along path segments. At each intersection, a **SelectOutput5** (or **SelectOutput**) block routes the car to the correct outbound road segment based on its destination. After traversing all required segments the car exits through a **CarDispose** block. Traffic lights are modelled as timed state machines attached to intersection nodes: the green-phase durations for West–East and North–South (or North / South) flows are exposed as model parameters and toggled by cyclic timers.

## Resources
No resource pools in the conventional sense. Capacity is implicit in the road network geometry (single-lane segments). Six CarSource entry points feed the three junctions:
- Crossroads (X): West–East and North–South approaches
- T1 junction: West–East and North approaches
- T2 junction: West–East and South approaches

Arrival rate per source: **700 vehicles / hour** (Poisson process via rate-based CarSource).

## Key settings worth copying
| Parameter | Default | Range searched |
|---|---|---|
| pX_WE — green time, crossroads W–E | 30 s | 1–60 s |
| pX_NS — green time, crossroads N–S | 20 s | 1–60 s |
| pT1_WE — green time, T1 W–E | 35 s | 1–60 s |
| pT1_N — green time, T1 North | 15 s | 1–60 s |
| pT2_WE — green time, T2 W–E | 20 s | 1–60 s |
| pT2_S — green time, T2 South | 40 s | 1–60 s |

- Model time unit: **seconds**
- Vehicle speed: 10 m/s (default road-network setting)
- Optimisation method: AnyLogic built-in **OptimizationExperiment** (OptimumSeek), minimising `meanTimeInSystem`

## KPIs instrumented
- **meanTimeInSystem** — the single scalar objective: average seconds a car spends from creation (CarSource) to disposal (CarDispose). This is what the optimiser minimises.
- Best parameter values are displayed on the optimisation experiment dashboard alongside current vs. best comparison panels for all six phase parameters.

## Reusable idea
Expose traffic-light phase durations as plain numeric parameters (one per direction per junction, range-bounded 1–60 s), then wire `meanTimeInSystem` directly into an OptimizationExperiment. This separates the simulation logic from the search completely: the same pattern applies to any network of signalised junctions — just add parameters, keep the KPI scalar, and let the optimiser sweep the space without touching the flow logic.
