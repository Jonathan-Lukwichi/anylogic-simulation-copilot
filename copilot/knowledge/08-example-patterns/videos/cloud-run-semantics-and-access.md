# Pattern card — AnyLogic Cloud run semantics: nested-KPI Outputs, what is computed and cached, versions and access roles
- **Source:** AnyLogic video "AnyLogic Cloud" (https://youtu.be/F93iENzUcWc) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Getting correct numbers out of a Cloud model, rather than animation artefacts or a single stored sample, and handing it to a client with the right rights.

## Mechanism
- **Scope.** `videos/cloud-decision-tool-for-stakeholders.md` already covers the Run Configuration basics, file inputs, the list of experiment types and the "identical inputs are recalled" caveat. This card adds the rest of the video's demo:
  - one distributor serves retailers by truck;
  - inputs: Fleet size, Demand;
  - outputs: order backlog, fleet utilisation, delivery-time distribution.
- **Nested KPI → top-level Output.** Delivery time was measured by a `TimeMeasureEnd` inside the Distributor agent, and Cloud cannot list it from there.
  - Fix: drop an `Output` on Main with Value `distributor.timeMeasureEnd.distribution.mean()`, add it under Outputs, and re-export.
- **Play ≠ Run.** Play animates using the inputs but produces no outputs. Only Run executes the experiment and fills the Outputs pane.
- **Result store.** Outputs are stored per model version and shared by every experiment of that version.
  - Discarding input edits brings back the stored run instantly.
  - After a re-upload (a new version), runs start over.
- **Monte Carlo 1st order grows incrementally.**
  - Raising 50 replications to 75 ran only replications 51–75.
  - Replications run in parallel on remote nodes.
  - The distribution is built from scalar Output values.
- **Scenarios.** Copy an experiment, edit its inputs and click *Save inputs* to make them that copy's defaults. *Compare* overlays the selected experiments on one dashboard.
- **Versions.** Exporting while the existing Cloud model is selected adds a version. The Versions screen deletes versions and downloads a version's source files.
- **Access.**
  - Invite by e-mail as **User**: can change inputs and run existing experiments, but cannot change the model.
  - Invite as **Developer**: full ownership.
  - **Publish** lists the model publicly. Anyone can then *Copy to my models* and gets full control of that copy.

## Resources
n/a

## Key settings worth copying
- **`Output` element** (Help): holds one scalar, either a Java primitive or a measurable type with a unit (no Object). Its *Calculated* property is one of:
  - *On simulation end* (default);
  - *At model time*;
  - *At calendar date*;
  - *User control*: call `update_<name>()`, or `update_<name>(value)` to set the value directly.
- **Run Configuration Inputs** (Help) accept only two kinds of element:
  - static parameters of the top-level agent, typed int, double, boolean, String, Date or a unit type;
  - files that the model references, that sit in the model folder and that use a relative path. Any other file is greyed out and blocks the export.
- **Run Configuration Outputs** accept any Analysis-palette element on the top-level agent, plus files. Files work as outputs only in single-run Simulation experiments. The labels set here are what users and the API see.
- **Other properties:** Top-level agent; Maximum available memory (heap for the model and the built-in DB); Model time stop; Animation stop and execution mode (virtual time, or real time with scale); zoom/pan and developer-panel toggles.
- **Tiers** (Cloud 2.6.x Help, 2025–26):
  - A subscription lifts the memory, output-file and run-time limits, allows external resources such as databases, and opens the full API.
  - The Cloud optimizer is the genetic engine only. Without a subscription, optimization stops at 5 min, and the best run may not reproduce exactly.
- **2026 naming.** The SaaS now appears as **AnyLogic Online** (anylogic.online), which also edits models in the browser. Private Cloud runs models but cannot edit them; its editions allow 16 (Lite), 64 (Pro) or unlimited (Enterprise) parallel runs. Check UI labels against current Help.

## KPIs instrumented
Demo: order backlog, fleet utilisation, delivery-time histogram, and the `deliveryTimeMean` Output. Going from 30 to 40 trucks lowered both utilisation and mean delivery time, but each figure is a single run.

## Pitfalls
- Reading outputs after Play: there are none.
- Choosing 30 vs 40 trucks from two single-run experiments, as the demo does. Each is one stored sample of a stochastic model. Use Monte Carlo 1st order or Variation with replications and compare the distributions.
- A KPI inside a sub-agent stays invisible until a top-level Output surfaces it. For a population, pool the samples into one top-level statistics object (`add()`); averaging per-node means ignores volume.
- An Output on *On simulation end* shows nothing mid-run. For a live figure, use *User control* and call `update_<name>()` from a cyclic event or a block action.
- A Dynamic parameter, or one typed as an option list, Object or collection, cannot be an input (inferred from the allowed types). Expose an int or String code instead.
- Publishing a client or thesis model lets anyone copy it with full control. Invite by role instead.
- Long runs, database-backed models and API use need a subscription or Private Cloud. Check the tier before promising a Cloud deliverable.

## Reusable idea
Treat Cloud as a store keyed by (version, inputs) → outputs. Make every decision KPI a scalar top-level Output, take variability from replicated experiment types, and give clients the User role.

## When the co-pilot should use this
- Build steps 5–6, whenever the deliverable is a Cloud model (after `videos/cloud-decision-tool-for-stakeholders.md`).
- A user reports blank, blurred or unchanging Cloud outputs.
- A user asks how to share a model with a client, supervisor or examiner.
- Before recommending Cloud for heavy replication, check the account tier.
