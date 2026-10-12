# Pattern card — Per-period probability tables in a statechart: a "synchronous" tick transition vs one time-to-event draw
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 7 "Designing state-based behavior: statecharts" — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** The data give a probability per period (per year of age, per month on a waiting list), not a time-to-event distribution. Turn that into state changes without fitting a distribution.

## Mechanism
The book's example gives the chance of starting to drink at each age: zero at 11, a peak of about 0.23 at 18, zero again by 24. The statechart has two states, NeverUser and User.
- NeverUser has a Timeout transition of 1 period (1 year) leading into a Branch:
  - Conditional exit `randomTrue(initiationProbability(age))` → User;
  - Default exit → back to NeverUser.
- `initiationProbability` is a Table Function whose *Out of range* setting is *Nearest*, so ages beyond the table reuse the end values (zero here). The book interpolates with a spline.
- **Age.** The book uses `time()` because every agent exists from time 0 and time is in years. Agents created mid-run should store `birthTime` and use `time() - birthTime` (Big Book p. 21).

The book calls these decisions made at regular ticks "synchronous" transitions, as opposed to the usual asynchronous ones. The KB already holds the other route: `models/alcohol-use-dynamics.md` turns the same kind of table into a single time-to-event draw per agent (`rateToDistribution`).

## Resources
n/a

## Key settings worth copying
Choosing between the two:

| | Tick + branch (this card) | Table → one draw (KB model) |
|---|---|---|
| Events per agent | one per period until it fires | one |
| Data use | as published, one Bernoulli trial per period | needs a survival-weighted conversion |
| Risk that changes mid-life (policy, exposure, peers) | picked up at the next tick | ignored unless the draw is redone |
| Timing | whole periods only | continuous |

- Use tick + branch when interventions or other agents change the risk during the run, or when the table is short and the population small.
- Use the single draw for large populations with fixed tables, where event count dominates run time.

## KPIs instrumented
Initiations per age band per year. Compare the simulated age-at-initiation histogram with the input table as a validation check.

## Pitfalls
- **The tick is an outside loop.** Every tick exits and re-enters NeverUser, so its entry action reruns and any other Timeout leaving NeverUser restarts each period. This follows from Help's rule that a timeout counts from entry into its source state. Keep other deadlines on an enclosing composite state or in events, and don't count state entries as events.
- **Changing the tick length.** A yearly probability p is not p/12 per month; use `1 - pow(1 - p, 1.0/12)` for a constant hazard *(standard conversion)*.
- **No Default exit** on the branch is a runtime error when the draw fails (Help *Branch*).
- **Tick phase.** Each agent's ticks fall on its own entry anniversaries. If the table is by exact age, create agents at birth or align the first tick deliberately *(inferred)*.

## Reusable idea
Let the shape of the data choose the trigger: per-period probabilities → a periodic trial; a hazard or duration distribution → one timeout draw; a rate that depends on others → a Rate trigger plus `onChange()`.

## When the co-pilot should use this
- Health, social or reliability ABMs fed by age- or period-specific probability tables (initiation, onset, dropout, failure per inspection).
- A user asks how to use a table of yearly probabilities in a statechart.
- Related: `models/alcohol-use-dynamics.md`, `bigbook/statechart-guards-branches-and-state-reentry.md`, and G56.
