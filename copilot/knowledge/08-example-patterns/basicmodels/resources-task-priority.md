# Pattern card — Resources Task Priority
- **Source:** AnyLogic example model "Resources Task Priority" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Process Modeling Library, moving resources)
- **Problem it solves:** Let an urgent job interrupt a moving resource that is already busy with a less urgent one, and control what happens to the interrupted job.

## Block chain
`Source` (a package every 5 s, first at time 0, at `arrivalNode`) → `Seize` (pool `sorter`; *Send seized resources* and *Attach seized resources* on; task priority `agent.priority`; *Task preemption policy* = **Wait for original resource**) → `MoveTo` (`processingPoint`; the sorter carries the package) → `Release` (*moving resources go home* off, so the sorter stays where it is) → `Sink`.
A second `Source` (arrivals by `inject()`) feeds the same `Seize` from a button, with the priority chosen on screen, to trigger an interruption on demand.

## Resources
Moving `ResourcePool` `sorter` of type `Sorter` (7 m/s, home node `homeNode`). Packages carry `priority` (0 green, 1 yellow, 2 red) and a running number.

## Key settings worth copying
- **Two separate knobs (Help 8.9.10, *Seize*):** *Task priority* (larger = more urgent, default 0) only orders the waiting requests; whether a running task can be interrupted is *Task preemption policy*, default **No preemption**. *Task may preempt* (default true) lets this block's tasks interrupt others when their policy allows it.
- **Preemption policies:** *Wait for original resource* (the interrupted task waits for the same unit), *Seize any resource* (it may take any unit that passes the resource-choice condition), *Terminate serving* (it is dropped: send the agent to an `Enter` block, remove it from the flowchart, or do nothing and handle it in *On task terminated*), *Continue without resource* (the task finishes without the unit).
- **Auto suspend/resume agents** (default on, for the first two policies): the interrupted agent is frozen in its current block and resumes when a unit is available again.
- **Tie-break at equal priority (Help, *Using resources*):** first the unit's own queue of suspended tasks (from *Wait for original resource*), then the pool's queue of suspended tasks (*Seize any resource*), then new tasks — the unit's queue before the pool's. To change this order, lower the task's priority in *On task suspended*.
- **Skewed priority classes in one expression:** `(int) triangular(0, 0, 3)` gives 0, 1, 2 with probabilities 5/9, 3/9, 1/9 (min 0, mode 0, max 3; G55 on argument order).
- Package numbers come from a class-level counter, `Package.lastNumber++`, in the `newEntity` constructor call.

## KPIs instrumented
None in the demo. Add: waiting time per priority class (TimeMeasureStart/End split by `priority`), a count of suspensions in *On task suspended*, sorter utilization, and distance travelled per delivered package (preemption adds empty trips).

## Pitfalls
- Setting priorities alone never interrupts anything; the policy must allow preemption (G? proposed in `.ingest/proposals/m-basic-3.md`).
- Each interruption of a **moving** resource costs travel: in the demo the sorter puts its package on hold, fetches the urgent one, then comes back. Under heavy urgent load the low class can starve; watch its waiting-time tail.
- *Terminate serving* with *do nothing* leaves the agent in the block until its delay ends; handle it in *On task terminated* or it silently continues.

## Reusable idea
Model urgency as two decisions: priority orders the queue, the preemption policy decides the fate of interrupted work. For carried items prefer *Wait for original resource* (the same unit finishes the job); for services by interchangeable staff prefer *Seize any resource*.

## When the co-pilot should use this
Emergency jobs that interrupt porters, forklifts, AGV-like staff or nurses; urgent orders in picking; repair crews pulled to a higher-priority breakdown. For preemption among waiting agents (not resources) use `Queue`/`Wait` preemption instead (G7). Material Handling fleets: `SeizeTransporter` has the same priority fields but only *No preemption* or *Seize any resource* (Help 8.9.10); `basicmodels/mobile-rack-system.md` uses the latter.
