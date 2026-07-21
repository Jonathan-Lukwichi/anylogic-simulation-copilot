# Pattern card — Wandering Elephants
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Models how a herd of animals degrades a shared landscape resource (vegetation) through random movement and periodic visits to water sources, showing ecosystem feedback between consumers and environment.

## Block chain
Each Elephant agent runs a two-state statechart: **FreeWandering** and **ThirstyHeadingToWater**. While free-wandering the agent fires a periodic `NewDir` self-loop transition (every 12 hours) that calls `headingRandom()`, picking a uniformly random compass heading and issuing a long-range `moveTo()`. An `AfterStep` callback runs every simulation step: it reads the agent's grid cell, subtracts vegetation if the cell has enough, and detects boundary/water collisions — on collision the elephant resamples a valid heading. After `uniform(0.8, 1.2) * drinkingPeriod` days, the `GotThirsty` timeout fires, sets `thirsty = true`, and calls `headingToWater()` to navigate toward the nearest lake (altitude < 0). When the step code detects the elephant is standing in water, it sends the message `"Drink"` to the statechart; the `DrinkWater` message-triggered transition fires and returns the agent to FreeWandering. The Main agent holds two 100×100 double arrays (`altitude[][]`, `vegetation[][]`) and a vegetation regeneration loop that caps each cell at `maxVegetation[c][r]` derived from altitude.

## Resources
- Agent population: elephants (configurable count, default implied by seed loop)
- Shared grid: 100x100 cells over a 500x500 model-unit continuous space (each cell ~5 units / ~5 km side)
- Lake locations determined by negative altitude values; 30 procedurally generated hill clusters

## Key settings worth copying
- `uniform(0.8, 1.2) * drinkingPeriod` — multiplicative jitter on a base period keeps agents desynchronised
- `uniform(-Math.PI, Math.PI)` for random heading; rejection-sample loop (up to 100 tries) ensures chosen direction is land-only
- `uniform_discr(0, 99)` for hill centre placement; `triangular(-30, 0, 30)` for hill footprint spread
- Time unit: Day; velocity expressed in MPS then scaled by model space
- Moore neighbourhood (8-connected) defined on the environment, used for spatial queries
- `AfterStepCode` pattern: per-step logic embedded directly in agent movement callback rather than a scheduled event — efficient for high-frequency cell interaction

## KPIs instrumented
- Vegetation coverage (sum or mean of `vegetation[][]` over all cells) tracked over time
- Visual layer toggle between altitude map and vegetation density map for qualitative inspection
- No explicit throughput/wait/utilisation KPIs — primary output is spatial vegetation depletion pattern

## Reusable idea
Embed environment-interaction logic in the agent's `AfterStep` callback rather than scheduling discrete events: the agent reads and modifies a shared 2-D array every movement step, giving continuous spatial feedback (grazing, pollution, heat spread) at near-zero overhead — the same trick applies to any model where agents passively affect a GIS raster as they traverse it.
