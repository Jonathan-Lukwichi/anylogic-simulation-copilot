# 04-manufacturing-warehouse

Manufacturing & warehouse DES. Job-shop tutorial, Cloud examples.

- **OEE:** definitions are standard lean/TPM material (course copies are not in this repo — see
  `../PRIVATE-MATERIALS.md`); AnyLogic instrumentation and traps (performance = 100 % by construction, `utilization()` ≠
  OEE, line vs machine OEE) in `../08-example-patterns/videos/oee-instrumentation-in-des.md` and
  gotcha G41. At intake, ask for nameplate cycle times and planned production time.
- **Sequencing rules (FCFS / EDD / least slack / critical ratio) as an experiment lever:**
  `../08-example-patterns/videos/dispatching-rule-as-optimizable-policy.md` (and gotcha G15).
- **Repeated stations or lines:** custom flowchart blocks — `videos/custom-flowchart-block-from-repeated-chain.md`.
- **Material Handling Library vs PML for movement:** use the MHL whenever the KPI depends on physical
  interaction (belt space, accumulation, merges, vehicles queuing or giving way, crane reach, lift
  contention); plain Delay/MoveTo only when a move is just elapsed time. The PML `Conveyor` block is
  deprecated since 8.9.5. Cards: `../08-example-patterns/videos/mhl-*.md` (Convey routing and
  offsets, conveyor types / spurs / merge priority / transfer elements, stations and re-assembly,
  sensors and breakdowns, AGV dispatch, crane reach and movement mode); traps G42–G45.
- **Multi-floor facilities, lifts, AGVs:** `videos/multi-level-facility-lift-landings.md`; ramps and
  spirals: `videos/spiral-conveyor-per-point-z.md`.

See SOURCES.md for the exact links and download/fetch-live status.
