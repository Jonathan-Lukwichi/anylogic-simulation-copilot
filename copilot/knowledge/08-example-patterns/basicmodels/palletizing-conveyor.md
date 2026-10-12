# Pattern card — Palletizing Conveyor
- **Source:** AnyLogic example model "Palletizing Conveyor" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling + Process Modeling)
- **Problem it solves:** A layer palletiser: items arrive on one belt, are split over three lanes, grouped into rows, arranged into a 3 × 3 layer, and the layers are stacked on a pallet until it is full.

## Block chain
`Source` (1 item / 2 s, first at 1 s, custom population `items`) → `Convey` to **custom station** `horizontalBatchStation`, forced through one of three split conveyors with *Conveyors to include* = `{ getConveyor(agent) }` (lane = `item.getIndex() % 3`) → `Delay` (manual, capacity 3; *On enter*: when 3 are present, `stopDelayForAll()`) → `ConveyorExit` → `Hold` (blocks itself after 9) → `MoveTo` an attractor slot (`node.getAttractors().get(index % itemsPerLevel)`) → `Batch` (9 items → one layer agent, 3 × 3 m; *On exit* re-opens the Hold) → `Convey` the layer (turned `AGENT_ORIENTATION_LEFT`) to custom station `verticalBatchStation`, removed from the conveyor → `MoveTo` *place to* `palletNode` with `offsetZ = 10 + 10 * currentPallet.nLevels` → `Assembler` in2. Pallets: `Source` (manual, first injected at start) → `Convey` empty pallet to the vertical station → `Assembler` in1 (1 pallet + 5 layers, 1 s) → `Convey` full pallet → `Sink`; *On exit* injects the next pallet.

## Resources
n/a (no operators; the conveyor network, two Custom Stations and the pallet node carry the process).

## Key settings worth copying
- **Force a lane:** Convey *Conveyors to include* — conveyors the automatic route must pass through, in the given order (Help); a round-robin lane from `getIndex() % nLanes`.
- **Leave the belt at a Custom Station:** Convey target type *custom station* (`TARGET_CUSTOM_STATION`); for the layer, *Leave conveyor on exit* with removal so PML blocks take over.
- **Release in groups:** manual `Delay` + `stopDelayForAll()` when the group size is reached; a self-blocking `Hold` (`BLOCK_AFTER_N_ENTITIES`) admits exactly one layer's worth, re-opened by the `Batch` exit.
- **Layer pattern from attractors:** place each item on attractor `index % itemsPerLevel` of an area node before batching, so the batch agent's animation shows a real layer.
- **Stack height from a counter:** `MoveTo` with *offset* (`useOffsets`, `offsetZ`) grows with `nLevels`, incremented in Assembler *On enter 2*; the current pallet is remembered in *On enter 1*.

## KPIs instrumented
Visual only (3D view).

## Pitfalls
- Grouping by `getIndex() % k` assumes items are never removed from the population out of order; with dynamic populations use a counter instead.
- The single `currentPallet` variable works because one pallet is on the stacker at a time; parallel stackers need the pallet stored per station.
- Items must be off the conveyor (ConveyorExit / leave-on-exit) before PML movement blocks (`MoveTo`, `Batch`) animate them, or the two libraries fight over the position.

## Reusable idea
Palletising, case packing and layer-building lines decompose into: lane choice (`Conveyors to include`), exit at a custom station, grouping (manual Delay / self-blocking Hold), spatial arrangement (attractors), `Batch` to a layer agent, and `Assembler` with a height offset per level.

## When the co-pilot should use this
End-of-line packaging (palletisers, case packers, stackers), and any time items must leave a conveyor to be grouped and then return as a new unit. For a robot/AGV-served palletising cell see `models/palletizing-system-with-agv.md`; for leave-on-exit details see `videos/mhl-convey-routing-offsets-leave-on-exit.md`.
