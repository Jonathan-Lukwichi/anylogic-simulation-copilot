# Recipe — auto-generate pattern cards with Claude Code

Goal: turn AnyLogic's local example models into distilled pattern cards in
`knowledge/08-example-patterns/`, without copying their files verbatim.

## Why this works
AnyLogic model files are plain XML (.alp) or fragmented XML + .java (.alpx). Claude Code reads
local files directly, so it can parse a model's structure, parameters, and embedded Java —
AnyLogic does not need to be running, and no app-to-app integration is required.

## One-time setup
1. Locate the AnyLogic examples folder (inside the installation directory), OR open an example
   in AnyLogic and use File > Save As into a working folder, e.g. `./_anylogic-examples/`.
   Keep that folder OUTSIDE this repo (it holds AnyLogic's copyrighted files).
2. Open this kit folder in VS Code with Claude Code.

## Prompt to give Claude Code
> Read the AnyLogic model files in `<path-to-examples>` (they are XML for .alp, or XML + .java
> inside the `_alp` folder for .alpx). For each model, identify the paradigm, the block chain,
> the resources, the key settings, and the KPIs. When you are unsure what an element or property
> means, fetch the relevant page from https://anylogic.help/ to interpret it. Then, using
> `templates/pattern-card-template.md`, write ONE distilled card per model into
> `knowledge/08-example-patterns/`, in your own words. Do NOT copy the model's XML or Java
> verbatim — summarise. Start with the Healthcare and Supply Chain examples.

## Guardrails
- Cards are original summaries, not copies (IP — see the category README).
- Claude Code reads/extracts; it does not run models or edit the AnyLogic GUI.
- Pair local reading with live `anylogic.help` fetches to interpret AnyLogic's schema correctly.

## Refresh
Re-run after AnyLogic updates or when you add new reference models. Log additions in SOURCES.md.
