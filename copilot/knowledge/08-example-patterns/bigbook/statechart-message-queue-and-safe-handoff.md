# Pattern card — Messages into statecharts: the zero-time queue, fireEvent vs receiveMessage, and a hand-off that cannot be lost
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 7 "Designing state-based behavior: statecharts" — distilled, original wording
- **Paradigm:** Method (ABM and hybrid statecharts)
- **Problem it solves:** Get a notification into a statechart so it is neither lost nor taken by the wrong transition, and detect when it was not heard.

## Mechanism
Checked against Help 8.9.10 (*Transition → Statechart queue*, *Statechart functions*).

| Call | Queued? | Returns | Behaviour |
|---|---|---|---|
| `statechart.receiveMessage(m)` | no | `true` if an active transition matched | Matched at once or discarded. If two simultaneous messages match the same trigger, the second is ignored. |
| `statechart.fireEvent(m)` | yes, for the current instant only | void | The queue is scanned oldest first. A matching message is consumed **together with every older message still waiting**. Messages still unmatched are dropped once model time moves on. |

- **Messages sent to the agent** (`send`, `sendToRandom`, …) reach its statecharts only if they are ticked in the agent's *connections* → *Forward message to*. Forwarding uses `fireEvent()` (Big Book p. 15).
- **What this adds to G21.** "Discarded if nothing matches" is true once time advances. Within one instant, though, a burst of messages is worked through: the statechart takes several zero-time steps, one per message, as long as each message matches a transition made active by the step before. The flip side: an unrelated older message is silently thrown away when a newer one matches.
- **Matching order** (Help):
  1. The type filter comes first: `int`, `double`, `boolean`, `String`, or a class name. `Object` lets everything through.
  2. Then one of: *Unconditionally*; *On particular message*, which compares with `equals()`; or *If expression is true*, which reads the message as `msg`.

## Resources
n/a

## Key settings worth copying
- **Use an Option List for commands.** For a finite command set (SEIZE/RELEASE, ESPRESSO/LATTE…), make the message type an Option List (Big Book p. 14). A misspelt option will not compile; a misspelt String compiles and strands the agent (G21 cause 2).
- **Use a class for payloads.** When a message carries data (sender, order id, quantity), set the message type to a class or agent type with fields, and filter on `msg.qty > 0`.
- **Detect a lost command** *(suggested pattern)*. `receiveMessage` reports whether anyone listened, so the sender can keep the command and retry:
  `if (!truck.statechart.receiveMessage(Cmd.GO)) pendingGo.add(truck);`
- **Latch when the order of events is uncertain** *(suggested pattern)*. The notifier may act before the receiver reaches its waiting state. Instead of a message:
  - set a flag on the receiver: `receiver.released = true; receiver.onChange();`
  - let the waiting state's exit be a Condition `released`, with Action `released = false;`

  Help says a Condition that is already true on entry fires at once, so an early notice waits in the flag. A message sent too early is gone.

## KPIs instrumented
Count commands that found no listener (`receiveMessage` returned false), by type. In a model that relies on hand-offs, any non-zero count is a wiring bug.

## Pitfalls
- A message may arrive while the statechart is executing a transition. Only the queue (`fireEvent`) holds it until the statechart can react (Help *Statechart queue*); `receiveMessage` would drop it.
- One message can match transitions on nested levels at once. All matches get scheduled, and firing one can cancel the others (Big Book p. 14). Keep triggers of inner and outer states distinct.
- *On particular message* uses `equals()`. With a custom message class, it matches only the same instance unless the class overrides `equals()` *(Java rule)*.

## Reusable idea
A message is an event: if nobody listens when it fires, it is gone. A variable is state: it waits. Use messages for "react now" and latched flags for "whenever you get there".

## When the co-pilot should use this
- After G21's checks, an agent is still stuck waiting for a message, or a statechart skips a step when several messages arrive together.
- Designing command protocols between agents: dispatcher and vehicles, controller and machines, retailer and trucks.
- Related: G21, G22, G24, and `videos/statechart-agent-through-hosted-flowchart.md`.
