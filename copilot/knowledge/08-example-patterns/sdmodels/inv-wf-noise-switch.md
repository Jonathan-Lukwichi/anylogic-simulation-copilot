# Pattern card — Inv-WF Noise Switch
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models a firm's inventory and workforce adjustment loop under stochastic productivity, letting the analyst toggle between two noise regimes mid-run to compare their effects.

## Block chain
Stocks (levels) represent Labor, Vacancies, and WIP Inventory. Aux variables compute desired rates — desired hiring, desired layoff, desired vacancy creation — and feed back into flow rates (hiring rate, quit rate, layoff rate, production start rate, shipment rate). A separate pink-noise sub-chain generates correlated random disturbances to productivity; a switch variable redirects that chain from one pink-noise stream to another at a configurable switch time. A second switch lets the modeler choose between pink noise and normally distributed white noise for the productivity perturbation altogether.

## Resources
No agent pools or DES resource pools. Stocks act as aggregate accumulators:
- Labor (workers employed)
- Vacancies (open positions)
- WIP (work-in-progress inventory)

## Key settings worth copying
- **Noise switch time:** `SwitchTime` parameter controls the week at which the pink-noise input is redirected — useful for scenario comparisons within a single run.
- **Noise type switch:** binary switch (0 = normally distributed white noise, 1 = pink noise) for productivity perturbation.
- **White noise draws:** `uniform(-0.5, 0.5)` sampled each time step to drive the pink-noise integrator; separate stream `uniform()` for a third noise variable.
- **Productivity perturbation:** `1 + step(1, StartTimeForNoiseInProductivity) * normal(0, 4, Mean, StdDev)` — noise only activates after a specified start time.
- **Time unit:** Week.
- **Layoff policy:** `WillingnessToLayOff` parameter (0 = no-layoff policy, 1 = symmetric hire/fire response).
- **Adjustment times:** separate time constants for labor adjustment, vacancy adjustment, expected time to fill vacancies, and productivity smoothing — all tunable.

## KPIs instrumented
- Fraction of customer orders filled (shipment rate vs. desired rate ratio)
- Expected vs. actual productivity
- Labor force level vs. desired labor
- Vacancy stock vs. desired vacancies

## Reusable idea
The mid-simulation noise-stream switch: by wiring two independent pink-noise generators through a conditional switch keyed on simulation time, you can subject the same model to different stochastic environments in a single run — eliminating the need for separate scenario experiments and making the structural response to a change in noise character directly visible on a single time chart.
