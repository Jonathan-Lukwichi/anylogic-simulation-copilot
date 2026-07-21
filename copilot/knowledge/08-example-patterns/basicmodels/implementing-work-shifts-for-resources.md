# Pattern card — Implementing Work Shifts for Resources
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model resource availability that follows a daily shift timetable so that staffing levels and arrival rates both vary realistically throughout the day.

## Block chain
Agents enter through a **Source** whose arrival rate is driven by a time-varying schedule (`rateSchedule`). They flow into a single **Service** block that seizes workers from a **ResourcePool** for a service duration drawn from `uniform(20, 40)` minutes. Finished agents exit through a **Sink**.

## Resources
One **ResourcePool** with capacity controlled by a named schedule (`schedule`). The schedule defines three working periods: 4 resources are active from 08:00–13:00, zero resources during the 13:00–14:00 lunch break, and 4 resources again from 14:00–18:00. Outside working hours capacity drops to zero, causing agents to queue until the next shift window opens.

## Key settings worth copying
- **Model time unit:** Hour
- **ResourcePool capacity binding:** `capacitySchedule = schedule` — capacity is read directly from a Schedule object rather than a fixed integer
- **Service time distribution:** `uniform(20, 40)` (minutes, within an hourly model)
- **Arrival rate binding:** Source `rateSchedule = rateSchedule` — a second Schedule object controls the inter-arrival rate so demand peaks can be synchronised with staffing peaks
- **Shift timetable structure:** define one Schedule with day-of-week rows and hourly columns; set the numeric value to the headcount for each interval

## KPIs instrumented
Queue length and wait time in the Service block (built-in statistics); resource utilisation tracked by the ResourcePool during active shift hours only.

## Reusable idea
Binding both the **resource pool capacity** and the **source arrival rate** to separate AnyLogic Schedule objects lets you encode realistic shift patterns and demand curves declaratively — no conditional logic or event-based capacity changes needed. Swap the schedule values to model night shifts, weekend rosters, or seasonal staffing without touching the process flow.
