# Mini ED 2D-3D — a generated AnyLogic model (verified example)

A small emergency department — arrivals, triage, treatment, admission or discharge — generated as an AnyLogic
model file by `build_mini_ed.py`, then opened and run in AnyLogic 8.9.10 PLE with a 2D floor plan, a 3D view and
a live dashboard. Spec and assumptions: `brief.md`. Procedure: `workflow/model-generation.md`.

## Rebuild it
```powershell
cd <repo>
python .claude/skills/anylogic-model-builder/scripts/alp_templates.py      # once per machine
python copilot/examples/mini-ed-2d3d/build_mini_ed.py                              # -> Documents\AnyLogic demos\Mini ED 2D-3D
python .claude/skills/anylogic-model-builder/scripts/verify_alp.py "$HOME\Documents\AnyLogic demos\Mini ED 2D-3D\Mini ED 2D-3D.alp"
.claude/skills/anylogic-model-builder/scripts/al_run.ps1 open "$HOME\Documents\AnyLogic demos\Mini ED 2D-3D\Mini ED 2D-3D.alp"
# press F5 in AnyLogic, then:
.claude/skills/anylogic-model-builder/scripts/al_run.ps1 status            # 'running', or use 'window' if it waits
```
Close the model in AnyLogic before regenerating (G125).

## What was verified (2026-10-02)
| Claim | Evidence |
|---|---|
| The generated file opens in AnyLogic 8.9.10 PLE | `evidence/2026-10-02_1-editor-opened-generated-model.png`: floor plan, 3D window, charts, flowchart, parameters |
| It builds | AnyLogic log: "Generate build sources 'Mini ED 2D-3D'", classes in `Mini ED 2D-3D_BUILD`, no build error |
| It runs, in 2D and 3D | `evidence/..._2-running-day1-0041.png` and `..._3-running-day1-1837.png`; thread dump: engine advancing |
| The logic matches the design | Day 1 18:37: 150 arrived, 37 admitted of 146 finished (25.3 % vs 0.25 set); nurses busy 0.54 (hand 0.51), doctors 0.80 (hand 0.78); average time in ED 40 min (hand 35–45) |
| The admission split is wired as intended | Generated Java: `conditionIsProbabilistic = true`, `probability = admitProbability`, `outT → walkToWard` |

Run conditions: AnyLogic had been started from the agent's shell, so the model waited for its window until
`http://127.0.0.1:<port>/` was opened in the browser (G124); the run itself was unaffected.

## Not yet verified
- The file produced by the current `build_mini_ed.py` (library version, 2026-10-02 evening) has the same agent
  types, shapes, connections, parameters and block settings as the verified file; only the flowchart spacing and
  the parameter order inside three block types differ. It has not itself been opened in AnyLogic yet.
- In the 3D view the staff figures are visible; the patient figures in 3D were not checked at close zoom.
- Camera position is a first guess (camera at X 315, Y 560, Z 280, tilt 38°).

## Files
`build_mini_ed.py` (the source of the model — change this, not the .alp) · `brief.md` · `evidence/`.
