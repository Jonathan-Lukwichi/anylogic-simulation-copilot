# Pattern card — Statechart for Product Lifecycle
- **Source:** AnyLogic example model "Statechart for Product Lifecycle" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid (statechart + one SD stock)
- **Problem it solves:** Carry a product or project from development to withdrawal, with management interventions (suspend, resume, kill, discontinue) and money flows that depend on the phase.

## Structure
Agent `Product`, time unit Week, starts 1 Jan 2020 and stops at a date 10 years later.
- **NewProductDevelopment** (composite): FrontEnd → Prototyping → Testing → Development. The Timeouts are in MONTH units: `uniform(3, 24)`, `uniform(1, 3)`, `uniform(6, 24)`. The composite also holds a shallow History state.
- **Launch:** Development → InMarket, timeout `uniform(6, 12)` months, Action `timeOfLaunch = time()`.
- **InMarket** (composite): Introduction → Growth → Maturity → Decline. The transitions are Conditions on `sales()`: > 2500, > 4000, < 1000. Decline → final `dead` when `sales() - costs() < 500`.
- **Decisions** are String messages sent by buttons, each enabled only where it applies (`EnableExpression = inState(...)`):
  - "Suspend": NPD border → Suspended;
  - "Resume": Suspended → the History state;
  - "Kill": NPD border or Suspended → final `killed`;
  - "Discontinue": InMarket border → `dead`.
- **Money:**
  - `sales()` is 0 in development and `salesTable(m)` in the market.
  - `costs()` in development comes from a `switch (statechart.getActiveSimpleState())` over FrontEnd 20, Prototyping 40, Testing 100, Development 200. In the market it is `inMarketCostsTable(m)`.
  - `m = differenceInCalendarUnits(MONTH, timeOfLaunch, time())`. Both tables have 11 points over 0–60 months, Spline, out of range Nearest.
- **SD stock** `AccumuatedProfit` (sic): derivative `(sales() - costs()) / toTimeoutInCalendar(MONTH, 1)`.
- **Sibling demo** "Statechart for Pharmaceutical NPD Pipeline" (same batch). NPD is Discovery (`uniform(50, 200)` weeks), then three Evaluations (`uniform(100, 200)` each), with a branch after each phase. The failure exits (`randomTrue(0.5 / 0.4 / 0.3 / 0.2)`) end in final states inside NPD, and "Kill" leaves from NPD's border.

## Resources
n/a

## Key settings worth copying
- **Phase value by state:** state names work as `case` labels in `switch (statechart.getActiveSimpleState())`.
- **Monthly amounts in a weekly model:** divide by `toTimeoutInCalendar(MONTH, 1)`, the current calendar month's length in model time units. That makes the stock's inflow a per-model-time rate.
- **Suspend and resume:** leave from the composite's border and come back through its History state. Help 8.9.10 uses this model as its *History state* demo.

## KPIs instrumented
Plots of sales, costs and profit, sampled monthly; the accumulated-profit stock. For portfolio studies add time to market, the share of products launched (0.5 × 0.6 × 0.7 × 0.8 ≈ 17 % in the NPD pipeline) and NPV per product.

## Pitfalls
- **Resuming through History restarts the phase clock.** A timeout is evaluated and counted from entry into its state (Help *Transition*), and a resume is a new entry. A product suspended 20 months into a 24-month FrontEnd starts a fresh `uniform(3, 24)` draw, so the work done is lost and the phase is re-sampled. If progress must survive a pause, end the phase with a user-control Event and use its `suspend()`/`resume()`, which keep the remaining time (Help *Event*), or store the remaining time and use it as the next timeout *(suggested)*.
- **The market Conditions depend on time only through `sales()`.** They are re-tested continuously only because the agent has an SD stock: Help says conditions are monitored by the numeric engine when the agent has continuous variables, and otherwise only on `onChange()`. Delete the profit stock and the product stays in Introduction forever. Keep a continuous variable, add a periodic `onChange()`, or use a monthly tick.
- **`getActiveSimpleState()` returns the innermost state.** A `switch` over it needs a case for every simple state that can be active. Here Suspended sits outside both composites, so `costs()` returns 0 during a suspension. Decide whether holding costs should apply.
- **Chart recurrence** uses `toTimeout(MONTH, 1)`. It is still in the 8.9.10 engine but deprecated (javap) and absent from Help. Use `toTimeoutInCalendar`.
- **A final state ends the whole statechart** (Help *Final state*). In the pipeline, a Discard inside NPD stops the agent's lifecycle; later messages go unheard.

## Reusable idea
A project or asset lifecycle as nested composites: management actions leave from composite borders, suspension resumes through History, per-phase costs come from `getActiveSimpleState()`, and a stock accumulates money. Decide explicitly whether a pause keeps or loses phase progress.

## When the co-pilot should use this
- Portfolio, R&D pipeline, construction-project or asset-lifecycle models with go/stop decisions.
- A user asks why a resumed phase takes longer than planned, or why Condition transitions never fire.
- Related: `bigbook/statechart-guards-branches-and-state-reentry.md` (history, composite interrupts), `bigbook/event-modes-condition-monitoring-and-lifecycle.md` (when conditions are tested), G56.
