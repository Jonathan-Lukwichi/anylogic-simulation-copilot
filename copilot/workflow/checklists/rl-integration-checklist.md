# RL integration checklist (show AI efficiency)
- [ ] Baseline model runs and KPIs are trustworthy
- [ ] Decision point exposed as the RL action
- [ ] Observation, action, configuration and stop condition defined in the RL experiment; reward computed in the Alpyne / Gym wrapper from observation fields (the 8.9.10 RL experiment has no reward field)
- [ ] Configuration code assigns fields directly (`root.x = …`), never `set_x(...)` — the model may not be initialised yet (Help 8.9.10; gotcha G120)
- [ ] The trained policy is queried with the same observation/action scaling it was trained with (gotcha G121)
- [ ] Model exported; driven from Python via Alpyne
- [ ] Policy trained (Stable-Baselines3 PPO) on the same seed/scenario
- [ ] Baseline vs ML vs RL compared on identical KPIs
- [ ] Efficiency delta reported (time, utilisation, cost)
