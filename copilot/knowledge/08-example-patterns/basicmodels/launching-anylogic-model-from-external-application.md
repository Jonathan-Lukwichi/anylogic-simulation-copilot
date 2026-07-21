# Pattern card — Launching AnyLogic Model from External Application
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Shows how to programmatically launch and control an AnyLogic simulation from a Java application outside the AnyLogic IDE.

## Block chain
No process-flow library blocks are used. The model itself is minimal — its value lies in the export and launch mechanism. The model is exported as a standalone application JAR, then a custom Java entry-point class (`MyApplication`) replaces the default `Simulation` launcher class. The external application instantiates the engine, sets up the experiment, and drives the run programmatically. The bat/sh/cmd script is edited to reference `MyApplication` instead of the default class.

## Resources
n/a

## Key settings worth copying
- Time unit: **Minute**
- Export target: standalone application (File → Export Model)
- Launcher swap: change the main class in the generated run script from `<modelname>.Simulation` to `<modelname>.MyApplication`
- The custom `MyApplication` class calls `EngineSettings`, creates the `Simulation` experiment object, and calls `run()` — all via the AnyLogic Engine API

## KPIs instrumented
n/a — the pattern is about integration, not metrics collection

## Reusable idea
Export the model as a standalone JAR and replace the default launcher with your own Java class to embed or automate an AnyLogic simulation inside a larger software system (batch pipelines, optimisation loops, or enterprise dashboards) without needing the AnyLogic IDE at runtime.
