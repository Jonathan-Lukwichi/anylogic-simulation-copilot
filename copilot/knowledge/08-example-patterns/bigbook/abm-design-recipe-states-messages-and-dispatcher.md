# Pattern card — Designing an agent-based model on paper: state splits, message sequences and a function-based dispatcher
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 4 "How to build agent-based models. Field service example" — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Turning "many objects raise requests, mobile teams serve them" into agents whose statecharts, messages and shared queue neither lose requests, double-book a unit nor strand a team.

## Mechanism
1. **Ask the design questions in this order** (ch. 4 p. 1):
   - Which objects matter? They become the agents. Which relations persist? They become links or reference variables.
   - Does space matter (GIS, continuous or discrete)? Which events happen to each agent, from outside or from within?
   - Then map each behaviour to a construct:

   | The agent… | Construct |
   |---|---|
   | only reacts to stimuli | functions and message handlers |
   | has modes | statechart |
   | has its own timing | events, Timeout or Rate transitions |
   | runs an internal process | flowchart inside the agent |
   | has continuous dynamics | stock-and-flow inside the agent |

   Memory goes in variables and states. Anything shared (map, queue, dispatcher) lives on the top level. Plan outputs
   at both the individual and the population level.
2. **Split a state only when it earns it.** Split when the duration differs, when the same message must mean something
   different, when exit behaviour differs, or when you want time-in-state statistics. The failed unit's states qualify:
   waiting for a crew, repair, replacement, maintenance.
3. **Keep the mover's destination in its state** (`DrivingToWork` vs `DrivingHome`) rather than testing the location
   on arrival. Transitions take no time, so fold an inspection into the next state's duration.
4. **Walk the message sequences before coding** (ch. 4 pp. 9–12). Draw one lifeline per agent, then play the awkward
   cases: two failures and one crew; one request and two idle crews; a notice that arrives while a crew is busy or
   heading home. An ABM behaves like a distributed system: notices get ignored in the wrong state, simultaneous
   checks race, and replies go to agents that have moved on. Each case you find becomes a state, a queue rule, or a
   transition on a composite state's border; here, that border transition lets crews heading home accept work. The
   diagram is a paper aid; AnyLogic has no such element.
5. **A dispatcher without state or timing is just functions on Main** (ch. 4 pp. 12–15, 27–28):
   - The queue is a collection on Main (*LinkedList*, element type `EquipmentUnit`).
   - `requestService(unit)` and `requestMaintenance(unit)` append to their own list, then send every crew
     `"CHECK REQUEST QUEUE"`.
   - `thereAreRequests()` tests whether either list has entries. `getRequest()` takes from the head of the repair list
     first, and from the maintenance list only when no repair is waiting.
   - The unit's own reference is the request. Switch to a request class once requests need a time, priority or type
     (as in `basicmodels/maintenance-phase-1.md`).
6. **Refuse duplicates at the door.** A repair request cancels the same unit's pending maintenance request. Any request
   is dropped while a crew already holds that unit, and a maintenance request is dropped while that unit's repair
   request waits. The unit's state when the crew arrives decides the work: working means maintenance, failed means
   repair or replacement. So a crew sent to service a unit that fails meanwhile repairs it instead.
7. **Pair agents through typed references.** The crew sends itself as the message (`send(this, equipmentUnit)`). The
   unit stores it (`serviceCrew = msg`), later replies with `send("FINISHED", serviceCrew)`, then sets the variable to
   `null`. A typed variable names the relation; `connectTo()` gives an untyped two-way link (Javadoc 8.9.10).

## Resources
Populations `equipment` (50 `EquipmentUnit`) and `service` (`ServiceCrew`, sized by `ServiceCapacity`); no process blocks.

## Key settings worth copying
- Replace-or-repair branch: `randomTrue(ProbabilityReplacementNeeded)`. Service-after-repair branch:
  `timeSinceMaintenance() > MaintenancePeriod`. Every branch has a default exit.
- Crew: the notice arrives on the border of a composite state around `Idle` and `DrivingHome`. A branch then tests
  `main.thereAreRequests()`:
  - if true: `equipmentUnit = main.getRequest(); moveTo(equipmentUnit);`
  - otherwise: `moveTo(main.home)`.
- Costs: each finishing transition adds its operation cost to one accumulator on Main (`main.WorkCost += …`).

## KPIs instrumented
Units and crews per state, from population statistics with state conditions, shown on a time stack chart at 100 %
scale in the state colours. In 8.9+ the condition is `agent.inState(...)`; the book's `item.inState(item.Working)`
(pp. 31–32) fails (G53). Revenue comes from the time-averaged number of working units (Statistics, *Continuous*).

## Pitfalls
- **Broadcast-and-race.** Every crew hears the notice, so simultaneous-event order picks the crew (G60). A crew already
  on the road may lose to one at the depot. If distance matters, let the dispatcher choose, e.g. the idle or homeward
  crew with the smallest `distanceByRoute(unit)` (Javadoc 8.9.10), and message only that crew. This is judgement: the
  book's crews do not optimise routes (assumption 6, p. 49). For a KB dispatcher that picks explicitly, see
  `findTransport()` in `basicmodels/maintenance-phase-5.md`.
- **Release code in an entry action also runs when the statechart starts,** because the initial state's entry action
  runs too (Help *Execution order*). Keep "release the crew" in the transitions into `Working`, as the book does.
- **"Typical" durations.** `triangular(0.5*T, T, 2.5*T)` averages 1.33 T, not T (G55).

## Reusable idea
Play the three worst coincidences on paper, make a stateless dispatcher a set of Main functions, and let the
receiver's current state decide what a message means.

## When the co-pilot should use this
- Field service, maintenance crews, taxi or ambulance dispatch, and any "many requesters, mobile servers" ABM.
- A user's ABM loses requests, double-books a unit, or leaves a mover idle while work waits.
- Related:
  - `models/field-service.md`;
  - `bigbook/statechart-guards-branches-and-state-reentry.md` and `bigbook/statechart-message-queue-and-safe-handoff.md`;
  - `bigbook/abm-time-dependent-hazard-rate-refresh.md` and `bigbook/abm-runtime-resizing-of-a-busy-agent-population.md`.

## Additions (8.9.10 review, 2026-10-01)
- Typed relations: *Link to Agents* elements — in 8.9.10 split into *2-Way* and *1-Way Link to Agents* (release notes) — give typed single or collection links whose peer ends stay in sync and clean themselves up when an agent is destroyed (8.9.10 engine bytecode), and can draw themselves (`bigbookmodels/kinship-model-with-customized-statistics.md`).
- Dispatcher races: an idle check followed by `send()` double-books a crew when two requests coincide (gotcha G77; `videos/dispatch-idle-check-then-send-double-booking.md`).
