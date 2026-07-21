# Pattern card — Adaptive Exp Random Walk
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a decision-maker's perceived state of a system lags behind a noisy reported signal, using first-order exponential smoothing (adaptive expectations).

## Block chain
A stochastic input (RandomWalk stock) is driven by a flow whose rate is drawn from a normal distribution each day, producing a wandering signal. That signal becomes the reported value fed into an adaptive-expectations structure: an auxiliary computes the Error (reported minus perceived), a flow adjusts the Perceived-Value stock at a rate of Error ÷ AdjustmentTime, and the resulting stock represents what the agent "believes" the system state to be. The gap between the two stocks illustrates perception delay.

## Resources
n/a — pure SD stocks and flows; no agent populations or resource pools.

## Key settings worth copying
- **Noise distribution:** `normal(-100, 100, 0, 50)` — mean 0, std dev 50 units/day applied as a flow to drive the random walk
- **AdjustmentTime:** a plain variable (time constant) controlling smoothing speed; longer values produce slower perception updates
- **Time unit:** Day
- **Initial value of perceived stock:** set equal to the initial reported value so the system starts in equilibrium
- **Converted from Vensim ADAPTIVE2.mdl** — useful reference for cross-tool SD equivalence

## KPIs instrumented
- Visual gap between RandomWalk (reported) and Output_PerceivedValueOfInput (perceived) over time — qualitative tracking of lag
- No explicit numeric KPI outputs; the chart comparison is the primary instrument

## Reusable idea
First-order exponential smoothing expressed as a stock-and-flow is the canonical SD technique for bounded rationality: `dPerceived/dt = (Reported − Perceived) / AdjustmentTime`. Drop this two-stock sub-model into any SD model wherever an agent or organisation needs a perception delay, forecast anchoring, or information smoothing effect.
