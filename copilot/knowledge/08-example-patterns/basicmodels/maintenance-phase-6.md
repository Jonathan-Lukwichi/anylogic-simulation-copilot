# Pattern card — Maintenance - Phase 6
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (ABM + statecharts)
- **Problem it solves:** Coordinating multi-modal maintenance logistics for a fleet of wind turbines spread across a geographic area, where repair crews must travel to assets using either road trucks or helicopters depending on request type.

## Block chain
The model maintains a population of **Turbine** agents and a **Maintenance Centre (MC)** agent. Each turbine runs its own statechart with an `Operating` superstate that contains two sub-states: normal running and `ScheduledService`. A rate-triggered transition fires periodically to initiate a breakdown or scheduled service; the turbine then creates a `ServiceRequest` object tagged with either `AUTO` (road) or `AVIA` (helicopter) and sends it to the MC.

The MC agent holds separate fleets of **Truck** and **Helicopter** (Transport) agents. On receiving a request it iterates the appropriate fleet to find an idle vehicle. The chosen transport agent's statechart drives it from the hangar, to the turbine, through a repair wait, and back — sending a `"repaired"` message to the turbine when done, which transitions the turbine back to normal operation. The hangar is visualised as a 3-D scene object so the full round-trip is animated in the 3-D environment.

## Resources
- `trucks` — fleet of AUTO transport agents (road vehicles), initially type = AUTO
- `helicopters` — fleet of AVIA transport agents, initially type = AVIA
- Turbine population — N wind turbine agents, each self-managing via statechart
- MC (Maintenance Centre) — single coordinating agent that owns both fleets

## Key settings worth copying
- Breakdown / scheduled service trigger: `rate`-triggered statechart transition (rate value configurable)
- Scheduled repair interval sampled with `uniform(0, 14)` hours — adds stochastic jitter to prevent all turbines queuing at once
- Repair duration: `type == AVIA ? uniform(10, 20) : 10` hours — helicopter jobs take variable time; truck jobs are fixed
- Time unit: **Hour**
- Transport selection logic: iterate fleet list, pick first idle vehicle — simple greedy dispatch
- Turbine colour reflects state dynamically: green (operating), yellow (scheduled service), red (broken/being repaired)

## KPIs instrumented
- Visual state of each turbine (colour-coded in 3-D view) as a real-time availability indicator
- Implied downtime: time a turbine spends outside the `Operating` state
- Fleet utilisation: fraction of trucks / helicopters away from hangar at any moment

## Reusable idea
**Request-object dispatch pattern**: rather than wiring turbines directly to transport agents, each turbine packages its service need into a plain data object (`ServiceRequest`) and hands it to a central coordinator. The coordinator then selects the right resource class and lets the resource's own statechart manage the full travel-repair-return cycle, keeping turbine logic, fleet logic, and routing logic cleanly separated. This pattern scales directly to any scenario where multiple heterogeneous asset types must be serviced by differentiated mobile crews.
