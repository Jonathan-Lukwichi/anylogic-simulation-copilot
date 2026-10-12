# Pattern card — SIR Agent Based Calibration
- **Source:** AnyLogic example model "SIR Agent Based Calibration" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (with Optimization-based calibration and a Monte Carlo experiment)
- **Problem it solves:** Fit a *stochastic* agent-based epidemic to an observed infection curve, then show how widely single runs scatter around the fitted behaviour.

## Structure
- **`Person` statechart:**
  - Susceptible → Infectious on any message.
  - Infectious keeps an internal Rate transition, rate `ContactRate * InfectionProbability`, that runs `send("Infection", RANDOM)`.
  - Recovery at Rate `1 / AverageIllnessDuration`.
- **Main:**
  - 10,000 people. Startup seeds one case with `sendToRandomAgentInside("Infection")`.
  - `InfectiousDS` samples `people.nInfectious()` every 2 days and keeps 100 samples, which covers the 200-day run exactly.
  - Table function `InfectiousHistoric` holds the observed data every 2 days.
  - Outputs `maxPrevalence` and `differenceWithHistoricData = difference(InfectiousDS, InfectiousHistoric)`, the Cloud-ready fit error.
- **The shared calibration mechanics are already carded** in `bigbookmodels/epidemic-model-various-experiments.md`: `difference()` as an RMSE over the overlapping x-range, why the fit error is an Output for Cloud, `fillFrom(TableFunction)`, dataset coverage, and identifiability. This card adds what changes when the model is **stochastic**.

## Resources
n/a

## Key settings worth copying
- **The "Calibration" is an Optimization experiment.**
  - Free parameters: `ContactRate` ∈ [0.5, 5] and `InfectionProbability` ∈ [0.1, 0.8], with `AverageIllnessDuration` fixed at 15 days.
  - Random seed, **fixed 5 replications per iteration**. The engine takes one objective sample per iteration, the mean across its replications (Help 8.9.10, *Optimization experiment*). Here that is the mean of the per-run RMSEs.
- **Experiment-side bookkeeping.**
  - *After simulation run*: `dsInfectiousCurrent.fillFrom(root.InfectiousDS)`.
  - *After iteration*: `if (getCurrentIteration() == getBestIteration()) dsInfectiousBest.fillFrom(dsInfectiousCurrent)`.
  - Objective traces come from `getCurrentObjectiveValue()` and `getBestObjectiveValue()`.
- **Monte Carlo fan chart.** A Parameter Variation experiment (fixed parameters, random seed) runs `dataInfectious2D.reset()` *Before each experiment run* and `dataInfectious2D.add(root.InfectiousDS)` *After simulation run*.
  - `dataInfectious2D` is a `Histogram2DData` with 80 × 40 cells over x 0–200 days and y 0–8000, and **envelopes 0.25, 0.5, 0.75**.
  - Help 8.9.10 (*Histogram 2D data*): `add(DataSet)` adds a whole trajectory; each x-column keeps its own histogram; an envelope is the band holding the given share of the data.
  - The `Histogram2D` chart is set to show the **bins** (density spots). The envelopes are defined in the data but drawn only if the chart's *Show envelopes* option is chosen (Help *Histogram 2D*); switch to it for a quartile-band picture.

## KPIs instrumented
Misfit per iteration (current vs best), best-fit trajectory vs data, peak prevalence, and the spread of trajectories (a 2D density of all runs).

## Pitfalls
- **Identifiability.** The two free parameters act only through their product, so every pair with the same c·i fits equally well; the reported "best" pair is arbitrary. This is KNOWN-KB (`bigbookmodels/epidemic-model-various-experiments.md`); the model still frees both.
- **The plotted "best" curve is one replication.** It is the last replication of the best iteration, not that iteration's mean behaviour. Plot the mean of the best iteration's replications before judging the fit visually *(suggested)*.
- **The mean of per-run RMSEs is not the RMSE of the mean curve.** Averaging each run's misfit also penalises run-to-run noise, so it favours parameter sets with less variable epidemics. Use it for "typical run" fidelity. To fit the average epidemic, compare the mean trajectory of the replications instead *(reasoned)*.
- **Possible one-run lag.** The objective reads an experiment-level copy filled in *After simulation run*. Help does not document the order of that action and the objective sample, so reading `root.differenceWithHistoricData` directly avoids the risk *(unverified ordering)*.
- **Too few replications chase noise** (G11; `videos/sim-opt-lucky-optimum-and-shortlist-reverification.md`). Re-verify the winner with many more replications.

## Reusable idea
Treat calibration of a stochastic model as noisy optimisation:
- a scalar misfit Output;
- a fixed number of replications per candidate;
- an explicit choice between "fit the typical run" (mean per-run misfit) and "fit the mean curve";
- after the fit, a Histogram2D fan chart so users see how far single runs stray from the fitted behaviour, instead of one curve.

## When the co-pilot should use this
- **Use cases:** fitting any ABM or DES model to a historical time series (epidemics, adoption, WIP), and reporting run-to-run spread as bands instead of one line.
- **Related cards:** `bigbookmodels/epidemic-model-various-experiments.md` (deterministic SD calibration), `models/sir-agent-based-networks.md` (topology Monte Carlo) and `basicmodels/calibration-from-within-simulation.md`.
