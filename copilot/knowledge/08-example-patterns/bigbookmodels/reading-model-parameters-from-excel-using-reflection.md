# Pattern card — Reading Model Parameters from Excel Using Reflection
- **Source:** AnyLogic example model "Reading Model Parameters from Excel Using Reflection" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Drive a model from a hand-kept workbook whose layout you do not control (parameters in any row, mixed cell types, formulas), and hand results back into a formatted workbook, without importing sheets into the built-in database.

## Block chain
A call centre: Source (`CallsPerMinute`) → Service (pool `operators` of size `NumberOfOperators`, delay `triangular(ServiceTimeMin, ServiceTimeMode, ServiceTimeMax)`, timeout `uniform(AbandonTimeMin, AbandonTimeMax)`) → Sink "answered"; the timeout exit leads to Sink "abandoned". All seven values are parameters of Main, filled from `parameters.xlsx`.
Companion example models: `Reading Data of Various Types from Cells in Excel` and `Displaying the Model Output as a Chart in Excel`.
- **Reflection loader** (Main, On startup; the Excel File element has *Load on model startup* on):
  1. Walk row 1 of sheet "Call center" to find the columns headed "Name" and "Value".
  2. From row 2, while `cellExists(sheet, row, nameCol)`, read the name and let `getClass().getField(name).getType()` choose the reader: numeric (cast for `int`), string or boolean.
  3. Apply the value with `getMethod("set_" + name, type).invoke(this, value)`.
  4. Any exception becomes `error(...)`, naming the parameter.
- **Typed reads** (companion 1). Every getter has three address forms: `"Sheet1!B2"`, `(sheetName, row, col)` and `(sheetIndex, row, col)`, all one-based.
  - A numeric cell goes into a variable or a parameter (use `set_…`), a boolean into a check box, a string into a text shape.
  - A date cell arms an event: `event.restartTo(date)`.
  - `readTableFunction(tf, "Sheet1!B10", 10)`: arguments in that column, values in the next.
  - `readHyperArray(ha, "Sheet1!F3", false)`: `false` puts the first dimension across columns.
  - A button calls `setCellValue(250, "Sheet1!B23")`, then `evaluateFormulas()`, then re-reads a formula cell. This what-if stays in memory: *Save on model termination* is off.
- **Writing** (companion 2):
  - An SIR model samples `Infectious` every 2 days into a dataset. Main's On destroy calls `writeDataSet(dataset, 1, 1, 1)`, and *Save on model termination* saves the workbook.
  - The workbook already contains a formatted chart over that empty range, so opening it after a run shows the curve.

## Resources
ResourcePool `operators` (static), sized by `NumberOfOperators`.

## Key settings worth copying
All from Help 8.9.10 *Excel file* unless marked.
- **Empty cells raise no error:** numeric → 0, string → "", boolean → false, date → null. Type mismatches (a text cell read as a number, a number read as a string) throw.
- `setCellValue` and `setCellFormula` do not recalculate; call `evaluateFormulas()`.
- `readTableFunction` returns the number of points it actually read.
- `writeDataSet` writes (X, Y) rows into two columns. `writeFile()` saves on demand; call `setFileName()` first to save elsewhere. `readFile()` reloads and drops unsaved edits.
- **8.9.1 change:** `getCellType()` and `getCellFormulaType()` return a `CellType` enum after the Apache POI update. Old code comparing them with ints no longer compiles; use `var`, or import `org.apache.poi.ss.usermodel.CellType`.
- **Why `set_…`:** it runs On change, and blocks bound *directly* to the parameter follow it — here the pool's capacity is simply `NumberOfOperators` (Help *Parameter propagation*). Per-agent expressions, such as the triangular delay, read the new values anyway.

## KPIs instrumented
Answered and abandoned calls (the two sinks). The companion's Infectious curve lands in Excel.

## Pitfalls
- **Silent zero.** A blank or misplaced value arrives as 0 or "", which looks plausible. Check `cellExists` and the cell type before reading, fail on unknown names (`getField` throws), and echo what was loaded on screen or in the log.
- **Reflection sees only public fields of Main.** It cannot reach anything fixed while the model is built, such as population sizes or block fields bound through an expression rather than directly. Such inputs must be set before Main exists, or taken from the built-in database *(judgement; propagation through expressions not verified)*.
- **Tail of the dataset.** A dataset keeps only its latest *Keep up to … samples* (50 in this model). Sampling every 2 days for 100 days gives 50 or 51 points, so the day-0 point can drop out of the export. Size the tail as run length ÷ recurrence + 1.
- **Cloud and multi-run.** Keep the workbook in the model folder with a relative path (G39). With *Save on model termination*, every run of a multi-run experiment writes the same file, so the last one wins *(inferred)*.

## Reusable idea
Treat an input workbook as a key–value contract: find columns by header, keys by parameter name, and fail loudly on anything unknown or empty. For outputs, format the chart in Excel beforehand and let the model fill only the data range.

## When the co-pilot should use this
- Clients who keep parameters in their own spreadsheet layout, with notes and formulas, and edit it without opening the model.
- Time series into formatted Excel reports with no post-processing.
- Old models or course code that compares `getCellType` with integers (8.9.1 change).
- Choosing the route: row-shaped tables → built-in database import with autoupdate (`videos/excel-round-trip-results-and-cloud.md`); scattered cells, formulas, templates → the Excel File element (this card).
