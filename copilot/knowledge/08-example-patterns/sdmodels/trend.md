# Pattern card — TREND
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how decision-makers perceive and lag behind the true growth rate of an input signal, enabling analysis of trend-detection delays in management or forecasting contexts.

## Block chain
Three stock-and-flow chains capture the perception pipeline:

1. **Perceived Present Condition** (stock) — adjusts toward the actual input value via first-order smoothing; time constant `TPPC` (perception lag).
2. **Reference Condition** (stock) — an exponentially weighted average of past perceived values; time constant `THorizon` (how far back decision-makers look).
3. **Perceived TREND** (stock) — adjusts toward the Indicated TREND (the ratio of Perceived Present Condition to Reference Condition, minus 1) via first-order smoothing; time constant `TPT` (trend adjustment delay).

The **test input** driving the system is a synthetic exponential: `InitialInput * exp(GrowthRate * time)`.

**Indicated TREND** = (PerceivedPresentCondition / ReferenceCondition) − 1, representing the fractional growth rate implied by the gap between "now" and "the past".

## Resources
n/a — pure SD model, no agent populations or resource pools.

## Key settings worth copying
- **Time unit:** Day
- **Test input formula:** `InitialInput * exp(GrowthRate * time())` — easy to swap for real data
- **TPPC** (time to perceive present condition): controls reporting/measurement lag
- **THorizon** (time horizon): longer values filter out short-term noise in growth estimates
- **TPT** (time to perceive trend): models how slowly beliefs about growth rates change
- All three time constants are independent parameters — vary them separately to study sensitivity
- Model converted from Vensim MDL via AnyLogic import; the three-stock structure is a reusable TREND macro pattern from Sterman (2000)

## KPIs instrumented
- **Output (Perceived TREND)** vs. true GrowthRate — tracks tracking error over time
- Visual comparison of Indicated TREND vs. Perceived TREND to show smoothing effect
- Convergence time — how long before perceived trend catches up to actual growth rate

## Reusable idea
Encapsulate belief-formation delay as a three-level perception pipeline (present condition → reference condition → perceived trend), each with its own time constant. This lets you independently tune measurement lag, memory horizon, and belief-adjustment speed — a transferable pattern for any SD model where agents or managers must infer rates of change from noisy, delayed signals.
