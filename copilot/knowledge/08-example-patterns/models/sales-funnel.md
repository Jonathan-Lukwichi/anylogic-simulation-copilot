# Pattern card — Sales Funnel
- **Source:** AnyLogic example model "Sales Funnel" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (a process written as a customer statechart, served by salesman agents with caseloads)
- **Problem it solves:** Find where a staged sales process (contact → quote → credit review → funding) loses customers, and how sales-force size, caseload, skill and review speed move each loss.

## Structure
- **Arrivals:** an event with timeout `exponential(ProspectsPerDay)` (a Poisson stream, 30/day by default) adds a `Customer`. It is assigned to the first salesman with a free slot, if any.
- **Customer statechart:**

  | Stage | What can happen |
  |---|---|
  | Prospect | Contact fires on the condition `salesman != null`. Discarded after 1 month without a salesman. |
  | Contact branch | 20 % do not qualify; of the rest, 30 % are not interested; the others move to WaitingQuote. |
  | WaitingQuote | A race: QuoteMade after `uniform(6, 13) / salesman.SkillLevel` days vs QuoteIsLate after 10 days. |
  | Quote branch | 30 % dislike the quote, the rest go to CreditReview. |
  | CreditReview | A race: ReviewFinished after `uniform(6, 13) / CreditReviewEfficiency` days vs TooLongReview after 10 days. |
  | Review branches | 30 % credit declined; of the rest, 10 % rejected by the customer; the others go to Funding (1 week). |

  Every loss goes through Leaving (1 day) to a final state that removes the agent. Each named exit transition increments its own counter on Main (`NDiscarded`, `NQuoteIsLate`, `NTooLongReview`, …).
- **Salesman:** a `customers` collection, capped at `CustomersMax` (5).
  - `assignCustomer(s, c)` adds the customer, sets `c.salesman`, then calls `c.onChange()` so the Contact condition is re-tested (G56).
  - `free(c)` runs from the customer's exit from CreditReview or Leaving. It removes the customer, then pulls the first unassigned customer still in Prospect.

## Resources
50 salesmen × 5 slots = 250 concurrent customers. One salesman keeps a customer from contact until the credit review ends (sticky assignment). Credit review has no staff resource, only a speed factor.

## Key settings worth copying
- **Loss attribution.** One counter per exit transition. Bar charts show `zidz(NReason, NProspects)` per stage, and `resetStats()` clears them after a warm-up.
- **Heterogeneous servers.** Duration scales with the assigned agent's attribute (`/ salesman.SkillLevel`).
- **Patience as a competing timeout.** Service time and deadline are two Timeout transitions out of one state; whichever fires first wins.

## KPIs instrumented
Share of prospects lost per reason and per stage, conversions (`NCreditAwarded`), and each salesman's caseload (drawn as links to their customers).

## Pitfalls
- **Races have cliffs.** With skill 1, P(uniform(6, 13) > 10) = 3/7 ≈ 43 % of quotes are late; with skill ≥ 1.3 none are. Small lever changes can flip whole loss categories. Compute the race probability before calibrating (G55).
- **Skill changes timing only.** In this model skill affects lateness, not the qualification or acceptance splits. Tie the branch probabilities to salesman attributes too if that matters.
- **Unbalanced workloads.** First-fit assignment scans salesmen in index order, so low-index salesmen are always full. Per-salesman utilisation is then skewed, which matters for incentive or fatigue questions; use least-loaded assignment if it does.
- **Credit review has no queue.** The review team is only a speed factor, so review congestion cannot appear. Give it a resource if capacity is the question.

## Reusable idea
Write a multi-stage pipeline with abandonment as one statechart per client:
- each stage is a state racing a completion timeout against a patience timeout;
- each branch is a decision;
- each loss is a named, counted transition.

Servers are agents that hold a caseload (K clients at once, across several stages) and pull the next waiting client when a slot frees up. That is awkward to express with PML `Seize`/`ResourcePool`, where a unit serves one agent at a time.

## When the co-pilot should use this
- **Use cases:** sales or lead pipelines, loan and insurance underwriting, recruitment, case management, permit or claims processing. It fits whenever one person owns several open cases across stages and clients drop out at each stage on their own clock.
- **Related:** `videos/abm-adoption-flow-counters-vs-state-counts.md` (count at the event), gotchas G55 and G56.
