# Pattern card — Statechart for Life Phases
- **Source:** AnyLogic example model "Statechart for Life Phases" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Move a person through life phases at random ages when people can join the model at any age (seeded population, births, in-migration).

## Structure
In the demo, `Person` is the top-level agent. Time unit Year, start date 1 Jan 2020.
- `birthTime` is an int parameter drawn with `uniform_discr(-50, 0)`. `age()` returns `(int) time() - birthTime`, the completed years.
- **Top level:** a composite `Alive` and a final state `Dead`.
  - The entry point leads to a branch that places the person by age: ≤ 14 Child; 14–49 Adult; 49–65 MidAge; Default Senior. The branch's action starts a text log.
  - Inside Alive, Child → Adult → MidAge → Senior are Timeout transitions.
  - `death` leaves Alive's border. It is drawn once, on entry to Alive, and acts as a deadline over every phase.
- **Adult is composite (family life).** Its initial pointer leads to a branch, not a state.
  - 30 % go to NoMoreKids.
  - The rest go to WantFamily (age ≤ 23) or WantKids.
  - WantFamily's timeout leads to a branch: WantKids with probability `0.6 / noOfKids` (always, while childless: 0.6/0 is infinite in Java double arithmetic), else NoMoreKids.
  - WantKids → `Kid` (Action `noOfKids++`) → WaitBetweenKids → back to that branch.
  - Leaving Adult for MidAge abandons whichever family state is active.
- `noOfKids` starts from a function of age, so a late entrant already has children: 0 up to 23; 0 or 1 at 23–26; 0–2 at 26–32; `negativeBinomial(0.8, 10)` after that.
- `Dead` runs `finishSimulation()`.

## Resources
n/a

## Key settings worth copying
- **Event age conditioned on the age already reached.** Adult → MidAge uses `normal(age(), infinity, 49, 5) - age()`. The other phases use the same form with 14 ± 2, 65 ± 7, family 21 ± 2 and death 65 ± 10. The truncated normal with min = current age draws the event age *given* survival to now. The timeout is never negative, and someone who enters Adult at 48 cannot be scheduled to reach MidAge at, say, 45.
- **Plain durations** use AnyLogic order `normal(sigma, mean)`:
  - `normal(0.2, 1)`: mean 1 year to the next child;
  - `normal(1, 5)`: mean 5 years between children.
- **Entry branch:** mutually exclusive exits plus one Default (`bigbook/statechart-guards-branches-and-state-reentry.md`).
- **Readable agents:** a String `history` appended in transition actions gives a per-agent life log. `getYear(timeToDate(birthTime))` shows the birth year.

## KPIs instrumented
Demo: text only (age, kids, log). For a population: phase counts over time (statistics with `agent.inState(Person.Adult)`, G53), completed fertility and the age-at-death histogram.

## Pitfalls
- **Book notation vs AnyLogic order.** Big Book ch. 7 p. 25 (and Fig. 7.19, p. 26) writes `normal(49,5) – age()` and means mean 49, sd 5. Typed into AnyLogic that is sigma 49, mean 5: phase ages spread over ±100 years. The shipped model avoids it with the truncated form, where the mean is the 3rd argument and the sd the 4th. See the proposed gotcha in `.ingest/proposals/m-bigbook-3.md`.
- **Untruncated `normal(sd, mean) - age()` can go negative** whenever the draw falls below the current age. Help 8.9.10 does not say how a negative timeout is handled *(unverified)*; do not rely on it.
- **`finishSimulation()` belongs to a one-agent demo.** In a population, the final state should remove the agent with the population's generated remove function. Otherwise the first death ends the run.
- **The death deadline ignores later changes.** It is drawn once, on entering Alive. If mortality should depend on phase, health or policy, redraw it per phase or model a hazard (`bigbook/abm-time-dependent-hazard-rate-refresh.md`).
- **`age()` is whole years.** That is fine for yearly phases and coarse for monthly decisions. A timeout uses the age at the moment its state is entered (Help *Transition*: the expression is evaluated once, on entry).

## Reusable idea
For "the event happens at age, tenure or operating hours X ~ F" with agents that start part-way, draw from F truncated below at the current value and subtract it: `normal(now, infinity, mu, sd) - now`. The truncated `weibull(min, max, alpha, shift, stretch)` or `gamma(...)` forms work the same way for wear-out. Pair this with an entry branch that places each agent in its current phase.

## When the co-pilot should use this
- Demographic, health, workforce or asset-life ABMs whose agents start at different ages.
- A user has copied `normal(mean, sd)` from a paper or from the Big Book.
- Related: `basicmodels/initialize-agents-in-different-states.md`, `bigbook/synchronous-tick-transition-from-probability-table.md`, `models/agent-based-population-model.md`, `bigbookmodels/probability-distributions.md`.
