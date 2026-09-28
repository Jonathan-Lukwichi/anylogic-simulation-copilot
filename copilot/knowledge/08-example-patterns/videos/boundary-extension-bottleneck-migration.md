# Pattern card — Boundary one interface past the lever (bottleneck migration)
- **Source:** AnyLogic video "Webinar | How Simulation-Driven Insights Strengthen Strategic Decision-Making" (https://youtu.be/UVppYf_O4H8) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** An improvement tested inside the modelled area can push the constraint just outside the model boundary, where no KPI can see it.

## Mechanism
- **The case (inbound distribution centre):** a client first modelled only the inside of the building to set worker numbers. The winning plan cycled trucks faster, and congestion then built up in the truck traffic outside the building, beyond the model. The webinar's proof-of-concept model inspired by that case spans both sides: gate security inspection for a subset of trucks, on-site truck routing, docks, and the inbound floor (put-away vs unpack decision, unpack stations, temporary storage when a station is busy, forklifts for pallets, AGVs for tote replenishment and empty-pallet removal). Outbound is deliberately cut: once an order releases a tote, it simply leaves.
- **Rule:** a lever that changes a flow *rate* (turnaround, release timing, throughput) changes the load on the neighbouring interfaces. For each lever, ask at intake: "if this works, where does the faster or larger flow land next, and can that place absorb it?" Extend the boundary to that interface at the lowest fidelity that can form a queue (a capacity, a queue, a KPI). Collapse everything beyond it into a `Source`/`Sink`.
- **Scenario set that exposes it:** baseline, lever on, reduced resources (the "budget cut": fewer docks, inspection crews, forklifts, pack stations), and a peak arrival wave. Judge every scenario on internal *and* boundary KPIs.

## Resources
Boundary stubs are ordinary PML resources: an inspection-crew `ResourcePool`, a dock `ResourcePool`, a finite yard `Queue`. Internal pools are unchanged.

## Key settings worth copying
- Stub chain: `Source` (trucks, arrivals with the peak wave) → `Queue` (yard, capacity = slots) → `SelectOutput` (inspection needed?) → `Service` (inspection, crew pool) → `Seize` (dock) → in-scope inbound logic → `Release` → `Sink`.
- One parameter per boundary capacity (`numDocks`, `numInspectionCrews`, `numForklifts`, `numPackStations`), applied with `pool.set_capacity(n)`. The budget-cut scenario then becomes a parameter set, not a model edit.
- Model the interface with PML first. Move to the Road Traffic Library only if vehicle interaction on site roads is itself part of the question.
- Tie each dock shape's *Visible* or fill-colour expression to the capacity parameter, so the animation matches the scenario being shown.

## KPIs instrumented
- Boundary: trucks waiting on site (max and time-average), truck turnaround (arrival → exit), inspection wait.
- Internal: dock-to-storage time, station and forklift utilisation, pallets in temporary storage.
- Report both sets for every scenario. Internal KPIs improving while boundary queues grow is a relocated bottleneck, not a gain.

## Pitfalls
- Scoring scenarios on internal KPIs only: the moved bottleneck stays invisible.
- Average conditions hide it. In the demo the on-site truck queue stayed near zero for most of the run and only built up when the peak wave met reduced capacity.
- Capacity removed by a parameter still shows in the drawing (the demo said so openly). Stakeholders read the picture literally and then doubt the numbers.
- Over-extending: detailing the whole site road network when a capacitated queue answers the question.

## Reusable idea
Draw the boundary around the decision, then push it one interface further wherever the lever changes a flow rate. Model that interface cheaply, instrument it, and report it next to the internal KPIs.

## When the co-pilot should use this
- Stage 0, item B6 (boundaries), whenever a lever speeds up or enlarges flow through a subsystem (warehouse inbound, theatre turnover, ED discharge, a line upgrade).
- When a user says the model "proved" a fix but the problem reappeared somewhere else.
- When listing scenarios: add reduced-resource and peak-wave cases, and name the boundary KPIs explicitly.
