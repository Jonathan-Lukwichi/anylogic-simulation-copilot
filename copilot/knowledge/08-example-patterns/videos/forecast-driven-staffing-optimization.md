# Pattern card — Forecast in, staffing out: optimise against an output requirement
- **Source:** AnyLogic video "Webinar | How Simulation-Driven Insights Strengthen Strategic Decision-Making" (https://youtu.be/UVppYf_O4H8) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Turn an ML demand forecast into a staffing level the simulation can defend, with "lose no customers" enforced as a hard service promise.

## Mechanism
1. An ML model forecasts arrivals (e.g. customers per hour for the coming week) and exports a table. The forecast is a *scenario input*, not model logic.
2. The model reads the table at startup and drives arrivals from it, so a new forecast means a new file, not a rebuild.
3. An Optimization experiment searches the staffing lever: one flat headcount for the week (the webinar's case), or one per day-part.
4. Objective: maximise throughput or profit. **Requirement:** lost customers = 0 (or at most an agreed tolerance).
5. Compare plans on identical KPIs: the manager's own time-varying roster, a constant level, and the optimiser's plan. This is the concrete form of "baseline vs ML-informed".
6. Stress the winner: rerun it with the forecast's error band and an uncertain channel mix (Monte Carlo 2nd order in Cloud) and check that the requirement still holds.

## Resources
A staff `ResourcePool` sized by the optimised parameter(s), plus a `Schedule` if staffing varies by day-part.

## Key settings worth copying
- **Requirements vs Constraints:**
  - Output limits go in the experiment's **Requirements**. These are tested after each run, and a failing candidate is rejected as infeasible. Example: `root.lostCustomers` ≤ 0.
  - **Constraints** are tested *before* a run and limit parameter combinations. Example: `morningStaff + lunchStaff` ≤ 20.
- For a stochastic model, enable replications in the optimization (a fixed count, or a varying count up to a confidence target) so the search does not chase noise.
- Drive the forecast through **Arrivals defined by: Rate schedule**. See `anylogic-gotchas.md` G5: the rate-field expression under-samples a rising rate.
- Make "lost" measurable:
  - Bound the drive lane or waiting area at its physical size.
  - Count balks (arrival to a full lane) and reneges (queue timeout) into one `lostCustomers` counter.
  - An unbounded queue never loses anyone, so the requirement would be met trivially.
- Keep a switch between schedule-driven and constant staffing (see `models/border-checkpoint-optimization.md`).

## KPIs instrumented
Lost customers (balked + reneged), time in system by channel, staff utilisation, labour cost / profit.

## Pitfalls
- Writing the service promise as a Constraint. Constraints act on parameters before the run and cannot enforce an outcome.
- A requirement judged on a replication mean can hide bad replications. Also report the share of replications with any loss.
- Optimising against the forecast's point estimate tunes the plan to one demand curve.
- A flat level sized for the peak looks wasteful off-peak. Show labour cost next to the day-part schedule.

## Reusable idea
The forecast is an input file, the requirement is the service promise, and the optimiser finds the cheapest plan that keeps the promise.

## When the co-pilot should use this
- Any staffing or capacity question where a demand forecast exists or ML is in scope (INSTRUCTIONS: baseline vs ML-informed vs RL).
- When the success criterion is a guarantee (no lost customers, SLA met) rather than an average.
- When filling the intake card's objective/constraints field: separate the objective, the constraints (parameters) and the requirements (outputs).
