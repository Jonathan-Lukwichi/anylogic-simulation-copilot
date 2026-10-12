# Pattern card — Pipeline
- **Source:** AnyLogic example model "Pipeline" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Make a continuous stream in a pipe visible and traceable as a train of distinct batches (slugs) that move first-in-first-out, e.g. to follow product changes or contamination fronts in a pipeline.

## Block chain
`FluidSource` (maximum rate, custom batch) → `Valve` (rate when open 100 m³/s) → `Pipeline` (capacity 250 m³, drawn on a pipe markup) → `FluidDispose`. A button toggles the valve; a slider is linked to `valve.openRate`.

## Resources
n/a

## Key settings worth copying
- **Start a new batch from code:** `fluidSource.set_customBatch(<object>)` — fluid leaving the source from that moment belongs to the new batch. A batch can be any object (a random number, a string, an agent).
- **Cut the stream every N units:** Valve *Recurrent action on portion* (`actionOnPortion = true`, `portionSize = 100` m³) with *On portion passed* calling `set_customBatch(...)` → a new slug every 100 m³.
- **Cut on flow disturbances:** Pipeline *On rate change* also calls `set_customBatch(...)`, so every stop, restart or rate change starts a fresh slug.
- **Colour per batch:** on the source `customBatchColor = true` with `batchColor = randomColor()`; the demo relies on the colour being worked out again for each new batch *(per-batch re-evaluation not stated in Help — unverified)*.
- **Inspect the pipe:** `numberOfBatches()`, `getBatch(i)`, `getBatchSize(i)` — index 0 is the batch nearest the **output**; Pipeline actions *On new batch at input*, *On new batch at output*, *On full*.
- Valve API: `open()`, `close()`, `toggle()`, `isClosed()`, `dispense(amount)` (+ *On dispense completed*, not the same as *On portion passed*).

## KPIs instrumented
n/a (visual demo); in real models use *On new batch at output* to time-stamp arrivals and compute batch transit times.

## Pitfalls
- Pipelines move batches FIFO and tanks do not mix batches unless a MixTank is used (Help, *Batches*); do not expect blending in a plain Tank.
- The batch-to-colour mapping is not global: the same batch object can be given different colours in different blocks; colour where the batch is created and let it propagate.
- The order in which *On new batch* actions fire across blocks is not guaranteed (a downstream block may react first) — do not chain logic on that order.
- An empty pipeline can still report a zero-size batch that appeared at its input but has not started flowing.
- *On full* is not a level alarm: it fires at most once in the pipeline's life (line fill) and never if the pipe starts full.

## Reusable idea
Batch identity is the Fluid Library's tracking mechanism: generate a new batch object whenever something about the product changes (grade, order, time slice, disturbance) and read it at the outlet — you get product-change tracking and transit times without converting the flow to agents.

## When the co-pilot should use this
Multi-product pipelines, line-fill/flush questions, "which product is at the outlet now", contamination-front tracking, or when a user wants to see flow as slugs. For the valve block itself see `valve.md`; for scheduling many commodities over a network see `models/crude-oil-pipeline-network.md`.
