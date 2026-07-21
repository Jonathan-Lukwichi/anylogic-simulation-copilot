# Pattern card — Maintenance - Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Deciding how to dispatch repair crews (ground truck vs. helicopter) to failing wind turbines scattered across a large geographic area.

## Block chain
The model places a single Maintenance Center (MC) agent on a continuous 2-D space scaled at roughly 10 km per 100 pixels. Twenty-five Turbine agents are distributed across that space; each turbine can be in an operational or broken-down state and, when it fails, it generates a ServiceRequest. The ServiceRequest carries two fields: which turbine needs attention and what transport mode should be used (AUTO for ground truck, AVIA for helicopter). A fleet of five Trucks and two Helicopters — modelled as separate Transport agents — are dispatched from the MC. The chosen vehicle travels to the turbine location, performs the repair, and returns to base. The 3-D scene (hangar, turbine tower, blade, lorry, helicopter DAE meshes) visualises every movement in real time. Time runs in hours; the experiment uses a fixed random seed (1) and runs indefinitely so operators can watch fleet dynamics settle into steady state.

## Resources
- Maintenance Center: 1 (home base for all crews)
- Trucks (AUTO transport): 5
- Helicopters (AVIA transport): 2
- Turbines: 25 (demand generators)

## Key settings worth copying
- Time unit: Hours
- Space scale: 10 km per 100 model units (set via ScaleRuler, LengthUnits = KILOMETER)
- Transport type enum: {AUTO, AVIA} — lets routing logic branch cleanly on vehicle capability
- ServiceRequest agent carries a `type` parameter (TransportType) and a `turbine` reference, so the dispatcher knows both where to go and which vehicle class to use
- Random seed fixed at 1 for reproducible baseline runs
- 3-D assets loaded from DAE files; animation runs at real-time scale 1.0

## KPIs instrumented
- Dataset auto-collected every 1 hour (OccurrenceAtTime, RecurrenceCode = 1 HOUR) on both MC and ServiceRequest agent types — supports time-series plots of fleet utilisation and queue length
- Implicit throughput: count of ServiceRequests completed per simulation hour
- Fleet utilisation: fraction of trucks / helicopters in transit vs. idle at base

## Reusable idea
Encode dispatch decisions as a typed enum on the work-order agent itself (TransportType AUTO vs. AVIA). This keeps the dispatcher logic simple — it reads the field and routes the right vehicle class — and makes it trivial to extend with new vehicle types (boat, drone) without restructuring the flow.
