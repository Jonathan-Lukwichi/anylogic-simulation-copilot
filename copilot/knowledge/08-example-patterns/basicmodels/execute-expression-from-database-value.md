# Pattern card — Execute Expression From Database Value
- **Source:** AnyLogic example model "Execute Expression From Database Value" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (data input)
- **Problem it solves:** Keep per-type stochastic inputs (which distribution, which parameters) as data in the model database — editable like any table — instead of hard-coding them in blocks.

## Block chain
`Source` (10 per minute; agent type `Component` with a `String` parameter `type`; *Set agent parameters from DB* on table `components`, `type` ← column `type`) → `Queue` → `Delay` *processing* → `Sink`.
- Table `components`: `typeA | triangular(3, 5, 7)`, `typeB | uniform(5, 10)`, `typeC | triangular(2, 4, 6)`. The column `processing_time` has the database type **Code**.
- The Delay's *Delay time* is a query built in the field's database mode: *select unique value* of `processing_time` where `type` equals `agent.type`. Because the cell is Code, AnyLogic evaluates the stored expression, so every agent gets a fresh draw from its type's distribution (Help 8.9.10, *Data types → Code*).
- *On enter* prints the agent type and `self.delayTime(agent)` to the console.

## Resources
n/a

## Key settings worth copying
- **Code column → property value:** select the Code cell in a block property's database mode; AnyLogic retrieves, evaluates and uses the result (Help *Data types*).
- **Code in plain code** (Help *Executing functions from the database*): `executeExpression(code, "name1", v1, …)`, `executeExpression(ResultType, code, …)` for a typed result, `executeAction(code, …)` for statements. Since 8.9.6 a Code cell can also be run with `execute(this)`. If a stored snippet will not run that way, keep it in a String column and use `executeExpression` / `executeAction`.
- **Version notes (release notes):** 8.9.10 fixed `executeExpression()` failing when called from an agent other than Main; 8.8.6 removed a needless warning; 8.3 made it safe for parallel multi-run experiments.

## KPIs instrumented
Console trace per agent (type and a delay value).

## Pitfalls
- **The trace does not show the real delay.** `self.delayTime(agent)` re-evaluates the dynamic expression, so it prints a new random draw, not the one the Delay scheduled. To log the value used, draw it once into an agent variable upstream and set Delay time to that variable.
- **Arrivals cycle the table in order.** A rate-driven Source with *Set agent parameters from DB* reads the rows one after another and starts again at the first (Help *Source creates agents with parameters read from DB*): here the mix is A, B, C, A, B, C… — deterministic, not a random mix. If the mix must be random, untick that option and draw `type` in the Source's *On exit* from a discrete distribution (e.g. a Custom Distribution over the types) and keep the table only for the times.
- **Typos surface only at run time.** A malformed expression in a cell is not compiled with the model; evaluate every Code cell once in Main's *On startup* to fail fast.
- Stored code runs with full model access — treat the table as code under review, not free-text data.
- Edited in Excel: the table is refreshed only if imported tables auto-update (G48).

## Reusable idea
"Distributions as data": one column names the entity class, a Code column holds its time/size expression, and blocks look it up per agent. Analysts change a distribution or add a class without touching the model logic.

## When the co-pilot should use this
When processing, service or travel times differ by product/patient/order type and are maintained in spreadsheets; when a user asks how to put `triangular(...)`-style expressions in the database; when a scenario table must switch distributions between runs.

## Additions (8.9.10 review, 2026-10-01)
- 8.9.10 fixed a bug where `executeExpression()` threw an error when called from an agent other than Main (release notes); on 8.9.9 and earlier, call it from Main.
