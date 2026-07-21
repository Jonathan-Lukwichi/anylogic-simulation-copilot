# Pattern card — Pink Noise
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Generates realistic first-order autocorrelated noise (pink noise) from a simple uniform white-noise input, producing output that is asymptotically normal and controllable via mean, standard deviation, and correlation time.

## Block chain
1. **WhiteNoise_random** — an auxiliary variable that draws a fresh `uniform(-0.5, 0.5)` sample every time step (seeded by `NoiseSeed` for reproducibility).
2. **WhiteNoise** — scales and shifts the raw sample: `Mean + StandardDeviation × sqrt(24 × CorrelationTime / TIME_STEP) × WhiteNoise_random`. This pre-scales the white noise so the resulting pink noise lands at the user-specified standard deviation.
3. **PinkNoise** (Stock) — initialized to `Mean`; accumulates `ChangeInPinkNoise` over time.
4. **ChangeInPinkNoise** (Flow) — first-order smoothing inflow: `(WhiteNoise − PinkNoise) / CorrelationTime`. This single-pole filter is what converts white noise into correlated (pink) noise.

Time unit: **Week**.

## Resources
n/a — pure SD signal-generation model; no agents, queues, or resource pools.

## Key settings worth copying
| Parameter | Role |
|---|---|
| `NoiseSeed` | Integer seed; identical seeds reproduce identical noise sequences across runs, enabling controlled comparisons |
| `CorrelationTime` (weeks) | Controls how "memory" the noise has — larger value = smoother, more persistent fluctuations |
| `Mean` | Long-run average the pink noise oscillates around |
| `StandardDeviation` | Desired spread of the pink noise output |
| `TIME_STEP` | Must be consistent with the model's week-based time unit; affects the scaling factor inside `WhiteNoise` |

The scaling formula `sqrt(24 × CorrelationTime / TIME_STEP)` ensures variance is independent of the chosen time step — a critical numerical detail.

## KPIs instrumented
- Time-series plot of `PinkNoise` vs. simulation time — visual inspection of autocorrelation and spread.
- Interactive slider for `StandardDeviation` allows real-time sensitivity exploration during a run.

## Reusable idea
**Seed-controlled, step-size-invariant pink noise via a one-stock SD structure.** Any SD model that needs realistic demand variability, environmental fluctuations, or market noise can embed this two-variable pattern (one auxiliary + one stock/flow pair) with its `NoiseSeed` parameter to produce repeatable yet stochastic inputs — without importing external time-series data.
