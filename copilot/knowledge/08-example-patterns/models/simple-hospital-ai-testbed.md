# Pattern card — Simple Hospital (AI Testbed)
- **Source:** AnyLogic example model "Simple Hospital (AI Testbed)" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (with two trained neural networks called through the Pypeline library)
- **Problem it solves:** Test trained ML predictors in a dynamic bed-capacity system before trusting them: an arrival-rate forecaster and a patient length-of-stay (LOS) regressor.

## Block chain
- **Flow:** `Source` (rate 0 at start, set by an event) → `Queue` (unlimited) → `Delay stay` (capacity = `hospitalCapacity`, 300 beds; delay = predicted LOS in **days**) → `Sink`.
- **Python session:** *On startup*, `pyCom.run("from nn_model_parser import HospitalPredictor", "predictor = HospitalPredictor()")`. This imports the helper and creates one predictor object that persists in the Python session.
- **The helper class** (`nn_model_parser.py`) loads two Keras `.h5` models:
  - `predict_rate()` keeps its last six outputs in a queue, scaled to [-1, 1], and returns the next hourly rate rescaled to real units;
  - `predict_los(array)` takes a 1 × 24 feature array.
- **Arrivals:** a cyclic event every 4 h runs `source.set_rate(pyCom.runResults(double.class, "predictor.predict_rate()"), PER_HOUR)`.
- **LOS:** the delay time is `pyCom.runResults(double.class, "predictor.predict_los(" + agent.getArrayStr() + ")")`.

## Resources
Beds = the capacity of `stay` (a Delay, not a ResourcePool); the Queue holds patients waiting for a bed.

## Key settings worth copying
- **Feature contract in one function.** `getArrayStr()` formats the 24 features in the training order as `[[...]]`: booleans as 0/1, continuous labs z-scored with training means and SDs stored on the agent, and `numberOfIssues = count(Arrays.asList(...), b -> b)`.
- **Synthetic patient attributes:**
  - `randomTrue(prevalence)` flags;
  - truncated normals `normal(0, 250, mean, sd)`;
  - plain `normal(sd, mean)`;
  - `roundToInt(poisson(...))` and `roundToInt(exponential(1.11, 0))`.
- **Pypeline calls** (Help 8.9.10, *Pypeline*):
  - `run(String... lines)` for set-up statements;
  - `runResults(Class<T>, code)` returns a typed value;
  - `run(fmt, args...)` passes AnyLogic values into `%s` placeholders;
  - `runFileHeadless(...)` runs a script in parallel and returns a `FutureAttempt`.
- **Time in system:** at the `Sink`, `time(DAY) - toTimeUnits(agent.getFlowchartEntryTime(), DAY)`. `getFlowchartEntryTime()` is the time the agent entered the first block and returns NaN before that (Help *Agent API*). No TimeMeasure pair is needed.

## KPIs instrumented
Histograms of predicted LOS and of time in system (days); time plots of the arrival rate, beds taken and patients waiting; a bed-capacity slider for what-if runs.

## Pitfalls
- **Point predictions remove variance.** A regressor returns something like a conditional mean. Used directly as the service time, it drops the residual spread, so bed blocking and waits come out too low. Add noise drawn from the model's validation residuals, or predict a distribution *(modelling judgement)*.
- **The forecaster feeds on itself.** After the first day it forecasts from its own outputs, so arrivals follow the network's closed-loop pattern rather than data. The six seed values come from NumPy's **unseeded** generator, so runs cannot be reproduced even with a fixed AnyLogic seed (G17). Seed NumPy from AnyLogic *before* the predictor is created, e.g. `pyCom.run("import numpy; numpy.random.seed(%s)", seed)` *(suggested)*.
- **The start date is set to today** in *Before simulation run*, a wall-clock dependency. It is harmless here (only the clock colours use the hour), but date-driven logic would change from day to day.
- **Encoding mismatches fail silently.** Feature order, scaling and 0/1 coding (here `isMale ? 0 : 1`) must match the training pipeline exactly; a wrong order still returns a plausible number. Test `getArrayStr()` against rows the training code has already scored.
- **Units.** The Delay's unit is DAY while the model runs in hours, so the network must output days.
- **Environment.** Python must be on PATH, and the Microsoft Store Python is not supported (Help). The model pins old numpy/TensorFlow versions (`requirements.txt`).
- **Latency.** Each patient costs one round trip to Python. That is fine at this scale; for big experiments batch the predictions or precompute them *(unverified magnitude)*.

## Reusable idea
Wrap the trained models in one Python class, create it once per run, and call it at the exact point where AnyLogic consumes the prediction: an event for time-varying rates, a delay-time field for durations. This tests the predictors in the loop. Capacity and waiting KPIs show how the model's errors play out in operations, which a static test-set score cannot show.

## When the co-pilot should use this
- **Use cases:** a user asks "can I plug my ML model into AnyLogic?"; evaluating ML forecasts or policies in a digital twin; bed or capacity planning driven by patient-level LOS models.
- **Label ML outputs clearly.** Keep ML-driven inputs labelled as forecasts beside the simulated baseline (`videos/oee-instrumentation-in-des.md`).
- **Related cards:** `basicmodels/basic-functionality-interactive.md` (Pypeline basics), `models/lorenz-weather-model-pypeline.md`, and `models/supply-chain-optimizer.md`.
