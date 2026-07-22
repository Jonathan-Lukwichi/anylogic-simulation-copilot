---
name: triangulate-verify
description: Truth-verification protocol for high-stakes claims. Use before any external claim enters a deliverable - market/industry figures, benchmark numbers, literature citations, vendor performance claims, "best practice" assertions - or when sources disagree. Diverge across independent sources, converge on consensus only, grade confidence, and ground-truth citations. Single-source claims are never cited as fact.
---

# triangulate-verify

No single query, source, or model is trustworthy on its own: LLMs are coherence
optimizers with no ground-truth mechanism, and they fail *confidently* (see the 2025
Deloitte AU$440k refund over hallucinated citations in a government report — the
canonical cautionary case). Truth is approached by **triangulation**; the human is the
final arbiter.

Run this BEFORE a claim lands in anything that ships: reports, theses, README claims,
business cases, client deliverables.

## Phase 1 — Diverge (gather widely, independently)

- Search/ask **multiple independent routes**: different search queries, different
  source types (academic, official statistics, industry press, practitioner forums),
  and where available different models/tools. Independence is the point — don't let
  route 2 see route 1's answer.
- **Competing-claims mandate:** actively look for sources that DISAGREE with the
  emerging answer, not just ones that confirm it.
- Every candidate fact is captured with: exact quote (or figure), source name, URL,
  and date. No quote+source = not a candidate fact.
- Break the English-only / first-page-of-results bubble when the topic is regional
  (for SA topics: local sources — StatsSA, industry bodies, local press).

## Phase 2 — Converge (consensus only, clean room)

- In a fresh pass (not the gathering context), keep ONLY facts confirmed by
  **independent** sources (two outlets quoting the same press release = one source).
- Everything else goes to an explicit **"Areas of Disagreement / Unconfirmed"**
  section — never silently dropped, never silently promoted.

## Phase 3 — Grade and decide

| Confidence | Meaning | Action |
|---|---|---|
| **Strong** | ≥2 truly independent sources agree; citation ground-truthed | Cite it |
| **Moderate** | Single credible source, or minor disagreement | Include WITH explicit caveat ("single-source", "vendor-claimed") |
| **Weak/Contested** | Sources conflict or only low-quality sources | Exclude; park in "claims under investigation" |
| **Unverified** | Cannot trace to any real source | Remove entirely |

## Ground-truthing rules (non-negotiable)

- **Assume every citation is hallucinated until opened.** Fetch the URL / check the
  DOI; confirm the source says what the claim says (lateral reading: judge the source
  by what others say about it, not by its own self-description).
- Vendor and marketing figures are ALWAYS labeled as such ("vendor-claimed"), never
  presented as independent fact.
- Round-number red flag: suspiciously clean figures ("80% of companies…") demand a
  primary source before use.
- When replacing a bad citation, re-examine the CLAIM, not just the reference — if the
  only support was hallucinated, the claim itself is probably unsupported.

## Where this plugs into the workflow

- Market/opportunity claims in business docs (the workspace's evidence-first rule is
  this skill's contract: never fabricate statistics, citations, or ROI figures).
- Literature claims in thesis/report writing → the Strong/Moderate/Weak decision rules
  ARE the inclusion rules.
- Benchmark or "best practice" numbers found in course material or blogs → grade
  before reuse; most belong at Moderate with a caveat.
- Disagreements between the knowledge base and a live web source → fetch, ground-truth,
  and prefer the verifiable one; record the correction.
