# Pattern card — Group Behavior in Services
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Pedestrian / Agent-based hybrid using Pedestrian Library)
- **Problem it solves:** Modelling how groups of pedestrians (families, tour groups) are handled at service points when the service policy differs from individual treatment.

## Block chain
Three parallel scenarios run side-by-side, each following the same skeleton:

**PedSource → PedGoTo → PedService → PedSink**

Each PedSource spawns pedestrian *groups* of variable size. After arrival, a PedGoTo steers the group toward the service area. A PedService block applies one of three policies:
1. **All members serviced individually** — every person in the group occupies a server slot (turnstile analogy).
2. **One member serviced; rest queue together** — a single representative is served while the others stand in the queue behind them (cinema ticket-counter analogy).
3. **One member serviced; rest wait in a holding area** — the representative joins the queue alone while the rest disperse to a designated waiting zone until service is complete (museum tour-guide analogy).

After service, agents proceed to a PedSink to exit the scene.

## Resources
- Service counters embedded in PedService blocks (one per scenario, capacity implicit in the pedestrian space layout).
- Waiting areas (AreaNodeDescriptor zones) used as holding regions for scenarios 2 and 3.
- 3-D office-worker and table assets for visual representation of servers.

## Key settings worth copying
- **Group size distributions per source:**
  - Scenario 1: `uniform_discr(2, 4)` persons per group
  - Scenario 2: `uniform_discr(1, 3)` persons per group
  - Scenario 3: `uniform_discr(3, 5)` persons per group
- **Inter-arrival time:** `exponential(3)` seconds between groups (all scenarios); arrival rate expressed as `exponential(1000 / hour())`.
- **Service duration:**
  - Scenario 1 (individual): `uniform(10.0, 15.0)` seconds per person
  - Scenarios 2 & 3 (representative only): `uniform(30.0, 35.0)` seconds per transaction
- **Model time unit:** Seconds
- **Agent startup animation:** `setAnimation(uniform_discr(0, animations.size() - 1))` — randomly picks a pedestrian appearance at creation for visual variety.

## KPIs instrumented
- Throughput of pedestrian groups through each service channel.
- Queue length and waiting time differences across the three service policies.
- Utilisation of the service counter implied by agent occupancy in PedService.
- Visual comparison of congestion patterns in the 2-D/3-D environment.

## Reusable idea
The transferable trick is **decoupling group-level arrival from individual-level service logic**: by controlling which group members enter the PedService queue versus which wait in a separate area node, you can faithfully replicate real-world service policies (individual, representative-in-queue, representative-only) without splitting agents or using complex custom code. Simply configure the PedService group behaviour flag and assign an AreaNode for the non-queuing members.
