# Pattern card — Adaptive Expectations
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a decision-maker's perceived value of a noisy input gradually converges toward the reported value via first-order exponential smoothing (adaptive expectations).

## Block chain
A single **StockVariable** (`Output_PerceivedValueOfInput`) accumulates over time.  
An **AuxVariable** computes the `Error` as the gap between the exogenous reported input and the current perceived value.  
A **Flow** feeds into the stock at the rate `Error / AdjustmentTime`, closing the feedback loop: the larger the gap, the faster perception adjusts.  
The exogenous `Input_ReportedValueOfVariable_X_` is driven by `normal(20, 200, 100, 25)` — a normally distributed signal with seed 20, max 200, mean 100, and standard deviation 25.

## Resources
n/a — pure equation-based SD; no agents, queues, or resource pools.

## Key settings worth copying
- **Smoothing formula:** `Flow = (Reported − Perceived) / AdjustmentTime` — the canonical first-order lag
- **Input distribution:** `normal(seed, max, mean, std) = normal(20, 200, 100, 25)` for a bounded noisy signal
- **Time unit:** Day
- **ODE solver:** Euler (primary); RK45+Newton available for stiff/mixed systems
- **AdjustmentTime** is a plain `PlainVariable` (constant), making it easy to expose as a slider for sensitivity analysis

## KPIs instrumented
- Time-series plot of `Input_ReportedValueOfVariable_X_` vs `Output_PerceivedValueOfInput` — visual convergence gap
- Implicit: steady-state lag (how many days until perception tracks the signal)

## Reusable idea
The **first-order exponential smoothing stock** pattern — `dS/dt = (Target − S) / τ` — is the single most transferable SD building block. It represents any gradual belief update, demand smoothing, inventory adjustment, or workforce ramp-up. Expose `τ` (AdjustmentTime) as a parameter slider to instantly show how faster or slower adaptation changes system responsiveness.
