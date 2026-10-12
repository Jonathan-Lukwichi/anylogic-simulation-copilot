# Pattern card — OEE (availability × performance × quality) instrumented in a DES model
- **Source:** AnyLogic video "Supply Chain Management Twin for Pharmaceutical Using AnyLogic" (https://youtu.be/uyVqhY-aZSo) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Reporting OEE per machine or line from a simulation so the split between downtime, slow running and defects reflects the system, not the way the model was built.

## Mechanism
- **From the video:** the pharma plant twin shows OEE for mixers, filling lines and packaging equipment.
  - Availability = run time over scheduled time.
  - Performance = actual speed over design speed.
  - Quality = good units over all units.
  - Units/hour, throughput and defect rate sit alongside, and the panel is used to see which loss dominates.
- The OEE definitions themselves are standard lean/TPM material. Everything below is supplementary AnyLogic instrumentation; the video does not show it.
- **Per machine, keep these accumulators and counters:**
  - `plannedTime`: time the machine is scheduled to produce, excluding breaks and off-shift time.
  - `downTime`: failures and setups. Add starved and blocked time only if your stated convention counts them as availability loss.
  - `runTime` = `plannedTime` − `downTime`.
  - `totalCount`, and `goodCount` for first-pass good units only (reworked units are not "good" for OEE).
- **Formulas:**
  - A = `runTime / plannedTime`
  - P = `idealCycleTime * totalCount / runTime`
  - Q = `goodCount / totalCount`
  - OEE = A × P × Q
- **Self-checks:**
  - OEE must equal `goodCount * idealCycleTime / plannedTime`.
  - `plannedTime` must equal the sum of four parts:
    - down time;
    - speed loss (`runTime − idealCycleTime*totalCount`);
    - quality loss (`idealCycleTime*(totalCount − goodCount)`);
    - fully productive time (`idealCycleTime*goodCount`).

## Resources
Each machine is either an agent with a small statechart (Running, Idle/starved, Blocked, Down, Setup) or a resource unit in a pool.

## Key settings worth copying
- **State time:** on each state's exit, add `time() - enteredAt` to that state's accumulator. This is the idiom in `models/oil-terminal.md` and `models/autoclaved-aerated-concrete-factory.md`. For a visual cross-check, drive a Time Color Chart from `unit.getState()` (`basicmodels/gantt-chart.md`).
- **Counts:** `totalCount++` in the machine block's On exit; `goodCount++` on the pass branch of the QC `SelectOutput`.
- **`idealCycleTime`** is a parameter holding the nameplate time per unit. It is **not** the mean of the fitted process-time distribution.
- **Batch equipment** (dryer, steriliser): count units, and set ideal time = batch cycle ÷ full-load units. Under-filled loads then show up as performance loss.
- Guard every ratio with `zidz(a, b)` (see `models/oil-terminal.md`). Reset all accumulators and counters at the end of warm-up.
- Expose A, P, Q and OEE as scalar `Output` elements for experiments and Cloud (`videos/cloud-run-semantics-and-access.md`).

## KPIs instrumented
- A, P, Q and OEE per machine, and for the bottleneck.
- Loss hours by category: down, speed, quality.
- Units/hour and defect rate.

## Pitfalls
- **P = 100 % by construction.** If the Delay or Service time equals the nameplate time, the model cannot lose speed, and OEE collapses to A × Q. Model slow running explicitly, e.g. a process-time distribution whose mean is above the ideal, or micro-stops.
- **`utilization()` is not OEE, and not availability either.** It measures the busy share only and carries no speed or quality information.
- **Starved and blocked time.** Starvation upstream lowers the availability of the machine downstream. State the convention you use, or report both views: the machine's own losses, and the line view.
- **Line OEE is not the mean of the machine OEEs.** Use the bottleneck's OEE, or line good output × line ideal cycle time / `plannedTime`.
- **An ML-predicted OEE** (the video used Python via Pypeline) is a forecast. Compare it with the simulated OEE on the same definition, framed as baseline vs ML-informed, as `INSTRUCTIONS.md` requires.

## Reusable idea
Derive OEE from time accounting plus two counts. Prove the instrumentation with the identity check and with a loss waterfall that sums back to planned time.

## When the co-pilot should use this
- The intake KPI list names OEE, equipment effectiveness or TPM, or the study compares maintenance strategies. Maintenance-strategy comparisons commonly use OEE as the comparison KPI.
- At intake item D12, ask for nameplate cycle times and planned production time. Without them, P and A are undefined.

## Additions (8.9.10 review, 2026-10-01)
- `Delay.statsUtilization` is size ÷ capacity over time (Help 8.9.10), so it means nothing on a Delay with *Maximum capacity* ticked; a Queue's only built-in statistic is `statsSize` (length).
