# Pattern card — Choosing Closest Resource
- **Source:** AnyLogic example model "Choosing Closest Resource" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Decide *which* unit of a resource pool serves a request (here: the nearest idle vehicle) instead of accepting whatever unit the pool hands out.

## Block chain
Two streams — `Source` at `enter1` (0.5/s) and at `enter2` (0.2/s), each followed by `MoveTo` its processing area — merge into one `Seize` (*Send seized resources* and *Attach seized resources* ticked; *Customize resource choice* ticked with the condition `findClosest(agent, (Transporter) unit)`) → `Delay` *processing* (triangular 3 / 5 / 7 s) → `Release` (wrap-up: return home only if no other task) → `MoveTo` exit → `Sink`.
`findClosest` scans the pool's population for idle units, finds the smallest `distanceTo`, and returns true only for a unit at that distance — so only the nearest idle unit passes the condition.

## Resources
`ResourcePool` of 5 `Transporter` units (custom population `transporters`), home nodes `home1`, `home2`. Unit animation switches with `isBusy()` / `isIdle()`.

## Key settings worth copying (Help 8.9.10, *Seize*)
- **Filter vs rank.** *Resource choice condition* (`customizeResourceChoice`) says which units are *allowed* (skill, zone, `agent.myAssistant == unit`); if no available unit passes, the agent waits for the first unit that does. **Resource selection** (`dispatchingPolicy`) *ranks* the allowed units: `Seize.RESOURCE_SELECTION_NEAREST` (nearest to the agent), `…_NEAREST_BY_ROUTE` (GIS routes), `…_BASED_ON_COMPARISON` ("unit1 is preferred to unit2", must be transitive), `…_BASED_ON_RATING_VALUE` (unit rating; largest wins).
- For "closest", "longest idle", "least used" or "highest skill", prefer *Resource selection* over the example's trick of computing a minimum inside the condition.
- `seize.recalculateResourceChoiceConditions()` (or the per-agent overload) re-tests waiting agents when something the condition depends on has changed.

## KPIs instrumented
None in the demo. Worth adding: pool utilisation, waiting time inside the Seize, and empty travel per job (time from seize to the unit's arrival).

## Pitfalls
- **Hard-coded search radius.** The example starts its minimum at 1000; if every idle unit is farther away, nothing equals the "minimum", the condition is false for all units and the agent waits although units are idle. Start from `Double.POSITIVE_INFINITY` — or use the built-in policy.
- **Cost.** The condition runs once per candidate unit, and each run scans the whole pool: quadratic in pool size per request.
- **Straight-line distance.** `distanceTo` ignores the network; on winding layouts the "nearest" unit can have the longest drive (compare G44). Whether *Nearest to the agent* in Seize uses straight-line distance is not stated in Help *(unverified)* — use a comparison on route length where it matters.

## Reusable idea
Separate eligibility (condition) from preference (selection policy). Dispatch rules then become explicit, testable model inputs — and can be compared as scenarios, like any other policy (`videos/dispatching-rule-as-optimizable-policy.md`).

## When the co-pilot should use this
Porters, mobile nurses, forklifts, service technicians — any pool whose units are spread out in space or differ in skill; when a user asks "how do I make Seize pick the nearest / least busy / specific unit?". For MHL transporter fleets see `videos/mhl-agv-dispatch-choice-and-cargo-position.md`.
