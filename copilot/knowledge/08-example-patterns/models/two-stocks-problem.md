# Pattern card — Two Stocks Problem
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Quantifies whether inserting a regional distribution warehouse between a port stock and end clients lowers total supply-chain cost compared to direct long-haul delivery to each client site.

## Block chain
Two parallel supply chains are simulated side-by-side:

**Scenario 1 — direct delivery:** Client orders arrive via a cyclic rate trigger (inter-arrival time drawn from `triangular(minOrders, meanOrders, maxOrders)` days). Each batch of orders is consolidated and fulfilled directly from a single port stock. When the port stock level drops below an alarm threshold, a replenishment order is placed and arrives after `portStockReplenishmentTime` days. Trucks of capacity `longTripTruckCapacity` are dispatched; each trip costs `longTripCost`.

**Scenario 2 — warehouse hub:** Orders are still generated the same way, but fulfillment draws first from a nearby regional warehouse stock (`wVStock`). The warehouse is itself replenished from a second port stock via long-haul trucks; clients are served from the warehouse via short-haul trucks (`shortTripTruckCapacity`, `shortTripCost`). Each stock independently monitors its alarm level and triggers replenishment via a timeout event (`stockReplenishment` timer restarted to the appropriate lead time).

Order quantities per day are also triangularly distributed (`minOrdersPerDay`, `meanOrdersPerDay`, `maxOrdersPerDay`), and individual client delivery deadlines are set as `uniform_discr(1, 7)` days from order time.

## Resources
- Three inventory stocks: `portStock1` (scenario 1), `portStock2` + `wVStock` (scenario 2)
- Each stock defined by: capacity, initial fill, alarm level (fraction of capacity), and a boolean `waitingReplenishment` flag
- Truck fleets implicitly modeled via cost-per-trip calculations; no explicit vehicle agents

## Key settings worth copying
- `triangular(min, mean, max)` for both inter-order intervals and order quantities — easy to calibrate from historical data
- `uniform_discr(1, 7)` for client delivery deadline variability
- Alarm-level replenishment pattern: when `stock.quantity < stock.capacity * alarmLevel`, set `waitingReplenishment = true`, compute `replenishmentOrder = capacity - quantity`, and restart a timeout equal to the lead time
- `ceil(quantity / truckCapacity) * tripCost` to translate demand into discrete truck dispatches and transport cost
- Running mean tracked via a `StatisticsDiscrete` object (`portStock1QuantityStats.mean()`) to compute average inventory holding cost

## KPIs instrumented
- **Global expenditures (scenario 1):** `(time(YEAR)+1) * (portStock1Rent + avgStock1 * relatedCostPricePerTonne * interestRate) + transport costs`
- **Global expenditures (scenario 2):** same formula extended over both port and warehouse stocks plus the initial warehouse fill transport cost
- **Cost per tonne delivered** displayed for each scenario
- **Average stock utilization** (mean quantity in each stock) tracked continuously
- Dashboard shows side-by-side cost comparison updated in real time

## Reusable idea
The key transferable trick is the **alarm-level reorder point with a one-shot timeout for lead time**: rather than a continuous-review loop, a single boolean flag (`waitingReplenishment`) prevents duplicate orders, and a named timeout event fires exactly once after the lead-time duration to replenish the stock to capacity. This pattern cleanly models (s, S) inventory policies in AnyLogic without needing dedicated inventory library blocks.
