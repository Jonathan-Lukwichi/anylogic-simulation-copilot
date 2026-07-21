# Pattern card — Bass Diffusion Agent Based
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Simulates how a product or innovation spreads through a population driven by both advertising (external influence) and word-of-mouth (peer-to-peer contact).

## Block chain
Each of the 50,000 Person agents owns a two-state statechart: **PotentialAdopter** → **Adopter**. Two independent transition triggers drive adoption. The first is a rate-based trigger that fires from the PotentialAdopter state, representing the advertising (innovation) coefficient — every agent has a small constant probability per month of converting on their own after seeing an ad. The second trigger is a message: when an Adopter contacts another agent, it sends a message that pushes the recipient directly into the Adopter state, modelling word-of-mouth (imitation) effect. A fully connected network is assumed, so any Adopter can reach any PotentialAdopter. Main tracks two aggregate counts — `potentialAdopters` and `adopters` — by querying the agent population each month, producing the classic S-curve of cumulative adoption over time.

## Resources
- Agent population: up to 50,000 Person agents (configurable via UI slider)
- No service pools or queues — purely statechart-driven state transitions

## Key settings worth copying
- **Time unit:** Month; fixed time step 0.01 months for smooth rate transitions
- **Contact rate** parameter on Main controls how frequently Adopters reach out (imitation coefficient q)
- **Advertising rate** embedded as a rate trigger on PotentialAdopter state (innovation coefficient p)
- Population size slider (1–50,000) lets you trade fidelity for speed during experiments
- Two dataset series (`dsPotentialAdopters`, `dsAdopters`) sampled each month for chart replay

## KPIs instrumented
- Count of Potential Adopters over time
- Count of Adopters over time (cumulative S-curve)
- Chart: "Number of Potential Adopters and Adopters by Months" overlaying both series

## Reusable idea
Split peer influence from external influence using two separate statechart triggers on the same transition target: a **rate** trigger for broadcast/advertising effects and a **message** trigger for direct agent-to-agent contagion. This two-trigger pattern cleanly separates the Bass p (innovation) and q (imitation) coefficients inside a single statechart without needing any shared variables or complex condition checks.
