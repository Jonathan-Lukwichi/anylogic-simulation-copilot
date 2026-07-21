# Pattern card — Agent Moves Between Spaces
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (ABM pedestrian library + Process Modeling library)
- **Problem it solves:** Coordinating the handoff of pedestrian agents across physically distinct spaces (waiting area, platform, train) including boarding, travel, and alighting.

## Block chain

Two interleaved flows work together:

**Pedestrian flow:**
PedSource → PedGoTo (waiting area) → PedWait → PedGoTo (platform) → PedEnter (board train) → PedGoTo (seat inside train) → PedWait (ride) → PedExit (alight) → PedGoTo (exit zone) → PedSink

**Train / vehicle flow:**
Source (one train agent) → Wait (hold at station during boarding) → Pickup (collect all boarded passengers) → MoveTo (GIS destination node — depart) → MoveTo (return station node) → Dropoff (release passengers back to pedestrian space) → Enter (back into station logic) → Sink

The two flows are coupled: the train's Pickup triggers the pedestrian PedEnter, and its Dropoff triggers PedExit, so passengers physically travel inside the train agent rather than independently.

## Resources

- No explicit ResourcePool; the train agent itself acts as a capacity-bounded carrier.
- PedSource generates the initial crowd (rate set to 2000 persons at startup, then set to 0 — i.e., a one-shot batch arrival).
- A GIS WorldMap provides the spatial context with named nodes for origin and destination stations.

## Key settings worth copying

- **Time unit:** Seconds.
- **Crowd generation:** Instantaneous batch — rate is set high at time 0 then immediately zeroed, producing a fixed crowd rather than a continuous arrival stream.
- **Pickup block:** Collects all waiting pedestrians at once; capacity is effectively unlimited (whole-train boarding).
- **Dropoff block:** Releases passengers back into the pedestrian layer at the destination, restoring their autonomous navigation.
- **MoveTo (GIS):** Uses named GIS nodes so the train's route is geography-aware; swap node references to relocate the route without restructuring the logic.
- No stochastic distributions are used — timing is deterministic or event-driven (boarding completes when the waiting area empties).

## KPIs instrumented

- n/a (the model is a structural/spatial demonstration rather than a performance-measurement study; no explicit KPI collectors or statistics blocks are present).

## Reusable idea

Use a **Pickup → MoveTo → Dropoff** triplet on a vehicle agent to move a crowd of pedestrian agents as a single unit across a GIS map, preserving each pedestrian's identity and allowing them to resume autonomous navigation after alighting. This pattern cleanly separates the vehicle's route logic from the individual pedestrian's space-navigation logic, making it easy to extend to buses, elevators, or any batch-transport scenario.
