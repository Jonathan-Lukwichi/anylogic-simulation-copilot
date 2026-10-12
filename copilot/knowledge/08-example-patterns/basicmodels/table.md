# Pattern card — Table
- **Source:** AnyLogic example model "Table" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (presentation / reusable component)
- **Problem it solves:** Show live textual or numeric results as a formatted table on the model canvas with one drop-in component, instead of drawing and updating dozens of text shapes.

## Structure
- Agent type `Table` (copy it into your model by Ctrl+dragging it to your project tree). Main embeds one instance with
  20 rows, 7 columns, `columnWidths = {100, 50, 70}`, headers `{"RRR", "Value"}` and cell content `row + ":" + column`.
- Inside `Table`: one replicated text shape for all cells (`rows × columns` copies) whose text is
  `data(index / columns, index % columns)` and whose X comes from an offsets array; one replicated text for the header;
  replicated rectangles for alternate row shading; replicated lines for the grid. On startup the column offsets are
  computed from either one width or a width array.

## Resources
n/a

## Key settings worth copying
- **Dynamic parameter with arguments:** `data` is a *Dynamic* String parameter with *Parameter arguments* `row` and
  `column` (Help 8.9.10, *Parameters*: arguments are available for Dynamic and Action parameters). The user's expression
  is re-evaluated every time a cell is drawn, so the table shows live values — e.g. `stations.get(row).queueSize()` or a
  `switch` on `column`.
- **Replicated shapes indexed into a grid:** row = `index / columns`, column = `index % columns` (replication basics:
  `../bigbook/replicated-shapes-and-group-pivots.md`).
- **A proper property page:** each parameter has an editor label, a control type (check box, text box) and hide
  conditions, e.g. the even-row colour appears only when *different odd and even rows* is ticked.
- Missing values degrade gracefully: fewer widths than columns reuse the last width; fewer headers than columns leave
  blanks.

## KPIs instrumented
n/a (display component).

## Pitfalls
- The expression runs on every redraw for every cell; keep it cheap (read stored values, avoid scanning populations or
  querying the database in it).
- The number of rows and columns is fixed when the shapes are created — size them for the largest content *(inferred
  from replication being evaluated at creation)*.
- A dynamic parameter is read with call syntax inside the type (`data(r, c)`), not as a field (Help, *Dynamic parameters*).

## Reusable idea
Build display widgets as agent types whose content is a dynamic parameter with arguments — effectively a callback the
host fills in. The same trick gives reusable KPI boards, legends and Gantt rows without copying drawing code.

## When the co-pilot should use this
KPI tables on dashboards, per-station or per-resource summaries, and any request for a reusable presentation component.
Related: `../videos/custom-flowchart-block-from-repeated-chain.md` (dynamic parameters in custom blocks, G35),
`gantt-chart.md`.
