# Pattern card — Tank
- **Source:** AnyLogic example model "Tank" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Run a tank as a fill-and-draw batch vessel — fill completely, then empty completely, then start a new batch — driven by the tank's own full/empty events.

## Block chain
`FluidSource` (100 m³/s, custom batch = `uniform()`, colour = `randomColor()`) → `Valve` inputValve (100 m³/s) →
`Tank` (capacity 500 m³, starts empty, drawn on a *Storage tank* markup) → `Valve` outputValve (200 m³/s, initially
closed) → `FluidDispose`.
- `Tank` *On full*: `outputValve.open(); inputValve.close();`
- `Tank` *On empty*: `outputValve.close(); fluidSource.set_customBatch(uniform()); inputValve.open();`

Result: fill 5 s, drain 2.5 s, repeat, each fill a new coloured batch.

## Resources
n/a

## Key settings worth copying
- **Tank events** (Help 8.9.10, *Tank*): *On full*, *On empty*, *Action on above* / *Action on below* with thresholds
  (`amountAbove`, `amountBelow`), *On new batch at input* / *at output*, *On rate change*.
- **Behaviour at the limits:** a tank that is not full accepts any input rate; when full, its input is throttled to its
  output; when empty, its output is limited to its input. Optional *Limited output rate* (`maxRateOut`, default 10 m³/s).
- Capacity or initial amount may be `infinity` — a tank can act as an unlimited source or sink.
- Batches pass through a Tank in FIFO order and are **not mixed** (use MixTank for blending); the output batch can be the
  original, the default or a custom one.
- New batch per cycle: `fluidSource.set_customBatch(...)` in *On empty* labels every fill separately (see `pipeline.md`).

## KPIs instrumented
Visual (tank level and batch colours). Useful: `tank.amount()`, cycle count, fill and drain durations.

## Pitfalls
- **No event for the starting state.** *On full* does not fire if the tank starts full, nor *On empty* if it starts empty
  (Help). A tank initialised full with the drain valve closed never starts its cycle — open the right valve in On startup.
- **Plain Tank ≠ mixing vessel:** the layers stay separate batches; blending needs MixTank.
- Keep valve switching in the level events rather than in *On rate change*, where one change can trigger the next
  immediately (livelock warning in the Help for rate-change actions).

## Reusable idea
Let the vessel's level events own the cycle: full → close inlet, open outlet; empty → close outlet, relabel the batch,
open inlet. The same three lines turn any Tank into a day tank, reactor charge vessel or silo with a fill-and-draw rule.

## When the co-pilot should use this
Batch tanks, day tanks, surge vessels, silo fill/empty cycles, and questions about Tank full/empty behaviour. Related:
`valve.md`, `fluidpickup.md` (threshold events), `fluidenter-and-fluidexit.md`, `mixtank.md`, `pipeline.md`.
