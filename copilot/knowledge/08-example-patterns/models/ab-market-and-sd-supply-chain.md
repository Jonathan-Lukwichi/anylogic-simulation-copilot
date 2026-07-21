# Pattern card — AB Market and SD Supply Chain
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Shows how individual consumer brand-switching behaviour (ABM) drives aggregate demand that feeds directly into competing supply chains (SD stocks and flows).

## Block chain
Two parallel supply chains — one for Brand A, one for Brand B — are each modelled as a classic SD inventory loop: a FactoryStock drains through a Delivery flow at rate `FactoryStock / DeliveryTime`, while a Production flow refills it in response to a demand forecast. Retailer stocks sit downstream and are decremented whenever a consumer actually purchases.

On the demand side, a population of Consumer agents each carry a statechart with states representing brand preference (UsesA, UsesB, plus intermediate consideration/switching states). Transition triggers are a mix of rate-based spontaneous switching and condition-based switching that checks retailer stock availability before decrementing. When stock is zero the consumer cannot switch, creating a natural stock-out feedback.

The two layers are coupled at two points: (1) the ABM counts `NUseA()` and `NUseB()` which drive the SD forecast variables `ForecastA`/`ForecastB`, and (2) consumer purchase transitions directly decrement `RetailerStockA`/`RetailerStockB` SD variables. The result is a closed loop where aggregate market share emerges from micro decisions and then steers factory production.

## Resources
- Consumer agent population (size set via database or parameter)
- Two factory stocks (FactoryStockA, FactoryStockB) — continuous SD level variables
- Two retailer stocks (RetailerStockA, RetailerStockB) — continuous SD level variables
- Each factory has Production and Delivery flow variables

## Key settings worth copying
- Time unit: **Day**
- Delivery flow formula: `FactoryStock / DeliveryTime` (first-order pipeline)
- Consumer brand-loyalty timeout drawn from `uniform(17, 23)` days before reconsideration
- Purchase transition guard: `main.RetailerStock >= 1` — prevents negative inventory
- Network links between consumers: `ConnectionsPerAgent = 2` (sparse word-of-mouth graph)
- SD forecasts wired to ABM counts: `ForecastA = consumers.NUseA()` pattern

## KPIs instrumented
- Market share over time: `consumers.NUseA()` vs `consumers.NUseB()` plotted as demand series
- Demand for A, B, and either (three separate dataset series)
- Implicit: factory and retailer stock levels (tracked by SD variables, visible in stock charts)

## Reusable idea
The transferable trick is the **count-to-flow coupling**: read an ABM population count each time step and feed it directly into an SD flow formula (forecast → production). This one-liner bridge lets you keep micro-level heterogeneity in consumer behaviour while the supply network stays computationally cheap as a continuous SD model — ideal whenever demand is stochastic and individual-driven but supply is aggregate and volume-based.
