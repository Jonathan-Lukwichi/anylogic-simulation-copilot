# Pattern card — Maintenance - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Dispatch limited repair vehicles (trucks and helicopters) across a geographically dispersed wind-farm to service failed turbines as efficiently as possible.

## Block chain
The model contains five distinct agent types living in a shared continuous 2-D space. A central maintenance depot (MC) acts as the base from which repair missions originate. Twenty-five Turbine agents are scattered across the landscape; when a turbine breaks down it raises a ServiceRequest object that specifies which transport mode is required (AUTO for truck, AVIA for helicopter). A fleet of five Trucks and two Helicopters — both extending a shared Transport base class — each run an identical four-state statechart:

1. **AtCenter** — idle at the depot, waiting for a message that a job has arrived.
2. **MovingToTurbine** — the agent physically navigates through continuous space toward the target turbine; the transition fires on spatial *arrival*.
3. **Servicing** — the agent stays on-site for a timeout duration representing repair work.
4. **MovingToMC** — the agent returns to depot; on arrival a branch decides whether another queued request is waiting (loop back to MovingToTurbine) or the vehicle is truly idle (return to AtCenter).

Message-passing between agent populations drives dispatch: the MC sends a ServiceRequest message to an available vehicle of the correct type, and the vehicle stores the request reference to navigate to the right turbine.

## Resources
- Maintenance center (MC): 1 depot agent, acts as dispatcher and home base
- Turbines: population of 25
- Trucks: fleet of 5, speed 70 kph, type = AUTO
- Helicopters: fleet of 2, speed 10 m/s (~36 kph but unconstrained by road), type = AVIA
- Transport base class shared by both vehicle subtypes (statechart inherited)

## Key settings worth copying
- Time unit: Hour
- Truck speed: 70 kph; Helicopter speed: 10 m/s — set at agent-type level so the same statechart movement logic produces different travel times automatically
- TransportType enum (AUTO / AVIA) embedded in ServiceRequest lets the dispatcher route jobs to the correct vehicle pool without branching logic in the statechart
- Statechart transition triggers: *message* (job arrives) → *arrival* (reached destination) → *timeout* (repair done) → *timeout* (returned to base) — mixing trigger types keeps each phase clean
- Branch after return-to-base cleanly handles the "pick up next job or go idle" decision without a separate queue block

## KPIs instrumented
- Implicit: vehicle utilisation (fraction of time not in AtCenter state)
- Implicit: turbine downtime (time between failure and end of Servicing)
- Dataset auto-created every 1 hour for trend tracking

## Reusable idea
Encode the *required resource type* inside the work-order object (ServiceRequest.type) rather than in routing logic, then let the dispatcher match requests to pools by type. This keeps the vehicle statechart universal and makes it trivial to add a third transport category — just extend the enum and create a new agent subclass with a different speed.
