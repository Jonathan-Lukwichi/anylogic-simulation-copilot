# Pattern card — Epidemic and Clinic with Accumulating Concern
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD + DES)
- **Problem it solves:** Models how individual patients decide to seek clinic treatment based on a privately accumulated concern level, and how clinic capacity shapes subsequent epidemic waves.

## Block chain
Each patient is an agent carrying a Susceptible → Infectious → Recovered statechart. While infectious, a System Dynamics stock called Concern grows continuously inside the agent. When Concern exceeds a threshold of 300, the patient self-refers to the clinic — an independent DES flowchart at the top level built from Queue → Delay → Exit blocks. Treatment duration follows a triangular(5, 20, 12) day distribution. After treatment the agent's Concern resets to zero and it transitions to Recovered. Immunity duration before returning to Susceptible is drawn from uniform(ImmunityMin, 30) days. The infection itself spreads via a rate-triggered transition driven by contact between agents. The top-level Main wires the ABM population to the DES clinic: agents enter via an Enter block, flow through Queue and Delay (the treatment step), and leave via an Exit block. Clinic capacity is a slider-controlled parameter; low capacity means the queue grows, patients remain infectious longer, and secondary epidemic waves emerge.

## Resources
- Clinic treatment slots: `Treatment.capacity` (integer, user-controlled slider)
- Patient population: `patients` agent population (size controlled by `population` parameter)
- Per-agent SD stock: `Concern` (continuous accumulator, resets on recovery)

## Key settings worth copying
- Concern threshold for self-referral: `Concern > 300`
- Treatment duration: `triangular(5.0, 20.0, 12.0)` days
- Post-recovery immunity window: `uniform(ImmunityMin, 30.0)` days (ImmunityMin is a slider)
- Infection spread: rate-triggered statechart transition (contact-rate style)
- Time unit: Day
- Cross-paradigm messaging: `send("TreatmentStarted", agent)` and `send("Treated", agent)` link DES clinic back to individual agent statechart

## KPIs instrumented
- **Total Concern** — sum of `item.Concern` across all agents (`patients.TotalConcern()`)
- **Total Concern by days** — time-series plot of aggregate concern accumulation
- **Clinic queue length** — implicit from Queue block content
- **Epidemic wave count** — observable from Susceptible/Infectious/Recovered population plots over time

## Reusable idea
Embed a SD stock *inside* each agent to accumulate a latent pressure variable (concern, fatigue, urgency), then use a threshold condition on that stock to trigger discrete actions (seek help, escalate, abandon) — this bridges continuous within-agent dynamics to discrete system-level service processes without polling or scheduled events.
