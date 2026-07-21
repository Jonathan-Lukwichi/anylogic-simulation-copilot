# Pattern card — Air Defense System - Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** ABM (Agent-Based Modeling)
- **Problem it solves:** Establish the spatial scene and agent population for a 2D/3D air-defense scenario, placing defended buildings inside a protected zone before adding threat logic in later phases.

## Block chain
No process-flow chain (no Source → Sink). Instead: Main agent owns a continuous 2D/3D environment (500 × 500 model units, scale 10 m per unit) → a population of 10 Building agents is injected into a polygon node called `protectedArea` at model start → Building agents carry a 3D mesh (house.dae) and bidirectional agent-link collections so they can communicate with each other and with the Main agent at runtime. All movement uses continuous-space kinematics at a default speed of 10 m/s.

## Resources
- **Agent populations:** 10 Building agents (array-list collection, each placed randomly inside the `protectedArea` polygon node at initialization)
- **Agent links:** one bidirectional `connections` link collection per agent (capacity 2 links per agent by default)
- **Space:** continuous 2D/3D, 500 × 500 units, Moore neighborhood, no network auto-wiring (USER_DEF layout)
- No ResourcePools, schedules, or service capacities — this phase is scene setup only

## Key settings worth copying
- **Time unit:** Second — appropriate for fast-moving physical systems (projectiles, aircraft)
- **Space type:** CONTINUOUS with a 100 × 100 reference grid; scale ruler set to 100 m per 100 units, giving 1 unit = 1 m
- **Building replication count:** 10 (parameterisable integer) — easy to scale the target population up or down
- **Placement:** agents initialised to a named polygon node (`protectedArea`) rather than random absolute coordinates, so the defended zone can be repositioned without touching agent code
- **3D camera:** pre-configured perspective camera (elevation ~46°, azimuth ~−114°) giving a cinematic overhead-oblique view out of the box
- **Dataset sampling:** auto-collected every 1 second, keeping 100 samples — sets up time-series plots without extra code

## KPIs instrumented
- n/a (Phase 1 is scene construction only; KPIs such as buildings destroyed, intercept rate, and response time are introduced in later phases)

## Reusable idea
Separate scene construction from behavior logic by building Phase 1 as a pure spatial scaffold — define the environment dimensions, place named polygon nodes for each zone (protected area, launch zone, etc.), populate agent collections with a single replication parameter, and wire up agent-link collections — so that Phase 2 onwards can layer statecharts and threat logic onto an already-validated visual layout without reworking the spatial setup.
