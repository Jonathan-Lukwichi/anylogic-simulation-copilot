# Pattern card — Processing on the conveyor: Station markup (capacity modes, built-in resources) and batch-and-re-enter assembly
- **Source:** AnyLogic video "Webinar | Fundamentals of the AnyLogic Material Handling Library" (https://youtu.be/pY44q0g3LAE) — distilled, original wording
- **Paradigm:** DES (Material Handling Library + PML)
- **Problem it solves:** Model a machine that works on items where they sit on the belt (weld 3 parts into 1), with operators, and put the new assembled item back on the line.

## Block chain
The webinar's welding cell, which follows the entry chain in `videos/mhl-convey-routing-offsets-leave-on-exit.md`:
1. `Convey` to the station. Tick **Leave conveyor on exit**.
2. `Batch`: size 3, new batch type = `WeldedItem`, a Material item 3 m long.
3. `ConveyorEnter`: place the batch at a Position on conveyor `afterWeld`, just downstream of the station.
4. `SelectOutput`: 50 % go to inspection.
5. `Service`: the engineer inspects the item.
6. `Convey` to the end. The target conveyor is chosen from `agent.passed`.
7. `Sink`.

Why it works:
- **The Station does the timing** (20 s, **Capacity** 3, processing starts once all 3 are inside). No Delay or Service block is needed for the weld. The Station is markup on the conveyor, and a Convey whose route crosses it triggers the processing.
- **Leave conveyor on exit is required** on the first Convey. Without it, the three batched parts would stay on the belt as obstacles.
- **Re-enter instead of converting in place.** The assembly is removed and re-inserted downstream; its type is not changed on the belt. Help 8.9 warns that stations must not change the material item type, because the conveyor expects the same type after them.

## Resources
- **`welders`** ResourcePool, 2 units. The **Station itself** seizes both (*Use resources*). Home = a rectangular node with attractors.
- **`engineer`** pool, 1 unit, used by the inspection `Service` with **Send seized resources** ticked, so he walks to the item.

## Key settings worth copying (Station, Help 8.9)
- **Delay type:**
  - *Specified time*: a Process time expression, with `agent` available.
  - *Until stopProcess() is called*: end processing with `station.stopProcess()` or `stopProcess(agent)`.
- **Capacity:** `getCapacity()` / `setCapacity(n)`, and it can be changed at runtime. The webinar's older build calls it Quantity; `getQuantity()` is now deprecated.
- **Processing modes:**
  - *Starts when capacity is full*: collect N items and process them together. The **Loading** option then sets whether new items load *simultaneously with unloading* or *start when unloading completes*.
  - *Starts when agent enters station*: each item is timed on its own. It creeps to the exit and waits there until done.
- **Use resources:**
  - *Seize* either units of the same pool (Resource pool + Number of units) or (alternative) resource sets.
  - **Send seized resources**, with a Destination: node, attractor, or (x, y, z).
  - *Customize resource choice*, e.g. `agent.myAssistant == unit`.
  - Task priority and preemption.
- **Quality flag:** add `boolean passed = true` to `WeldedItem`. In the inspection Service's On exit, write `if (randomTrue(0.5)) agent.passed = false;` and recolour the item.

## KPIs instrumented
- **Webinar:** welder and engineer utilization, taken from their pools.
- **Suggested:**
  - `station.getUtilization()`.
  - `station.totalStateTime(ConveyorSimpleStationState.WAITING_FOR_RESOURCES, MINUTE)`: time the station spent starved of crew. Its states are `IDLE`, `WAITING_FOR_RESOURCES`, `PROCESSING`, `MAINTENANCE`, `FAILED` and `CUSTOM_DOWNTIME`.
  - `meanStateTime(...)` and the pass rate.

## Pitfalls
- **No Leave conveyor on exit before Batch/Combine:** phantom parts keep blocking the conveyor.
- **Agent-enters mode:** resources are held per station session, so resource-related callbacks run only for the item that wakes an idle station (Help 8.9).
- **Capacity-full mode** waits for N items. If fewer than N can ever arrive (for example, the tail of a finite order), the last parts never get processed *(inferred)*.
- **Placement:** a Station cannot sit on a reversible conveyor. It does not split the conveyor, unlike transfer tables, turntables and turn stations.
- **Instant vs timed work:** a Position on conveyor is for instant actions. Anything that takes time belongs in a Station.

## Reusable idea
Put *where the work happens* in the markup: a Station with its own delay and crew. Keep the flowchart for *what changes*: batching, quality flags, routing. To change the product type, take the parts off the line and re-enter the new item downstream.

## When the co-pilot should use this
- **Use cases:** welding, assembly or packing cells on a line; scanning or labelling stations with a dwell time; conveyor workstations served by operators.
- **Typical questions:** "merge N parts into one on a conveyor", "attach workers to a conveyor station", "why does my batch leave items on the belt".
- **Related cards:**
  - `basicmodels/lead-acid-battery-production-phase-1.md` (a station on the line)
  - `basicmodels/lead-acid-battery-production-phase-4.md` (the batch → unbatch sandwich)
