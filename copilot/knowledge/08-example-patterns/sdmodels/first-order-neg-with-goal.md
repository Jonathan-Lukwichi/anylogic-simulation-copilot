# Pattern card — First Order Neg with Goal
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a system state exponentially approaches a desired goal through a negative-feedback correction loop, converted from a classic Vensim reference model.

## Block chain
Single stock `SStateOfTheSystem` accumulates `NetInflowRate`. The flow rate equals `Discrepancy / AdjustmentTime`, where `Discrepancy` is the gap between the constant goal (`S_DesiredStateOfTheSystem = 100`) and the current stock level. As the stock rises toward the goal, the discrepancy shrinks and the inflow tapers — producing the classic S-shaped / exponential-approach curve.

```
[Cloud] --> (NetInflowRate) --> [SStateOfTheSystem]
                ^
                |  Discrepancy_S__S_ / ATAdjustmentTime
                |
         S_DesiredStateOfTheSystem - SStateOfTheSystem
```

The negative polarity on the discrepancy-to-flow link closes the loop and ensures goal-seeking behaviour.

## Resources
n/a — pure SD; no agent populations or resource pools.

## Key settings worth copying
| Parameter | Value | Meaning |
|---|---|---|
| `InitialStateOfTheSystem` | 0 | Stock starts empty |
| `S_DesiredStateOfTheSystem` | 100 | Constant goal/target |
| `ATAdjustmentTime` | 20 Days | Time constant — controls how fast the gap closes (63 % closed at t = 20 days) |
| Time unit | Day | Simulation clock unit |
| Flow formula | `Discrepancy / ATAdjustmentTime` | First-order linear correction |

The adjustment time is the key lever: halving it doubles the correction speed; doubling it slows convergence proportionally.

## KPIs instrumented
- Stock level `SStateOfTheSystem` over time (plotted as an exponential-approach curve)
- Implied: discrepancy (gap to goal) shrinking to zero; convergence time relative to `ATAdjustmentTime`

## Reusable idea
The **first-order negative-feedback archetype** is the universal building block for any goal-seeking process (inventory replenishment, workforce hiring, budget correction, temperature regulation). Parameterise it with your own stock name, goal value, and adjustment time, and you instantly get a calibrated convergence model without writing equations from scratch.
