# Pattern card — Linked Charts
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Demonstrates how to synchronise selection state across multiple chart types and a list box so that clicking any one control highlights the same data items in all others.

## Block chain
A simple System Dynamics population model (Stock → Births flow in, Deaths flow out) serves as the data backbone. The SD layer drives three dashboard controls — a pie chart, a time-plot, and a bar chart — plus a list box. Each chart's **On selection change** callback calls `setSelectedItemIndices()` on the other two charts and the list box, propagating the user's click to every widget simultaneously. The list box fires the same cross-update in its action code.

## Resources
n/a — no resource pools; the only "resource" is the population Stock initialised at 1 000 000.

## Key settings worth copying
- **FractionalBirthRate** and **AverageLifetime** are exposed as editable Parameters, making the SD sub-model easy to experiment with at run-time.
- Time unit: **Year**.
- Cross-chart wiring lives entirely in the **Advanced → On selection change** code field of each chart — no external event or agent is needed.
- Pattern for list-box → charts: `chart.setSelectedItemIndices(listbox.getValuesIndices())`.
- Pattern for chart → others: capture `selectedIndices` from the event, then call `setSelectedItemIndices(selectedIndices)` on every peer control.

## KPIs instrumented
Population level over time (time-plot); share per category (pie chart); category magnitudes (bar chart). No explicit wait/utilisation KPIs — the model is a UI-interaction showcase rather than a performance study.

## Reusable idea
The transferable trick is the **symmetric cross-update pattern**: every selectable widget holds references to its peers and calls a single setter on each peer inside its own selection-change handler. This one-liner per widget is all that is needed to create fully synchronised, multi-view dashboards without any custom event bus or shared selection model.
