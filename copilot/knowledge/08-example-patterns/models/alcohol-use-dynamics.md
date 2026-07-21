# Pattern card — Alcohol Use Dynamics
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Model)
- **Problem it solves:** Simulate long-term population-level alcohol use progression, comparing baseline trends against a public-health intervention, and quantifying the cost and life-expectancy impact of each pathway.

## Block chain
Each simulated person (agent type `PersonWithAlcoholUsage`) moves through a lifecycle that begins at birth and ends at death. At model start, agents are seeded from a database (one agent per record) so the population reflects a realistic age distribution. Over simulated years, each agent may transition through three behavioural states — non-drinker, drinker, and quitter — plus an absorbing death state. Transition timings are not fixed constants; instead they are drawn from empirical distributions built by converting age-specific rate tables (given in percentages) into proper probability density functions via a `rateToDistribution` helper. Two parallel populations are maintained side-by-side: a control cohort that uses the baseline initiation/quit rates, and an intervened cohort that uses modified (policy-shifted) rates for initiation and quitting. Agents in both cohorts are placed on a 2-D canvas with `uniform(250)` scatter so they are spatially visible but location has no causal role. A Kaplan-Meier plot tracks survival curves for each cohort, and population pyramids visualise the age-sex structure over time.

## Resources
- Two agent populations (control and intervened), each initialised from the same database table
- No shared resource pools or queues — all dynamics are individual agent state machines
- Bidirectional agent-link collection records social connections (2 connections per agent)

## Key settings worth copying
- **Time unit:** Year (long-horizon demographic simulation)
- **Rate tables:** `AlcoholInitiationRate`, `AlcoholAddictionRate`, `AlcoholQuitRate`, `DeathRate` — all age-dependent, stored as argument/value arrays in %
- **Intervened variants:** `AlcoholInitiationIntervenedRate`, `AlcoholQuitIntervenedRate` — same structure, different values to represent a policy scenario
- **`rateToDistribution` trick:** converts a % rate-vs-age table into an empirical time-to-event distribution, accounting for survival probability (`probNotBefore`) at each age bin; death rate under addiction is scaled by a multiplier capped at 100 %
- **Spatial scatter:** `uniform(250)` for x/y placement — purely visual, zero runtime cost
- **Database initialisation mode:** `ONE_AGENT_PER_DATABASE_RECORD` for realistic cohort seeding

## KPIs instrumented
- **Annual cost per agent** (`AnnualCost()` method; `AnnualCostOfQuitter` parameter)
- **Life expectancy impact** — parameters `ImpactOfAddictionOnLifeExpectancy` and `ImpactOfQuitOnLifeExpectancy`
- **Survival curves** — Kaplan-Meier plot comparing control vs. intervened cohorts
- **Population structure** — two PopulationPyramid charts (one per cohort) showing age-sex composition over time
- **Quitter prevalence** — `person.inState(person.Quitter)` queried in chart datasets

## Reusable idea
Convert any age-specific hazard/rate table (given in %) into a proper empirical time-to-event distribution with the `rateToDistribution` pattern: iterate age bins, compute survival probability up to that bin, multiply by the bin rate, and build a PDF table. This lets you drive agent lifecycle transitions directly from published epidemiological tables without needing to fit a parametric distribution.
