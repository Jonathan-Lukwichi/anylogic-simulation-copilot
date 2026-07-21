# Pattern card — Network Effect
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how two competing products gain or lose market share when a growing installed base makes a product increasingly attractive to new buyers (positive feedback / lock-in dynamics).

## Block chain
Two stock-and-flow chains run in parallel, one per product:

InstalledBase (stock) ← Sales (flow) driven by TotalDemand × MarketShare

MarketShare for each product = its Attractiveness / TotalAttractiveness

Attractiveness = EffectOfCompatibility × EffectOfOtherFactors

EffectOfCompatibility = exp( Sensitivity × InstalledBase / Threshold )

The exponential compatibility term creates the self-reinforcing loop: a larger installed base raises attractiveness, which raises market share, which raises sales, which grows the installed base further.

## Resources
n/a — pure SD; no agent populations or queue resources. TotalDemand is a constant (1 million units/year) representing the exogenous market size that both products compete for.

## Key settings worth copying
- **Compatibility effect formula:** `exp( SensitivityOfAttractivenessToInstalledBase * InstalledBase / ThresholdForCompatibilityEffects )` — the sensitivity parameter is a slider for sensitivity analysis; the threshold scales the inflection point of the S-curve.
- **Noise on attractiveness:** `normal(0, 4, 1, StandardDeviation, NoiseSeed)` applied each time step via a scheduled event, injecting stochastic variation into each product's exogenous attractiveness factor. Two independent seeds allow controlled comparison runs.
- **Time unit:** Day (converted from a Vensim original).
- **Initial installed base:** separate parameters for each product, allowing asymmetric starting conditions to explore first-mover advantages.

## KPIs instrumented
- Market share trajectory for Product 1 and Product 2 over time
- Installed base levels (stocks) for each product
- Attractiveness values and the compatibility multiplier (visible as auxiliary variables for diagnosis)

## Reusable idea
Wrap any "bigger-is-better" feedback loop inside a single exponential compatibility multiplier whose strength is governed by one sensitivity slider. This decouples the structural loop from its intensity, making sensitivity analysis (and teaching) trivial: set sensitivity to zero and the network effect vanishes; increase it to watch winner-take-all dynamics emerge from identical starting conditions.
