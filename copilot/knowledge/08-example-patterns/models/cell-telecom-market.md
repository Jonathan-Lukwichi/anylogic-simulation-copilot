# Pattern card — Cell Telecom Market
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Model competitive subscriber dynamics in a mobile telecom market where age-heterogeneous agents adopt, churn, or switch operators based on pricing and service mix.

## Block chain
Each person enters the simulation as an **Addressable Market** prospect — a potential subscriber who has not yet chosen a carrier. A monthly probability (shaped by the agent's age) governs conversion into a **Mobile User**. Once subscribed, the agent's statechart tracks whether they are on *our* operator or a *competing* operator. A separate branch handles churn entirely out of the market (final state). Transitions between operator states fire on a timeout trigger calibrated monthly; the guard condition compares a normalised price-aggression difference between operators, so a more aggressive competitor raises the switch probability. Agents generate revenue each month through two service types — **Voice calls** (length in minutes varies by age and is further scaled by a price-sensitivity coefficient) and **VAS** (value-added services, priced per request by age band). Model time unit is **Month**.

## Resources
- `clients` — agent population of type `Client`, each carrying its own statechart
- Two competing operator strategies (ours vs. other) parameterised via interactive controls
- Age-distribution table for seeding new entrants into the Addressable pool
- Market growth rate slider that controls the inflow rate of new Addressable agents

## Key settings worth copying
- **Time unit:** Month — align all rate parameters and timeout durations accordingly
- **Adoption probability:** age-dependent lookup table (not a fixed rate); wire it to a `condition`-triggered transition
- **Churn / switch probability:** normalised difference of (our price × aggression) vs. (competitor price × aggression), clamped 0–1, used as a `timeout`-trigger probability
- **Voice call length:** age-lookup multiplied by a price-elasticity coefficient — a clean way to model demand response without a separate DES queue
- **VAS requests per day:** age-lookup table → multiply by days-in-month to get monthly revenue contribution

## KPIs instrumented
- **ARPU Voice** (`ARPUVoice`): total voice revenue / number of our subscribers
- **ARPU VAS** (`ARPUVAS`): total VAS revenue / number of our subscribers
- **Market share**: count of agents in `OUR_USER` state vs. total active subscribers
- **Revenue** aggregated across all Client agents each month

## Reusable idea
Use a **three-state agent statechart** (Addressable → [OurUser | OtherUser] → Final) with age-indexed lookup tables driving both transition probabilities and usage quantities. This separates heterogeneity (age) from competitive dynamics (price/aggression difference) cleanly, letting you swap in any demand or churn function without restructuring the statechart topology.
