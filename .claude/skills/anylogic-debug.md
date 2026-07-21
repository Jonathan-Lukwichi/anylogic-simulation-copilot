---
name: anylogic-debug
description: Root-cause debugging for AnyLogic models (and any simulation with silent logic bugs). Use when a model errors, won't compile, floods agents, or two runs give wrong/identical results. Teaches the reasoning to FIND the cause, then records each new case so the skill sharpens with use.
---

# anylogic-debug

A debugging **method**, not a fix-list. The fix-list (the Ledger, bottom) is memory; the value is
the **logic** above it. Follow the loop, reason to the ROOT, confirm before fixing, then record what
you learned so the next run is smarter.

## Prime directive: symptom ≠ cause
The error text tells you *where it surfaced*, rarely *why*. Never fix the symptom. Trace it one step
back at a time until you reach the thing that, if changed, makes the symptom impossible — that's the
root. A fix at the symptom re-breaks; a fix at the root holds.

## The loop (run every time)
1. **Read exactly.** Copy the literal error text + the *location* (which agent/block/event/experiment).
   Location is half the diagnosis — the same message means different things in `Main` vs an experiment.
2. **Classify.** (a) compile-time (won't build), (b) runtime crash (throws mid-run),
   (c) silent-logic (runs fine, output wrong or two arms identical). Class picks the heuristic below.
3. **Hypothesise the root**, not the symptom. State it in one sentence: "I believe X, because Y."
4. **Confirm with a cheap probe BEFORE editing.** Add a `traceln(...)` that prints the suspected
   variable/branch/scope. Run. If the probe doesn't match the hypothesis, the hypothesis is wrong —
   loop back to 3. *Never edit on a guess; a wrong fix hides the real cause.*
5. **Fix at the root, minimally.** Smallest change that removes the cause. Leave the probe until green.
6. **Verify the specific signal**, not "it ran." Name the number/behaviour that proves it (e.g. "the two
   arms now differ by 5pp", "planErr prints 0.209 vs 0.134"). Then remove the probe.
7. **Record** (see Self-improvement). Every novel error updates this file.

## Diagnostic heuristics (reason, don't pattern-match blindly)

**Two runs give IDENTICAL results when they shouldn't** → a parameter you *think* is varying isn't.
Ask: *where is that parameter actually set at run time?* In AnyLogic, an **experiment's Parameters
override the agent's default** — changing the checkbox on `Main` does nothing to a Parameter-Variation
run. Probe: print the parameter at t=0 in the actual run. Fix at the layer that really drives it.
→ Generalises: *when an input seems ignored, find the last place it's assigned before it's read.*

**Output is wrong but no error (silent logic)** → something is read BEFORE it's set, or set in the
wrong scope/order. Classic: a routing/decision variable set in the *On enter* of the deciding block,
but the engine evaluates the exit at *preview* (before On enter) → decision made on a stale value →
everything takes one path. Fix: set the decision **upstream** (prior block's On exit). Probe: print the
variable at the moment of the branch.
→ Generalises: *trace the read/write ORDER of the offending variable; the bug is almost always a
write that happens after the read.*

**"Duplicate local variable / duplicate method"** → new code was pasted alongside the old; two
definitions now collide. Don't rename — **find and delete the other definition.** Note branches
(`if/else`) each have their own scope, so the *same* local name in both is legal — the clash is a third
copy outside the braces, or a function you re-created that already existed.

**"X cannot be resolved"** → scope/reference mismatch. Inside an agent's own code, reference its
fields **bare** (`forecastDriven`); from another agent, go through the reference (`main.forecastDriven`).
Also check the symbol actually exists *on that agent* (right type, right owner). Probe: does it
autocomplete in that context?

**Runaway agents / "could not leave port" / population explosion** → suspect **block toggles and
rate-driving events before model logic.** e.g. Source "Forced pushing" pushes agents with nowhere to
go; a rate-setting event paired with a rate-field expression double-drives arrivals into the cap.
Check the block's checkboxes and any event that calls `set_rate()`/`inject()` first.

**Missing block/feature ("there's no Wait block")** → don't assume the reference name; AnyLogic's
idioms differ. Adapt to the actual palette (e.g. wait = `Delay` "Until stopDelay()" + `stopDelay()`).
→ Generalises: *verify the tool's real API/palette before coding against a remembered name.*

**A metric/number "looks wrong"** → do NOT defend it from memory or an earlier console print.
Re-derive it at the SOURCE (re-run the script, read the file), then report what it actually is — even
if it contradicts what you said. Units matter: state them (e.g. RMSE is an *error* in patients/week,
not a patient count).

## Self-improvement protocol (the "regenerating" part)
This skill must get better each use. After resolving any error:
1. **Append** a one-line entry to the Ledger: `symptom → root cause → fix → confirm-signal`.
2. If a root cause now appears **≥2 times** across entries, **promote** it: write (or sharpen) a
   Diagnostic Heuristic above, phrased as *reasoning* ("ask X; trace Y"), not a recipe. Then tag the
   Ledger lines it subsumes with `[→heuristic]`.
3. If a heuristic keeps resolving cases first-try, **move it higher** in the heuristics list (most
   predictive first). If one never fires, prune it.
4. Keep the Ledger to concrete, verified cases only. Delete anything later proven wrong (say so).
Result: the reasoning section grows sharper and shorter; the Ledger stays a thin, trustworthy index.

## Ledger (verified cases — newest at top; keep concrete)
- "model paused itself during iteration 2 … call finishSimulation()" in a Parameter-Variation run →
  the interactive `pauseAtStart` event (`getEngine().pause()`, added for the Simulation experiment's
  dashboard) also fires under Param-Variation and stalls its run loop → guard it with a boolean
  `interactiveMode` param, set FALSE in the experiment's Parameters. Tell-tale companion symptom: all
  stats identical and at t=0 values (coverage exactly 100, overtime/locum 0, cost = initial stock
  value) because each run aborts at t≈0. Confirm: stats show 30 samples with a real spread.
  (Watch for a 2nd case of "interactive/UI code breaks a batch experiment" → then promote to a heuristic.)
- P1 waited LONGER than P2 despite priority logic → specialty blocks had Task priority set, but
  `triage` block had priority 0 = FIFO; plus small P1 sample → set the same ternary priority on every
  queueing block; check EVERY block, not just one. [→heuristic: silent logic]
- `vaX cannot be resolved` on nav buttons (3× this project) → the View Area didn't exist yet or name
  case-mismatched → ALWAYS create the named View Area before the button that calls navigateTo().
- `DataSet(int, boolean) constructor undefined` → PLE lacks that constructor → use the palette
  **Data Set** element (or `new DataSet(365)`); palette element is the robust route.
- `itemName cannot be resolved or is not a field` → CSV loader only read numeric columns; the name
  was in `c[1]` unloaded → add a String field to the agent and load it. Open the CSV header first.
- `occupiedBeds cannot be resolved to a variable` → it's a FUNCTION; missing `()`. That exact error
  wording = function referenced as variable.
- Dashboard text shows raw code with quotes and `+` → the Text was static; the `=` (dynamic) toggle
  was never clicked. Code-as-text on screen = missed `=`.
- Two Reps30 arms identical → experiment's Parameter (Freeform Expression) overrode Main's default; both
  ran the same value → set the toggle in the *experiment* Parameters, run each value → arms diverge. [→heuristic: input seems ignored]
- Duplicate method `kpiLocumShare()` → function already existed on Main → deleted the re-created copy.
- Duplicate local `dBar`/`fcDaily` → old (s,S) code left in the event beside the new if/else branch →
  deleted the leftover; kept one block (branches have own scope). [→heuristic: duplicate]
- `confidence()` undefined on `StatisticsDiscrete` → method doesn't exist in PLE → compute CI manually
  `t*deviation()/sqrt(count())` (t=2.045 for 30 seeds).
- All patients discharged (wrong routing) → `dispo` set in disposition block's On enter, read at preview →
  set it UPSTREAM in arrival's On exit. [→heuristic: read-before-write / silent logic]
- "main cannot be resolved" inside a Main block action → used `main.` prefix in Main's own scope →
  use bare names. [→heuristic: cannot be resolved / scope]
- 50k-agent flood → `updateRate` event calling `set_rate()` while the rate field also had an expression →
  deleted the event, drove rate via `lambda(time())` field alone. [→heuristic: runaway agents]
- "agent could not leave port arrival.out" → Source **Forced pushing** was ON (not a resource issue) →
  unchecked it. [→heuristic: runaway agents / port]
- No "Wait" block in the palette → used `Delay` "Until stopDelay()" + `stopDelay()`. [→heuristic: missing block]
- lambda "missing argument" → rate/expression lambda needs its arg → added `double t`.
- rel_err naive beat ML at weekly aggregation → wrong granularity → compute rel_err DAILY vs a flat-mean
  baseline. [→heuristic: metric looks wrong / re-derive]
- Learning-curve RMSE doubted → re-ran train_forecaster.py at source; endpoints confirmed but the smooth
  2-point chart hid a COVID plateau → redrew with all 20 measured points. [→heuristic: metric looks wrong]
