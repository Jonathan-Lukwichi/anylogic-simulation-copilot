# Pattern card — "Find an idle vehicle, then message it": the double-booking race in agent dispatch
- **Source:** AnyLogic 8.9.10 Help tutorial "Wind Turbine Maintenance (Agents)" — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Stop a dispatcher that picks an idle crew by its state and then notifies it from giving one vehicle two jobs, losing a request and closing the wrong work order.

## Mechanism
The tutorial's dispatch, as built in the 8.9.10 model *Maintenance - Phase 7*:
- A turbine's state entry calls `sendRequest(type)`. It creates `new ServiceRequest(type, this)` and calls Main's
  `findTransport(req)`, which walks `trucks` or `helicopters` and returns the first vehicle with
  `inState(Transport.AtCenter)`, else `null`.
- Vehicle found: `t.request = req; send(req, t);`. None free: the request is appended to `autoRequests` or
  `aviaRequests` (LinkedList collections on Main).
- Vehicle statechart: `AtCenter` →(message of type ServiceRequest; `moveTo(msg.turbine)`) `MovingToTurbine` →(arrival)
  `Servicing` →(timeout `type == AVIA ? uniform(10, 20) : 10` h; `send("repaired", request.turbine); moveTo(main.center);
  request = null;`) `MovingToMC` →(arrival) branch: a queued request of its type → take the head and `moveTo` it; else `AtCenter`.

**The race.** `send()` delivers in a separate event after the current one, at the same model time (Help 8.9.10,
*Communication between agents*). Until then the vehicle is still `AtCenter`, so a second `findTransport` in that window
returns the same vehicle. Then:
1. `t.request` is overwritten by the second request;
2. the first message sends the vehicle to turbine 1; the second arrives in `MovingToTurbine`, where no transition takes a
   ServiceRequest, and is discarded (G21);
3. after servicing turbine 1, `"repaired"` goes to `request.turbine`, i.e. turbine 2. Turbine 1 stays down for good,
   turbine 2 recovers without a visit, and no queue holds turbine 1's job. No error is raised.

It is certain when two requests are raised inside one action (a loop over assets, a start-up batch, a shift-start event).
For requests from separate events at the same instant it depends on the engine's simultaneous-event order (LIFO by
default since 8.6, G60), which a model must not rely on. The tutorial escapes only because failures are rate-driven and
each turbine's first scheduled visit is random, so exact ties are practically impossible *(reasoned from the model code
and the Help; not run)*.

## Resources
5 trucks (AUTO, 70 km/h) and 2 helicopters (AVIA, 200 km/h) at one depot `center`; 25 turbines. `Truck` and `Helicopter`
extend `Transport`, which owns the statechart; each subtype sets `type` in its On startup.

## Key settings worth copying
- **Claim in the same step as the check.** `if (t.inState(Transport.AtCenter) && t.request == null) return t;` works here
  because `request` is set synchronously at dispatch and cleared after service. Alternatives: an idle list that the
  dispatcher removes from (the vehicle re-adds itself in `AtCenter`'s entry action), or a PML ResourcePool, whose Seize
  reserves a unit at once.
- **Tie the reply to the job.** Send the `ServiceRequest` object back rather than a bare `"repaired"`, and let the turbine
  accept only the request it has open.
- Short-lived requests live in LinkedList collections on Main, not in a population (the tutorial's reasoning).
- Staggered periodic work: a cyclic event per turbine, First occurrence `uniform(0,14)` **days**, Recurrence `serviceTimeout`
  (2 weeks), action `statechart.receiveMessage("scheduled")`. Failures: Rate `1/MTTF` per day, MTTF = 50 days.

## KPIs instrumented
None in the tutorial. Add: requests raised vs requests completed per turbine (they must match), request-to-repair time,
vehicle utilisation (time outside `AtCenter`) and turbine downtime.

## Pitfalls
- **Test for it.** In one action, raise two AUTO requests while only one truck is idle, then check that both turbines
  get serviced and each receives exactly one completion.
- **Nested states change the KPI.** `ScheduledService` sits inside `Operating`, so availability read from
  `inState(Operating)` counts scheduled work as up-time, and the blades keep turning (`inState(Operating) ? time() : 0`).
- **Crossed jobs.** The Failure transition leaves the composite `Operating`, so a turbine can fail while a truck is on the
  way or working. The truck's `"repaired"` then ends the failure, and the helicopter later "repairs" a working turbine.
  `bigbook/abm-design-recipe-states-messages-and-dispatcher.md` shows the fix: let the unit's state decide the work.
- **Deadheading and bias.** A vehicle looks at the queue only after driving back to the depot, and `findTransport` takes
  the first idle vehicle in population order, not the nearest (compare G44). Both are policy levers, not neutral defaults.

## Reusable idea
"Check, then notify" is two steps with a gap between them. Make the reservation in the same step as the check, and let
every reply carry the identity of the job it closes.

## When the co-pilot should use this
- Any explicit dispatcher over mobile agents: field service, maintenance crews, taxis, ambulances, AGVs driven by statecharts.
- Symptoms: an asset never gets repaired, a vehicle "serves" the wrong customer, requests raised vs completed do not add up.
- Related: G21, G24, G60; `bigbook/statechart-message-queue-and-safe-handoff.md`; `basicmodels/maintenance-phase-5.md`.
