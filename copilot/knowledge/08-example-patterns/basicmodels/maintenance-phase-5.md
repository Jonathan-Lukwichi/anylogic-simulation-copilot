# Pattern card — Maintenance - Phase 5
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM / Hybrid (agent-based machines + discrete-event service logistics)
- **Problem it solves:** Scheduling preventive and corrective maintenance for a fleet of wind turbines dispersed across a geographic area, dispatching either trucks or helicopters depending on access type.

## Block chain
Each Turbine agent hosts a statechart that governs its lifecycle: an operating state transitions to a broken-down state at a rate driven by 1/MTTF (mean time to failure). On breakdown the turbine raises a ServiceRequest flagged as AUTO (truck) or AVIA (helicopter). The Maintenance Center (MC) agent holds two queues — autoRequests and aviaRequests — and a findTransport() method that iterates over the truck or helicopter fleet to find an idle Transport agent. The chosen Transport's own statechart moves it from its base to the turbine location (MovingToMC state), performs the repair, then returns to base. A separate scheduled-maintenance trigger fires on a uniform(0, 14)-hour interval and sends a "scheduled" message into the turbine's statechart, initiating planned service before failure occurs.

## Resources
- **Turbine population:** 25 agents, each with individual MTTF parameter
- **Truck fleet:** configurable count of Transport agents (ground, TransportType.AUTO)
- **Helicopter fleet:** configurable count of Transport agents (air, TransportType.AVIA)
- **MC (Maintenance Center):** 1 agent acting as dispatcher/coordinator
- Speed unit: m/s; time unit: hours

## Key settings worth copying
- Failure rate expressed as `1/MTTF` on a statechart transition — cleanly separates the MTTF parameter from the rate expression
- Transport type enum (`AUTO` / `AVIA`) on ServiceRequest lets a single findTransport() loop serve two heterogeneous fleets
- `uniform(0, 14)` hours for scheduled-maintenance offset randomises planned visits to avoid convoy clustering
- `setTransportBase()` startup code positions all vehicles before simulation starts
- 3-D scene assets (.dae files) for turbines, lorry, and helicopter enable visual validation of routing

## KPIs instrumented
- Turbine downtime (time spent in broken/waiting-for-repair states)
- Transport utilisation (fraction of time each truck/helicopter is en route or repairing)
- Queue length of pending service requests (auto and avia separately)
- Number of completed repairs per transport type

## Reusable idea
Encode the access-mode requirement directly on the work order (ServiceRequest.type = AUTO | AVIA) and let the dispatcher's findTransport() method pick from the matching fleet — this pattern cleanly extends to any scenario where different job classes require different resource categories without needing separate process flows for each.
