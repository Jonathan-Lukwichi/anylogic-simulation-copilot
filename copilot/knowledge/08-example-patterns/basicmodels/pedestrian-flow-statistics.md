# Pattern card — Pedestrian Flow Statistics
- **Source:** AnyLogic example model "Pedestrian Flow Statistics" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Measure pedestrian flow through cross-sections (corridor widths, doors, gates), per direction, as peds/hour and peds/(hour·metre).

## Block chain
Two counter-flows in one corridor: `PedSource` *sourceGreen* (1500/h, diameter `uniform(0.2, 0.3)` m) → `PedGoTo` blue line → `PedSink`, and `PedSource` *sourceBlue* (2000/h) → `PedGoTo` green line → `PedSink`. Three **Ped Flow Statistics** lines across the corridor: one counts only right-to-left, one only left-to-right, one both directions. Sliders are linked to each source's `rate`.

## Resources
n/a

## Key settings worth copying
- Ped Flow Statistics (Pedestrian Library → Space Markup): draw a line across the flow; *Direction* Left / Right / Both (`setDirection(FLOW_STATISTICS_LEFT | _RIGHT | _BOTH)` at run time); it counts on its own *Level* only.
- Functions (Help 8.9.10): `countPeds()` — total crossings since start; `traffic()` — peds/hour estimated from the **last five minutes** of model time (count × 12); `intensity()` — `traffic()` divided by the line length, peds/(hour·m); `reset()`.
- Plot `traffic()` and `intensity()` per line on time plots, as the demo does, to compare directions and corridor loading.

## KPIs instrumented
Traffic (peds/h) and intensity (peds/(h·m)) per line over time.

## Pitfalls
- The model's own description says `traffic()` covers the last hour; Help 8.9.10 says five minutes × 12. Trust Help: the value is a short moving estimate, noisy for bursty flows.
- During the first five minutes of the run and after `reset()` the ×12 scaling is still applied to a shorter window, so traffic reads **low** — skip that period or use your own window.
- For an hourly or whole-run KPI, take differences of `countPeds()` over your chosen interval instead of averaging `traffic()`.

## Reusable idea
Place flow-statistics lines at every design-critical cross-section and report intensity against level-of-service thresholds; derive long-window flow from `countPeds()` deltas, and keep `traffic()` for live dashboards.

## When the co-pilot should use this
Corridor/door/gate sizing, level-of-service studies, counter-flow analysis, and any request for "how many people pass here per hour" in a pedestrian model. For area density use `pedestrian-density-map.md`.
