# Pattern card — Split One Stream into Multiple Streams
- **Source:** AnyLogic example model "Split One Stream into Multiple Streams" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Divide one continuous stream into N equal (or weighted) streams, when FluidSplit only has two outputs, and keep the shares right when one branch is shut.

## Block chain
- **Hand-built 1→4 cascade:** `FluidSource` → `FluidSplit` (1/4 : 3/4) → out1 to a pipeline; out2 → `FluidSplit1`
  (1/3 : 2/3) → out1 through a `Valve` to a pipeline; out2 → `FluidSplit2` (1/2 : 1/2) → two pipelines. Every branch ends
  in a `FluidDispose`, and each gets a quarter.
- **Reusable 1→N block `FluidSplitN`:** `FluidSource1` → `FluidExit` (*Forward flow to* =
  `fluidSplitN.splits.get(0).enter`) → inside `FluidSplitN`, a population `splits` of `fluidEnters.length − 1` agents of
  type `FluidSplitConnectable` (`FluidEnter` → `FluidSplit` → two `FluidExit`s) → the ten `FluidEnter` blocks passed in as
  the parameter `fluidEnters` (each → `FluidDispose`).

## Resources
n/a

## Key settings worth copying
- **Cascade fractions for equal shares:** split *i* (0-based) of a chain feeding *n* outputs takes `fraction1 = 1.0 / (n - i)`
  and `fraction2 = (n - i - 1.0) / (n - i)`: the first keeps 1/n and passes the rest, the next keeps 1/(n−1) of what is
  left, and so on — every output ends with 1/n. For weights w₀…wₙ₋₁, use w_i / (w_i + … + wₙ₋₁).
- **Wiring at start-up:** `FluidSplitN.initialize()` runs on startup (and from the parameter's *On change*): for each
  split, `split.exit1.connect(fluidEnters[i])`; `split.exit2.connect(...)` to the next split's `enter`, or to the last
  output for the final split; then `set_fraction1()` / `set_fraction2()`. `FluidExit` → `FluidEnter` links exist for
  exactly this: networks built from data or from replicated fragments (Help 8.9.10, *FluidExit*; one exit ↔ one enter).
- **Shutting a branch:** a check box closes the valve and switches that split to `SplitMergeMode.SPLITMERGE_NEUTRAL`,
  then `recalculateFractions()` re-spreads 1/n over the splits still in `SPLITMERGE_PROPORTIONAL` (n = their count + 1).
- The custom block's icon has *On click* `return true;` so it can be opened at runtime (G36).

## KPIs instrumented
Visual (flow rate per branch). Read `fluidSplit.out1.rate()` / `out2.rate()` or `amountPassed()` on the disposes to
verify equal shares.

## Pitfalls
- **Proportional mode couples the outputs** (out1/fraction1 = out2/fraction2, Help *FluidSplit*): a closed branch
  forces its sibling to zero and backs up the whole chain. Switch that split to Neutral, or change its fractions, when
  a branch closes.
- The `splits` population is sized when `FluidSplitN` is created; changing `fluidEnters` later re-wires but cannot add
  splits *(inferred from the replication expression)*.
- `priorityOutput2Custom = 10` on the first split is a leftover: priorities act only in Priority mode.

## Reusable idea
Build N-way continuous splitting from a chain of two-way proportional splits with fractions 1/(n−i), wrapped in a
custom agent whose outputs are connected by code through FluidExit/FluidEnter. The same trick distributes a feed over
a variable number of tanks, lines or customers read from data.

## When the co-pilot should use this
Manifolds and distribution headers, splitting a bulk feed over several lines or silos, fluid networks whose shape
comes from data, and "my split stops when one line is closed" questions. Related: `fluidsplit.md`,
`fluidenter-and-fluidexit.md`, `fluidmerge.md` (modes), `valve.md`.
