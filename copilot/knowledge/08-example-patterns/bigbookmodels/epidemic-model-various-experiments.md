# Pattern card — Epidemic Model - Various Experiments
- **Source:** AnyLogic example model "Epidemic Model - Various Experiments" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Fit parameters that cannot be measured to an observed time series, on the desktop and on AnyLogic Cloud, and let users re-run what-ifs instantly.

## Structure
- **SIR model.**
  - Stocks: Susceptible (starts at `TotalPopulation - 1`), Infectious (starts at 1), Recovered.
  - `InfectionRate = Infectious * ContactRate * Infectivity * Susceptible / TotalPopulation`; `RecoveryRate = Infectious / AverageIllnessDuration`.
  - Parameters 5, 0.08, 1000 and 12. Time runs 0–100; the unit is nominally Minute.
- **Observed data:** table function `InfectiousHistoric`, 21 points at t = 0, 5, …, 100, Linear, out of range *Error*.
- **Outputs:** datasets `SusceptibleDS`, `InfectiousDS` and `RecoveredDS` sample the stocks every time unit and keep 100 samples.
- **Experiments:**
  1. **Simulation.**
  2. **Calibration**, an OptQuest Optimization experiment:
     - objective: minimise `difference(root.InfectiousDS, InfectiousHistoric)`;
     - varied: Infectivity continuous in [0, 0.1] and AverageIllnessDuration in [3, 30];
     - fixed: ContactRate and TotalPopulation;
     - 500 iterations, no replications, fixed seed, parallel evaluations;
     - custom UI: it copies the current and best curves into experiment datasets with `fillFrom` after each run and iteration, and a button puts the best values on the clipboard.
  3. **InstantCharts**, a Compare Runs experiment whose sliders set a value and call `run()`. KNOWN-KB: Big Book ch. 5 pp. 40–43; `bigbook/sd-instant-charts-and-step-pause-flight-simulator.md`.
- **Cloud-ready fit** (model mechanics beyond the book):
  - Main's On startup copies the table into a DataSet: `InfectiousHistoricData.fillFrom(InfectiousHistoric)`.
  - An `Output` named `differenceRequirement` holds `difference(InfectiousDS, InfectiousHistoricData)`, calculated on simulation end. The model's own comment says it serves calibration on AnyLogic Cloud.

## Resources
n/a

## Key settings worth copying
- **`difference()`** (Help 8.9.10, *Calibration experiment*): `difference(DataSet, TableFunction)` and `difference(DataSet, DataSet)` return a non-negative **RMSE**. It is taken over the **intersection of the two X ranges**, with both curves linearly interpolated.
- **Why an Output:** a Cloud optimisation minimises or maximises one of the model's Outputs, with the genetic engine only (Cloud Help, *Optimization*). Desktop experiment code does not run on Cloud (G49). So the observed series must live in the model, and the fit error must be a scalar Output calculated on simulation end.
- **`fillFrom(TableFunction)`** discards old data and resets the dataset's capacity to the table size (Help *Data set*). The historic dataset's "keep 1 sample" setting is therefore harmless.

## KPIs instrumented
- RMSE per iteration and the best feasible value;
- fitted vs observed Infectious curve;
- best Infectivity and AverageIllnessDuration.

## Pitfalls
- **Identifiability.** ContactRate and Infectivity appear only as a product, so every pair with the same product fits equally well. Calibrate one of them; the model fixes ContactRate. This is general calibration practice, and the KB makes the same point for Bass models in `videos/abm-word-of-mouth-contact-targeting.md`. Look for other trade-offs, such as a rate against a duration, before choosing decision variables.
- **The fit sees only the overlap.** A run shorter than the history, or a dataset whose tail size drops early samples, silently removes those periods from the RMSE. A dataset keeps only its latest N samples (Help *Data set*; compare G18); here 100 samples at step 1 cover about t = 1–100. Set *Keep up to … latest samples* to at least run length ÷ sampling step.
- **Sampling step.** Record the model output at least as often as the data points, or interpolation will blur peaks.
- **Stochastic models** need replications per iteration (G11). This SD model is deterministic, so one run per iteration is right.
- **Parallel evaluations** require table functions and custom distributions that are not *Static* (Help *Calibration*).
- **The historic table's *Error* setting** is safe inside `difference()`, which uses only the overlap. It throws if the table is called directly past t = 100.
- **"Create default UI"** on a calibration experiment deletes the wizard-built UI (Help).

## Reusable idea
Store the observed series in the model (table function → DataSet at startup) and expose the fit error as a scalar Output on simulation end. The same model then calibrates on the desktop and on Cloud, and the fit error becomes a reportable validation KPI. For several series, add one RMSE per series and weight them (Help: coefficients on calibration criteria).

## When the co-pilot should use this
- Calibrating SD or ABM models to historical curves (epidemics, adoption, demand, inventory), especially when the tool will run on AnyLogic Cloud.
- A user asks what `difference()` computes.
- A calibration returns many equally good parameter sets.
- Related: `07-optimization/README.md`, `videos/cloud-run-semantics-and-access.md`, `videos/optimizer-engine-and-venue-choice.md`, `sdmodels/sir-model.md`.
