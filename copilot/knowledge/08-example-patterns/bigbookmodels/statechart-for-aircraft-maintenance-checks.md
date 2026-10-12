# Pattern card — Statechart for Aircraft Maintenance Checks
- **Source:** AnyLogic example model "Statechart for Aircraft Maintenance Checks" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Schedule nested preventive-maintenance levels, each due by calendar age and/or usage, for an asset that alternates between work and standby.

## Structure
Agent `Aircraft`, model time unit Day.
- **States:** Available, Flight, and the checks ACheck, BCheck, CCheck, DCheck. Four branches are chained: `branch` → `branch1` → `branch2` → `branch3`.
- **Start.** The entry point leads to `branch`, so a new aircraft passes through the check cascade before its first flight.
- **TakeOff** (Available → Flight): timeout `randomTrue(0.5) ? 2 : 15` hours. Action: `TimeOfTakeOff = time()`.
- **Landing** (Flight → `branch`): timeout `uniform(3, 12)` hours. Action: adds `differenceInCalendarUnits(HOUR, TimeOfTakeOff, time())` to both usage counters.
- **Cascade, heaviest first.** Each branch has one conditional exit to its check and a Default exit to the next branch. The last Default returns to Available.
  - D: `differenceInCalendarUnits(YEAR, DateOfLastDCheck, date()) >= 5`
  - C: `…(MONTH, DateOfLastCCheck, date()) >= 18 || FlightHoursSinceLastCCheck >= 9000`
  - B: `…(MONTH, DateOfLastBCheck, date()) >= 3`
  - A: `…(MONTH, DateOfLastACheck, date()) >= 1 || FlightHoursSinceLastACheck >= 500`
- **Check durations** are the timeouts back to Available: A 15 h, B 15 h, C 2 weeks, D 2 months.
- **Downward reset.** The action on each check's exit transition stamps `date()` on that check and on every lighter one, and zeroes the matching hour counters. D resets A–D and both counters; A resets only A.
- **Data:** four `Date` variables that start at `date()`, two hour counters, and `TimeOfTakeOff`, a model time. A TimeColorChart plots the state over time.

## Resources
n/a. Hangar and crew capacity are not modelled.

## Key settings worth copying
- **Priority by chaining branches.** Two checks can fall due together, e.g. A and C. With several true exits on one branch the choice is arbitrary (Big Book ch. 7 p. 18). A chain of single-condition branches makes "the heaviest due check wins" explicit and deterministic.
- **Calendar arithmetic.** `differenceInCalendarUnits(unit, a, b)` has overloads for Dates and for model times (Help 8.9.10). Here it turns one flight into hours, whatever the model time unit.
- **Reset on completion.** Put the reset in the check's *exit* transition, so a check that is still running does not count as done.
- **Month means 30 days.** As a timeout unit, MONTH is a fixed 30 days (Help *Model time*). Use `toTimeoutInCalendar(MONTH, 2)` when exact calendar months matter.

## KPIs instrumented
The demo shows only the state timeline. Worth adding:
- availability: the share of time in Available + Flight;
- checks per type per year;
- flight hours between C checks;
- for a fleet, the number of aircraft in maintenance at once, which sizes hangar capacity.

## Pitfalls
- **Due tests run only at creation and on landing.** An asset that stands in Available for days never starts a calendar-due check. Add a Condition transition from Available with the same tests. Because this agent has no continuous variables, the condition must be re-tested, e.g. with a daily cyclic event calling `onChange()` (Help *Transition*) *(suggested; flagged by batch book-2)*.
- **Unlimited capacity.** Every aircraft could be in C check at once. When capacity matters, send the check through a shared ResourcePool or a hangar agent.
- **Usage is booked only by Landing's action.** Any new way out of Flight (diversion, breakdown) must also add the hours.
- **"Just checked" start.** Dates set to `date()` at creation make every new aircraft freshly checked, so the first year shows no C or D checks. For a real fleet, load last-check dates and hours per tail number and discard the warm-up.

## Reusable idea
A multi-level inspection regime as a branch cascade:
- each level is due on calendar age OR usage;
- the cascade is evaluated after each use cycle (and on a periodic tick);
- the heaviest due level wins;
- finishing a level resets it and every lighter level.

This fits aircraft A–D checks, rail-car and bus inspections, and generator minor, intermediate and major overhauls.

## When the co-pilot should use this
- Fleet availability or maintenance-planning ABMs, including power-plant and generator maintenance (`09-course-materials-buk780/INVENTORY.md`).
- A user asks how to combine time-based and usage-based maintenance triggers.
- Related: `bigbook/statechart-guards-branches-and-state-reentry.md`, `basicmodels/maintenance-phase-5.md`, `models/field-service.md`.
