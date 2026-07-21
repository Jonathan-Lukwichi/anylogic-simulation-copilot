# Pattern card — Widgets w Backlog
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models a manufacturing firm's order-fulfillment pipeline where a backlog of customer orders drives production scheduling, revealing how inventory policies create oscillation and delay.

## Block chain
Customer orders flow into a **Backlog** stock. Shipments drain the backlog at a rate limited by available finished-goods **Inventory**. A **Demand Forecast** (exponential smoothing) feeds the **Desired Production** calculation, which targets a level adjusted for inventory gaps and WIP gaps. **Production Starts** enter a third-order delay pipeline that accumulates **WIP Inventory**, eventually completing as production output that replenishes finished goods inventory. Shipments are capped by a feasibility check: if inventory coverage falls short, an order-fulfillment fraction scales down actual shipments below desired shipments.

Key auxiliary chain:
- Average Delivery Delay = Backlog / Shipment Rate
- Desired Shipment Rate = f(Backlog, Target Delivery Time)
- Fraction Filled = min(1, Normal Shipment Rate / Desired Shipment Rate)
- Desired Production = Demand Forecast + Inventory Adjustment + WIP Adjustment

## Resources
- **Stocks:** Backlog, Finished Goods Inventory, WIP Inventory, Demand Forecast, Pink Noise
- **Capacities:** No discrete resource pools; capacity is implicit through inventory availability ratios
- **Time unit:** Week

## Key settings worth copying
- **Demand forecast:** First-order exponential smoothing with an adjustable time constant (demand forecast adjustment time in weeks)
- **Production delay:** Third-order pipeline delay with a configurable average production delay (weeks), approximating Erlang-3 shape
- **Inventory targets:** Desired coverage = normal order processing time + safety stock coverage (weeks of expected orders)
- **Adjustment times:** Separate time constants for inventory adjustment and WIP adjustment allow independent tuning of bullwhip sensitivity
- **Test input modes:** Switchable exogenous demand — step, pulse, ramp, sine wave, and pink noise (first-order autocorrelated noise with configurable standard deviation and correlation time) — all driven from a single `Input` dimensionless multiplier applied to the initial order rate (10,000 widgets/week)
- **White noise sampling:** `uniform()` drawn once per time step via a timed event, fed into the pink noise differential equation

## KPIs instrumented
- Backlog level over time
- Finished goods inventory level
- Shipment rate vs desired shipment rate
- Average delivery delay
- Fraction of orders filled (service level)
- WIP inventory level
- Production start rate vs desired production rate

## Reusable idea
The key transferable trick is the **order-fulfillment fraction** feedback: rather than hard-blocking shipments when inventory is low, the model computes a smooth ratio (feasible rate / desired rate) and multiplies it into the actual shipment flow. This soft constraint prevents algebraic loops while realistically capturing service-level degradation — a pattern directly reusable in any SD supply chain or service capacity model where output is constrained by a finite stock rather than by a hard switch.
