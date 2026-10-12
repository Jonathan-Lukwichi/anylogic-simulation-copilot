# Pattern card — Python from Experiment Screen
- **Source:** AnyLogic example model "Python from Experiment Screen" (basicmodels), AnyLogic 8.9.10, with its `io_manager.py` — distilled, original wording
- **Paradigm:** DES + Pypeline at the experiment level
- **Problem it solves:** Let Python design and post-process a multi-run experiment — Python supplies each iteration's parameter values, collects every run's result and draws the summary plot — while the model itself stays pure AnyLogic.

## Block chain
- **Model (Main):** `Source` (rate `arrivalRate` per second) → `Service` (pool `workerPool` of `numWorkers`, `triangular(0.75, 2.5, 4)` s) → `Sink`. The Service's *On enter delay* adds `time() - agent.getBlockEnterTime()` to a HistogramData `queueTimeHD` — each customer's wait in the queue. Output `workerUtilization`.
- **Experiment `ParametersVariation`:** *Freeform* parameters, **9 runs**, *Allow parallel evaluations* **off**; both parameters left at 0 because code sets them. Experiment variables: `pyCommunicator` (not initialised), `isNewExperimentRun`.
  - *Before each experiment run* (each click on Run): `isNewExperimentRun = true`.
  - *Before simulation run* (each iteration): create `new PyCommunicator(PythonCommandType.PYTHON)` and `createAndStart(root)`; import the helper functions from `io_manager.py`; on a new experiment run call Python's `reset()` (empties the CSV log, deletes the old plot); then `root.numWorkers = pyCommunicator.runResults(int.class, "get_num_workers(%s)", getCurrentIteration() - 1)` and the same for `arrivalRate` (`double.class`).
  - *After simulation run*: `run("log_outputs(%s, %s, %s)", root.numWorkers, root.arrivalRate, root.queueTimeHD.mean())`; when `getCurrentIteration() == getMaximumIterations()`, `runResults(String.class, "save_results()")` returns a PNG name (or "None" if numpy/matplotlib are missing), shown with `Desktop.getDesktop().open(new File(name))`, and errors go to `getExperimentHost().showMessageDialog(...)`.
- **Python side:** the design lives in two functions of the 0-based iteration index — workers `index // 3 + 4` (4, 5, 6) and rate `(index % 3) / 2 + 1.5` (1.5, 2.0, 2.5 per s), a 3 × 3 grid; results go to a CSV, then a 3D bar chart (matplotlib with the non-GUI `Agg` backend).

## Resources
`workerPool`, capacity = `numWorkers`.

## Key settings worth copying
- **PyCommunicator is an agent.** On an experiment it cannot be dropped from the palette; declare it as a variable and start it with `createAndStart(root)` so it has a live agent to run in. Its connection ends with each run, hence one per run.
- **Iteration numbering:** `getCurrentIteration()` counts from 1; Python lists count from 0 — subtract 1.
- **Typed returns:** `runResults(int.class | double.class | String.class, "fmt %s", args)` casts Python's answer; `run(...)` for statements (Help 8.9.10, *Pypeline*).
- **Experiment hooks:** *Before each experiment run* fires once per click; *Before/After simulation run* once per iteration; use them to separate "reset the study" from "per-run work".
- **Queue wait in one line:** in `Service` *On enter delay*, `time() - agent.getBlockEnterTime()` is the time spent in the Service's own queue.

## KPIs instrumented
Mean queue wait per run (`queueTimeHD.mean()`), worker utilization (Output); the 3D chart of wait over workers × arrival rate.

## Pitfalls
- **Parallel runs share one communicator and one CSV.** Keep *Allow parallel evaluations* off, as the demo does (G? in `.ingest/proposals/m-basic-3.md`).
- **Desktop only:** Cloud skips experiment-level code (`videos/excel-round-trip-results-and-cloud.md`), so this set-up does not carry over; for Cloud sweeps drive runs through the Cloud API instead.
- **Python install:** Python 3 on PATH; the Microsoft Store Python is not supported (Help, *Pypeline*). The helper runs with the model folder as working directory, so the CSV and PNG appear there *(inferred from the relative file names)*.
- **One replication per point:** the design has no replications; with random arrivals, 9 single runs give noisy points. Add replications (and a seed per replication) before comparing configurations.

## Reusable idea
Put the *design of experiments* in Python (grids, Latin hypercubes, adaptive or Bayesian proposals) and let AnyLogic only execute: Python answers "what next?" in *Before simulation run* and receives the result in *After simulation run*, keyed by iteration.

## When the co-pilot should use this
A user wants Python to drive or analyse a parameter sweep on the desktop (custom sampling, plots, surrogate models) without the Cloud API. In-model Python calls: `basicmodels/basic-functionality-interactive.md`; runs driven entirely from outside: `videos/cloud-api-programmatic-runs.md`; RL training: `basicmodels/reinforcement-learning-example-abca-model.md`.
