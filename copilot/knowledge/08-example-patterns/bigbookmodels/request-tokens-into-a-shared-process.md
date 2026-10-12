# Pattern card — Request tokens into a shared process: back-reference, callback, agent-owned reneging (Epidemic and Clinic, User Satisfaction, Cell Phone Users)
- **Source:** AnyLogic example models "Epidemic and Clinic", "User Satisfaction", "Cell Phone Users and Network Capacity" (bigbookmodels/Multimethod), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid
- **Problem it solves:** Agents that keep living their own lives (patients, subscribers, phone users) need a shared, capacity-limited service, must learn the outcome, and may give up — without moving the agent itself through the flowchart.

## Block chain
On Main: `Enter` → `Queue` (maximum capacity) → `Delay` (capacity = number of servers) → `Sink`.
1. **Request.** A transition action creates a small agent type holding a typed back-reference and pushes it in:
   `main.requestTreatment.take(new TreatmentRequest(this));` (Epidemic, on developing symptoms),
   `main.enter.take(new Request(this));` (User Satisfaction, service issue at rate 1),
   `main.enter.take(new Transaction(this, time()));` (Cell Phone, every 5 minutes while online).
2. **Callback** in the Sink's On enter: `send("Treated", agent.patient);`, `send("Completed", agent.user);` — a message
   transition in the agent fires — or a direct call carrying a measurement:
   `agent.user.UpdateExperience(time() - agent.timestamp);`.
3. **Reneging owned by the agent** (Epidemic). In `Infected`, the message transition "Treated" races a Timeout
   `IllnessDuration * uniform(0.5, 2)`. If the timeout wins, its action calls `main.cancelTreatmentRequest(this)`, which
   scans `wait` and then `treatment` for the token whose `patient == this` and removes it; `error(...)` if absent.
4. **Measured experience** (Cell Phone). The callback appends the response time to a DataSet of capacity 100; once it
   is full, the mean of the last 100 becomes `AverageResponseTime` and the function ends with `onChange()`, so the
   condition `AverageResponseTime > 3 * minute()` (to `FrustratedUser`) is re-tested. Forgiving resets both
   (`RecentExperience.reset(); AverageResponseTime = 0;`).
5. **Main talks to everyone** (User Satisfaction): the Promotion button runs `sendToAllAgentsInside("Promotion")`;
   frustrated users take `Satisfaction += 5`.

## Resources
A `Delay` with capacity n stands in for n parallel servers (20 treatment places, 66 agents, 10 servers), each linked to
a slider (`treatment.capacity`, `service.capacity`, `servers.capacity`). Help *Delay*: after a cut, agents already
inside finish and newcomers wait until the count falls below the new capacity.

## Key settings worth copying
- **Enter → Agent type** = the token type, so `agent.patient` compiles downstream (G23).
- **Keep the token in the agent** instead of scanning: `myRequest = new TreatmentRequest(this);` then, on giving up,
  `if (main.wait.remove(myRequest) == null) main.treatment.remove(myRequest);` — Help: Queue `remove(agent)` returns
  null when the agent is not there; Delay supports removing agents too.
- **Dispose of withdrawn tokens.** A removed token is in no block and is never disposed (Help *Sink*): take it into an
  `Enter` → `Sink` named `cancelled`, which also counts reneges, or call `tr.deleteSelf()` *(inferred from Help)*.
- **Moving window without a loop:** set the DataSet's *Keep up to 100 latest samples* and read `getYMean()` (Help
  *Data set*); the model's `for` loop over `getY(i)` computes the same mean.
- **Remote change, then wake:** a variable changed by another agent's event is invisible to this agent's conditions
  until `onChange()` (G56).
- **Messages from Main work:** all three models call `send(msg, agent)` from Main's Sink. Only space-addressed sends
  (`sendToAll`, `sendToRandom`) need the sender to live in a space (engine 8.9.10 — narrower than G22 as currently
  worded). Main reaches all its embedded agents with `sendToAllAgentsInside(msg)`.

## KPIs instrumented
Population state counts (`NInfected`, `nUsing`, `NFrustrated` …) on time stack charts. Worth adding: token waiting
time (timestamp at Enter, read at Sink), cancelled-token count, and the response-time distribution.

## Pitfalls
- **The window needs a full buffer.** No frustration is possible before 100 transactions (about 8 online hours at one
  per 5 minutes). Size the window to the behaviour you mean to model.
- **`error("Agent not found")`** stops the run on an unexpected ordering — good while debugging; count instead in
  production.
- **Quoted service times.** `triangular(10, 30, 150) * second()` averages 63 s, not 30 s (G55).

## Reusable idea
When the requester must keep its own behaviour going while it waits (fall ill, go offline, gossip), send a proxy into
the process: the token queues and is served, the agent keeps its statechart, and the Sink closes the loop. Prefer the
agent itself (`videos/statechart-agent-through-hosted-flowchart.md`) when it is physically in the process; prefer
tokens when it is not, when one agent can have several requests at once (Cell Phone), or when it may withdraw.

## When the co-pilot should use this
- Patients requesting care, customers raising tickets, users generating transactions, machines requesting service.
- Any hybrid model where service quality feeds back into agent behaviour (satisfaction, churn, word of mouth).
- Related: `bigbookmodels/multimethod-interface-catalogue.md`, `models/epidemic-and-clinic-with-accumulating-concern.md`,
  `videos/abm-stock-gated-purchase-allocation-and-brand-tie.md`, G21, G22, G23.
