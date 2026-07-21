# Pattern card — Labor w Layoffs
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a firm manages its workforce by balancing hiring, voluntary attrition, and optional layoffs against a fluctuating desired labor target.

## Block chain
Two stocks sit at the core: **Labor** (the active headcount) and **Vacancies** (open positions). Four flows connect them:

1. **Hiring** — fills vacancies and adds workers; rate = Vacancies / AverageTimeToFill  
2. **Quit Rate** (voluntary attrition) — drains Labor; rate = Labor / AverageDurationOfEmployment  
3. **Layoff Rate** — drains Labor when desired hiring is negative and the firm allows layoffs; capped by a maximum rate derived from LayoffTime  
4. **Vacancy Creation / Cancellation** — opens or closes positions based on the gap between desired and actual vacancy stock; cancellation rate bounded by MinimumCancellationTime

Auxiliary variables compute **Desired Hiring Rate** (close the gap between Desired Labor and actual Labor plus expected attrition over a time-to-adjust horizon) and **Desired Vacancies** (vacancies needed to hit the desired hiring rate given expected fill time).

A **Pink Noise** sub-structure (first-order exponential smoothing of white noise) generates autocorrelated random demand signals; the model also supports step, pulse, ramp, and sine-wave test inputs for Desired Labor.

## Resources
- No discrete resource pools — workforce modelled as continuous stock (persons)
- Key capacity parameters: AverageDurationOfEmployment, AverageTimeToFill, LayoffTime

## Key settings worth copying
- **Time unit:** Week  
- **White noise seed:** `uniform()` sampled each time step via a timed event  
- **Pink Noise:** first-order lag of white noise — correlation time and standard deviation are user parameters  
- **Willingness to lay off** (0–1 switch): set to 0 for a pure no-layoff policy, 1 for symmetric hire/fire response  
- **Input mode selector:** step / pulse / ramp / sine / pink-noise driven through a single dimensionless Input variable  
- Desired Labor adjustment horizon: a smoothing time constant (weeks) that controls how aggressively the firm chases the target

## KPIs instrumented
- Labor stock trajectory vs. Desired Labor  
- Vacancies stock over time  
- Hiring rate, quit rate, layoff rate flows  
- Pink Noise value (to compare demand volatility vs. workforce response)

## Reusable idea
The **bounded layoff flow** pattern: compute a *desired* layoff rate from a policy rule, then take the minimum of that and a *maximum feasible* rate (stock / delay time). This prevents the model from laying off more workers than exist and enforces a realistic adjustment speed — a broadly applicable guard clause for any SD stock that must not go negative due to overly aggressive outflow rates.
