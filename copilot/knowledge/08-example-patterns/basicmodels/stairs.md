# Pattern card — Stairs
- **Source:** AnyLogic example model "Stairs" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Pedestrian Library)
- **Problem it solves:** Let pedestrians walk up a staircase from one floor to another — logically changing level and visibly climbing in 3D — with markup rather than a dedicated stairs object.

## Block chain
`PedSource` (200 per hour at an entry line on the lower level, comfortable speed 0.5 m/s) → `PedChangeLevel` (*Exit line
on current level* `exitLowerGround`, *Entry line on new level* `enterUpperGround`) → `PedGoTo` (to the exit line on the
upper level) → `PedSink`.

## Resources
n/a. Markup: two levels (`lowerGround`, `upperGround`), walkable areas on each, a stairs node, and two target lines.

## Key settings worth copying
- **The stair flight is a sloped rectangular node** on the lower level (Help 8.9.10, *Modeling stairs*, *Rectangular
  node*): *Slope for pedestrians* ticked; *Define slope as* = angle (*Vertical angle*) or **guiding line** with **dZ = the
  height between the levels in pixels** (here 100 px over the node's 250 px length). Point the slope line in the
  direction of rising Z. The slope affects pedestrian movement only (the same setting as in the Sloped Area example).
- **Changing level:** one target line on the lower level at the top edge of the stair node, and a second target line on
  the upper level lying exactly on top of it; `PedChangeLevel` goes from the first to the second, placed just before the
  first block that works on the new level.
- **One-level alternative:** keep a single level and just the sloped node — pedestrians climb in Z but stay logically on
  the same level (no PedChangeLevel needed).
- **3D steps are drawn separately:** one rectangle replicated 25 times with X and Z computed from `index` (each step
  shifted by its depth and by level height ÷ number of steps). The logic ignores this drawing.
- A node's *Speed restriction* (*Maximum speed*) can model slower walking on the stairs; the demo instead lowers every
  pedestrian's comfortable speed.
- Pedestrian look: the pedestrian type shows one of several 3D figures chosen at random in On startup
  (`setAnimation(index)` toggles shape visibility and colours the 2D marker).

## KPIs instrumented
n/a. Useful: flow over the stairs (PedFlowStatistics on a line), density on the stair node, travel time floor to floor.

## Pitfalls
- The two target lines must coincide in plan and each must lie on its own level; a mismatch makes pedestrians jump or
  stall at the level change.
- dZ is entered in **pixels**; keep it equal to the difference between the level Z values, or pedestrians arrive above
  or below the upper floor *(same unit trap as G25 for lifts)*.
- The stair node's slope and the 3D step drawing are independent — edit both when the geometry changes.

## Reusable idea
Treat stairs as three pieces: a sloped walkable node (geometry), a pair of coincident target lines with PedChangeLevel
(logic), and replicated steps (picture). Ramps, escalator approaches and mezzanine steps follow the same recipe.

## When the co-pilot should use this
Stations, stadiums, offices and evacuation models with floors joined by stairs; questions on how pedestrians change
level. Related: `../models/evacuation.md` (multi-floor pedestrians), `../videos/multi-level-facility-lift-landings.md`
(lifts cannot carry pedestrians; Elevator markup or PedChangeLevel), `../bigbook/replicated-shapes-and-group-pivots.md`.
