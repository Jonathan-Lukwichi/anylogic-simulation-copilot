# Pattern card — Optimization in Custom Experiment
- **Source:** AnyLogic example model "Optimization in Custom Experiment" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (simulation-based optimisation in code)
- **Problem it solves:** Run an optimisation loop entirely in code (no Optimization-experiment UI) with either the Genetic engine or OptQuest, including constraints on inputs and requirements on outputs.

## Structure
`Main` has two decision parameters (`doubleParam`, `intParam`) and `getObjective()`. Two Custom experiments:
- **CustomOptimizationGenetic** uses a Java class **`GeneticOptimization<R>` that ships inside the model** (a wrapper around the open-source jMetal NSGA-II; not part of the AnyLogic API — copy the class into your model). You subclass it anonymously and override `prepareEngine()` (required: `createEngine()`, seed, stop time), optionally `prepareRoot(root, cs)` (fixed inputs) and `afterIterationCallback(root, cs)` (tracing). Then: `addIntegerVariable("intParam", -2, 10)`, `addDoubleVariable("doubleParam", -0.3, 3.14)`, `enableParallelMode()`, `addConstraint(root -> …)`, `addRequirement(root -> …)`, `setObjectiveEvaluator(root -> root.getObjective())`, `run(500)`, `getResult()`, and the static helpers `getVariable(cs, name)` / `getIteration(cs)`; feasibility via jMetal `ConstraintHandling.isFeasible(cs)`.
- **CustomOptimizationOptQuest** uses `ExperimentOptimization.createOptimization(engine, callback)`: variables `COptQuestContinuousVariable` / `COptQuestIntegerVariable` with `SetLowerBound/SetUpperBound`; objective `COptQuestUserControlledObjective` + `SetMinimize()`; in `evaluate(optimization, solution, engine)` create the root, read `solution.GetVariableValue(var)`, `engine.start(root)`, `engine.runFast()`, write `solution.SetObjectiveValue(obj, value)`, `engine.stop()`; `monitorStatus(...)` for per-iteration tracing. Then `AddVariable`, `AddObjective`, `SetMaximumIterations(500)`, optional warm start (`CreateSolution()`, `SetVariableValue`, `AddSuggestedSolution`), `Optimize()`, `GetBestSolution()` (`IsFeasible()`, `GetIteration()`); errors arrive as `COptQuestException` (`Description()`).

## Resources
n/a

## Key settings worth copying
- **Sign convention (Genetic wrapper):** every constraint or requirement is written as `F(root) >= 0` — e.g. "intParam ≥ 5" becomes `root.intParam - 5`.
- **Constraints are checked before the run** (on inputs): if violated, the simulation is skipped and the objective set to infinity — cheap pruning. **Requirements are checked after the run** (on outputs). Same meaning as in the GUI (gotcha G8).
- **Minimisation only** in the wrapper: to maximise, return the negative of the KPI.
- Decision-variable names must match the root agent's parameter names exactly (set by reflection; a typo throws at start).
- `enableParallelMode()` only before `run(...)`; each evaluation then gets its own engine from `prepareEngine()`, so all run set-up belongs there.

## KPIs instrumented
Trace table per iteration (iteration, variables, objective, best so far); best solution and its feasibility at the end.

## Pitfalls
- The model description promises constraints and requirements in both versions, but the 8.9.10 OptQuest version defines none — only the Genetic version shows them.
- Both versions fix the seed (1) and do one run per candidate: fine for this deterministic toy, a lucky-optimum trap for stochastic models (see gotcha G11; add replications and re-verify).
- Keep a suggested (warm-start) solution inside the variable bounds; the demo's 50/50 lies outside them.
- Custom experiments (and `runFast()`) are listed among AnyLogic **Professional** features in Help; PLE users cannot run this route.

## Reusable idea
When the GUI optimiser is too rigid (data-driven bounds, many variables added in loops, custom logging, parallel control), copy the demo's `GeneticOptimization` class and drive it from a Custom experiment: variables by name, constraints as input checks that skip runs, requirements as output checks, objective as a lambda.

## When the co-pilot should use this
When a user needs optimisation in code, Genetic in a custom experiment, many or computed constraints, or asks for the exact OptQuest custom-experiment calls. For engine/venue choice see `videos/optimizer-engine-and-venue-choice.md`.
