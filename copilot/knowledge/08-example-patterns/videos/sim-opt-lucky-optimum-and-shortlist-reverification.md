# Pattern card — Sim-opt lucky optima: replication settings and shortlist re-verification
- **Source:** AnyLogic video "Webinar | Simulation-Based Optimization in AnyLogic" (https://youtu.be/YyDJDqMqYng) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Keeping a stochastic optimization from recommending a plan that only won on a favourable random draw.

## Mechanism
- **How a lucky optimum happens.** The optimizer keeps whichever candidate *looks* best. With one run per candidate, a marginal plan can clear a requirement on a lucky draw and win. Over hundreds of candidates the search will almost surely find such flukes. The reported optimum is therefore biased optimistic, most of all when a requirement binds.
- **Webinar evidence.** Same job shop, same problem (minimise cost, service ≥ 90 %):
  - desktop, 50 replications per iteration: (5,3,4,5), cost 235;
  - AnyLogic Cloud, experiment type "Optimization", one run per candidate: (4,3,4,5), cost 225, at a reported 91 %.

  The cheaper plan is most likely a fluke: the replicated search over the same ranges settled 10 k$ higher. The presenter expected replications to change the Cloud answer.
- **Why a separate step is needed.** Replications take most of the noise out of the *search* (basics in `videos/forecast-driven-staffing-optimization.md`). They do not remove the bias of picking the best of many noisy scores, so the winners need re-verifying.

## Resources
n/a

## Key settings worth copying
- **Desktop:** Optimization experiment, *Use replications*, then one of:
  - **Fixed:** replications per iteration (the webinar used 50).
  - **Varying number of replications:** set Minimum replications, Maximum replications, Confidence level and Error percent. Error percent is 0–1: the CI half-width as a fraction of the mean. An iteration stops adding replications once its CI is that tight or the maximum is reached.
- **Engine support:** Varying works with OptQuest only. The Genetic engine takes a fixed count (AnyLogic 8.8.4 notes).
- **Cloud:** choose the experiment type **"Optimization with replications"**. The plain "Optimization" type evaluates each candidate once.
- **Seeds:** replications need different seeds. A custom generator with a constant seed makes every replication identical; see `videos/rng-seed-control-and-custom-generator.md`.
- **Sizing a fixed count:** run a pilot of the incumbent plan, then size the count with a standard sample-size calculation for a mean (e.g. the NIST e-Handbook, see `../../../SOURCES.md`).
- **Run budget:** iterations × replications model runs (500 × 50 = 25,000 in the demo).

## KPIs instrumented
For each shortlisted plan: the mean, CI and histogram of the binding KPI, plus the share of replications that meet the target.

## Pitfalls
- **Optimizing a stochastic model on single runs:** replications switched off on the desktop, or the plain Cloud "Optimization" type.
- **Re-running only the winner.** Its score is biased upward (see `videos/optimization-requirement-on-time-averaged-kpi.md`). A single re-run can still miss a runner-up that is really cheaper or safer.
- **Too few replications near a binding requirement:** neighbouring plans flip between feasible and infeasible, and the search wanders.

## Reusable idea
Search on replicated means, then re-verify the winners:
1. take the best 3–5 feasible plans from the optimization log;
2. rerun each with a much larger replication count, e.g. a Parameter Variation in Freeform mode listing exactly those combinations;
3. give every plan the same replication seeds (dedicated streams, see `videos/rng-seed-control-and-custom-generator.md`), so the differences reflect the plans, not the noise;
4. recommend the cheapest plan whose CI still clears the target.

Re-verification is standard sim-opt practice. It was not shown in the webinar.

## When the co-pilot should use this
- Any optimization of a model with random inputs.
- When a user shows an optimizer result from single runs, or a "best" plan sitting right on a requirement bound.
- Before a recommendation leaves Phase 6.
