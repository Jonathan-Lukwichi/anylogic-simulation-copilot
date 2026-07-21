# Pattern card — Areas with Limited Access for Transporters
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Controlling transporter (AGV/crane) movement in a manufacturing facility by restricting access to specific floor zones based on capacity, equipment activity, door state, or vehicle type.

## Block chain
Multiple parallel material flows each follow the pattern:
Source → MoveByTransporter (or MoveByCrane) → optional Delay → Sink

A second set of flows introduces Queue blocks before movement to buffer loads waiting for a restricted zone to clear. The TransporterFleet block governs each fleet (standard AGVs and HeavyLoadAGVs are separate fleets), and RectangularNode / PolygonalNode markup elements on the space markup carry the access-restriction settings that gate transporter entry.

## Resources
- Two TransporterFleet pools: one for standard AGVs, one for HeavyLoadAGV units.
- Node capacity limits (integer slots) on intersection nodes control simultaneous occupancy.
- Crane ownership of a zone acts as a binary lock — no AGVs may enter while the crane is active there.
- Door/gate nodes toggle open/closed to allow or block particular routes.
- Zone type-filters restrict entry to only the matching AGV class.

## Key settings worth copying
- Arrival rate at primary Source: `triangular(3, 4.5, 6)` seconds between arrivals (time unit: Second).
- Secondary flow arrival count drawn from `uniform_discr(2, 3)` — models variable batch pickup sizes (KITSet agents).
- Access restriction modes available on a node: **capacity limit**, **equipment lock**, **door/gate toggle**, **vehicle-type filter**, and **congestion-reduction buffer zone**.
- Separate TransporterFleet blocks for each AGV class keeps routing logic clean and avoids cross-fleet interference.

## KPIs instrumented
- Visual congestion near loading/unloading docks (observable in the 2-D animation).
- Implicit throughput: items reaching Sink blocks across each sub-flow.
- Queue length at buffer nodes ahead of restricted zones (Queue block content).
- Interactive controls let the user toggle restrictions at runtime and observe flow-rate changes directly.

## Reusable idea
Attach access-restriction policies directly to space-markup nodes rather than coding logic in agent behavior — this cleanly separates *where* constraints apply from *what* the transporter does, making it trivial to add, remove, or switch restriction types (capacity cap → door lock → type filter) without touching the process flowchart.
