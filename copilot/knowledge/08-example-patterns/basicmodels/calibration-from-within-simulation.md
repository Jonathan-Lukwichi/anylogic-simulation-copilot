# Pattern card — Calibration from Within Simulation
- **Source:** AnyLogic example model "Calibration from Within Simulation" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (experiment framework, any paradigm)
- **Problem it solves:** Launch a calibration (an OptQuest search over a model parameter) on demand from an interactive Simulation experiment, and bring the fitted value back into that experiment, without leaving it.

## Structure
- **Main (the model):** input parameter `mainParameter`, unknown parameter `parameterToCalibrate`, and a dynamic variable `calibrationCriterion` = squared gap between the unknown and a target computed from the input (a toy: the target is `mainParameter²`, so the right answer is known).
- **Simulation experiment `CallToCustomExperiment`:** an experiment-level variable `mainParameter` bound to a slider, a result variable `calibrationResult` shown in a text, and a button *Run calibration*. The button disables itself, calls the experiment's function `callCustomExperiment()`, then re-enables itself.
- **The call (the technique):** the function constructs the custom experiment with the *calling experiment* as the constructor argument, copies the input into a public field of the custom experiment, calls `run()` — which returns only when the search is over — and reads the answer from another field.
- **CustomExperiment:** its *Additional class code* declares the two hand-over fields (`mainParameter`, `calibratedParameter`). Its Code builds an engine with `createEngine()` and `setStopTime(1)`, one `COptQuestContinuousVariable` in [0, 100000], a `COptQuestUserControlledObjective` set to minimise, and `ExperimentOptimization.createOptimization(engine, callback)`. Each `evaluate(...)` builds a **fresh root** (`new Main(engine, null, null)`), sets both parameters (the input from the field, the candidate from `solution.GetVariableValue(v)`), runs `engine.start(root)` + `engine.runFast()`, reports `solution.SetObjectiveValue(obj, root.calibrationCriterion)` and calls `engine.stop()`. A warm start at 50 is added; 500 iterations max; the best value goes into `calibratedParameter`. The OptQuest calls themselves are carded in `optimization-in-custom-experiment.md`.

## Resources
n/a

## Key settings worth copying
- Help 8.9.10 (*Custom experiment*): a custom experiment may be run from another experiment by passing that experiment to its constructor; from model code use `new MyCustomExperiment(getExperiment())`. Public fields in *Additional class code* are the whole interface — inputs before `run()`, outputs after.
- Keep the objective a single dynamic variable or function on Main (here a squared error); for several targets, sum weighted squared errors there, not inside the callback.
- Button hygiene: `button.setEnabled(false)` before the blocking call and `true` after, so a second click cannot start a second search.
- Imports: `com.opttek.optquest.*` in the custom experiment's *Imports section*.

## KPIs instrumented
The fitted value and a trace line per iteration (iteration, candidate, objective, best objective) from `monitorStatus(...)`.

## Pitfalls
- **Edition:** the Help page for Custom experiment carries the PRO badge — check the user's edition before prescribing this.
- **Nested runs are separate models.** Every iteration starts its own engine and root; nothing in the running Simulation is touched or read. Pass all needed inputs through fields. Set every parameter of the new root, or call `root.setParametersToDefaultValues()` first (Javadoc: provided for setting up a custom experiment's top-level agent); whether `engine.start()` fills unset parameters by itself is *(unverified)*.
- **Engine settings are not inherited** from the Simulation experiment: seed, stop time and simultaneous-event order are whatever the new engine gets. Set them (`setStopTime`, `setDefaultRandomGenerator(new Random(seed))`, `setSimultaneousEventsSelectionMode(...)`) — the sister demo *Custom Experiment Interacting with Console* sets LIFO explicitly.
- **One run per candidate** is fine for this deterministic toy; for a stochastic model average replications inside `evaluate`, or the fit follows noise (gotcha G11).
- **The demo only displays** `calibrationResult`; to use it, bind the model parameter's value on the experiment's Parameters page to that variable *(suggested)*, and keep the experiment screen visible (G50).

## Reusable idea
Treat a custom experiment as a subroutine: any experiment (or Main via `getExperiment()`) can call it with inputs and receive outputs. Uses: calibrate-then-run buttons, an embedded "what-if solver" on an experiment page, or a console-driven loop (the sister demo reads commands from `System.in`, and each command triggers a fresh `createEngine` / root / `runFast` / `stop` cycle).

## When the co-pilot should use this
- A user wants to fit one or two parameters to data and then run scenarios in the same session.
- An interactive tool must show a fitted or optimised value before the main run.
- Desktop only: Cloud runs the model under its own experiment framework, and desktop experiments and their code are not uploaded (G49); for Cloud use its Optimization run types (`videos/optimizer-engine-and-venue-choice.md`).

## Additions (8.9.10 review, 2026-10-01)
- A custom experiment can take its input from the command line of an exported application: leave the field at `Double.NaN` and read `getCommandLineArguments()[0]` while it is still NaN, failing loudly if absent (8.9.10 *Simple Custom Experiment*). Useful for batch scripts — mind that standalone export is a paid option since 8.9.10.
