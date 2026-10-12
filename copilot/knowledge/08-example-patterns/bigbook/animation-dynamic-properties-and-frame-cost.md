# Pattern card — Animation driven by model state: dynamic properties, per-frame cost, and progress from getRest()
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 12 "Presentation and animation: working with shapes, groups, colors" — distilled, original wording
- **Paradigm:** Method (presentation; any paradigm)
- **Problem it solves:** Show states and progress smoothly without adding model events, and stop heavy animation from slowing runs or changing results.

## Mechanism
- **Dynamic fields are recomputed for every animation frame** (Big Book p. 22), and the model runs in the gaps between frames. The first frame draws all shapes in Z-order; after that, only shapes whose dynamic values changed are redrawn (p. 32).
- **Visible is evaluated first.** If it is false, no other field of that shape is evaluated (p. 23). Use Visible to guard expressions that would throw, such as a null agent or an empty collection.
- **Progress with no extra events.** Drive the drawing from the time remaining in the activity already scheduled:
  - *Elevator doors* (pp. 27–28): door width = `inState(Opening) ? 50 * OpeningCompleted.getRest() / 0.5 : …`, where 0.5 is the opening time in model units. The second door simply copies the first (`leftDoor.getWidth()`).
  - *Missile* (pp. 30–31): X follows `hitTarget.getRest()`; the picture switches through the Image element's *Image index* `hitTarget.isActive() ? 0 : 1`; after the hit, the group's scale grows with `time()`.
  - Each model holds one timed element; everything else is presentation.
- **Free in experiments.** Presentation is not evaluated when animation is off, as in optimization or parameter variation. Effects built from dynamic fields therefore cost nothing there, whereas extra "animation step" events would still run (p. 31).
- **Event-driven alternative.** When a dynamic expression would have to test many states, set the property once from each state's entry action instead: `curve.setFillColor(royalBlue);` (p. 40).
- **Canvas for dense grids.** `ShapeCanvas` is a raster:
  - draw with `fillRectangle(x, y, w, h, color)` and `fillCircle(...)`; erase with `clear()` and `clearRectangle(...)` (Help *Canvas*);
  - redraw in a group's *On draw* field, which runs whenever the group is about to be redrawn, and repaint only the cells whose colour changed, keeping the last colour per cell (p. 8);
  - a painted cell is not a shape: no clicks and no per-cell API. Help recommends canvas only when normal shapes animate too slowly (heatmaps of thousands of cells).

## Resources
n/a

## Key settings worth copying
- **Special values:** a `null` colour means that fill or line is not drawn. Rotation fields are in radians (`PI` = 180°). Line styles are `LINE_STYLE_SOLID`, `_DASHED` and `_DOTTED`.
- **Colour objects:** `new Color(r, g, b, alpha)` inside a dynamic field creates a new object every frame, so declare frequently used colours once as constants (p. 46).
- **Transparency:** alpha runs from 255 (opaque) to 0; vary it to show intensity. `semiTransparent(c)` gives alpha 128.
- **Palettes** (already used in the KB: `models/billiard-balls.md`, `models/gridded-system-dynamics-population.md`):
  - `spectrumColor(i, n)`: n distinct hues;
  - `lerpColor(f, c0, c1)`: a ramp; f is clamped to 0…1, so scale it first (e.g. density / 500).
- **Text fields** take numbers and concatenation: `(d > 0 ? "+" : "") + d`.
- **Scaling a picture with a value:** put its shapes in a group and set the group's *Scale X/Y* (e.g. `Money / 1000`). The group origin is the fixed point.

## KPIs instrumented
n/a. A bar or door driven by `getRest()` is itself a cheap live indicator of any timed activity.

## Pitfalls
- **`getRest()` returns infinity when nothing is scheduled.** Guard with `isActive()` or with Visible.
- **Hidden side effects.** If a run with animation on gives different outputs from the same run (same seed) with animation off, some presentation code changes model state. Keep dynamic fields and *On draw* read-only *(verification practice)*.
- **Many heavy dynamic fields slow the animation, not the logic.** Measure speed with animation off before blaming the model.
- **Integer positions at design time.** Design-time coordinates are whole pixels; runtime coordinates are doubles, so sub-pixel placement needs dynamic fields or the API (p. 11).

## Reusable idea
Animate from state that already exists (states, `getRest()`, stocks, counters) instead of scheduling events for the picture, and keep the presentation layer read-only.

## When the co-pilot should use this
- Building demos, digital-twin views or stakeholder screens; smooth door, crane or vehicle progress; heatmaps.
- Symptoms: animation slows the model, or results differ with animation on and off.
- Related: `videos/flowchart-block-animation-binding.md`, `videos/per-agent-3d-material-color.md`, `bigbook/replicated-shapes-and-group-pivots.md`, and gotchas G33, G34, G54.
