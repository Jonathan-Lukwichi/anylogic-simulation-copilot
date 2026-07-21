# Pattern card — Custom Routing for Transporters
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Controlling exactly which path an AGV takes through a material-handling network instead of always defaulting to the shortest route.

## Block chain
A Source generates material items at a configurable arrival rate. A MoveByTransporter block seizes an AGV, moves the item from a pickup node to a drop-off node, then releases the transporter. A Sink destroys completed items. The AGV fleet is managed by a TransporterControl block whose custom `setRoute()` callback is the heart of the model — it fires every time a transporter needs a new route and returns a `RouteData` object that the AGV follows exactly.

## Resources
- One AGV agent (type AGV) operating on a path network; fleet size is implicitly one unit in the base configuration.
- Two fixed nodes (source node, target node) connected through a graph of path segments.

## Key settings worth copying
- **Routing policy selector (3 modes):**
  1. *Shortest path* — call `findShortestPath()` to populate a `RouteData`; this is the out-of-the-box default.
  2. *Shortest path excluding a specific link* — remove the unwanted segment from the candidate graph before calling `findShortestPath()`.
  3. *Manual task list* — build a `RouteData` from scratch by appending individual movement tasks in the desired order.
- The `setRoute(ILocation source, ILocation target, AGV agv)` function signature is the standard hook; inspect `agv`'s current state inside it to make the decision conditional on runtime context.
- Return trip (home → home) always uses the default shortest path, keeping idle travel efficient.
- Model time unit: **Minute**; AGV speed expressed in **m/s** (10 m/s default); path network scaled in metres.

## KPIs instrumented
- Throughput visible through the Sink's count of destroyed agents.
- No explicit wait-time or utilisation dashboards in the base model; the focus is on routing correctness rather than performance metrics.

## Reusable idea
Hook into `TransporterControl`'s `setRoute()` callback and return a hand-crafted `RouteData` to enforce business rules (avoid congested aisles, respect one-way zones, prioritise certain corridors) while still delegating the return trip to the automatic shortest-path algorithm — giving you surgical control over outbound movement without rebuilding the whole routing engine.
