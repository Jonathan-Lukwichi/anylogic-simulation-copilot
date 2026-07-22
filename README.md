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
| [.claude/skills/](.claude/skills/) | Nine skills: seven AnyLogic skills (DES, ABM, SD, 2D, 3D, libraries, debug) encoding idioms and root-caused bugs from real builds, plus `simulation-welcome` (guided project intake) and `simulation-build-plan` (step-by-step build plan with a preview flow diagram and canvas layout). The debug skill **self-updates**: every new root cause is recorded, so the system sharpens with use |
| [docs/adr/](docs/adr/) | Architecture decision records (tooling choice; the single-grounding-router design) |

## Where each kind of knowledge lives (the contract)

- **Method** (what to do, in what order) → `copilot/workflow/` and `copilot/INSTRUCTIONS.md`
- **Idioms** (how to do it in AnyLogic without stepping on rakes) → `.claude/skills/anylogic-*.md`
- **Ground truth** (facts, patterns, sources) → `copilot/knowledge/` behind `INDEX.md`
- **Provenance** (where sources come from, download vs fetch-live) → `copilot/SOURCES.md`

One home per fact. New lessons go to the skill or the knowledge base — never duplicated
into the prompt.

## Getting started

### What you need

| Requirement | Why | Cost |
|---|---|---|
| **VS Code + the Claude Code extension** (or the Claude Code CLI) | The AI runtime this workflow is built for | Claude subscription (Pro/Team) or API key |
| **AnyLogic** (Personal Learning Edition is fine) | You build the actual model — the AI only specifies | PLE is free |
| **Git** (or the Download-ZIP button) | To get this folder | Free |
| Python 3 *(optional)* | Only for `check-knowledge.py`, the knowledge-base linter | Free |

### Install (three steps)

1. **Get the folder:**
   ```
   git clone https://github.com/Jonathan-Lukwichi/anylogic-simulation-copilot.git
   ```
   or use **Code → Download ZIP** on the repo page and extract anywhere.

2. **Open the folder in VS Code** with the Claude Code extension signed in. That is all
   the installation there is — the setup lives in the folder layout:
   - `.claude/skills/` — the seven AnyLogic skills load **automatically** when Claude
     Code opens this folder. No configuration.
   - `copilot/knowledge/` — the grounding router and 223 pattern cards are read from
     disk on demand.

3. **Start working.** Make your first message:
   > *Read `copilot/INSTRUCTIONS.md` and act as the co-pilot. I want to model
   > [your problem].*

   The assistant will run **Phase 0 first** (choose DES / ABM / SD / hybrid, with
   justification), then guide the build block-by-block while you drive AnyLogic —
   grounding its claims in the knowledge base and pulling the right skill (DES idioms,
   debugging method, …) as you go.

### No VS Code? Use a Claude Project

From a browser at claude.ai: create a Project → paste `copilot/INSTRUCTIONS.md` into
the custom instructions → upload the Markdown files from `copilot/knowledge/` as
project knowledge. You lose the auto-loading skills and live file access, but the
method and grounding still work.

### Maintenance

Verify the knowledge base any time: `python copilot/scripts/check-knowledge.py`
(exit 0 = clean; it fails on index drift or broken links).

## Licence

Dual-licensed:

- **Code, scripts, templates, workflow, system prompt, and skills** — [MIT](LICENSE).
- **Knowledge content** under `copilot/knowledge/` (pattern cards, category notes,
  indexes) — [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Attribute as
  "Jonathan Lukwichi, AnyLogic Simulation Co-pilot".
