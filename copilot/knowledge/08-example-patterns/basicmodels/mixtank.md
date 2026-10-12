# Pattern card — MixTank
- **Source:** AnyLogic example model "MixTank" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Blend up to five fluid components in a fixed recipe, hold the finished mix for a processing time, then discharge it as one new product batch — a batch-mixing vessel in one block.

## Block chain
Five `FluidSource` blocks (20 m³/s each, each tagged with its own custom batch 1–5 and colour) → `MixTank` inputs `in1`…`in5` → `FluidDispose`. The MixTank is animated on a Storage Tank markup shape.

## Resources
n/a

## Key settings worth copying
- **Cycle (fixed, per Help 8.9.10):** *filling* (each input stays open until its component quantity is in) → *processing* (all ports closed for **Delay time**) → *emptying* (output open, inputs closed). A new mix starts only after the previous one has fully flowed out; the tank starts empty.
- **Recipe:** `mixByAmounts = false` → total amount + `fraction1..5` (normalised, so 0.2/0.1/0.3/0.15/0.25 need not sum to 1 exactly); `true` → absolute `amount1..5`. Demo: total 500 m³.
- **Delay time** is evaluated when the mix completes (`uniform(7, 10)` s here) and can use the input batches `batch1..batch5`.
- **Outflow:** inputs are unlimited; cap the discharge with `limitRateOut = true`, `maxRateOut` (100 m³/s here).
- **Output batch:** `modeOutputBatch = OUTPUT_BATCH_CUSTOM` with any object (a string `"output"` here) — the blend leaves as a new product identity; colour via `customOutputBatchColor`/`outputBatchColor`. During processing the tank colour is interpolated from the component colours to the output colour.
- **State tests for dashboards:** `isEmpty()`, `isFilling()`, `isProcessing()`, `isEmptying()`; `remainingTime()` (s, or `remainingTime(MINUTE)`) while processing; `amountOf(i)` per component (bar chart in the demo); `amountPassedIn(i)`, `amountPassedOut()`.
- **Actions:** *On mix completed*, *On mix ready* (after the delay, before discharge), *On empty*, *On rate change*.
- **Recipe change at run time:** `set_amountN(...)` / `set_fractionN(...)`, then `updateAmounts()` — allowed only while the tank is empty.

## KPIs instrumented
Stage indicators (four text labels coloured by the state tests), component amounts (`amountOf(1..5)`), remaining processing time.

## Pitfalls
- Help 8.9.10 names the total-amount property `totalAmount` with `set_totalAmount()`, but the 8.9.10 class has neither: the property is **`capacity`** (read with `capacity()` / `getCapacity()`, no setter; checked in the Fluid Library Javadoc and the model file). Drive it from a variable/parameter and call `updateAmounts()` while empty.
- `getBatch(i)`, `getBatchColor(i)`, `getBatchSize(i)` index the components **in reverse** while filling/processing (index 0 = input 5, index 4 = input 1); while emptying only index 0 (the mix) exists.
- A slow or empty component source stalls the whole cycle — the mix never completes, and the other inputs stay closed once their share is in. Check component supply before blaming the tank.
- Changing flows inside *On rate change* can trigger itself again (Help warns of a livelock).

## Reusable idea
Use one MixTank per batch vessel whenever a process is "charge ingredients in proportion → react/mix for a time → discharge as a new product" (paint, beverages, chemicals, concrete, feed). The state tests give a free vessel-utilisation breakdown (filling/processing/emptying/idle shares) for bottleneck analysis.

## When the co-pilot should use this
Batch blending or reactor stages in Fluid Library models; recipe what-ifs (fractions as parameters); when a user tries to build mixing from Tank + FluidMerge + Valves by hand (MixTank already does the fill/hold/discharge logic). For a single-input hold-then-release vessel see ProcessTank instead.
