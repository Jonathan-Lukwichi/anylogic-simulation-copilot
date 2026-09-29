# Pattern card — Excel round trip: workbook in, results sheet out (desktop and Cloud)
- **Source:** AnyLogic video "Using files as inputs and outputs in AnyLogic Cloud" (https://youtu.be/LVoEVGHKHZk) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Drive a model from a user-editable Excel workbook and hand each run's results back in that same workbook, locally and as a Cloud file input/output.

## Mechanism
Demo: distributor agents built from an imported `distributors` sheet (plus a `trucks` sheet). Each run writes every distributor's total fleet size to a new `results` table, which is exported to the same workbook. The Cloud side — file inputs, one workbook as both input and output, file outputs only from single runs — is already in `videos/cloud-decision-tool-for-stakeholders.md`, `videos/cloud-run-semantics-and-access.md` and G39. This card adds the database mechanics.
1. **Keep the input live.** Database → Import → tick **Autoupdate imported tables on model startup** (Help 8.9.9), so each start re-reads the workbook into the built-in tables. The model reads those copies, so without it a replaced workbook — e.g. a Cloud input override — changes nothing *(inferred)*.
2. **Results table.** Create it in AnyLogic with typed columns (`distributor` String, `fleet_size` int).
3. **Purge, then write, both from Main's On startup** (code below). Rows written during a run stay in the built-in database, so without the purge the table grows with every run (the video's observation).
4. **Export.** Database → *Export settings*: the workbook (relative path, inside the model folder) and only the result tables; then tick **Export tables at the end of model execution**, which fires at a normal end and when the user stops the run (Help). Each exported table becomes a sheet.
5. **Cloud.** Run Configuration: drag the workbook into both Inputs and Outputs, then export. A Cloud Simulation run offers the workbook as a replaceable input and, after Run, as a downloadable output that includes the results sheet.

## Resources
n/a

## Key settings worth copying
```java
// Main → On startup. It runs LAST, after every Distributor's own On startup.
deleteFrom(results).execute();                 // clear rows left by earlier runs
for (Distributor d : distributors)
    insertInto(results)
        .columns(results.distributor, results.fleet_size)
        .values(d.companyName, d.fleetSize)
        .execute();
```
- QueryDSL is built in (Help, *Writing database queries*): `insertInto`, `update(t).where(...).set(...)`, `deleteFrom(t).where(...)`; plain SQL through `executeStatement("DELETE FROM results")`. For thousands of rows, batch them with `SQLInsertClause`.
- Programmatic export, instead of the checkbox: `getEngine().getModelDatabase().exportToExternalDB("results", new Database(this, "out", "results.xlsx").getConnection(), "results", false, false)`. The target sheet must already exist with matching header names, and rows are **appended** — the clear flag does not work on Excel (Help, *Exporting data to MS Excel*).

## KPIs instrumented
The results table itself. Add columns that identify the run (scenario label, seed, stop time) so a downloaded workbook explains itself *(suggested)*.

## Pitfalls
- **Startup order.** On startup runs on the innermost agents first and on Main last (Help 8.9.9, *Model execution order*). The video inserts rows in each Distributor's On startup and purges in Main's On startup; in that arrangement the purge runs after the inserts and deletes them, unless the agents are created later by code. Keep the purge and the writes together in Main, as above, or write later in the run.
- **Silently stale input.** If the startup update fails (renamed sheet or column, changed type), the error goes only to the console and the run continues on the old built-in data (Help, *Importing database tables*). Nobody sees that console in Cloud, so show what was read (row count, sum of a key column) as an `Output` or on-screen text.
- **Excel lock.** Exporting into a workbook that is open in Excel fails with an error (Help). Close it between runs.
- **Experiment-level code does not run in Cloud.** Cloud skips the experiment's *Initial experiment setup*, *Before each experiment run* and *Before simulation run* code (Help, *Model execution order*), so keep the purge in Main.
- **End-of-run rows.** The Help does not say whether the automatic export runs before or after On destroy *(unverified)*. Write result rows from model logic before the run ends, and check the sheet after two consecutive runs: it should hold one run's rows.
- **Multi-run experiments.** Whether parallel runs share the one built-in database is *(unverified)*; if they do, a startup purge could delete another run's rows. Cloud file outputs are single-run only anyway; on the desktop, collect multi-run results through the experiment.
- **Two paths.** The import source and the export target are set in different places; for Cloud both must be relative and inside the model folder (G39).

## Reusable idea
Treat the workbook as the model's I/O contract: input sheets re-read (and checked) at every start, result sheets cleared and rewritten on every run, and one file the stakeholder uploads and downloads.

## When the co-pilot should use this
- A stakeholder tool whose inputs are tables (rosters, demand, site lists) — the mechanics behind `videos/cloud-decision-tool-for-stakeholders.md`.
- "How do I write results to Excel?", "My output sheet has duplicate rows", "I uploaded a new file and nothing changed".
- Thesis runs that need per-agent result tables for Python or R.
