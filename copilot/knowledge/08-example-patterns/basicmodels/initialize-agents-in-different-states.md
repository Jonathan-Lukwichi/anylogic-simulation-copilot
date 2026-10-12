# Pattern card — Initialize Agents in Different States
- **Source:** AnyLogic example model "Initialize Agents in Different States" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Start a population whose agents are already spread over the stages of a life-cycle statechart (not all in the first state) while keeping one ordinary statechart.

## Structure
- Option List `LifeCycle` = {growth, maturation, harvest}.
- Agent type `Tomato` with a parameter `initialState` of type `LifeCycle`; population `tomatoes` on `Main` sets it per agent to `randomFrom(LifeCycle.values())`.
- Statechart: entry point → `growth` → `maturation` → `harvest` → final state, all **timeout** transitions. The timeout of each transition is conditional on the parameter: it is the normal duration (10 s) when the agent should really live in the source state, and **0** when the agent started in a later stage — e.g. leaving `growth` waits `initialState == LifeCycle.growth ? 10 : 0`; leaving `maturation` waits 10 only if the initial state was `growth` or `maturation`. The last transition always uses the real duration.
- Transition actions recolour the agent's shape, so skipped stages still leave the animation in the right colour.

## Resources
n/a

## Key settings worth copying
- Store the start stage in a parameter typed with an Option List; draw it with `randomFrom(LifeCycle.values())` as in the demo (an Option List is a Java enum), or with the equivalent helpers listed in Help 8.9.10 — `randomFrom(LifeCycle.class)` or `LifeCycle.random(this)` — or read it from data. For a non-uniform start mix use a custom distribution over the options.
- On each transition out of stage *k*: timeout = `initialState` is stage *k* or earlier ? normal duration : 0.
- Everything after the start stage runs with normal timings — only the "catch-up" is zero-time.

## KPIs instrumented
n/a — visual demo (colour per stage).

## Pitfalls
- The skip is real execution: entry/exit actions of the skipped states and the transition actions all run at time 0. Counters or statistics updated there (e.g. "entered maturation") will count agents that never really lived in that stage — guard them with the same condition or move the counting elsewhere.
- The conditions grow with the number of stages (each transition lists every earlier stage). For long statecharts prefer a **branch** right after the entry point with one condition per start state, pointing straight at that state (no zero-time chain, no replayed actions) — but then per-state entry actions that set up the agent (colour, variables) must be repeated on the branch exits.
- Zero-time transitions are still events at time 0; anything that reads the population's state counts "at start-up" sees the agents mid-chain. Read state statistics after time 0.

## Reusable idea
Warm-starting an agent-based model: seed the population in a realistic mix of stages (disease stages, equipment age classes, customer lifecycle, product maturity) with a start-state parameter and conditional timeouts, instead of simulating a long warm-up from "everyone in state 1".

## When the co-pilot should use this
When a user asks how to make agents start in different statechart states (from a distribution or a data column), or complains that all agents begin in the first state and the model needs a long warm-up. Mention the replayed-actions pitfall and the branch alternative.

## Additions (8.9.10 review, 2026-10-01)
- For agents that start mid-life, see also `bigbookmodels/statechart-for-life-phases.md`: an entry branch plus age-conditioned residual timeouts (`normal(age(), infinity, mu, sd) - age()`, the truncated normal — gotcha G66) starts agents mid-life without replaying earlier states' actions.
