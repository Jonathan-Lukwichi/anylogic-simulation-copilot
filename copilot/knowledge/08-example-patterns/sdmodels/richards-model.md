# Pattern card — Richards Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models population growth toward a carrying capacity using a generalised logistic curve whose shape is controlled by a single exponent parameter.

## Block chain
A single Stock (Population) accumulates a Flow (Net Birth Rate). The net birth rate is the product of the current population and a Fractional Net Birth Rate auxiliary. The fractional rate is itself a declining function of how close the population is to the carrying capacity, raised to the power of an exponent m. When m = 2 the curve degenerates to the standard logistic (S-curve); as m approaches 1 the shape converges toward the Gompertz curve. Time is scaled so that one time unit equals 1/g* (where g* is the maximum fractional growth rate), making the baseline logistic run in normalised time.

## Resources
n/a — no resource pools or agent populations; purely a stock-and-flow structure with five auxiliary parameters.

## Key settings worth copying
- **m (shape exponent):** default 2 (logistic); decrease toward 1 for Gompertz-like asymmetric growth; increase for faster early acceleration.
- **K (carrying capacity):** normalised to 1.0 for unit testing; rescale to any real-world capacity limit.
- **P0 (initial fraction):** population seeded as a fraction of K, enabling sensitivity runs from different starting points.
- **g* (max growth rate):** set to 1 so time is already in natural units; adjust to match observed doubling time.
- **Time unit:** Day (easily changed to Month/Year for longer horizons).

## KPIs instrumented
- Population level over time (stock trajectory)
- Net birth rate flow (instantaneous growth speed)
- Implied inflection point (when growth rate peaks, determined analytically by m and K)

## Reusable idea
The transferable trick is the **single-parameter shape switch**: by exposing the exponent m as a slider you turn one model into a family of S-curves (logistic, generalised Richards, near-Gompertz) without changing any other equation. This lets you fit the model to real adoption or growth data by tuning m alone, making it ideal for product-adoption forecasting, epidemic spread calibration, or any capacity-constrained growth scenario where the symmetric logistic assumption is too rigid.
