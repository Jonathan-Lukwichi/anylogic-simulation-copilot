---
name: anylogic-sd
description: System Dynamics and paradigm choice in AnyLogic - when stocks/flows beat DES/ABM, how to build and couple SD with agent models, and the Phase-0 decision method for picking DES vs ABM vs SD vs hybrid. Use before starting any simulation, or when a model only needs aggregates.
---

# anylogic-sd

System Dynamics (SD) models AGGREGATES: continuous stocks changed by flows, feedback loops, no
individuals. In AnyLogic it's the stock-and-flow palette. This skill covers when to use it, how,
and — most valuable — the Phase-0 paradigm decision that should precede ANY build.

## Phase 0 — choose the paradigm BEFORE building (the decision that matters most)
Ask, in order:
1. **Do individuals need identity/state?** (this nurse's fatigue, this item's stock)
   → yes: **ABM** for those actors.
2. **Do entities queue through shared process steps with resources?**
   → yes: **DES** for that flow.
3. **Is the question about aggregate accumulation & feedback** (bed-stock vs demand growth,
   epidemic dynamics, workforce attrition pipelines, budget flows over years)?
   → yes: **SD**.
4. **Mixed answers → hybrid** (the common case; our hospital = DES flow + ABM actors, no SD).
Honest rule: if you track individuals anywhere, don't force SD there — and if only totals matter,
don't burn effort simulating individuals. Choose per SUBSYSTEM, not per model.

## SD building blocks (AnyLogic System Dynamics palette)
- **Stock** — an accumulation (Beds Occupied, Backlog, Staff Pool). Has an initial value.
- **Flow** — rate in/out of stocks (admissions/day, attrition/month). AnyLogic integrates
  continuously; you write the rate equations.
- **Auxiliary/Parameter** — computed quantities and constants the flows read.
- **Links** — dependency arrows; AnyLogic enforces that equations only use linked inputs.
- Time-unit discipline is critical: a flow is "per model time unit" — with hours as the unit, a
  "per day" rate must be divided by 24. Wrong scaling here is the classic silent SD bug.

## A minimal useful SD pattern (capacity strain)
```
Stock:  WaitingBacklog     init 0
Flow in:  demandRate       = arrivalsPerDay/24 (per hour)
Flow out: serviceRate      = min(capacityPerHour, WaitingBacklog>0 ? capacityPerHour : demandRate)
Aux:    strain             = WaitingBacklog / normalBacklog
```
Feedback: strain can feed staff burnout or diversion decisions — loops are the point of SD; if
your diagram has no feedback loop, plain variables + events are simpler and clearer.

## Coupling SD with DES/ABM (hybrid patterns)
- **ABM/DES → SD**: write agent aggregates into SD auxiliaries each cycle
  (e.g. flow `admissionRate = admittedSink.countLastHour()`).
- **SD → ABM/DES**: read stock levels to set rates/decisions
  (e.g. Source rate scaled by an SD "community illness" stock).
- Keep couplings in named functions on Main; one audit point.

## When SD is the WRONG tool (honest boundaries)
- Queue waiting-time questions (needs DES — SD has no queue discipline).
- Individual heterogeneity effects (needs ABM — SD averages them away).
- Short horizons with few events — discrete logic is clearer than integrating flows.
- Our hospital twin correctly used NO SD: every question was flow-through-queues or
  per-individual state. Being able to SAY why a paradigm was not used is part of a defensible
  methods chapter.

## Deliverable discipline (any paradigm)
State in the write-up: chosen paradigm(s) per subsystem, the Phase-0 reasoning, time unit,
run length, replication count, and warm-up policy. Reviewers probe paradigm choice first.
