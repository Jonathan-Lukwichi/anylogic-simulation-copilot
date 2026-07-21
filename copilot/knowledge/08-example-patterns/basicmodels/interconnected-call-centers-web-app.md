# Pattern card — Interconnected Call Centers (Web App)
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Discrete-Event Simulation)
- **Problem it solves:** Models a network of call centers that can overflow or redirect calls between nodes, letting analysts tune per-center capacity, arrival rate, and agent skill to balance load across the system.

## Block chain
Each CallCenter agent encapsulates its own mini-pipeline: **Source** → **SelectOutput** (overflow check) → **Seize** (grab operator) → **Service** (handle call) → **SelectOutput** (resolution or escalation) → **Release** → **Exit/Sink**. Calls that cannot be served locally leave via **Exit**, traverse a **Link** with a configurable capacity, and re-enter a neighboring center through **Enter**. A top-level **Main** agent holds the ResourcePool for operators and wires the CallCenter agents together with directional Links whose widths are drawn proportional to link capacity in the network diagram.

## Resources
- **ResourcePool** (operators) per CallCenter — capacity set dynamically via `operators.set_capacity(operatorsCapacity)`
- **Link capacity** — integer parameter controlling max simultaneous transfers between any pair of centers; adjustable at runtime via the web UI slider

## Key settings worth copying
- **Arrival rate:** `exponential(callsPerHour / 60.0)` — converts an hourly parameter into a per-minute inter-arrival time; rate is hot-updated with `source.set_rate(callsPerHour, PER_HOUR)` on slider change
- **Service time:** `uniform(callDurationMean / skillLevel * 2, callDurationMean / skillLevel * 3)` — skill level compresses the duration range, rewarding higher-skilled agents
- **callsPerHour** initialised with `uniform_discr(100, 500)` per center; **skillLevel** with `(int)uniform(5, 25)`; **operatorsCapacity** with `(int)uniform(1, 5)`
- **Time unit:** Minutes
- **Web App UI:** sliders for callsPerHour, skillLevel, and link capacity update live model parameters without restarting — pattern for interactive what-if dashboards

## KPIs instrumented
- Queue length / wait time inside each CallCenter's Service block
- Operator utilisation (ResourcePool statistics)
- Overflow volume (flow through Exit/Enter links between centers)
- Link utilisation displayed as line thickness in the network diagram

## Reusable idea
The transferable trick is **agent-encapsulated DES pipelines connected by parameterised links**: wrap each service node (call center, warehouse, clinic) as a self-contained agent with its own Source-to-Sink chain, then let a parent agent wire these nodes with Link objects whose capacity becomes the inter-node bandwidth. This decouples local service logic from network topology and enables runtime reconfiguration (add a link, change its capacity) without restructuring any process flowchart.
