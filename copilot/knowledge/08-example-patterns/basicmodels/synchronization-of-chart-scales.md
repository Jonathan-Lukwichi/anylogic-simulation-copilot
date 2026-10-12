# Pattern card — Synchronization of Chart Scales
- **Source:** AnyLogic example model "Synchronization of Chart Scales" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (presentation)
- **Problem it solves:** Keep two or more time plots on the same vertical scale so their curves can be compared by eye, while the range still follows the data.

## Structure
Two dynamic variables `A` and `B` (products of sine waves, amplitude up to 10) are each drawn on their own time plot
(`plotA`, `plotB`; window 100 time units, 1,000 samples kept, updated every 0.1 min, vertical scale set to *Fixed*).
A cyclic event `synchronize` (first at 0.5 min, then every minute) takes the larger of the two plots' maxima and the
smaller of their minima and applies that range to both plots.

## Resources
n/a

## Key settings worth copying
- Chart items by index: `plotA.get(0)` returns the plot's first data item — for a time plot its DataSet — so
  `plotA.get(0).getYMax()` / `getYMin()` read the range of the stored samples (`Chart<E>.get(int)`; Help 8.9.10,
  *Time Plot*, *Data set*).
- `plot.setFixedVerticalScale(min, max)` sets the range for time plots and plots; a time stack chart only has
  `setFixedVerticalScale(max)`.
- Loop over all item indices (`getCount()`) and all plots when there are more than two.

## KPIs instrumented
n/a (display technique).

## Pitfalls
- **Empty data gives infinities:** `getYMax()` is −∞ and `getYMin()` +∞ while a data set is empty (Help), so do not run
  the synchronisation before the first sample exists — the demo starts it at 0.5 min for that reason.
- The range covers the *stored* samples; if a plot keeps more samples than its window shows, off-screen history
  widens the scale.
- A flat curve gives min = max; add a small margin before applying.
- There is no call that switches a plot back to automatic scaling (only `setFixedVerticalScale` exists in the 8.9.10
  engine, checked with `javap`); once code fixes the scale, code owns it.
- The model's description is stale: it mentions a 5-unit period and internal data-set names; the current code uses
  the public `get(i)` API and a 1-minute period.

## Reusable idea
For side-by-side comparisons (scenario A vs B, station 1 vs 2), compute one shared range from all charts' data sets on a
timer and push it to every chart, adding a margin. Viewers then compare heights, not axis labels.

## When the co-pilot should use this
Dashboards with small multiples, scenario comparison screens, and "my two charts look similar but the axes differ"
complaints. Related: `linked-charts.md` (shared selection across charts), `../bigbook/controls-link-direction-sync-and-replicated-controls.md`.
