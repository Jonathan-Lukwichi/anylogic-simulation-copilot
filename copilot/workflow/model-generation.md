# Model generation — build the AnyLogic model as a file, then run and verify it

> Build path B. Path A (the default everywhere) is `phase-1-6-build.md`: the co-pilot specifies and the user
> builds in the AnyLogic IDE. Path B is for Claude Code on a Windows PC with AnyLogic installed: the co-pilot
> generates the `.alp` itself, opens it, runs it and proves the result. Same intake, same verification standard.
> Tools: `../.claude/skills/anylogic-model-builder/` (commands below run from the repository root). Verified example: `examples/mini-ed-2d3d/` (2026-10-02).

Each step has a **checkpoint**: do not start the next step until it holds.

## G0 · Preconditions
- AnyLogic 8.9 installed with its example models; Python 3; PowerShell.
- The user has agreed to screen control and to screenshots of AnyLogic windows; private windows closed.
- **Checkpoint:** `scripts/al_run.ps1 status` runs and reports AnyLogic (running or not).

## G1 · Spec
- Real project: intake (the `simulation-welcome` skill) → confirmed brief. Demo: write the assumed spec in `brief.md`.
- The spec must give: arrivals (rate or interarrival), each step's time distribution, resources and counts,
  routing probabilities, the layout (rooms and sizes in metres), the KPIs to display, run length, time unit.
- Do the hand calculation now: utilisation ρ = λ·E[S]/c for every resource; every ρ < 1 (or the model is meant
  to overload). Example: Mini ED doctors 8/h × 23.3 min / 4 = 0.78.
- **Checkpoint:** `brief.md` written and (real project) confirmed by the user.

## G2 · Templates
- `python .claude/skills/anylogic-model-builder/scripts/alp_templates.py` once per machine and after every
  AnyLogic upgrade. It copies, from AnyLogic's own example models, one saved instance of every Process Modeling
  Library block, the colour table of every library 3D object used in an example, and the reference file header
  (Bank Office tutorial phase 4, AlpVersion 8.9.6, with its converter list).
- **Checkpoint:** the script lists the blocks you need and the 3D objects you plan to use.

## G3 · Generate
- Write `build_<model>.py` with `AlpModel` (copy `examples/mini-ed-2d3d/build_mini_ed.py`). Order: agent types →
  floors/walls/labels → nodes and attractors → 3D furniture → camera + 3D window → dashboard → parameters →
  blocks (only non-default settings) → connections → `write()`.
- Layout rules: 10 px = 1 m; floors `zh=1`, walls `zh=12` (1.2 m, so the camera sees inside); leave wall gaps where
  agents enter and leave; keep the visible dashboard inside the window frame (default 1100 × 580) and the
  flowchart below it.
- Movement: MoveTo with `straightMovement = true` between standalone nodes; add a path network only when the
  route matters (G4 applies to moving resources).
- **Checkpoint:** `write()` returns without error (well-formed XML, unique ids, 3D files copied).

## G4 · File checks
- `python .../verify_alp.py "<model>.alp"` → `OK`. It also catches absolute paths (G123) and unknown parameter
  names in hand-edited files.
- **Checkpoint:** OK printed.

## G5 · Open
- `.../al_run.ps1 open "<model>.alp"` — opens it **through Windows Explorer**, i.e. in the user's session.
  Starting `anylogic.exe` from the agent's shell makes every run hang without a window (G124).
- If the model is already open in AnyLogic, ask the user to close it (File → Exit) before regenerating: an open
  model and its `.autosave` hold the old version (G125). `write()` refuses when the autosave is newer.
- **Checkpoint:** a capture (`al_screen.ps1 snap <png> ide`) shows the model in the editor with no error dialog.

## G6 · Build and run
- The user presses F5, or `al_screen.ps1 keys "{F5}"` while AnyLogic is in front.
- `al_run.ps1 status`: *running* → go on. *WAITING FOR ITS WINDOW* → `al_run.ps1 window` (opens the model's local
  page in the default browser; the engine then starts). No model process → build failed: `al_run.ps1 log 80`, or
  capture the IDE and read the Problems view.
- **Checkpoint:** status shows *running* and the CPU time of the model process rises.

## G7 · Evidence
- `al_screen.ps1 snap <png> model` at least twice, some simulated hours apart (the second at a higher speed if
  needed). Read: the clock moves; counts grow; queues and utilisation are plausible against G1's hand numbers;
  branch shares match their probabilities (Mini ED: 37 of 146 admitted = 25 % vs 0.25 set).
- 3D: check the camera shows the layout and the figures; adjust camera X/Y/Z or rotations and regenerate.
- **Checkpoint:** two captures saved, the numbers written down, any gap from the hand estimate explained.

## G8 · Iterate
- Change the build script, never the `.alp` by hand (the script is the source). Close the model in AnyLogic,
  regenerate, repeat G4–G7.

## G9 · Record and hand over
- In the example/project folder: `build_<model>.py`, `brief.md`, `README.md` (how to rebuild, what was verified,
  the numbers, what was not verified), `evidence/` (2–3 images: editor, running early, running later).
- Stop the runs you started (`al_run.ps1 stop`); leave AnyLogic for the user to close.
- Report generated / built / ran separately, each with its evidence.

## Failure modes seen so far

| Symptom | Cause | Fix |
|---|---|---|
| F5 builds, nothing appears; AnyLogic log shows "Run model" | Model waits for its window: built-in browser could not start (AnyLogic launched from an agent shell) | `al_run.ps1 window`; next time open via Explorer (G124) |
| Request to the model's page "times out" in PowerShell | The page streams (chunked) — not an error | Use `curl.exe -v`; a `200 OK` header means the server is fine |
| AnyLogic offers to restore an automatically saved copy | `.alp.autosave` older than your regenerated file | Choose *Discard autosave* (G125) |
| `write()` refuses: autosave newer than the model | Model still open in AnyLogic | Close it in AnyLogic, then regenerate |
| `KeyError: unknown parameters` | Wrong parameter name for that block class | The message lists the valid names (from the template) |
| `KeyError: 3D object has no template` | That library object is used in no example | Pick another object from `alp_templates.py --show` |
| Verifier: absolute path | A data file opened by `C:/...` | Relative file name + *referenced from user code* (G123) |
