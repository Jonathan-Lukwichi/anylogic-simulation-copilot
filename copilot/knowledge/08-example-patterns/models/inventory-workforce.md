# Pattern card — Inventory Workforce
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Shows how inventory replenishment policy and labor hiring/firing dynamics interact, producing oscillation and delay that neither sector alone would generate.

## Block chain
Two coupled System Dynamics sectors run in parallel and feed each other.

**Inventory sector** — Customer orders arrive at a rate that can be set to a sporadic step or driven manually. A smoothed exponential average of that rate forms the Expected Order Rate, which drives Desired Production. The gap between Desired Inventory (= Desired_Inventory_Coverage * Expected_Order_Rate) and actual Inventory generates a Production Adjustment that is added to the desired production start rate. Production starts flow into a WIP stock and exit after a third-order delay equal to Manufacturing_Cycle_Time. Finished goods leave as Shipments scaled by an Order Fulfillment Ratio read from a lookup table that compares maximum possible shipment rate to desired shipment rate — the table creates a nonlinear capacity constraint.

**Workforce sector** — Desired Labor is back-calculated from the Desired Production Start Rate divided by Productivity times the Standard Workweek. The gap between Desired Labor and actual Labor, divided by Labor_Adjustment_Time, produces an Adjustment for Labor. Desired Hiring Rate = Expected Attrition Rate + Adjustment for Labor. A Vacancy stock accumulates open positions; actual Hiring Rate fills vacancies after an Average Time to Fill Vacancies delay. Quit Rate drains Labor continuously (proportional to Average Duration of Employment). Layoffs are gated by a Willingness_to_Lay_Off parameter so management reluctance can be modeled. A toggle switch (Switch_for_Labor_in_Production) lets the user choose whether production capacity is labor-constrained or simply driven by the desired production formula — useful for sensitivity experiments.

## Resources
- **Labor** stock (workers) — initial value = Desired_Labor
- **Vacancies** stock (open positions)
- **Work_in_Process_Inventory** stock — initial value = Desired_WIP
- **Inventory** (finished goods) stock — initial value = Desired_Inventory
- **Expected_Order_Rate** stock (information smoothing)

No DES resource pools; all capacity is represented as continuous SD stocks.

## Key settings worth copying
- `Manufacturing_Cycle_Time` — third-order production delay (delay3 function); governs WIP build-up
- `Time_to_Average_Order_Rate` — exponential smoothing constant for demand signal
- `Inventory_Adjustment_Time` / `WIP_Adjustment_Time` — separate time constants for inventory gap correction vs. WIP gap correction
- `Labor_Adjustment_Time` — how quickly the firm tries to close the labor gap
- `Average_Time_to_Fill_Vacancies` — hiring pipeline delay
- `Average_Duration_of_Employment` — drives steady-state quit rate
- `Safety_Stock_Coverage` — added buffer weeks on top of Minimum Order Processing Time
- `Willingness_to_Lay_Off` (0–1) — scales the layoff rate; set to 0 to model no-layoff policy
- `Switch_for_Labor_in_Production` (0/1) — toggles between labor-constrained and unconstrained production
- Order fulfillment table — nonlinear lookup mapping supply/demand ratio to actual shipment fraction
- Time unit: Day

## KPIs instrumented
- Inventory level and coverage (days of supply)
- Shipment Rate vs. Customer Order Rate (service level gap)
- Work-in-Process Inventory vs. Desired WIP
- Labor vs. Desired Labor
- Hiring Rate and Layoff Rate over time
- Vacancies outstanding
- Order Fulfillment Ratio (0–1)

## Reusable idea
Separate the demand signal from the production signal with an exponential smoother (Expected_Order_Rate stock), then use that smoothed signal — not raw orders — to drive both inventory targets and labor targets. This single architectural choice reproduces the classic bullwhip / workforce-oscillation dynamic: any noise in customer orders gets amplified into large swings in hiring and inventory because both sectors react to the same lagged, imperfect information.
