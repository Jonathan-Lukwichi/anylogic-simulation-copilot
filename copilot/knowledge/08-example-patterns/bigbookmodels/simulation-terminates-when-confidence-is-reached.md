# Pattern card — Simulation Terminates when Confidence is Reached (and why the rule stops too early)
- **Source:** AnyLogic example models "Simulation Terminates when Confidence is Reached" and "Statistics as Function of the Number of Observations" (bigbookmodels/Output data), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** End a run automatically once an output mean is "precise enough" — and know what AnyLogic's confidence interval really measures before trusting such a rule.

## Block chain
`Source` (1 bill per minute, `new Bill(time())` stamps the creation time) → `Service processBill` (pool `clerks`,
capacity 15, `triangular(5, 10, 25)` min) → `SelectOutput billOK` (p = 0.8) → `Sink`; the other 20 % pass
`Service fixError` (3 min, same pool) → `Sink`.
Sink On enter: `latestTimeInSystem = time() - agent.timestamp; statsTimeInSystem.add(latestTimeInSystem);` then
`if (statsTimeInSystem.meanConfidence() / statsTimeInSystem.mean() < 0.001) finishSimulation();`. Stop = *Never*,
fixed seed. A time plot shows the mean, mean ± `meanConfidence()`, mean ± `deviation()` and the latest value.
Companion model: a cyclic event adds one `normal(10, 30)` draw per time unit to a Statistics element and plots the
same curves, which narrow roughly as 1/√n.

## Resources
`clerks` ResourcePool, 15 units. Offered load ≈ 13.9 clerk-minutes per bill (13.3 mean processing + 0.2 × 3 fixing)
at one bill a minute: about 93 % utilisation.

## Key settings worth copying
- **What `meanConfidence()` returns** (Help *Statistics*: half-width, level fixed at 95 %; engine 8.9.10,
  `com.anylogic.engine.analysis.StatisticsDiscrete`): 0 with no sample, +Infinity with one (so the rule cannot fire on
  the first bill), otherwise `t · deviation() / √n` with t from an internal table that starts at 2.776 and is read one
  degree of freedom high; 1.96 from 100 degrees of freedom up. For n = 2, 3, 4 that gives 2.776 instead of 12.71,
  4.30 and 3.18 — up to 4.6 times too narrow; n = 5–8 are 2–7 % too narrow.
- **Exact small-n half-width:** `tValue * s.deviation() / Math.sqrt(s.count())`, with `tValue` taken from a t-table
  for `s.count() - 1` degrees of freedom and the level you report (4.303 for n = 3 at 95 %).
- **Relative precision:** `meanConfidence() / mean()` is the right shape for a stop rule, but only on independent
  observations (below).
- **`normal(a, b)` is `normal(sigma, mean)`:** the companion's `normal(10, 30)` has mean 30 and SD 10, although its
  description announces mean 5 and SD 10 (Big Book ch. 15 pp. 4–6; *AnyLogic in 3 Days* p. 83).

## KPIs instrumented
Mean time in system with its 95 % half-width and ± one SD band; the latest value.

## Pitfalls
- **Within-run observations are not independent.** At about 93 % utilisation, bills that follow each other share the
  same backlog, so their times in system are strongly positively correlated. The i.i.d. formula then understates the
  standard error of the mean by roughly √(1 + 2Σρₖ) (standard output-analysis result), and the 0.1 % target is met long
  before the mean is that precise.
- **Start-up bias.** The run starts with idle clerks and no backlog; early bills are fast, so the mean is biased low
  until the warm-up is over. Stopping "as soon as precise" also favours stopping on a lucky stretch.
- **Small n** (above): never let a stop rule fire before a minimum count (for example 30 batches or replications).
- **Stop = Never plus `finishSimulation()`** ends every run of every experiment type the same way; an optimisation or
  sweep inherits the rule.

## Reusable idea
Keep the stop-when-precise idea, but apply it to independent units: after a warm-up, group observations into 20–30
equal batches (or run independent replications), compute the CI over batch or replication means with the exact t value,
and stop when its relative half-width meets the target and the minimum count is reached.

## When the co-pilot should use this
- Choosing run length or replication counts; reporting any CI from AnyLogic Statistics elements; reviewing a model that
  ends itself on a precision rule.
- Related: G16 (identical replications), G18 (dataset capacity), `videos/sim-opt-lucky-optimum-and-shortlist-reverification.md`,
  `02-statistics-input-modeling/README.md`.
