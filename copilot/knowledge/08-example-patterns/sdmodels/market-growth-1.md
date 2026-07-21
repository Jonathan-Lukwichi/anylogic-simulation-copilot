# Pattern card — Market Growth 1
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a high-tech firm's market share evolves as delivery delays, sales force size, and production capacity interact in a self-reinforcing growth-and-constraint feedback system.

## Block chain
Three coupled feedback loops drive the model:

1. **Order-backlog-delivery loop** — Orders flow in (determined by sales force × sales effectiveness) and accumulate in a *Backlog* stock. Shipments drain the backlog at a rate constrained by production *Capacity* and capacity utilisation. The ratio backlog/shipments yields the actual *Delivery Delay*.

2. **Perceived-delay → sales-effectiveness loop** — The market perceives delivery delay with a first-order lag. When perceived delay exceeds the competitor norm, *Sales Effectiveness* drops (via a nonlinear lookup table), which reduces new orders — a balancing loop that caps growth.

3. **Revenue → sales-force → orders loop** — Shipped revenue funds a sales budget (with a quarter-year budget lag). The budget drives a *Target Sales Force*; actual *Sales Force* adjusts toward the target through an 18-month hiring/training delay stock. A larger sales force books more orders, closing the reinforcing growth loop.

Capacity itself is a stock that adjusts toward *Desired Capacity* with an average lag. Desired capacity is anchored on current capacity then modified by *Expansion Pressure*, which is a nonlinear function of the ratio of perceived delivery delay to the delivery-delay goal.

## Resources
- **Production Capacity** stock — initial value 500 units/month; adjusts via a symmetric expansion/contraction flow.
- **Sales Force** stock — grows/shrinks through a net-hiring flow.
- **Backlog** stock — initial value 1 unit (near zero, representing startup).
- **Recent Revenue** stock — first-order smoothed revenue used for budgeting.

## Key settings worth copying
- Time unit: **Day** (converted from a Vensim month-based original).
- Capacity utilisation saturates at **25 % above normal** (nonlinear lookup).
- Sales-effectiveness lookup maps delivery-delay ratio to a 0–1 attractiveness factor.
- Perceived delivery delay uses **first-order smoothing** separately for the company (internal perception lag) and the market (customer perception lag).
- Budget lag: **one quarter-year**; sales-force adjustment lag: **18 months**; capacity adjustment lag: configurable (symmetric for both expansion and contraction).
- Sales cost: **\$8,000 per sales rep per month**; average product price assumed constant.
- Normal order rate per rep set at a baseline "sales effectiveness = 1" value for easy sensitivity testing.
- Switch variables (0/1) allow toggling each feedback loop off independently for partial-model testing (orders exogenous, delivery delay exogenous, expansion pressure exogenous, shipments exogenous).

## KPIs instrumented
- **Book-to-bill ratio** (orders / shipments) — common high-tech health indicator.
- **Delivery delay** (actual and perceived by market and company).
- **Capacity utilisation** (desired production / capacity).
- **Revenue** (recognised at shipment).
- **Sales force size** and **sales budget**.
- **Backlog** level over time.

## Reusable idea
Use **parallel perception lags** (one for the internal company view, one for the external market view) on the same underlying variable — here delivery delay — to capture the realistic gap between what a firm believes its lead time is and what customers actually experience, producing more nuanced oscillation than a single smoothing stock would.
