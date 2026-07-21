# ADR-0001: Standardize on AnyLogic / Simio for simulation; do not default to FlexSim

- **Status:** accepted
- **Date:** 2026-06-23

## Context
The platform's Simulation (S5) and Digital Twin (S6) service lines need a primary
simulation toolset, and a venture's tooling bet shapes hiring, training, partnerships,
and client credibility — costly to switch later. The original IDEA doc named AnyLogic
and FlexSim interchangeably. The fact-checked market research found that real South
African digital-twin/simulation deployments use **Simio, SimMine, and AnyLogic** (e.g.
SET/Letseng on Simio; TUT and University of Pretoria teach/use AnyLogic), while
**FlexSim has no established SA footprint** in the surviving evidence.

## Decision
Standardize on **AnyLogic** (and **Simio** where discrete-event/mining fits) as the
primary simulation/digital-twin tooling. Treat **Python (SimPy + OR-Tools)** as the
embeddable engine for the productized SaaS. Do **not** default to FlexSim.

## Consequences
- Easier: aligns with the local talent pool (Stellenbosch/TUT/UP), local case-study
  precedent, and partnership/hiring; AnyLogic's multi-method (DES + system dynamics +
  agent-based) matches the ML + system-dynamics + digital-twin thesis.
- Harder: if a future client mandates FlexSim, we take it on as an exception, not the
  default; we forgo FlexSim's 3D material-handling strengths for bespoke demos.
- Committed: glossary, IDEA, and BUSINESS-PROPOSAL all reflect AnyLogic/Simio, not FlexSim.
