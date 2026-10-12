# Pattern card — Choosing the method: abstraction line first, closed loops, time-in-state shape and the deciding unit
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 1 "Modeling and simulation modeling", ch. 2 "The three methods in simulation modeling" and ch. 4 "How to build agent-based models. Field service example" (§4.10) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Phase 0 picks DES, SD or ABM from surface cues and misses the checks that decide whether the model will be valid.

## Mechanism
The KB's method authority (Borshchev & Filippov 2004, `00-method-selection/`) already covers the abstraction scale, the three
paradigms, the SD→AB and DE→AB conversions and multi-method architectures. These chapters add six checks. Run them
after the intake card is confirmed and before recommending an approach.

1. **Draw the abstraction line before naming a method.** Say what the question needs and what may stay below the line:
   physical movement and contact, individual identity and history, single events such as one purchase. The method
   follows the line. SD covers the aggregate end, DES the middle to operational end, and ABM any level (ch. 1 p. 12).
   Start coarse, add detail only when a question needs it, and redraw the line when the question moves.
2. **Close the loop or justify leaving it open.** A queue fed by a fixed arrival stream is open-loop. If congestion
   changes behaviour, outputs feed back into inputs and the open-loop answer is wrong exactly where the decision
   bites (ch. 2 p. 2). Examples: people leave long queues or give up waiting, demand drifts with service level,
   overtime raises attrition. Model the loop (balk/renege logic in DES, a feedback structure in SD, agent decisions in
   ABM), or record why it is negligible.
3. **Ask whether the shape of time-in-state matters.** An SD stock drained at `Stock / AverageTime` treats its contents
   as well mixed, so residence times are exponential (ch. 2 p. 13). If durations are fixed or narrow, you need
   pipeline or higher-order delays (`delay`, `delay3`, aging chains). If individual histories matter, use DES or
   agents. The SEIR agent model is justified partly by uniform, non-exponential phase durations (ch. 2 p. 15).
4. **Make the agent the unit that decides.** Pick households, firms or crews rather than persons when the choice is
   made at that level. A car purchase, for example, is a household decision (ch. 2 p. 19). Agents need not be people
   and need not interact. A passive-looking asset with its own schedule, cost and failure events makes a good agent
   (ch. 2 pp. 19–20).
5. **Find out who generates the demand.** Suppose each request stream belongs to one object, and its next request
   depends on that object's state and history. Examples: the next failure is possible only after repair, the next
   service is timed from the last one, the risk grows with age. Then the sources are agents with statecharts, not a
   Source block. A DES version needs one generator per unit, cross-linked by code to state held elsewhere, and the
   flowchart stops explaining itself (ch. 4 §4.10). DES tools also rarely let a mobile resource be re-tasked on its
   way back to base.
6. **Treat structural ABM assumptions as sensitivity levers.** In the epidemic demo (ch. 2 p. 17), a narrower
   immunity-duration spread turns recurring waves into one outbreak, and long-range links in the contact network make
   the disease persist. Network type and duration spread change the regime, not just the numbers.

## Resources
n/a

## Key settings worth copying
- SD delay forms (Help 8.9.10, SD functions): outflow `Stock / T` gives exponential residence; `delay3(x, T)` gives a
  bell-shaped lag; `delay(x, T, x0)` gives a fixed pipeline shift that returns `x0` until `T` has passed.
- The approach record's "Rejected, and why" section of the approach record guards against the bias the book
  names. The modeller's background, not the problem, often picks the method (ch. 2 p. 1).

## KPIs instrumented
n/a (method)

## Pitfalls
- Adding detail because simulation "scales" (ch. 1 p. 10). Add a detail only when a question needs it.
- Assuming an ABM needs a global tick. Asynchronous timing (rates, timeouts, messages) is the norm and is cheaper
  (ch. 2 p. 19; same point in Borshchev & Filippov p. 9).
- Converting passive, indistinguishable stocks (money, bulk material) to agents. It adds cost and no insight (paper
  p. 11).

## Reusable idea
Decide in this order: the question, what may sit below the abstraction line, whether anything feeds back, whether
duration shape or individual history matters, who decides, and only then the method.

## When the co-pilot should use this
- Stage 1 (Phase 0 Stage B), before recommending an approach, and when a user asks for a method out of habit.
- Reviewing a model that ignores behavioural feedback (fixed arrivals into long queues), or an SD model whose
  delays should not be exponential.
- Related: `videos/statechart-agent-through-hosted-flowchart.md` (movers visiting capacity-limited sites);
  `bigbook/abm-design-recipe-states-messages-and-dispatcher.md`.
