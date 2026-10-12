# Pattern card — Statechart agent through a flowchart hosted in another agent (Enter.take + Exit/send)
- **Source:** AnyLogic video "How to use agents in a process flow" (https://youtu.be/88D95QYtduM) — distilled, original wording
- **Paradigm:** Hybrid (ABM statechart + DES flowchart)
- **Problem it solves:** A mobile agent run by a statechart (truck, AGV, ship) must queue for scarce resources at the site it visits and then resume its own behaviour, keeping its identity instead of being destroyed and re-created.

## Block chain
The concept is already in the KB (`models/container-line.md`, Reusable idea). This card adds the exact wiring. The video extends the Supply Chain GIS tutorial (phase 4) with truck unloading at retailers.
1. **Host the process in the site's agent type** (`Retailer`): `Enter` → `Service` (named `unloading`) → `Exit`, plus a `ResourcePool` `forkliftTrucks`. Every Retailer instance gets its own queue and its own forklifts.
2. **Push the agent in.** The statechart transition `MovingToRetailer → Unloading` (Triggered by: Agent arrival) has the Action `order.retailer.enter.take(this);`. It follows the agent's own data to the host, then inserts *this* agent at the host's Enter block.
3. **Serve.** Service seizes a forklift, holds for `agent.order.amount * 10` (unit: minutes), then releases.
4. **Hand back.** In Exit → On exit: `send("unloaded", agent);`.
5. **Leave.** The transition `Unloading → MovingToDistributor` is Triggered by **Message**, Fire transition = **On particular message**, Message = `"unloaded"`.

The video's first version used a plain 2-hour Timeout on that last transition. That is enough while the dwell does not compete for shared resources.

## Resources
- `ResourcePool` `forkliftTrucks` inside the host type. Capacity = forklifts per site.
- Visiting agents stay members of their own population the whole time.

## Key settings worth copying
- **Enter → Agent type.** Set it to the visiting type (`Vehicle`). It defaults to `Agent`. The type propagates to the downstream blocks, which is what lets `agent.order.amount` compile.
- **Enter → New location.** Leave it *Not specified* (the default). The agent then stays where its own movement left it.
- **Enter → Forced pushing** defaults to on, so every taken agent is pushed straight into Service. Service's internal queue (default capacity 100) must hold the worst-case number of visitors at one site; otherwise expect G4's "not able to leave the port" error *(same push mechanism as G4; inferred)*. *Beyond the video: AnyLogic Help 8.9.*
- **Exit, not Sink.** Exit only removes the agent from the flowchart. Sink disposes of it.
- **Enter API** (Help 8.9): `take(agent)`; `size()` counts agents taken but not yet accepted downstream; `cancel(agent)` / `cancelAll()` withdraw them; `count()` counts insertions.
- **Message matching.** "On particular message" calls `equals()` on the descriptor, so String messages match by value.

## KPIs instrumented
The video has none. Suggested: `unloading.queueSize()` and `unloading.utilization()` per retailer, `forkliftTrucks.utilization()`, and the share of vehicle time spent in `Unloading`.

## Pitfalls
- **The transition never fires, so the vehicle waits forever.** A statechart only sees agent messages if it is ticked under **Forward message to**. Find this under the receiving type's *connections* element → Communication. It is AnyLogic's own troubleshooting entry. *Beyond the video.*
- **Unheard messages are dropped, not stored.** A message that arrives while no matching transition is active is discarded. Take the agent in the transition *into* the waiting state, as the video does, and use `send()`. `send()` delivers in a separate zero-time event, scheduled after the current one, so the transition into the waiting state has already completed.
- **Typos fail silently.** A mismatch between the `send` string and the transition's Message compiles fine and strands the agent. Keep the string in one constant.
- **Process drawn on Main.** Point-to-point `send("unloaded", agent)` works from a flowchart on Main; only the broadcast and random sends (`sendToAll`, `sendToRandom`, `send(msg, ALL | RANDOM)`) raise "Environment must be defined" there (8.9.10 engine; three 8.9.10 example models call `send(msg, agent)` from Main; corrected 2026-10-01 — gotcha G22). Help's wording ("any" message function) is broader than the engine.
- **Pull an agent out of whatever block holds it** with `currentBlock().remove(this)` (Agent API), for example from a click on its own shape, then `enter.take(this)`; if it was on a conveyor, follow that `Enter` with `ConveyorExit` to free the belt (8.9.10 *Enter and Exit* example). A round-robin split over a list is `list.get(++counter % list.size())`.
- **`deliver()` and `receive()` are deprecated since AnyLogic 8.9.2.** Use `send()`. Note that `basicmodels/air-defense-system-phase-3.md` still shows `deliver`.
- **Re-attached transitions keep their old trigger.** When the old Agent-arrival transition is re-attached to start at the new dwell state, change its trigger. The video switches it to Timeout, then to Message.

## Reusable idea
Exit → `target.enter.take(agent)` is a general router that can cross agent boundaries. Pick the target at run time (shortest queue, nearest site). Help 8.9 gives `receiver(i).enter.take(agent)` for replicated receivers. The same pair lets statecharts, events or other flowcharts "call" a flowchart as a subroutine.

## When the co-pilot should use this
- **Phase 0.** Choose this when a system mixes autonomous movers (trucks, AGVs, ambulances, ships) with capacity-limited service at the places they visit.
- **Prefer it** over sinking the agent and re-creating it in a Source, because the agent keeps its attributes, statechart and history. Prefer it over a statechart timeout whenever the dwell depends on shared resources.
- **Related:** `models/container-line.md` (the concept), `models/epidemic-and-clinic-with-accumulating-concern.md` (DES→statechart `send`), and `anylogic-gotchas.md` G4.
