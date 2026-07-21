# Pattern card — Agent Based Population Model
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Simulate how individual life-stage and employment decisions drive aggregate population and job-market dynamics over decades.

## Block chain
Each simulated person is a `Person` agent whose behaviour is governed by a multi-layer statechart. The outermost layer tracks life stage: **Junior → Adult → Senior → (death)**. Inside the Adult state, two nested sub-charts run concurrently — one for employment status (**Employed / Unemployed**) and one for family formation (**NoFamily → OneKid → TwoKids → ThreeKids**). Transitions fire on age thresholds and on probabilistic timeout events (e.g., a uniform random wait before finding a partner, triangular waits for having successive children). When a female agent in the NoFamily state finds an eligible male neighbour, the two link as spouses and the family sub-chart advances. New child agents are spawned near the mother's coordinates. On death or retirement the agent cleans up its spouse and mother links before being removed from the population.

The job market is handled entirely in **System Dynamics**: two stocks — `Vacancies` and `Employed` — exchange flow driven by agent actions. When an agent enters the Employed state it decrements Vacancies and increments Employed; retirement does the reverse. A SD flow (`JobCreation`) adds new vacancies only when total jobs (Vacancies + Employed) are below the 150-job ceiling, at a rate proportional to the number of unemployed agents (`Unemployed * 0.001`). This couples the micro (agent decisions) directly to the macro (stock levels) without duplication.

Agents are initialised from a database table, each row supplying an `InitialAge` and a `Male` flag. Spatial placement uses `moveTo(uniform(800), uniform(300))` so agents scatter randomly across a 2-D canvas. 3-D shapes (office worker / nurse meshes) are swapped at runtime based on the `Male` flag.

## Resources
- Job market: 150-job capacity ceiling shared across the population (SD stocks: Vacancies + Employed ≤ 150)
- Agent population: size driven by births and deaths; no fixed cap
- Network links per agent: 2 bidirectional connections (spouse link, mother link)

## Key settings worth copying
- **Life-stage durations:** retirement age hardcoded at 50; Junior/Senior boundaries set by age-threshold transitions
- **Family timing:** `uniform(5, 35)` years before seeking a partner; `triangular(2, 4, 6)` years between successive children (used twice for child-2 and child-3 waits); `uniform(3, 5)` for a further family event
- **Spatial scatter on birth:** `uniform(-4, 4)` offset from mother position for child spawn
- **Job-creation flow formula:** `(Vacancies + Employed < 150) ? Unemployed * 0.001 : 0`
- **Agent initialisation:** one-agent-per-database-record mode; `InitialAge` and `Male` loaded from DB
- **Model time unit:** Year

## KPIs instrumented
- Count of agents in each life stage: NJunior, NSenior (stacked time-series chart)
- Count of agents in each employment state: NUnemployed
- Count of agents in each family state: NNoFamily, NOneKid, NTwoKids, NThreeKids
- SD stocks over time: Vacancies, Employed (implicitly tracked via flow accounting)

## Reusable idea
Couple individual agent decisions to aggregate SD stocks by having agents directly increment/decrement stock variables on state entry/exit — this avoids writing separate aggregation logic and keeps the macro model automatically in sync with micro behaviour at zero extra cost.
