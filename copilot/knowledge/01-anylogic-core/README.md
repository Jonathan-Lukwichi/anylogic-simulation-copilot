# 01-anylogic-core

AnyLogic block reference, PLE limits, tutorials, example models.

- **Traps and error messages:** `anylogic-gotchas.md` — start from its quick-lookup table (G1–G60).
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
- **PLE limits (Help 8.9.9, Editions):** at most 10 agent types per model; 50,000 dynamically
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

See SOURCES.md for the exact links and download/fetch-live status.
