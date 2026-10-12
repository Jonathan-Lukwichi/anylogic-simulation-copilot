# Pattern card — Replicated shapes and group pivots: grids, rings and clickable maps from one drawn shape
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 12 "Presentation and animation: working with shapes, groups, colors" — distilled, original wording
- **Paradigm:** Method (presentation)
- **Problem it solves:** Draw and animate N similar items whose number or state comes from data (seats, bays, slots, beds, cells) without drawing N shapes by hand.

## Mechanism
- **Replication.** Put an integer expression in Advanced → *Replication* to get that many copies. The variable `index` (0 … N−1) is then available in every dynamic field of the shape (Help, Big Book p. 33). The count may be a variable.
- **Layout by index.** A grid of 10 per row: `X: 100 + 50 * (index % 10)`, `Y: 100 + 50 * (index / 10)` (integer division). A dynamic X or Y replaces the drawn position completely, so include the origin offset (pp. 34–35).
- **State by index** (pp. 36–37):
  - add a variable `boolean[] sold = new boolean[50]`;
  - set the Fill color to `sold[index] ? red : limeGreen`;
  - set *On click* to `sold[index] = true;`, since `index` is in scope in *On click*. A click reaches only the topmost shape under the cursor (Help).
- **Count and fields from a collection.** Replication `object.size()` with fields such as `object.get(index).x` binds each copy to one element (Help *Animating replicated objects*).
- **Rings.** Replicate a *group* and rotate it `index * PI / 6`; the group origin is the pivot (pp. 38–39). Copies are drawn in index order, so the last one is on top.
- **Moving a pivot.** A shape rotates and scales about its own origin (the upper-left corner, for a rectangle). To move the pivot:
  1. wrap the shape in a one-shape group;
  2. use *Select Group Contents* and move the contents until the group origin sits where the pivot should be (p. 18).

  A group also gives its members a local coordinate system: move the group, and the members' coordinates stay as they are (p. 19).
- **Groups at runtime.** `ShapeGroup` offers `size()` and `get(i)`. `get(i)` returns an Object (a Shape subclass or a ReplicatedShape), so test it with `instanceof`. It also offers `add(shape)` and `remove(shape)`, and `shape.getGroup()` finds a shape's group. Every agent's top-level groups are `presentation` and `icon` (pp. 20–21).
- **Configure the model from the drawing.** In On startup, loop over `presentation` and collect shapes by class and property (e.g. every `ShapeOval` with a red fill) into a collection, then let the logic use them. On startup runs after all graphics exist (p. 43).

## Resources
n/a

## Key settings worth copying
- **Visible cannot hide single copies.** It is evaluated before Replication, so false hides all of them. To hide some copies, return `null` for their line and fill colours *(Big Book p. 34; not restated in Help 8.9.10)*.
- **1-based labels:** replicated text with Text `1 + index`.
- **Rotation limits:** controls, charts and 3D windows inside a rotated group move with it but do not rotate (p. 17).
- **Levels:** shapes on different levels cannot share a group; adding a shape to a group moves it to the group's level (p. 16).

## KPIs instrumented
n/a

## Pitfalls
- **Array too short.** An array read with `index` must be at least as long as the replication count, including when the count grows at runtime *(inferred)*.
- **Replicating agents by hand.** Agents in populations, and the agents of library blocks, animate themselves. Use replication for things that are not agents, such as seats, slots, sensors or labels (p. 33).
- **No names for copies.** A replicated copy cannot be addressed by name; reach it through its index-driven fields or the group API.

## Reusable idea
One drawn prototype, plus index arithmetic, plus an array for state, gives an interactive map of any size. A group origin is the only pivot you ever need.

## When the co-pilot should use this
- Seat maps, parking bays, storage or rack slots, bed boards, dials, small heatmaps, row and column labels.
- Laying out a model from drawn markers (collect shapes at startup).
- Related: `bigbook/animation-dynamic-properties-and-frame-cost.md`, `videos/agent-type-graphics-visible-on-upper-agent.md`, `videos/flowchart-block-animation-binding.md`.

## Additions (8.9.10 review, 2026-10-01)
- Changing a replication count rebuilds every copy, so state set on a copy through its API is lost — keep per-copy state in an array. For replicated controls read by other shapes, call `createShapes()` in the container's On startup (Help 8.9.10 *Replicated controls*; gotcha G113; `controls-link-direction-sync-and-replicated-controls.md`).
