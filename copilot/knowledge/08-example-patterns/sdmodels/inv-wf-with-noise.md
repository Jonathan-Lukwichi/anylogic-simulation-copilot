# Pattern card — Inv-WF with Noise
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a firm manages inventory, workforce, and vacancies under stochastic demand and productivity noise, converted from a classic Vensim inventory-workforce model.

## Block chain
Customer order rate (exogenous, with step/pulse/ramp test inputs) → Demand Forecast (exponential smoothing) → Desired Production → Production Start Rate (adjusted for WIP adequacy) → WIP Stock → Production Completions → Inventory Stock → Shipment Rate → back to fill fraction.

In parallel, a workforce loop runs: Desired Labor (from desired production start rate and expected productivity) drives Desired Hiring Rate → Vacancy Creation → Vacancy Stock → Hiring Rate → Labor Stock → Voluntary Quit Rate + Layoff Rate (both draining Labor). Vacancy Cancellation is a balancing drain on the Vacancy stock.

Productivity is perturbed each time step by a switchable noise source: either normally distributed white noise (`normal(0, 4, mean, stddev)`) or a pink noise process built from two white noise inputs (`uniform(-0.5, 0.5)`) filtered through a first-order delay (correlation time constant). A switch variable mid-run can change which pink noise stream is active.

## Resources
- **Labor stock** — workers; capacity driven by desired production and expected productivity
- **Vacancy stock** — open positions; targeted at the number needed to achieve the desired hiring rate
- No discrete resource pools; all resources are continuous SD stocks

## Key settings worth copying
- Time unit: **Week**
- Noise type switch: `0` = pink noise, `1` = normally distributed white noise; toggled via a parameter
- White noise seed samples: `uniform(-0.5, 0.5)` for pink noise inputs; `normal(0, 4, mean, stddev)` for productivity shocks
- Pink noise correlation time constant: separate constants for each noise stream
- Productivity formula: `AverageProductivity * (1 + step(1, StartTimeForNoiseInProductivity) * noiseVariable)` — noise is off until a specified start week
- Inventory coverage target = normal order processing time + safety stock coverage (weeks of expected demand)
- WIP adjustment time and inventory adjustment time are key policy levers
- Willingness-to-layoff switch: `0` = no layoffs, `1` = full layoff policy

## KPIs instrumented
- Fraction of customer orders filled (service level) — ratio of achievable shipment rate to desired rate
- Inventory coverage (weeks of supply on hand)
- Workweek (average hours; can exceed or fall below target)
- Labor stock and vacancy stock over time
- Production start rate vs. customer order rate (amplification measure)

## Reusable idea
The transferable trick is the **switchable noise architecture**: a single switch parameter lets you toggle between smooth pink noise (autocorrelated, realistic demand drift) and independent white noise shocks, injected into productivity mid-simulation via a `step()` function. This lets you benchmark policy robustness under both correlated and uncorrelated uncertainty without changing the model structure — just flip the switch and re-run.
