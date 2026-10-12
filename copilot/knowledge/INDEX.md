# Knowledge INDEX — the single grounding router

**Start here.** This is the one entry point the co-pilot uses to route any task to
ground truth. Do not reconstruct routing from memory; look it up here, open the named
files, and **cite the specific file**. Never invent block names, settings, or numbers.

> **GROUNDING RULE (single source of truth):** when a task touches modelling approach,
> statistics / input distributions, supply chain, manufacturing, healthcare, optimization,
> the AI/ML-RL layer, or a worked AnyLogic pattern — consult the matching row below FIRST.
> Prefer these sources over guessing. For version-specific AnyLogic block fields and API, check
> the **offline Help of the installed AnyLogic** (below) first, then anylogic.help (see
> SOURCES.md) — never rely on memory, and name the version you cite.

## Task → where to look

| If the task is about… | Go to | Notes |
|---|---|---|
| **Choosing the modelling approach** (DES / ABM / SD / hybrid — Phase 0) | `00-method-selection/` | Borshchev & Filippov is the approach-choice authority (see `../SOURCES.md`). Always settle this before blocks. Six pre-checks (abstraction line, feedback, residence-time shape, deciding unit): `08-example-patterns/bigbook/method-choice-abstraction-feedback-and-agent-unit.md`. Hybrid wiring: `videos/statechart-agent-through-hosted-flowchart.md` and the per-direction catalogue `bigbookmodels/multimethod-interface-catalogue.md`. |
| **Framing the decision** (boundary, living tool vs one-off study, digital-twin kind, layout and equipment questions) | `../workflow/phase-0-framing.md` | Boundary "one interface past the lever"; twin = which layer / sync mode; layouts are ranked, not optimised. |
| **AnyLogic blocks, PLE limits, RL/Alpyne APIs** | offline Help (below) → else anylogic.help; `01-anylogic-core/README.md` | Version-specific; never freeze. See SOURCES.md. |
| **A symptom, error message or "it behaves oddly"** | `01-anylogic-core/anylogic-gotchas.md` — **quick-lookup table at the top** | G1–G122: symptom → cause → fix → why, checked against the 8.9.10 Help and engine. G122 lists Help names that do not compile. Then `anylogic-debug`. |
| **AnyLogic build/debug idioms** (DES, ABM, SD, 2D/3D, libraries, debugging) | `../../.claude/skills/anylogic-*.md` | Battle-tested skills; the debug skill self-updates with each new root cause. |
| **Statistics / input distributions / goodness-of-fit / interpreting results** | `../../.claude/skills/stats-analyst.md` + `02-statistics-input-modeling/README.md` (fitted vs empirical rule) + NIST e-Handbook (see SOURCES.md) | Fit properly (scipy.stats / fitdistrplus) + report KS/AD. Don't eyeball. Empirical forms can't exceed the observed range. Results interpretation in plain English → the skill. |
| **Randomness, seeds, replications, distributions** | gotchas G16–G17, G65–G67 + `08-example-patterns/videos/rng-seed-control-and-custom-generator.md`; argument orders: `bigbookmodels/probability-distributions.md` (G3, G55, G66) | Fixed seed for building; replications for estimates. Small-n CIs: compute the t value yourself (G67). |
| **Supply chain, inventory policy, network/distribution** | `../../.claude/skills/supply-chain-analyst.md` + `03-supply-chain/README.md` + Ivanov book (see SOURCES.md) | Simchi-Levi et al. is the textbook anchor — supply your own copy (see PRIVATE-MATERIALS.md). Pharma twin card in `08-.../videos/`. Domain interpretation of results → the skill. |
| **Manufacturing / warehouse / lean / job-shop / OEE / material handling** | `04-manufacturing-warehouse/README.md` + AnyLogic job-shop tutorial (fetch live) | Pair with pattern cards (job-shop, distribution-center); OEE, dispatching-rule and `mhl-*` cards in `08-.../videos/`. |
| **Healthcare / ED / patient flow** | `05-healthcare/` | DES-in-ED systematic reviews; efficiency-metric framing. |
| **AI / ML / RL integration to show efficiency** | `06-ai-ml-integration/README.md` + `templates/rl-pipeline/` | Always frame baseline vs ML-informed vs RL on the SAME KPIs. Alpyne, Cloud API or Pypeline — see the README's route choice. |
| **Optimization and calibration experiments / OptQuest / Genetic / sim-opt design** | `07-optimization/README.md` (technique matrix, setup essentials, experiment ladder) → sim-opt cards in `08-.../videos/`; `bigbook/optquest-conditional-lever-constraint-and-small-grids.md`; calibration: `bigbookmodels/epidemic-model-various-experiments.md` | Constraint vs Requirement, replications and lucky optima, many-lever tactics, engine limits (G8–G15), non-identifiable pairs (G69), custom experiments (G118, Professional only). |
| **Delivering on AnyLogic Cloud** (stakeholder tool, run semantics, API) | `01-anylogic-core/README.md` (Cloud bullet) → `08-.../videos/cloud-*.md` | Run Configuration rules, Play vs Run, stored results (G38–G40). |
| **Space markup: levels, lifts, rail, pedestrians, road traffic, CAD, 3D, animation** | `08-example-patterns/videos/` (multi-level, rail shuttle, crossing, CAD walls, shapefile → rail markup, spiral conveyor, 3D scene, animation binding); rail: `bigbook/rail-*.md`; presentation and controls: `bigbook/animation-*`, `click-handling-*`, `controls-*`, `3d-shape-*`, `replicated-shapes-*` | Traps G25–G34, G52, G54; rail G98–G100; road and pedestrians G101–G108; controls and shapes G112–G114. |
| **Real geography** (sites on a GIS map, routes, networks from shapefiles) | `08-example-patterns/videos/gis-agent-placement-from-table.md`, `videos/gis-shapefile-to-rail-markup.md`; examples `models/shape-file-example.md`, `models/corporate-education.md` | Store coordinates, not place names (G51); a converted network is geometry to curate (G52). |
| **Excel / database input and output, Cloud files** | reading: `08-example-patterns/basicmodels/getting-values-from-anylogic-database.md` (+ *AnyLogic in 3 Days*, database chapter); writing and Cloud files: `videos/excel-round-trip-results-and-cloud.md`; route choice by data shape: `01-anylogic-core/README.md` (data I/O table) | Autoupdate on startup, purge then write, startup order (G46–G49); Excel cells read as 0 (G116); removed Query elements (G117); DB-fed Source rotation (G91). |
| **Agent-based market / word-of-mouth models** | `bass-diffusion*`, `consumer-market`, `ab-market-and-sd-supply-chain` cards + `videos/abm-*.md` | Contact targeting, conversion done once, flow counters, stock allocation and ties (G56–G60). |
| **Statecharts, events and messages** (ABM and hybrid) | `08-example-patterns/bigbook/statechart-guards-branches-and-state-reentry.md`, `bigbook/statechart-message-queue-and-safe-handoff.md`, `bigbook/event-modes-condition-monitoring-and-lifecycle.md`, `bigbook/synchronous-tick-transition-from-probability-table.md` | Guards on timeouts, absolute event times, condition re-arming, history resets, message races (G70–G78, G21, G56). |
| **Agent-based service and maintenance fleets** (dispatch, failures, crew sizing) | `08-example-patterns/bigbook/abm-design-recipe-states-messages-and-dispatcher.md`, `bigbook/abm-time-dependent-hazard-rate-refresh.md`, `bigbook/abm-runtime-resizing-of-a-busy-agent-population.md`, `models/field-service.md`, `videos/dispatch-idle-check-then-send-double-booking.md` | Rates that never refresh (G70); dispatch double-booking (G77). |
| **Spatial grids, contact networks and agent relations** | `08-example-patterns/bigbookmodels/wildfire-with-wind.md`, `models/the-game-of-life.md`, `bigbookmodels/periodic-repair-of-a-standard-network.md`, `bigbookmodels/kinship-model-with-customized-statistics.md`, `basicmodels/agent-network-and-layouts-demo.md` | Synchronous steps vs event-driven cells; angle wrap (G109); null neighbours (G110); network rebuilds (G111). |
| **Building or checking a system dynamics model** (lookups, noise, solver step, units, sectors) | `08-example-patterns/bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`, `bigbook/sd-units-check-sectors-and-hierarchical-interfaces.md`, `bigbook/sd-instant-charts-and-step-pause-flight-simulator.md`; examples in `sdmodels/` | Halve the step to verify; lookups, noise, constants, competing outflows, pulses, hybrid cost (G79–G84). |
| **Calendar, dates and time units** | `08-example-patterns/bigbook/calendar-time-dst-safe-events-date-fields-and-run-speed.md`, `videos/sd-calendar-seasonality-start-date-and-months.md` | Setter units (G61), multiplier + drop-down (G62), DST (G63), 0-based months (G64), start date (G65). |
| **Material handling: conveyors, storage, AGVs, cranes, tugger trains, fluids** | `08-example-patterns/videos/mhl-*.md` + `basicmodels/` (storage, stacker crane, tugger train, transporter, fluid cards — search `08-example-patterns/INDEX.md`) | Version-gated features (Downtime 8.9.1, initial stock 8.9.5, tugger trains 8.9.9, `startDelivery()` 8.9.10); traps G42–G45, G93–G97. |
| **AnyLogic's own AI Assistant (8.9.10)** | `01-anylogic-core/README.md` (AI Assistant bullet) | What it can and cannot do, and how this co-pilot complements it. |
| **A worked AnyLogic example to copy idioms from** | `08-example-patterns/INDEX.md` | Distilled cards indexed by paradigm + problem (count in its header). Open the index, not the tree. `videos/` holds techniques distilled from AnyLogic videos and webinars. |

> **Private materials.** The original knowledge base also carried university course PDFs
> (lecture slides, textbooks) that cannot be redistributed. They are **not in this repo** —
> see `PRIVATE-MATERIALS.md` for what was removed and how to supply your own equivalents.
> The router works without them; `SOURCES.md` lists free, legal replacements for each category.

## Version-exact AnyLogic reference: the offline Help
Every AnyLogic install (PLE included) ships the full Help and API docs, exact to that version:

- Help pages (8.9.10: 785 HTML pages among 3,504 files, mirroring anylogic.help):
  `<AnyLogic install>\plugins\com.anylogic.ui_<version>\resources\help\en\` — e.g. on a default
  Windows install of 8.9 PLE, under `C:\Program Files\AnyLogic 8.9 Personal Learning Edition\plugins\`.
  Useful pages: `library-reference-guides/process-modeling-library/wait.html`, `markup/lift.html`,
  `anylogic/experiments/optimization.html`, `cloud/…`.
- Engine Javadoc: `<install>\plugins\com.anylogic.engine_<version>\javadoc\`; per-library Javadoc
  under `<install>\plugins\com.anylogic.<library>_<version>\lib\doc\`; exact signatures with
  `<install>\jre\bin\javap -cp <library jar> <class>`.
- Defaults new elements get in the editor when a Help page doesn't say (e.g. *Visible on upper
  agent*): `com/anylogic/objectmodel/factory/ame_initialization_plan.json` inside
  `<install>\plugins\com.anylogic.objectmodel8impl_<version>.jar`.
- Member names, when Help and code disagree: each library's `lib\doc\member-search-index.js`
  (engine: `plugins\com.anylogic.engine_<ver>\javadoc\member-search-index.js`) or `javap`; the
  library code wins (known Help misprints: gotcha G122).
- Example models (`.alp` XML, read in place):
  `C:\ProgramData\AnyLogic 8.9 <edition>\eclipse\plugins\com.anylogic.examples_<version>\` (default Windows install)
  — `basicmodels`, `models`, `sdmodels`, `bigbookmodels`. Cite what a model does, not its description
  text, which can be stale.
- Search it: `grep -rli "<term>" "<help folder>"`, then read the page. The folder name changes with
  each AnyLogic upgrade — update the path, and rebuild any text copy of the Help made for searching.

anylogic.help blocks automated fetches; when no install is reachable, fetch the archived page
(`https://web.archive.org/web/2025id_/https://anylogic.help/<path>` with `curl --compressed`).

## Searching your PDFs
PDFs are invisible to grep. `python scripts/extract-pdf-text.py` writes a local text copy of every
PDF under `knowledge/` to `knowledge/.pdf-text/` (gitignored, with `=== p. N ===` page markers), so
`grep -rn -i "<term>" knowledge/.pdf-text/` finds what your books already teach. Run it again after
adding PDFs.

## The sub-indexes this router sits on top of
- `08-example-patterns/INDEX.md` — the pattern cards (AUTO-GENERATED; `scripts/build-pattern-index.py`).
- `../SOURCES.md` — external source manifest (download vs fetch-live status + links), including the
  AnyLogic videos distilled into `08-example-patterns/videos/`.
- `PRIVATE-MATERIALS.md` — what is deliberately absent (copyrighted course material) and how to replace it.

## Keeping it honest
Run `python scripts/check-knowledge.py` to verify the KB is internally consistent
(cards well-formed, pattern index in sync, download files present, index links resolve, gotchas file
numbered and cross-referenced).
