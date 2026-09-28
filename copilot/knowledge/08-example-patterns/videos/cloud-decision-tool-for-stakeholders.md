# Pattern card — Cloud decision tool for non-modeller stakeholders
- **Source:** AnyLogic video "Webinar | How Simulation-Driven Insights Strengthen Strategic Decision-Making" (https://youtu.be/UVppYf_O4H8) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Many non-technical users must test their own scenarios repeatedly, without an AnyLogic licence, the IDE, or seeing the model internals.

## Mechanism
- **The case:** a drive-thru restaurant model handed to franchise holders. Each franchisee edits a proposed week of staffing by day-part in Excel, uploads it, runs the model headless in a browser and reads the KPIs. Nobody sees the flowchart.
- **Phase-0 trigger:** the answer to "who acts on the result?" is *several non-modellers, repeatedly* (weekly rosters, seasonal plans, site-by-site use). In that case the deliverable is a tool, not a report, and inputs and outputs must be designed for it from the start: a lever that is not exposed cannot be used.
- **Lifecycle, not one-and-done:** when the business changes (a new product, a new site), the modeller updates and re-uploads the model, and users keep the same entry point. A Cloud repository also lets several modellers collaborate on the same models.

## Resources
n/a

## Key settings worth copying
- Export through the model's **Run Configuration**: pick the top-level agent, list the levers under **Inputs** (parameters of that agent) and the KPIs under **Outputs** (Analysis-palette elements such as Output, datasets and statistics). Only listed items appear in the Cloud UI.
- Table-shaped inputs (a roster by day-part, a forecast arrival curve) become a **file input** (Excel) that the model reads at startup. Cloud keeps uploaded files for reuse, and one workbook can act as both input and output (input sheet in, results sheet out).
- Match the Cloud experiment to the question:
  - Simulation: one run.
  - Parameter variation: with or without replications.
  - Monte Carlo 1st order: replications with fixed inputs.
  - **Monte Carlo 2nd order**: uncertain inputs sampled per iteration, optionally with replications each.
  - Optimization: with or without replications.
- Use Monte Carlo 2nd order when an input is itself uncertain. The webinar replaced one global app-ordering share with a random one, which tests whether the plan survives input uncertainty and not just run-to-run noise.
- Cloud stores every run's inputs and outputs. Sort the history by one output (e.g. most profitable configuration), filter by a threshold on another (e.g. cook time), then compare the winners. Results export to Excel or JSON.
- Before sharing, open the link in a private/incognito browser window to see exactly what an anonymous end user gets.

## KPIs instrumented
The intake card's KPIs exposed as Outputs, e.g. time in system by channel, kitchen time, staff utilisation, lost customers and profit. Label each with its units and replication count. Viewers can restyle charts (pie to bar) without changing results.

## Pitfalls
- With identical inputs, Cloud recalls the stored result instead of re-running (AnyLogic docs exempt stochastic multi-run experiments). Clicking Run again on a single run is not a new replication.
- Levers that are hard-coded or buried in a sub-agent cannot be exposed. Lift them to top-level parameters and pass them down before export.
- A user-edited Excel file drifts in format. Ship a template and validate it at startup, failing loudly rather than silently using defaults.
- Long-horizon models (the mine demo covered months to years of model time) belong in headless experiments. Animation explains; it does not decide.

## Reusable idea
Treat the model as a product: parameters are the user's knobs, a file is the user's plan, Outputs are the verdict, and the stored run history is the audit trail.

## When the co-pilot should use this
- Intake A2 names many or non-technical users, or the decision recurs.
- The user asks how a manager can "play with it" or how to share results.
- In the build plan: add a Run Configuration step and a validated input-file template before verification.
