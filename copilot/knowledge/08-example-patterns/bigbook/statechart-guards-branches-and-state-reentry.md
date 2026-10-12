# Pattern card — Statechart transition semantics: guards that disarm, self-loops that re-arm, branches and history
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 7 "Designing state-based behavior: statecharts" — distilled, original wording
- **Paradigm:** Method (statecharts in ABM, DES and hybrid models)
- **Problem it solves:** Agents freeze or change timing silently because a guard, a loop or a branch does something other than what the drawing suggests.

## Mechanism
Checked against Help 8.9.10 (*Transition*, *Branch*, *History state*, *Execution order*, *Statechart functions*). Items only in the book are marked (Big Book).
1. **A false guard can disarm a trigger for good.** The guard is read only at the instant the trigger fires ("guards-after-triggers", Help). If it is false at that instant (Big Book p. 17):

   | Trigger | What happens next |
   |---|---|
   | Timeout | disarmed; fires again only after the source state is re-entered |
   | Rate | disarmed until the rate value changes |
   | Condition | keeps watching; fires when condition and guard next hold together |
   | Message / Agent arrival | waits for the next matching message / next arrival |

   So `Timeout: 5 min` with `Guard: queue.size() > 0` strands the agent forever if the queue is empty at minute 5, with no error.
2. **Guard is not condition.** A Condition trigger is watched while the transition is active. A guard is a one-time check at trigger time. Put "wait until X" in the trigger.
3. **An outside self-loop restarts the state's clocks; an inside one does not.** A loop drawn outside the state exits and re-enters it: exit and entry actions run, and every Timeout leaving that state starts again (Help: a timeout counts from entry into its source state). That is the tool for an inactivity timer; in the book's laptop, each key press loops back and restarts the 5-minute screen-off timeout. A loop drawn wholly inside the state is internal: nothing is exited, so a trip-length timeout keeps running while calls fire inside it (Big Book pp. 1, 18–19). Likewise a Timeout on a composite state's border counts from entry into the composite, so moves between its inner states never reset it. That makes it a natural overall deadline.
4. **Branches.** Control never rests in a branch, and branch exits carry conditions, not guards. Per Help, the first exit whose condition is true is taken; with none true and no *Default* exit, a runtime error. The book warns the pick is nondeterministic when two are true. Make conditions mutually exclusive and give every branch one Default.
5. **`msg` does not reach the branches.** The received message is in scope only in the triggered segment. Copy it in that segment's Action (`x = msg;`) and test `x` in the branch conditions (Big Book p. 18).
6. **Interrupt and resume.** Draw a composite state around the states that share a reaction (breakdown, low battery, suspension); one transition from its border fires from whichever inner state is active. Come back through a History state:
   - *shallow* returns to the last state on that level and then follows its initial pointer;
   - *deep* returns to the last simple state;
   - with no history yet, control goes to the initial state (Help).

   A repair that should resume the interrupted Busy/Idle state therefore targets an H inside Operational, not Idle. History restores *which* state is active, not its clocks: resuming is a new entry, so the state's timeouts are evaluated and start again (Help *Transition*; gotcha G75). If progress must survive a pause, use a *User control* event with `suspend()` / `resume()`, or store the remaining time.
7. **Action order** (Help *Execution order*):
   1. exit actions, from the current simple state outwards to the outermost state being left;
   2. the transition's action;
   3. entry actions, inwards to the new simple state.

   Branch and initial-pointer actions run as control passes them. A composite state that the transition stays inside is neither exited nor entered. All actions take zero time.
8. **Parallel concerns need separate statecharts.** Orthogonal regions are not supported, so give one agent several statecharts and couple them with guards; for example, the engine starts only if `gearbox.isStateActive(Parked)`. State and transition names belong to the agent, so they must be unique across all of its statecharts (Big Book p. 23).

## Resources
n/a

## Key settings worth copying
- **Statechart API (Help):** `isStateActive(S)` (simple or composite); `getState()` / `getActiveSimpleState()`; `getFullState()`.
- **Agent API:** `inState(S)`. From outside the agent, `truck.inState(Truck.Moving)`.
- **Transition API:** `isActive()`; `getRest()` and `getRest(MINUTE)`, which return infinity when nothing is scheduled.
- **State API:** `getContainerState()`, `getStatesInside()`, `containsState(s)`, `isSimpleState()`.
- **Initial state by attribute:** the entry point may lead to a branch, so agents start in different states, e.g. a life phase chosen by age at creation (Big Book p. 25).

## KPIs instrumented
Debugging aid:
- At runtime the active states are outlined, and the transitions that just fired or are scheduled are highlighted. Timeout and Rate transitions show their time to fire.
- The developer panel's *Events* view lists scheduled transitions separately from monitored Condition transitions (Big Book p. 24).
- An agent stuck in a state with an entry in neither list has lost its trigger: see item 1, G21 or G56.

## Pitfalls
- A guarded Timeout (item 1): move the test into a Branch after the timeout, with a Default exit.
- An outside loop on a state that owns a long timeout resets the timeout on every loop. Draw the loop inside the state, or move the periodic job to an event.
- Branch conditions with gaps (runtime error) or overlaps (arbitrary pick).
- `msg` read in a branch condition does not compile (item 5).

## Reusable idea
For every transition, write down what arms it (entry into which state), what can disarm it (a false guard, a re-entry, an unheard message), and what wakes it (its own timer, a message, `onChange()`). Then draw it.

## When the co-pilot should use this
- A user reports an agent stuck in a state with no error, a timer that keeps restarting, or a branch that picks oddly.
- Designing breakdown/repair, suspend/resume, life-phase or multi-statechart agents.
- Related: G21, G56, G60, and `videos/abm-adoption-flow-counters-vs-state-counts.md` (an outside loop reruns entry actions).
