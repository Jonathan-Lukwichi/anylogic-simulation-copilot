# Pattern card — Petri Nets
- **Source:** AnyLogic example model "Petri Nets" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Build and run a timed Petri net (places, tokens, timed transitions) in AnyLogic from two reusable agent types that the modeller wires on the canvas. The example is a producer–consumer system with a bounded buffer and a semaphore.

## Structure
- **Two node types.**
  - `Place` holds an integer `tokens` (from an *initial tokens* parameter) and lists of its input and output
    transitions.
  - `TimedTransition` holds a delay parameter, lists of its input and output places, a firing counter, and a
    two-state statechart (idle ↔ delay).
  - Both have an `in` and an `out` **port**. A third, tiny type carries a registration message: the sender and a
    direction flag.
- **Arcs are connectors between ports**, drawn in the top-level agent. The example net:
  - *Producer:* 1 token cycles through "works" (exponential 1 s) and "writing".
  - *Consumer:* 1 token cycles through "reading" and "works" (0.7–1.3 s).
  - *Buffer:* 5 tokens in an empty-buffers place; written data waits in a data-in-buffer place.
  - *Semaphore:* one 1-token place is both input and output of *writing* and *reading*, so only one of them runs at a
    time.
- **Self-wiring at startup.** On startup every node sends a registration message through both of its ports. The
  receiving port's *On receive* code does three things:
  - checks that the partner is of the other node type and that the direction is legal;
  - stops the run with `error()` on an illegal arc;
  - otherwise adds each node to the other's lists, skipping duplicates.

  So the drawing on the canvas becomes adjacency lists at runtime.
- **Firing.** A transition's condition-triggered transition fires when `enabled()` holds (every input place has ≥ 1
  token). Its action takes one token from each input place at once. The *delay* state then times out after the
  delay; the exit action adds one token to each output place and counts the firing.
- **Wake-up.** Every token change calls the place's `inform()`, which calls `onChange()` on each downstream
  transition so that its condition is re-tested.

## Resources
n/a. Shared resources are **token counts**: the semaphore place is a mutex of capacity 1, and the empty-buffers place
is the buffer size.

## Key settings worth copying
- Initial marking: producer 1, consumer 1, empty buffers 5, semaphore 1.
- Delays (model time unit minutes, delays given in seconds):
  - producer work `exponential(1)` s;
  - write `uniform(0.1, 0.2)` s;
  - read `uniform(0.05, 0.1)` s;
  - consumer work `uniform(0.7, 1.3)` s.
- Token timing: tokens are **removed when firing starts and added when it ends**. They are unavailable during the
  delay, which is what makes the semaphore work.
- Arc rules enforced at startup: a place's `in` port takes a transition's `out`, and vice versa.
- Animation: each place draws up to 25 tokens as dots and shows a number above that. Each transition is coloured by
  its state: firing (gold), enabled (blue) or disabled (silver). `toString()` gives an inspection summary.
- **The port handlers are hidden by default.** A port's *On receive* / *On send* fields show only when **Library
  developer mode** is on (Tools > Preferences > Development; Help 8.9.10 `advanced/libraries/ports.html`).

## KPIs instrumented
n/a — no charts. Available for instrumentation: each transition's firing count (reads and writes completed), tokens
in the data-in-buffer place over time (buffer fill), and the share of time the semaphore holds 0 tokens (contention).

## Pitfalls
- With developer mode off, the model appears to have no wiring logic at all.
- Any code that changes `tokens` outside a firing (a button, an event) must also call `inform()`. Otherwise the
  downstream transitions stay asleep: a condition trigger is re-tested only on events in its own agent or on
  `onChange()` (KB: `videos/statechart-live-controls-trigger-reevaluation.md`).
- **Conflicts** (two enabled transitions that share one token) go to whichever transition is evaluated first. The net
  has no explicit priority or random choice. Add one if your semantics need it *(inferred)*.
- One agent plus a statechart per node suits nets of tens to hundreds of nodes. Reachability or invariant analysis
  belongs in a dedicated Petri-net tool.

## Reusable idea
A modelling formalism of your own can be just two agent types with ports. Draw the graph with connectors, let a
startup handshake over the ports build and validate the adjacency lists, and drive the behaviour with
condition-triggered statecharts plus explicit `onChange()` notifications (event-driven, with no polling). The same
pattern works for any user-drawn network of custom nodes.

## When the co-pilot should use this
- A user asks whether AnyLogic can model Petri nets, or wants to study concurrency, mutual exclusion, bounded buffers
  or synchronisation (shared robots or tools, interlocks, protocol logic) as states and resource tokens rather than
  entities moving through a flowchart.
- Explaining deadlock or starvation structurally (a token that never returns).
- As the template for building a small custom library whose topology is drawn by the modeller.
