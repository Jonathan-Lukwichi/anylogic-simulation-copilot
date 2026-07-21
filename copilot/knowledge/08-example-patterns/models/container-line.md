# Pattern card — Container Line
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + DES)
- **Problem it solves:** Models a global container-shipping network where ships autonomously navigate between ports and enter port-service queues, with a dynamic storm hazard that slows transit in a defined ocean zone.

## Block chain
Each ship is an independent agent that follows a statechart with three behavioural states: sailing normally, slowed by storm, and in port being serviced. On departure a ship picks its next destination randomly from the current port's list of connected ports. It moves across a GIS map toward that port. If the ship enters the Pacific storm zone while `stormOn` is true, it transitions to the Storm state and its speed drops. Once clear of the zone (or the storm flag turns off) it resumes normal speed. On arrival the ship enters a Process Modeling Library flowchart inside the `ContainerPort` agent: an **Enter** block injects it into a **Service** block backed by a **ResourcePool** (the berths). Service duration is drawn as `uniform(meanServiceTime * 0.7, meanServiceTime * 1.3)`. When service is complete the port sends the ship a "Service finished" message, the ship's statechart transitions back to sailing, and the cycle repeats. Ten named ports (Le Havre, Dubai, Durban, Singapore, Shanghai, Osaka, Melbourne, San Francisco, Colon, Valparaiso) are instantiated as separate `ContainerPort` agent populations on the map.

## Resources
- **ResourcePool** inside each `ContainerPort` — capacity set via the port's `capacity` parameter (default 100 berths per port)
- Ship agent population — count configurable; each ship is one autonomous moving agent

## Key settings worth copying
- Service time: `uniform(meanServiceTime * 0.7, meanServiceTime * 1.3)` — simple ±30 % spread around a per-port mean; easy to swap for triangular or lognormal
- Next-port routing: `uniform_discr(port.connectedPorts.length - 1)` — random selection from an explicit adjacency list defined per port
- Storm condition guard: `main.stormOn && main.stormArea.contains(getX(), getY())` — a polygon area check evaluated as a statechart transition condition; no scheduler needed
- Transit time: `uniform(2, 3)` days sampled on each sailing leg
- Time unit: **Day**
- Initial port assignment: `uniform_discr(ports.size() - 1)` — ships start at a random port from the global list

## KPIs instrumented
- Ship state distribution over time (chart tracks `statechart.getActiveSimpleState().ordinal()`) — separates sailing-normal, storm-slowed, and in-service fractions
- Visual colour coding on the map: ships turn red when in Storm or InService state, dark blue otherwise — instant qualitative throughput read

## Reusable idea
The key transferable trick is **embedding a DES flowchart inside an ABM agent (ContainerPort) and using message-passing to hand off control between the agent statechart and the flowchart**. The ship's statechart drives spatial movement; when it arrives, the port's Enter/Service/ResourcePool chain takes over for queuing logic; the port fires a message back to release the ship. This clean handshake lets you mix autonomous navigation (ABM) with capacity-constrained queuing (DES) without coupling them tightly — a pattern directly applicable to any mobile-entity + fixed-station system (ambulances docking at hospitals, AGVs at workstations, trucks at loading bays).
