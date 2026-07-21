# Pattern card — Action Oriented Problem Solving
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Captures how a decision-maker updates a working diagnosis under time pressure, revealing whether over-confidence (self-confirming bias) or indecision ("vagabonding") causes failure during clinical resuscitation training.

## Block chain
Three stocks drive the feedback loops. `ActionStepsCompleted` accumulates as the clinician executes protocol steps; the rate `TakeAction` pushes it toward 1.0 over `TimeNeededToTakeSteps` minutes. As more steps are completed, `CuesAvailable` slides from the initial plausibility toward 1.0 (if the leading diagnosis is correct) or stays low (if wrong), providing evidence that feeds back into `PlausibilityOfLeadingDiagnosis` via the `UpdateLeading` flow. A second reinforcing loop lets the trainee "cultivate" an alternative diagnosis: `PlausibilityOfAlternativeDiagnosis` grows through the `Cultivate` flow, but only when the leading diagnosis plausibility is low, creating a natural switching pressure. The auxiliary `WeightOnCues` — computed as `(1 - PlausibilityOfLeadingDiagnosis)^PlausibilityEffectOnCueInterpretation` — controls how open the clinician is to new evidence; high existing plausibility shrinks the weight, modelling confirmation bias mathematically. `AccuracyOfLeadingDiagnosis` is a Boolean-style auxiliary that equals 1 when `CurrentDiagnosis >= TrueDiagnosis`, injecting accuracy into the cue signal. Rather than modifying stocks through continuous flows only, the model demonstrates how AnyLogic condition-triggered events can update stocks directly, replacing the "change trigger divided by timestep" hack common in converted SD models.

## Resources
n/a — pure System Dynamics; no agents, queues, or resource pools.

## Key settings worth copying
- `InitialPlausibility` = 0.5 (starting belief; raise toward 1.0 to simulate over-confidence)
- `PlausibilityEffectOnCueInterpretation` = 0.5 (slider 0.1–0.9; higher values mean stronger confirmation bias)
- `TrueDiagnosis` = 4 (slider 4–10; the correct answer hidden from the trainee)
- `TimeNeededToTakeSteps` = 8 min, `TimeNeededToUpdate` = 2 min, `TimeNeededToCultivate` = 4 min
- Time unit: Minutes
- All three time parameters are exposed as slider/unit-editor controls for interactive scenario comparison

## KPIs instrumented
- `PlausibilityOfLeadingDiagnosis` (converges to 1 = correct; stays low = vagabonding)
- `ActionStepsCompleted` (completion fraction 0–1 within the session clock)
- `PlausibilityOfAlternativeDiagnosis` (rises when leading diagnosis stalls, signalling diagnosis switching)
- `AccuracyOfLeadingDiagnosis` (1 if the trainee has reached the true diagnosis, 0 otherwise)

## Reusable idea
Encode cognitive bias as a nonlinear weight on information uptake: `WeightOnCues = (1 - currentBelief)^biasExponent`. A low exponent (near 0) makes the weight nearly constant — the agent always listens. A high exponent (near 1) collapses the weight as belief rises — the agent stops listening once committed. Dropping this single auxiliary into any belief-update SD loop instantly parameterises a spectrum from fully Bayesian to fully dogmatic behaviour, making it directly applicable to any model of human decision-making under uncertainty (triage, fault diagnosis, quality inspection).
