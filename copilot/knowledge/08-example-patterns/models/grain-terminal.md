# Pattern card — Grain Terminal
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + Fluid)
- **Problem it solves:** Sizing and scheduling a multi-modal bulk-commodity terminal where trains and trucks deliver grain to silos and ships load from those silos via conveyor networks.

## Block chain
Grain arrives at the terminal by two vehicle types: trains (TrainSource → TrainMoveTo unloading stop → Delay for unloading → TrainMoveTo exit → TrainDispose) and road trucks/cars (CarSource → SelectOutput routing → Queue → Hold → Seize unloading dock → CarMoveTo → Delay for unloading → Release → CarDispose). Both streams deposit grain into intermediate storage modelled as fluid tanks connected by bulk conveyor belt networks (BulkConveyorBelt elements organised into ConveyorsNet). Valves (Valve blocks) gate flow between the intake conveyor network and the main silo tanks, and between the silo tanks and the ship-loading conveyor network. When a ship berths at one of the available piers it seizes the pier resource, then each bilge is filled sequentially from the appropriate silo via the pier conveyors (piersConveyors); a RestrictedAreaStart/End pair enforces single-bilge access at a time. FluidEnter and FluidExit connectors bridge the discrete vehicle events into the continuous fluid layer, and FluidCut blocks let the model interrupt flow when a tank is full or empty.

## Resources
- Pier berths (finite count; ships Seize on arrival, Release on departure)
- Unloading dock positions for trucks (Seize/Release with Hold/Queue upstream)
- Train unloading stops (dedicated TrainMoveTo path; implicit capacity = number of stops on the rail network)
- Bulk conveyor belts (speed-limited; shared between intake and ship-loading directions)
- Silo tanks (fluid capacity; grain type partitioned per bilge/silo mapping)

## Key settings worth copying
- **Time unit:** Second (fine-grained enough to capture conveyor transit times)
- **Conveyor speed:** Parameterised label "Conveyor speed" — expose as a slider to run speed-sensitivity experiments
- **Multi-commodity routing:** SelectOutput checks grain type on the vehicle agent to route to the matching silo; replicate this pattern whenever commodity identity must be preserved through a shared conveyor
- **Valve gating:** Valves are toggled in event code triggered by tank level thresholds — a clean way to implement level-controlled filling without polling
- **Bilge-by-bilge ship loading:** a loop over bilge agents, each seizing the pier conveyor, loading to target volume, then releasing — models realistic partial-load sequencing

## KPIs instrumented
- Ship turnaround time (berth arrival to departure)
- Truck and train queue length / wait time at unloading docks
- Silo fill level over time (fluid content)
- Conveyor utilisation (throughput vs rated capacity)
- Terminal throughput (tonnes per day)

## Reusable idea
Bridge discrete vehicle arrivals into a continuous fluid layer using FluidEnter/FluidExit connectors and Valve blocks controlled by tank-level events. This hybrid handoff lets you keep accurate vehicle counts and queuing logic (DES) while modelling bulk commodity flow at realistic rates (fluid) — avoiding the combinatorial explosion of tracking individual grain particles as discrete entities.
