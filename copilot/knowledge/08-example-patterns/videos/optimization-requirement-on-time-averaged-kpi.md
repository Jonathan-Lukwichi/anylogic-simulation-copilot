# Pattern card — Optimization with a time-averaged requirement, set up so every iteration ends and replays
- **Source:** AnyLogic video "How to run optimization experiment" (https://youtu.be/3pM30wQfxV8) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Give the optimizer a whole-run average rather than an end-of-run snapshot as its requirement, and configure the experiment so each iteration finishes, is replicated and can be replayed in the Simulation experiment.

## Mechanism
1. **Objective scalar.** Add a value-returning Function on Main that sums the per-product Output elements, e.g. `return petrolExport + dieselFuelExport + fuelOilExport + crudeOilExport;`. Set the objective to **maximize** `root.productsExportedTotal()`.
2. **Run-averaged limit.**
   - The population statistic `trains.queue()` (a count over the trains population, called like a function) returns only how many trains are waiting right now.
   - A requirement is evaluated once, when the run ends, so on its own it would judge a single moment.
   - Wrap the statistic in a **Statistics** element (Analysis palette) named `trainsQueue`, with Value `trains.queue()` and **Update data automatically**.
   - The requirement then tests `root.trainsQueue.mean()` with type `<=` and bound `0`.
3. **Search space.**
   - Fix what the real system fixes. There is one tanker type, so tank count and tank capacity stay **fixed**.
   - Vary the real levers: train interarrival **continuous** from 120 to 600 min, and train capacity **discrete** from 400 to 1000 m³ with **step 50** (about one rail tank car).
4. **Run settings.** Keep the default iteration count and turn on **Automatic stop**. Set model time to **Stop at specified time**, 120 h. Choose **Random seed**, tick **Use replications** and set 10 per iteration.
5. **Read and replay.**
   - **Create default UI** plots every iteration: blue is feasible, red means the requirement failed.
   - **Copy** the best parameters, then click **Paste from clipboard** in the Simulation experiment's properties to run the optimum there.

## Resources
n/a

## Key settings worth copying
- `root` is the experiment's top-level agent (Main). Objective and requirement expressions are compiled in the experiment, so Main's members need the `root.` prefix.
- Statistics element type (from AnyLogic Help; the video doesn't show it):
  - **Continuous** gives a time-weighted mean. Use it for queue lengths, stock levels and occupancy.
  - **Discrete** gives the plain average of the samples.
- Make the discrete step the real-world lot size, so every candidate the engine proposes can actually be built.
- An iteration produces a value only when its runs end. A finite stop time, or `finishSimulation()` in the model, is mandatory.
- **Automatic stop** ends the search when the objective stops improving. That saves time on long models. On a flat, noisy objective, check whether it stopped early.

## KPIs instrumented
Total exported volume (the objective), time-averaged number of trains waiting (the requirement), and feasibility of each iteration.

## Pitfalls
- A requirement on a live value, such as a raw population statistic, judges only the last instant of the run.
- Sampling happens at the recurrence interval, so a queue that forms and clears between samples is never seen. If "no train may wait" is the real rule, shorten the interval or also count trains that ever waited.
- `mean <= 0` on a non-negative quantity tolerates no waiting at any sample. Agree a tolerance unless zero is contractual.
- Population statistics are computed by iterating the population on every call. A large population with a short recurrence interval costs run time.
- The best iteration is the maximum of noisy estimates, so its objective is biased upward. Re-run the pasted optimum with fresh replications before you report the number.
- For requirement vs constraint and the replication-mean caveat, see `videos/forecast-driven-staffing-optimization.md`.

## Reusable idea
Feed the optimizer only run-aggregated scalars: one objective function, plus one auto-updating Statistics element for each operational limit, each checked by a requirement.

## When the co-pilot should use this
- The limit is a level over time (queue, stock, WIP, occupancy) rather than a count of events. Use a time-weighted Statistics element, not the live value.
- Whenever you write an objective or requirement expression: add the `root.` prefix, confirm the run has a finite end, and plan to re-validate the optimum.

## Additions (8.9.10 review, 2026-10-01)
- Population statistics functions — `count`, `sum`, `average`, `min`, `max` and `sumWhere(pop, value, cond)`, `averageWhere`, `minWhere`, `maxWhere` — are global functions that scan the whole population on every call (Help 8.9.10, *Functions to collect statistics on agent population*); keep them out of anything evaluated per step in a large model (gotcha G84).
- *Create default UI* replaces everything on the optimization experiment's diagram: create it first and customise afterwards (Bass Diffusion tutorial, phase 13).
