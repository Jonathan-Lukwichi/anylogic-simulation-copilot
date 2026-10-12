# Pattern card — Multimethod interface catalogue (models A–S): wiring SD, events, statecharts and flowcharts
- **Source:** AnyLogic example models "A - SD Triggers Condition Event" … "S - DE process Generates Outgoing Message" (bigbookmodels/Multimethod), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid
- **Problem it solves:** Pick the construct for each direction of coupling between system dynamics, agents/statecharts and process flowcharts, and know when each side actually notices the other.

## Structure
Nineteen one-screen demos (Big Book ch. 6, not in `.pdf-text/`). Rows marked *known* are already in the KB; the
engine behaviour column is what matters when wiring your own model.

| Direction | Construct (model) | What 8.9.10 actually does |
|---|---|---|
| SD → trigger | Condition event `Money <= 0` (A); Condition transition `Interest > 1000` (B) | Re-tested every solver step while the model has any SD, switch point located to solver accuracy (*known*: `bigbook/event-modes-condition-monitoring-and-lifecycle.md`) |
| SD → event frequency | Rate event, Rate = `ImigrationRate` (C) | Read when the next occurrence is scheduled and on the agent's `onChange()` (Help *Event*); **not** on solver steps — the engine's per-step set holds condition triggers only (engine) |
| SD → arrivals | Source *Interarrival time* `exponential(AdmissionsPerDay)` (D) | *Arrival rate* is a static parameter, computed once when the block is built; only `set_rate()` changes it (engine). *Interarrival time* is re-evaluated for every agent |
| SD → decision | Read the variable in a function (E) | Plain Java value (*known*: ch. 5 p. 11) |
| Statechart ↔ stock | Condition `RetailerStock >= 1`, action `RetailerStock--` (F); `+=` on message (K); arrayed stocks (L) | A stock may jump; integration resumes from the new level. A flow or auxiliary with a formula is overwritten — tick *Constant* (*known*) |
| Agents → SD | `ShopRunningCostPerMonth * shopChain.size()` (G); population statistic in a formula (H) vs *Constant* variable refreshed by a cyclic event (I) | A formula runs every solver step — fixed step 0.001 here, so ≥1,000 population scans per time unit in H; I scans once per time unit |
| Statechart → SD | Flow `inState(Waiting) ? Interest * LossRate : 0`; transition `Interest <= InterestThreshold` closes the loop (J) | *known*: `models/epidemic-and-clinic-with-accumulating-concern.md` |
| Movement → SD | Inflow `RadiationLevel(truck.getX(), truck.getY())` (M) | *known*: `models/exposure-to-radiation.md` |
| DE events → SD | Count accidents over 5 units, then `AccidentRate = count / 5.0` (N) | A lagged finite difference that needs two helper elements and a window choice; incrementing the stock at the event is exact |
| DE state → SD | Flow `FinishedGoods.size() > 2 ? 0 : 1` (O) | *known*: ch. 5 p. 11 |
| Agent serves a DE process | `Queue` → `Hold` → `Sink`; statechart `Idle → Working` on `queue.size() > 0`, `Working → Idle` after 0.9 with `hold.setBlocked(false)` (P) | Purely discrete, so the condition is re-tested only on the statechart owner's own events — the Queue's On enter must call `onChange()` |
| Agent consumes from DE | Condition `RetailerStock.size() > 0`, action `RetailerStock.removeFirst()` (Q) | Same wake-up rule; with many consumers let the stock owner allocate (*known*: G56, `videos/abm-stock-gated-purchase-allocation-and-brand-tie.md`) |
| Message → DE | On message received `RawMaterialDeliveries.inject((Integer) msg)`, Source in *Calls of inject()* mode (R) | *known* |
| DE → message | Sink On enter `send(1, this)` (S) | Works from Main (`send(msg, agent)` needs no space, engine). To pass the item itself use Exit → target `Enter.take()` (*known*) |

## Resources
n/a. In P the agent is the server; in Q the Queue is the inventory.

## Key settings worth copying
- **D, guard zero:** Help *Source* — an interarrival that evaluates to infinity stops the Source for good, and zero or a
  negative value is an error. If λ can reach 0, write `lambda > 0 ? exponential(lambda) : timeToReopen`.
- **D, fidelity:** the next gap is drawn at the current λ and held, so after a quiet spell a rising rate starts late. For
  exact time-varying arrivals use *Rate schedule*.
- **I:** `Demand` has no formula (*Constant*, value 0); a cyclic event every 1 time unit runs
  `Demand = consumers.NumberReadyToBuy();`. Pick the period well below the SD time constants. The exact O(1)
  alternative is a counter changed in the agents' state entry and exit actions.
- **N, the better way:** `Accidents++` (or `+= size`) in the Accident event itself. Any stock can take such a jump.
- **P, gate:** Hold *Initially blocked* = true and On enter `self.setBlocked(true);`, so exactly one agent passes per
  release. The 8.9.10 Hold also has the mode *Block automatically after N agents* (N = 1) with `unblock()`.
- **L, array elements** (syntax as used in the 8.9.10 model): `OccupiedHouses.get(Midtown)` and
  `OccupiedHouses.set(OccupiedHouses.get(Midtown) - 1, Midtown)` — value first, then the enum index.
- **K:** the demo button calls `this.receive(...)`, deprecated since 8.9.2 (G24). Use `send(qty, this)`.
- **Engine-wide conditions:** once any SD exists, every armed condition in every agent is re-tested at each solver step
  (Big Book ch. 8 p. 10; engine). An SD-free agent's `time()`-based condition then fires on time, but only as long as
  the SD part exists — and each armed condition costs one evaluation per step.

## KPIs instrumented
The demos only `traceln`. Useful checks: (D) arrivals per period against ∫λ dt; (H vs I) run time with animation off;
(N) final stock against the event count.

## Reusable idea
Couple by who owns the change: continuous levels trigger the discrete side through conditions; discrete events change
stocks by jumps, never through estimated rates or assignments to formula variables; populations reach SD as sampled or
incrementally kept counts; SD drives arrivals through per-arrival interarrival times; flowcharts and agents wake each
other with `onChange()`, `inject()`, `take()` and `send()`.

## When the co-pilot should use this
- Phase 1 of any hybrid build, before writing a formula that reads agents or blocks, or a condition that reads another
  agent.
- Symptoms: a hybrid model that slows as agents are added; a coupling that reacts late or never; an arrival stream
  that ignores its SD driver.
- Related: `bigbook/event-modes-condition-monitoring-and-lifecycle.md`,
  `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`, G5, G22, G56,
  `bigbookmodels/request-tokens-into-a-shared-process.md`.
