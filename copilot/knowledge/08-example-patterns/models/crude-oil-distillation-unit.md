# Pattern card — Crude Oil Distillation Unit
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid)
- **Problem it solves:** Models a petroleum refinery's first-stage distillation loop where crude oil arrives by train, is split into product fractions (fuel oil, diesel oil, gasoline), buffered in storage tanks, and exported by dedicated product trains — capturing both continuous fluid flow and discrete train scheduling simultaneously.

## Block chain
Crude oil railcars arrive and unload into a central crude oil storage tank. A pipeline feeds the distillation unit, represented as a FluidSplit that divides the incoming stream into three product fractions at fixed ratios. Each fraction travels through a FluidConvert block (unit transformation) and a Pipeline into its dedicated storage tank (fuelOilTank, dieselOilTank, gasolineTank). On the discrete side, three separate train agents (one per product type) cycle between the refinery and export destinations: a FluidPickup block loads product from the relevant tank into the train's tank cars, a TrainMoveTo block moves the train to the export point, and Seize/Release blocks manage access to shared rail infrastructure. The crude supply side mirrors this with railcars delivering to the crude tank. Alerts fire when the crude tank runs critically low or critically high, signalling operational imbalance.

## Resources
- Three dedicated export trains (one per product: fuel oil, diesel oil, gasoline)
- Crude oil supply trains (number of tank cars configurable via slider, default 8, range 4–12)
- Shared rail resource pool governing single-track access (Seize/Release pattern)
- Four StorageTank objects: crudeOilTank, fuelOilTank, dieselOilTank, gasolineTank
- Tank car capacity configurable at runtime

## Key settings worth copying
- **Time unit:** Hour
- **Product enum:** CrudeOil, FuelOil, DieselOil, Gasoline (typed enum drives routing logic)
- **Split ratios:** Fixed fractions in FluidSplit (no stochastic variation — deterministic chemistry)
- **Car count slider:** numberOfCarsCrude and numberOfCarsFuel (4–12 cars) — lets users explore throughput sensitivity without recompiling
- **Tank alert thresholds:** crudeOilTank.amount() > 5500 triggers overflow warning; < 500 triggers shortage warning — good practice for operational dashboards
- **productionInterruptions counter:** incremented whenever distillation must pause due to supply or capacity constraints

## KPIs instrumented
- Volume passed through each product tank since last export: fuelOilTank.amountPassedIn(), dieselOilTank.amountPassedIn(), gasolineTank.amountPassedIn() (delta tracked against snapshot variables fuelOilPassed, dieselOilPassed, gasolinePassed)
- Real-time tank levels displayed as time-series chart (all four tanks on one plot)
- Production interruption count (discrete event counter)
- 3D animated view of the entire facility as default startup view

## Reusable idea
Mix a continuous Fluid Library network (FluidSplit → Pipeline → Tank) with a discrete-event train scheduling loop (Seize → FluidPickup → TrainMoveTo → Release) in the same model to capture both the steady-state flow physics and the bursty, capacity-constrained logistics of bulk material export — the two paradigms share tank-level state as the handshake point.
