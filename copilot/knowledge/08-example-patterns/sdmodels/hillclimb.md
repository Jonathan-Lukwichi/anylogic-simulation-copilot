# Pattern card — Hillclimb
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a system state anchors on its current level and then drifts toward a desired state that is itself shifted by exogenous pressures — capturing the "hillclimbing" or ratchet behaviour seen in goal adjustment dynamics.

## Block chain
One **Stock** (the system state, initialised at 100 units) feeds a **Flow** that drives the state toward a desired level. A set of **Auxiliary variables** computes:
1. External pressure — a step function that increases at one point in time and decreases at another.
2. Desired state — anchored on the actual state and then multiplied by the exponential of the weighted external pressure, allowing arbitrary nonlinear goal shifts.
3. State adjustment — the gap between desired and actual state divided by an adjustment time constant, producing the inflow/outflow rate for the stock.

There are no agent populations or process-flow blocks; the entire model is a small stock-and-flow loop with lookup-style auxiliary calculations.

## Resources
n/a — no resource pools or agent populations. The single stock represents the system's condition level.

## Key settings worth copying
- **Time unit:** Day
- **Desired-state formula:** `actualState * exp(sensitivityParameter * externalPressure)` — the exponential form keeps the desired state positive and multiplicatively scales the anchor, making it straightforward to add multiple independent pressure terms.
- **Adjustment flow:** `(desiredState - state) / stateAdjustmentTime` — classic first-order goal-gap formulation.
- **Pressure schedule:** two discrete time parameters (increase time, decrease time) with fractional increase/decrease magnitudes, making the exogenous driver easy to parameterise in experiments.
- **Converted from Vensim** (HILLCLIM1.mdl) via AnyLogic import — confirms the pattern is textbook Sterman-style SD.

## KPIs instrumented
- Trajectory of the **system state** stock over time (primary output plot).
- **Desired state** auxiliary tracked alongside actual state to visualise the gap.
- **External pressure** auxiliary shown to correlate input shocks with state response.

## Reusable idea
The transferable trick is separating goal formation from goal pursuit: anchor the desired state multiplicatively on the current state (so relative gaps drive behaviour) and apply external pressures through an exponential scaling factor. This prevents negative desired states and naturally produces diminishing returns — a pattern directly applicable to demand forecasting, inventory target-setting, or any model where aspirations chase reality while being nudged by outside forces.
