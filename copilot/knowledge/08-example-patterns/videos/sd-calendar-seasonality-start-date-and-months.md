# Pattern card — Calendar-driven SD inputs: zero-based getMonth(), a start date that defaults to the build date, and three kinds of "month"
- **Source:** AnyLogic 8.9.10 Help tutorial "Bass Diffusion (System Dynamics)" — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Make monthly seasonality, monthly costs and month-based decision variables line up in a years-based SD model, and keep results from depending on the day the model was built.

## Mechanism
Phases 11–13 of the tutorial add seasonality, a promotion switch and an optimization to the Bass model:
- Table function `demand` with 12 points on arguments 1…12, Linear interpolation, Out of range *Nearest*.
- `AdoptionFraction` becomes a dynamic variable fed by a function that returns `demand(getMonth())/200.0`
  (the shipped models call it as `adoptFraction(time())`; the argument is unused).
- A cyclic event adds `MonthlyExpenditures` to `TotalExpenditures` every month. A two-state statechart sets the spend
  to 0 after the Timeout `SwitchTime` (years).

Three calendar facts collide (Help 8.9.10):
1. **`getMonth()` is zero-based.** January is 0 and December is 11 (Help *getMonth*). With a table on 1…12, January reads
   row 1 only because *Nearest* clamps 0 up to 1. Every later month reads the previous month's row, and row 12 (the
   pre-holiday peak) is never used. The shipped 8.9.10 models *Bass Diffusion - Phase 4, 5 and 6* all pair
   `demand(getMonth())` with a 1…12 table. *Out of range = Error* would have exposed this in January.
2. **Calendar functions read start date + model time.** The start date defaults to the date the model was created
   (Help *Model time*), and every experiment keeps its own start date (each experiment in the `.alp` stores its own
   `InitialDate`). The shipped models start on 21 May 2010. A copy built today starts today, shifting the season, so
   its runs and its optimum differ.
3. **Three different months.** In a years model a year is 365 days and a model month is 30 days (G2), so an event
   repeating "every month" fires every 30/365 = 0.0822 years. The tutorial's optimizer steps `SwitchTime` by
   0.0833 = 1/12 year, and `getMonth()` follows real calendar months of 28 to 31 days.

## Resources
n/a

## Key settings worth copying
- Index fix: `demand(getMonth() + 1)`, or rebuild the table on 0…11. To anchor the season to elapsed time rather than the
  calendar, define the table on 0…12 (last value = first), set Out of range *Repeating* (periodic, with the argument
  range as the period — Help *Table function*), and pass `time() * 12` in a years model. The start date then no
  longer matters.
- Set the start date explicitly in **every** experiment that runs the model (Simulation, Optimization, …) to the
  scenario's real start. Check it once with `traceln(date() + " month " + getMonth())` in Main's On startup.
- Accrue spend as a stock: `CumulativeSpend` with inflow `MonthlyExpenditures * 12` (per year). Unlike a cyclic event,
  this is exact for any switch time.
- Tutorial optimization (phase 13): objective `root.TotalExpenditures` (minimize); `MonthlyExpenditures` continuous
  0–10,000; `SwitchTime` discrete 0–1.5, step 0.0833; requirement `root.Adopters >= 80000`; stop at 1.5 years.

## KPIs instrumented
Time plots of AdoptionFraction, AdoptionRate and DiscardRate. Add a validation plot of the lookup value against
`getMonth()` over one simulated year: the peak must fall in the intended month.

## Pitfalls
- **Event-based accrual bills whole months up front.** The event first fires at time 0 and then every 30 days. On the
  optimizer's grid (`SwitchTime` = k/12 year, k < 72) it therefore fires k + 1 times before the switch, and the
  objective is a step function of `SwitchTime`. At `SwitchTime = 0` the switch and the first billing happen at the
  same instant, and their order decides the charge (G60).
- **Assigning a parameter directly** (`MonthlyExpenditures = 0.0;` in an entry action) skips its On change handler
  (Help *Parameters*). SD formulas still pick up the new value; use `set_MonthlyExpenditures(0)` when something listens
  to On change.
- **Unit tags on SD constants.** The shipped Phase 6 stores `ContactRate` as a Rate of 100 *per minute* and
  `ProductLifeTime` as a Time of 2 *minutes*, while the tutorial defines 100 per year and 2 years. The Help pages checked
  do not say whether the tag is applied when a formula reads the value *(unverified)*. Print both at start before
  reusing the model. In new models, give such constants the model's own time unit or a plain double type.
- **Deterministic model.** One run per candidate is exact, so replications only waste the 500-iteration budget (G14).

## Reusable idea
Anything that reads the calendar turns the start date into a model input. Pin it, test the index at the month
boundaries, and use one definition of "month" throughout.

## When the co-pilot should use this
- Seasonal demand from monthly tables, calendar-timed policies, month-grid decision variables, and monthly cost accrual
  in SD or hybrid models.
- Symptoms: a seasonal peak one month late, results that differ between machines or after creating a new experiment,
  costs that jump in steps as a switch time moves.
- Related: G2, G14, G60; `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`; `basicmodels/bass-diffusion-phase-4.md`, `-phase-6.md`.
