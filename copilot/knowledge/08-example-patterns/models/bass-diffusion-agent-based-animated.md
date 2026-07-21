# Pattern card — Bass Diffusion Agent Based Animated
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Models how a product or innovation spreads through a spatially distributed population driven by both advertising exposure and peer-to-peer contact.

## Block chain
Each person is an independent agent carrying a two-state statechart: **PotentialAdopter** → **Adopter**. Transition out of PotentialAdopter can happen via two competing mechanisms: (1) a global advertising effect that acts on every non-adopter at each tick, and (2) local word-of-mouth — an agent scans neighbours within a fixed geographic range and, upon contacting an Adopter, converts with a given adoption fraction probability. Once an agent enters the Adopter state it stays there; a flag (`adAdopter`) distinguishes ad-driven adopters from peer-driven ones for colour-coded animation. The Main agent holds the full population collection (`people`) and aggregates headcounts via filtered `count` statistics (`potentialAdopters`, `adopters`).

## Resources
- **Agent population:** `people` — a collection of `Person` agents placed at random geographic coordinates on a 2-D canvas.
- No resource pools, queues, or service blocks; the model contains no DES process library elements.

## Key settings worth copying
- **`adoptionFraction`** — probability that a susceptible agent converts upon contacting an adopter neighbour (slider-controlled at runtime).
- **`contactRate`** — rate at which each potential adopter attempts to contact neighbours (rate-triggered transition, time unit: Month).
- **Neighbour range** — spatial radius used to filter the `people` collection when searching for nearby adopters; controls the locality of word-of-mouth spread.
- Statechart transitions use `rate`-type triggers, making adoption speed proportional to the fraction of current non-adopters who meet an influencing condition each month.
- Agent colour encodes state visually: neutral (PotentialAdopter), dark-violet (ad-driven Adopter), dark-orange (peer-driven Adopter).

## KPIs instrumented
- **Potential Adopters count** — tracked via `dsPotentialAdopters` dataset and live chart.
- **Adopters count** — tracked via `dsAdopters` dataset and live chart.
- **Total population** — static parameter displayed on the dashboard.
- **Adopters amount** — dynamic label showing current cumulative adopters.
- Adoption fraction and contact rate are displayed as live parameter readouts.

## Reusable idea
Split a single state-transition into two independent rate-based triggers — one global (broadcasting/advertising) and one local (proximity search among neighbours) — then colour-code agents by which trigger fired. This makes the relative contribution of mass-media versus word-of-mouth immediately visible in the animation without any extra instrumentation code.
