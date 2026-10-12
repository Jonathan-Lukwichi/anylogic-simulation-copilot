# Pattern card — Summary Statistics
- **Source:** AnyLogic example model "Summary Statistics" (sdmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Judge the historical fit of a model with more than one number: bias, variance mismatch and unsystematic error (Theil inequality statistics), plus RMSE, MAPE, R² and MAE ÷ mean, computed inside the SD model itself.

## Structure
A template converted from a Vensim model; its variable notes cite Sterman (1984). Two placeholders, `Historical` (the data, X) and `Simulated` (the model output, Y), are to be wired to the real series. Here they are constants 1 and 10.
- **Sample picker.** `Pick` is 1 only at data points: after `StartTime`, up to and including `EndTime`, and when `time()` is a whole multiple of `Interval`. It is built from two `step()` calls and an equality test on `time() / Interval`. `Xi = Pick * X` and `Yi = Pick * Y`.
- **Exact sums with stocks.** Each accumulator is a stock whose inflow is the sampled quantity divided by `Dt` (the fixed step, `TIME_STEP` = 0.25). With Euler, one step of `value / Dt` adds exactly `value`. This gives `Count`, `SumXi`, `SumYi`, `SumX2`, `SumY2`, `SumXY`, `SumAE`, `SumAPE` and `SumXmY2`.
- **Statistics (auxiliaries), all guarded with `zidz`:**
  - means `MX`, `MY`, `MX2`, `MY2`, `Mxy`;
  - standard deviations by the "hand" formula, `Sx = sqrt(MX2 - MX²)` and `Sy = sqrt(abs(MY2 - MY²))`;
  - correlation `R = (Mxy - MX·MY) / (Sx·Sy)` and `R_2 = R²`;
  - the three MSE components: `DifMea = (MX - MY)²`, `DifVar = (Sx - Sy)²`, `DifCov = 2·Sx·Sy·(1 - R)`;
  - `MSE` = their sum, `RMSE = sqrt(MSE)`;
  - **Theil shares** `Um = DifMea / MSE` (bias), `Us = DifVar / MSE` (unequal variation) and `Uc = DifCov / MSE` (unequal covariation), which sum to 1;
  - `MAPE = SumAPE / Count` and `MAEOverMean = (SumAE / Count) / MX`.
- **Solver:** Euler, fixed step 0.25, run 0–12 (checked in the `.alp`).

## Resources
n/a

## Key settings worth copying
- **Reading the decomposition** (standard SD validation practice).
  - A large **Um** means the model is offset from the data: check parameters and initial values.
  - A large **Us** means the amplitude or trend differs: check the structure, delays and gains.
  - Error concentrated in **Uc** is unsystematic point-by-point error. It is acceptable when the model's purpose is the pattern, not each point.
  - Always report RMSE or MAPE *together with* the shares; a small RMSE can hide a pure bias.
- **Self-check for free.** `SumXmY2 / Count` is the directly computed MSE. The model accumulates it but does not use it. Compare it with the decomposed `MSE`: a gap exposes cancellation error in the hand formulas.
- **In AnyLogic you can also compute these in a function** at the end of the run from a DataSet of model output and a table function of data. That avoids the step and equality issues below *(suggested)*. Unlike the point-by-point statistics here, `difference()` (Help *Calibration*) compares linearly interpolated curves over their overlapping range.

## KPIs instrumented
RMSE, MSE and its three components, Um / Us / Uc, R and R², MAPE, MAE ÷ mean, and the number of points used.

## Pitfalls
- **The picker needs exact time values.** `time()/Interval == (int)(time()/Interval)` works with a binary-exact step such as 0.25. With a step like 0.1, sample points can be missed *(floating-point reasoning; engine step alignment unverified)*. Keep the step a power-of-two fraction or use a tolerance (proposed gotcha in `.ingest/proposals/m-examples-2.md`).
- **The `/ Dt` sums assume Euler.** RK4 also evaluates flows at mid-step, so a one-step pulse is no longer added exactly once *(reasoned)*.
- **MAPE here divides by the simulated value** (`|Xi - Yi| / Yi`), while the usual MAPE divides by the data. Decide which one you report. Some of the model's variable notes also label x as "simulated" although x is the historical series.
- **`Sx` has no `abs()` guard.** For an almost constant data series, rounding can make `MX2 - MX²` slightly negative and `Sx` NaN; `Sy` is guarded.
- **Uc also absorbs timing errors.** A model that lags the data by a few periods lowers R and piles error into Uc. Plot `Residuals` over time before calling Uc noise *(reasoned)*.
- **Only in-range points count.** Data outside `StartTime`…`EndTime` and model output between data points are ignored by design.

## Reusable idea
Instrument any calibration or validation run with the full fit profile: bias, variance and covariance shares, plus scale-free errors (MAPE, MAE ÷ mean). Accumulate point sums exactly (stocks fed by value ÷ DT at sample instants, or a closing function over datasets), and keep a direct MSE as a check on the formulas.

## When the co-pilot should use this
- **Use cases:** a user asks whether a model "fits the history", compares calibrated parameter sets, or must document validation for a thesis or client. Report the Theil decomposition next to RMSE and MAPE.
- **Related cards:** `bigbookmodels/epidemic-model-various-experiments.md` (`difference()` calibration), `models/sir-agent-based-calibration.md` (stochastic fits) and `sdmodels/sir-model-threshold.md` (the same pulse idiom).
