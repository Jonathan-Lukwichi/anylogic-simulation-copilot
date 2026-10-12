# Pattern card — Kinship Model with Customized Statistics
- **Source:** AnyLogic example model "Kinship Model with Customized Statistics" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Keep a population's relationship network (spouse, parents, children) consistent through births and deaths, and measure the population without re-scanning every agent at each chart update.

## Structure
The Big Book series shares one `Person` statechart across four models. *Kinship Modeled Using Custom Links* holds the relations; *…with Standard Statistics*, *…with Customized Statistics* and *…with Dynamic Histograms* each add a way of measuring.
- **Life course.** Junior → Adult (composite: NoFamily, Family) → Senior → Dead, a final state. Stage changes are timeouts of 15–25 years. The customized version uses years as the time unit; the others use minutes read as years.
- **Relations are typed fields, not the standard `connections`:** `spouse`, `father` and `mother` (type `Person`), plus a collection `kids` (`ArrayList` of `Person`).
- **Marriage.**
  1. An unmarried man fires a Rate transition (once a year on average).
  2. Its action scans `main.people` for a woman in NoFamily, stores her as `spouse`, and sends himself to her with `send(this, her)`.
  3. Her message transition stores `msg` as her spouse and walks her to him.

  The handshake itself is in `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`.
- **Births.** A Rate transition inside Family, guarded "female with a living husband", creates the child with `main.add_people()`. It adds the child to both parents' `kids`, sets the child's `mother` and `father`, and places it near the father.
- **Death.** Dead's action removes every pointer to the dying person before `main.remove_people(this)`:
  - each child's `father` or `mother` becomes null;
  - `spouse.spouse` becomes null;
  - the person leaves each parent's `kids`.
- **Links on screen.** Two lines are drawn inside `Person`:
  - one Line replicated `kids.size()` times, with dx/dy = child position − own position;
  - one Line to the spouse, visible only on the man's side, so each couple is drawn once.

## Resources
n/a

## Key settings worth copying
**AnyLogic 8 alternative to hand-kept fields: Link to Agents elements** (Agent palette; Help 8.9.10 *2-way link to agents* uses this very family as its example):
- Make `spouse` a single 2-way link whose peer is the same link, and parents ↔ `kids` a 2-way pair (collection on one side).
- `connectTo(a)` then sets both ends at once.
- Single link: `getConnectedAgent()`, `disconnect()`. Collection: `getConnections()`, `getConnectedAgent(i)`, `isConnectedTo(a)`.
- In the 8.9.10 engine, single and collection links disconnect when their owner is destroyed, and drop a destroyed agent they point to (`onDestroy()` and `onDestroy(Agent)`). Plain fields get no such cleanup *(bytecode check, not stated in Help)*.
- *Draw line connecting agents* in the link's Animation section replaces the replicated lines.

Three ways to measure the same population:

| | Standard statistics | Incremental counters (the "customized" model) | Snapshot histograms |
|---|---|---|---|
| Set-up | Population → Statistics: count with `agent.inState(agent.Junior)`; average of `agent.kids.size()` over non-junior women | `int` variables on Main: `+1` in a state's Entry action, `−1` in its Exit action | a cyclic event calls `ageDist.reset()`, then `ageDist.add(p.age())` for every agent |
| Cost | Scans every agent at every call (Help *Collecting statistics*), i.e. once per statistic per chart sample | Constant per transition | One scan per refresh |
| Risk | none | a missed entry or exit path drifts silently | shows the present only |

- **The hard aggregate is a sum over a relation** — total children of living adult women. It changes at three events: +1 at each birth; −1 per child when a mother dies; −1 when a child dies while its mother lives. Display it as `zidz((double)totalKids, nFemaleNonJunior)`.
- **HistogramData:** `reset()` discards all samples and statistics (Javadoc). Untick CDF and percentiles when they are not shown. `age()` returns `time() - birthdate`, where `birthdate` is set to `time()` at creation.
- **Link lines inside an agent:** set Rotation to `-getRotation()`, or the line turns with the agent's own rotation.
- **High churn:** a population with frequent births and deaths can be switched to Advanced → *Optimize for: Add/remove operations* (LinkedHashSet). Index access then gets slower (Help *Optimizing the performance of an agent population*).

## KPIs instrumented
Juniors, adult women, adult men and seniors over time (time stack chart); average children per woman (bar chart); age and family-size distributions (histograms).

## Pitfalls
- **Two-sided cleanup.** The general rule "clear references before removal" is in `bigbook/abm-runtime-resizing-of-a-busy-agent-population.md`. With plain fields, family links make it two-sided and collection-valued. Skip one side and nothing errors: a widow keeps having children with a removed husband, or code reads a dead agent's position. Link to Agents elements avoid most of this; counters still need their own updates.
- **Everyone starts newborn.** All 300 people start as Juniors with age 0, so the charts show cohort waves for decades. Seed initial ages and stages instead (`basicmodels/initialize-agents-in-different-states.md`), or discard a long warm-up.
- **Proposal race** *(design judgement)*. The message handshake is safe here only because Rate events almost never coincide. If proposals are made at the same instant (steps, or a cyclic loop over all men), two men can choose the same woman. Set both sides in one action, or test `p.spouse == null`.
- **Counter drift.** While building, compare each counter with a population count in a periodic check, and remove the check afterwards. Write statistic conditions with `agent.`, not `item.` (G53).

## Reusable idea
- Name each relation. Prefer a 2-way Link to Agents element; otherwise use a typed field plus a removal routine that walks the reverse links.
- Pick the statistic by size:
  - population statistics while N is small;
  - entry/exit counters plus a conservation check when N is large;
  - histograms rebuilt from scratch when the question is "what does the population look like now".

## When the co-pilot should use this
- Demographic and household ABMs; any ABM with typed relations (employer, landlord, carer, owner).
- ABMs that slow down as their charts sample large populations.
- Age pyramids and other current-state distributions, as opposed to all-time accumulations.
- Related: `videos/abm-adoption-flow-counters-vs-state-counts.md` (flows vs levels), `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`.
