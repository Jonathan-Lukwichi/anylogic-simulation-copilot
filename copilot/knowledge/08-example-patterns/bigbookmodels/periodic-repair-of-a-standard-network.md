# Pattern card — Periodic Repair of a Standard Network
- **Source:** AnyLogic example model "Periodic Repair of a Standard Network" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** A standard contact network is built once, so it goes stale as agents are born, die and move. Keep it meaningful, and extend a standard network by hand without losing the extra links.

## Structure
Companion: *Custom Network Built Using Standard Connections* (same Big Book folder).
- **Repair model.**
  - Space: 50 `Person` agents in a 500 × 500 continuous space, random layout, network type *Distance-based* with range 50.
  - Each person arms a User-control timeout `death` in On startup (it fires after `uniform(80, 100)` minutes), then wanders: On arrival picks a new random point.
  - On Main, a Rate event `birth` (1 per minute) calls `add_persons()`, and a cyclic event `repairNetwork` (every 5 minutes) calls `applyNetwork()`.
- **Custom-network model.**
  1. 20 persons start in a *Ring lattice* (2 links each, Ring layout).
  2. Main's On startup gives each of them three new persons, via `add_persons()` then `sub.connectTo(hub)`.
  3. `setLayoutType(Agent.LAYOUT_SPRING_MASS)` and `applyLayout()` re-arrange the resulting hub-and-spoke graph.
- **Link drawing, both models.** A Line inside `Person` is replicated `getConnectionsNumber()` times. Its end points at `getConnectedAgent(index)` (dx/dy relative to the agent), and its rotation is set to `-getRotation()`.

## Resources
n/a

## Key settings worth copying
Verified in Help 8.9.10 (*Agent*, *Agent API*, *Standard agent contacts network*):
- Network fields apply only to their own type:
  - Connections per agent: Random, Ring lattice, Small world;
  - Connection range: Distance-based, continuous space only;
  - Neighbor link fraction: Small world;
  - M: Scale-free.
- Layout limits: Ring and Spring mass work in continuous space only.
- `setNetwork…(…)` and `setLayoutType(…)` only change the setting. `applyNetwork()` and `applyLayout()` carry it out.
- **`applyNetwork()` discards every existing connection and rebuilds from the current settings**, including links made by `connectTo()`. With the User-defined type it does nothing.
- **Removal cleans up after itself.** In the 8.9.10 engine an agent's standard connections are disconnected when the agent is destroyed (bytecode: `onDestroy()` → `disconnectFromAll()`; not stated in Help). Deaths leave no dangling links.
- **New agents join unwired.** The model relies on the next repair to connect newborns *(inferred from its design)*. To wire one at birth, in its On startup: `for (Person p : main.persons) if (p != this && distanceTo(p) <= 50) connectTo(p);` (`connectTo` returns false if already linked and errors on self).
- **Proximity without stored links:** `agentsInRange(r)` or `agentsInRange(r, METER)` returns the population members within r at the moment of the call. Nothing goes stale.
- **Built-in drawing:** *Space and network → Draw line connecting agents* draws the standard network (colour, width, style, arrows). Replicated lines are now needed only for custom relations (see `bigbookmodels/kinship-model-with-customized-statistics.md`).

## KPIs instrumented
None in the demos. For a network study, track degree (`getConnectionsNumber()`), the share of isolated agents, and the mean link length.

## Pitfalls
- **Stale between repairs.** Distance links reflect positions at the last `applyNetwork()`, and newborns have no contacts until then. Contagion over links is then under-counted among movers.
  - Size the repair period so an agent moves only a fraction of the range between repairs.
  - Or use `agentsInRange()` where the relation really is just proximity.
- **A repair wipes hand-made links** (companion model). Apply the standard network once, before adding custom links, and never again. Keep lasting ties in their own link element or typed field, which `applyNetwork()` leaves alone.
- **Repairs reshuffle random-type networks.** Re-applying a Random or Small-world network re-draws every contact. That is partner churn, a modelling assumption, not neutral upkeep.
- **Double drawing.** The replicated line is drawn from both ends of every two-way link, doubling the drawing work.

## Reusable idea
Treat a standard network as a snapshot. Decide who re-applies it and when, or keep proximity implicit with `agentsInRange()`. Keep lasting ties in structures that a rebuild cannot touch.

## When the co-pilot should use this
- Contact-network ABMs with population churn or movement: mobile epidemics, word of mouth with births and deaths, peer effects in migrating populations.
- Building a custom topology on top of a standard one (hubs on a ring, spokes, clusters).
- Symptoms: newborns never catch the infection or idea; contacts do not follow agents as they move; hand-made links vanish.
- Related: `basicmodels/agent-network-and-layouts-demo.md` (generators), `videos/abm-word-of-mouth-contact-targeting.md`.
