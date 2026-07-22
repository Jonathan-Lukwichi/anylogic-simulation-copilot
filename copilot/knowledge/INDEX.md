# Knowledge INDEX — the single grounding router

**Start here.** This is the one entry point the co-pilot uses to route any task to
ground truth. Do not reconstruct routing from memory; look it up here, open the named
files, and **cite the specific file**. Never invent block names, settings, or numbers.

> **GROUNDING RULE (single source of truth):** when a task touches modelling approach,
> statistics / input distributions, supply chain, manufacturing, healthcare, optimization,
> the AI/ML-RL layer, or a worked AnyLogic pattern — consult the matching row below FIRST.
> Prefer these sources over guessing. For version-specific AnyLogic block fields, FETCH
> live from anylogic.help (see SOURCES.md) rather than relying on memory.

## Task → where to look

| If the task is about… | Go to | Notes |
|---|---|---|
| **Choosing the modelling approach** (DES / ABM / SD / hybrid — Phase 0) | `00-method-selection/` | Borshchev & Filippov is the approach-choice authority (see `../SOURCES.md`). Always settle this before blocks. |
| **AnyLogic blocks, PLE limits, RL/Alpyne APIs** | `01-anylogic-core/` → **fetch live** from anylogic.help | Version-specific; never freeze. See SOURCES.md. |
| **AnyLogic beginner traps / conventions** (naming, etc.) | `01-anylogic-core/anylogic-gotchas.md` | Growing list of common mistakes + fixes. |
| **AnyLogic build/debug idioms** (DES, ABM, SD, 2D/3D, libraries, debugging) | `../../.claude/skills/anylogic-*.md` | Battle-tested skills; the debug skill self-updates with each new root cause. |
| **Statistics / input distributions / goodness-of-fit / interpreting results** | `../../.claude/skills/stats-analyst.md` + `02-statistics-input-modeling/` + NIST e-Handbook (see SOURCES.md) | Fit properly (scipy.stats / fitdistrplus) + report KS/AD. Don't eyeball. Results interpretation in plain English → the skill. |
| **Supply chain, inventory policy, network/distribution** | `../../.claude/skills/supply-chain-analyst.md` + `03-supply-chain/` + Ivanov book (see SOURCES.md) | Simchi-Levi et al. is the textbook anchor — supply your own copy (see PRIVATE-MATERIALS.md). Domain interpretation of results → the skill. |
| **Manufacturing / warehouse / lean / job-shop** | `04-manufacturing-warehouse/` + AnyLogic job-shop tutorial (fetch live) | Pair with pattern cards (job-shop, distribution-center). |
| **Healthcare / ED / patient flow** | `05-healthcare/` | DES-in-ED systematic reviews; efficiency-metric framing. |
| **AI / ML / RL integration to show efficiency** | `06-ai-ml-integration/` + `templates/rl-pipeline/` | Always frame baseline vs ML-informed vs RL on the SAME KPIs. Alpyne or Azure ML. |
| **Optimization experiments / OptQuest** | `07-optimization/` → fetch live | Parameter optimisation; WSC tutorials. |
| **A worked AnyLogic example to copy idioms from** | `08-example-patterns/INDEX.md` | **223 distilled cards** indexed by paradigm + problem. Open the index, not the tree. |

> **Private materials.** The original knowledge base also carried university course PDFs
> (lecture slides, textbooks) that cannot be redistributed. They are **not in this repo** —
> see `PRIVATE-MATERIALS.md` for what was removed and how to supply your own equivalents.
> The router works without them; `SOURCES.md` lists free, legal replacements for each category.

## The sub-indexes this router sits on top of
- `08-example-patterns/INDEX.md` — 223 pattern cards (AUTO-GENERATED; `scripts/build-pattern-index.py`).
- `../SOURCES.md` — external source manifest (download vs fetch-live status + links).
- `PRIVATE-MATERIALS.md` — what is deliberately absent (copyrighted course material) and how to replace it.

## Keeping it honest
Run `python scripts/check-knowledge.py` to verify the KB is internally consistent
(cards well-formed, pattern index in sync, download folders non-empty, index links resolve).
