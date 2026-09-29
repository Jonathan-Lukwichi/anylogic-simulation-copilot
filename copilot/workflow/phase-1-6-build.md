# Phases 1-6 — the build (after Phase 0 is confirmed)

1. **Decompose** — entities, resources, activities, routing logic.
   If the system spans more than one AnyLogic library (Pedestrian, Road Traffic, Rail, Material
   Handling, PML), **list every hand-off between libraries** — they do not sense each other (gotcha
   G27). Two mechanisms cover most cases: an agent *changes library* through exit/enter blocks
   (e.g. PedExit → Queue → Pickup … Dropoff → PedEnter), or an *event in one library gates agents in
   another* through a callback (Traffic Light *On phase change* → `area.setOpen(...)`; vehicle
   arrival → `waitBlock.freeAll()`).
2. **Characterise data** — name each distribution; separate *given* from *fit-from-data*. If no
   family passes a goodness-of-fit test, or the data are categorical or banded, use an empirical
   Custom Distribution and say that it cannot produce values beyond the observed range
   (`knowledge/02-statistics-input-modeling/README.md`).
3. **Map to constructs**

   | Real-world concept | AnyLogic construct |
   |---|---|
   | Arrival | Source (interarrival distribution) |
   | Limited-capacity processing | Service, or Queue + Seize + Delay + Release |
   | Timed hold (known or sampled duration) | Delay |
   | Hold until something else releases it | **Wait** + `free(agent)` / `freeAll()` (or Delay "until stopDelay()") — gotcha G7 |
   | Close/open the flow for everyone | Hold (a gate) |
   | Assemble N into 1 | Combine / Batch |
   | Decision / branch | SelectOutput |
   | Exit | Sink |
   | Movement that is just elapsed travel time (no interaction) | Delay / MoveTo on a path |
   | Movement where physical interaction drives the KPI (belt space, merges, vehicles queuing or giving way, crane reach, lifts) | **Material Handling Library** — see the Beyond-PML table (the PML `Conveyor` block is deprecated and off the palette since 8.9.5; it treats items as zero-size) |
   | Shared limited staff/equipment | ResourcePool |
   | Interval measurement | TimeMeasureStart / TimeMeasureEnd (one End may reference several Starts) |
   | An existing agent (population / statechart) passes through a process | Enter + `enter.take(agent)`; leaves via **Exit** (not Sink), whose On exit can `send()` it a message — card `videos/statechart-agent-through-hosted-flowchart` |
   | Custom routing across agents (shortest queue, nearest site) | Exit → `target.enter.take(agent)` |
   | Same block chain repeated per zone/station/line | Custom flowchart block — refactor once the logic is verified; per-agent parameters must be **Dynamic** (G35) |
   | Per-agent raw KPI export | Database → Log model execution (Simulation experiment only, G19) or Export tables at the end of model execution |
   | Per-run result rows for Excel / Cloud | Results table in the model database: `deleteFrom(...)` then `insertInto(...)` from Main (G46, G47) + *Export tables at the end of model execution* — card `videos/excel-round-trip-results-and-cloud` |
   | Count adoptions / churn / infections | Counter in the target state's Entry action; per-agent flag for distinct reach (G59) |
   | Word-of-mouth conversion | Sender rate c + receiver guard `randomTrue(i)`, or sender rate c·i + no guard — never both (G58); target `randomFrom(population)`, not `sendToRandom()` (G57) |
   | Agents wait for a stock or capacity another agent holds | Owner-side allocation: ordered waiting list + a serve function that reserves a unit and calls `onChange()` on the buyer (G56, G60) |

   **Beyond PML** (library-specific constructs, built by hand in AnyLogic):

   | Real-world concept | AnyLogic construct |
   |---|---|
   | Walkers wait for an event (vehicle arrival, signal) | PedWait released by `free()` / `freeAll()` |
   | Walkers ride a vehicle | PedExit → Queue → Pickup (in the vehicle's flow) … Dropoff → PedEnter |
   | Signal-controlled pedestrian access | Pedestrian area/node opened and closed with `setOpen()` from a controller callback |
   | Vehicle shuttles back and forth on one track | One TrainMoveTo per change of direction; return leg Direction = Backward (G28) |
   | Movement between floors | Lift landings (main landing holds the settings, G25) or paired network ports for path-guided transporters and conveyor items; level gates for free-space transporters; PedChangeLevel / Elevator for pedestrians |
   | Ramp or spiral (conveyor, road, track) | Per-point Z values in the markup's Points table — card `videos/spiral-conveyor-per-point-z` |
   | Goods on a belt with accumulation, merges or singulation | Conveyor markup (roller / belt / cell type; gap; merge priorities — higher wins) + `ConveyorEnter` / `Convey` |
   | Timed operation on the line (machine, operator) | **Station** markup (capacity, processing mode, resources) — no Delay block |
   | Sensor, stop or escapement on the line | Position on conveyor: edge callbacks, `block()` / `unblock()` |
   | N parts become 1 product on the line | `Convey` (Leave conveyor on exit, G42) → `Batch` → `ConveyorEnter` downstream |
   | 90° divert keeping orientation vs turning the item | Transfer table vs turntable / turn station |
   | Vehicles that queue, give way or collide | `TransporterFleet` (path-guided or free-space) + `SeizeTransporter` / `MoveByTransporter`; set the dispatch policy explicitly (G44) |
   | Lifting by crane | `MoveByCrane` (safe height, component movement mode; reach and crane height, G45) |
   | Equipment breakdown (8.9) | `Downtime` block attached to the MHL markup, or `fail()` / `repair()` — not `stop()` (G43) |
   | Sites at real locations | Population loaded from a table with columns mapped to *GIS location latitude / longitude* — not place names (G51) |
   | An existing rail yard or street grid | GIS shapefile → *Convert Shapefile to Space Markup*, then curate the topology (G52) |

4. **Configure environment** — model time units (set them before drawing statecharts, events or
   charts — new timed elements take the unit in force when they are created, G2), runtime window,
   scaling (decide the Scale before
   drawing markup — G26). Randomness: **fixed seed** while building, verifying and demoing; random seed
   (or per-replication seeds) for any estimate (G16, G17).
5. **Animate & instrument** — displays, indicators, live KPI counters/plots.
   - [ ] Every block that holds agents for non-zero time has an agent location (Service needs both
     its queue and its delay location); queue paths run tail → server (G30).
   - [ ] 3D: one vertical datum; floor rectangles with Z-Height 0 (or Z = −t, Z-Height = t); lights
     either none or a complete set (G31, G32). Multi-level: level Z and lift Floor elevation come
     from the same heights (G25).
   - [ ] Colour carries information: 2D fills, or `shape.setColor("<material>", color)` in 3D (G33).
   - [ ] Scenario changes that remove capacity are visible in the drawing too (G34).
   - [ ] Custom blocks show `in.count()` / `out.count()` and open on click (`return true;`, G36).
   - [ ] Each lever sits where the model reads it: inputs read while the model is built (population
     size, layout id, which table to load) are pre-run controls or Cloud inputs (G50); only runtime
     policy levers get live controls on Main, and those call `onChange()` for Rate/Condition
     triggers (G56).
   - [ ] Agent types: only the agent's own body is *Visible on upper agent* — notes, screenshots,
     charts and controls inside agent types are unticked (G54).
6. **Verify & extract** — run, sanity-check against theory (e.g. Little's Law), check conservation
   (`source.count()` = exits + WIP — G37), read off KPIs. **Never report a KPI from a single
   fixed-seed run**; use replications and give a confidence interval.
   *If the deliverable runs on AnyLogic Cloud:* every decision KPI is a scalar `Output` on the
   top-level agent (nested KPIs surfaced by expression, G39); scenario comparisons use a replicated
   experiment type; outputs come from **Run**, not from watching the animation (G40); check the
   account tier (run time, memory, API) before promising delivery — card
   `videos/cloud-run-semantics-and-access`. Put every set-up step in the top-level agent's On startup
   (Cloud skips the experiment's set-up code, G49); table inputs need *Autoupdate imported tables on
   model startup*, and each run should show what it read (G48).
   *Agent-based face checks:* state counts sum to the population and users = initial + adoptions −
   exits (G59); a word-of-mouth model's mean curve tracks the SD Bass curve with the same p and
   q = contact rate × adoption fraction; exits of a state left by competing timeouts split as their
   race probability predicts (G55); every rare-path transition (give up, switch, stock-out) has a
   counter; no state has two transitions that can fire at the same instant without an explicit
   choice rule (G60).
