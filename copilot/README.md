# IE Simulation Co-pilot

A reusable, transferable workflow that helps industrial engineers plan, build, and
validate **modeling and simulation** projects — discrete-event, agent-based, hybrid —
in AnyLogic (FlexSim-aware), including **AI/ML integration** to show efficiency gains.

It is an *advisor*, not an autocomplete: it chooses the **modeling approach first**,
then guides the build, the statistics, and the AI/ML layer.

## What's in here
- `INSTRUCTIONS.md` — the system prompt (persona + Phase 0 + the six-phase build method + rules).
- `knowledge/INDEX.md` — **the single grounding router** (task → files). Start here for any task.
- `SOURCES.md` — the knowledge-base manifest: every source, its URL, and whether to **download** it or **fetch live**.
- `workflow/` — the method as usable documents (Phase 0 framing, Phases 1-6 build, checklists).
- `knowledge/` — the curated, downloaded reference core, organised by category. `08-example-patterns/INDEX.md` indexes 223 distilled pattern cards.
- `templates/` — reusable scaffolds (model spec, distribution fitting, RL pipeline).
- `examples/` — worked briefs to test the co-pilot (ED patient flow, water-bottle filling).
- `scripts/` — maintenance tools: `build-pattern-index.py` (regenerate the pattern index),
  `check-knowledge.py` (lint the KB for consistency), plus update notes.
- `../.claude/skills/anylogic-*.md` — the battle-tested build/debug idiom skills (DES, ABM, SD,
  2D/3D, libraries, debugging). The workflow owns the *method*; the skills own the *idioms*.
- `knowledge/PRIVATE-MATERIALS.md` — copyrighted course PDFs were stripped before publishing;
  this file lists what was removed and the free, legal replacement for each category.

## Set it up (pick one runtime)
1. **Claude Project (fastest):** create a Project, paste `INSTRUCTIONS.md` into the
   custom instructions, and upload the files under `knowledge/` to the project knowledge base.
2. **Claude Code in VS Code:** open this folder. Claude Code reads `knowledge/` locally and
   fetches the "fetch-live" sources on demand. Point it at `INSTRUCTIONS.md`.
3. **API app (advanced):** load `INSTRUCTIONS.md` as the system prompt and run RAG over `knowledge/`.

## Sustainability
- Download the stable core (books, NIST, reviews, method-selection paper) into `knowledge/`.
- Leave version-specific AnyLogic block docs as **fetch-live** so they never go stale.
- Keep `SOURCES.md` current and re-pull on each AnyLogic release (see `scripts/update_sources.md`).

## Building the example-pattern library (new)
`knowledge/08-example-patterns/` holds distilled "pattern cards" from AnyLogic's built-in
example models. Use `scripts/generate-pattern-cards.md` to have Claude Code read your local
AnyLogic example files (plain XML) and auto-write the cards. See `templates/pattern-card-template.md`.
