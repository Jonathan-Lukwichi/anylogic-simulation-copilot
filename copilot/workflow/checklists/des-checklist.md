# DES build checklist
- [ ] Phase 0 approach confirmed (DES is the right paradigm)
- [ ] Entities, resources, activities, routing identified; hand-offs between libraries listed
- [ ] Distributions fitted with goodness-of-fit reported (empirical Custom Distribution only when no family fits)
- [ ] Decision lever parameterised (variable/schedule, not hard-coded)
- [ ] Repeated block chains refactored into custom blocks (after verification); their per-agent parameters are Dynamic
- [ ] Runtime window, time units and scale set; fixed seed while building, random/per-replication seeds for estimates
- [ ] Source: if Forced pushing is off, *Agents which can't exit* = wait in this block; conservation checked (`source.count()` = exits + WIP)
- [ ] KPIs instrumented and exposed as experiment Outputs
- [ ] Replications show real spread (no constant-seeded custom generator or model-level `new Random(const)`)
- [ ] Sanity check vs theory (utilisation, Little's Law)

## Sim-opt (only if an Optimization experiment is used)
- [ ] Objective and requirement KPIs are functions/statistics on Main, referenced with `root.` (and Output elements if it will run on Cloud)
- [ ] Lever-only limits entered as Constraints; limits on results as Requirements (level-type limits — queue, stock, WIP — on a time-weighted statistic)
- [ ] Finite stop time; replications on (fixed N from a pilot, or OptQuest's varying count with a CI)
- [ ] Engine chosen with its limits in mind (bundled OptQuest ≤ 7 variables / 500 iterations; Genetic 8.8.4+; Cloud = Genetic)
- [ ] No best value sits on a range edge; coarse-to-fine refinement done if the steps were large
- [ ] Top 3–5 plans re-verified with extra replications; result reported as "best found", with a CI

## Cloud deliverable (only if it runs on AnyLogic Cloud)
- [ ] Levers are static top-level parameters of allowed types; input files in the model folder with relative paths
- [ ] Every decision KPI is a scalar `Output` on the top-level agent; comparisons use replicated experiment types
- [ ] Account tier checked (run time, memory, API) before promising delivery
