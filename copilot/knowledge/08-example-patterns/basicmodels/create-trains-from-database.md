# Pattern card — Create Trains from Database
- **Source:** AnyLogic example model "Create Trains from Database" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Rail Library, data-driven)
- **Problem it solves:** Generate each arriving train with its exact consist (how many cars of each type) and timetable taken from database tables, instead of a fixed car count and a `carindex` formula.

## Block chain
`TrainSource` → `TrainMoveTo` (target: a point on track) → `TrainDispose` (its *On enter* ends the run after the third train).
- **Tables.** `t_trains` (`id`, `arrival_date` timestamp) and `t_railcars` (`train_id`, `car_type` — an Option list `CarType` —, `qty`).
- **TrainSource.** *Arrivals defined by: Arrival table in Database* on `t_trains` with the timestamp column; the custom train type `Train` gets `id` and `arrivalDate` from the row.
- **The consist is pre-built inside the train.** `Train` holds an embedded population `railCars` *Loaded from database*: table `t_railcars`, condition `train_id` equals the train's `id`, multiple agents per record, quantity column `qty`, `carType` mapped from `car_type`.
- **Hand-over to TrainSource.** *Number of cars* = 1 + the sum of `qty` for this train (a query); *New rail car* = a new locomotive for `carindex == 0`, otherwise `train.railCars.get(carindex - 1)` — the already-created car agents are passed in one by one; *Add cars to custom population* = `car.getPopulation()` for those cars (they stay where they were loaded) and `getDefaultPopulation()` for the locomotive.
- *On exit* of TrainSource appends to an arrival log and crosses the train off a schedule text (a query of its `arrival_date`); a clock text shows `getHourOfDay()` / `getMinute()` / `getSecond()`.

## Resources
n/a (one track, no signalling)

## Key settings worth copying
- TrainSource (Help 8.9.10): *Arrival table in Database* generates one train per record at its timestamp; *Set agent parameters from DB* fills the train's parameters; *Number of cars* must be at least 1.
- Car agent type with an option-list parameter (`carType`) and one 3D figure per type shown by a *Visible* test — the per-car-type look comes from data.
- The nested load itself is the same pattern as `feeding-populations-from-anylogic-database.md`.

## KPIs instrumented
Arrival log and timetable text only. Add per-train dwell or transit time with a TimeMeasureStart/End pair if needed.

## Pitfalls
- **Two sources of truth.** The car count comes from a query, the cars from the population. If they ever disagree (filter change, NULL quantity), `get(carindex - 1)` throws or cars are left unused. Safer *(suggested)*: *Number of cars* = `1 + train.railCars.size()`.
- **Car order follows the population order** (the table rows here). Add a position column and load or sort by it if the order in the consist matters (hump sorting, coupling).
- Hard-coded end condition (`in.count() == 3`): tie it to the table's row count, or let the run stop at the stop time.
- The whole train must fit on the track at the entry point (G29); longer consists from data may need a new entry offset.

## Reusable idea
Pre-build variable composite objects as agent populations loaded from a child table, then feed them to the library block that assembles them. The same trick works wherever a block asks "give me the next element": rail cars now, pallet loads or batch contents elsewhere.

## When the co-pilot should use this
Rail yards and terminals with timetabled trains of mixed car types from an operator's schedule; any arrival process where each arrival's composition is data. Related: `bigbook/rail-car-types-callbacks-and-yard-statistics.md` (`carindex`, car types, car setup).
