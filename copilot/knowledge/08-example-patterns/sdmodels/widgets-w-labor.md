# Pattern card — Widgets w Labor
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models how a manufacturing firm's labor force dynamics (hiring, layoffs, attrition, vacancies) interact with production capacity, inventory, and customer demand to create amplified oscillations even under steady external orders.

## Block chain
The model is a pure System Dynamics stock-and-flow structure converted from a Vensim reference model (WIDGETS1.MDL). Three coupled subsystems run in parallel:

1. **Demand & inventory loop** — Customer orders (exogenous, with switchable test inputs: step, pulse, ramp, sine, pink noise) flow into a Demand Forecast stock via exponential smoothing. Desired Production is set to the forecast plus an inventory correction term. Finished Goods Inventory accumulates production completions and drains through shipments; a feasibility check caps shipments when inventory falls short.

2. **WIP & production loop** — Production Starts are gated by available labor capacity (labor force × productivity × workweek). A third-order delay pipeline converts starts into completions, representing the average manufacturing lead time. A WIP stock tracks in-process units; a WIP adjustment term nudges starts up or down to hit the desired WIP target.

3. **Labor market loop** — Desired Labor is derived from desired production starts divided by expected productivity. The gap between desired and actual labor drives vacancy creation or cancellation. Open vacancies fill at a rate governed by average time-to-fill. Voluntary attrition drains the Labor Force stock continuously. Layoffs are optional (controlled by a willingness-to-layoff switch) and are bounded by a maximum layoff rate.

A pink-noise generator (first-order autocorrelated noise built from a uniform() white-noise sample taken each time step) provides a realistic stochastic demand signal when selected.

## Resources
- **Labor Force** stock (workers) — initial value driven by equilibrium demand ÷ productivity
- **Vacancies** stock (open positions)
- **Workweek** auxiliary (target hours/week, constant in base case)
- **Productivity** auxiliary (widgets per worker per week, constant in base case)
- No resource pools in the DES sense; capacity is an emergent property of the labor stock

## Key settings worth copying
- **Time unit:** Week
- **Demand test inputs:** step, pulse, ramp, sinusoidal (period ≈ 50 weeks), or pink noise — toggled by a single switch parameter; makes it trivial to run stress tests
- **Pink noise construction:** `PinkNoise += (WhiteNoise − PinkNoise) / CorrelationTime` per time step, where `WhiteNoise_random = uniform()` is re-sampled each step via a recurring event
- **Inventory adjustment time** and **WIP adjustment time** are separate tunable delays — decoupling them is key to reproducing realistic oscillation frequencies
- **Layoff willingness switch:** 0 = no involuntary separation; 1 = full layoff policy — lets you compare labor-hoarding vs. lean-staffing strategies without changing the rest of the model
- **Third-order production delay** (not a simple first-order smooth) — use `DELAY3` logic to capture the S-shaped completion curve of a pipeline

## KPIs instrumented
- Production rates per week (starts vs. completions)
- Staff rates per week (hiring, attrition, layoffs)
- Vacancy rates per week (creation, cancellation, fill)
- Finished Goods Inventory level
- Fraction of customer orders filled (service level)
- Inventory coverage (weeks of demand)
- WIP inventory level
- Demand Forecast vs. actual Customer Order Rate

## Reusable idea
The central transferable trick is the **dual-adjustment architecture**: desired production corrects both for the demand forecast AND for the current inventory gap, while desired labor corrects both for expected attrition AND for the labor gap — each with its own adjustment time constant. Separating "what we expect to need" from "catching up on the gap" prevents the model from over-reacting and lets you tune responsiveness independently for inventory vs. workforce decisions. This same pattern applies to any resource-capacity problem where a stock must track a noisy signal with inertia (hospital staffing, fleet sizing, cloud compute provisioning).
