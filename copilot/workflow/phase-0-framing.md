# Phase 0 — Framing & approach selection (run this FIRST)

The most important gate. Never suggest blocks before this is done.

## Intake questions
1. What decision/question must the model answer? (e.g. "Will dynamic staffing cut ED wait time?")
2. Unit of analysis? (patients, machines, vehicles, orders...)
3. What drives the behaviour? Use the chooser below.
4. Abstraction level? (high/aggregate vs low/individual)
5. What data exist? (arrival logs, service times, layouts)
6. KPIs? (wait time, utilisation, throughput, cost, service level)

## Approach chooser
- **Flow of entities through limited resources, event-ordered** -> Discrete-Event (DES)
- **Many autonomous individuals with their own state/decisions and interactions** -> Agent-Based (ABM)
- **Aggregate stocks, continuous feedback loops, high abstraction** -> System Dynamics (SD)
- **A combination (e.g. DES process inside an agent population)** -> Hybrid / multimethod

## Output of Phase 0
A one-paragraph recommendation: chosen approach + justification + abstraction level + the KPIs,
confirmed with the user. Reference: knowledge/00-method-selection (Borshchev & Filippov).
