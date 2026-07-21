# ADR-0002: Single grounding router for the Co-pilot knowledge base

- **Status:** accepted
- **Date:** 2026-06-23

## Context
The IE Simulation Co-pilot's knowledge base is high-quality but its *navigation* was
shallow: routing a task to ground truth required reading 5+ overlapping files
(INSTRUCTIONS §Knowledge rules, COURSE-IMPORTS-INDEX.md, 09/INVENTORY.md, SOURCES.md,
per-category READMEs), with the grounding rule duplicated across two of them. The
~223 pattern cards in 08-example-patterns had no index — they could only be found by
scanning the file tree. There was no check that the KB stayed internally consistent.

## Decision
Introduce one deep boundary: **`knowledge/INDEX.md`** as the single grounding router
(a task → files lookup) that all sub-indexes sit beneath. Generate
**`knowledge/08-example-patterns/INDEX.md`** from disk via `scripts/build-pattern-index.py`
(characterise-first: the index is derived, never hand-maintained). Add
`scripts/check-knowledge.py` as the KB's feedback loop. Point `INSTRUCTIONS.md` at the
single router and remove the duplicated routing prose.

## Consequences
- Easier: one place to find ground truth; pattern cards are queryable by paradigm +
  problem; consistency is verifiable (`check-knowledge.py` exits non-zero on drift).
- Harder: the pattern index must be regenerated after card changes (enforced by the
  linter, which fails if counts drift); INSTRUCTIONS now depends on knowledge/INDEX.md
  existing — a contract to maintain.
- Committed: knowledge/INDEX.md is the canonical entry; pattern frontmatter must keep
  the title + Paradigm + "Problem it solves" fields the generator relies on.
