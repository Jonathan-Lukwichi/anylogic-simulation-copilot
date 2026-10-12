# Pattern card — Cross Belt Conveyor
- **Source:** AnyLogic example model "Cross Belt Conveyor" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Model a loop sorter whose carriers each hold a small belt that loads an item from an induction line and ejects it sideways into its destination chute (cross-belt sorter; the same scheme fits tilt-tray and pocket sorters).

## Block chain
- **Carriers as agents.** Agent type `BeltSegment` owns a short **belt conveyor** `belt` (5 m/s) with a centre position whose *On leading edge enter* calls `belt.stop()`. Inside it: `Enter` → `Convey` along `belt` (*leave conveyor on exit*, *removed from space*) → `Exit` (`main.enter.take(agent)`).
- **The loop.** Main's two **cell conveyors** (`acceptConv` and the loop `conveyor`) carry the carriers: `Source` (manual; *inject* = `getNumberOfCells()` at start) → `Queue` → `Convey` → `Convey` → back to the first `Convey`, forever.
- **Items.** `Source` → `Queue` → `Hold` (initially blocked) → `SelectOutput5` (three induction lines) → `Convey` to the end of each induction conveyor (*leave conveyor on exit*, *removed from space*) → `Exit` (`agent.beltSegment.enter.take(agent)`) — the item enters its carrier's own flowchart and space.
- **Discharge.** Back in Main: `Enter` → `Queue` → `Convey` along `agent.exitConveyor` (the chute chosen at release) → `Sink`.

## Resources
n/a — the carriers are the capacity (one item per carrier).

## Key settings worth copying
- **Carrier count = cells:** for each cell conveyor, `length(METER) / (getCellSize(METER) + getGap(METER))`, summed and injected once.
- **Fast fill, then run:** both cell conveyors start at 100 m/s so the carriers spread around the loop at once; when the carrier queue empties, `setMaxSpeed(1, MPS)` on both and `hold.unblock()` the item flow.
- **Induction:** a Position on conveyor near the end of each induction line is a stop (`…_block`). Edge callbacks keep it blocked — it is blocked as an item approaches while nobody is held there, and it re-blocks itself when a released item's trailing edge leaves. A position on the loop at each induction point fires as each carrier passes: if that carrier's belt is empty and an item waits at the stop, the item is assigned (`item.beltSegment = carrier`) and the stop `unblock()`ed.
- **Discharge:** a position on the loop at each chute; when a carrier passes with a load whose `itemType` matches the chute, `releaseItem` stores the chute in `exitConveyor` and calls `belt.run()`, so the item rides off the carrier's belt, leaves its space and is re-entered on the chute conveyor in Main.
- Item destination: `itemType = uniform_discr(1, 10)`; a colour per type.

## KPIs instrumented
Entry-stop colours (red while blocked). Worth adding: sorted items per hour, share of loaded carriers, waiting time at each induction stop, laps per item.

## Pitfalls
- **The side transfer is logical.** Once a carrier is assigned, the item reaches it by `Exit` → `enter.take` whatever the carrier's position by then; induction rates are optimistic unless an induction window or time is modelled.
- Chute capacity is not checked before `belt.run()`; check the chute (or let the item stay on board and try again on the next lap) if chutes can fill up.
- The fast-fill period is warm-up: start statistics after `hold.unblock()`.
- Carriers must match the cells exactly; the count is recomputed from the drawn lengths, so keep cell size and gap consistent when editing the loop.

## Reusable idea
Moving equipment that carries its own conveyor (sorter carriers, shuttles with belts, transfer carts) = an agent with its own conveyor network, carried by the main network; move items between networks with *leave conveyor / removed from space* on one side and `Exit` → `enter.take` → `Convey` on the other, and let position sensors do the control.

## When the co-pilot should use this
Parcel hubs and e-commerce sortation (cross-belt, tilt-tray), any loop with fixed carriers and induction/discharge logic, or any hand-off between conveyor networks in different agents or levels. Related: `videos/mhl-conveyor-control-sensors-and-breakdowns.md` (position sensors), `videos/mhl-convey-routing-offsets-leave-on-exit.md`, `order-picking-line.md` (joining networks by ports).
