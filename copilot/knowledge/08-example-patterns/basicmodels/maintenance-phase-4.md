# Pattern card — Maintenance - Phase 4
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Sizing and dispatching a mixed transport fleet (trucks + helicopters) to service a field of remote assets (wind turbines) that fail stochastically.

## Block chain
A Maintenance Center (MC) agent sits at a fixed depot. Twenty-five Turbine agents are scattered across a spatial environment (scale: 10 km per 100 pixels, time unit: hours). When a turbine needs service it creates a ServiceRequest and queues it on the MC — either in the `autoRequests` list (road-accessible, AUTO type) or `aviaRequests` list (aviation required, AVIA type).

The MC calls `findTransport(request)` to locate a free vehicle of the correct type from its pools: five Truck agents or two Helicopter agents. Each Transport agent owns a statechart with four sequenced states — **AtCenter → MovingToTurbine → Servicing → MovingToMC** — followed by a branch that checks whether another request is waiting. If yes, the transport heads straight to the next turbine without returning home; if no, it idles at the center until dispatched again.

The Turbine agent similarly carries a statechart that mirrors the repair lifecycle. Bidirectional agent-link messaging between MC and transport agents coordinates dispatch and job completion signals.

## Resources
- 5 Truck agents (AUTO transport pool)
- 2 Helicopter agents (AVIA transport pool)
- 1 MC agent (dispatcher + request queues)
- 25 Turbine agents (demand generators)

## Key settings worth copying
- TransportType enum {AUTO, AVIA} drives routing logic in `findTransport()` — clean way to branch fleet dispatch without separate process flows
- Spatial scale ruler: 100 px = 10 km (KILOMETER units), so travel-time timeouts in the statechart are proportional to real distances
- Transport statechart branch after returning to MC: looping immediately to a waiting job rather than resetting to idle avoids unnecessary deadhead trips
- Agent-link `connections` network (bidirectional, COLLECTION_OF_LINKS) used for MC-to-transport messaging — avoids polling, push-driven dispatch

## KPIs instrumented
- Dataset sampled every 1 hour from simulation start for time-series tracking
- Implicitly: transport utilisation (fraction of time not in AtCenter state), turbine downtime (time spent waiting for and receiving service), queue depths of autoRequests / aviaRequests

## Reusable idea
Encode transport mode as an enum on the ServiceRequest, then use a single `findTransport()` helper to select from heterogeneous resource pools — this keeps dispatch logic centralized and makes adding a third transport type (e.g., a boat) a one-line pool addition rather than a restructured process flow.
