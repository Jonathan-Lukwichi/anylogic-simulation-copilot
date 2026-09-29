# Phase 0 — Framing & approach selection (run this FIRST)

The most important gate. Never suggest blocks before this is done.

## Intake questions
1. What decision/question must the model answer? (e.g. "Will dynamic staffing cut ED wait time?")
2. Unit of analysis? (patients, machines, vehicles, orders...)
3. What drives the behaviour? Use the chooser below.
4. Abstraction level? (high/aggregate vs low/individual)
5. What data exist? (arrival logs, service times, layouts)
6. KPIs? (wait time, utilisation, throughput, cost, service level)

## Sharper framing questions (ask the ones that apply)
- **One-off study or living decision tool?** Will the model settle this decision once, or be re-run
  as conditions change (new forecast, roster, product, site)? If re-run: by whom, how often, with
  what data refresh? A living tool changes the build — levers become top-level parameters, tables
  become input files, KPIs become Outputs, and delivery is usually a Cloud experiment
  (`knowledge/08-example-patterns/videos/cloud-decision-tool-for-stakeholders.md`).
- **"Digital twin" — which kind?** AnyLogic supplies the simulation (what-if) layer and in-model
  dashboards; data ingestion, a live state store, alerting and the end-user app are separate
  systems. Is it offline on a data snapshot, initialised from live state at run start, or
  continuously synced? Through what data interface (Excel/DB snapshot, DB polling, MQTT, API), and
  who consumes the output? Most thesis "twins" are snapshot-initialised what-if models
  (`knowledge/08-example-patterns/videos/pharma-supply-chain-twin-hybrid.md`).
- **Boundary — one interface past the lever.** For every lever, ask where the faster or larger flow
  lands next if the lever works, and whether that place can absorb it. Extend the boundary to that
  interface as a cheap stub (capacity + queue + KPI) and report its KPIs next to the internal ones —
  an internal fix can simply move the bottleneck just outside the model
  (`knowledge/08-example-patterns/videos/boundary-extension-bottleneck-migration.md`).
- **Layout.** If a CAD plan exists and people move through the space, ask for the file, which layers
  hold walls, and one real dimension to check scale (`videos/cad-drawing-to-pedestrian-walls.md`).
  If the question is *where to put things*, say now that the model ranks candidate layouts —
  AnyLogic has no built-in layout optimiser (`videos/layout-candidates-and-design-time-api.md`).
- **Real map.** If sites, depots, customers, a rail yard or a street grid sit on a real map, ask for
  each site's coordinates (latitude/longitude, WGS 84) rather than addresses, whether a shapefile or
  OSM extract of the network exists, and which scale is needed: network-level GIS routes, or
  yard-level Rail / Road Traffic markup converted from the shapefile
  (`knowledge/08-example-patterns/videos/gis-agent-placement-from-table.md`,
  `videos/gis-shapefile-to-rail-markup.md`).
- **Equipment rules** (when material moves on equipment): conveyor type and merge priorities;
  station cycle time, batch vs per-item processing, crew; fleet size, fixed path vs free space, and
  the dispatch rule; crane motion mode, safe height and reach; MTBF/MTTR and who repairs. Record
  crane mode and dispatch rule as realism settings, not free levers, unless the decision is about
  them (`knowledge/08-example-patterns/videos/mhl-*.md`).
- **Which uncertainty does each scenario address?** Run-to-run randomness needs replications;
  uncertainty about an input's *value* (a forecast's error band, a mix share) needs that input
  sampled across iterations (Cloud "Monte Carlo 2nd order", or a sensitivity sweep) with
  replications inside each.
- **Finding the best setting?** Name ONE objective KPI. Limits on the levers themselves (budget,
  headcount) become optimization *Constraints*; limits on simulated results (service level, lost
  customers) become *Requirements*. Must a target hold on average, or nearly always?
- **Markets where supply can run short:** what does a buyer do when their brand is out (wait,
  switch, leave)? Is patience a trait of the person or drawn per episode? Who gets restocked units
  first? State these policies instead of inheriting engine defaults.

## Approach chooser
- **Flow of entities through limited resources, event-ordered** -> Discrete-Event (DES)
- **Many autonomous individuals with their own state/decisions and interactions** -> Agent-Based (ABM)
- **Aggregate stocks, continuous feedback loops, high abstraction** -> System Dynamics (SD)
- **A combination (e.g. DES process inside an agent population)** -> Hybrid / multimethod.
  Typical case: movers with their own behaviour (routes, schedules, breakdowns — a statechart) that
  visit capacity-limited sites. Keep each mover as one persistent agent and host the site's process
  inside the site agent type; hand over with `enter.take(agent)` and hand back from Exit's On exit
  with `send(msg, agent)` (`knowledge/08-example-patterns/videos/statechart-agent-through-hosted-flowchart.md`).
  Don't re-create movers in a Source at every visit, and don't fake a dwell that competes for
  shared resources with a statechart timeout.

**Is simulation-based optimization the right search tool?** If the model must *find* the best
setting, check the technique matrix in `knowledge/07-optimization/README.md` first (LP/MILP vs
sim-opt vs RL vs ML). Default experiment ladder: named scenarios → Parameter Variation with
replications → Optimization with replications → re-verify the shortlist → report "best found" with
a confidence interval.

## Output of Phase 0
A one-paragraph recommendation: chosen approach + justification + abstraction level + the KPIs,
confirmed with the user. Reference: knowledge/00-method-selection (Borshchev & Filippov).
