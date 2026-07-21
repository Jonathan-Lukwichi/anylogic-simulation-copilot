# Pattern card — Consumer Market
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Models how competing candy brands gain or lose market share as children influence each other's preferences through social contact, random switching, and relocation across towns.

## Block chain
A population of Kid agents is distributed across Town agents placed on a spatial canvas. Each kid carries two internal arrays — a memory vector and a preference vector — one slot per candy brand. On startup, memory is seeded with uniform-random values so initial brand allegiance is heterogeneous.

Three independent exponential-rate timers drive behaviour per kid:
1. **Contact event** — the kid picks a random neighbour in the same town and, if their favourite brand differs, delivers an InfluenceAction that temporarily boosts the neighbour's memory for that brand. The influence decays after a configurable promotion duration; only a fraction (`remainingInfluence`) persists in long-term memory.
2. **Relocation event** — the kid moves to a randomly chosen different town, carrying all memory intact. This spreads brand loyalty geographically.
3. **Accidental switch event** — the kid spontaneously picks a new brand at random, independent of social influence, modelling external shocks or advertising untracked by the model.

After any memory update the kid re-computes preferences by blending memory and current influence, weighting by `memoryWeight` / `influenceWeight`, then dividing by brand price. The kid switches favourite only when the leading brand's preference exceeds the current favourite by more than `switchDelta`, preventing jitter.

Market share at any instant is read off the live population distribution of `favoriteCandyType`.

## Resources
- Agent populations: Kid (N configurable), Town (N configurable)
- No capacity-constrained queues or resource pools — throughput is governed purely by event rates

## Key settings worth copying
- `contactRate` — exponential inter-contact time; tune to accelerate or dampen word-of-mouth spread
- `moveRate` — exponential inter-relocation time; controls geographic diffusion speed
- `accidentalSwitchRate` — exponential rate of brand defection independent of social influence
- `memoryWeight` / `influenceWeight` — blend ratio between long-term memory and active promotion effect
- `switchDelta` — minimum preference gap before a kid switches brand; raises inertia and stabilises equilibrium shares
- `price[]` per brand — divides preference, making cheaper brands more attractive all else equal
- `nCandyTypes` — number of competing brands; scales the memory and preference arrays
- Time unit: Day

## KPIs instrumented
- Market share per brand (fraction of kids whose `favoriteCandyType` equals each brand index)
- Contact volume and promotion duration effects on preference shift
- n/a — no explicit wait-time, utilisation, or cost KPIs; focus is on share dynamics over time

## Reusable idea
**Preference-as-weighted-memory blend with a switch threshold:** storing brand affinity as a normalised array rather than a single state variable lets you model gradual opinion drift driven by repeated social contact and price sensitivity, while `switchDelta` prevents the agent from flip-flopping on every minor fluctuation. This pattern transfers directly to any ABM where agents hold graded preferences across competing options (products, parties, routes) and switch only when conviction is strong enough.
