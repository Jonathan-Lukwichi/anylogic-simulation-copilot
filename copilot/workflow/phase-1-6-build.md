# Phases 1-6 — the build (after Phase 0 is confirmed)

1. **Decompose** — entities, resources, activities, routing logic.
2. **Characterise data** — name each distribution; separate *given* from *fit-from-data*.
3. **Map to constructs**

   | Real-world concept | AnyLogic construct |
   |---|---|
   | Arrival | Source (interarrival distribution) |
   | Limited-capacity processing | Service, or Queue + Seize + Delay + Release |
   | Hold / wait | Delay |
   | Assemble N into 1 | Combine / Batch |
   | Decision / branch | SelectOutput |
   | Exit | Sink |
   | Movement | Conveyor / path |
   | Shared limited staff/equipment | ResourcePool |
   | Interval measurement | TimeMeasureStart / TimeMeasureEnd |

4. **Configure environment** — model time units, runtime window, fixed seed, scaling.
5. **Animate & instrument** — displays, indicators, live KPI counters/plots.
6. **Verify & extract** — run, sanity-check against theory (e.g. Little's Law), read off KPIs.
