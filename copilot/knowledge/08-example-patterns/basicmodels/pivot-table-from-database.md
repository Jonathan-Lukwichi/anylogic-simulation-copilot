# Pattern card — Pivot Table from Database
- **Source:** AnyLogic example model "Pivot Table from Database" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (data and presentation; no process logic)
- **Problem it solves:** Aggregate raw transaction rows (store, device, quantity, revenue) into a cross-tab with row and column totals inside the built-in database, and show it on the model canvas.

## Structure
- Built-in database table `sales` (date, store, device, quantity, revenue).
- Three **database views** (SQL, stored in the model's database): `device_sales` — one row per device with one revenue column per store built by conditional aggregation (`SUM(CASE WHEN store = '…' THEN revenue ELSE 0 END)`) plus a row total; `store_totals` — a single `'TOTAL'` row with the same columns; `pivot_table` — the union of both.
- `Main` *On startup*: `queryTableData()` reads `SELECT * FROM pivot_table` with `selectResultSet(...)` in try-with-resources, takes column names and types from `ResultSetMetaData` (`getColumnCount`, `getColumnName`, `getColumnType`), converts every cell to text (doubles via `getDouble`) into `String[][] content` + `String[] headers`, then `add_table()` creates a `Table` agent (reused from the "Table" example) whose parameters take the grid, headers, column widths and styling; the Table draws cells as replicated text shapes (`data(index / columns, index % columns)`).

## Resources
n/a

## Key settings worth copying
- **Views (Help 8.9.10):** a view is a query result computed on each access, so it always reflects the current table data; views can be nested; they store only the definition. Create them in the database with an SQL *View definition*; AnyLogic's logs are views too (copy a log view to edit it).
- Pivot in SQL, not Java: one conditional `SUM(CASE …)` column per category, a separate totals view, and a union for the final grid.
- Generic reader: `selectResultSet(sql)` + `ResultSetMetaData` handles any view without hard-coding columns (the hidden `al_id` column exists only in base tables, not in these views).

## KPIs instrumented
Revenue per device × store, device totals, store totals, grand total.

## Pitfalls
- **Rows of a view are unordered** (Help: `ORDER BY` inside a view definition is meaningless). The demo reads the union view without sorting, so the TOTAL row is last only by chance — add `ORDER BY` (e.g. a sort key that puts TOTAL last) in the reading query.
- Category columns are hard-coded in the view (`'Fukuoka'`, `'Kyoto'` …); a new store in the data silently falls out of the pivot until the view is edited.
- Close the result set (try-with-resources) — Help asks for it for every ResultSet.

## Reusable idea
Keep aggregation in database views (live, nested, no copies) and keep Java only for reading and display; the same views can feed canvas tables, charts or Excel export of results tables.

## When the co-pilot should use this
Summary tables of inputs or results (per-scenario KPIs by resource and shift, costs by product and site), dashboards inside the model, or when a user wants SQL-side aggregation of logs. For writing results to tables see `videos/excel-round-trip-results-and-cloud.md`; for the reusable Table object see `table` (batch m-basic-4).
