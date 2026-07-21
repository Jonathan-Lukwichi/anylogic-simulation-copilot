---
name: anylogic-3d
description: 3D modelling and animation in AnyLogic - the 3D Window, built-in 3D object library, agent 3D presentations, space markup shared with 2D, cameras, scale, walls, and the minimal-3D recipe that avoids the multi-day trap. Use when adding a 3D view to an existing model.
---

# anylogic-3d

Rule zero: **3D is not a different model.** It is the SAME logic and the SAME space markup,
re-rendered in perspective through a 3D Window with 3D shapes instead of flat ones. Build and
verify everything in 2D first (`anylogic-2d`); 3D is a presentation layer added at the end.

## The four ingredients
1. **3D Window** (Presentation palette): the viewport. Drop it on Main, size it; at runtime it
   renders all 3D-capable elements. Orbit = drag, zoom = wheel, pan = right-drag.
2. **Space markup with height**: the same Point Nodes / Paths / Rectangular Nodes used for 2D
   agent locations position agents in 3D too — one markup layer serves both views.
3. **3D objects** (3D Objects palette): ready-made people, beds, furniture, vehicles, and
   primitives (Box, Cylinder, Cone, Sphere) for walls/counters. Drag onto the canvas; they exist
   at (X,Y) with a Z/height. No external files needed for a credible scene.
4. **Agent 3D presentation**: open the agent type, delete/keep its 2D shape, add a 3D object
   (e.g. Person) at the agent's origin. Agents then render as that object wherever the process
   blocks place them (Agent location nodes). Dynamic colour works on 3D shapes too.

## Minimal-3D recipe (half a day, 80% of the wow)
1. Lay out Point Nodes per stage (arrival, triage, each specialty, wards, exits) + Paths between.
2. Set each block's Agent location to its node (identical to the 2D dot recipe).
3. Patient agent → 3D Person object; optionally colour by acuity.
4. Drop a 3D Window + a **Camera** aimed at the scene (set the camera as the window's default).
5. A few props only: beds in wards (Bed object), a triage counter (Box primitive). STOP THERE.
Deliverable: patients walking node-to-node through a schematic ED in 3D, orbit-able, demo-ready.

## Scale, cameras, navigation
- **Scale element** (a ruler on the canvas) defines metres-per-pixel — set it ONCE early; resizing
  later distorts every 3D object's proportions.
- Multiple **Camera** elements = saved viewpoints; switch at runtime:
  `window3d.setCamera(camera2, true);` on buttons for guided tours.
- The nav-bar/tab pattern from 2D still applies — a "3D" tab button can jump to the region holding
  the 3D Window (`va3D.navigateTo();`).

## Walls & buildings (know the cost before starting)
- Walls: Pedestrian palette **Wall / Rectangular Wall / Circular Wall** (render in 3D with height),
  or Box primitives. A full floor plan means placing every wall by hand — this is the multi-day
  trap. A flagship-demo look (AnyLogic's Trauma Center) is weeks of specialist work.
- Honest default for research models: schematic zones + people + a handful of props. Architectural
  fidelity adds zero analytical value; say "3D visualisation is schematic" in the write-up.

## Performance & pitfalls
- Hundreds of detailed 3D objects slow the frame rate; keep populations' 3D shapes simple
  (Person, not high-poly imports). Turn the 3D window off (or don't open that view) for batch
  experiments — rendering is pure overhead in Parameter Variation runs.
- Imported models (.obj/.3ds/.dae) work via the 3D Object element but bring scale/orientation
  fiddling; prefer built-ins unless a specific asset truly matters.
- Agents stacking on one point → add Attractors in the node, or use Paths so they travel visibly.
- Z-order confusion (objects buried in the floor) → check the object's Z and the node's height.
- If the 3D view is empty: the 3D Window shows only elements at the same level (Main), and only
  3D-capable ones — plain 2D Rectangles/Text do not appear in 3D.

## Decision rule (from the Steve Biko project)
2D zones + coloured dots answered every "show the flow" need more clearly than 3D would, at ~10%
of the effort. Choose 3D only for stakeholder-facing wow with time budgeted; never for analysis.
