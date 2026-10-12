# Pattern card — SD numerical hygiene in AnyLogic: lookup edges, random draws, externally set inputs and the solver step
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 5 "System dynamics" — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Stock-and-flow models that go negative, divide by zero, depend on the integration step, ignore a slider, or settle somewhere other than the "capacity" the modeller typed in.

## Mechanism
Checked against Help 8.9.10 (*Table function*, *Dynamic variable*, *Numerical solvers for SD*, *delay*, *delay3*) and the
8.9.10 book models *Population and Carrying Capacity* and *Stock Management Game*.
1. **Lookup edges are a modelling decision.** A table function's *Out of range* options:

   | Option | Beyond the table it… |
   |---|---|
   | Error | raises a runtime error |
   | Nearest | holds the end value |
   | Repeating | repeats the table periodically |
   | Custom | returns a fixed value |
   | Extrapolate | continues the interpolation (with Linear, the slope of the end segment) |

   A declining effect curve set to Extrapolate crosses zero past its last point. That gives a negative lifetime or
   rate, or a division by zero. The book's crowding-on-lifetime table is safe only because its last two points are
   equal (0.01, 0.01) and its first segment is flat. For effect lookups, use Nearest, or end the table with flat
   segments. Keep any lookup used as a divisor above zero; the book stops at 0.01 for that reason (p. 21).
2. **Equilibrium comes from the effect curves, not the label.** With `CarryingCapacity` = 5,000, the population settles
   near 4,980 (p. 25). The level is where births equal deaths through both effect functions. If the equilibrium must
   hit a target, calibrate the curve shapes or make the goal an explicit part of the structure.
3. **No random functions inside SD formulas** (p. 11). A formula is recomputed at every solver step (fixed step 0.001
   in the book's 8.9.10 models), so the draw is resampled at that frequency. How much noise gets through then depends
   on the step and the integration method. Instead, sample once per period in an event and store the result in a
   Constant variable. The game's demand is a daily random walk: `Demand = max(0, Demand + uniform(-1, 1))`. The
   pink-noise structures in `sdmodels/` do the same.
4. **Anything set from outside must be Constant or a parameter.** A slider, button or event that assigns an ordinary
   dynamic variable is overwritten by its formula at the next evaluation (p. 47). A *Constant* variable has no
   re-evaluated formula (Help). The event side of this rule is also in
   `bigbook/event-modes-condition-monitoring-and-lifecycle.md`.
5. **The time unit and the solver step are different things.** The unit is the clock's scale; the step is the
   integrator's micro-step. In 8.9.10, the method and *Fixed time step* are set in the model's properties, section
   *System Dynamics solver*:
   - differential equations: Euler or RK4;
   - mixed equations: RK45 Newton or Euler Newton.

   The book's pointer to the experiment's Advanced section (p. 45) is outdated. To test the step, halve it; results
   should not move.
6. **Gate outflows by feasibility, not by sign.** `Stock > 0 ? Demand : 0` lets the stock undershoot zero within a
   step; the book plots `max(0, Stock)` to hide it (p. 46). Prefer `min(Demand, Stock / MinTimeToShip)`, the bounded
   form in `sdmodels/labor-w-layoffs.md` and `sdmodels/widgets-w-mat-inv.md`.
7. **Choose the delay form on purpose.**
   - `delay(x, T, x0)` shifts `x` by `T` and returns `x0` until then (a pipeline).
   - `delay3(x, T)` spreads the output (a third-order lag).
   - A delay inside a balancing loop produces overshoot and oscillation (p. 26).

## Resources
n/a

## Key settings worth copying
- Table function: *Interpolation* Linear, *Out of range* Nearest (or flat end segments).
- Noise: a Cyclic event every time unit writes a Constant dynamic variable.
- Model properties, *System Dynamics solver*: method, and *Fixed time step* below the fastest time constant.

## KPIs instrumented
n/a (verification). Face checks: no stock below zero, results stable when the step is halved, and equilibrium versus
the intended target.

## Pitfalls
- **A zero delay time behaves differently by function.** `delay3` returns NaN for a zero or negative delay time;
  `delay` returns its input unchanged (Help). Guard delay times that come from parameters or sliders.
- **Spline interpolation can overshoot** between table points, so an effect can leave its intended 0..1 range. Check
  the curve preview, or use Linear.
- **Models ported from Vensim:** compare each lookup's out-of-range behaviour with the original.

## Reusable idea
Treat every lookup edge, random draw and externally set value as a numerical design decision, and prove the model
with a step-halving run.

## When the co-pilot should use this
- Building or reviewing any AnyLogic SD model, especially one with effect lookups, noisy inputs or interactive controls.
- Symptoms: negative stocks, Infinity or NaN, a slider that does nothing, results that change with the step.
- Related: `sdmodels/pop-and-carrying-capacity.md`, `sdmodels/pink-noise.md`,
  `bigbook/sd-units-check-sectors-and-hierarchical-interfaces.md`.
