# Pattern card — Resizing a population of busy agents at runtime: hire at once, release at safe points
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 4 "How to build agent-based models. Field service example" (§4.6) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Changing how many crews, vehicles or other working agents exist during a run without deleting one mid-job, which would leave its job unfinished, send replies to a destroyed agent and distort costs.

## Mechanism
Checked against the 8.9.10 model *Field Service Phase 5* and Help 8.9.10 (*Dynamic creation and destruction*,
*ResourcePool*).
1. **Bind the population size to a top-level parameter** (`ServiceCapacity`, int). The population's initial number reads
   it, so it can be an experiment input.
2. **In the parameter's On change on Main:**
   - while the population is smaller than the parameter, call `add_service()`;
   - then send every crew `"CHECK IF LAID OFF"`.
3. **Each crew decides only at safe points:**
   - on finishing a job, via the Finished transition;
   - on receiving the notice while idle or heading home, via a transition on the composite state's border.

   Both lead to one branch that tests `getIndex() >= main.ServiceCapacity`. If it holds, the crew enters a final
   state whose action is `main.remove_service(this)`. Otherwise it carries on.
4. **Busy crews finish first.** A crew in the middle of a job ignores the notice, completes the job, then re-checks and
   leaves. If capacity rises again before that, it simply stays.
5. **Cost the time-averaged headcount, not the end-of-period count.** Feed `service.size()` into a *Continuous*
   Statistics element and bill `mean()` × daily cost × days (book p. 41).

**Contrast with DES (Help *ResourcePool*):** `set_capacity(n)` resizes a pool, and busy units above the new capacity
stay until released. *When capacity decreases* then decides their fate:
- `destroyExcessUnits = false`: kept off shift, the default;
- `true`: destroyed.

With agents, you write that policy yourself.

## Resources
Population `service` of `ServiceCrew`; parameter `ServiceCapacity` on Main.

## Key settings worth copying
- Population API: `add_<population>()` returns the new agent; `remove_<population>(agent)` removes and destroys it. An
  agent removes itself with `main.remove_<population>(this)` (Help).
- Change the parameter from a control with `set_ServiceCapacity(v)` so that On change runs. A plain assignment skips it,
  and On change also skips unchanged values (see `videos/statechart-live-controls-trigger-reevaluation.md`).
- Radio buttons return a 0-based index. In the book's panel (ch. 4 p. 39):
  - the crew-count group calls `set_ServiceCapacity(value + 1)`, with default `ServiceCapacity - 1`;
  - the policy group maps to a boolean (`value == 1`);
  - the edit box for the age threshold is linked to its parameter and enabled only while the policy is on.

## KPIs instrumented
Time-averaged crew count, annual crew cost, and crews per state over time. The time averages come from a
*Continuous* Statistics element reset each year by a cyclic event.

## Pitfalls
- **Index order is not fairness.** The highest-indexed crews go, even when busy, while lower-indexed idle crews stay.
  The cut therefore takes effect late. If it must act at once, pick idle crews first and mark them with a flag
  (design judgement).
- **`getIndex()` is linear-time.** The Javadoc 8.9.10 notes it scans the list. That is fine for tens of agents but
  costly in large populations or frequent checks.
- **Dangling references.** Clear every reference to an agent before removing it: queue entries and the unit's
  `serviceCrew` variable. The book's scheme is safe because a crew leaves only after its unit has released it.
- **Keep the check on the Finished path.** A notice reaching a crew outside the composite state, such as one driving
  to a job, is ignored. The re-check after the job is what catches it; don't remove it.

## Reusable idea
Grow the population at once; shrink it only at points the agent itself chooses; account for it with time averages.

## When the co-pilot should use this
- Live staffing or fleet-size controls in agent-based models; shift patterns that add and drop vehicles or crews
  mid-run; any agent population that stands in for a resource pool.
- Related: `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`,
  `basicmodels/implementing-work-shifts-for-resources.md` (the DES route).
