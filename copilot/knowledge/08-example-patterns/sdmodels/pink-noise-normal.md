# Pattern card — Pink Noise Normal
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Generates first-order autocorrelated (pink) noise from normally distributed white noise, providing realistic stochastic variation for SD models rather than purely random white noise.

## Block chain
A normally distributed random draw (`WhiteNoise_random`) is produced each time step using a seeded `normal()` call. That raw draw is scaled into a `WhiteNoise` auxiliary that respects the desired mean and standard deviation while compensating for the time-step size. A single Stock (`PinkNoise`) is smoothed toward the white noise input through a Flow (`ChangeInPinkNoise`) governed by a first-order exponential smoothing equation: `(WhiteNoise − PinkNoise) / CorrelationTime`. The result is noise that drifts gradually rather than jumping independently each step.

## Resources
n/a — no agent populations or resource pools; purely equation-driven SD structure.

## Key settings worth copying
- `NoiseSeed` (integer parameter): controls the random sequence; identical seeds reproduce identical noise series, enabling controlled comparisons across runs.
- `CorrelationTime` (auxiliary, units: Day): the lag constant of the first-order smooth — longer values produce slower-drifting noise.
- `Mean` (auxiliary): shifts the entire noise process to any desired centre value.
- `StandardDeviation` (parameter, default exposed in experiment): scales the spread of the resulting pink noise output.
- White noise scaling formula: `Mean + sqrt((SD² × (2 − DT/CT)) / (DT/CT)) × WhiteNoise_random` — compensates so output SD equals the user-specified value regardless of time step.
- `ModelTimeUnit`: Day (converted from original Vensim PINKNOIS1.mdl).

## KPIs instrumented
- Time plot of `PinkNoise` stock value over the simulation horizon (visual inspection of autocorrelated drift pattern).

## Reusable idea
Wrap any white-noise draw in a one-stock first-order smoother to turn it into pink noise; expose `CorrelationTime` and `NoiseSeed` as parameters so downstream SD models can inject realistic, reproducible, autocorrelated demand or environmental variation without external data.
