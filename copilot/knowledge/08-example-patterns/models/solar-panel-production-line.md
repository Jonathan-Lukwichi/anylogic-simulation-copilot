# Pattern card — Solar Panel Production Line
- **Source:** AnyLogic example model "Solar Panel Production Line" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library conveyors and stations, robots, AGV fleet) with machine agents written as statecharts
- **Problem it solves:** Model a panel line whose inline machines (layup, laminators, framer) have multi-phase cycles and consumable wear. Station timing then comes from the machine logic, not from a fixed process time.

## Block chain
- **Cell strings:**
  1. `Source` (1 cell/s) → `Queue` → `Convey` to the flipping station (removed from the conveyor on arrival).
  2. `Batch` of `nCellsInRow` = 10 cells into a string.
  3. `Seize` of a **static 1-unit pool** `layupCellBuffer`, a token for the single flip position.
  4. `Delay` flip (15 s).
  5. `Seize layupRobot` (moving pool; *send* and *attach* resources) → `Release` of the token.
  6. `MoveTo` scanner (trip time 10 s). If the layup station is not processing a glass panel, wait in a `Delay` (type *manual*).
  7. `MoveTo` (x, y, z) of the next row on the glass → `Release layupRobot` (does not go home; *On enter* counts rows and calls `layup.stopProcess()` after the last one) → `Sink`.
  8. From Release's **`wrapUp`** port: `MoveTo` robot back to its start pose → `ResourceTaskEnd`.
- **Panels:**
  1. `Source` (manual) → `Convey` to a photo-eye position.
  2. `Convey` to the end of the line with **Include conveyors** `{ chooseLaminatingStation(agent).getConveyor() }`.
  3. `ProcessByRobot` (safe height 1.3 m, destination a random stack node, returns to its initial position).
  4. `SelectOutput5` by stack → permanent `Batch` per stack → `MoveByTransporter` (AGV forklift fleet) → `Sink`.
- **Stations on the conveyors:** soldering, flipping, laminating ×3 (capacity `laminatorCapacity` = 4, cycle time chosen by EVA type), cooling, trimming (operator pool), framing, edge sealing, junction box, flasher, labelling.

## Resources
Layup robot (moving pool), the static flip token, operator pools bound to stations (bussing ×2, trimming, junction box, flasher), the unloading robot, and the forklift AGV fleet.

## Key settings worth copying
- **Machine statechart drives a manual station** (the framer). The station's *Delay type* is *Until stopProcess() is called*, and its *On process started* runs `send("startProcess", framingMachine)`. The machine then runs top/bottom attach → side attach → seal → release (each a Timeout, e.g. `10 / attachingSpeed`), and the last transition calls `station.stopProcess()`. Cycle time is the sum of the phases, so speed parameters act where the engineer thinks of them.
- **Consumable life with `fail()` / `repair()`** (laminator agent, replicated ×3, `laminatorStation = laminatingStations.get(index)`):
  - The station's *On process started* / *On process finished* send "close" / "open".
  - Opening is guarded by `!laminatorStation.isProcessing()` and decrements `currentMembraneLife`.
  - When the life reaches 0, the machine enters a change state: `station.fail()` plus a red colour. After `membraneChangingTime` (20 min) it calls `repair()` and resets the life to `3000 + (int)triangular(0, 3, 10)` cycles.
  - Help 8.9.10: during `fail()` no new item can enter, and items inside wait for the repair. The station's state reads `FAILED`.
- **Batch-wise dealing to parallel batch machines.** `chooseLaminatingStation()` sends `laminatorCapacity` consecutive panels to the same laminator before moving to the next, so each laminator fills a full load.
- **Wrap-up after release** (Help *Release*). The resource's own post-task flowchart starts at `wrapUp` and must end in `ResourceTaskEnd`. The policy is *each time*, *if no other tasks*, or *custom* (priority and preemption); *each time* cannot be pre-empted, not even by Downtime. Its usage can be counted busy, idle or not at all.
- **Throughput KPIs.** A cyclic event runs `dataProductionRate.add(hourOutput); hourOutput = 0;` for hourly output, and the unloading robot's *On exit* records the time between consecutive finished panels.

## KPIs instrumented
Panels per hour, time between outputs (takt), production start time per panel, station busy/idle colours, and laminator membrane-change downtime.

## Pitfalls
- **Deprecated message call.** The model sends to the laminator with `laminator.get(0).receive("close")`; `receive()` is deprecated (Help release notes). Use `send(...)` or the statechart's `receiveMessage(...)` in new models (see G24).
- **Built-in downtime triggers.** Before hand-writing a wear counter, check the `Downtime` block's cycle trigger (Help: the number of seizes between occurrences) and whether it counts station cycles for your element *(unverified for stations)*. The statechart route is needed when wear depends on custom events (openings, not seizes) or is randomised per replacement.
- **Manual-mode timing is invisible.** A manual station's *Process time* field is ignored, so document the machine phases as the real cycle time.
- **Tokens for positions.** Use a static token pool for a one-place position that no markup represents. Otherwise two strings can occupy the flip position.

## Reusable idea
Keep the MHL station as the place where items wait and are processed, and put the machine's own behaviour (phases, wear, changeovers) in an agent statechart linked to it:
- station callbacks send messages to the machine;
- the machine answers with `stopProcess()`, `fail()` and `repair()`.

The same division works for presses, ovens, testers and any inline machine with sub-steps or consumables.

## When the co-pilot should use this
- **Use cases:** multi-phase inline machines on conveyor lines, consumable or tool-life downtime (membranes, dies, filters), and robots that must return or reset after each task (wrap-up).
- **Related cards:**
  - `videos/mhl-conveyor-station-processing-and-reassembly.md` (station modes)
  - `videos/mhl-conveyor-control-sensors-and-breakdowns.md` (fail/repair, Downtime)
  - `videos/mhl-convey-routing-offsets-leave-on-exit.md` (Include conveyors)
  - `videos/mhl-agv-dispatch-choice-and-cargo-position.md`
