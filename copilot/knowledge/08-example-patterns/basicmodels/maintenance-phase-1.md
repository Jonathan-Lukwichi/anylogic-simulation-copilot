# Pattern card — Maintenance - Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Deciding how to dispatch repair crews (ground truck vs. helicopter) to failing wind turbines scattered across a large geographic area.

> **Verified corrections (2026-10-01).** Checked against the shipped 8.9.10 example `.alp` and the tutorial text (AnyLogic Help tutorials, *AnyLogic in 3 Days*). Where they differ from the text below, these win.
> - `center` is a single MC agent, not "Maintenance Centres: 100 (field capacity)". Trucks run at 70 km/h and helicopters at 200 km/h (not a 10 m/s default).
> - Scale: in phases 1, 2 and 7 Main uses 5 px per **km**; MC, Turbine and Truck use 10 px/km and Helicopter 5 px/km. "10 px per m" is only the untouched default of the animation-less `Transport` type, and "10 km per 100 model units" is the agent types' scale, not Main's.
> - Readable 3D in a km-scale world: each agent type has its own explicit scale (Help 8.9.10 *Scale*: different agents may have different scales) with *Resize automatically to match agent scale* unticked and an *Additional scale* (Help *3D object*); subtypes can untick the scale's *Inherited from parent*; parts of a grouped figure are re-placed in code, e.g. blades Z = `22.25 * Scale.DEFAULT_SCALE.pixelsPerUnit(METER)`.

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
