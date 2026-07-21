# Pattern card — Airline Fleet
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (agent-based with discrete-event elements)
- **Problem it solves:** Determines the optimal monthly spare-parts order size to minimise combined downtime costs and on-hand inventory costs for an airline fleet.

## Block chain
Each aircraft in the fleet is an agent (class `Plane`) that carries its own collection of `Equipment` spare parts, each of which can be in states such as In-Use, Broken, or Repaired. When a random breakdown event fires, the affected plane transitions to a BROKEN state and one of its installed spares is marked Broken. Repair shops work through the broken spares queue; once fixed, the spare is returned to the plane and the plane can resume flying. Separately, a monthly procurement cycle fires on a calendar schedule: for each spare-part type the model places a bulk order whose size is a user-controlled slider (`monthlyOrderSize[]`). Users may also trigger one-off emergency purchases at any time. An optimisation experiment sweeps the monthly order quantities to find the combination that minimises total cost.

## Resources
- `fleet` population of `Plane` agents (number configurable; each holds a sub-population of `Equipment` spares)
- `Flight` population representing scheduled routes assigned to aircraft
- `schedule` agent managing the flight timetable
- Repair technicians implied by `repairTime` parameter per equipment type (no explicit ResourcePool block — capacity embedded in repair-time table)

## Key settings worth copying
- Breakdown inter-arrival time: `triangular(timeBetweenBreakdowns, 2*timeBetweenBreakdowns)` — asymmetric triangular giving a realistic right-skewed failure interval
- Per-spare repair time looked up from a data table (`order_db`) keyed on equipment type
- Monthly order quantity: integer array `monthlyOrderSize[]`, one entry per spare category, driven by sliders for interactive experimentation
- `uniform_discr(100, 1000)` for random spare serial numbers; `uniform_discr(100000, 999999)` for flight IDs
- Time unit: **Minute**; cost flows tracked in **PER_DAY** and **PER_MINUTE** rates
- Downtime penalty charged as `35000 * freePlanes.size()` per day an aircraft is grounded waiting for a spare

## KPIs instrumented
- `downtimeCosts` — cumulative penalty for grounded aircraft (lease of replacement capacity from third-party airlines)
- `costOfOnHandInventory` — running value of spares stock on hand, reset monthly to isolate period cost
- `inventoryPurchase` — total spend on parts ordered (monthly bulk + emergency singles)
- `monthlyOrderSum` — cost of the current month's bulk order
- `singleOrderSum` — cumulative emergency purchase spend
- Breakdown count per spare type (chart: repaired counts filtered by type)

## Reusable idea
Pair a **user-controlled order-quantity slider** with an **optimisation experiment** over the same parameter: the interactive mode lets a domain expert explore policy intuitively, while the optimiser confirms or improves on that intuition automatically — a two-layer decision-support pattern applicable to any inventory or staffing problem where the optimal level is non-obvious.
