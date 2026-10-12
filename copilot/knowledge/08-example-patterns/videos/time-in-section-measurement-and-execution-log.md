# Pattern card — Time in a flowchart section, plus per-agent export via the execution log
- **Source:** AnyLogic video "How to measure the agents’ time in the system" (https://youtu.be/JcFqegObRK8) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Measure how long agents spend in any stretch of a flowchart (the whole system or one segment), then get the per-agent values out of AnyLogic for offline analysis without writing logging code.

## Block chain
Put `TimeMeasureStart` where the interval begins and `TimeMeasureEnd` where it ends. For time in system, the end block goes just before the `Sink`. The two blocks are linked by reference, not by a connector. In the end block's **TimeMeasureStart blocks** list you pick its start block, or several of them. One end block can list many start blocks, so agents that enter through different doors are rolled into one KPI. Several pairs can share a flowchart and overlap, which splits one journey into segments. The video's job shop measures dock wait plus transfer, rack dwell, and truck total.

## Resources
n/a

## Key settings worth copying
- Built-in statistics of `TimeMeasureEnd`:
  - `distribution` is a HistogramData over every measured agent (e.g. `tmEnd.distribution.mean()`).
  - `dataset` is a DataSet of recent measurements, sized by **Dataset capacity** (default 100).
- Values are in model time units. Convert them explicitly for reporting, e.g. `tmEnd.distribution.mean() / minute()`.
- One-step histogram: right-click the end block and choose **Create chart → Distribution**. Put the unit in the chart title.
- Raw export:
  1. Select the model's **Database** item. In its Log section, tick **Log model execution**.
  2. Run the model, then **stop** it. A **Log** branch appears under Database.
  - `datasets_log` holds every dataset in the model. Filter its `agent` column to your TimeMeasureEnd block. Library blocks are agents, so they appear there. Each row is one agent's measurement. Help describes the stored value as the time since the start block; the video reads the pair as the agent's timing. Check the column meaning on first use.
  - `histograms_log` holds the per-bin PDF and CDF of each histogram data object. Filter it the same way.
- Logs are read-only, so copy the rows into a spreadsheet or analysis tool. *Beyond the video (AnyLogic Help):* Database → Export → **Export tables at the end of model execution** writes chosen tables, logs included, to an Excel file automatically.
- Histogram-data, dataset and statistics elements have a **Log to database** checkbox that feeds `histograms_log`, `datasets_log` and `statistics_log`.
- Run in virtual time to fill the histogram faster.

## KPIs instrumented
Time in system or in any segment: mean, full distribution (PDF/CDF) and per-agent values.

## Pitfalls
- Execution logging works for the **Simulation** experiment only. Parameter Variation, Optimization and Monte Carlo runs do not fill it, so collect per-replication KPIs through the experiment instead.
- The Log branch appears only after the model is stopped.
- `dataset` keeps only the last *Dataset capacity* points. Use `distribution` for whole-run statistics, or raise the capacity. It is unverified whether `datasets_log` is capped the same way, so compare its row count with the Sink's count.
- Logging slows long runs. On each log item you don't need, tick **I do not need this type of log**.

## Reusable idea
Use TimeMeasure pairs for live, in-model interval KPIs. Add execution logging when you need an audit-ready per-agent dataset. You get both without any custom Java.

## When the co-pilot should use this
- The user wants cycle time, time in system or time in a sub-process, or needs its distribution and not just the mean.
- The user needs raw per-agent rows for a report, a distribution fit or an external tool (Excel, Python). Enable logging on a single Simulation run. For multi-run experiments, export replication-level KPIs instead.

## Additions (8.9.10 review, 2026-10-01)
- Chart creation wizard (8.9.6+; Help 8.9.10 *Chart creation wizard*): right-click any block or markup element of the PML, MHL, Rail, Road Traffic or Pedestrian libraries → *Create Chart…*, pick a statistic (Entries, States, Utilization, MTBF, MTTR, WIP), a chart type and metrics; the data items come pre-wired — the fastest way to instrument MHL states and reliability.
- Every Data Set keeps only its latest *Keep up to … samples*; size it as run length ÷ recurrence + 1 before exporting (gotcha G18).
