# Pattern card — Match
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Pairing two independent agent streams by a shared attribute before allowing either to proceed — the classic "two-sided queue" rendezvous problem.

## Block chain
Two separate Source blocks feed two independent queues inside a single **Match** block (`matchColor`). One stream generates Person agents, the other generates Suitcase agents. Neither can leave the Match block until a pair satisfying a custom condition is found. Once a matched pair is identified they are handed off to a **Combine** block that merges them into one composite agent, which then travels via **MoveTo** to an exit **Sink**. A deadlock handler is wired to both queue-full events so the model can detect and report gridlock when no valid pairing remains possible.

## Resources
n/a — no resource pools or capacities; throughput is limited purely by the matching condition and arrival rates of both streams.

## Key settings worth copying
- **Match condition (agent1 × agent2):** `agent1.favoriteColor.equals(agent2.suitcaseColor)` — a one-line boolean expression; swap in any attribute comparison to reuse the pattern.
- **Color assignment at source:** `randomFrom(availableColors)` applied on each agent at creation; `availableColors` is a shared `Color[]` array, making it easy to control the palette and therefore the match probability.
- **Deadlock callback:** both `onMaxCapacityReached` hooks call `handleDeadlock(queue1.size, queue2.size, ...)` — copy this guard whenever a two-sided queue can theoretically stall.
- **Time unit:** Second.
- **Downstream merge:** Combine block fuses the matched pair so downstream logic sees one agent, not two — clean separation of matching logic from post-match processing.

## KPIs instrumented
- Queue lengths in both internal queues (monitored via `matchColor.queue1` and `matchColor.queue2` for deadlock detection).
- Implicit throughput visible through Sink entry count.

## Reusable idea
The transferable trick is the **attribute-equality match gate**: instead of a resource seizing an entity, two independent entity streams gate each other. Any scenario where two populations must be paired by a property — job-to-worker skill matching, organ-to-recipient compatibility, order-to-vehicle type assignment — can be modeled by replacing the color equality check with the relevant domain condition, leaving the rest of the block chain unchanged.
