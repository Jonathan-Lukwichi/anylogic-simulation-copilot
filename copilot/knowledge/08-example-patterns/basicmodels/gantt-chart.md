# Pattern card — Gantt Chart
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Visualising per-resource-unit activity states over time using a Time Color Chart (Gantt-style display) driven by a live resource pool.

## Block chain
Entities arrive via **Source** → enter a **Hold** that gates flow until capacity is available → proceed through one or more **Delay** blocks representing work phases → are retrieved from or stored in a **StorageSystem** via **Store / Retrieve** blocks → finally exit through a **Sink**. A **TransporterFleet** of **Forklift** agents moves items between storage areas. A second parallel path (Source → Hold → Delay → Sink) handles a simpler job stream, illustrating that multiple independent chains can share the same Gantt visualisation.

## Resources
- **TransporterFleet** containing Forklift units (material-handling transporters)
- **StorageSystem** with two **StorageDescriptor** rack areas
- Resource pool units expose `getState()`, `isIdle()`, and `isBusy()` — each unit must have "Use in flowcharts as: Resource unit" enabled so these helper functions work correctly

## Key settings worth copying
- **Delay durations:** `uniform(100, 200)` seconds for storage operations; `uniform(5, 15)` seconds for transport legs
- **Time unit:** Seconds
- **Gantt setup:** Add a *Time Color Chart*; bind each series to one resource-unit agent; map the value to `unit.getState()` so idle / busy / blocked states render as distinct colour bands
- **Hold block:** used as a gate — unblock programmatically when upstream conditions are satisfied, preventing premature entity release

## KPIs instrumented
- Visual resource utilisation (idle vs. busy vs. blocked) per unit on the Gantt chart
- Implicit throughput visible from Sink statistics
- n/a for explicit numerical wait-time or cost outputs in this example

## Reusable idea
The central trick is wiring a **Time Color Chart** to the `getState()` function of each resource-unit agent rather than to a custom variable — this gives a zero-extra-code Gantt timeline that automatically tracks every state transition in the resource pool, making it immediately reusable in any DES model that already uses AnyLogic's built-in resource or transporter constructs.
