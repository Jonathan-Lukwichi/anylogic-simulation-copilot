# Pattern card — Scaling sim-opt: shrink the search space before searching
- **Source:** AnyLogic video "Webinar | Simulation-Based Optimization in AnyLogic" (https://youtu.be/YyDJDqMqYng) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Keeping simulation-based optimization tractable with dozens to ~100 decision variables.

## Mechanism
0. **Check the engine ceiling first.** The OptQuest bundled with AnyLogic accepts at most 7 decision variables and 500 iterations unless you buy the paid add-on. The Genetic engine (AnyLogic 8.8.4+) has no cap; see `videos/optimizer-engine-and-venue-choice.md`. Each tactic below also helps a problem fit under that cap.
1. **Decompose.** When groups of levers barely interact (say 20 of 50 are unrelated to the rest), optimize one group, freeze it, then optimize the next.
2. **Pareto-aggregate.** Example: safety stock (days of supply) for 100 SKUs. Give the ~20 SKUs that carry ~80 % of sales their own parameter, and let one shared parameter cover the other 80. That is 21 variables instead of 100.
3. **Edge check.** If the best value lands on a range limit, the real optimum is probably outside the range. Move or widen the window, keeping the old edge inside it, and re-run.
4. **Coarse-to-fine.** First search a wide range with a big step (e.g. 1000–5000 in steps of 100–200). Then search a narrow window around the winner (e.g. around 2200, step 10).
5. **Read the plateau.** In the demo, the best-feasible curve went flat by about iteration 180 of 500, and Automatic stop ended a stalled run near iteration 300. Set iteration budgets by watching this curve, not by formula.

**Field evidence** from the presenter's team: problems with up to ~100 levers were solved this way. Typical cases:
- departure times for about 90–100 daily cross-dock trucks, against a service-time target;
- quick-service-restaurant staffing by skill, against order-to-delivery time;
- days of supply for a short-shelf-life product, trading service level against write-offs.

## Resources
n/a

## Key settings worth copying
- Each decision variable has a Min, Max and Step. Treat Step as a lever for tractability, not only a choice of resolution.
- Keep a stage log: window, step, best value, and whether the best value hit an edge.

## KPIs instrumented
Best feasible objective at each stage, and the number of iterations to plateau.

## Pitfalls
- **Decomposition assumes weak interaction.** Test it by re-optimizing an early group after the later ones. If its best values move a lot, optimize the groups jointly (judgement).
- **A coarse step can jump over a narrow optimum** in a spiky response. Coarsen only where the response is smooth (judgement).
- **One shared "tail" parameter** can starve a low-volume but critical item. Carve out exceptions.
- **Metaheuristics return a best-found answer**, not a proven optimum. Report it that way.

## Reusable idea
Shrink the problem first, then search. Use fewer variables (decompose, aggregate), honest bounds (edge check) and coarse grids that you refine afterwards. Run the search in stages, not as one huge search.

## When the co-pilot should use this
- A user wants to optimize more than a handful of levers.
- A search hits the default OptQuest cap of 7 variables or 500 iterations.
- An optimum sits on a range edge.
- Before recommending a paid engine upgrade.
