# Pattern card — Nonlinear Polya Process
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Demonstrates how early random chance creates lock-in via positive feedback — the classic path-dependence phenomenon (Polya urn) extended with a nonlinear probability function.

## Block chain
Two Stock variables accumulate the count of black and white stones in the jar. Each time step an event fires, draws a single uniform(0,1) random number, and compares it against the current probability of choosing each color. The result gates two Flow variables (one per color) that add either 0 or StonesAddedPerPeriod stones to the corresponding stock. The selection probability for each color is not simply its proportion; instead an exponential function warps the proportion, amplifying the advantage of whichever color is already ahead. Two Auxiliary variables track the running proportions, and a Nonlinearity parameter controls how steeply the exponential curve bends.

## Resources
n/a — no agents, queues, or resource pools; the model is purely stock-and-flow with a stochastic event trigger.

## Key settings worth copying
- **Time unit:** Day; one stone added per period (StonesAddedPerPeriod = 1 by default).
- **Random draw:** `uniform(0, 1)` evaluated at every time step via a cyclic event.
- **Nonlinear probability:** `exp(Nonlinearity * proportion)` normalized over both colors — increasing Nonlinearity sharpens path-dependence.
- **Initial conditions:** one black stone and one white stone, giving an unbiased start.
- **Flow guard:** `RandomDraw <= ProbabilityOfChoosingABlackStone ? 1 : 0` (mirrored for white) keeps flows integer-valued each step.
- **Converted from:** Vensim NONLINEA1.mdl (imported via AnyLogic's Vensim import feature).

## KPIs instrumented
- Proportion of black stones and proportion of white stones over time (time-series charts showing convergence to one color).
- Absolute stock counts of black and white stones.
- RandomDraw value plotted each step to show the stochastic forcing.

## Reusable idea
Embed a **nonlinear reinforcement function** (exponential of proportion) inside an SD flow guard to model market lock-in, technology adoption tipping points, or brand dominance: once one option gains a lead the exponential term accelerates its growth, but the exact winner is determined by early random fluctuations — making each run a unique path-dependent trajectory.
