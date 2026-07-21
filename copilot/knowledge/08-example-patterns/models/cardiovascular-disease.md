# Pattern card — Cardiovascular Disease
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Model)
- **Problem it solves:** Simulate long-run cardiovascular health outcomes and accumulated third-party costs across a patient population, where individual risk factors drive heterogeneous event histories.

## Block chain
A cohort of 1 000 Patient agents is created at time zero, each starting at age 0. The simulation runs for 100 years (model time unit = Year). Each year, every living patient independently rolls three probabilistic checks in sequence: death, myocardial infarction (MI), and stroke. None of these checks uses a DES queue or service block; instead a cyclic yearly timeout fires on each agent, which then executes the probability logic directly in code. Death removes the agent; MI and stroke set Boolean flags on the patient that persist and compound future risk. The agent population is embedded in a network space (100 × 100 grid, ~2 connections per agent, neighbor-link fraction 0.95) though connectivity is primarily structural rather than transmission-based in this model.

## Resources
- No explicit service resources or capacity pools.
- Agent population: 1 000 Patient agents, all spawned at model start.
- Network: small-world-style grid topology (100 × 100, M = 10 connections per agent).

## Key settings worth copying
- **BMI distribution:** `triangular(15, 25, 40)` — assigned once per agent at creation; drives both MI and stroke annual probability multipliers (`prob * BMI / 20`).
- **Lookup tables:** `DeathProbabilityTable`, `MIProbabilityTable`, `StrokeProbabilityTable` — age-indexed; Base probability scales linearly with BMI ratio.
- **Event costs (one-time):** Death $200, MI $1 000, Stroke $2 000.
- **Background costs (recurring per year after event):** MI history +$200/yr, Stroke history +$200/yr.
- **Model time unit:** Year — keeps probability tables and age logic simple and readable.
- **Random seed / `randomTrue()`:** AnyLogic built-in Bernoulli draw, no external library needed.

## KPIs instrumented
- **Life expectancy distribution** — histogram of agent death ages, updated live.
- **MI age distribution** — histogram of ages at first MI event.
- **Stroke age distribution** — histogram of ages at first stroke event.
- **Accumulated third-party cost over time** — dataset `associated3rdPartyCostByYears` and running scalar `cost` (aggregated across all agents in Main).

## Reusable idea
Use a per-agent yearly timeout loop with age-indexed probability tables and an individual risk multiplier (here BMI / 20) to model heterogeneous chronic-disease trajectories without any queueing infrastructure — the entire model logic lives in a single annual callback, making it trivial to add new risk factors or event types by extending the multiplier and cost table.
