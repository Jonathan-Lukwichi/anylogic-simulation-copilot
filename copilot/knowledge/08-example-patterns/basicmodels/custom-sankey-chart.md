# Pattern card — Custom Sankey Chart
- **Source:** AnyLogic example model "Custom Sankey Chart" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (presentation; any flowchart model)
- **Problem it solves:** Show a chart type AnyLogic does not offer — here a Sankey (flow) diagram of how many agents took each route — by drawing it with an external Java charting library and displaying the result as SVG on the model canvas.

## Block chain
Two streams — `Source` *boxes* (20/min) and `Source` *mails* (50/min) — each go through a `SelectOutput` (60/40 and 30/70) into zero-time `Delay` blocks *process1–3* and on to `Sink`s. Each SelectOutput's *On exit (true/false)* adds 1 to the matching flow and redraws the diagram.

## Resources
n/a

## Key settings worth copying
- **Libraries:** `jfreechart-1.5.3.jar` and `jfreesvg-3.4.3.jar` sit in the model folder and are added to the model's dependencies (class path); Main's *Imports* bring in `JFreeChart`, `FlowPlot`, `DefaultFlowDataset`, `NodeKey`, `SVGGraphics2D`, `Rectangle2D`.
- **Objects as Main variables:** a `DefaultFlowDataset`, a `FlowPlot` on it, a `JFreeChart` on the plot, an `SVGGraphics2D` canvas (width × height) and an AnyLogic **`ShapeSVG`** placed in a presentation group.
- **Set-up (On startup):** register every source→target flow at stage 0 with value 0; colour nodes through `NodeKey(stage, name)` keys (sources at stage 0, targets at stage 1).
- **Counting:** `setFlow(0, source, target, 1 + getFlow(0, source, target).intValue())` in the routing block's exit action.
- **Redraw:** `chart.draw(svgCanvas, new Rectangle2D.Double(0, 0, w, h))`, then `shapeSvg.setSVG(svgCanvas.getSVGElement())` and `group.onDraw()`.
- `ShapeSVG` (engine Javadoc 8.9.10): a shape rendered from SVG XML given as a String; `setSVG`, `getSVG`, `removeSVG`; constructors with or without position.

## KPIs instrumented
The route-count matrix held in the flow dataset (source × target) — itself a useful routing KPI.

## Pitfalls
- **Redraw cost.** The demo re-renders the whole chart for every agent (70 per minute here). In long or fast runs, redraw from a cyclic event instead, or only while the animation is visible.
- **Growing canvas.** The demo reuses one `SVGGraphics2D` for every redraw; JFreeSVG records drawing operations, so the SVG text may keep growing — create a fresh canvas per redraw if memory or speed degrades *(unverified)*.
- Ship the jars with the model: keep them in the model folder and listed as dependencies, or the model will not compile elsewhere (and check the export when sharing).
- Flow keys are plain strings — a typo creates a new node silently.

## Reusable idea
Any Java library that can paint on a `Graphics2D` (JFreeChart's other plots, custom diagrams, heat maps) can be shown in AnyLogic through an SVG canvas and a `ShapeSVG`; the same SVG string can also be written to a file for reports.

## When the co-pilot should use this
When a user needs Sankey/flow diagrams of patient, product or order routing, or any chart the Analysis palette lacks. For native charts see `linked-charts.md` and `gantt-chart.md`.
