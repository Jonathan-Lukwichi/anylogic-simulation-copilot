# Pattern card — Price Discovery
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a market price converges toward equilibrium when market makers respond to demand/supply imbalances without knowing the underlying curves — converted from a classic Vensim reference model.

## Block chain
The model is built entirely from SD stocks, flows, and auxiliary variables — no DES process blocks. A single stock holds the current **Price**, which adjusts toward an **Indicated Price** over a **Price Adjustment Time** (first-order smoothing). The Indicated Price is calculated by market makers who observe the ratio of Demand to Supply and apply a power-function sensitivity: when demand exceeds supply the signal pushes price up; when supply exceeds demand it pushes price down. Demand itself follows a constant-elasticity curve anchored to a Reference Demand at a Reference Price; Supply follows an analogous constant-elasticity curve. A step shift in the demand curve (triggered at a user-set time) creates the imbalance that the price-discovery loop must correct.

## Resources
n/a — pure equation-based SD model; no agent pools or resource pools.

## Key settings worth copying
- **Price Adjustment Time** (days): governs the lag between a price signal and actual price movement — increasing this slows convergence and can produce oscillation.
- **Demand/Supply elasticity exponents**: constant-elasticity formulas `Demand = RefDemand * (Price/RefPrice)^(-elasticity)`; separate exponents for demand-side and supply-side.
- **Price sensitivity to imbalance**: a power-function multiplier on the D/S ratio; higher sensitivity produces faster but potentially overshooting price responses.
- **Demand shift magnitude and timing**: a fractional step change applied to Reference Demand at a specified day — the main perturbation used to test market responsiveness.
- **Time unit:** Day; typical run horizon is tens to hundreds of days to observe convergence.

## KPIs instrumented
- **Price trajectory over time** — does it converge smoothly, overshoot, or oscillate?
- **Demand vs. Supply gap** — tracks the imbalance ratio driving the price signal.
- **Indicated Price vs. Actual Price** — reveals the lag introduced by Price Adjustment Time.

## Reusable idea
The transferable trick is the **first-order price-smoothing loop**: rather than snapping price instantly to the market-clearing level, pass the indicated price through a stock with a configurable adjustment delay. This single pattern reproduces realistic gradual price discovery, overshoot, and oscillation behaviour simply by tuning one time constant — applicable to any market, inventory, or capacity adjustment model where decision makers act on signals with a lag.
