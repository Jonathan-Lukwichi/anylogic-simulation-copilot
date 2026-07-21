# Private materials — deliberately NOT in this repository

The knowledge base this co-pilot was developed against also contained university course
material and commercial textbooks. Those files are **copyrighted and cannot be
redistributed**, so they were stripped before publishing. This file records what is
absent and how to supply your own equivalents. The co-pilot works without them — every
category still has a free, legal anchor in `../SOURCES.md`.

## What was removed (and the free replacement)

| Removed (kept private) | Category | Free, legal replacement (see `../SOURCES.md`) |
|---|---|---|
| MIL780 engineering-modelling lecture slides | `00-method-selection/` | Borshchev & Filippov approach-choice paper (AnyLogic-hosted, free) |
| Statistics course PDFs + REA "Statistics Super Review" chapters | `02-statistics-input-modeling/` | NIST/SEMATECH e-Handbook of Statistical Methods (free) + scipy.stats / fitdistrplus docs (fetch live) |
| BVK780 supply-chain slides + Simchi-Levi textbook editions | `03-supply-chain/` | Ivanov — *Operations & Supply Chain Simulation with AnyLogic* (free official PDF) + anyLogistix textbook (free) |
| Lean-manufacturing tools reference PDF | `04-manufacturing-warehouse/` | AnyLogic job-shop tutorial (fetch live) |
| *Python for Everybody* course copy | `06-ai-ml-integration/` | py4e.com (the book is freely available from its author) |
| University assignment models (.alp) + layout images | `08-example-patterns/from-courses-models/` | The 223 distilled pattern cards remain — they are original-wording distillations, not copies |
| Entire BUK780 course archive (78 files: slides, tutorials, Java basics, project domain) | `09-course-materials-buk780/` | Not replaced — it was project-specific. The reusable lessons were long since distilled into the skills and pattern cards |

## If you have your own course material

Drop it into the matching category folder under a `from-courses/` subfolder and add a row
to `INDEX.md` pointing at it. Keep it out of git: the repo `.gitignore` excludes
`copilot/knowledge/**/*.pdf` by default, so local PDFs never get committed by accident.

## Why the pattern cards are fine

`08-example-patterns/` contains **distilled descriptions** of AnyLogic's built-in example
models — block chains, key settings, and the reusable idea, written in original wording.
They are study notes about publicly shipped examples, not copies of the models or their
source. The `.alp` files themselves are never included.
