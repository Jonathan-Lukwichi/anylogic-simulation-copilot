# Pattern card — Layout decisions: rank supplied candidates, generate markup from data
- **Source:** AnyLogic video "Webinar | How Simulation-Driven Insights Strengthen Strategic Decision-Making" (https://youtu.be/UVppYf_O4H8) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** AnyLogic evaluates layouts but does not design them, so equipment-placement questions must be framed as a comparison of supplied candidate layouts.

## Mechanism
1. **Set expectations at intake.** "Where should the equipment go?" becomes "which of these layouts performs best on our KPIs?" There is no built-in spatial or layout optimiser. The presenter's example was a pizza kitchen: several equipment layouts drawn in CAD, each run as a scenario.
2. **Produce the candidates.** Either trace each one from a CAD drawing imported at true scale (align the drawing's scale reference with AnyLogic's scale before tracing), or generate the markup from data.
3. **Compare them as scenarios.** Encode the choice as one discrete parameter (e.g. `layoutId`) and run Parameter Variation with replications. An Optimization over `layoutId` can only pick among the candidates you provide.
4. **Handle many or data-derived layouts.** For several plants with different floor plans, or long repetitive conveyor systems, script the markup at design time with the **Python Design-time API** (AnyLogic 8.9.7+). The generated elements land on the canvas and stay editable. The presenter suggested having an LLM draft these scripts from the layout data.

## Resources
n/a

## Key settings worth copying
- Imports: `from anylogic_design_time_api import *` and `from anylogic_design_time_api.generated import *`. Workspace functions connect to the running editor; GeneratedClasses create markup and set or get its properties.
- Connection: set the **Graphical editor Python API connection port** in AnyLogic preferences. The script connects to the open editor on that port.
- Documented helpers: `createStraightPointsList()` builds the points for a polyline; `toggleArcSegment()` turns a straight segment into an arc.
- Runtime alternative (any version): build the network in Java at startup, as in `basicmodels/create-transporter-network-by-code.md`. That network exists only during the run; design-time markup is saved in the model.
- One workable switch (not confirmed as the presenter's method): one agent type or markup group per candidate, chosen from `layoutId` at startup, with the movement blocks pointed at that candidate's network.

## KPIs instrumented
The decision's own KPIs compared across candidates: travel distance and time per job, throughput, congestion points, cycle time and resource utilisation.

## Pitfalls
- Promising "layout optimisation" at intake. The model only ranks what it is given.
- Tracing candidates at inconsistent scales, which makes travel-time differences meaningless.
- Running one replication per layout. Travel-driven differences are often smaller than run-to-run noise, so use replications and confidence intervals.
- Assuming the design-time API is available. It needs 8.9.7+; fall back to the runtime Java approach on older installs.

## Reusable idea
Simulation ranks layouts; people or scripts propose them. A script can propose them from data, at scale.

## When the co-pilot should use this
- Intake item B8 mentions a layout, equipment placement or facility design.
- The user expects AnyLogic to "find the best layout".
- The same logic must be laid out for many sites, or the markup is large and repetitive (conveyor systems).
