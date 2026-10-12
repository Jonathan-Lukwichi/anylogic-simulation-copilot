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
- **Who decides, and does demand have a memory?** Who makes the decisions we model — individuals,
  households, firms, crews? Does each item that raises requests (machine, patient, customer) have its
  own history that drives the next request? If so it is an agent, not a Source.
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
- **Rail:** which track sections, merges and crossings may hold only one train, and what is the
  signalling rule? The Rail Library detects collisions but does not prevent them (G99), so the
  interlocking policy belongs in the conceptual model and the assumptions list
  (`knowledge/08-example-patterns/bigbook/rail-traffic-control-block-locking-and-lookahead.md`).
- **Durations and pauses.** Do durations matter as a spread — is a stay fixed, narrow or highly
  variable? Can work be paused, and does a pause keep the progress made (G75)?
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
- **Behaviour under strain, and decisions on estimates.** When the system is congested or performs
  badly, does anyone change behaviour — leave, give up, order less, quit? If so the model must close
  that loop or document why not. If people decide on forecasts or estimates (R&D funding, project
  kill, maintenance deferral, supplier approval), how good are those estimates? The model then holds
  a true and an estimated value per item, policies read the estimate and KPIs score the truth
  (`knowledge/08-example-patterns/models/product-portfolio-management.md`).
- **Data start date and per-period probabilities.** Which date does the data start on? It becomes the
  model's start date (G65). If a behavioural input comes as per-period probabilities (by age, month or
  inspection), record the choice: a periodic trial (tick transition + Branch) when risk changes during
  the run, or conversion to a time-to-event distribution when the tables are fixed
  (`knowledge/08-example-patterns/bigbook/synchronous-tick-transition-from-probability-table.md`).

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

**Six checks before recommending** (card `knowledge/08-example-patterns/bigbook/method-choice-abstraction-feedback-and-agent-unit.md`):
1. Draw the abstraction line first: what may stay below it (movement and contact, individual
   identity and history, single events)? The method follows from that.
2. Does any output feed back into the inputs (walk-aways, give-ups, demand reacting to service,
   overtime driving attrition)? The model must close that loop or say why not.
3. Does the shape of time-in-state matter? Plain SD stocks imply exponential residence.
4. Which unit decides — a person, a household, a firm, a crew? That unit is the agent.
5. Does each demand source have its own state and history driving its next request? Then agents,
   not a Source.
6. Which structural assumptions (network type, duration spread) could change the regime? Plan to
   sweep them.

Hybrid wiring, direction by direction (which construct and when each side is re-evaluated):
`knowledge/08-example-patterns/bigbookmodels/multimethod-interface-catalogue.md`. Discrete events
change stocks by jumps, never by estimating a rate; an SD-driven arrival stream uses *Interarrival
time*, not *Arrival rate* (G5). Grid models come in two engines: **synchronous steps** when every
cell re-decides each generation (Game of Life, Schelling), **event-driven cells** (a statechart per
cell, messages to neighbours, timeouts for durations) when activity is sparse, like a fire front —
run time then follows activity, not grid size
(`knowledge/08-example-patterns/bigbookmodels/wildfire-with-wind.md`).

**Is simulation-based optimization the right search tool?** If the model must *find* the best
setting, check the technique matrix in `knowledge/07-optimization/README.md` first (LP/MILP vs
sim-opt vs RL vs ML). Default experiment ladder: named scenarios → Parameter Variation with
replications → Optimization with replications → re-verify the shortlist → report "best found" with
a confidence interval.

## Output of Phase 0
A one-paragraph recommendation: chosen approach + justification + abstraction level + the KPIs,
confirmed with the user. Reference: knowledge/00-method-selection (Borshchev & Filippov).
