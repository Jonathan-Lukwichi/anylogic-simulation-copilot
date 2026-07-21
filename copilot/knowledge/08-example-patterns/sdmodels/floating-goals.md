# Pattern card — Floating Goals
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Demonstrates how allowing goals to erode toward actual performance creates a self-defeating feedback loop — the "floating goals" or "eroding goals" archetype from Sterman's business dynamics framework.

## Block chain
Two coupled stocks drive the model:

1. **DesiredStateOfSystem** (goal stock) — initialized to an exogenous target. Its flow `NetChangeInDesiredState` pulls the goal toward the current actual state at a rate proportional to the gap between them, divided by `GoalAdjustmentTime`. When performance is low, the goal drifts downward over time.

2. **StateOfTheSystem** (performance stock) — initialized to a separate exogenous starting level. Its flow `NetChangeInState` closes the gap between the current desired state and actual performance, divided by `StateAdjustmentTime`. This is a standard first-order goal-seeking loop.

The two loops interact: poor performance lowers the goal, a lower goal reduces corrective pressure, which sustains poor performance — a reinforcing spiral of decline even though each individual loop looks like negative feedback.

## Resources
n/a — pure stock-and-flow model, no agents or queues.

## Key settings worth copying
- **GoalAdjustmentTime** (weeks): controls how quickly the goal drifts to match reality; shorter = faster goal erosion.
- **StateAdjustmentTime** (weeks): controls how quickly performance responds to the current goal; longer = sluggish correction.
- **InitialDesiredStateOfSystem**: the aspirational starting target.
- **InitialStateOfSystem**: the starting performance level (set below target to trigger the dynamic); exposed as a slider for interactive experimentation.
- **Time unit:** Week — appropriate for mid-term organizational or process performance scenarios.
- No stochastic distributions; the model is fully deterministic, making the archetype cleanly visible.

## KPIs instrumented
- Time-series plot of **DesiredStateOfSystem** vs **StateOfTheSystem** on the same axes — visually shows the two curves converging downward instead of the actual state rising to meet a stable goal.

## Reusable idea
When modelling any improvement program, quality target, or service-level objective, add a second stock for the goal itself and connect actual performance back to it with a slow adjustment flow. This instantly reveals whether the system has a structural tendency toward goal erosion — a common failure mode in continuous-improvement initiatives, safety standards, and performance management that is invisible without the explicit goal-drift loop.
