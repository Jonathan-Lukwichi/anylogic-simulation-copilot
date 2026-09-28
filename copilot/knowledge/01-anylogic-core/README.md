# 01-anylogic-core

AnyLogic block reference, PLE limits, tutorials, example models.

- **Traps and error messages:** `anylogic-gotchas.md` — start from its quick-lookup table (G1–G45).
- **Block fields / API, exact to the installed version:** the offline Help and Javadoc shipped with
  every AnyLogic install (location and how to search it: `../INDEX.md`). anylogic.help itself blocks
  automated fetches; an archived copy (`web.archive.org/web/2025id_/https://anylogic.help/<path>`,
  fetched with `curl --compressed`) is the fallback when no install is reachable.
- **Version notes worth knowing:** 8.7+ converts CAD layers to walls; 8.8.4 added the Genetic
  optimization engine; 8.9.2 deprecated `deliver()`/`receive()` in favour of `send()` (G24);
  8.9.4 added Projects-view folders; 8.9.5 removed the PML Conveyor and Rack blocks from the palette
  (G7); 8.9.7 added a Python Design-time API that generates markup from scripts
  (`../08-example-patterns/videos/layout-candidates-and-design-time-api.md`).
- **AnyLogic Cloud** (being rebranded AnyLogic Online): delivery as a stakeholder tool
  (`../08-example-patterns/videos/cloud-decision-tool-for-stakeholders.md`); run semantics, Outputs,
  sharing roles and account tiers (`videos/cloud-run-semantics-and-access.md`); programmatic runs
  from Python, Java, JS or REST (`videos/cloud-api-programmatic-runs.md`); traps G38–G40.
- **Search your local PDFs:** `python scripts/extract-pdf-text.py`, then grep `knowledge/.pdf-text/`.

See SOURCES.md for the exact links and download/fetch-live status.
