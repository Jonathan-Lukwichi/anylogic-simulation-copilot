# Pattern card — CAD floor plan to pedestrian walls (layer triage)
- **Source:** AnyLogic video "How to convert CAD drawings to walls" (https://youtu.be/tjbS9FcuT2A) — distilled, original wording
- **Paradigm:** Method (space-markup workflow for Pedestrian Library models)
- **Problem it solves:** Turn an architect's DWG/DXF plan into AnyLogic wall markup in minutes instead of tracing it, keeping only the lines that are real obstacles.

## Mechanism
1. **Load the drawing.** Place a **CAD Drawing** (Presentation palette) on `Main` and load the .dwg or .dxf file.
2. **Set Fill color = No fill.** The default fill hides the linework.
3. **Position, size and calibrate.** Position and size the drawing, then calibrate its scale (see Pitfalls) *before* converting.
4. **Convert.** Right-click the drawing and choose **Convert to Markup**.
   - The wizard lists every layer. Select All and Clear All help here.
   - Tick only the layers that hold walls. The target type is walls.
   - *Beyond the video:* conversion to walls arrived in AnyLogic 8.7. Walls were the only target in the video's version.
5. **Check.** Compare the generated walls with the plan. Re-run the conversion for any layer you missed.
6. **Clean up.** Delete the CAD element. Also delete walls that came from parts of the file you are not modelling, since a DWG often holds several plans or views.
7. **Carry on.** Add the rest of the pedestrian markup (target lines, areas, services) and the Ped flowchart.

## Key settings worth copying (layer triage)
| Convert | Leave out | Reason |
|---|---|---|
| The wall / walls layer | Axes, grid, defpoints | Construction aids, not obstacles |
| Partition layers, e.g. gypsum/drywall ("gips") | Text, dimensions, title/info, decoration | Symbolic only |
| | Stairs ("communication" in the video's file) | Treads turn into a tangle of near-parallel walls. Model stairs with pedestrian markup instead; the video plans a rectangular node. |
| | Sanitary fixtures | Clutter that doesn't affect flow |
| | Doors | Pedestrian models leave doorways open. Converted door leaves or swings would seal them. |

Switch layers on one at a time to see what each holds before you decide, because layer names vary by author and language.

## Resources
n/a

## KPIs instrumented
n/a (a geometry-preparation step).

## Pitfalls
- **Scale.** Stretching the drawing "to fit the frame" gives it an arbitrary metres-per-pixel, and the converted walls inherit the error.
  - Before converting, measure a known dimension against the diagram's Scale: a door (about 0.9 m) or a room with a dimension on the plan. Adjust until they match.
  - Walking speeds, densities and level of service all depend on this.
  - The general "import at true scale" rule is already in `videos/layout-candidates-and-design-time-api.md`.
- **Doorways.** Check every doorway after conversion. A wall line drawn straight across an opening, or a converted door symbol, blocks the route and leaves pedestrians stranded.
- **Whole-file conversion.** The conversion covers the whole file, so expect walls from secondary views and delete them.
- **Only walls are produced.** Stairs, escalators, levels, queues and services are still drawn by hand. For multi-floor models see `models/evacuation.md`.

## Reusable idea
A CAD import is a filtering job, not a drawing job. Decide which layers are physical obstacles, convert only those, and add the pedestrian-specific constructs yourself.

## When the co-pilot should use this
- Phase 0 question B8 turns up a CAD, DWG or DXF plan for a pedestrian model, such as a station, terminal, museum, hospital or evacuation study.
  - Ask for the file and for which layers hold walls and partitions.
  - Calibrate the scale, then convert.
- A user is tracing walls by hand over a background image.
- For GIS sources (shapefiles) of rail, roads, paths or walls, see `gis-shapefile-to-rail-markup.md`.
