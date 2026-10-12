# Pattern card — Source With Arrivals From Database Table
- **Source:** AnyLogic example model "Source With Arrivals From Database Table" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Replay recorded arrivals — each row of a table is one arrival at its exact timestamp, optionally bringing several agents and carrying attribute values — instead of sampling arrivals from a distribution.

This card also folds in the sister demo "Source Arrival Modes" (basicmodels, 8.9.10) as a mode-choice guide.

## Block chain
- `Source` (*Arrivals defined by* = **Arrival table in Database**, table `arrivals`, *Arrival date* = column
  `arrival_date`, *New agent* = `Truck` with parameter `name` mapped to column `truck`) → `Sink` (*On enter* prints the
  name and `date()`).
- Second pair: the same table with *Multiple agents per arrival* ticked and *Agents per arrival* bound to column `n`
  (e.g. a truck bringing 40 pallets) → `Sink`.
- The table (built-in database): `arrival_date` TIMESTAMP, `truck` text, `n` integer — four trucks on one day.

## Resources
n/a

## Key settings worth copying
- **Arrival table in Database** (`Source.DATABASE_ARRIVAL_TABLE`; Help 8.9.10, *Source*, *Source creates agents
  according to timestamps in DB*): one agent per row at the row's timestamp; *Agents per arrival* may be an expression
  or, via the field's menu, a **table column**. Agent parameters are mapped to columns in the *New agent* table; a
  matching agent type can be generated from the table (Projects → table → *New > Agent type*).
- **Mode choice (Source Arrival Modes demo):**
  | Situation | Mode (`arrivalType`) |
  |---|---|
  | Poisson stream, constant rate | *Rate* (`RATE`) |
  | Regular or non-exponential gaps | *Interarrival time* (`INTERARRIVAL_TIME`; first arrival after timeout / at start / at a time) |
  | Rate varying by hour of day or week | *Rate schedule* (`RATE_SCHEDULE`; intervals with a rate each; optional *Modify rate* = expression of `baseRate`) — see G5 |
  | Known moments with known group sizes (bus, shift start) | *Arrival schedule* (`ARRIVAL_SCHEDULE`; a `Schedule<Integer>` in exact-times mode, value = agents at that instant) |
  | Recorded history, one row per arrival | *Arrival table in Database* |
  | Triggered by model logic | *Calls of inject()* (`MANUAL`) |
- In the demo the rate schedule repeats daily with 24 hourly rates and a histogram of `getHourOfDay()` at exit checks
  the realised profile; the arrival schedule holds nine daily instants with 4–20 agents each.

## KPIs instrumented
Console trace of each arrival; in the modes demo, a histogram of arrivals by hour.

## Pitfalls
- **Absolute timestamps meet the model start date.** The demo's first truck is 7.5 days after the model start date, so
  a run that stops at a fixed time can end before anything arrives. Set the start date just before the first record;
  what happens to rows dated before the start is *(unverified)*.
- **Help name error:** the *Source* page lists the schedule modes as `Source.RATE_TABLE` / `Source.ARRIVAL_TABLE`; 8.9.10
  defines `RATE_SCHEDULE` / `ARRIVAL_SCHEDULE` (`javap`). The old names belong to the table-function modes deprecated
  since 6.5.1.
- *Set agent parameters from DB* is hidden in this mode — the mapping lives in the *New agent* table instead.
- Rate: a rate ≤ 0 schedules no arrival until it turns positive; Interarrival: an infinite value stops the Source for
  good, zero or negative raises an error (Help).
- A replayed trace reproduces the past exactly once; it has no randomness to replicate. Use it to validate, then fit
  distributions or schedules for what-if runs.

## Reusable idea
Keep two arrival generators ready: a trace-driven Source reading the historical table (validation: does the model
reproduce last month's queues?) and a fitted or scheduled Source (experiments). Switch between them with one
parameter so both runs share every downstream block.

## When the co-pilot should use this
Users with timestamped arrival logs (truck gate logs, ED registrations, order books), validation against history,
scheduled deliveries with known quantities, or questions about which *Arrivals defined by* option to choose. Related:
G5, `getting-values-from-anylogic-database.md`, `../videos/excel-round-trip-results-and-cloud.md` (keeping imported
tables up to date).
