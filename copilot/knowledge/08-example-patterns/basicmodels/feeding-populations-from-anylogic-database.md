# Pattern card — Feeding Populations From AnyLogic Database
- **Source:** AnyLogic example model "Feeding Populations From AnyLogic Database" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (data-driven structure)
- **Problem it solves:** Build a two-level agent hierarchy (companies that each own a fleet) straight from two linked database tables, with no start-up code.

## Structure
- **Tables.** `distributors` (unique `name`, `type`) and `trucks` (`distributor`, `truck_type`, `fleet_size`). `trucks.distributor` is a **foreign key** to `distributors.name`. The `type` and `truck_type` columns are typed with the model's Option lists (`DistributorType`: LOCAL/REGIONAL; `TruckType`: LIGHT/HEAVY), so they map straight onto option-list parameters.
- **Level 1.** Main's population `distributors` is *Loaded from database*: table `distributors`, **one agent per record**, parameters `name` and `type` mapped to columns.
- **Level 2.** Inside the `Distributor` type, population `truckFleet` is also *Loaded from database*: table `trucks`, fetch condition `distributor` **equals `name`** — the owning distributor's own parameter — and mode **multiple agents per record** with the quantity in `fleet_size`; `truckType` mapped from `truck_type`. Each distributor therefore receives only its own trucks, e.g. one with 21 light + 5 heavy.
- Presentation: each truck shows one of two 3D shapes chosen by `truckType`.

## Resources
n/a

## Key settings worth copying
- Population properties (Help 8.9.10, *Agent population*): *Population is: Loaded from database*, *Table*, fetch conditions, *Mode* = one agent per record / multiple agents per record, *Quantity is contained in column*.
- The condition's value is an expression evaluated in the **owning agent** — a parameter of the parent (`name`) is what makes the child query per-parent.
- Declare the link as a foreign key in the table editor (Help *Creating a table → Foreign key*); here updates cascade and deletes set the child's key to null.

## KPIs instrumented
n/a (structure demo). Useful checks: `truckFleet.size()` per distributor, `count(truckFleet, t -> t.truckType == HEAVY)`.

## Pitfalls
- **The key must be a mapped parameter.** It works because a parent's parameters are set when it is created, before its embedded populations are loaded. A key computed in the parent's *On startup* comes too late — On startup runs from the innermost agents upwards (G46), so the child query would see the default value.
- **Mismatches fail silently.** A key typo, trailing space or case difference gives a parent with an empty fleet, not an error; the foreign key blocks orphans in the database but not childless parents. Assert at start-up that every parent has children and that the loaded count equals the table's sum of quantities.
- Multiple-agents-per-record clones identical agents; if trucks need individual attributes (age, capacity), use one row per truck or set them afterwards.

## Reusable idea
Model the master–detail structure of the real system as linked tables and let populations load themselves: parent table → top population, child table filtered by a parent parameter → embedded population, a quantity column for counts. Changing a fleet is then a data edit, not a model edit.

## When the co-pilot should use this
Distribution networks with depots and fleets, hospitals with wards and beds, factories with lines and machines — any model whose layout of owned assets comes from spreadsheets. Related: `create-trains-from-database.md` (same pattern building rail consists), `getting-values-from-anylogic-database.md`, `feeding-a-collection-from-access-database.md` (external databases).
