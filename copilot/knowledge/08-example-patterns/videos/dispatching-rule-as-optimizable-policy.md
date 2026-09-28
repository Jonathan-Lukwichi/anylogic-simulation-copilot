# Pattern card — Dispatching rule (FCFS/EDD/LST/CR) as an optimizable job-shop policy
- **Source:** AnyLogic video "Webinar | Simulation-Based Optimization in AnyLogic" (https://youtu.be/YyDJDqMqYng) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Letting experiments choose a job-shop sequencing rule and weigh it against buying machines, judged on on-time %.

## Block chain
1. `Source` generates orders. The arrival rate is known; the arrival times are random.
2. Each order agent draws a product type (1–4) from a known mix and gets `dueDate` = arrival + a promised lead time that depends on the customer (roughly 2–10 days).
3. The order agent carries `step`, arrival time, `dueDate` and completion time.
4. It enters the `WorkCenter` agent that its product's routing names at `step`: a `Queue`, whose discipline is set by the rule code, feeding a `Service` with `n` parallel machines. Processing time depends on product and work centre, ±10 %.
5. On exit, `step++`. The order moves to the next work centre, or to `Sink` when its routing is done.
6. At `Sink` the order counts as on time if its completion time ≤ `dueDate`.

The shop has four work centres (A–D) and four products, each with its own ordered routing (e.g. A→B→C→D; D→B→C). There are no transfer times; breakdowns are optional.

## Resources
Machines per work centre is an integer parameter (demo range 1–6; cost per machine 10/15/10/20 k$ for A/B/C/D). The rule acts in the queue in front of each work centre.

## Key settings worth copying
- **Rule code:** an integer parameter, range 1..4, step 1. 1 = FCFS, 2 = EDD, 3 = least slack time (LST), 4 = critical ratio (CR). For encoding a choice as a discrete parameter, see `videos/layout-candidates-and-design-time-api.md`.
- **Urgency keys** (smaller means serve first):
  - EDD: `dueDate`
  - LST: `dueDate - time() - remainingWork`
  - CR: `(dueDate - time()) / remainingWork`
  - `remainingWork` is the nominal processing time of this operation and all later ones.
- **When AnyLogic's `Queue` ranks an agent:** it fixes the agent's place when it enters.
  - *Priority-based*: priority of the incoming agent; larger is served first.
  - *Agent comparison*: the newcomer is compared with the agents already waiting.
- **Consequences for each rule** (derived):
  - FCFS: use FIFO.
  - EDD: use priority `-agent.dueDate`, or the comparison `agent1.dueDate < agent2.dueDate`.
  - LST: all waiting jobs share the same `time()`, so their ranking never changes while they wait. Use the static priority `-(agent.dueDate - agent.remainingWork())`. Do not compute slack with `time()` at each job's own entry: that mixes different clocks and mis-ranks jobs.
  - CR: the ranking can flip while jobs wait, so choose at dispatch time. Hold waiting jobs in a `Delay` set to "until stopDelay() is called" (gotcha G7). When a machine frees, call `stopDelay()` on the job with the lowest current CR.
- **One queue for three rules:** a comparator function that switches on the rule code keeps FCFS, EDD and LST in a single `Queue`.

## KPIs instrumented
- Service level = on-time orders / completed orders (one demo run: 137 of 200, about 68 %).
- Investment cost = Σ machines × unit cost.
- A histogram data set of service level per rule across replications (the screening run).

## Pitfalls
- **Using sampled actual durations in `remainingWork`** lets the rule "see the future". Use nominal or mean times (judgement).
- **Ranking rules on one run.** With about 200 orders, on-time % moves several points from run to run. Compare distributions.
- **Treating the rule code as ordinal.** It is nominal: rule 2 is not "between" 1 and 3. That is fine for four rules. With many options, enumerate them in Parameter Variation rather than rely on the optimizer's neighbourhood moves (judgement).

## Reusable idea
Test the free policy lever before the capital one. With 4 machines at every work centre:
- FCFS gave about 68 % on time;
- EDD or LST gave about 76–77 %.

That came from a Parameter Variation with 100 replications per rule and zero investment. Next, let the optimizer choose rule and capacity together (F2 in `videos/sim-opt-dual-formulations-and-bounds.md`).

## When the co-pilot should use this
- Job shops, make-to-order lines, repair or maintenance work orders: any queue where jobs carry due dates and the KPI is on-time %.
- When a user wants to "buy more machines" before trying a sequencing rule.
