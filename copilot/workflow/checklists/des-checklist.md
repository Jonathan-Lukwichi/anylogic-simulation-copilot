# DES build checklist
- [ ] Phase 0 approach confirmed (DES is the right paradigm)
- [ ] Entities, resources, activities, routing identified; hand-offs between libraries listed
- [ ] Distributions fitted with goodness-of-fit reported (empirical Custom Distribution only when no family fits)
- [ ] Decision lever parameterised (variable/schedule, not hard-coded)
- [ ] Repeated block chains refactored into custom blocks (after verification); their per-agent parameters are Dynamic
- [ ] Runtime window, time units and scale set; fixed seed while building, random/per-replication seeds for estimates
- [ ] Source: if Forced pushing is off, *Agents which can't exit* = wait in this block; conservation checked (`source.count()` = exits + WIP)
- [ ] No block still runs on a library default (Source 1 per second; Delay and Service `triangular(0.5, 1, 1.5)` s; SelectOutput 0.5); ρ = λ·E[S]/c written down and below 1 for each station
- [ ] Time-varying arrivals use a Rate schedule or an interarrival expression, not a time expression in *Arrival rate*; every `set_…(v)` on a block passes a unit (G5, G61)
- [ ] One time-unit mechanism per field — drop-down or multiplier, not both (G62); calendar pinned: start date set in every experiment, months 0-based (G63–G65)
- [ ] Each SelectOutput's mode matches its intent — a stored condition is ignored in probability mode (G86); routing values are set before the preceding block's On exit (G6)
- [ ] Requests cancelled from a Queue or Delay are disposed of (Enter → Sink `cancelled`) and counted (G88); `stopDelay` never receives null (G87)
- [ ] Every refusal port is wired or shown unreachable (`CarMoveTo.outWayNotFound`, `TrainMoveTo.outHit`, …)
- [ ] KPIs instrumented and exposed as experiment Outputs
- [ ] Replications show real spread (no constant-seeded custom generator or model-level `new Random(const)`)
- [ ] Sanity check vs theory (utilisation, Little's Law)

## Statecharts and events (ABM / hybrid)
- [ ] No guard on a Timeout or Rate transition unless "try once" is meant — test in a Branch with a Default exit instead (G71); branch conditions use a stored copy of `msg` (G72)
- [ ] Every Branch has exactly one Default exit and mutually exclusive conditions
- [ ] A loop that must not reset the state's timers is drawn inside the state; a History resume restarts timeouts (G75)
- [ ] Commands sent as messages use an Option List type; a notice that may arrive before the receiver waits is latched in a variable and read by a Condition (G21)
- [ ] Each event inside an agent type: absolute time (Occurs once, first occurrence) or relative (`time() + N`, User control)? Agents born mid-run depend on it (G73)
- [ ] Each Condition event: who re-arms it (`restart()` after making the condition false, G74)? Is it re-tested when a remote value changes (`onChange()`, synchronous steps, G56)?
- [ ] Continuous thresholds use `>=` / `<=`; rates that depend on time or age have a refresh path (G70)

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
