# Pattern card — Agent Moving Along Path
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Show how a mobile agent navigates a road network to reach another agent's location on demand.

## Block chain
Two custom agent types (Truck and Warehouse) are placed in a continuous-space environment that contains a user-defined road network. The Truck is registered to the network at startup via `setNetwork(...)`. When the user clicks a button, the Truck's `moveTo(warehouse)` method is called, causing the Truck to find a path through the network and travel to the Warehouse agent's current position. There are no Process Modeling Library blocks (no Source/Sink chain) — the logic is entirely event-driven through agent methods and UI controls.

## Resources
- **Agent populations:** one Truck agent, one Warehouse agent, both residing in the Main environment
- **Network:** a single user-defined road network (`road`) defined in Main; the Truck joins this network on startup
- No ResourcePools or schedules — resource ownership is implicit in the single-agent scenario

## Key settings worth copying
- **Time unit:** Seconds
- **Truck speed:** 10 m/s (set in AgentProperties > VelocityCode with unit MPS)
- **Space type:** Continuous (not grid or GIS)
- **Network attachment:** call `setNetwork(networkRef)` in the agent's startup code so the agent is path-aware from the first simulation step
- **Trigger mechanism:** a button control whose action calls `agentRef.moveTo(targetAgent)` — demonstrates on-demand, user-triggered movement rather than scheduled movement
- **Animation:** Truck icon rotation is synced to the direction of travel (`RotateAnimationTowardsMovement = true`)

## KPIs instrumented
n/a — this is a minimal demonstration model; no statistics, datasets, or output charts are configured beyond the visual animation

## Reusable idea
Attach a mobile agent to a named network at startup, then trigger network-aware pathfinding to any target position (including another agent's dynamic location) with a single `moveTo()` call. This pattern scales directly to fleet-routing, warehouse picker, or campus-navigation models where vehicles or people must follow defined paths rather than moving in a straight line.
