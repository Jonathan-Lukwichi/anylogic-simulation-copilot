# Pattern card — Maintenance - Phase 7
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Optimising a field maintenance fleet (trucks and helicopters) that must travel to and repair remote wind turbines with two distinct breakdown modes.

## Block chain
The model contains three agent populations: **Turbine**, **Truck**, and **Helicopter** (all under a coordinating **MC** — Maintenance Centre — agent). Each Turbine runs its own statechart with an **Operating** superstate that has two child states: normal running and **ScheduledService**. A rate-triggered transition fires at a fixed hazard rate to push the turbine out of Operating (breakdown); on entry to either failure sub-state the turbine calls `sendRequest(type)` where type is `AUTO` (ground breakdown — truck) or `AVIA` (aerial/offshore breakdown — helicopter). The MC agent holds the fleet collections and on receiving a `ServiceRequest` iterates the appropriate transport list to dispatch a free vehicle. Transport agents (Truck / Helicopter) each carry their own statechart: **Idle → MovingToMC ↔ MovingToTurbine → Repairing → MovingToMC → Idle**. Travel-to-turbine and travel-back steps use `moveTo()` calls against the turbine agent's location. Repair duration uses `uniform(10, 20)` hours for helicopter jobs and a fixed 10 hours for truck jobs. Once repair is complete the transport sends the string message `"repaired"` to the turbine, which transitions back into Operating. The turbine's 3-D blade animation rotates only while `inState(Operating)`, providing an instant visual health indicator. Scheduled preventive service is initiated from within Operating via a separate timeout using `uniform(0, 14)` hours offset.

## Resources
- **Truck fleet** — population of Truck agents (ground transport, type AUTO)
- **Helicopter fleet** — population of Helicopter agents (air transport, type AVIA)
- **Maintenance Centre (MC)** — single coordinating agent that queues and dispatches service requests
- **Turbines** — population of 10 Turbine agents, each with independent failure statechart

## Key settings worth copying
- Breakdown trigger: `rate`-based transition out of Operating superstate (exponential inter-failure times)
- Scheduled service offset: `uniform(0, 14)` hours — spreads preventive visits to avoid fleet conflicts
- Repair duration: `uniform(10, 20)` h for helicopter; fixed 10 h for truck
- Transport type routing: ternary `request.type == AUTO ? trucks : helicopters` to select fleet
- Time unit: **Hour**
- 3-D colour feedback: `inState(Operating) ? (inState(ScheduledService) ? yellow : green) : red`

## KPIs instrumented
- Fleet utilisation (auto-scaled presentation bars for turbines, trucks, helicopters populations)
- Turbine downtime (implicit via statechart state durations — time spent outside Operating)
- Visual throughput: blade rotation stops when turbine is down, providing real-time availability dashboard

## Reusable idea
Encode equipment health entirely inside the equipment agent's own statechart and let it self-report failures by messaging the dispatch centre — keeping fleet scheduling logic in one MC agent rather than scattering it across the environment. This separation of concerns (asset state vs. dispatch logic) scales cleanly: add more turbine types or transport modes without touching existing agent classes.
