# Pattern card — Schedule Created Programmatically
- **Source:** AnyLogic example model "Schedule Created Programmatically" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Process Modeling Library)
- **Problem it solves:** Build a time-varying schedule in code at startup (here a 4-week cyclic arrival-rate pattern) and plug it into a Source, when the schedule's shape comes from data or parameters rather than from the editor.

## Block chain
`Source` (the editor says *Rate* 1 per day, *Rate schedule* field = the variable `schedule`) → `Delay` (`triangular(0.5, 1, 1.5)` days, maximum capacity) → `Sink`. Model time unit: day.
Main's *On startup* calls `initSchedule()`, which builds the schedule and then switches the Source to it.

## Resources
n/a

## Key settings worth copying
- **The build sequence** (Help 8.9.10, *Schedule API*; the demo's order):
  1. `schedule = new ScheduleWithUnits(PER_WEEK);` — a rate schedule; its values are rates in the unit given here. Other value types: `new Schedule<Integer>()` (counts, e.g. capacity), `new Schedule<Boolean>()` (on/off), `new Schedule<Double>()`.
  2. `setOwner(this)`, `setCalendarType(true)` (calendar dates, daylight-saving safe; `false` counts a day as exactly 24 h — machine time), `setFirstDayOfWeek(MONDAY)`, `setPeriod(4)`, `setGlueIntervals(true)` (touching intervals with equal values merge), `setDefaultValue(0.0)` (value outside all intervals).
  3. `addInterval(week, dayOfWeek, h, m, s, endWeek, endDayOfWeek, h, m, s, value)` once per week: weeks 1–4 get 2.4, 10.5, 32.1 and 1.8 per week. Other overloads take (day, h, m, s, …), (h, m, s, …), (h, m, s, …, value, `int[] weekDays`), or start/end in milliseconds; `addMoment(...)` for *Moments* schedules; `addException(y, mo, d, h, mi, s, …, value, annually)` for holidays.
  4. `schedule.initialize();`
  5. `source.set_rateSchedule(schedule); source.set_arrivalType(Source.ArrivalType.RATE_SCHEDULE);`
- **Reading it back:** `getValue()`, `getValue(time, units)`, `getNextValue()`, `getTimeOfNextValue()`, `getDateOfNextValue()`, `getTimeoutToNextValue()`. The engine Javadoc (*Schedule*) prefers `getTimeOfNextValue()` over the timeout form for scheduling an event at the next change (less rounding error): restart the event with `event.restartTo(schedule.getTimeOfNextValue())`.
- **Alignment:** `setSnapTo(year, month, day, h, m, s)` fixes where the period starts; without it the schedule is snapped to the date of model time zero.
- **Often no code is needed:** a Schedule element can load intervals or moments from a built-in database table (Help *Loading schedule data from database*). Build in code when the pattern is computed at run time — from a forecast, an optimizer's decision variables, per-agent rosters, or experiment parameters.

## KPIs instrumented
None. Check the construction at startup: `traceln(schedule.getValue(PER_WEEK))` and the next change time, then count arrivals per week against the intended rates.

## Pitfalls
- **Forgetting `initialize()` or the arrival-type switch** leaves the Source on its editor settings (G? in `.ingest/proposals/m-basic-3.md`).
- **`setPeriod` unit is ambiguous:** the Help says the schedule's time units, the engine Javadoc says milliseconds; the demo passes `4` with weekly intervals and never calls `setTimeUnits`. Set `setTimeUnits(TIME_UNIT_WEEK)` (or `TIME_UNIT_DAY`; the only calendar-mode units) explicitly and check one period at startup *(unverified)*.
- **Parallel experiments:** a schedule held by a parameter-variation or optimization experiment should use `setSingleThreadMode(false)` (Help).
- **Database route:** imported timestamps without a date get 31-12-1899 (Help); store full date-times.
- A rate schedule holds rates, not counts: 32.1 per week means about 4.6 arrivals per day in that week, drawn as a Poisson stream.

## Reusable idea
Treat a schedule as data: generate intervals from whatever produces the plan (forecast, roster table, decision vector), finish with `initialize()`, and attach it to the block. The same object type drives rates, capacities and on/off shifts.

## When the co-pilot should use this
Forecast-driven arrival profiles, rosters that are decision variables (staffing optimization — `videos/forecast-driven-staffing-optimization.md`), per-scenario seasonality, or any schedule whose number of intervals is not known at design time. Editor-drawn schedules: `basicmodels/defining-a-work-schedule-for-resources.md`.
