# Pattern card — Defining a Work Schedule for Resources
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Modelling realistic shift patterns so that resource pools shrink, grow, or go fully offline according to a clock-driven schedule rather than staying at fixed capacity throughout the simulation.

## Block chain
Two independent flowcharts run side-by-side, each consisting of Source → Service → Sink. Both flowcharts share the same basic structure but are driven by different ResourcePool scheduling modes:

1. **Integer-valued schedule mode** — A Schedule object whose value type is set to *integer* is attached to the ResourcePool's `capacitySchedule` field. The schedule explicitly lists time intervals and the exact headcount available in each interval (e.g., 3 resources from 08:00–12:00, 1 resource from 12:00–13:00, 3 again from 13:00–17:00, 0 overnight). The pool continuously adjusts its live capacity to match whatever value the schedule returns at the current simulation time.

2. **On/Off schedule mode** — A second Schedule object with value type *on/off* is attached to `capacityScheduleOnOff`. A fixed maximum capacity is declared on the ResourcePool; the schedule simply toggles the entire pool between fully available and completely unavailable. When the schedule reads "off", all resources disappear; when it reads "on", the full complement returns.

In both cases, entities arrive via a Source driven by an inter-arrival time expression. A Service block seizes one resource unit, holds the entity for a `triangular(0.5, 1, 1.5)` hour service time, releases the unit, and passes the entity to Sink.

## Resources
- Two ResourcePool blocks, one per flowchart
- Pool 1: capacity varies by integer schedule (multiple discrete levels across the day)
- Pool 2: fixed total capacity toggled on/off by a boolean schedule

## Key settings worth copying
- **Model time unit:** Hour — aligns naturally with shift-based schedules
- **Service time distribution:** `triangular(0.5, 1, 1.5)` hours (min, mode, max)
- **Schedule value types:** `integer` for fine-grained headcount control; `on/off` for binary shift blocks
- **ResourcePool field:** `capacitySchedule` (integer mode) or `capacityScheduleOnOff` (on/off mode) — only one is active per pool
- **Arrival:** inter-arrival time expression on Source (constant or distribution-based)

## KPIs instrumented
- Implicit queue build-up during off-shift periods (entities queue at Service when pool capacity drops to zero)
- Resource utilisation visible through standard ResourcePool statistics
- Throughput observable via Sink's `count()` statistic

## Reusable idea
Attach a named Schedule object directly to a ResourcePool's capacity field instead of hard-coding headcount — this single change makes any resource pool shift-aware without touching flowchart logic, and you can swap between granular integer schedules (for partial staffing) and simple on/off schedules (for full-shift blocks) by pointing to a different schedule object.
