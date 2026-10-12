# Pattern card — Path-guided AGVs loaded by a crane: explicit seize, transporter choice and dispatching, cargo placement
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Call an AGV to a pickup point, load it by crane, deliver to a conveyor, and control which AGV is chosen and how the load sits on it.

## Block chain
1. `Source`: an engine every 30 s, the first at t = 0, 9 in total. A plain `Agent` type is enough; a transporter's or crane's cargo does not need to be a Material item.
2. `SeizeTransporter`: fleet `agvs`, destination = the point node under the crane.
3. `MoveByCrane`: destination = that same node, so the crane lowers the load onto the waiting AGV.
4. `MoveByTransporter`: *Seize transporter* **off**, *Release transporter* **on**, destination = the start of the conveyor.
5. `Convey`: from the current position to the end of the conveyor.
6. `Sink`.

The crane → AGV hand-off itself is already in `basicmodels/crane-system-with-multiple-bridges.md`. This card adds the choice rules and the set-up details.

## Resources
`TransporterFleet agvs`:
- Navigation type = path-guided, capacity 3.
- A custom Transporter type: AGV 3D shape scaled to 125 %, with **Length = 1.5 m** to match it. Spacing and collision checks work on the modelled size, not on the picture *(inferred)*.
- Home = a rectangular node with 3 attractors. The attractor count caps how many vehicles can park there.
- The network is a looped path with two point nodes, one under the crane and one at the conveyor. Joining the rectangular node to the path auto-adds a point node.

## Key settings worth copying
- **Embedded vs explicit seize/release.**
  - MoveByTransporter's own seize/release is enough when loading and unloading are plain delays and the trip has no intermediate stops.
  - Use `SeizeTransporter` … `ReleaseTransporter` when loading is a process (a crane or an operator) or the trip has stops. Then untick the matching option in MoveByTransporter.
- **Customize transporter choice** → `transporterChoiceCondition(agent, unit, fleet)`. It is a boolean filter. If no available transporter passes, the agent waits for the first one that does.
  - To re-seize "my" AGV, store it on the agent and test `unit == agent.myAgv`.
- **Dispatching policy** is applied to the set the condition leaves (Help 8.9):
  - *Nearest to agent*: **straight-line** distance, ignoring walls and route length.
  - *Shortest path*: the transporter with the shortest route to the agent.
  - *The most preferred*: `transporterComparison(unit1, unit2, agent)` returns true if unit1 is preferred. Keep it transitive.
  - *Transporter with top rating*: `transporterRating(unit, agent)`; the larger value wins.
  - *Off*: any matching unit.
- **Cargo placement:** in the transporter type's On startup, call `setCargoPosition(0, 0, 0.3, METER);`. This places the load 0.3 m above the vehicle's centre. An overload adds rotation and vertical rotation; `resetCargoPosition()` undoes it.
- **After release:** by default the AGV returns home only if no task is waiting (`RP_IF_NO_OTHER_TASKS`). Other moving policies are `MP_RETURNS_TO_HOME`, `MP_RETURNS_TO_NEAREST_HOME`, `MP_STAYS_WHERE_IT_IS` and `MP_GO_TO`.
- **Traffic.**
  - Path-guided AGVs take the shortest route and avoid each other. Add `TransporterControl` only to change the rules (`basicmodels/custom-routing-for-transporters.md`).
  - By default they only see transporters of their own navigation type. In mixed fleets, tick **Recognize all transporters** (Help 8.9).

## KPIs instrumented
The webinar shows none. Suggested:
- `agvs.utilization()`, `agvs.numberOfIdle()`.
- Per vehicle: `timeInState(TransporterState.DELIVERING, MINUTE)` and `timeInState(TransporterState.GOING_TO_AGENT, MINUTE)` (empty travel), plus `getDistanceTravelled(METER)`.
- The queue length at `SeizeTransporter`.

## Pitfalls
- **Point nodes split a path.** Dropping a point node onto a path cuts it into sections. Re-check that every section is still joined (the endpoints highlight), or AGVs cannot route. The general check is in `01-anylogic-core/anylogic-in-3-days.pdf` p. 144.
- ***Nearest to agent* in a looped or one-way network** can pick an AGV that is close as the crow flies but far by route. Prefer *Shortest path*.
- **Cargo inside the vehicle in 3D:** fix it with `setCargoPosition`. Scaling the shape alone does not help.
- **Destination geometry:** for Node, Attractor or (x, y, z) destinations, the point marks the transporter's centre while it travels. On release, the load is placed at that destination (Help 8.9).

## Reusable idea
Keep **who** does the job (condition + dispatching policy) separate from **how** it moves (network + TransporterControl). Split seize and release out of MoveByTransporter whenever something else must happen while the vehicle is held.

## When the co-pilot should use this
- **Use cases:** AGV or forklift fleets served by cranes, robots or operators; fleet sizing; "wrong AGV gets picked" questions; 3D cargo that floats or is buried.
- **Choosing a library:** use transporters, not ResourcePool moving units, when congestion and give-way at crossroads matter. PML network movers do not interfere with each other (`anylogic-in-3-days.pdf` p. 138).
- **Related cards:** `models/palletizing-system-with-agv.md`, `models/transporters-moving-in-free-space.md`.

## Additions (8.9.10 review, 2026-10-01)
- `SeizeTransporter` can send the vehicle to a point on a path (`destinationPath`, `destinationPathOffset`) instead of a node. For crane unloading, the crane first lifts the load clear of the AGV (`MoveByCrane` to `agent.getZ() + 10`, *Release crane* off) **before** `ReleaseTransporter`, and only then puts it on the conveyor; `Convey` can turn items on the belt (*Change orientation*, `AGENT_ORIENTATION_LEFT`) (8.9.10 *SeizeTransporter and ReleaseTransporter*).
- 8.9.10 adds `getEstimatedTimeOfArrival()`, `jump()`, `recalculatePriorities()` on SeizeTransporter/MoveByTransporter, a *Fastest* routing policy and an *On collision* action (release notes).
