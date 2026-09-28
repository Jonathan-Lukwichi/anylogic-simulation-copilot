# Pattern card — Sim-opt dual formulations: min cost for a service target vs max service for a budget
- **Source:** AnyLogic video "Webinar | Simulation-Based Optimization in AnyLogic" (https://youtu.be/YyDJDqMqYng) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Posing one cost-vs-service decision two ways in an Optimization experiment, and making its bounds behave.

## Mechanism
`videos/forecast-driven-staffing-optimization.md` defines the two kinds of limit:
- a Constraint limits the levers only and is checked before a run;
- a Requirement limits an output and is checked after the run, on the replication mean.

This card uses that pair to pose a decision and to cross-check it.
- **F1: cheapest plan that meets a target.** Minimise `root.totalCost()` with the requirement `root.serviceLevel() >= 0.9`.
- **F2: best service a budget buys.** Maximise `root.serviceLevel()` with the linear constraint `10*nA + 15*nB + 10*nC + 20*nD <= 240` (cost per machine in k$).
- **Webinar job shop:** machines per work centre A–D, 1..6 in steps of 1 (model in `videos/dispatching-rule-as-optimizable-policy.md`).
  - F1: rule fixed to EDD, 50 replications, 500 iterations. Result (5,3,4,5) at cost 235, service just above 90 %. No gain after about iteration 180.
  - F2: rule also free (1..4), Automatic stop on. Result (4,4,4,5) at cost exactly 240, so the budget binds; service about 93 %. Stopped near iteration 300.
- **Reading the pair:** F1 tells you what the service target costs; F2 tells you what the budget buys.
  - Rerun either one with a few bounds (service 85/90/95 %, or budgets 220/240/260) to get the cost–service trade-off curve. This is an ε-constraint sweep.
  - A scatter chart of service vs cost over all iterations shows the same frontier while the search runs.
- `totalCost`, `serviceLevel` and `nA`…`nD` are illustrative names: KPI functions on Main, reached through `root`.

## Resources
n/a (method)

## Key settings worth copying
- **Requirement row:** Expression / Type (`>=`, `<=`, `=`) / Bound.
  - As the webinar showed, Bound takes a literal, not `root.…`.
  - Workaround (derived): put the target in the expression, e.g. `root.serviceLevel() - root.slTarget` with type `>=` and Bound `0`. The target then stays a model parameter.
- **Constraint rows:** coefficients and bound are typed as numbers.
  - A constraint is checked before any model instance exists, so it cannot read `root` (derived from that timing).
  - Keep constraints linear in the optimization parameters, as in the demo. OptQuest can then discard a violating candidate without simulating it.
- **Enable checkboxes:** every Constraint and Requirement row has one. Keep F1's requirement and F2's budget both in the table and toggle between them.
- **Lever-only limits** (budget, headcount, total capacity) go in a Constraint, never a Requirement. As a Requirement, each violating candidate still costs a full replicated run.
- **Two KPIs on different scales** in one objective: normalise them before weighting (the presenter's advice). When a manager must see the trade-off, prefer the F1/F2 split.

## KPIs instrumented
Objective per iteration, best feasible value, feasibility per iteration, and a user-added scatter of service vs cost.

## Pitfalls
- **F1's optimum sits right on the bound.** The engine trades away every spare point of service to save cost. A plan averaging about 90 % misses 90 % in many single runs, so add a margin if the target means "nearly always".
- **A requirement plus a tight budget can leave nothing feasible.** The presenter warned about this for F2. Disable the requirement, run F2 to learn what is attainable, then set the bound.
- **Hard-coded coefficients go stale.** They do not follow later edits to the model's cost parameters, so note their source beside them.
- **F1 and F2 can differ in more than the bound.** Here F2 also freed the rule. Change one thing at a time when comparing them.

## Reusable idea
Pose the decision both ways. The min-cost plan prices the service target; the max-service plan prices the budget. A short sweep of either bound turns two answers into a trade-off curve a manager can choose from.

## When the co-pilot should use this
Use it when a user asks for "the best … subject to …" and both a cost KPI and a service KPI are in play:
- fill the intake card's objective with one KPI;
- sort every limit into Constraint or Requirement;
- offer the dual run and a bound sweep before recommending a single point.
