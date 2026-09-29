# Pattern card — Live controls on statechart agents: when a changed parameter reaches Timeout, Rate and Condition triggers
- **Source:** AnyLogic video "AnyLogic ABM Tutorial Part 8 | Modelling Consumer Impatience" (https://youtu.be/iVOqcz5iZTw) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** A slider moved during a run changes a parameter, but agents already waiting in a statechart state keep their old behaviour, so the live what-if looks delayed, weaker or dead.

## Mechanism
The video is the Market model's impatience phase (3-days pp. 80–91). It puts two levers on Main, each linked to a slider with step 1: `MaxDeliveryTime` (5–25) and `MaxWaitingTime` (2–15). The consumer statechart reads them in the two Timeouts that leave `WantsToBuy`, both in days:
- Purchase: `triangular(1, main.MaxDeliveryTime, 2)`.
- CantWait: `triangularAV(main.MaxWaitingTime, 0.15)`.

The video never says *when* a moved slider reaches the agents. Help 8.9.9 (*Transition*, *Agent API*) does:

| Trigger | Its expression is read… | Do agents already in the source state see a change? |
|---|---|---|
| Timeout | once, when the statechart enters the source state | No. Only agents that enter later use the new value. |
| Rate | on entry, and again each time `onChange()` runs for that agent (then rescheduled with a fresh exponential draw) | Only after that agent's `onChange()`. The engine calls it by itself only when the agent originates an event or receives a message. |
| Condition | when something changes *in that agent*: its own event, a received message, its parameter's On change, or `onChange()` | Not when only Main or another agent changed. |
| Message | on delivery | n/a |

In the Market model this means:
- **Either slider** affects only consumers who enter `WantsToBuy` afterwards. Those already waiting finish on their old draws, so the response lags by up to one waiting episode (up to 25 days).
- **A slider on the advertising rate is the silent case.** `Ad` is a Rate transition out of `PotentialUser`, and a potential user has no events until its own Ad timer fires. It re-reads the rate only when a word-of-mouth message happens to reach it. With ads as the only channel, the slider changes nothing for the existing pool.

## Resources
n/a

## Key settings worth copying
- **Push the change.** Add `for (Consumer c : consumers) c.onChange();` to the slider's *Action*, which runs every time the control is touched. Rate and Condition triggers then re-read at once, and the fresh exponential draw is statistically exact (memoryless). If code elsewhere also calls `set_X()`, put the loop in the Main parameter's *On change* field instead. That field runs only on `set_X()` calls, and not when the value is unchanged (Help).
- **Where the lever lives:**
  1. On Main, read as `main.X` (the video's choice). Every agent gets one value, and the lever can be an experiment input, because experiments set only top-level parameters (G9; *Compare runs experiment* Help). Changing it notifies no agent.
  2. In the agent type, bound to a Main parameter in the population's properties (Help: *parameter propagation*; both must have the same type). Changes on Main flow into every agent's parameter. Whether that alone re-reads their rates is *(unverified)*, so call `onChange()` anyway.
  3. In the agent type, with a per-agent random default. This gives heterogeneous agents but no experiment lever.
- **A deadline that must follow the slider** (only when agents already waiting must obey a new threshold):
  1. Replace the CantWait Timeout with a *User control* Event `patience` in `Consumer`.
  2. On entering `WantsToBuy`, store `waitStart = time()` and `pf = triangularAV(1, 0.15)`, then call `patience.restartTo(waitStart + pf * main.MaxWaitingTime * day())`.
  3. The event's action is `statechart.fireEvent("cantWait")`. It fires CantWait, which is now Triggered by that message.
  4. Call `patience.reset()` on exit.
  5. The slider's Action repeats the `restartTo(max(time(), …))` call for every agent in `WantsToBuy`.

## KPIs instrumented
The video shows only the state stack chart. To see the lag, count exits per transition (a counter incremented in the Purchase and CantWait actions) and plot the daily CantWait share around the moment the slider moves.

## Pitfalls
- **Reading a slider's effect in the first days after moving it.** You are mostly watching old draws.
- **Using mid-run moves as evidence.** They also break reproducibility (G17). Change inputs between runs instead, as Part 9 of the series does with a Compare Runs experiment, and use replications for any number. For inputs read while the model is built, use pre-run controls (`experiment-page-pre-run-controls.md`).
- A rate that becomes negative after a change throws a runtime error (Help).

## Reusable idea
Treat each live control as an intervention with a delivery path. For every trigger it feeds, decide whether agents already waiting must see the new value:
- For Rate and Condition triggers, push it with `onChange()`.
- For deadlines, use a re-armable Event.
- Otherwise, label the control "applies to new arrivals".

## When the co-pilot should use this
- A user adds sliders or edit boxes to an agent-based or statechart model, or reports "I moved the slider and nothing happened" or "it reacted late".
- Building interactive demos or decision tools in which stakeholders move levers during a run.
- Reviewing any Rate or Condition trigger that reads Main or another agent's data.
