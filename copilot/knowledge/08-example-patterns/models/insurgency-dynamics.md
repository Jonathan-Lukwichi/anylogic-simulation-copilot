# Pattern card — Insurgency Dynamics
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (SD + ABM side-by-side comparison)
- **Problem it solves:** Models how a government-supporting population gradually radicalises into dissidents and insurgents through social contagion, and compares aggregate SD results against individual-level ABM results.

## Block chain

The model runs two parallel sub-models that answer the same question with different fidelity levels.

**SD sub-model:** Four stocks track population cohorts — Government_Supporters, Dissidents, Insurgents, and Removed_Insurgents. A Birth flow continuously adds people to the supporter stock. Three inter-stock flows govern radicalization: Becoming_Dissident (supporters converted by propaganda), Insurgent_Recruitment (dissidents escalating), and Removing_Insurgents (government suppression). A fifth stock, Perceived_Intensity_of_Anti_Regime_Messages, acts as a message-buffer between active insurgents and the social network, smoothing the recruitment signal.

**ABM sub-model:** Each person is one agent carrying a statechart with four states mirroring the SD stocks. Active dissidents and insurgents broadcast messages at ContactRate. A Government_Supporter who receives a message switches to Dissident with probability Propensity_to_be_Recruited. Dissidents relax back to supporter via a rate scaled by Appeasement_Fraction and Avg_Time_as_Dissident, or escalate to Insurgent via a separate rate. Government removal is modelled as agent deletion (abs(normal(…)) delay around Desired_Time_to_Remove_Insurgents).

A comparison dashboard plots the percentage difference between SD and ABM counts for each cohort over time, letting the user see where aggregate assumptions diverge from emergent individual behaviour.

## Resources

- **SD stocks:** Government_Supporters, Dissidents, Insurgents, Removed_Insurgents, Perceived_Intensity_of_Anti_Regime_Messages
- **ABM population:** `people` — Person agents, each with an embedded statechart
- **No capacity pools or queues** — movement between states is rate-driven, not resource-constrained

## Key settings worth copying

| Parameter | Role |
|---|---|
| `ContactRate` | Messages sent per active opponent per day |
| `AdoptionFraction` | Fraction of contacts that actually deliver a message |
| `Propensity_to_be_Recruited` | Probability a supporter accepts the message |
| `Appeasement_Fraction` | Government policy lever reducing dissident persistence |
| `Avg_Time_as_Dissident` (days) | Mean dwell time before relaxation or escalation |
| `Desired_Time_to_Remove_Insurgents` (days) | Mean suppression delay; sampled as `abs(normal(mean, mean))` |
| `People_Birth` | Constant inflow rate to supporter stock |
| `Initial_Government_Supporters / Initial_Dissident / Initial_Insurgent` | Scenario seeds |
| Time unit: **Day** | |
| Agent placement: `uniform(x_min, x_max)` spatial scatter | |

Recruitment rate formula (SD): `(Propensity_to_be_Recruited × Supporters × Opponents × ContactRate) / (Opponents + Supporters)`

## KPIs instrumented

- Population counts per cohort over time (both models)
- Percentage divergence between SD and ABM cohort sizes
- Active insurgent count
- Removed insurgent cumulative total

## Reusable idea

Run the same conceptual model as both SD (stocks/flows) and ABM (statechart agents) simultaneously, then display the delta between them. This dual-paradigm validation pattern is directly transferable to any epidemic, adoption, or opinion-spread scenario: the SD version is fast and analytically tractable; the ABM version captures stochastic variance and individual heterogeneity. Comparing the two in a single dashboard tells you when the mean-field assumption is safe and when individual-level detail actually changes the answer.
