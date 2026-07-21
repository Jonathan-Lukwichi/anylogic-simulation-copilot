# Pattern card — SIR Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how an infectious disease spreads and subsides through a fixed population using three coupled stock-and-flow compartments.

## Block chain
Three stock variables represent the epidemiological compartments: **Susceptible (S)** → **Infectious (I)** → **Recovered/Removed (R)**. Two flows connect them: an *infection rate* drains S and fills I, while a *recovery rate* drains I and fills R. Population is conserved — total S + I + R remains constant throughout the simulation. The infection rate is driven by mass-action mixing: susceptible individuals encounter others at a fixed contact rate; the fraction of those contacts that are infectious, multiplied by disease infectivity, yields new infections per day. The recovery rate is simply I divided by the average infectious duration.

## Resources
n/a — no capacity-constrained resources; the model tracks population fractions, not service queues.

## Key settings worth copying
| Parameter | Value | Notes |
|---|---|---|
| Total population (N) | 10,000 | constant throughout run |
| Initial infectious (I₀) | 1 | single seed case |
| Contact rate (c) | 6 contacts/person/day | from Sterman reference model |
| Infectivity (i) | 0.25 | probability of transmission per contact |
| Infectious duration | 2 days | average time before recovery |
| Time unit | Day | |
| ODE solver | Euler (primary); RK45+Newton available | set in experiment |

Derived basic reproduction number R₀ = c × i × duration = 6 × 0.25 × 2 = **3.0** — well above epidemic threshold of 1.

## KPIs instrumented
- Peak infectious population (I_max) and day it occurs
- Cumulative recovered (final epidemic size)
- Time to epidemic peak
- Implied herd-immunity threshold (1 − 1/R₀ ≈ 67 %)

## Reusable idea
The transferable trick is **mass-action incidence**: infection rate = S × (I/N) × c × i. Dividing I by N converts absolute stock levels into a *prevalence fraction*, making the nonlinear feedback self-scaling regardless of population size. Drop this single formula into any SD model where one compartment "infects" another proportionally, and the classic epidemic S-curve emerges automatically.
