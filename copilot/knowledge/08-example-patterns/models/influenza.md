# Pattern card — Influenza
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Model)
- **Problem it solves:** Simulates how influenza spreads through a small population as people alternate between home and workplace, capturing household and occupational transmission networks.

## Block chain
Each Person agent carries two statecharts: one for illness progression (Susceptible → Exposed → Infectious → Recovered) and one for daily movement (home → commuting → at work → commuting → home). Infected agents emit "Infection" messages at a contact rate to randomly chosen family members (when at home) or workplace colleagues (when at work). Recipients accept infection with a configurable probability, transitioning from Susceptible to Exposed. Symptomatic individuals stay home, breaking the workplace transmission chain. Family agents group 2–5 Person agents sharing a house; Work agents hold a dynamic list of colleagues currently on-site. The model runs 100 replications in a Monte Carlo experiment to characterise outbreak variability.

## Resources
- **Person agents** — population sized via parameters (families × members)
- **Family agents** — household groups of `uniform_discr(2, 5)` members
- **Work agents** — office locations, number configurable; each maintains a live `colleagues` list
- No queues or resource pools — capacity constraints are implicit (infection probability gate)

## Key settings worth copying
- **Time unit:** Day
- **Contact rate trigger:** `rate` transition on the illness statechart fires at a tunable rate; recipient chosen via `uniform_discr(0, list.size()-1)`
- **Incubation / symptom / recovery durations:** `triangular(1, 1.5, 3)`, `triangular(1, 1.7, 3)`, `triangular(2, 3.5, 5)` days respectively
- **Infection probability:** slider parameter (0–1), checked on message receipt
- **Work assignment:** random from works list — `uniform_discr(0, works.size()-1)`
- **Commute position:** `uniform(110)` / `uniform(40)` offsets inside the work location shape

## KPIs instrumented
- Counts of agents in each disease state (Susceptible, Exposed, Infectious, Recovered) tracked over time
- Outbreak size distribution across 100 Monte Carlo replications
- Effect of infection probability and contact rate on peak infected count (parameter variation experiment)

## Reusable idea
Split agent behaviour into two independent statecharts — one governing location/mobility and one governing disease state — then use message-passing between agents to couple them. This separation keeps each statechart simple and makes it easy to add new disease stages or new locations without rewriting the movement logic. The same pattern applies to any contagion model (rumour spreading, equipment failure cascades) where exposure depends on who is physically co-located at a given moment.
