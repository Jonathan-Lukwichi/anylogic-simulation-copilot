---
name: anylogic-model-builder
description: Generate a complete AnyLogic model file (.alp) — process flowchart, 2D floor plan, 3D view, dashboard and charts — from a written specification, then open, run and check it in AnyLogic on this Windows PC with evidence (screenshots, logs, thread dumps). Use when the user asks Claude Code to build, generate, run, demonstrate or check an AnyLogic simulation on their own machine (e.g. "build me a 2D/3D model", "make it run", "show me it working"). Not for chat-only environments, and not a replacement for the intake (`simulation-welcome`) on real projects.
---

# AnyLogic model builder (generate → open → run → verify)

The full procedure, with checkpoints, is `copilot/workflow/model-generation.md`. This file is the operating summary.
Verified end to end on 2026-10-02 with `copilot/examples/mini-ed-2d3d/` (AnyLogic 8.9.10 PLE): the generated file
opened, built and ran in 2D and 3D; a simulated day matched the design within chance.

## Before you start

- **This PC only**: needs AnyLogic 8.9 installed (`C:\Program Files\AnyLogic 8*`) and its example models.
- **Consent**: screen control and screenshots need the user's go-ahead. Captures are of AnyLogic windows only;
  ask the user to close anything private anyway.
- **Real project?** Run the intake first (the `simulation-welcome` skill). A demo may use a stated, assumed spec — write it
  down (`brief.md`) before building.
- **Never edit a user's model in place.** Generate into a new folder; for existing models work on a copy and keep
  a change log next to the model.

## Steps

1. **Templates (once per machine / AnyLogic version):**
   `python scripts/alp_templates.py` → `.cache/templates.json` (35 Process Modeling Library block types, ~270
   3D objects, the reference file header). Git-ignored: the fragments come from AnyLogic's own files.
2. **Write the model as a Python script** using `scripts/alp_builder.py` (`AlpModel`): agent types with 3D
   figures, parameters, blocks with only the non-default settings, connections, floors/walls/labels, nodes and
   attractors, 3D furniture, camera + 3D window, dynamic texts, charts. Copy `copilot/examples/mini-ed-2d3d/build_mini_ed.py`
   as the starting point. Unknown block parameters or 3D objects raise an error naming the valid ones.
3. **File checks:** `python scripts/verify_alp.py "<model>.alp"` — must print `OK`.
4. **Open through Explorer:** `scripts/al_run.ps1 open "<model>.alp"`. Never start `anylogic.exe` from the
   agent's shell (G124). If AnyLogic is already open with the model, ask the user to close it first (G125).
5. **Run:** the user presses **F5**, or `scripts/al_screen.ps1 keys "{F5}"` while AnyLogic is in front.
6. **Check the run:** `scripts/al_run.ps1 status` — each model shows *running* or *WAITING FOR ITS WINDOW*.
   If waiting: `scripts/al_run.ps1 window` opens `http://127.0.0.1:<port>/` in the user's browser and the model
   starts. Build problems: `scripts/al_run.ps1 log 60`.
7. **Evidence:** `scripts/al_screen.ps1 snap <png> model` (the running model; browser tab strip cropped) or
   `... snap <png> ide` (the editor). Read the image; compare the KPIs with what the design predicts
   (utilisation ≈ arrival rate × service time ÷ servers; branch shares ≈ their probabilities).
8. **Record:** save the build script, `brief.md`, a README with the verified numbers and 2–3 evidence images in
   the example/project folder; log what changed. Stop runs you started: `scripts/al_run.ps1 stop`.

## Rules that came from real failures

- **Claim only what you saw.** "Built" = AnyLogic opened it and the log shows no build error; "runs" = a capture or
  thread dump shows the engine advancing. Say which.
- **A run that shows nothing is usually waiting for its window** (`Experiment.waitFrontend` in the thread dump),
  not broken model logic — G124.
- **Generated files use the reference model's format version** (Bank Office tutorial, AlpVersion 8.9.6, with its
  converter list); AnyLogic 8.9.10 upgrades them on open. Do not mix a newer header with older XML.
- **Walking without paths:** MoveTo with `straightMovement = true` moves agents straight between standalone
  nodes; add a path network only when routing matters.
- **Coordinates:** 10 px = 1 m (default scale); Z and wall heights in the same pixels (ZHeight 12 = 1.2 m).
- **Safety:** `al_screen.ps1` acts only while AnyLogic is the foreground window — the user can stop it by clicking
  anything else. Windows may refuse to bring AnyLogic to the front while the user types; capture by handle
  (`snap`) instead of fighting for focus.

## Files

| File | Purpose |
|---|---|
| `scripts/alp_templates.py` | Build the template cache from the local AnyLogic install |
| `scripts/alp_builder.py` | `AlpModel`: blocks, connectors, parameters, markup, 3D, charts, write + checks |
| `scripts/verify_alp.py` | File checks before opening (ids, connectors, parameter names, resources, absolute paths) |
| `scripts/al_run.ps1` | `open` via Explorer, `status`, `window` (unblock a waiting run), `log`, `stop` |
| `scripts/al_screen.ps1` | `snap` (capture by handle), `info`, `front`, `click`/`drag`/`keys` (AnyLogic-only) |
| `../../../copilot/examples/mini-ed-2d3d/` | Verified example: spec, build script, evidence |
