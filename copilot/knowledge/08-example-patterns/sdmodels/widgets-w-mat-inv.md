# Pattern card — Widgets w Mat Inv
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models a widget manufacturing supply chain showing how finished-goods inventory, work-in-process, order backlog, and raw-materials inventory interact and create oscillations under various demand patterns.

## Block chain
Customer orders feed an **order backlog** stock. A **shipment rate** flow drains the backlog at a rate constrained by available finished-goods inventory. **Finished inventory** is replenished by a **production completion** flow (third-order delay of production starts). **Production starts** are driven by a desired production rate, itself adjusted for WIP gaps and inventory gaps relative to a demand forecast. On the supply side, a **raw-materials inventory** stock is filled by a **material delivery** flow and drained by a **material usage** flow; actual usage can fall below desired usage when materials are short, throttling production starts. A **demand forecast** stock uses exponential smoothing to track the incoming order rate. Pink-noise and step/pulse/ramp/sine input modes drive the customer order rate for stress-testing.

## Resources
- No agent populations or resource pools (pure SD)
- Key stocks: MaterialsInventory, WIP, FinishedInventory, Backlog, DemandForecast, PinkNoise
- Capacities expressed as coverage targets (weeks of demand) and adjustment time constants

## Key settings worth copying
- **Time unit:** Week
- **Demand test inputs:** step, pulse, ramp, sine (period ~50 weeks), and pink noise — switchable via a single dimensionless `Input` variable
- **Pink noise:** first-order autocorrelated noise built from `uniform()` white-noise samples captured at each time step via a timed event; standard deviation and correlation time constant are parameters
- **Inventory coverage targets:** safety-stock coverage + normal order-processing time = desired inventory coverage; same pattern repeated for materials
- **Shipment and usage ratios:** actual rate = desired rate × (feasible rate / desired rate), clamped to avoid negatives — clean way to model resource scarcity without conditionals
- **Production delay:** third-order exponential delay (pipeline) of production starts

## KPIs instrumented
- Inventory coverage (weeks)
- Average delivery delay (weeks)
- Fraction of customer orders filled
- Material usage ratio (feasible / desired)
- WIP vs desired WIP gap
- Separate time-series charts for material flow rates and finished-goods flow rates

## Reusable idea
The **ratio-based scarcity throttle** — actual flow = desired flow × min(1, feasible/desired) — is a clean, continuous SD idiom that replaces hard IF-THEN cutoffs. Pair it with an exponential-smoothing forecast stock and coverage-gap inventory adjustment and you get a self-correcting supply chain archetype that can be transplanted into any manufacturing or distribution SD model.
