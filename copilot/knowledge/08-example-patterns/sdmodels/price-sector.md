# Pattern card — Price Sector
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models how commodity prices form dynamically through traders' adaptive expectations and inventory-driven signals, starting from an equilibrium and responding to cost or supply shocks.

## Block chain
A single stock — `Traders_ExpectedPrice` — accumulates via the flow `ChangeInTraders_ExpectedPrice`. That flow is a first-order gap-closing equation: the difference between `IndicatedPrice` (the actual market price floored at variable cost) and the current expected price, divided by `TimeToAdjustTraders_ExpectedPrice` (1 day). The observable `Price` is then computed as an auxiliary by multiplying the expected price by two multiplicative correction factors: `EffectOfInventoryCoverageOnPrice` (a power-law function of relative inventory coverage) and `EffectOfCostsOnPrice` (a linear response to the gap between expected costs and expected price). Exogenous step-function inputs drive `InventoryCoverage` and `ExpectedProductionCosts` to simulate shocks.

## Resources
n/a — pure System Dynamics; no agent populations or resource pools.

## Key settings worth copying
- `InitialPrice = 100` (constant) — sets starting equilibrium for both the stock and expected costs.
- `UnitVariableCost = 60` — a price floor; `MinimumPrice = UnitVariableCost` prevents prices from going below variable cost.
- `ReferenceInventoryCoverage = 0.2` — the normal coverage ratio used to compute relative inventory pressure.
- `SensitivityOfPriceToInventoryCoverage = -1` — negative exponent in `pow(RelativeInventoryCoverage, -1)` so that low coverage raises price and high coverage lowers it.
- `SensitivityOfPriceToCosts = 0.5` — linear multiplier on cost-price gap effect.
- `TimeToAdjustTraders_ExpectedPrice = 1` day — controls lag in belief updating.
- Exogenous shocks use `step()` pulses on inventory coverage and production cost to test the price response at specific times (t=1, t=400, t=700, t=1200 days).
- Model time unit: Day.

## KPIs instrumented
- `Price` (observable output: the commodity price at each time step)
- `Traders_ExpectedPrice` (stock: belief about equilibrium price)
- `EffectOfInventoryCoverageOnPrice` and `EffectOfCostsOnPrice` (decomposing price drivers)

## Reusable idea
The transferable trick is the **multiplicative price formation structure**: instead of a single additive feedback, price is the product of a belief anchor (`Traders_ExpectedPrice`) and two dimensionless multipliers — one for supply/demand pressure (power-law of relative inventory) and one for cost pressure (linear ratio gap). This separates fast market-clearing signals from slower cost-expectation dynamics and makes it easy to disable or re-weight each driver independently. The same pattern applies anywhere a negotiated or market price must respond to multiple simultaneous pressures without ad hoc additive mixing.
