# Pattern card — FluidConvert
- **Source:** AnyLogic example model "FluidConvert" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Change the quantity basis or the product identity of a flow in-line — packaging/unpackaging, unit conversion, yield gain or loss — without a tank.

## Block chain
`FluidSource` (100 m³/s, custom batch 1, red) → `FluidConvert` (custom output batch 2, yellow-green) → `FluidDispose`. A slider is linked to `fluidConvert.factor`; a stacked time chart plots `currentRateIn()` and `currentRateOut()`.

## Resources
n/a

## Key settings worth copying
- **Rule (Help 8.9.10):** output rate = input rate × `factor` at every instant; `factor` > 0, may be above or below 1. Change it at run time with `set_factor(x)` (or a linked slider).
- **Zero capacity:** the block holds no fluid, so any blockage downstream stops the upstream flow at once — put a Tank before or after it if a buffer is needed.
- **Relabel the product:** *Custom output batch* (`modeBatchCustom`, `customBatch`, optional colour) gives the converted flow a new batch identity, and the expression may depend on the input batch.
- Rates below `Utils.RATE_TOLERANCE` (1e-9) are snapped to 0.

## KPIs instrumented
Input vs output rate over time (`currentRateIn()`, `currentRateOut()`).

## Pitfalls
- The factor changes *rates*, so mass balance is intentionally broken: `amountPassed` in and out differ by the factor. Document the unit on each side (e.g. m³ in, "pallet-equivalents" out) or later KPIs will mix units.
- Using it to model a *time* delay does not work — it has no volume; use a Pipeline or Tank for transit time.

## Reusable idea
Treat FluidConvert as the continuous-flow equivalent of "1 input becomes k outputs": filling litres into bottles (factor = 1/bottle volume), tonnes of ore to tonnes of concentrate (factor = yield), wet to dry mass (factor = 1 − moisture). Pair it with a custom output batch so the downstream flow is also renamed to the new product.

## When the co-pilot should use this
When a Fluid Library model crosses a unit boundary or a yield step (bulk → packages, raw → refined) and the user is tempted to rescale numbers by hand in several blocks. For converting a fluid stream into discrete agents use FluidToAgent instead (`fluidtoagent-and-agenttofluid.md`).
