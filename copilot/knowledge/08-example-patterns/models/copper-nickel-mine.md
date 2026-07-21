# Pattern card — Copper Nickel Mine
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Sizing and scheduling underground mining fleets (jumbos, chargers, LHDs, trucks, roof bolters) for room-and-pillar ore extraction while enforcing a mine-wide blast synchronization barrier.

## Block chain
Rooms in a mine panel move through a strict sequence: drilling → charging → blast wait → loading → hauling to ore pass → roof bolting. Each room is an entity that seizes specialist equipment at each stage. When charging for every room in the panel is complete, a panel-level gate fires: all active machines are interrupted and must return to the equipment station before blasting can occur. After the blast delay the fleet redeploys and the cycle restarts for the next panel. The hauling leg uses a dedicated `HaulProcess` sub-model with `MoveInMine` blocks to track travel along mine roadways. A `SelectOutput` block after the blast event routes entities either to release seized rooms or to seize new ones, depending on whether the panel is finished.

## Resources
- **Jumbo drills** — ResourcePool, configurable quantity, seized during drilling
- **ANFO chargers** — ResourcePool, seized during charging
- **LHD (Load Haul Dump) units** — ResourcePool, paired with mine trucks for the haul cycle
- **Mine trucks** — ResourcePool, paired with LHDs; quantity set via "LHD & truck pairs qty" parameter
- **Roof bolters** — ResourcePool, seized during bolting
- All pools surface through `getResourcePools()` and `getResourcePoolsWithWork()` helper functions so the blast-recall logic can interrupt every active unit at once.

## Key settings worth copying
- **Drilling time:** `uniform(110, 150)` minutes per room
- **Charging time:** `uniform(55, 75)` minutes per room
- **Bolting time:** `uniform(100, 140)` minutes per room
- **Time unit:** Minutes
- **Panel blast gate:** a boolean flag checked after each charging completion; only when all rooms in the panel are charged does the blast sequence trigger — modelled as a `blastDemandsSource` that releases a single token to proceed
- **Continuous mode toggle:** a parameter lets the run either stop after one panel (for clean single-cycle statistics) or loop through multiple panels indefinitely (cloud/long-run mode)
- **Fleet recall:** active resource tasks in `{ drilling, charging, bolting }` are interrupted via `SingleOperation` cancel actions; machines then navigate back via `MoveInMine` before the blast `Delay` begins

## KPIs instrumented
- **Drilling time statistics** — `drillingTimeStat` histogram/dataset
- **Hauling time statistics** — `haulingTimeStat` histogram/dataset
- **Mine panels excavated** — counter `nPanels` displayed on dashboard
- **Equipment utilisation** — colour-coded 3-D mine view distinguishes "useful work at face" vs. travel vs. idle/waiting states

## Reusable idea
The **blast synchronization barrier** pattern: use a token-gate source (`blastDemandsSource`) that only fires after a counted set of upstream tasks all complete, then broadcast an interrupt to every active ResourcePool before resuming. This is directly transferable to any process that requires a full-fleet or full-batch hold before a shared critical event (e.g., a kiln charge, a sterilisation cycle, a shift-change lockout).
