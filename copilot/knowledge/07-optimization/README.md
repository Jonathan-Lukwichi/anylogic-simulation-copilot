# 07-optimization

Simulation-based optimization (sim-opt) in AnyLogic: the Optimization experiment with the OptQuest or
Genetic engine, Custom-experiment optimizers, and Cloud optimization. Exact field names: check the
installed Help first, then anylogic.help (see `../INDEX.md`). Method cards live in
`../08-example-patterns/videos/`; the traps are gotchas G8–G15 in
`../01-anylogic-core/anylogic-gotchas.md`.

## First: is sim-opt the right tool?
Judge by how large the solution space is and how fast the answer is needed.

| Problem shape | Fit | Examples | KB route |
|---|---|---|---|
| Structured allocation; randomness not central; an answer in days is fine | LP / MILP (exact) | network design, master production planning | Python bridge: `../08-example-patterns/basicmodels/machine-optimizer.md`, `models/supply-chain-optimizer.md` |
| Huge combinatorial space | metaheuristic / specialised solver | vehicle routing, cutting | `models/traveling-salesman.md` (OR-Tools) |
| Stochastic process detail; a handful to ~100 levers | **sim-opt** (Optimization experiment) | machines per station, staffing by skill, days of supply | `videos/sim-opt-*` cards |
| Online, time-critical sequential decisions | RL policy trained on the simulator | loading boxes as they arrive | `../../templates/rl-pipeline/`, `models/border-checkpoint-optimization.md` |
| Detect or predict from sensor/history data | ML | predictive maintenance, demand forecast | `../06-ai-ml-integration/` |

Adding the real rules and randomness makes an exact formulation intractable; simplifying until a
solver copes can make the answer irrelevant. Sim-opt keeps the valid model and accepts a
near-optimal **"best found"** answer — say so when reporting.

## Setup essentials
- ONE objective: a `root.`-prefixed scalar (G9). A finite stop time (G10).
- Limits on the levers → **Constraints** (checked before each run). Limits on results →
  **Requirements** (checked after each run, on the replication mean) (G8). Level-type limits
  (queue length, stock, WIP) belong on a time-weighted statistic, not a live value
  (`videos/optimization-requirement-on-time-averaged-kpi.md`).
- Replications per iteration with distinct seeds; re-run the top 3–5 plans with fresh, larger
  replications before recommending one (G11). An optimum on a range edge means widen the range (G12).
- Engine limits: bundled OptQuest ≤ 7 variables / 500 iterations per AnyLogic's 8.8.4 notes;
  Genetic (8.8.4+) has no such cap but uses a fixed replication count and a finite iteration count;
  Cloud optimizes with Genetic only (G14).
- **Two populations, one lever** (signal phases: cars vs pedestrians; shuttle dwell: waiting riders
  vs cycle time): minimise the primary KPI and cap the other as a Requirement; instrument both flows
  first (`models/traffic-light-phases-optimization.md`, `videos/traffic-light-gated-pedestrian-crossing.md`).
- Copy the best parameters into a Simulation experiment and re-validate them with fresh replications.

## Method cards (`../08-example-patterns/videos/`)
- `sim-opt-dual-formulations-and-bounds.md` — min cost for a target vs max service for a budget; bound mechanics; trade-off sweep.
- `sim-opt-lucky-optimum-and-shortlist-reverification.md` — replication settings; lucky optima; re-verifying winners.
- `sim-opt-search-space-reduction.md` — many levers: decompose, Pareto-aggregate, edge check, coarse-to-fine.
- `optimizer-engine-and-venue-choice.md` — OptQuest vs Genetic vs Custom experiment vs Cloud; limits and licensing.
- `dispatching-rule-as-optimizable-policy.md` — a sequencing rule as a lever, vs adding capacity.
- `forecast-driven-staffing-optimization.md` — forecast → input file → optimizer with an output requirement.
- `optimization-requirement-on-time-averaged-kpi.md` — requirement on a time-averaged KPI; setup checklist.

## Default experiment ladder
1. Named scenarios. 2. Parameter Variation with replications, to screen levers. 3. Optimization with
replications. 4. Re-verify the shortlist. 5. Report "best found" with a CI.

See SOURCES.md for the exact links and download/fetch-live status.
