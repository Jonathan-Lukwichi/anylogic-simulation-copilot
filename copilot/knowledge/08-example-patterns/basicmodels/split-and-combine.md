# Pattern card — Split and Combine
- **Source:** AnyLogic example model "Split and Combine" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Take parts off a unit, work on the parts in parallel, and put them back on the same unit — here, four wheels off a car for tyre service and back on.

## Block chain
`Source` (a car every 3 min, first at start) → `MoveTo` (to the service bay, 5 km/h) → **`Split`** (*Number of copies* 4,
new agent type `Wheel`; each copy placed at `getNodeForWheel(indexCopy)`; *On at enter* hides the car's wheel group)
- original car (`out`) → `Combine.in1` — the car waits there;
- copies (`outCopy`) → `Delay` tyre service (2 min, capacity 4) → **`Batch`** (size 4) → `Combine.in2`;

→ **`Combine`** (*The resulting agent is* **agent1**, i.e. the car) → `MoveTo` (leave the bay; *On enter* shows the
wheel group again) → `Sink`.

## Resources
n/a (the service is a capacity-4 Delay).

## Key settings worth copying
- **Split** (Help 8.9.10): creates *Number of copies* new agents per original in zero time and sends them out of
  `outCopy`; the original leaves through `out`. In *New agent (copy)* and *On exit copy* the locals `original` and
  `indexCopy` (0…n−1) are available — use them to copy attributes (`agent.attribute = original.attribute`) or to give each
  copy its own place (`nodesForWheels.get(indexCopy)`). The count may be an expression.
- **Batch before Combine:** Combine joins exactly one agent from each port, so the four copies are first batched into
  one agent of size 4 = number of copies.
- **Combine** (Help): waits for one agent at each port in any order; result = completely new, **agent1** or agent2 —
  the other original is destroyed. Keeping agent1 preserves the car's identity and attributes. With a custom result type,
  set *Agent type (out)* under Advanced so later blocks see its fields.
- **Animation continuity:** hide the part shapes on the parent at split, show them again after reassembly.

## KPIs instrumented
None. Natural ones: time in bay per car (TimeMeasureStart/End around Split → Combine), parallel-service utilisation.

## Pitfalls
- **Combine does not match by identity.** It pairs whatever arrives first at each port. The Help recommends Combine
  only when there is one copy per original and the order in both flows is unchanged; otherwise store the original's ID
  on the copies and reunite with `Match`. The demo is safe only because one car is in the bay at a time and service time
  is fixed.
- **Copy count and batch size must agree.** If a copy is scrapped or diverted, the Batch never completes and the car waits
  at Combine for ever.
- The destroyed agent is not checked (Help): make sure it holds no seized resources when it enters Combine.

## Reusable idea
Disassembly → parallel work → reassembly: Split for the parts (with `indexCopy` for placement), Batch to regroup them,
Combine keeping the parent as agent1. Switch to an ID-based Match as soon as several parents can be in process at once.

## When the co-pilot should use this
Maintenance of multi-part assets (wheels, engine modules, pallet layers), sample splitting in labs, documents copied for
parallel approvals, patients whose samples go to the lab while they wait. Related: `match.md` (matching by condition),
`lead-acid-battery-production-phase-8.md` (Hold + Combine synchronisation), `station-and-crane-maintenance.md` (Split
to create a by-product).
