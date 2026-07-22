---
name: model-premortem
description: FMEA-style pre-mortem on a simulation build plan BEFORE the user starts building. Use immediately after simulation-build-plan produces a plan (or when the user asks "what could go wrong"). Assume the build already failed, enumerate the likeliest failure modes with severity and root cause, and write a guardrail for each into the plan. Turns the debug ledger from reactive to proactive.
---

# model-premortem

Debugging catches failures after they cost hours; a pre-mortem prevents the
predictable ones for the cost of ten minutes. The stance: **"the model was built and
its results were wrong or it never ran — why?"** Work backwards from that assumed
failure. This is the proactive counterpart to `anylogic-debug` (reactive) — the two
share one failure vocabulary, and every new root cause recorded in the debug ledger
becomes a candidate row here.

Run it on a completed build plan, before Step 1 of the build.

## The procedure

1. **Oracle pass (model-specific).** Given THIS plan — its paradigm, blocks, data,
   and experiment design — predict the **top 3–5 most likely failure modes for this
   specific model**, not generic ones. Reason from the plan's risk surface: data-driven
   arrivals? routing conditions? experiment parameters? agent populations? long-tailed
   distributions?
2. **FMEA table.** For each failure mode, one row:

   | Plan step | Failure mode | Effect (what the user would see) | Severity 1–10 | Root cause | Guardrail |
   |---|---|---|---|---|---|

   Severity anchors: 9–10 = silently wrong results that could be published; 6–8 =
   wrong results but detectable; 3–5 = crash/won't run (annoying but honest); 1–2 =
   cosmetic.
   **Prioritise silent failures over crashes** — a model that runs and lies is far more
   dangerous than one that won't compile.
3. **Write the guardrails INTO the plan.** Each guardrail becomes either (a) an added
   property/setting in the relevant build step, (b) an added verify checkpoint ("probe:
   traceln X at t=0; expect Y"), or (c) an added sanity check in the plan's final
   section. A guardrail that isn't attached to a step is a wish, not a guardrail.
4. **Confirm with the user** which high-severity rows they accept as residual risk
   versus which get guardrails.

## Standing high-severity rows (check EVERY plan against these)

Paid-for failures from real builds — the ledger's greatest hits:

| Failure mode | Severity | Guardrail |
|---|---|---|
| Experiment Parameters table overrides Main's defaults — the lever you toggle on Main does nothing | 10 | Set treatment parameters IN the experiment; probe: print the parameter at t=0 in the actual run |
| Routing variable set in the deciding block's On-enter — SelectOutput reads a stale value, one branch takes everything | 9 | Set routing upstream (previous block's On exit); probe the variable at the branch |
| A queueing block left at default priority 0 — FIFO silently defeats the priority scheme | 8 | Task-priority expression on EVERY queueing block, including the first |
| Rate expression AND inject()-event both driving a Source — double-driven arrivals flood the model (PLE agent cap) | 8 | One arrival mechanism only; assert daily counts against the input data |
| Single-run numbers treated as results | 9 | Reps experiment (N=30) exists from day one; every cited number = mean ± CI |
| Untruncated heavy-tailed distribution (lead times, service times) generates physically impossible values | 7 | Cap at a justified physical maximum; state the truncation in the plan |
| Statistic collected but never fed / fed a dead variable — reports 0 or min=max forever | 7 | Verify checkpoint per statistic: N samples, min ≠ max, plausible magnitude |
| Model time-unit changed mid-build — every rate and delay silently rescales | 8 | Time units locked in plan Step 1; never changed after |
| Policy formula's assumed input distribution ≠ what the model actually generates (e.g. multipliers applied after variance was computed) | 9 | Probe: measure the realised distribution in-model and compare to the formula's assumption |

## Output

Append to the build plan: the FMEA table, the modified steps (marked), and a one-line
risk summary ("top residual risk: X, accepted by user"). Then the build starts.

## Self-improvement contract

When `anylogic-debug` root-causes a NEW failure that a pre-mortem could have caught,
add it to the standing rows above (one line, severity, guardrail). The ledger teaches
the oracle.
