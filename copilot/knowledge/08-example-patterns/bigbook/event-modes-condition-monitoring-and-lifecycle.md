# Pattern card — Event elements: choosing the mode, keeping a Condition event alive, and when conditions are really tested
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 8 "Discrete events and Event model element" — distilled, original wording
- **Paradigm:** Method (any paradigm)
- **Problem it solves:** Events that fire once too often or never, at the wrong absolute time, or after the moment they were meant to catch.

## Mechanism
Checked against Help 8.9.10 (*Event*, *Dynamic event*, *Model time*). Book-only items are marked.

**Which set-up for which job** (condensed from Big Book pp. 4–5):

| Job | Event set-up |
|---|---|
| Arrivals or births in an agent-based model | Rate, or Cyclic with a random recurrence |
| Periodic review, reporting, custom statistics | Cyclic with a fixed recurrence |
| Delayed action outside any flowchart ("door closes in 5 s") | Timeout, *User control*, armed with `restart(dt)` |
| React when a threshold is reached | Condition |
| Scripted change or demo step at a known time | Timeout, *Occurs once* |
| Code at time 0 that must run **after** every On startup | *Occurs once* at time 0 (Help) |
| Many concurrent timed items, each carrying data | Dynamic event, `create_Name(dt, args…)` |

**Condition events** (Help *Event*):
- **They fire once, then stop watching.** To keep watching, end the action with `restart()`, but first make the condition false; otherwise the event fires again at the same instant, in a loop.
- **When they are tested:**
  - on anything that happens in the same agent: its events, transitions, messages, a parameter's On change, a control;
  - on a call to `onChange()`;
  - at every solver step, if the model has any continuous (SD) variables — and then for every armed condition in every agent, not only the agent that holds the SD part (Big Book ch. 8 p. 10; 8.9.10 engine bytecode; Help words it per agent). A time-only condition in an SD-free agent may therefore fire on time only while some SD exists (gotcha G56).

  Changes inside embedded agents, or anywhere else, are not seen.
- **Polling conditions that depend on embedded agents or populations** (Help): tick *Enable synchronous steps* on the container agent and put `onChange();` in the On step of the agent that holds the conditions. This is cheaper than one cyclic event per agent.
- **Movement is only two events,** departure and arrival. A condition such as `distanceTo(target) <= 50` on a moving agent is not re-tested on the way (Big Book p. 11). Poll it with a cyclic event or on synchronous steps, with a step short enough for the speeds involved.
- **Continuous values:** test with `>=` or `<=`, never `==`, because an integrated stock can step past 100. A value that crosses a threshold and comes back between two solver steps is missed; tighten the numerical accuracy (Help: *sensitivity problem*).
- **Hysteresis pair** (Big Book p. 12). Two events re-arm each other:
  - `stockAt100`: Condition `stock >= 100`, Action `flow = 0; stockBelow100.restart();`
  - `stockBelow100`: Condition `stock < 100`, Action `flow = 10; stockAt100.restart();`

  A flow that an event sets must be ticked *Constant*, or the SD equations overwrite it.

## Resources
n/a

## Key settings worth copying
- **Timeout event API** (Help):
  - `restart()`, `restart(dt)`, `restart(dt, MINUTE)`;
  - `restartTo(t)` and `restartTo(date)`, which avoid the rounding error of `restart(t - time())`;
  - `reset()`, `getRest()`, `isActive()`;
  - `suspend()` / `resume()`: a countdown that pauses and keeps its remaining time. Called from the event's own action, `suspend()` acts as `reset()`.
- **Rate event:** a rate set to 0 or below cancels the event. After making it positive again, call `restart()` (Help).
- **Cyclic recurrence** is re-evaluated after each occurrence, so it may be random or state-dependent *(Big Book p. 8; Help 8.9.10 confirms it indirectly by recommending a recurrence of `toTimeoutInCalendar(DAY, 1)`, which works only if the field is re-read each time — gotcha G63)*.
- **Dynamic events:** an instance exists only while scheduled. Keep its handle to cancel it: `Delivery d = create_Delivery(dt, order); … d.reset();`. `getDynamicEvents()` returns an agent's active instances (Help *Dynamic event*).
- **Demo pacing:** an *Occurs once* event on a calendar date can call `getEngine().setRealTimeMode(true)` to skip a warm-up fast and then slow down (Big Book p. 15; ch. 16 in batch book-3).

## KPIs instrumented
n/a. For debugging, the developer panel's *Events* view lists every scheduled event (e.g. `root.Delivery`) with its time to fire.

## Pitfalls
- **Absolute times inside agent types.** *Occurs once* and a Cyclic event's first occurrence are absolute model times (Help):
  - an agent created after that time never fires its Occurs-once event;
  - a Cyclic event is phased as if it had started at time 0.

  For "N units after this agent appears", put `time() + N` in the first-occurrence field, or use a User-control event restarted in On startup.
- **Months and years as timeout units are fixed lengths,** 30 and 365 days (Help *Model time*). For calendar-exact times use `toTimeoutInCalendar(...)` or `restartTo(date)`.
- **Simultaneous-event order is no longer an experiment setting.** It was removed in 8.6, with LIFO the default (release notes), so the FIFO/LIFO/Random dropdown in Big Book ch. 8 pp. 3–4 is outdated. Keep models insensitive to it (G60).

## Reusable idea
For every event, answer three questions: who arms it, is its time absolute or relative, and who re-arms it after it fires?

## When the co-pilot should use this
- Any Event element in a generated model, above all Condition events, events inside agent types, and "after start-up" actions.
- Symptoms: an event fires only once, an endless zero-time loop, a threshold is missed, a late-born agent's event never fires.
- Related:
  - gotchas G46 (start-up order), G56 (`onChange`), G60 (simultaneous events);
  - `videos/abm-stock-gated-purchase-allocation-and-brand-tie.md` (the restart pattern);
  - `models/competition-in-global-pulp-market.md` (zero-delay dynamic events).
