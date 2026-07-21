# Pattern card — Commodity1
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how commodity markets self-regulate through interacting feedback loops linking inventory, price expectations, capacity investment, and demand.

## Block chain
The model is a pure SD structure built from stocks (levels), flows (rates), and auxiliary variables.

Key stocks:
- **Inventory** — finished goods held by producers; fed by production completions and drained by shipments to satisfy demand.
- **CapitalStock** — productive capacity in service; grows via AcquisitionRate (a third-order delay on orders) and shrinks via DiscardRate (lifetime depreciation).
- **CapitalOnOrder** — supply line of capacity under construction, bridging OrderRate and AcquisitionRate.
- **PinkNoise / PinkNoise0** — smoothed white-noise stocks used to inject correlated random demand or cost shocks.

Key flows:
- **ProductionStartRate** = ProductionCapacity × CapacityUtilization — actual output entering the pipeline.
- **AcquisitionRate** = delay3(OrderRate, CapacityAcquisitionDelay) — new capacity arriving after a third-order construction lag.
- **DiscardRate** = CapitalStock / AverageLifeOfCapacity — retirement of worn-out capacity.
- **OrderRate** = max(0, IndicatedOrders) — investment orders, clamped non-negative.

Price is set by an auxiliary formula combining traders' expected price, an inventory-coverage effect, and a cost effect. Both short-run and long-run price expectations are formed by first-order exponential smoothing (smooth()). Demand responds to price via a linear demand curve with elasticity, also smoothed over a DemandAdjustmentDelay. Capacity utilization is a nonlinear lookup of the expected markup ratio (ShortRunExpectedPrice / ExpectedVariableCosts) and adjusts with its own delay.

## Resources
No agent populations or DES resource pools. The equivalent "capacity" concept is modelled as the continuous stock CapitalStock (units of capital, each able to produce one unit of output per year at normal utilization). CapacityUtilization (0–1+) acts as the throttle on actual output.

## Key settings worth copying
- **Time unit:** Day.
- **Third-order capacity acquisition delay:** `delay3(OrderRate, CapacityAcquisitionDelay)` — creates realistic S-shaped delivery lags without a pipeline stock array.
- **Adaptive expectations (smooth):** `smooth(Price, TimeToAdjustLongRunPriceExpectations, initialValue)` — standard first-order lag for belief updating; used for both long-run and short-run price expectations and for perceived inventory coverage.
- **Pink noise generation:** white noise via `uniform(0,1,seed)` fed through a first-order smoothing stock — produces autocorrelated random shocks useful for stress-testing without structured scenarios.
- **Non-negative order clamp:** `max(0, IndicatedOrders)` and `max(0, DesiredAcquisitionRate + AdjustmentForSupplyLine)` — prevents the model from placing negative orders during downturns.
- **Supply-line anchoring:** desired supply line = ExpectedAcquisitionDelay × DesiredAcquisitionRate, and actual CapitalOnOrder is pulled toward that target over SupplyLineAdjustmentTime.
- **Exogenous test inputs:** an Input auxiliary can switch between step, pulse, sine-wave, and pink-noise patterns for scenario testing without changing model structure.

## KPIs instrumented
- **Price** (endogenous market-clearing price driven by expectations and inventory coverage)
- **InventoryCoverage** (days of inventory on hand relative to reference level)
- **CapacityUtilization** (fraction of installed capacity actually running)
- **ProductionCapacity** (total potential output)
- **IndustryDemand** (units demanded per period)
- No explicit cost or profit P&L stock, but ExpectedProfitFromNewInvestment and ExpectedMarkupRatio serve as profitability proxies.

## Reusable idea
The transferable trick is the **supply-line correction heuristic**: producers track both the gap between desired and actual capital stock AND the gap between the required and actual pipeline of orders under construction, then add both adjustments to the base replacement order. This prevents the classic "ordering surge then collapse" oscillation by making decision-makers explicitly account for what is already on order — a pattern directly applicable to any SD model with delayed capacity acquisition (e.g., hospital bed planning, fleet expansion, IT infrastructure scaling).
