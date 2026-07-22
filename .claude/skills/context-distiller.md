---
name: context-distiller
description: Two-stage "cognitive hygiene" protocol (ThoT then CoT) for messy inputs. Use whenever the user shares a long, noisy, or multi-source input - an uploaded brief/SOP/thesis chapter at intake, a raw results dump, conflicting stakeholder notes, or several documents at once. FIRST distill a clean attributed thread, THEN reason. Never reason directly over chaos.
---

# context-distiller

Reasoning over a noisy context contaminates the reasoning: facts get lost in the
middle, contradictions slip through, and the model's own early misreadings become
"ground truth" later. The cure is an air gap: **Stage 1 analyses without answering;
Stage 2 answers using ONLY the analysis.**

Trigger test — run this skill when ≥2 of these hold: long input (multiple pages),
multiple sources or authors, mixed relevance (signal buried in noise), unordered or
conflicting information.

## Stage 1 — The Analyst (distill, do NOT answer)

Walk the source(s) sequentially and produce an **Analytical Thread**:

- Number each source: `[SOURCE-1]`, `[SOURCE-2]` … (a section, file, or speaker counts
  as a source). **Every extracted fact carries its source tag.**
- Extract exhaustively: facts, figures (with units), constraints, decisions, names.
- Separate **fact from inference**: anything not literally stated is tagged
  `[INFERENCE]`.
- Flag loudly, inline:
  - `[!!! CONTRADICTION: SOURCE-2 says X, SOURCE-4 says Y !!!]`
  - `[!!! GAP: <what the question needs that no source provides> !!!]`
- No conclusions, no recommendations, no answering the user's question yet. The
  thread's only job is to be a faithful, clean, citable representation.

For scenario documents at intake, structure the thread by the intake card fields
(decision, system & boundary, resources, variability, data, KPIs) so it hands straight
to `simulation-welcome` Step 2.

## Stage 2 — The Reasoner (answer from the thread ONLY)

- Reason step by step **exclusively over the Analytical Thread** — if it isn't in the
  thread, it doesn't exist; go back to Stage 1 rather than "remembering" the raw text.
- Cite the thread per point (`per SOURCE-3`).
- **Address every CONTRADICTION and GAP flag explicitly** — resolve it, ask the user,
  or carry it as a stated assumption. Silent dropping of a flag is the failure mode
  this skill exists to prevent.

## Multi-perspective variant (for contested decisions)

When the input argues for a decision (vendor docs, a stakeholder proposal): run Stage 1
twice — once as **proponent** (strongest case FOR, attributed) and once as **skeptic**
(strongest case AGAINST, attributed) — then a Stage 2 synthesis that cites both
threads and names the core tension before recommending.

## Where this plugs into the workflow

- `simulation-welcome` Step 2 (document given) → distill first, reflect the thread
  back, then ask only the questions the thread leaves open.
- `stats-analyst` / `supply-chain-analyst` results uploads → Stage 1 the raw dump
  (which experiment, which arm, how many reps, which KPIs) before any verdict.
- Any multi-document research task → thread per document, then synthesis.
