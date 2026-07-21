# Pattern card — Widgets
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models a manufacturing supply chain's inventory oscillation and production instability when a firm responds to customer demand with delayed production and inventory-gap correction policies.

## Block chain
Customer orders arrive exogenously (step, pulse, sine, or uniform-noise test inputs) as `CustomerOrderRate`. The firm forecasts demand via a first-order smoothing stock (`ExpectedOrderRate`). It then computes a `DesiredProduction` target by correcting for the gap between actual `Inventory` and `DesiredInventory` (coverage-based target) over an `InventoryAdjustmentTime`. A separate WIP correction loop adjusts `ProductionStartRate` upward or downward to bring `WorkInProcessInventory` in line with `DesiredWIP` over a `WIPAdjustmentTime`. Actual `ProductionRate` is a third-order delay of `ProductionStartRate` with lag `ManufacturingCycleTime`. Finished goods flow into `Inventory`; shipments drain it at `ShipmentRate`, which is capped by `MaximumShipmentRate` (inventory divided by minimum order-processing time). A lookup table (`TableForOrderFulfillment`) translates the ratio of maximum to desired shipment rate into the fraction of orders actually fulfilled.

## Resources
No agent pools or queues. The three stock variables serve as the accumulator resources:
- `Inventory` — finished-goods stock (units: widgets)
- `WorkInProcessInventory` — WIP stock (widgets)
- `ExpectedOrderRate` — smoothed demand forecast stock (widgets/week)

## Key settings worth copying
- **Time unit:** Week
- **Demand test inputs:** step change, pulse, sine wave, `uniform()` white noise — easy swap via a single selector parameter
- **Production delay:** `delay3(ProductionStartRate, ManufacturingCycleTime)` — third-order material delay captures pipeline realism
- **Inventory target formula:** `DesiredInventoryCoverage * ExpectedOrderRate` where `DesiredInventoryCoverage = MinimumOrderProcessingTime + SafetyStockCoverage`
- **Order fulfilment lookup:** non-linear table mapping shipment-ratio to fill-fraction, preventing over-shipment
- **WIP adjustment:** `(DesiredWIP - WorkInProcessInventory) / WIPAdjustmentTime` additive correction to start rate
- **Non-negativity guard:** `max(0, DesiredProductionStartRate)` on the flow

## KPIs instrumented
- Inventory level over time (oscillation amplitude and settling)
- Shipment rate vs. customer order rate (fulfilment gap)
- Production start rate and production rate (pipeline lag)
- Order fulfilment fraction (service level)

## Reusable idea
The transferable trick is the **dual-gap correction architecture**: separate adjustment loops for finished-goods inventory and WIP inventory, each with its own adjustment time constant, feeding additively into the production start rate. This prevents the model from over-correcting through one loop alone and is directly portable to any make-to-stock SD model (food supply chains, spare-parts stocking, healthcare consumables) where both pipeline and shelf-stock need independent buffering.
