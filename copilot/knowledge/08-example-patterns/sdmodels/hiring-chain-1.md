# Pattern card — Hiring Chain 1
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a firm's workforce evolves over time when new hires start as low-productivity rookies and gradually assimilate into the experienced, fully-productive staff pool.

## Block chain
Two stock variables hold the workforce state: **Rookies** (inexperienced new hires) and **Experienced Workers** (fully productive staff). Four flow rates connect them:

1. **Hire rate** — adds rookies to replenish all quits and meet an exogenous fractional growth target for the total labor force.
2. **Assimilation rate** — moves rookies into the experienced pool after they complete a learning period.
3. **Rookie quit rate** — drains rookies at a fixed fractional rate per week.
4. **Experienced quit rate** — drains experienced workers at a separate fractional rate per week.

A set of auxiliary variables computes derived quantities: total employees, fraction of workforce that is inexperienced, average workforce productivity (weighted blend of rookie and experienced productivity), and potential output (total tasks the workforce can complete per week).

## Resources
- No explicit resource pools (SD model, not process-flow).
- Two stock levels act as the "resource reservoirs": Rookies stock (initial equilibrium value) and Experienced Workers stock (initial equilibrium value).
- Capacities are implicitly governed by hire rate balanced against total quit rate.

## Key settings worth copying
- **Time unit:** Week.
- **Rookie productivity:** parameter (default 0 < value < 1 relative to experienced = 1.0).
- **Experienced worker productivity:** set to 1 (normalisation reference).
- **Fraction quitting per week:** separate parameters for rookies and experienced workers.
- **Assimilation time:** average weeks a rookie takes to become experienced (drives the assimilation flow = Rookies / assimilation_time).
- **Exogenous growth rate:** fractional weekly growth in desired total workforce, activated at a configurable start time — useful for testing ramp-up scenarios.
- Model imported from Vensim HIRINGCH1.mdl; direct Vensim-to-AnyLogic conversion pattern is reusable for other legacy SD models.

## KPIs instrumented
- **Average workforce productivity** — weighted average of rookie and experienced productivity, tracks dilution effect during rapid hiring.
- **Potential output** — throughput capacity of the entire workforce at any point in time.
- **Fraction inexperienced** — leading indicator of productivity risk.
- **Total quit rate** — combined drain from both stocks.

## Reusable idea
The key transferable trick is the **two-tier workforce stock** pattern: separating new hires (low productivity) from seasoned staff (full productivity) with an assimilation flow between them. This captures the hidden productivity cost of rapid hiring — even if headcount grows, average output per person falls until rookies assimilate. Plug this pattern into any model where resource capability ramps up over time (e.g., new machines during break-in, software onboarding, training pipelines).
