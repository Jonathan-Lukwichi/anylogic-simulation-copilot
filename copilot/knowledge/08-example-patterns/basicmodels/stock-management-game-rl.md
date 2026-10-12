# Pattern card — Stock Management Game (RL)
- **Source:** AnyLogic example model "Stock Management Game (RL)" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (SD model + Reinforcement Learning experiment + Python via Alpyne and Pypeline)
- **Problem it solves:** Make one model serve as a game, a baseline-policy testbed, an RL training environment and a trained-policy testbed, so an RL controller can be compared with human and heuristic control on the same KPIs.

## Structure
- **SD core (days):** stock `Stock` (starts at 5,000) filled by the order flow and drained by `SalesRate = Stock > 0 ?
  Demand : 0`. A new order rate takes effect gradually: `actualRate` ramps from the old to the new rate over
  `acquisitionLag` days with `ramp(...)`. `Demand` is rewritten daily by an event: two seasonal cycles plus normal noise
  (`volatility`), scaled to 0–50.
- **Decision point:** a cyclic event every `actionRecurrence` (30) days branches on the parameter `mode`:
  0 = player (pauses the run), 1 = automatic (static, random or heuristic rate), 2 = training
  (`RLExperiment.takeAction(this)`), 3 = trained policy (Python query). All paths end in `updateAssignedRate(value)`,
  which also logs the action and the stock at that moment.
- **Heuristic baseline:** raise the rate when stock is below randomised low bands, cut it above high bands, clip to [0, 50].

## Resources
n/a. Python side (model folder): `train.py` (Alpyne + Stable-Baselines3 PPO), `policy_querier.py`, `requirements.txt`,
trained `SMG_PPO.zip`.

## Key settings worth copying
- **RL experiment** (Help 8.9.10, *Reinforcement Learning experiment*) — an interface for export, not something that runs
  in the IDE; one per model:
  - *Observation*: fields `stock`, `last_stock`, `order_rate`, `demand`, filled from `root`;
  - *Action*: `order_rate`, applied as `root.updateAssignedRate(limit(0, order_rate, 50))`;
  - *Configuration*: `acquisition_lag_days`, `action_recurrence_days`, `stop_condition_limits`, `demand_volatility` —
    validated and clamped, then assigned **directly** to root parameters (the Help says no `set_` calls here);
  - *Simulation run stop condition*: stock ever outside the configured limits (from a daily Statistics element).
- **Decision point:** `takeAction(agent)` schedules a pause in zero time; repeated calls in one action add nothing.
- **Reward lives in Python:** the Alpyne environment scores each step (here 1 at stock 5,000, falling off with the 4th
  power, floored at −1); training wraps the env to rescale observations and actions to [−1, 1].
- **Inference inside the model:** a `PyCommunicator` (enabled only when `mode == 3`) imports the querier on startup;
  each decision calls `pyCom.runResults(double.class, "querier.query([%s, %s])", Stock, actualRate)`. The querier undoes
  the training-time scaling by hand.
- Testing without a platform (8.8.6+): `createObservation()` / `getObservation(root, obs)`, `applyAction(...)`,
  `applyConfiguration(...)`, `checkEpisodeStopCondition(root)`.

## KPIs instrumented
`amountSold` (Output), daily demand dataset, histogram of assigned rates, 2-D histogram of demand vs rate, stock
statistics (drives the stop condition).

## Pitfalls
- **Scaling mismatch:** a policy trained on rescaled spaces must be queried with the same scaling (see the gotcha
  proposal); keep the constants in one place.
- **Leaked information:** `demand` is in the observation "for debugging only"; the training script feeds the policy just
  `stock` and `order_rate`. Decide explicitly what the controller may see.
- `pythonExecPath` holds the author's absolute path — point it to your own environment (an executable path or a
  command found on PATH, see `basic-functionality-interactive.md`); the Pypeline add-on must be installed for the model
  to compile.
- Randomness: the Help advises a random seed for training so the agent sees variability; compare policies over the same
  seeds afterwards.
- Alpyne needs the exported model (`ModelExported/model.jar`); Microsoft Bonsai export was dropped in 8.8.6 (release notes).

## Reusable idea
Route every control path through one decision event and one "apply action" function, selected by a mode parameter.
The same model then runs human play, rule-based baselines, RL training and trained-policy testing, and all of them are
judged on identical outputs.

## When the co-pilot should use this
Any request to "add RL" or "compare AI control with a rule" — inventory control, dispatching, staffing. Fill the gap
behind `templates/rl-pipeline/`: define spaces and the decision point in AnyLogic, reward and training in Python, and
report baseline vs heuristic vs RL on the same KPIs (INSTRUCTIONS rule). Related: `basic-functionality-interactive.md`
(Pypeline calls), `../bigbook/sd-instant-charts-and-step-pause-flight-simulator.md` (the original game),
`../videos/cloud-api-programmatic-runs.md` (route choice).
