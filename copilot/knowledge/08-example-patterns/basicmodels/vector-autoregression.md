# Pattern card — Vector Autoregression
- **Source:** AnyLogic example model "Vector Autoregression" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (stochastic input process in discrete time)
- **Problem it solves:** Generate several input series that move together over time — each driven by its own and the others' recent values — instead of drawing each input independently.

## Structure
- A VAR(p) process of `size` variables and order `order` (demo: 3 and 2):
  **Y(t) = C + A₁·Y(t−1) + … + Aₚ·Y(t−p) + E(t)**.
- Plain Java arrays on Main: history `Y[order+1][size]` (`Y[0]` = now, `Y[k]` = k steps ago), intercepts `C[size]`,
  coefficient matrices `A[order][size][size]` (`A[k-1]` multiplies the values k steps back), errors `ER[size]`.
- Helper functions `times(a, y)` (matrix × vector) and `plus(v1, v2)` (vector sum).
- A cyclic event `step` (every 1 time unit): draw a new error vector, shift the history back by one step, compute
  `Y[0]` from C, the lagged terms and the errors. On startup C and all A entries are drawn at random (demo only).
- Other events and continuous equations can run between the steps; the VAR only changes at step times.

## Resources
n/a

## Key settings worth copying
- Make `size` and `order` parameters and size the arrays from them in their initial values, so one model handles any
  VAR dimension.
- Shift by re-pointing rows (`Y[t] = Y[t-1]` from the oldest down) and give `Y[0]` a fresh array each step; nothing
  needs copying element by element.
- Expose the current values (`Y[0][i]`) through functions or plots; other model parts read them as time-varying inputs
  (demand per product, prices, arrival-rate multipliers).

## KPIs instrumented
Time plot of the series.

## Pitfalls
- **Stability:** random coefficients can make the process explode. A VAR is stable when every eigenvalue of its
  companion matrix lies inside the unit circle — check fitted or chosen coefficients before use.
- **Errors are independent here** (`uniform(-0.1, 0.1)` per series), so series are linked only through lags. Real data
  usually also has same-period correlation: draw errors from a multivariate normal with the fitted residual covariance
  (Cholesky factor times independent normals).
- **Start-up transient:** the history starts at zero; discard early steps or seed the history from data.
- Values can go negative; for demands or prices model logs or clip, and document it.
- The step allocates new arrays every time; for long runs with large `size`, reuse buffers (the model's own note).

## Reusable idea
When inputs are cross-correlated over time (demand across related SKUs, energy price and load, arrivals at linked
sites), fit a VAR offline (e.g. Python `statsmodels` VAR), paste the coefficients and residual covariance into arrays,
and step the process with a cyclic event at the data's time resolution. Independent distributions per input would
understate joint peaks.

## When the co-pilot should use this
Correlated demand streams, scenario generation for supply-chain or energy models, and any input-modelling discussion
where the user's inputs co-move. Related: `../sdmodels/pink-noise.md` (single autocorrelated series),
`../../02-statistics-input-modeling/README.md` (fitting inputs).
