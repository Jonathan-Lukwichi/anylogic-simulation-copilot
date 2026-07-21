# Pattern card — Air Defense System
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Evaluates how well a radar-and-missile defense network protects ground assets against an incoming stream of hostile aircraft dropping bombs.

## Block chain
Hostile aircraft spawn at a configurable rate and fly across the 3-D terrain toward defended ground assets. Each aircraft follows a statechart that governs its flight, bomb-drop decision, and destruction sequence. Radar agents continuously scan a circular coverage zone; when an aircraft enters that zone the radar selects and fires a missile agent. Missile agents home in on their assigned target and detonate on contact. Ground assets each run their own statechart tracking intact vs. destroyed state. The model time unit is Days, but the fast event cadence (rate-triggered transitions) makes effective resolution sub-minute.

## Resources
- **Radar agents** — each carries a configurable `maxMissiles` capacity (slider: "Radar max missiles")
- **Aircraft population** — size driven by "Aircraft intensity" (arrivals per day)
- **Asset population** — ground targets placed at uniform random positions within a bounded zone (x in [400,600], y in [200,400])

## Key settings worth copying
- Aircraft arrival: rate trigger, intensity controlled by slider (aircraft/day)
- Aircraft altitude: `uniform(max(0, baseZ-5), baseZ+5)` — adds realistic altitude scatter
- Asset initial position: `uniform(400,600)` × `uniform(200,400)` — random scatter within defended area
- Radar scan interval: `uniform(0.5, 2)` days — randomised polling avoids lock-step artefacts
- Target selection inside radar: `uniform_discr(0, nalive-1)` — picks a random live aircraft from those in range
- Missile and aircraft speeds are independent sliders, letting the user tune intercept probability without code changes

## KPIs instrumented
- Assets destroyed vs. surviving (statechart state counts)
- Aircraft shot down vs. reaching target (implicit from statechart exit transitions)
- Missiles fired per radar (derivable from missile agent population events)

## Reusable idea
**Randomised radar polling with uniform scan intervals** (`uniform(0.5, 2)`) prevents all radars from sampling simultaneously, which would create artificial burst behaviour; applying a small uniform jitter to any periodic sensing or inspection agent in an ABM avoids synchronisation artefacts at negligible modelling cost.
