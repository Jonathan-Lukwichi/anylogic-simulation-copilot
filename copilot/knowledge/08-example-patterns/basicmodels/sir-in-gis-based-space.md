# Pattern card — SIR in GIS Based Space
- **Source:** AnyLogic example model "SIR in GIS Based Space" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM on a GIS map (metapopulation)
- **Problem it solves:** Spread an infection across many cities where people mix only inside their own city and the disease travels between cities with carriers (planes), with cheap per-city and national S/I/R counts.

## Structure
- **Main:** GIS map; `cities` *loaded from a database table* with only two columns — the name (mapped both to the `name` parameter and to the built-in *GIS location name*, so each city is placed by map search) and the population; `people` starts **empty**; `planes` (5). On startup `createPlanes()` parks each plane at a random city (`loc = city; setLocation(city)`). A cyclic event (daily) sends every idle plane to another city: `for (Plane p : filter(planes, x -> x.isIdle)) p.fly(randomWhere(cities, c -> c != p.loc));`.
- **City** (On startup): creates one `Person` per 200 inhabitants with `main.add_people(6, 0.05, this)` (contact rate per week, infectivity, home city) and keeps them in its collection `citizens`; `infection()` sends `"CONTACT"` to a share `percentOfInitialInfected` of distinct citizens. Variables `NSusceptible`, `NInfected`, `NRecovered`.
- **Person statechart (SIRS):** susceptible —message `"CONTACT"`→ infected —timeout `triangular(20, 30, 40)` days→ recovered —timeout `triangular(20, 40, 60)` days→ susceptible. Inside *infected*, a rate transition (`contactRate * infectivity` per week) sends `"CONTACT"` to a random member of `city.citizens`. Each state's entry/exit action does `city.N… ++ / --`, guarded by `city != null`.
- **Plane:** `fly(dest)` takes a random citizen out of the current city (`loc.personDeparting()`: removes it from `citizens`, decrements that city's counter for its state, sets `person.city = null`), then `moveTo(dest)`; *On arrival* `loc.personArrival(person)` adds it to the new city's list and counter. The person agent itself never moves in space — only the plane does.

## Resources
n/a

## Key settings worth copying
- **Mixing by list, not by space:** contacts go to `city.citizens`, so every city is a well-mixed patch and travel is the only coupling. No distance queries, no GIS routing for people.
- **Incremental counters:** state entry/exit actions keep per-city S/I/R counts exact in O(1); the `cities` population's *Statistics* of type **sum** (`agent.NInfected` etc.) give national totals for a time plot (`cities.NInfected()`).
- **Scaled agents:** one agent = 200 people keeps a country-sized model small; population sizes come from the table.
- Collection utilities used: `filter(collection, predicate)`, `randomWhere(collection, predicate)`, `population.random()`; agents created with the generated `add_people(...)` taking the type's parameters in order.

## KPIs instrumented
National S/I/R curves (sum statistics over cities); per-city counts shown on the map.

## Pitfalls
- **Traveller's city is never set again (read from the model code, not run):** `personDeparting()` sets `person.city = null`, and `personArrival()` does not assign the new city. The traveller's later state changes then update no city counter, and its contact action reads `city.citizens` with no null guard. Add `person.city = this;` in `personArrival` (and guard the contact action) before reusing this pattern.
- **One traveller per flight** and five planes make coupling tiny and fixed; parameterise passengers per flight from travel data.
- **Scaled agents coarsen the dynamics:** infectivity and contact rate act per agent (200 people), small cities hold few agents, and early extinction is common. Replicate and report ranges.
- It is SIRS despite the name (immunity wanes after 20–60 days).
- Placement by city name takes the first map-search hit at every start (G51); for real studies store coordinates in the table (`videos/gis-agent-placement-from-table.md`).
- `randomWhere(...)` returns null when nothing matches (e.g. a one-city test); guard it.

## Reusable idea
Metapopulation in AnyLogic: patches as agents that own a list of members and running counters; people change patch only through carriers; aggregate with population sum statistics. It scales to many regions without spatial contact searches.

## When the co-pilot should use this
Infection import through travel, regional epidemic comparisons, patient transfers between hospitals, or any patch-structured ABM (farms, schools, prisons) where mixing is local and movement is by discrete trips. Single-city SIR on networks or a grid: `models/sir-agent-based-calibration.md`; placing sites from a table: `videos/gis-agent-placement-from-table.md`.
