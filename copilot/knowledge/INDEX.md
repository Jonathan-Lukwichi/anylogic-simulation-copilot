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
| **Choosing the modelling approach** (DES / ABM / SD / hybrid — Phase 0) | `00-method-selection/` | Borshchev & Filippov is the approach-choice authority (see `../SOURCES.md`). Always settle this before blocks. Hybrid wiring (statechart agent through a hosted flowchart): `08-example-patterns/videos/statechart-agent-through-hosted-flowchart.md`. |
| **Framing the decision** (boundary, living tool vs one-off study, digital-twin kind, layout and equipment questions) | `../workflow/phase-0-framing.md` | Boundary "one interface past the lever"; twin = which layer / sync mode; layouts are ranked, not optimised. |
| **AnyLogic blocks, PLE limits, RL/Alpyne APIs** | offline Help (below) → else anylogic.help; `01-anylogic-core/README.md` | Version-specific; never freeze. See SOURCES.md. |
| **A symptom, error message or "it behaves oddly"** | `01-anylogic-core/anylogic-gotchas.md` — **quick-lookup table at the top** | G1–G60: symptom → cause → fix → why, verified against the 8.9.9 Help. Then `anylogic-debug`. |
| **AnyLogic build/debug idioms** (DES, ABM, SD, 2D/3D, libraries, debugging) | `../../.claude/skills/anylogic-*.md` | Battle-tested skills; the debug skill self-updates with each new root cause. |
| **Statistics / input distributions / goodness-of-fit / interpreting results** | `../../.claude/skills/stats-analyst.md` + `02-statistics-input-modeling/README.md` (fitted vs empirical rule) + NIST e-Handbook (see SOURCES.md) | Fit properly (scipy.stats / fitdistrplus) + report KS/AD. Don't eyeball. Empirical forms can't exceed the observed range. Results interpretation in plain English → the skill. |
| **Randomness, seeds, replications** | gotchas G16–G17 + `08-example-patterns/videos/rng-seed-control-and-custom-generator.md` | Fixed seed for building; replications for estimates. |
| **Supply chain, inventory policy, network/distribution** | `../../.claude/skills/supply-chain-analyst.md` + `03-supply-chain/README.md` + Ivanov book (see SOURCES.md) | Simchi-Levi et al. is the textbook anchor — supply your own copy (see PRIVATE-MATERIALS.md). Pharma twin card in `08-.../videos/`. Domain interpretation of results → the skill. |
| **Manufacturing / warehouse / lean / job-shop / OEE / material handling** | `04-manufacturing-warehouse/README.md` + AnyLogic job-shop tutorial (fetch live) | Pair with pattern cards (job-shop, distribution-center); OEE, dispatching-rule and `mhl-*` cards in `08-.../videos/`. |
| **Healthcare / ED / patient flow** | `05-healthcare/` | DES-in-ED systematic reviews; efficiency-metric framing. |
| **AI / ML / RL integration to show efficiency** | `06-ai-ml-integration/README.md` + `templates/rl-pipeline/` | Always frame baseline vs ML-informed vs RL on the SAME KPIs. Alpyne, Cloud API or Pypeline — see the README's route choice. |
| **Optimization experiments / OptQuest / Genetic / sim-opt design** | `07-optimization/README.md` (technique matrix, setup essentials, experiment ladder) → sim-opt cards in `08-.../videos/` | Constraint vs Requirement, replications and lucky optima, many-lever tactics, engine limits (gotchas G8–G15). |
| **Delivering on AnyLogic Cloud** (stakeholder tool, run semantics, API) | `01-anylogic-core/README.md` (Cloud bullet) → `08-.../videos/cloud-*.md` | Run Configuration rules, Play vs Run, stored results (G38–G40). |
| **Space markup: levels, lifts, rail, pedestrians, CAD, 3D, animation** | `08-example-patterns/videos/` (multi-level, rail shuttle, crossing, CAD walls, shapefile → rail markup, spiral conveyor, 3D scene, animation binding) | Traps G25–G34, G52, G54. |
| **Real geography** (sites on a GIS map, routes, networks from shapefiles) | `08-example-patterns/videos/gis-agent-placement-from-table.md`, `videos/gis-shapefile-to-rail-markup.md`; examples `models/shape-file-example.md`, `models/corporate-education.md` | Store coordinates, not place names (G51); a converted network is geometry to curate (G52). |
| **Excel / database input and output, Cloud files** | reading: `08-example-patterns/basicmodels/getting-values-from-anylogic-database.md` (+ *AnyLogic in 3 Days*, database chapter); writing and Cloud files: `videos/excel-round-trip-results-and-cloud.md` | Autoupdate on startup, purge then write, startup order (G46–G49). |
| **Agent-based market / word-of-mouth models** | `bass-diffusion*`, `consumer-market`, `ab-market-and-sd-supply-chain` cards + `videos/abm-*.md` | Contact targeting, conversion done once, flow counters, stock allocation and ties (G56–G60). |
| **A worked AnyLogic example to copy idioms from** | `08-example-patterns/INDEX.md` | Distilled cards indexed by paradigm + problem (count in its header). Open the index, not the tree. `videos/` holds techniques distilled from AnyLogic videos and webinars. |

> **Private materials.** The original knowledge base also carried university course PDFs
> (lecture slides, textbooks) that cannot be redistributed. They are **not in this repo** —
> see `PRIVATE-MATERIALS.md` for what was removed and how to supply your own equivalents.
> The router works without them; `SOURCES.md` lists free, legal replacements for each category.

## Version-exact AnyLogic reference: the offline Help
Every AnyLogic install (PLE included) ships the full Help and API docs, exact to that version:

- Help pages (≈2,700 HTML, mirroring anylogic.help):
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
- Search it: `grep -rli "<term>" "<help folder>"`, then read the page. The folder name changes with
  each AnyLogic upgrade.

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
(cards well-formed, pattern index in sync, download folders non-empty, index links resolve).
