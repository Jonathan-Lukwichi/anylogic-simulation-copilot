# Pattern card — Using Prepared Statement when Writing to Databases
- **Source:** AnyLogic example model "Using Prepared Statement when Writing to Databases" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Write one row per entity, plus run metrics, to an external database during a run, without per-statement SQL parsing slowing the model and without leaving half-written tables when a run fails.

## Block chain
Source (1 per minute) → Service (pool `server`, capacity 2, `triangular(0.5, 1, 1.5)` minutes) → Sink. The run lasts 1,000 minutes in virtual time.
Companion example model: `Dumping Simulation Output into a Database Table` — the same model logging with plain SQL strings.
- **Database element** `OutputDB`: an Access file in the model folder, *Connect on startup*. Two tables:
  - `Log`: transaction id, time entered, time exited;
  - `MainMetrics`: name, value.
- **Main, On startup:**
  1. `OutputDB.modify("DELETE FROM Log")`;
  2. `con = OutputDB.getConnection()`, then `con.setAutoCommit(false)`;
  3. prepare two statements, held in variables of type `java.sql.PreparedStatement`: an INSERT with placeholders for id and entry time (exit time 0), and an UPDATE that sets the exit time for an id.
- **Source, On exit:** bind the INSERT (`setInt(1, id)`, `setDouble(2, time())`), then `executeUpdate()`.
- **Sink, On enter:** bind the UPDATE (`setDouble(1, time())`, `setInt(2, id)`), then `executeUpdate()`.
- **Main, On destroy:** two `modify()` updates store `sink.count()` and `server.utilization()` in MainMetrics; then `commit()` and auto-commit back on.
- Every JDBC call sits in try/catch, and the catch calls `error(...)`.
- The companion builds each statement by string concatenation inside `modify(...)`. The database parses every call afresh, and the run slows noticeably once logging is on.

## Resources
ResourcePool `server` (capacity 2).

## Key settings worth copying
- **Database element API** (Help *Database API*): `modify(sql)` returns whether it succeeded; `getConnection()` hands out the JDBC `Connection`. For reading, see `basicmodels/feeding-a-collection-from-access-database.md`. Since 8.9.1 the element also connects to Oracle, PostgreSQL, MySQL and MariaDB (release notes).
- **Prepared statements.** Prepare once, in On startup. Bind values with the 1-based setters (`setInt`, `setDouble`, `setString`) and run `executeUpdate()` per row. Bound values also avoid the quoting and decimal-separator problems of pasted SQL *(standard JDBC)*.
- **One transaction per run.** Call `setAutoCommit(false)` at the start and `commit()` at the end; `rollback()` leaves the database as it was before a failed run. Help asks you to commit or roll back explicitly before `disconnect()`.
- **Fewer round trips** with `addBatch()` / `executeBatch()` every N rows *(standard JDBC; not used in the model)*.
- **When On destroy runs.** Main's On destroy runs once the run completes, either at the stop time or after a manual Stop, following the experiment's *After simulation run* (Help *Model execution order*). Final metrics and the commit therefore also land when the user stops early.

## KPIs instrumented
- Per transaction: entry and exit time, from which SQL can compute time in system.
- Per run: transactions processed and server utilisation.

## Pitfalls
- **`hashCode()` as a key.** Both models key rows by `agent.hashCode()`, which is not guaranteed unique (the book says so too). Give each agent a serial id at the Source (`agent.id = ++lastId`) and index that column.
- **Old rows.** The startup DELETE is what limits the table to one run, as in G47. For multi-run experiments, tag rows with a run id rather than deleting them; parallel runs would otherwise erase each other's rows *(judgement)*.
- **Entities still inside at the end** keep exit time 0. Treat them as censored; do not average them in as zero.
- **Uncommitted work is lost.** Runs that end abnormally lose everything since the last commit. That is right for failed runs, but in very long runs commit every N rows or every simulated day *(judgement)*.
- **Pick the store first.** For results that stay with the model, the built-in database is simpler and Cloud-friendly (QueryDSL `insertInto`, batch `SQLInsertClause`, *Export tables at the end of model execution*; see `videos/excel-round-trip-results-and-cloud.md`). An external database suits shared servers, very large logs and live dashboards.

## Reusable idea
Log entities as rows keyed by your own id: insert at entry, update at exit. Prepare statements once, commit once per run, and write the run summary in On destroy.

## When the co-pilot should use this
- A user needs per-entity traces (patients, orders, jobs) in SQL Server, MySQL, PostgreSQL or Access for BI tools, or the model slowed down once database logging was added.
- Any "write my results to a database" request: settle built-in vs external first.
- Related: G46–G47 (startup order; purge, then write), `videos/time-in-section-measurement-and-execution-log.md` (the execution-log route).
