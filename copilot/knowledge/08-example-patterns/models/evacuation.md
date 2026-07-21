# Pattern card — Evacuation
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Measure how long it takes to empty a multi-storey building when a fire alarm fires, and identify bottlenecks caused by stairwells, exits, and crowd density.

## Block chain
Two populations share the same floor plan: workers who arrive at a steady rate throughout the day, and visitors whose arrival is scaled by a multiplier parameter. Both populations go about normal activities (waiting in areas, receiving service at counters, moving between targets) until the alarm boolean flips to true. At that point every agent abandons its current task and routes toward the nearest staircase or exit via PedGoTo. PedChangeLevel handles floor transitions, funnelling everyone from the upper floor down before they reach a PedSink at the building exit. A SelectOutput block decides whether an agent heads to a primary or secondary exit; toggling the "Add exit" parameter opens a second exit door, letting users compare single- vs. dual-exit evacuation times. The variable evacTime captures the elapsed time between alarm start and the moment the last pedestrian exits.

## Resources
- Two pedestrian populations: workers (rate-driven, per hour) and visitors (multiplier-scaled)
- Two floors connected by staircases (PedChangeLevel blocks)
- One mandatory exit; one optional second exit toggled by the addExit boolean parameter
- Service counters (PedService) and waiting zones (PedWait) representing cafeteria and workstations

## Key settings worth copying
- `workerArrivalRate`: 60 per hour (PER_HOUR rate unit) — controls building occupancy at alarm time
- `visitorArrivalMultiplier`: default 2 — scales visitor load relative to workers
- `alarmTime`: default 540 minutes (slider 0–100 mapped to simulation time) — sets when the alarm fires
- `addExit`: boolean toggle — activates a second exit for comparative scenarios
- Model time unit: Minute; pedestrian speed: 10 m/s (configurable); floor scale: 1 m per pixel
- Space defined as a 500 × 500 unit floor with 100 × 100 grid and 2 connections per agent

## KPIs instrumented
- `evacTime` — total evacuation duration (alarmEnding minus alarmBegining, in seconds)
- `visitorCount` — live count of visitors still inside
- Implicit throughput visible via PedSink exit counts per exit node

## Reusable idea
Separate normal-operations flow from emergency flow using a single boolean flag (alarm). When the flag trips, every agent's PedSelectOutput condition re-evaluates and redirects toward exits — no need to destroy and recreate agents. This pattern cleanly reuses the same pedestrian population for both steady-state and emergency scenarios, making it straightforward to measure the gap between normal dwell time and evacuation time with minimal model restructuring.
