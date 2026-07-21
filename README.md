# AnyLogic Simulation Co-pilot — an AI pair-modeling workflow for industrial engineers

A reusable **human-in-the-loop workflow** for planning, building, and validating AnyLogic
simulation models (DES / ABM / SD / hybrid) with an AI assistant — including AI/ML
integration (forecasting, RL) to demonstrate measurable efficiency gains.

Built and battle-tested on a real project: a hybrid digital twin of an academic
hospital's emergency department (patient flow + nurse workforce + pharmacy inventory +
an ONNX-deployed ML demand forecast), with replicated, statistically disciplined
results. The full case study is not yet published; the lessons it paid for are encoded
throughout this repo — especially in the skills.

## The core idea

The AI **specifies**; the human **builds**; the results get **replicated**. The assistant
never claims to have built or run a model — it supplies the modeling approach, the
block-by-block specification, the Java logic, the statistics, and the ML code. Three
rules make it trustworthy:

1. **Paradigm before blocks.** A mandatory Phase 0 chooses DES vs ABM vs SD vs hybrid
   (grounded in Borshchev & Filippov) before a single block is proposed.
2. **Ground before you simulate.** Every claim routes through a single knowledge index
   to a citable file; version-specific AnyLogic details are fetched live, never recalled
   from memory. A linter keeps the knowledge base internally consistent.
3. **Single runs lie.** Every reported number is a Monte-Carlo mean over ≥30 replications
   with confidence intervals; findings must survive full-experiment replication.

## Repository layout

| Path | What it is |
|---|---|
| [copilot/](copilot/) | The product: system prompt ([INSTRUCTIONS.md](copilot/INSTRUCTIONS.md)), knowledge base + grounding router ([knowledge/INDEX.md](copilot/knowledge/INDEX.md)), the Phase 0→6 method ([workflow/](copilot/workflow/)), templates, worked example briefs, and maintenance scripts |
| [.claude/skills/](.claude/skills/) | Seven AnyLogic skills (DES, ABM, SD, 2D, 3D, libraries, debug) encoding idioms and root-caused bugs from real builds. The debug skill **self-updates**: every new root cause is recorded, so the system sharpens with use |
| [docs/adr/](docs/adr/) | Architecture decision records (tooling choice; the single-grounding-router design) |

## Where each kind of knowledge lives (the contract)

- **Method** (what to do, in what order) → `copilot/workflow/` and `copilot/INSTRUCTIONS.md`
- **Idioms** (how to do it in AnyLogic without stepping on rakes) → `.claude/skills/anylogic-*.md`
- **Ground truth** (facts, patterns, sources) → `copilot/knowledge/` behind `INDEX.md`
- **Provenance** (where sources come from, download vs fetch-live) → `copilot/SOURCES.md`

One home per fact. New lessons go to the skill or the knowledge base — never duplicated
into the prompt.

## Quick start

1. **Claude Code (recommended):** open this folder in VS Code with Claude Code. The
   skills load automatically; point the assistant at `copilot/INSTRUCTIONS.md` and start
   with your modeling question — it will run Phase 0 first.
2. **Claude Project:** paste `copilot/INSTRUCTIONS.md` into the custom instructions and
   upload `copilot/knowledge/` (Markdown files) to project knowledge.
3. Verify the knowledge base any time: `python copilot/scripts/check-knowledge.py`
   (exit 0 = clean; it fails on index drift or broken links).

## What is deliberately not here

- **Copyrighted course material** (university slides, commercial textbooks) was stripped
  before publishing. [copilot/knowledge/PRIVATE-MATERIALS.md](copilot/knowledge/PRIVATE-MATERIALS.md)
  lists what was removed and the free, legal replacement for each category.
- **The hospital case study** (evidence log, configuration snapshot, replicated results)
  is held back pending research sign-off and will be published separately.

## Licence

Dual-licensed:

- **Code, scripts, templates, workflow, system prompt, and skills** — [MIT](LICENSE).
- **Knowledge content** under `copilot/knowledge/` (pattern cards, category notes,
  indexes) — [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Attribute as
  "Jonathan Lukwichi, AnyLogic Simulation Co-pilot".
