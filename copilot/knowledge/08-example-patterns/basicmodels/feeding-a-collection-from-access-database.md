# Pattern card — Feeding a Collection from Access Database
- **Source:** AnyLogic example model "Feeding a Collection from Access Database" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (data input)
- **Problem it solves:** Read the rows of an external database (an MS Access `.accdb` file here) at start-up and turn each row into a Java object in a collection, or into an agent of a population, without importing the table into the built-in AnyLogic database.

## Structure
No flowchart. `Main` holds a **Database** connectivity element (type Access/Excel, *Connect on startup* ticked, the `.accdb` kept next to the `.alp` as a model resource), a collection `collection` (`ArrayList`, *Elements class* = a custom Java class `Country` with public fields `name`, `capital`, `population`), and two functions:
- `executeQuery()` returns the result of `database.getResultSet("SELECT * FROM [Table]")`;
- `executeQueryAndMap()` opens that result set in a try-with-resources block, walks it row by row with `next()`, reads each column **by its label** (`getString`, `getInt`), fills a new `Country` object and adds it to the collection.
`Main` *On startup* calls `executeQueryAndMap()`.

Companion model **Feeding a Replicated Object from Access Database** (same folder family, same two functions) maps each row into an agent instead: the population `persons` (agent type `Person` with parameters `name`, `birthYear`) is set to *initially empty*, and the loop calls the generated `add_persons(name, birthYear)` — the add-function overload that takes the agent's parameter values in declaration order.

## Resources
n/a

## Key settings worth copying
- Database element API (Help, *Database API*): `getResultSet(sql)`, `getValue(sql)` (one aggregate value), `getRow(sql)` (one row as a map of strings), `getMatrix(sql, type)` (2-D array), `modify(sql)` (INSERT/UPDATE/DELETE), `connect()` / `disconnect()`, `getConnection()` for raw JDBC.
- Close every result set (try-with-resources does it); Help asks for `ResultSet.close()` after use.
- Access SQL quotes identifiers with square brackets: needed for reserved words (the demo's table is literally named `Table`) and for labels with spaces (`Year of birth`).
- Column labels in `ResultSet` getters are not case-sensitive; you must call the getter that matches the column's type.
- Population to be fed by code: *Population is initially empty*, then `add_<population>(p1, p2, …)` per row.

## KPIs instrumented
n/a — a data-loading demo; the loaded objects are shown in a list on the canvas.

## Pitfalls
- The model's own description (and canvas text) still talks about a "Query" connectivity object with a *Mapping* page. The Query element (with Insert, Update and Key-Value table) was deprecated and removed from the palette in 8.9.5; old models that use it still open (fixed in 8.9.8), and one 8.9.10 example still contains a Query. The 8.9.10 version of this model does the mapping in code; do not build new logic on the old element (gotcha G117). Do not send users looking for it.
- Help warns that an Access/Excel link stores a file path: if the database file moves, the connection breaks. Keep the file inside the model folder.
- For a population, `ONE_AGENT_PER_DATABASE_RECORD` works only with tables of the **built-in** AnyLogic database; an external Database element needs the code loop (or import the table first).

## Reusable idea
Three ways to get table data into agents, in order of preference: (1) import the table into the built-in database and use *Load from database* / `ONE_AGENT_PER_DATABASE_RECORD` (no code, portable); (2) keep a live external connection and map rows with `getResultSet` + `add_<population>(…)` when the data must be read fresh from a file or server at each run; (3) map rows into plain Java objects in a collection when the records are reference data, not agents (no per-agent overhead).

## When the co-pilot should use this
When a user must read an Access/SQL Server/MySQL table at run time, needs lookup records held as plain Java objects, or asks why their "Query object / Mapping page" instructions do not match the 8.9 UI. For static inputs, steer them to import into the built-in database instead (`getting-values-from-anylogic-database.md`).
