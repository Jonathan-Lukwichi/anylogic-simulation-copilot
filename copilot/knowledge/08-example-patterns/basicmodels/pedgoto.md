# Pattern card — PedGoTo
- **Source:** AnyLogic example model "PedGoTo" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Choose how pedestrians find their way — automatic path-finding to a target, or following a drawn route — and know when each is appropriate.

## Block chain
Two parallel flows at 2000 peds/h each: `PedSource` → `PedGoTo` *reachTarget* (mode **Reach target**, target line) → `PedSink`; and `PedSource` → `PedGoTo` *followRoute* (mode **Follow route**, `route = path`, a Pathway drawn through the scene) → `PedGoTo` to the exit line → `PedSink`.

## Resources
n/a

## Key settings worth copying
- `mode = MODE_REACH_TARGET` (default): the library computes the path on the current level to a target line, area node (rectangular/polygonal) or point (x, y).
- `mode = MODE_FOLLOW_ROUTE`: pedestrians walk along a **Pathway** to its end; chain a second `PedGoTo` (reach target) from the route's end to the real destination.
- Help's judgement: with many walls or a maze-like layout, automatic path calculation can take a lot of time; draw routes and use *Follow route* instead.
- Per-pedestrian animation: a random 3D figure and a colour picked in the pedestrian agent (`setAnimation()`), with a `poses` array for the walking animation.

## KPIs instrumented
Visual only (2D/3D views, several cameras).

## Pitfalls
- *Follow route* ends at the end of the pathway, not at a target — without a following reach-target step pedestrians stop there.
- Paths are found within the current level only; moving between levels needs a level-change element (stairs, escalator, elevator).

## Reusable idea
Use automatic targeting for open halls and drawn pathways for corridors, one-way circulation, queuing lanes or large wall-heavy layouts where path-finding cost matters.

## When the co-pilot should use this
Pedestrian models that run slowly in complex geometry, or that need prescribed walking lines (museum routes, one-way systems, evacuation routes).
