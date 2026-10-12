# Pattern card — Releasing Resource on Timeout
- **Source:** AnyLogic example model "Releasing Resource on Timeout" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Process Modeling Library)
- **Problem it solves:** Cap how long an agent may hold a resource unit: release it at the end of the agent's own work or at a fixed time after seizing, whichever comes first, without interrupting the agent's process.

## Block chain
- **Main flow:** `Source` → `Split` (one copy per agent: a `Sibling` whose `id` is the original's `hashCode()`) → `Match` port 1 (original) … `Match` port 2 (sibling after it has seized) → original: `Delay` "normal work", `uniform(20, 120)` s → `Sink`.
- **Resource flow (the sibling):** `Seize` (pool of 52 units) → `Match` port 2 → `Delay` 60 s → `Release` (all units from the pool) → `Sink`. An `Enter` block also feeds the `Release`.
- `Match` condition `agent1.hashCode() == agent2.id` pairs each original with its own sibling, so the original starts working only once its sibling holds a unit.
- **Early release:** the *On exit* of the "normal work" `Delay` looks for the sibling still waiting in the 60 s `Delay`; if found, it takes it out (`remove(sib)`) and pushes it into the `Enter` (`enterRelease.take(sib)`), which releases the unit at once. If not found, the timeout already released it.

## Resources
One `ResourcePool` (52 units). The unit is formally held by the sibling, not by the working agent.

## Key settings worth copying
- The trick is a **proxy token**: the process that must not be interrupted runs on the original; the resource is held by a second agent whose only job is timing the hold. Whichever event comes first ends the hold.
- `Split` → *New agent (copy)* can build any type: `new Sibling(original.hashCode())`; its *On exit copy* action sees both `agent` (the copy) and `original` (Help 8.9.10, *Split*).
- **Simpler 8.9 variant (suggested, not in the demo):** let the sibling wait in a `Wait` block with *Enable exit on timeout* (60 s); connect both `out` and `outTimeout` to the `Release`; for early release call `wait.free(sib)` (G7). No search, no `Enter`.
- **Direct reference instead of a hash:** in *On exit copy* store `original.sib = agent` (custom field) and use it for the match and the early release *(suggested)*.

## KPIs instrumented
None. Add: share of holds ended by the timeout versus by the work (count in each path), and pool utilization, which the proxy reports correctly.

## Pitfalls
- **`hashCode()` is not a guaranteed-unique ID** in Java; rare collisions would pair the wrong agents. Use a counter or an object reference.
- **Searching a `Delay` is slow:** `get(i)` on a Delay is documented as very slow, with no stable order (Help 8.9.10, *Delay*). With many holders, keep references.
- The working agent owns no unit: `agent.resourceUnits()` is empty, *Send/Attach seized resources* cannot follow it, and resource-based costing must be read from the sibling.
- Reusing it often? Wrap the dashed-line group (Split, Seize, Match, timers, Release) as a custom block, as the model's note suggests (`videos/custom-flowchart-block-from-repeated-chain.md`).

## Reusable idea
When a rule applies to the *hold* rather than to the *work* — maximum occupation of a bed, bay, dock or phone line; a lease that expires — give the hold its own token agent and let the token, not the process, seize and release.

## When the co-pilot should use this
Maximum dwell or lease times (parking or loading-bay limits, time-boxed consultations, equipment loans), and any "release at A or B, whichever first" rule. If the work itself must end at the timeout, cap the work time instead; the timeouts of `Seize`/`Service` only limit waiting in their queues. To take a unit away for a more urgent job, use preemption (`basicmodels/resources-task-priority.md`).
