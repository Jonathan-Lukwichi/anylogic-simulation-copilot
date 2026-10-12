# Pattern card — Write Experiment Parameters to New File
- **Source:** AnyLogic example model "Write Experiment Parameters to New File" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (experiment output)
- **Problem it solves:** Save each run's inputs (and, by extension, outputs) to a new, time-stamped CSV or Excel file — one file per single run, or one file with a row per run for a Parameter Variation — without touching the model's database.

## Structure
- Main has two parameters (`parameter1`, `parameter2`, random defaults) and a radio button choosing CSV or Excel.
- **Single run:** the Simulation experiment's *After simulation run* calls `root.createFile()`, a Main function that
  builds a file name from the wall-clock date and time plus the experiment type
  (`getExperiment().getClass().getSimpleName()` minus "Experiment"), then writes a header and one data row.
- **Multi-run:** the Parameter Variation experiment owns its own Text File and Excel File elements, a flag
  `fileCreated` and a `fileName`. Its *After simulation run* calls the experiment function `createFileMultiRun()`: on the
  first run it creates the file and writes the header; on every run it appends `getCurrentIteration()` and the
  parameter values.

## Resources
n/a

## Key settings worth copying
- **CSV** (Text File element, Help 8.9.10): `setFile(name, TextFile.WRITE)` to create or overwrite,
  `setFile(name, TextFile.WRITE_APPEND)` to add rows, `println(...)`, then `close()`.
- **Excel** (Excel File element): `setFileName(name)`; to append, `readFile()` first; `setCellValue(value, sheet, row,
  column)` with **one-based** indices; `writeFile()` to save (or tick *Save on model termination*).
- Row per iteration: Excel row = `getCurrentIteration() + 1` (row 1 holds the header), so rows land in the right place
  whatever order runs finish in.
- Why the multi-run writer lives on the experiment: Main is rebuilt for every run, so a flag or open file kept on Main
  would reset each time; the experiment object survives across iterations.

## KPIs instrumented
The files themselves. Add the run's outputs (from `root`) next to the inputs so every row is a complete record.

## Pitfalls
- **Parallel runs:** this experiment has *Allow parallel evaluations* on, and the function reads the varied values from
  the experiment's fields. The Help recommends `root` for per-run values in experiments with runs executed in parallel;
  read `root.parameter1` etc. *(whether the experiment fields always match the run just finished under parallel
  evaluation is unverified; safe choice: use `root`)*.
- *After simulation run* is **not executed when the run is terminated from the toolbar** (Help) — stop with a stop time
  or `finishSimulation()`, or no file is written.
- The name stamp is minute-resolution (`ddMMyy_HHmm`): two experiments started in the same minute write to the same file.
  Add seconds or a counter.
- Experiment code does not run in AnyLogic Cloud (G49), and Cloud file outputs come only from single runs (G39) — keep
  this recipe for desktop studies.
- Keep static variables out of models run in parallel (Help, *Parameter variation*).

## Reusable idea
Write multi-run results from the experiment, not from the model: open or create the file once (flag on the experiment),
append one self-describing row per run keyed by the iteration number, and take the run's values from `root`. Pair it with
database export (`../videos/excel-round-trip-results-and-cloud.md`) for single-run detail tables.

## When the co-pilot should use this
Thesis or study runs that need a flat file of inputs and KPIs per scenario for Python/R/Excel, parameter sweeps outside
the built-in charts, and "how do I save every run's results?" questions. Related:
`../videos/excel-round-trip-results-and-cloud.md`, `../videos/time-in-section-measurement-and-execution-log.md`
(logs only for Simulation experiments, G19).
