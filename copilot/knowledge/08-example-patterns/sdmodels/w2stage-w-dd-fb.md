# Pattern card — W2Stage w DD FB
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models a two-stage supply chain (manufacturer + supplier) with delivery-delay perception and demand-forecast feedback to explain why order oscillations amplify upstream (bullwhip effect).

## Block chain
Customer orders enter as an exogenous demand signal (with optional white-noise or pink-noise perturbation). The manufacturer stage accumulates a Backlog stock, drains it via a shipment rate capped by available Inventory, and replenishes Inventory by completing Work-In-Process (WIP). Production starts are driven by a desired production rate that corrects both finished-goods inventory gaps and WIP gaps relative to targets scaled by the Manufacturing Cycle Time. A parallel materials layer tracks MaterialsInventory and MaterialsOnOrder stocks; the firm orders materials at a rate that covers the desired usage rate plus an adjustment closing the gap between actual and desired materials on order. Perceived supplier delivery delay is smoothed (first-order exponential) with a separate perception time constant, and feeds a lookup table that scales the desired supply line — this is the delivery-delay feedback (DD FB) loop that causes over-ordering when lead times lengthen.

## Resources
- Stocks: Backlog, Inventory, WorkInProcessInventory, ExpectedOrderRate (demand forecast smoother), MaterialsInventory, MaterialsOnOrder, PinkNoise accumulator
- No explicit resource pools; production capacity is implicitly unlimited; shipment rate is constrained by Inventory / MinimumOrderProcessingTime

## Key settings worth copying
- **Time unit:** Week
- **Noise input:** `uniform()` draw held each time step (white noise) or accumulated pink noise stock for correlated demand variation
- **Demand smoothing:** first-order smooth of customer orders over `TimeToAverageOrderRate` weeks → `ExpectedOrderRate`
- **Inventory correction:** `AdjustmentFromInventory = (DesiredInventory - Inventory) / InventoryAdjustmentTime`
- **WIP correction:** `AdjustmentForWIP = (DesiredWIP - WIP) / WIPAdjustmentTime`; DesiredWIP = ManufacturingCycleTime × DesiredProduction
- **Supply-line correction:** `AdjustmentForMaterialsOnOrder = (DesiredMaterialsOnOrder - MaterialsOnOrder) / SupplyLineAdjustmentTime`
- **Delivery-delay perception:** `smooth(DeliveryDelay, MaterialsDeliveryDelayPerceptionTime, ReferenceDeliveryDelay)` then mapped through a nonlinear lookup table to expected delay
- **Safety-stock coverage:** DesiredInventoryCoverage = MinimumOrderProcessingTime + SafetyStockCoverage (additive buffer weeks)
- Converted from Vensim MDL (Sterman textbook model W2STAGEW)

## KPIs instrumented
- DeliveryDelay (Backlog / ShipmentRate) — fulfillment service level
- InventoryCoverage (Inventory / ShipmentRate) — weeks of stock on hand
- MaterialsInventoryCoverage — upstream buffer adequacy
- Order rate oscillation amplitude — implicit comparison between stages to illustrate bullwhip

## Reusable idea
The key transferable trick is the **perceived-delay feedback loop**: rather than reacting to the raw current delivery delay, the ordering policy smooths the delay signal over a perception lag and then passes it through a nonlinear table function to set the desired supply line. This single structure captures how managerial over-reaction to delayed (and noisy) information amplifies swings at every upstream tier — a pattern directly applicable to any multi-echelon inventory or staffing model where decision-makers observe lagged signals and hold safety buffers.
