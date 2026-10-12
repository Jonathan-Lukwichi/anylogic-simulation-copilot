# Pattern card — CustomStation
- **Source:** AnyLogic example model "CustomStation" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library + PML)
- **Problem it solves:** Pull a defective item off its planned conveyor route in the middle of the line and send it to an off-line rework zone where people work on it, with the conveyor network choosing the way there.

## Block chain
`Source` (every 7 s) → `Queue` → `Convey` *conveyThroughTest* (from the start to the end of the inspection conveyor, passing four Station markups) → `Sink`.
- Each test Station's *On process finished*: with probability `scrapPercentageAtStN` call `conveyThroughTest.cancel(agent)`.
- The cancelled item leaves through the Convey's **`outRedirect`** port → `Convey` *toRepairArea* (*from current position*; target type **custom station** `repairZone`; *leave conveyor on exit*) → `Service` *repair* (operator pool, triangular 0.5 / 1 / 1.5 min, operator walks to the item) → `Sink` (scrap).

## Resources
`ResourcePool` of repair operators (1 m/s, home node; downtime taken from the pool's own properties).

## Key settings worth copying
- **Custom station vs Station** (Help 8.9.10, *Custom station*): a Station times the processing itself; a **Custom station** is only a zone in the conveyor network — the work is whatever blocks you put after the Convey that ends there. It can be a transit point with any number of conveyors in and out, and a `Convey` target (`TARGET_CUSTOM_STATION`). Its polygon has no logical meaning; *Agent location* = near conveyor / centre / random; one *On enter* action.
- **Route to it is found automatically** from the item's current position (model description: the nearest conveyor that leads there is used).
- **Mid-route reroute:** `cancel(agent)` (or `cancelAll()`) on the Convey that is moving the item; it exits through `outRedirect` at once, where a second Convey takes over from *current position* (Help *Convey*).
- Per-station scrap probabilities as four parameters with sliders.

## KPIs instrumented
Visual only. Natural additions: scrap rate per station (count cancellations per callback), repair queue length, operator utilisation, good-output throughput.

## Pitfalls
- Connect `outRedirect` whenever `cancel()` is used (it is also used when a conveyor changes direction).
- Tick *leave conveyor on exit* on the Convey into the custom station, or the item keeps occupying the conveyor while it waits for the operator (G42).
- The station's *On process finished* runs per item only when the station processes items one by one; in *starts when capacity is full* mode it runs only once, when the whole batch is done (Help *Station*) — make per-item decisions elsewhere then, e.g. at a Position on conveyor just after the station.
- Four scrap decisions in series compound: overall yield = product of (1 − p_i); calibrate each station separately.

## Reusable idea
Keep the "happy path" as one long Convey and treat exceptions (defects, wrong labels, overweight) as cancellations from station or sensor callbacks, each redirected to a custom station where a PML sub-process handles it.

## When the co-pilot should use this
Inspection lines with rework/scrap, sortation with a manual reject area, any conveyor exception handling. Related: `videos/mhl-conveyor-station-processing-and-reassembly.md` (Station), `videos/mhl-convey-routing-offsets-leave-on-exit.md` (`outRedirect`, leave-on-exit), `create-conveyor-network-by-code.md`.
