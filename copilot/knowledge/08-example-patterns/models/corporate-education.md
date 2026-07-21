# Pattern card — Corporate Education
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Model with GIS)
- **Problem it solves:** Determine the optimal number and placement of internal trainers across regional branches so that employees stay certified under high turnover, while minimising trainer travel.

## Block chain
Employees and trainers are individual agents placed on a GIS map at their assigned branch. Each employee carries a personal training plan (sequence of required courses loaded from a database). A statechart drives employee lifecycle: the agent waits until a course is due, fires a `RequestTraining` call to the branch, joins a queue for that course, waits until a trainer with the matching competence is available and a minimum group size is reached (configurable 2–30), attends the session, then returns to normal work. Trainers likewise have a two-state statechart (Available / Busy) and travel to the hosting branch when assigned a session. Employee turnover is modelled by drawing a work-tenure from an exponential distribution parameterised by an annual turnover percentage read from the database; when tenure expires the agent leaves and a replacement is hired, resetting the training clock. The entire scenario—branch locations, employee counts by type, trainer counts and competences, course curricula—is read from an embedded database at startup, making the model a live demonstration of DB-driven parameterisation.

## Resources
- **Trainers:** typed agents (e.g., compliance trainer, technical trainer); count and home branch read from `number_of_trainers` DB table
- **Branch capacity:** implicit — each branch has an `AvailableTrainers` list and per-course `QueueForCourse` objects
- **Group policy:** `MinimumGroupSize` (default 6) and `MaximumGroupSize` (default 30) control when a session fires

## Key settings worth copying
- **Turnover-driven tenure:** `exponential(turnover/100.0) * WorkDaysPerYear` — converts an annual percentage into a random working-days horizon; swap the rate for any attrition scenario
- **Time unit:** Day
- **Minimum group threshold:** waiting until `MinimumGroupSize` agents are queued before starting a course; prevents running near-empty classes
- **DB-parameterised setup:** all branch coordinates, employee types, trainer types, and course plans loaded via table queries at model init — no hard-coded constants
- **GIS layer:** branch icons on an OpenStreetMap tile layer; zoom reveals individual employee/trainer agents

## KPIs instrumented
- Fraction of employees fully trained (all courses current)
- Fraction with training overdue
- Trainer travel distance / travel burden (as a function of trainer placement)
- Queue length per course at each branch over time

## Reusable idea
Use an exponential distribution on an annual-percentage turnover rate to generate realistic individual tenure durations, then reset the agent's training plan on replacement — this cleanly models workforce churn without any aggregate equation, and scales naturally to heterogeneous employee types each with their own turnover rate from a database column.
