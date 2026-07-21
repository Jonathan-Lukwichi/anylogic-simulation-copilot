# Pattern card — HIV Diffusion and Syringe Usage
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Models HIV transmission through shared needle use in a drug-user social network, letting analysts test the effect of safe-syringe adoption rates on infection spread.

## Block chain
The model hosts a population of intravenous drug users (IDUser agents) scattered randomly across a city map. Each agent carries two concurrent statecharts: one governing drug-use behaviour (alternating between Idle and InjectingActivity) and one tracking health state (Susceptible or Infected). A subset of agents play the role of session organiser: when their DrugUsageBehavior statechart enters InjectingActivity they broadcast an invitation message to all connected peers, pulling them into a shared injection event. During that event, if any participant is HIV-positive and uses an unsafe syringe, susceptible participants who also share an unsafe syringe can become infected. The social network is built from bidirectional AgentLink collections; each IDUser maintains roughly 2–5 connections depending on whether they act as organiser or participant. The model time unit is days, and session timing is driven by a discrete-uniform interval of 1–3 days offset by a few hours.

## Resources
- Agent population: IDUsers (configurable count, default visible on dashboard)
- Two agent types: IDUser (participant) and a specialised organiser sub-role within IDUser
- Network links: bidirectional collection-of-links, ~5 connections per organiser, ~2 per regular user
- No server/queue resources; infection risk is purely contact-network driven

## Key settings worth copying
- `SafeSyringeUsersFraction` — slider parameter (0–1) controlling the fraction initialised with `randomTrue(SafeSyringeUsersFraction)`; the single most impactful policy lever
- `PercentInitiallyInfected` — seeds the starting HIV-positive count
- `MeanHIVLifeDuration` — governs the rate transition out of the Infected state (rate trigger, per-day units)
- Session interval: `uniform_discr(1, 3) * day() - 5 * hour()` — stochastic meeting cadence
- Statechart triggers mix timeout (self-paced behaviour) and message (peer invitation) transitions
- Time unit: Day

## KPIs instrumented
- Live count of Susceptible vs Infected users (time-series chart updated each step)
- Distribution-of-experience histograms split by HIV status (SusceptibleH / InfectedH histograms)
- `IDUsers.NInfected()` and `IDUsers.NSusceptible()` aggregated counts displayed on dashboard

## Reusable idea
Encode a policy intervention as a single fractional parameter (here, safe-syringe uptake) that is assigned once at initialisation via `randomTrue(fraction)` on each agent, then let the network and statecharts do the rest — this clean separation makes sweeping the policy lever across scenarios trivial without touching any behavioural logic.
