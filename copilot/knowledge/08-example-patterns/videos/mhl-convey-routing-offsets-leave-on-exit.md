# Pattern card — MHL conveyor networks: ConveyorEnter vs Convey, leading-edge offsets, route control, Leave conveyor on exit
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Drive items through a multi-conveyor network with a thin flowchart: where they enter, where they stop, which route, and whether they keep occupying the belt.

## Block chain
The webinar's two-entrance line: `Source` → `SelectOutput` (70/30) → two `ConveyorEnter` (north / south entrance conveyors, offset 0) → one `Convey` (**Convey from = Current position**, target = end of the main conveyor, offset 0) → `Sink`.
- **Build in three steps.** Draw the markup, build the flowchart, then bind the blocks to the markup. It is the same split as the PML, Pedestrian, Rail and Road libraries.
- **`ConveyorEnter` only places the item.** From that moment the item takes up space and interacts with other items, but it does not move. **`Convey` is the only block that moves items inside a conveyor network.**
  - A lone `Convey` can do both jobs: set Convey from = *Conveyor* or *Position on conveyor*.
  - Splitting Enter and Convey makes separate entrances explicit, and lets PML blocks (colouring, decisions) sit in between.
- **One `Convey` crosses the whole network** by the shortest route: spurs, transfer elements and stations included. An item whose route passes a Station is processed there with no extra block.

## Resources
n/a. Conveyors are markup, not resource pools. For operators, see `videos/mhl-conveyor-station-processing-and-reassembly.md`.

## Key settings worth copying (Help 8.9 labels)
- **Offsets are measured to the item's leading edge.**
  - *Source offset from* defaults to the **beginning** of the conveyor.
  - *Target offset from* defaults to the **end**, so "target = conveyor X, offset 0" stops the item's nose exactly at X's end.
  - `ConveyorEnter` and `Convey` put the **leading edge** on a Position on conveyor when placing there.
- **Route is:**
  - *Calculated automatically* (shortest), optionally with **Avoid conveyors** / **Include conveyors** (`ConveyorPath[]`). Included conveyors are used in list order, so that route must exist.
  - *Sequence of conveyors*: give the full list, including the source and target conveyors. It may not contain reversible conveyors.
- **Per-item target:** switch *Target conveyor* to a dynamic value, e.g. `agent.passed ? conveyorNorthEnd : conveyorSouthEnd`. For decisions *while moving*, chain several `Convey` blocks with `SelectOutput`s between them.
- **Leave conveyor on exit** (Java `removeFromConveyor`). "Leave" means *depart*.
  - Unticked (the webinar's default): the item stays on the belt at its target point after exiting `Convey`, still occupying space.
  - Ticked: the item is removed from the network. **Exiting agents** = *stay where they are* / *are removed from space* (animation only).
- **`outRedirect` port:** items leave through it when the conveyor reverses direction, or after `cancel(agent)` / `cancelAll()`. Connect it whenever you use either.
- **Item size:** 1 × 1 × 1 m by default. Override it in the type, in Source (Agent → *Set dimensions*), in `ConveyorEnter` (*Set dimensions*), or at runtime with `agent.setDimensions(l, w, h, METER)`. Gaps and belt capacity use these modelled sizes, not the 3D shape.

## KPIs instrumented
The webinar shows no KPIs. Suggested:
- `conveyor.getUtilization()`, `conveyor.getState()` (`MOVING_EMPTY`, `TRANSPORTING`, `STOPPED`, `FAILED`…), `conveyor.size()`, `convey.size()`.
- Item position: `agent.getLeadingEdgeOffset(METER)`, `agent.getTrailingEdgeConveyor()`, and `agent.getConveyors()` (an item can straddle two conveyors).

## Pitfalls
- **Ghost items.** Items passed from `Convey` to a holding block (Batch, Queue, Service, Hold) without *Leave conveyor on exit* keep blocking the belt behind them. Tick it, or add `ConveyorExit`, when items truly leave the line.
- **Items only move while inside `Convey`.** An item parked on the belt in another block (the webinar's inspection `Service`) holds its spot, and roller-conveyor followers queue behind it. On belt or cell types the whole conveyor should stop *(inferred from the type definitions; verify)*.
- **No internal buffer.** A `Source` feeding `ConveyorEnter`/`Convey` needs Forced pushing off **and** *wait*, or a Queue; see `videos/spiral-conveyor-per-point-z.md`. The webinar chose *destroy*, which silently drops arrivals.
- **"End" follows the drawing direction.** The first point drawn is the start; right-click → *Change Direction* reverses it.

## Reusable idea
Treat the conveyor network as a routing graph and keep the flowchart thin: one `ConveyorEnter` per physical entrance, and one `Convey` per decision point. Destinations become per-agent expressions. Merging, processing and turning live in the markup.

## When the co-pilot should use this
- Any conveyor, sortation or induction question in AnyLogic 8.9+. The PML `Conveyor` block is deprecated and hidden from the palette since 8.9.5, and it treats items as zero-size, so default to MHL (Help 8.9).
- Debugging "items stop or pile up at one point": check *Leave conveyor on exit* and the target offsets first.
- **Related cards:**
  - `basicmodels/conveyor-singulator.md`
  - `basicmodels/item-flow-control-on-a-reversible-conveyor-spur.md`
  - `videos/mhl-conveyor-types-spur-priority-transfer-elements.md`

## Additions (8.9.10 review, 2026-10-01)
- An offset can come from where something stands in free space: `scale.toLengthUnits(agent.getX() - conveyor.getStartPoint().x, METER)` (Help *Scale*), so a worker drops an item exactly beside themselves; equally spaced stop points on a belt are `k * (agent.getLength(METER) + conveyor.getGap(METER))` from the end (`getGap` = the conveyor's minimum gap). The Queue in front of `ConveyorEnter` holds the item while a passing item occupies the spot (8.9.10 *Put Agent in Arbitrary Point of Conveyor*).
- Worked reject idiom (Lead Acid Battery phase 5): a QA verdict in a Station's *On process finished* calls `convey.cancel(agent)`, and `outRedirect` → Convey (*Convey from: Current position*) carries the item to a reject conveyor. The port Help calls `outRedirect` is stored as `ccl` in the `.alp` connectors; check the generated name before wiring it by code *(unverified)*.
