# Pattern card — Pedestrian Attractors
- **Source:** AnyLogic example model "Pedestrian Attractors" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Seat pedestrians at individual places (seats, desks, stands) inside a waiting area, hold them until released, and animate them sitting.

## Block chain
`PedSource` (at most **336** arrivals = the number of seats; custom population `person`) → `PedWait` (area node with attractors; *Attractor choice* **Free**; delay type **manual**; *On begin wait* `ped.sitDown()`) → `PedGoTo` exit (*On enter* `ped.standUp()`) → `PedSink`. A button "Leave the hall" calls `pedWait.freeAll()`.

## Resources
The rectangular area's **attractors** act as seats (laid out in a grid alongside replicated table shapes).

## Key settings worth copying
- *Attractor choice* (`attractorChoice`): `ATTRACTOR_CHOICE_NONE`, `…_RANDOM`, `…_FREE` (free attractors are taken first), `…_CUSTOM` (an expression per pedestrian).
- Manual delay: pedestrians wait until `free(ped)` / `freeAll()`; timed delays can instead be counted from reaching the waiting point or from entering the area.
- `cancel(ped)` / `cancelAll()` send pedestrians out through the **`ccl`** port, with *On cancel* per pedestrian — an emergency exit path separate from `out`.
- Pose switching: the pedestrian's 3D figure plays the pose names in a `String[] poses` variable; `sitDown()` swaps it to `{ "sit" }`, `standUp()` back to the walking set.

## KPIs instrumented
Visual only.

## Pitfalls
- With *Random* choice two pedestrians can target the same attractor; use *Free* when attractors are single-occupancy seats.
- *Free* only makes pedestrians *first* choose free attractors (Help) — so when all are taken, extra pedestrians presumably share occupied ones *(inferred)*; cap arrivals (here 336) or gate the area when seats are hard capacity.

## Reusable idea
Treat attractors as named places inside an area and PedWait's attractor choice as the seat-assignment rule; release by code (manual delay) or divert with `cancel` to an emergency route.

## When the co-pilot should use this
Waiting rooms, lecture halls, stadium seating, restaurants, workstations — whenever pedestrians occupy specific spots rather than just standing in an area.
