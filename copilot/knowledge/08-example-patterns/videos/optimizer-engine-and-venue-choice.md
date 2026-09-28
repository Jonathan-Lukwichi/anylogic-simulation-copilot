# Pattern card — Choosing the sim-opt engine and venue: OptQuest vs Genetic vs Custom experiment vs Cloud
- **Source:** AnyLogic video "Webinar | Simulation-Based Optimization in AnyLogic" (https://youtu.be/YyDJDqMqYng) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Picking the optimization engine and where to run it, given lever count, licensing, flexibility and compute.

## Mechanism
| Option | Use when | Watch out |
|---|---|---|
| Optimization experiment, engine **OptQuest** | ≤ 7 levers and ≤ 500 iterations, or you need varying replications | The bundled licence caps OptQuest at 7 variables and 500 iterations. Exporting an OptQuest experiment as a standalone app is a paid option (Professional). |
| Optimization experiment, engine **Genetic** (AnyLogic 8.8.4+) | Many levers, long searches, or a model you will export to a client | Fixed replication count only. |
| **Custom experiment** (code only, no UI) | Constraints or bounds built from data; 100+ parameters set in loops; logging every iteration or replication (e.g. to CSV); faster headless runs | You own the loop and the bookkeeping. The OptQuest route through `ExperimentOptimization` is documented as Professional-only. |
| **AnyLogic Cloud** optimization | The search is compute-bound and needs wide parallelism | KPIs must be Output elements. The plain "Optimization" type runs each candidate once. |

- **Quality is similar.** In the presenter's experience, OptQuest (OptTek, proprietary, scatter-search family) and Genetic (built by AnyLogic on the Java jMetal library) give very similar answers. Choose on limits, licensing and control, not on answer quality.
- **Sources.** The limits, licensing and replication support were checked against AnyLogic's 8.8.4 release notes and Help. The webinar itself only mentioned the export licence.

## Resources
n/a

## Key settings worth copying
- **Engine choice (GUI):** set the **Optimization engine** property of the Optimization (or Calibration) experiment to OptQuest or Genetic.
- **Custom-experiment skeleton.** These names are verified; check exact signatures in your version's Javadoc, and start from AnyLogic's "Optimization in Custom Experiment" demo model.
  - `ExperimentOptimization.createOptimization(Engine engine, OptimizationCallback callback)` returns an OptQuest optimization.
  - The callback `evaluate(COptQuestOptimization optimization, COptQuestSolution solution, Engine engine)` runs once per iteration or replication. Inside it:
    1. `Main root = engine.createRoot();`
    2. set the model parameters from each variable's `GetCurrentValue()`;
    3. `engine.start(root); engine.runFast();`
    4. report the result with `optimization.SetCurrentObjectiveValue(value)`;
    5. `engine.stop();`
  - `monitorStatus(...)` runs after each iteration, once feasibility is known.
  - Variables such as `COptQuestContinuousVariable` take `SetLowerBound()` and `SetUpperBound()`.
  - Drive the search with `SetMaximumIterations(n)`, `Optimize()` and `GetBestSolution()`.
  - Both engines implement `IOptimization`, as `OptQuestOptimization` and `MetalOptimization`. OptTek publishes the OptQuest API docs online.
- **Cloud (2.4.0+):**
  - Experiment types are **Optimization** and **Optimization with replications**.
  - List the levers as Run Configuration Inputs.
  - Wrap the objective and each requirement expression in an **Output** element and list it under Outputs.
  - Export mechanics are in `videos/cloud-decision-tool-for-stakeholders.md`.
  - Constraints exist but may need enabling in the experiment's dashboard settings, as shown in the webinar.

## KPIs instrumented
n/a (engine progress only: iteration, current and best objective, feasibility)

## Pitfalls
- Planning 20 levers on the default OptQuest. It takes at most 7.
- Shipping a client an exported model with an OptQuest optimizer: an unexpected licence cost. Genetic exports free.
- Choosing Genetic and then expecting "Varying number of replications". Genetic does not support it.
- A KPI left as a plain function or variable. The Cloud optimizer cannot see it.
- Expecting Cloud to run a custom optimizer. Cloud receives the simulation model, not your custom experiment, so a custom optimizer runs locally (the presenter's understanding; unverified).
- PLE or University users: check the edition before prescribing the custom-experiment OptQuest API.

## Reusable idea
Pick the engine from facts you can state up front: lever count, the need for per-iteration control, deployment licensing and compute. The same black-box loop can also be driven from Python (see `basicmodels/machine-optimizer.md` and `models/supply-chain-optimizer.md`).

## When the co-pilot should use this
- At Phase 0, when the intake says "let it search".
- Again at build time, before the user creates the experiment.
- When a user reports hitting OptQuest's limits or plans to hand the model to a client.
