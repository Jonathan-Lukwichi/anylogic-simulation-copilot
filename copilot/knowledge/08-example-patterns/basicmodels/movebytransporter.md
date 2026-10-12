# Pattern card — MoveByTransporter
- **Source:** AnyLogic example model "MoveByTransporter" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** AGVs pick coloured items off the ends of three feeding conveyors and place each one onto the outbound conveyor for its colour — a conveyor-to-conveyor transfer by a transporter fleet.

## Block chain
`Source` (item routing decided in *On at exit*: a random feeding conveyor and a target conveyor by colour) → `Convey` (along `agent.sourceConveyor` to its end) → `MoveByTransporter` (destination type **conveyor** = `agent.targetConveyor`, loading 5 s, unloading 15 s) → `Convey` (along the target conveyor) → `Sink`.

## Resources
`TransporterFleet` of 12 AGVs (1.25 × 0.5 × 0.25 m, acceleration 0.1 m/s², homes `node`, `node1`), path-guided.

## Key settings worth copying
- `destinationType = DEST_CONVEYOR`, `destinationConveyor = <ConveyorPath>` — the AGV drives to the conveyor and unloads the item onto it; the next `Convey` continues on that conveyor.
- Keep routing in agent fields (`sourceConveyor`, `targetConveyor`) set once at the Source, so every block reads `agent.<field>` instead of repeating the decision.
- Load/unload times on the block (`loadingTime`, `unloadingTime`) occupy the vehicle, not the conveyor.
- Release policy `MP_RETURNS_TO_NEAREST_HOME` spreads idle AGVs over the two home nodes.
- **Task priority and pre-emption (Help 8.9.10):** *Task priority* (larger first) orders waiting requests; with *Task may preempt* on, a higher-priority request can **intercept a transporter that is still travelling to** a lower-priority agent. *Task preemption policy*: `PP_NO_PREEMPTION` (default — the current task continues) or `PP_SEIZE_ANY_RESOURCE` (the interrupted task is suspended and tries to seize any other transporter; hooks *On task suspended* / *On task resumed*).
- Priorities are evaluated when the agent arrives; to make them dynamic (ageing, due dates) call `recalculatePriorities()` or `recalculateAgentPriority(agent)` — never applied to agents already being carried.

## KPIs instrumented
Visual only (logic and 3D views).

## Pitfalls
- In this demo every task has priority 0, so the `PP_SEIZE_ANY_RESOURCE` setting has nothing to act on; pre-emption only matters once priorities differ.
- A priority expression that depends on time (waiting time, slack) silently stays at its entry value unless the block is told to recalculate.
- `unloadingTime` is spent at the conveyor; if the target conveyor is full at that point the vehicle waits there, and the fleet can starve.

## Reusable idea
Treat an AGV transfer between two conveyor systems as one `MoveByTransporter` with a conveyor destination, and decide both conveyors once per item at creation. When some flows are urgent, combine *Task priority* + *Task may preempt* + `PP_SEIZE_ANY_RESOURCE` so urgent loads steal vehicles that are only en route, and the displaced task simply looks for another one.

## When the co-pilot should use this
AGV/forklift links between conveyor lines, sorters feeding outbound lanes, or questions about how transporter priorities and interception work. For dispatch rules and cargo position see `videos/mhl-agv-dispatch-choice-and-cargo-position.md`.
