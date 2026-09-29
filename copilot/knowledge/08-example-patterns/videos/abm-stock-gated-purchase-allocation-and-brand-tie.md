# Pattern card — Stock-gated purchases in an ABM competition: owner-side allocation and an explicit brand choice
- **Source:** AnyLogic video "Part 4: Scenario 1 – Consumer StateChart Setup" (https://youtu.be/QocfkYnwSYw) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Consumers buy from finite stocks held on Main. Waiting buyers must be served when stock returns, scarce units shared by a stated rule without overselling, and a buyer who would take either brand must choose deliberately.

## Mechanism
The series' statechart (Parts 1 and 4):
- PotentialUser → WantA/WantB, by ads (Rate) or word of mouth (message).
- WantA → UserA by the Condition `main.stockA >= 1`, with Action `main.stockA -= 1`.
- WantA/WantB → WantAnything after a give-up Timeout.
- WantAnything → UserA or UserB by two Condition transitions, `buyA1` and `buyB1`.
- Stocks A and B are SD Stocks on Main, 42,000 each, with no restocking in Scenario 1.

The structure is known (`models/ab-market-and-sd-supply-chain.md`; 3-days pp. 74–85). It is safe only while stock never rises. Two traps appear once it can:
1. **Waiting buyers are not woken by a restock.** A Condition in a consumer is re-tested only when something happens in that consumer, or when `onChange()` is called on it. The rule and a push loop are in `videos/statechart-live-controls-trigger-reevaluation.md`. Scenario 1 hides the trap because stock only falls.
2. **The engine picks the brand.** When both of WantAnything's conditions are true on entry, the two transitions fire as simultaneous events. Help 8.9.9 says these run "in some internal (not guaranteed) order", and the Engine Javadoc gives LIFO as the default since 8.6. Every indifferent buyer can therefore go to the same brand.

**Pattern: the agent that owns the stock allocates it.**
- **Main** holds ordered waiting lists `waitingA` and `waitingB` (Collection, `ArrayList<Consumer>`) and this function:
  `void serveA() { while (stockA >= 1 && !waitingA.isEmpty()) { Consumer c = waitingA.remove(0); stockA -= 1; c.gotA = true; c.onChange(); } }`
- **Consumer:**
  - `WantA` Entry action: `main.waitingA.add(this); main.serveA();`
  - `WantA → UserA`: Condition `gotA`, Action `gotA = false;`
  - give-up transition, Action: `main.waitingA.remove(this);`
- **Restocking:**
  - *By lots (an event):* `stockA += lot; serveA();`
  - *By SD inflow:* add a Main Event, Trigger = Condition `stockA >= 1 && !waitingA.isEmpty()`, Action `serveA(); serveAEvent.restart();`. Main owns the continuously changing stock, so the Help checks its conditions at every solver step. A condition event fires only once unless restarted (Help, *Events*).
- **WantAnything:** decide once, on entry, in code with `main.requestAny(this)`:
  - both brands in stock → an explicit rule (`randomTrue(0.5)`, price, share, last brand used);
  - one in stock → that one;
  - none → join a declared queue.

  Statechart-only alternative: one Condition transition `main.stockA >= 1 || main.stockB >= 1` into a Branch. The Branch's first exit carries the rule and its other exit is Default; a branch with no true condition and no default is a runtime error (Help). It still needs waking on a restock.

Units are reserved before the buyer is woken. No sale can exceed stock, and service is FIFO whatever order the engine runs events in.

## Resources
Two inventories on Main, and two or three ordered waiting lists. Each inventory can be an SD Stock or a plain `int`; a Stock is worth it only with continuous flows. Gate on `>= 1` either way.

## Key settings worth copying
- **`c.onChange()`** (Javadoc 8.9.9): re-evaluates that agent's Condition triggers and recomputes its Rate triggers.
- **Don't fix ties through the engine.** `getEngine().setSimultaneousEventsSelectionMode(...)` exists with FIFO, LIFO and RANDOM, but the Javadoc calls it experimental and not recommended in general, and RANDOM is slower. Model the choice instead.
- **Patience: trait or episode.**
  - `uniform(...)` typed into the Timeout field is drawn again each time the state is entered; Help says the timeout expression is computed once per entry.
  - A static agent parameter holding a distribution (the video's `giveUpA`) is drawn once per consumer. That consumer then waits the same time on every visit, making impatience a fixed trait: the same people keep switching.
  - Choose on purpose.
- **Dense agent events plus SD equations.** `getEngine().setEventAwareSolver(false)` in Main's On startup can speed runs up considerably. The trade-off: events then read continuous values up to one solver step (HTOL) old, and SD formulas refresh only on solver steps (Help 8.9.9, *System dynamics → Combining*; the default is true).

## KPIs instrumented
The video has count statistics per user state and a time plot. Add:
- stock-out time share per brand;
- `waitingA.size()` over time;
- give-ups per brand (forced switches);
- sales diverted to the rival;
- wait from enqueue until `gotA` is set.

## Pitfalls
- **A scenario that cannot bind.** 42,000 units per brand against 5,000 consumers who each buy once (the build has no discard) means no stock-out within a year. Give-up and WantAnything never run in Scenario 1. Before any supply scenario, compare the maximum possible demand over the horizon with stock, and report a counter on every rare-path transition.
- **Compounding artefacts** *(inference; Scenario 2 is not in these videos)*. Buyers who never notice A's restock time out into WantAnything, find both brands in stock, and the tie-break decides. A "supply chain decides the market" result can then be an artefact.
- **A duplicated guard is not a proven oversell barrier.** The video uses `main.stockA >= 1` as both condition and guard. Help does not say when that guard is evaluated relative to other buyers woken in the same instant. Central reservation does prevent overselling.
- **Allocation priority is a policy.** Loyal waiters before switchers, or one FIFO across both? State which. (`ArrayList.remove(Object)` is O(n): fine for thousands; beyond that use an ordered `LinkedHashSet`, G17.)

## Reusable idea
Whoever owns a scarce resource allocates it. Requesters register, the owner serves them in a declared order and wakes each winner. Thousands of agents polling a condition on another agent's variable is slow, and it can miss the change altogether.

## When the co-pilot should use this
- Any ABM where agents wait for something held elsewhere: inventory, beds, charging points, vaccine doses, housing.
- Reviewing statecharts with `Condition: main.<x>`.
- Any state with two transitions that can be enabled at the same instant.
- Related: DES analogue `Wait` + `free(agent)` (G7); `models/ab-market-and-sd-supply-chain.md`; `videos/statechart-live-controls-trigger-reevaluation.md`.
