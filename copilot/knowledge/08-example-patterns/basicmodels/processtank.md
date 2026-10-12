# Pattern card — ProcessTank
- **Source:** AnyLogic example model "ProcessTank" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Model a single-input batch vessel that fills to a set amount, holds it for a processing time and then drains completely before refilling — in one block instead of a Tank, two valves and a timer.

## Block chain
`FluidSource` (100 m³/s; custom batch with a random colour) → `ProcessTank` (capacity 500 m³; delay `uniform(7, 10)` s; output limited to 100 m³/s; drawn on a *Storage tank* markup; *On empty*: `fluidSource.set_customBatch(uniform())`) → `FluidDispose`. Texts show the four phases (empty, filling, processing, emptying) and a time plot shows the level.

## Resources
n/a

## Key settings worth copying
- **Fixed cycle (Help 8.9.10, *ProcessTank*):** filling (input open, output closed) until *Capacity* → processing (both closed for *Delay time*) → emptying (output open, input closed) until empty → next cycle. Inputs are unlimited; cap the discharge with *Limited output rate* (`limitRateOut`, `maxRateOut`).
- **Capacity is re-read every cycle** — at the start and each time the tank has emptied — so a dynamic expression gives a different batch size per cycle; `updateCapacity()` re-reads it at once (not below the current amount). `infinity` is allowed.
- **Partial batch on demand:** `forceProcessing()` closes the input of a partly filled, non-empty tank and starts processing now, calling *On full* as if full (end of a campaign or shift, a starving source). It does nothing while processing, emptying or empty.
- **Delay time** is evaluated when capacity is reached (or at `forceProcessing()`), with the local `batch`; since 8.9.5 it is a dynamic property in ProcessTank and MixTank (release notes), so the hold can depend on the product.
- **Actions:** *On full* (input just closed), *On ready* (hold done, before draining), *On empty* (just before the next cycle — the place to relabel the next batch, as here), *On rate change* (livelock warning, as for Tank).
- **State and timing API:** `isFilling()`, `isProcessing()`, `isEmptying()`, `isEmpty()`, `remainingTime()` / `remainingTime(MINUTE)`, `amount()`, `amountPassedIn()`, `amountPassedOut()`; output batch: same as input, default, or custom (`modeOutputBatch`), with the colour blended towards the output colour during processing.

## KPIs instrumented
Level over time (time plot) and the phase indicators. For capacity studies add the share of time in each phase (filling / processing / emptying / idle) and batches per hour.

## Pitfalls
- **Starved filling never ends:** without enough inflow the tank waits forever below capacity; use `forceProcessing()` (e.g. from an event at shift end) or a dynamic capacity.
- **Discharge rate sets the cycle too:** with a 100 m³/s limit, 500 m³ needs 5 s to drain on top of the hold; downstream throttling stretches it further.
- `remainingTime()` without units returns seconds, not model time units (Help).

## Reusable idea
Pick the vessel block by its rule: *Tank* + valves when you control the cycle yourself (`basicmodels/tank.md`), *ProcessTank* for fill → hold → drain of one stream, *MixTank* for recipes of up to five inputs (`basicmodels/mixtank.md`). Drive the batch size through the per-cycle capacity and close incomplete batches with `forceProcessing()`.

## When the co-pilot should use this
Reactors, pasteurisers, curing or settling tanks, chocolate conches (`models/chocolate-production.md`), any hold-time vessel in a Fluid Library line, and "how do I process a partial batch" questions. Per-cycle batch relabelling is shared with `basicmodels/tank.md` and `basicmodels/pipeline.md`.
