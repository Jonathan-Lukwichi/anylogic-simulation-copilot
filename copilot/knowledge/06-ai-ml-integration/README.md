# 06-ai-ml-integration

RL/Alpyne, ML-in-process efficiency. AnyLogic AI, FlexSim RL.

- **ML-informed recipe (no RL):** forecast → input file → simulation-optimization with an output
  requirement → compare against the baseline on the same KPIs —
  `../08-example-patterns/videos/forecast-driven-staffing-optimization.md`.
- **Driving a model from code — pick the route:** AnyLogic Cloud API (Python/Java/JS/REST; needs a
  subscription or Private Cloud), Alpyne (RL training loop), Pypeline (call Python from inside the
  model), or a standalone export — `videos/cloud-api-programmatic-runs.md`.
- **RL recipe (worked examples):** spaces (observation, action, configuration) and the stop condition
  live in AnyLogic's RL experiment, and decision points call `takeAction(...)`; reward and training
  live in Python (Alpyne); the trained policy is queried back inside the model through Pypeline with
  the *same* scaling (G121); a mode parameter runs human, heuristic and RL control on identical KPIs —
  `../08-example-patterns/basicmodels/stock-management-game-rl.md`,
  `basicmodels/reinforcement-learning-example-abca-model.md` (Alpyne `AnyLogicSim`, SAC training);
  traps G120–G121.
- **ML predictors inside a simulation:** when a trained model supplies inputs (durations, rates,
  routing), (a) add the predictor's residual spread to a point prediction used as a service time —
  otherwise waiting and blocking come out too low; (b) seed any Python-side randomness from AnyLogic
  (G17); (c) test the feature-encoding function against rows the training code already scored;
  (d) watch self-feeding forecasters, which drift into their own closed-loop behaviour; (e) label
  ML-driven runs as forecasts beside the baseline — `../08-example-patterns/models/simple-hospital-ai-testbed.md`.
- **Which search technique at all** (LP/MILP vs sim-opt vs RL vs ML): `../07-optimization/README.md`.

See SOURCES.md for the exact links and download/fetch-live status.
