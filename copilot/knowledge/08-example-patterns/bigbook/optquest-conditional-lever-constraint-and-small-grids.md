# Pattern card — Optimization set-up: a lean model, conditional levers as 0/1 constraints, and grids small enough to enumerate
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 4 "How to build agent-based models. Field service example" (§4.7) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** A search over an on/off policy plus a setting that matters only when the policy is on wastes runs on duplicate plans, and a model full of charts runs every candidate slower than needed.

## Mechanism
Checked against the 8.9.10 model *Field Service Phase 6* and Help 8.9.10 (*Optimization experiment*).
1. **Strip the model for search** (book p. 45). Delete charts, chart-only statistics and their reset events. Keep only
   what the objective reads: here, the continuous statistic of working units and the work-cost accumulator. Add one
   function evaluated at run end, `profit()` = mean daily revenue × days − crew cost − work cost, and maximize
   `root.profit()`. Animation that is not displayed costs nothing; statistics that iterate a population on a timer do.
2. **Judge the warm-up explicitly.** Ages and maintenance dates are spread at start, so the fleet begins near its usual
   state. What still differs at time 0: nothing has failed, crews are at the depot, and queues are empty. The book
   estimates this settles within a year, runs 4 years and keeps the first year (p. 45). Record that judgement as an
   assumption.
3. **Encode "this lever matters only if the policy is on" as a constraint.**
   - Levers: `ServiceCapacity` 2..6, `ReplaceOldEquipment` (boolean), `MtcePeriodsToReplace` 2..8. That is
     5 × 2 × 7 = 70 plans, but 30 of them duplicate others, because the threshold is irrelevant with the policy off.
   - Constraint in the 8.9.10 model: `MtcePeriodsToReplace - 10 * ReplaceOldEquipment <= 2`. A boolean counts as 0 or
     1 in a constraint.
     - Policy off: only the threshold's minimum passes.
     - Policy on: every threshold passes, because 10 exceeds the range width.
   - General form: `x - M*b <= xMin` with `M >= xMax - xMin`. Here it cuts 70 runs to 40.
4. **OptQuest tests linear constraints without running the model** (Help), so pruned plans cost nothing. Keep gating
   constraints linear. A non-linear one may still cost a run before it is rejected.
5. **Count the grid before choosing the tool.** The book reports that the search stopped at 70 of 500 iterations
   because every plan had been tried *(Big Book p. 48; not stated in Help 8.9.10)*. When the grid is a few dozen
   points, a full-factorial Parameter Variation with replications gives every plan a mean and a CI. The optimizer adds
   nothing there.
6. **Set the ranges from interactive runs.** The flight-simulator runs showed that 2 crews cannot cope and 5 sit idle.
   An optimum in mid-range (3 crews, 7 periods) indicates the bounds were not binding (G12).

## Resources
n/a

## Key settings worth copying
- Parameter types: boolean for the policy; discrete with step 1 for the counts.
- Constraint row: Expression `MtcePeriodsToReplace - 10 * ReplaceOldEquipment`, Type `<=`, Bound `2`.
- After the search, copy the best values into the Simulation experiment. The optimizer reports only the objective,
  not the time profile (book p. 47).

## KPIs instrumented
Total profit over the run as the objective. Equipment availability and crew utilisation come from a follow-up
simulation of the chosen plan.

## Pitfalls
- **One noisy run per plan.** The 8.9.10 Phase 6 experiment has replications off and a random seed. The book's
  $17.8 M four-year optimum is therefore a single draw; re-run the top few plans with replications before trusting it
  (G11).
- **M too small cuts valid plans.** Check both policy values against the bound by hand.
- **The model under-weights late maintenance** (`bigbook/abm-time-dependent-hazard-rate-refresh.md`), so the
  crew-versus-replacement trade-off may shift once the rate is refreshed.

## Reusable idea
Write "this lever only matters if that switch is on" as a linear 0/1 constraint, and count the plans before choosing
between an optimizer and plain enumeration.

## When the co-pilot should use this
- Any optimization with on/off policies that carry their own settings: overtime yes/no plus hours, reorder policy type
  plus its parameters, a replacement policy plus its age limit.
- Any search space small enough to enumerate.
- Related: `07-optimization/README.md`, `videos/sim-opt-search-space-reduction.md`, and gotchas G8, G11 and G12.
