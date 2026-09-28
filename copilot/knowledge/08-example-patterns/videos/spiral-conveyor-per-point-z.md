# Pattern card — Spiral conveyor via per-point Z offsets (and feeding it without losing items)
- **Source:** AnyLogic video "How to simulate a spiral conveyor" (https://youtu.be/Wjx2xnFTj8I) — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Turn an ordinary Conveyor into a 3D helix (or any climbing path) with no special element, and feed it from a Source without push errors or silently lost arrivals.

## Mechanism
1. **Draw the plan.** Draw one Conveyor in plan view: a straight lead-in, two half-circle arcs for each full turn, then a straight run-out.
2. **Open the Points table.** Find it in the conveyor's properties. Each row is an offset (X, Y, Z) from the start point. Row 1 is always (0,0,0) and cannot be edited.
3. **Lift the helix.**
   - Leave the end of the lead-in at Z = 0.
   - Add a constant step to every arc point. The video uses +20 px per point, i.e. 40 px per turn.
   - Give the final run-out point the same Z as the last arc point so the belt leaves level.
4. **Check in 3D.** The 2D editor looks unchanged, so check the shape in a 3D Window at runtime.
5. **Add the logic.** `Source` → `Convey` → `Sink`. Set both the source and the target of `Convey` to this conveyor, so items ride it from end to end.

## Resources
n/a. There are no transporters or resource pools; the conveyor is the only asset.

## Key settings worth copying
- **Units.** Z values in the Points table are in pixels. Convert them with the diagram's Scale: at 10 px/m, 20 px is 2 m.
- **Source → Advanced.** Untick **Forced pushing** and set **Agents that can't exit = wait in this block**.
  - An item cannot enter while the previous one still covers the belt entry, so new arrivals have to queue inside the Source.
  - *Beyond the video:* AnyLogic's Material Handling tutorial uses the same pair for items entering a conveyor (the "electrode batches" step).
- **Item look.** Create a Material Item Type with a 3D shape and use it as the Source's agent type. Fit the shape to the placeholder outline in the type's editor.

## KPIs instrumented
n/a (visual demo). For throughput studies, check conservation: items generated = items sunk + items on the belt + items waiting in the Source.

## Pitfalls
- **Unticking Forced pushing is only half the fix.** The companion setting reportedly defaults to destroying agents that can't exit (`discardHangingEntities` = true; verify in your version). If you leave it, arrivals disappear silently whenever the entry is blocked. Always choose "wait in this block", or insert a Queue. G4 in `anylogic-gotchas.md` covers the push-error side.
- **The first point cannot be raised.** If the whole spiral must start above the floor, lift the conveyor's own Z position.
- **Pitch.** The rise per turn must exceed item height plus belt thickness. Otherwise the 3D view shows items passing through the turn above.
- **Spacing follows the item type, not the 3D picture.** Belt spacing and accumulation use the item type's modelled size, so a badly sized 3D shape makes the animation misrepresent the gaps. That is why the video fits the shape to the placeholder. *(Exact source of the item size: unverified.)*
- **Length.** If transit time matters, check the conveyor length after adding Z. *(Whether the vertical rise counts towards it: unverified.)*

## Reusable idea
Any polyline-type markup with a Points table can climb by per-point Z offsets. The video names serpentine roads, multilevel highways, curved railways and spiral stairways as other uses. Draw in plan first, then lift point by point.

## When the co-pilot should use this
- Spiral or helical conveyors, ramps between mezzanines, and overpasses or elevated track in 3D models, when no lift element is wanted.
- Any Source that feeds a block which can refuse entry, such as a conveyor or a capacity-limited block. Apply the "wait in this block" setting.
