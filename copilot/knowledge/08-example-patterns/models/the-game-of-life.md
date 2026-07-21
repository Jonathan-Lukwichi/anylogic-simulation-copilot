# Pattern card — The Game of Life
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Demonstrates emergent complexity from simple local rules applied across a large grid of cellular agents.

## Block chain
A 100 × 100 grid of `Cell` agents is instantiated at startup. Each cell holds a boolean `alive` flag, initialised randomly with a 10 % probability of being alive (`randomTrue(0.1)`). Cells connect to their Moore neighbours once at startup via a `neighbors` network link. Every discrete time step (1 Day) two phases execute in order:

1. **BeforeStep** — each cell counts how many of its connected neighbours are currently alive (`nAliveAround`).
2. **AfterStep** — each cell applies Conway's survival rules: a living cell survives if it has exactly 2 or 3 alive neighbours; a dead cell is born if it has exactly 3 alive neighbours. Any change in state immediately repaints the grid cell colour (red = alive, lemon-chiffon = dead).

A `toggleState()` method allows interactive click-to-flip during runtime.

## Resources
No queues, pools, or capacities — the only shared resource is the neighbour network topology (small-world connections, fraction 0.95, range 50 units, M = 10).

## Key settings worth copying
- Grid: 500 × 500 px canvas, 100 columns × 100 rows → 10 000 cells
- Time unit: Day; step size: 1 Day; start time: 0
- Initial density: `randomTrue(0.1)` — 10 % alive at t = 0
- Neighbour connections: `NeighborLinkFraction = 0.95`, `ConnectionsRange = 50`, `ConnectionsPerAgent = 2`, `M = 10` (small-world wiring)
- `canvasScale = 5`, `agentSize = 4` for readable cell rendering

## KPIs instrumented
No formal KPI charts are wired in the base model; visual observation of live/dead cell patterns across generations is the primary output. Count of alive cells can be derived trivially by iterating the population.

## Reusable idea
Split per-agent logic into a **before-step / after-step pair** so all agents read the previous generation's state before any writes occur — this guarantees synchronous, bias-free cellular automaton updates without needing a separate state buffer array.
