# Pattern card — Faculty Aging Chain
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a university faculty population evolves over time as professors are hired, promoted through assistant → associate → full professor ranks, and eventually retire.

## Block chain
Three Stock variables hold headcounts at each rank: Assistant Professors, Associate Professors, and Full Professors. Flow variables connect them in a pipeline:
1. **Hire rate** (exogenous historic data) feeds new assistant professors into the first stock.
2. **Promotion flow (asst → assoc):** a fraction of assistants who complete an average review period are promoted; the rest leave.
3. **Promotion flow (assoc → full):** a fraction of associates who complete a second average review period are promoted; the rest leave.
4. **Retirement flow:** full professors leave after an average service time modelled as a third-order delay (pipeline delay), smoothing the outflow.

Auxiliary variables compute derived quantities: total faculty size, fraction of each rank in the total, and the two promotion fractions (set exogenously).

## Resources
No resource pools (pure SD). Stocks represent population levels; capacities are implicit in the promotion fractions and time constants.

## Key settings worth copying
- **Time unit:** Day (model converted from a Vensim MDL originally calibrated in years — watch unit conversions).
- **Initial conditions (circa 1930):** ~80 assistant, ~63 associate, ~86 full professors.
- **Review times:** separate average review durations for asst→assoc and assoc→full transitions (AuxVariables); straightforward to tune.
- **Promotion fractions:** exogenous constants — easy to swap for policy scenarios.
- **Retirement delay order:** third-order pipeline delay on full-professor retirement gives a realistic lag rather than a sharp step outflow.

## KPIs instrumented
- Total faculty count over time
- Fraction of each rank in the overall faculty (assoc fraction, asst fraction, full fraction)
- Hire rate trajectory (historic imputed data)
- Imputed promotion fractions for associate and assistant tracks

## Reusable idea
The **aging-chain pattern**: any multi-stage cohort pipeline (employee career ladders, product life cycles, patient disease progression) can be modelled as a series of stocks linked by promotion/transition flows, each governed by an average dwell time and an exit fraction. Using a higher-order delay (e.g., third-order) on the final outflow avoids unrealistic instantaneous retirement spikes and is the single most transferable trick here.
