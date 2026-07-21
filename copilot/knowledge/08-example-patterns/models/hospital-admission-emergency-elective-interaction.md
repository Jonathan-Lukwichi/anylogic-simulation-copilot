# Pattern card — Hospital Admission Emergency Elective Interaction
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how emergency and elective patient streams compete for a fixed pool of ward beds, revealing how surges in one stream force cancellations or delays in the other.

## Block chain
Three stock variables represent the main patient populations at any moment: patients waiting in the Emergency Department (ED), patients occupying ward beds, and patients on the scheduled elective admissions list. Flows connect these stocks: an ED admission rate drains the ED stock and fills the ward stock, while a ward discharge rate drains the ward. An elective admission rate also feeds the ward, but only when spare capacity exists. An occupancy-level auxiliary computes the gap between current ward census and fixed bed capacity; both the emergency and elective admission flows are capped by this gap using a `min()` constraint, so neither stream can push occupancy above capacity. When the ward is full, the elective admission rate drops to zero and a cancellation flow removes patients from the elective waiting list instead. A scheduling flow continuously replenishes the elective waiting list at a desired rate. The solver runs in Euler integration steps with time unit of days.

## Resources
- **Bed capacity:** single fixed parameter (`bedCapacity`) — no dynamic staffing in this simplified version
- **No agent populations or resource pools** — purely stock-and-flow aggregates

## Key settings worth copying
- `occupancyLevel = PatientsInWards - bedCapacity` (negative means spare capacity, positive means overloaded)
- Emergency admission rate: `min(PatientsInED * edAdmitFraction / patientTimeInED, -occupancyLevel)` — demand capped by available beds
- Elective admission rate: `min(-occupancyLevel, desiredElectiveAdmissionRate)` — electives only admitted into spare capacity
- Elective cancellation rate kicks in when occupancy is at or above capacity, pulling from the scheduled list
- Integration method: Euler; mixed equations fallback: RK45_NEWTON
- Time unit: Day
- Interactive sliders for `bedCapacity`, `desiredElectiveAdmissionRate`, and `edAdmitFraction` allow real-time policy experiments

## KPIs instrumented
- Ward occupancy level (bed utilisation proxy)
- Scheduled elective admissions stock over time (waiting list size)
- Implicit throughput: admission and discharge rates plotted as time-series

## Reusable idea
Use a single shared-capacity auxiliary (`occupancyLevel`) as a gating signal fed into every competing inflow via `min(flow_demand, -occupancyLevel)`. This one expression automatically prioritises emergency demand, throttles elective intake, and triggers cancellation logic — all without conditional branching — making it a clean, transferable pattern for any SD model where multiple demand streams contend for a capped resource.
