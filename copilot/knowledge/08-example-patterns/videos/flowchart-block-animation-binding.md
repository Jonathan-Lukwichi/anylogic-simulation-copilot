# Pattern card — Animating a PML flowchart: bind each block's Agent location, and know the layout rules
- **Source:** AnyLogic video "How to add 3D animation in your models" (https://youtu.be/L5SD_QdUUKE) — distilled, original wording
- **Paradigm:** DES (Process Modeling Library presentation)
- **Problem it solves:** A logically correct flowchart shows nothing moving, or shows agents piled on one spot or queued the wrong way round, because PML blocks do not animate agents by themselves.

## Mechanism
- **The principle.** PML blocks have **no built-in animation**. Every block that holds agents for non-zero time needs a space-markup shape (a path or node) selected in its **Agent location** property. The video draws a path and assigns it to the `Conveyor` block of Source → Queue → Conveyor → Sink.
- **Zero-time blocks need none.** SelectOutput, Release, ResourceAttach and the like hold agents for zero time (Help 8.9).
- **Composite blocks have one field per phase.** Service has **Agent location (queue)** and **Agent location (delay)**. Set both.
- **Already in the KB:** a Delay bound to a node (`anylogic-in-3-days.pdf` p. 176, and G4's Service "Agent location"). The layout rules below are what this card adds.

## How each shape lays agents out (Help 8.9)
| Shape | Agents are drawn… |
|---|---|
| Point node | all at the same point, so they overlap |
| Rectangular/polygonal node, layout *Random* | at random spots, any number |
| Rectangular/polygonal node, layout *Arranged* | laid out on a grid sized to the node (normally up to the block's capacity); a new agent takes the first free cell |
| Node with attractors | at the attractor positions |
| Path on a Delay, Conveyor, etc. | travelling along the path, rotated to the segment's angle |
| Path on Queue, or on the queue inside Service, Seize, Batch or Match | standing in line: the **head (position 0) is at the path's END point**; spacing = path length / (capacity − 1), fixed at startup |

## Resources
Resource units animate the same way (home and location nodes). A unit attached to an agent appears next to it, slightly offset (Help 8.9).

## Key settings worth copying
- **Queue path direction.** Draw a queue path from the **tail toward the server**, so the head of the line stands at the server.
- **Queue capacity sets the spacing.** Match it to the length of the drawn line. The default of 100 on a short path crams agents together. With *Maximum capacity* ticked, the formula gives near-zero spacing, so agents effectively stack at the end point. *(Inferred from the documented formula.)*
- **3D.** Keep the shape's *Show in* at "2D and 3D" and add a 3D Window (see `videos/3d-scene-z-order-and-lighting.md`).

## KPIs instrumented
n/a (presentation). Animation also works as a validation instrument: an agent drawn in the wrong place is a wiring bug that statistics alone may hide.

## Pitfalls
- **A point node on a queue** draws every agent on the same spot, so a long queue looks like a single agent.
- **Changing queue capacity at runtime** does not re-space the drawn line.
- **Path Type = Conveyor, Road or Railroad is cosmetic only** (Help 8.9). A path drawn as a belt adds no conveyor physics. For accumulation, gaps and transfers, use the Material Handling Library conveyor (e.g. `basicmodels/conveyor-singulator.md`).

## Reusable idea
Treat animation as a thin binding layer on top of verified logic: build the flowchart first, then give each holding block one markup shape. Let the layout carry meaning: a line for a FIFO queue, a grid for a buffer or rack, a point for a single machine.

## When the co-pilot should use this
- **Triggers:** the user asks "why can't I see my agents?", reports agents stacked or queued backwards, or wants 2D/3D animation of a PML model.
- **Build phase:** Phase 5, after the logic is verified. This mirrors G4's "logic first, animate later".
- **Related:** `anylogic-gotchas.md` G4 and `videos/3d-scene-z-order-and-lighting.md`.

## Additions (8.9.10 review, 2026-10-01)
- Delay's *Restore agent location on exit* (`restoreEntityLocationOnExit`): unticked, the agent stays where the Delay's path or node left it — the ConveyorEnter demo lifts a pallet along a path this way (Help 8.9.10 *Delay*).
