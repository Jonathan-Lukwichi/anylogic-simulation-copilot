# Pattern card — Calendar-true time: DST-safe daily events, 0-based date fields, clock readers and run-speed control
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 16 "Model time, date and calendar. Virtual and real time" — distilled, original wording
- **Paradigm:** Method (any paradigm)
- **Problem it solves:** Daily events and shifts that drift by an hour, dates off by a month, "opening hours" that break after noon, results that change with the PC's locale, and demos whose speed you want to script.

## Mechanism
Checked against Help 8.9.10 (*Time functions*, *toTimeoutInCalendar*, *toDate*, *getMonth*, *Model time*, *Schedule*, *Reproducible model runs*) and the 8.9.10 book demos.
1. **Two clocks.**
   - *Model time* is a double in model time units. Months and years used as units are fixed at 30 and 365 days (G2).
   - The *model date* is the Start date plus elapsed time, expressed in the computer's default time zone, daylight saving time (DST) included (Help *toDate*, *Schedule*).
   - Durations use the fixed multipliers `minute()`, `hour()`, `day()`, `week()` (KNOWN-KB: G3 units note). Calendar offsets need the date functions below.
2. **DST moves clock-time events.** `day()` is always 24 hours. A cyclic event that should fire every day at 08:00 therefore fires at 07:00 or 09:00 after a DST switch (Help).
   - **Fix:** set the recurrence to `toTimeoutInCalendar(DAY, 1)` and choose the model time unit in the unit drop-down next to the field. The function already returns model units, and a cyclic recurrence is re-evaluated at every occurrence.
   - For the first occurrence use `getTimeoutToNextTime(8, 0, 0)`.
   - `toTimeoutInCalendar` depends on the current date, so never use it to initialise a constant (Help).
3. **Schedules and DST** (Help *Schedule*):
   - A schedule mapped to calendar dates keeps the clock times, so a 00:00–08:00 shift lasts 7 or 9 hours on the switch nights.
   - An unmapped schedule keeps the durations, so the shift slides to 01:00–09:00 until DST ends.
   - The DST rules come from the operating system's locale. The same model can therefore give different results on a PC with other regional settings (Help *Reproducible model runs*). This applies to a model built where there is no DST (e.g. South Africa) and run elsewhere *(inferred)*.
4. **Date fields are Java-calendar style** (Help):
   - `getMonth()` and the `month` argument of `toDate(y, m, d, h, min, s)` are **0-based**: JANUARY = 0, DECEMBER = 11. Pass the constants, as in `toDate(2026, MARCH, 1, 8, 0, 0)`, and add 1 for display or 1-based tables.
   - `getDayOfWeek()` returns SUNDAY = 1 … SATURDAY = 7.
   - `getHourOfDay()` is 0–23. `getHour()` is the **12-hour** reading, paired with `getAmPm()`.
   - `hour()` is a duration, not a clock reading.
   - Every getter also takes a `Date` argument, e.g. `getDayOfWeek(d)`.
5. **Calendar arithmetic** (Help):
   - `addToDate(date, unit, amount)` is DST-aware;
   - `differenceInCalendarUnits(unit, a, b)` takes two dates or two model times;
   - `dateToTime(d)` and `timeToDate(t)`; `timeToDate` returns null for infinity;
   - `dropTime(d)` gives midnight; `getDateWithTimeNextTo(d, h, m, s)`;
   - `time(MINUTE)` gives the elapsed time in a chosen unit; `toModelTime(195, SECOND)` and `toTimeUnits(t, HOUR)` convert units.
   - Events can also target dates with `restartTo(date)` (`bigbook/event-modes-condition-monitoring-and-lifecycle.md`).
6. **Run speed.**
   - *Virtual time* runs as fast as possible. *Real time with scale* runs a given number of model units per real second, and the engine can only promise never to run faster than that.
   - Only the Simulation experiment offers real time; the other experiment types always run virtual (Help).
   - At runtime, call `getEngine().setRealTimeMode(true/false)`. `getEngine().setRealTimeScale(x)` changes the scale without switching mode. `getRealTimeMode()`, `getRealTimeScale()` and `getEngine().getTimeUnit()` read the current settings. The offline Help's Engine page lists only `getTimeUnit()`. All five methods exist on `Engine` in the 8.9.10 jar, and the 8.9.10 demo *Combo Box Controls Simulation Speed* calls the two setters.

## Resources
n/a

## Key settings worth copying
- **Opening hours** as a boolean function: `getDayOfWeek() != SATURDAY && getDayOfWeek() != SUNDAY && getHourOfDay() >= 9 && getHourOfDay() < 18`. For resource availability prefer a Schedule (`basicmodels/defining-a-work-schedule-for-resources.md`).
- **Speed selector.** A combo box with items x1 / x10 / Fast. The Action calls `setRealTimeMode(false)` for Fast; otherwise it calls `setRealTimeMode(true)` followed by `setRealTimeScale(1 or 10)`.
- **Start date.** It defaults to the day the model was created. Set it to the first timestamp of the input data.
  - The Help's recipe to start "today" is `getEngine().setStartDate(Calendar.getInstance().getTime())` in the experiment's *Initial experiment setup*.
  - A run then depends on the day it is launched, so keep a fixed date for analysis (Help: fix the start and stop dates when converting dates).
- **Stop at a date.** *Stop at specified date* recomputes the stop time from the start date and the unit.

## KPIs instrumented
n/a. Print `date()` beside KPIs, and label dashboards with calendar dates rather than raw model time.

## Pitfalls
- **Wrong table in the source text.** The Big Book's time-unit table (p. 3) gives wrong millisecond values for MONTH and YEAR. The prose, a 30-day month and a 365-day year, is right. Do not copy the table.
- **Calendar functions only mean something when the start date means something.** Set the start date before writing any date logic.
- **Mixing clocks.** Comparing `time()` with a date, or adding `day()` to schedule "the same time tomorrow", reintroduces the DST drift.

## Reusable idea
Durations come from fixed multipliers, and calendar positions come from date functions. Pin the start date and the locale before trusting any clock-time result.

## When the co-pilot should use this
- Models driven by dated data (arrivals by hour or weekday, shift rosters, monthly demand): hospital and ED twins, call centres, maintenance calendars.
- **Symptoms:** an event or shift drifts by one hour twice a year; a date lands in the next month; afternoon logic fails; results differ on another PC.
- Scripting demo speed.
- **Related:** G2, G3, G17; `bigbook/event-modes-condition-monitoring-and-lifecycle.md`; `basicmodels/implementing-work-shifts-for-resources.md`.
