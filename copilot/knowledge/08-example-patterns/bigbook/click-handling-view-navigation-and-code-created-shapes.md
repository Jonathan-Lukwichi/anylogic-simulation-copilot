# Pattern card — Click-driven presentation: click coordinates, overlapping handlers, click catchers, view links and shapes made in code
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 13 "Designing interactive models: using controls" (section 13.3) — distilled, original wording
- **Paradigm:** Method (interaction; any paradigm)
- **Problem it solves:** Turn clicks on the animation into actions, such as selecting an object, marking a point or jumping to a screen, without the click landing on the wrong shape or at the wrong coordinates.

## Mechanism
Checked against Help 8.9.10 (shape pages *On click*, *View area*, *How-to*) and the 8.9.10 book demos. Those demos are in batch m-bigbook-1.
- **Handler.** Every presentation shape has *On click* (Advanced). The code gets three local variables (Help):
  - `self`, the shape itself;
  - `clickx` and `clicky`, the click position **relative to the shape**.

  For container coordinates, add the shape's own position: `self.getX() + clickx`, `self.getY() + clicky`. Using `self` rather than the shape's name keeps the code reusable.
- **Overlapping clickable shapes: the two sources disagree.**
  - Big Book (p. 14): shapes are visited from the top of the Z-order down. Every *On click* on the way runs. Processing stops only when a handler returns `true`; the default is `false`.
  - Help 8.9.10: only the topmost shape under the cursor gets the click.
  - The 8.9.10 demo *Click-Sensitive Icon of Active Object* still ends its handler with `return true;`.
  - Design so both readings give the same result: one responsible shape per spot, any catch-all at the back, and `return true;` at the end of each foreground handler.
- **Catch a click anywhere.** Use a large rectangle with *No color* for fill and line, plus an *On click* handler. It cannot be picked in the editor afterwards, so select it in the Projects tree (Main → presentation). Send it to the back so that real targets win.
- **Shapes made at runtime** (Big Book p. 17; Help):
  - Build the object with its class constructor (`ShapeOval`, `ShapeRectangle`…). Style it with setters; `null` as a colour means "not drawn". Place it with `setPos(x, y)`, in container coordinates.
  - Nothing appears until you hand it to a group: `presentation.add(shape)`.
  - Z-order calls such as bring-to-front work only after the shape has been added (Help).
  - A code-made shape that is in no group cannot use `randomPointInside()`, which throws; pass a generator: `randomPointInside(rng)` (Help).
- **Screen links** (Help *View area*, *How-to*):
  - a text or shape with *On click* `viewOutput.navigateTo();`;
  - `_origin_VA.navigateTo()` returns to the default frame;
  - a 3D window with *Create view area at runtime* gets `_<windowName>_VA`, e.g. `_window3d_VA.navigateTo()`;
  - put `navigateTo()` in Main's *On startup* to open on that view;
  - web links: `getExperimentHost().openWebSite("https://…")`.

## Resources
n/a

## Key settings worth copying
- **Click-to-place marker:** `oval.setPos(self.getX() + clickx, self.getY() + clicky);` in the catch-all's *On click*.
- **Two-screen report:** view areas `viewAnimation` at (0, 0) and `viewOutput` at (0, 600). Draw a menu of two texts on each and cross-link them with `navigateTo()`, so the charts do not clutter the animation (Big Book pp. 15–16).
- **Replicated targets:** `index` is in scope in *On click* (see `bigbook/replicated-shapes-and-group-pivots.md`).

## KPIs instrumented
n/a

## Pitfalls
- **The KB's `basicmodels/getting-mouse-coordinates.md` names `getX()`/`getY()` as the click API.** The 8.9.10 model actually uses `clickx`/`clicky` in a rectangle's *On click* (a correction is proposed in batch book-3).
- **Shapes added in code accumulate.** Remove them with `presentation.remove(s)`, or cap their number. Hundreds of runtime dots slow every frame *(inferred)*.
- **User clicks make a run irreproducible** (G17). Keep click handlers for inspection and navigation. If a click changes the logic, log it with its time so the run can be explained.

## Reusable idea
Treat the animation as a UI:
- one responsible shape per clickable spot;
- `clickx`/`clicky` plus `self` for coordinates;
- view areas as screens;
- a transparent catch-all at the back.

## When the co-pilot should use this
- **Uses:** "click a machine to see its stats", point-and-click placement, menus between the animation, dashboard and 3D screens.
- **Symptoms:** a click is handled by the wrong shape or twice; markers appear offset; a runtime shape does not show.
- **Related:** `bigbook/controls-link-direction-sync-and-replicated-controls.md`, `bigbook/animation-dynamic-properties-and-frame-cost.md`.
