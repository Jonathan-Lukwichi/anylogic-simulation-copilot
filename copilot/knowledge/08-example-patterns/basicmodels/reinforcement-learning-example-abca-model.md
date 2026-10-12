# Pattern card — Reinforcement Learning Example - ABCA Model
- **Source:** AnyLogic example model "Reinforcement Learning Example - ABCA Model" (basicmodels), AnyLogic 8.9.10, with its shipped Python scripts — distilled, original wording
- **Paradigm:** DES + RL experiment (policy trained outside AnyLogic with Alpyne and Stable-Baselines3)
- **Problem it solves:** Train and test a policy on an existing DES model from Python: which side owns the reward, how an episode starts and ends, and how to keep a no-AI baseline in the same model.

## Block chain
- **Base model:** the costing line of `models/activity-based-costing-analysis.md` — `Source` → buffer `Queue` (capacity `sizeBufferQueues`; an overflow sets the flag `exceededCapacity`) → `Seize` A → buffer → `Seize` B → `Delay` (process) → `Release` A → `Queue` → conveyor → `Release` B → `Sink`, with cost per product `totalCostPerProduct()`.
- **Decision point:** a cyclic event (time 0, then every 181 days). If Main's boolean `enableLearningAgent` is false it calls `self.reset()` (cancels itself) and returns; otherwise `ExperimentReinforcementLearning.takeAction(this)`. The same model therefore runs as the plain baseline too.
- **RL experiment** (AnyLogic-side basics — spaces, `takeAction`, configuration rule, test functions — are in `basicmodels/pathfinder.md`):
  - Observation, 18 `int`/`double` fields: current settings, both pools' `utilization()`, each buffer's fill ratio (size ÷ capacity), products done, each cost category per product, `costPerProduct`, the overflow flag as 0/1, time.
  - Stop condition: `root.exceededCapacity || root.time(DAY) >= 36500`.
  - Action: `nResA`, `nResB` (int), `processTime`, `conveyorSpeed` (double), applied with `set_…`, then `resetCosts()` and `resetStats()` on both pools.
  - Configuration: arrival rate, the four starting settings and the buffer size, by plain assignment.
- **Python side** (`train_sac.py`, `test_sac.py`, `single_run.py`; requirements `anylogic-alpyne`, `gymnasium` 0.29.1, `stable-baselines3[extra]`): export the RL experiment and unzip it to `ModelExported/model.jar` first.

## Resources
Pools A and B sized by the action (`ResourceACapacity`, `ResourceBCapacity`); custom unit type with busy/idle cost rates.

## Key settings worth copying
- **Alpyne sim handle:** `AnyLogicSim("ModelExported/model.jar", engine_overrides=dict(seed=…, stop_time=UnitValue(180, "DAY")), config_defaults=dict(sizeBufferQueues=…))`. `sim.schema` prints the spaces; `sim.reset(arrivalRate=…)` starts an episode with that configuration; `sim.take_action(nResA=…, nResB=…, processTime=…, conveyorSpeed=…)` runs to the next decision point or the end and returns a status with `.observation['costPerProduct']`, `.stop` (the stop condition fired) and `.progress` (1.0 at the stop time); `sim.outputs()` returns the model's Output elements.
- **Gym wrapper:** subclass `AlpyneEnv` and fill `_get_config` (a random arrival rate per episode), `_get_obs` (here only the arrival rate, as a `(1,)` box), `_to_action` (round pool sizes to `int`, cast the rest to `float`), `_calc_reward`, `_is_terminal` (= `status.stop`) and `_is_truncated` (= `status.progress >= 1.0`). The action box bounds encode feasibility: 1–20 units per pool, process time 1–12, conveyor speed ≥ 1e-6.
- **Reward lives in Python:** minus cost per product, and an extra −1000 when the buffer overflowed (the terminal failure). The RL experiment has no reward field; expose whatever the reward needs as observation fields.
- **Training:** `make_vec_env(..., n_envs=5)` builds five environments, each with its own sim and a fresh seed per run (`engine_overrides=dict(seed=next_num)`); SAC `MlpPolicy` (two 512-unit layers), 10,000 steps, saved as a zip.
- **Testing:** load the policy, call `policy.predict(np.array([rate]))` for arrival rates 0.25–5.0 (twice the training range, to see extrapolation) on **one fixed-seed** sim, run each suggested setting, tabulate setting and cost per product.

## KPIs instrumented
Cost per product (reward), buffer overflow (failure), pool utilizations and buffer fill, cost breakdown (idle, waiting, processing, moving); Output `outputTotalCostPerProduct` for `sim.outputs()`.

## Pitfalls
- **Episode shape (inferred from the scripts):** with a 180-day stop time and a decision every 181 days, each episode has exactly one decision, at time 0. The policy is a *configuration chooser* for a given demand — contextual optimization, not sequential control. Check it against a plain optimization experiment per arrival rate before claiming that RL adds value.
- **Reset statistics after each action**, as the demo does; otherwise the next observation mixes the old and the new setting.
- **Integer actions** come out of SAC as reals; round them in `_to_action`, never in the model's Action code alone.
- **Seeds:** random seeds while training (the Help recommends it), one fixed seed when comparing policies; otherwise differences are noise.
- The base model still uses the PML `Conveyor` block, deprecated since 8.9.5 (G7); build new models with the Material Handling Library.

## Reusable idea
Split the work: AnyLogic defines the environment (observe, act, configure, stop); Python owns learning (reward, termination vs truncation, policy, evaluation). Keep a boolean that bypasses the decision event, so the baseline and the RL run come from one model and are compared on the same KPIs.

## When the co-pilot should use this
- A user wants to train a policy on an AnyLogic model with Stable-Baselines3 or Gymnasium, or asks where the reward goes.
- Planning the "baseline vs ML vs RL" comparison required by `INSTRUCTIONS.md`: start from this card, the checklist `workflow/checklists/rl-integration-checklist.md` and `templates/rl-pipeline/`.
- Related: `basicmodels/pathfinder.md` (multi-step episodes, replay of a learned policy inside AnyLogic); `06-ai-ml-integration/README.md`.
