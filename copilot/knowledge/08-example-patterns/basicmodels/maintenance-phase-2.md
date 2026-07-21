# Pattern card — Maintenance - Phase 2
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Optimising the dispatch of mixed transport assets (trucks and helicopters) from a single maintenance centre to service a field of 25 offshore wind turbines.

## Block chain
The model is built around four agent types that interact in continuous 2-D space. A central `MC` (Maintenance Centre) agent acts as the home base; it holds populations of `Truck` (5 units) and `Helicopter` (2 units) agents, both extending the abstract `Transport` superclass. The 25 `Turbine` agents are scattered across the field. When a turbine needs attention the maintenance centre selects an available transport vehicle, dispatches it to the turbine location, performs the service, and the vehicle returns to base. The `Transport` superclass carries a `type` parameter (enum `TransportType`: AUTO vs AVIA) that drives routing decisions — AUTO dispatches trucks, AVIA dispatches helicopters — enabling quick swap-and-compare experiments. Agent movement uses continuous space at 10 m/s with a `setTransportBase()` startup function that anchors all vehicles to the MC coordinates. Time unit is Hours; the run stops at t = 100 h.

## Resources
| Population | Count | Base class |
|---|---|---|
| Turbines | 25 | Agent |
| Trucks | 5 | Transport (AUTO) |
| Helicopters | 2 | Transport (AVIA) |
| Maintenance Centres | 100 (field capacity) | Agent |

## Key settings worth copying
- **Time unit:** Hour; simulation horizon 100 h (fixed stop time)
- **Random seed:** Fixed seed = 1 (reproducible baseline; switch to random for sensitivity runs)
- **Transport superclass pattern:** one `Transport` base class with enum parameter `type`; subclass agents (`Truck`, `Helicopter`) inherit movement logic and override only what differs
- **Startup hook:** `setTransportBase()` iterates all vehicle populations and sets initial location to the MC — clean way to initialise multi-population positions programmatically
- **Space:** continuous 2-D, 10 m/s default velocity; scale ruler: 100 px = 10 m
- **Event sampling:** datasets collected every 1 h

## KPIs instrumented
- Vehicle utilisation (implicit via travel vs idle time)
- Turbine downtime (time waiting for a vehicle to arrive)
- Number of maintenance trips completed within the horizon
- Transport type comparison (truck fleet vs helicopter fleet throughput at t = 100 h)

## Reusable idea
The single transferable trick is the **transport-type enum pattern**: define one abstract `Transport` agent class with a `type` parameter and let the dispatcher branch on that enum rather than on the concrete subclass. This means you can add a third transport mode (e.g., drone) by creating a new subclass and adding one enum value — the dispatch logic never changes. Apply this whenever a model has multiple asset categories that share a movement workflow but differ in speed, cost, or routing rules.
