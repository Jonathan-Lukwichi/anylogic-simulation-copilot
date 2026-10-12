# 01-anylogic-core

AnyLogic block reference, PLE limits, tutorials, example models. Techniques from 12 of the 16 free
*Big Book of Simulation Modeling* chapters are distilled in `../08-example-patterns/bigbook/` (chapter
links in SOURCES.md).

- **Traps and error messages:** `anylogic-gotchas.md` — start from its quick-lookup table (G1–G122).
- **Block fields / API, exact to the installed version:** the offline Help and Javadoc shipped with
  every AnyLogic install (location and how to search it: `../INDEX.md`). anylogic.help itself blocks
  automated fetches; an archived copy (`web.archive.org/web/2025id_/https://anylogic.help/<path>`,
  fetched with `curl --compressed`) is the fallback when no install is reachable.
- **Version notes worth knowing:** 8.6 made new models skip the Simulation experiment screen by
  default (G50) and removed the experiment's simultaneous-events setting — the engine runs them LIFO
  (G60); 8.7+ converts CAD layers to walls; 8.8.4 added the Genetic optimization engine; 8.8.5
  changed the GIS place-name search server, fixed again in 8.9.5 — store coordinates (G51); 8.9.0
  renamed the population-statistics variable `item` to `agent` (G53); 8.9.2 deprecated
  `deliver()`/`receive()` in favour of `send()` (G24); 8.9.4 added Projects-view folders; 8.9.5
  removed the PML Conveyor and Rack blocks from the palette (G7); 8.9.7 added a Python Design-time
  API that generates markup from scripts
  (`../08-example-patterns/videos/layout-candidates-and-design-time-api.md`); 8.9.8 joins converted
  rail-track ends less than 30 cm apart (G52).
- **AnyLogic 8.9.10 (Sep 2026), per its release notes:**
  built-in AI Assistant (below); the Schedule element remastered — the Days/Weeks type is gone (old
  schedules converted to daily or custom), weeks start on Monday, moment schedules exist only as
  arrival schedules, and values can come from functions, parameters or a database interval table
  (G92); *Link to Agent* split into *2-Way* and *1-Way Link to Agents*; *Frame* renamed *Animation
  Window*; 2D draw order now follows the Model Tree (drag to reorder; also inside GIS maps);
  *Export Model to Standalone Application* is now a paid option (G14); Jackson 2.21.4 — imports of
  `PropertyNamingStrategy` become `PropertyNamingStrategies`; Material Handling: *Fastest* routing
  policy and a *Route* property for custom routing, `recalculatePriorities()`,
  `getEstimatedTimeOfArrival()`, `jump()`, `startDelivery()` for tugger trains, *On collision* and
  *On movement suspended / resumed* actions, Level Gate *Time to reach paired port*; ResourcePool
  labels renamed to match the Schedule; `executeExpression()` now works outside Main (bug fix). No
  Process Modeling or Material Handling palette block was added or removed.
- **AnyLogic AI Assistant (8.9.10; Help *AI assistant*):** enabled in the installer, configured in
  Tools → Preferences → *AI Assistant* (AnyLogic AI through a public AnyLogic Cloud account, or a custom
  LLM with model id, API key and URL — Claude models included), opened with View → AI Assistant; the
  SLA is accepted at the first prompt. It drafts simple high-level models from a prompt, explains open
  models and troubleshoots errors, but cannot edit existing models (not even its own drafts), create
  custom blocks or markup, or use statecharts or system dynamics; AnyLogic says drafts must be reviewed
  and used only for reference. This co-pilot complements it: method choice before any build, ABM, SD
  and hybrid designs, verified traps (`anylogic-gotchas.md`), validation and decision framing. A good
  hand-off is to let the assistant draft a PML skeleton, then check it here against the spec and the
  gotchas.
- **PLE limits (Help 8.9.9, Editions; unchanged in 8.9.10):** at most 10 agent types per model; 50,000 dynamically
  created agents; 200 populations and flowchart blocks, and 200 system-dynamics variables, per agent
  type; OptQuest capped at 500 iterations and 7 decision variables per experiment; model time limited
  to 5 hours in libraries other than the Process Modeling Library (the Help does not define that
  scope further).
- **AnyLogic Cloud** (being rebranded AnyLogic Online): delivery as a stakeholder tool
  (`../08-example-patterns/videos/cloud-decision-tool-for-stakeholders.md`); run semantics, Outputs,
  sharing roles and account tiers (`videos/cloud-run-semantics-and-access.md`); programmatic runs
  from Python, Java, JS or REST (`videos/cloud-api-programmatic-runs.md`); workbook input/output
  through the model database (`videos/excel-round-trip-results-and-cloud.md`); traps G38–G40 and
  G46–G49 — set-up code belongs in Main's On startup, because Cloud skips the experiment's own set-up
  code.
- **Search your local PDFs:** `python scripts/extract-pdf-text.py`, then grep `knowledge/.pdf-text/`.

- **Data input and output — pick the route by the data's shape:**

  | Data shape / need | Route | Card |
  |---|---|---|
  | Row-shaped tables, Cloud delivery, results back to a workbook | Built-in database import with *Autoupdate*; QueryDSL; *Export tables at the end* | `../08-example-patterns/videos/excel-round-trip-results-and-cloud.md` |
  | Scattered cells, formulas, key–value parameter sheets, formatted report templates | Excel File element (typed cell API, `writeDataSet`) | `../08-example-patterns/bigbookmodels/reading-model-parameters-from-excel-using-reflection.md` |
  | Flat delimited files, curves, plain logs | Text File element | `../08-example-patterns/bigbookmodels/reading-agent-parameters-from-a-csv-file.md` |
  | Live company database, very large per-entity logs, BI tools | External Database element; prepared statements; one transaction per run | `../08-example-patterns/bigbookmodels/using-prepared-statement-when-writing-to-databases.md` |

  Whatever the route, show what was loaded (row counts, key values on screen or as an `Output`) and
  fail loudly on missing keys (G116).
See SOURCES.md for the exact links and download/fetch-live status.
