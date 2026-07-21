# Pattern card — Widgets w Labor and OT
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a manufacturing firm balances workforce size and overtime against fluctuating customer demand, tracking inventory and WIP through feedback loops.

## Block chain
Customer orders drive a desired production rate, which is adjusted by WIP and finished-goods inventory gaps. The firm sets a desired labor level based on planned workweek hours and expected productivity. When actual labor falls short, vacancy creation triggers hiring; excess labor triggers layoffs (subject to a willingness-to-layoff policy). The workweek (including overtime) expands or contracts with schedule pressure, acting as a short-run buffer before headcount can adjust. Shipments are capped by available inventory and minimum order-processing time; unfilled orders are lost.

## Resources
- **Labor stock:** workforce headcount; governed by hiring flow (via vacancy pipeline) and quit/layoff outflows
- **Vacancy stock:** open positions; created/cancelled with adjustment delays
- **Work-In-Process (WIP) inventory stock:** units in production pipeline
- **Finished goods inventory stock:** completed widgets awaiting shipment

## Key settings worth copying
- `uniform()` noise applied to customer order rate to simulate real-world demand variability
- Time unit: **Week**
- Standard workweek target with a nonlinear lookup (table function) mapping schedule pressure to actual workweek — captures overtime saturation
- Separate adjustment times for labor (`LaborAdjustmentTime`), vacancies (`VacancyAdjustmentTime`), WIP (`WIPAdjustmentTime`), and inventory (`InventoryAdjustmentTime`) — typically 4–12 weeks each
- `WillingnessToLayoff` switch (0 = no-layoff policy, 1 = full layoff allowed)
- Safety stock coverage added on top of minimum order processing time to set desired inventory coverage
- Demand forecast smoothed over a first-order delay to dampen order noise before it drives production targets

## KPIs instrumented
- Inventory coverage (weeks of demand on hand)
- Fraction of customer orders filled (service level)
- Workweek length (overtime indicator)
- Labor force size vs. desired labor
- WIP vs. desired WIP
- Vacancy count

## Reusable idea
Split the workforce response into two nested loops — a fast loop that stretches or shrinks the workweek (overtime/undertime) and a slow loop that adjusts headcount through hiring and layoffs — so the model naturally reproduces the realistic lag between demand shocks and actual staffing changes without any discrete-event logic.
