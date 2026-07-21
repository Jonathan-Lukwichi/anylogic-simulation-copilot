# Pattern card — Traveling Salesman
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based)
- **Problem it solves:** Demonstrates how to embed a Python-based combinatorial optimizer (OR-Tools TSP solver) inside an AnyLogic simulation so a truck agent receives a dynamically re-optimized delivery route each time a new batch of orders arrives.

## Block chain
Orders are generated sequentially and accumulated into a batch. When a batch is ready, order data (facility coordinates) is passed via the **Pypeline** bridge to a Python OR-Tools script that computes the shortest round-trip route starting and ending at the home depot. The optimized city sequence is returned to the simulation, and the **Truck** agent follows the route, visiting each **Facility** agent in sequence before returning home. The cycle then repeats with the next batch.

## Resources
- One **Truck** agent (the traveling salesman vehicle).
- A population of **Facility** agents loaded from `facilities.xlsx`, each carrying a `facility_data` record (name, latitude, longitude).
- A **PyCommunicator** object managing the AnyLogic-to-Python IPC channel.

## Key settings worth copying
- `uniform_discr(3, facilities.size()-1)` selects a random subset of 3 to N-1 facilities per order batch, making route complexity variable across runs.
- Time unit: **Hour**.
- Facility coordinates sourced from an Excel dataset (`facilities.xlsx`) — easy to swap for any real network.
- Requires the **Pypeline** add-on and a local Python 3 environment with OR-Tools installed (see `requirements.txt` bundled with the model).

## KPIs instrumented
- Total route distance / travel time per delivery cycle.
- Number of cities visited per tour.
- (Visual) animated truck movement on GIS map showing the optimized path.

## Reusable idea
The transferable trick is the **Python co-process pattern**: use AnyLogic's Pypeline bridge to offload NP-hard optimization (TSP, VRP, scheduling) to a mature Python solver at runtime, then feed the solution back as agent behavior — keeping the simulation loop clean while leveraging the full Python ecosystem for heavy computation.
