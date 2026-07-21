# Pattern card — Areas with Restrictions for Pedestrians
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Pedestrian Library)
- **Problem it solves:** Controlling pedestrian access to zones at runtime — both by occupancy cap and by toggling locked/unlocked states for emergency exits.

## Block chain
Two agent populations share the same space: **Client** agents and **Staff** agents, each with their own flow.

Client flow: PedSource → PedGoTo (table/zone) → PedWait (dine; `uniform(30, 90)` seconds) → PedGoTo (exit) → PedSink

Staff flow: PedSource → PedWait (station) → PedGoTo (work area) → PedSink

Areas with restrictions (AreaNodeDescriptor) gate entry into zones. Each restricted area carries an `accessRestrictionType` and a `capacity` parameter. Emergency exit areas start **closed** (`emergencyExit1/2/3.close()` in startup code) and are flipped open programmatically (`emergencyExit1/2/3.open()`) when an alarm event fires. The restaurant seating area uses a capacity restriction so no more than N clients occupy it simultaneously.

## Resources
- No ResourcePool blocks. Capacity constraint is enforced by the pedestrian area's built-in `capacity` setting, not a separate resource pool.
- Three named emergency-exit area nodes (`emergencyExit1`, `emergencyExit2`, `emergencyExit3`).

## Key settings worth copying
- **Client dwell time:** `uniform(30, 90)` seconds at the table (PedWait block)
- **Time unit:** Second
- **Area capacity:** integer cap set on the AreaNodeDescriptor — pedestrians queue outside until a slot is free
- **Emergency exit toggle:** call `.close()` at startup; call `.open()` inside an event/button action to redirect pedestrian routes at runtime
- **Arrival rate:** driven by a `rate` parameter on each PedSource (two sources: one for clients, one for staff)

## KPIs instrumented
- Visual occupancy of the restricted dining zone (pedestrians visible on the 2-D map)
- No explicit chart-based KPIs in this basic illustration; the observable output is pedestrian routing behaviour before and after the emergency trigger

## Reusable idea
Use pedestrian **area restrictions** as runtime switches: set capacity to cap simultaneous occupancy of any zone (ticket gate, lounge, clean room), and call `.open()` / `.close()` on named exit areas from event code to dynamically reroute crowds during drills, alarms, or policy changes — no extra logic blocks needed.
