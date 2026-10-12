# Pattern card — 3D beyond Z-order: what reaches the scene, tilting with groups, and cameras and lights that ride on agents
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 14 "3D animation" — distilled, original wording
- **Paradigm:** Method (3D presentation; any paradigm)
- **Problem it solves:** 3D shapes that do not appear or cannot stand upright, labels that flicker, a view that should follow a moving agent, and lights that recolour, darken or overload the scene.

## Mechanism
Checked against Help 8.9.10 (*Group*, *Curve*, *Rounded rectangle*, *3D window*, *Camera*, *Light*, *3D object*) and the 8.9.10 engine jar. It builds on `videos/3d-scene-z-order-and-lighting.md` (Z / Z-Height, floor slabs, default lights, navigation types, far clipping) and does not repeat it.
1. **What reaches 3D.** A shape's *Show in* decides whether it appears. Mappings:
   - a Rectangle becomes a box and an Oval a cylinder. Z is the bottom and Z-Height the vertical size; the editor's *Height* is the Y depth;
   - lines and arcs take `dZ`, the rise from start to end; a polyline takes Z per point;
   - text and images are zero-thickness sheets, visible from above and below;
   - curves, rounded rectangles and icon shapes are 2D-only (Help).

   In 8.9.10 a group shown in 3D may not contain 2D-only members: the Problems view reports an error (Help *Group*). The Big Book's "they just vanish" (p. 8) is outdated.
2. **Colours in 3D.** Line colour paints the side walls, inside and out; fill colour paints the body. A polyline or arc whose points differ in Z cannot be filled; only flat outlines fill (Big Book pp. 6–7).
3. **Coplanar faces render garbled.** Lift the top item a fraction: text at Z 2.1 on a sign whose top is at 2, a road at Z 0.1 over the ground (pp. 7, 9, 24). The same rule from ch. 12 is already proposed for the 3D card by batch book-2.
4. **Tilting needs a group.** A single shape turns only about Z (*Rotation Z* in 3D). Groups add **Rotation X** and **Rotation Y**, in radians. They are the only way to stand a flat drawing up:
   - draw the sign lying on the XY plane and group it;
   - move the group origin to the hinge line (the *Select Group Contents* technique in `bigbook/replicated-shapes-and-group-pivots.md`);
   - set Rotation X = `-PI/2` (pp. 8–9).

   Member Z values count from the group's Z. Lights and cameras can also be group members (Help *Group*). Whether they turn with a rotated group is untested; they at least move with it.
5. **Embedded agents are offset by their presentation.** The embedded presentation's X, Y and Z are added to everything the agent draws. A plane sent to (−100, 0, 100) appears at (100, 100, 150) when its presentation sits at (200, 100, 50). To make a whole population fly, set that Z (p. 12).
6. **Cameras on agents.** A Camera drawn in an agent type exists for every agent and moves with it. Switch a window at runtime (Help *3D window*):
   - `window3d.setCamera(plane.camera, true)` follows the agent;
   - `window3d.setCamera(camera, false, 500)` jumps to a static view with a 500 ms smooth transition. The time is real milliseconds, not model time.
   - Follow mode allows only *Rotation only* or *None*; a request for more falls back to None.
   - After leaving follow mode, restore free movement with `window3d.setNavigationMode(WINDOW_3D_NAVIGATION_FULL)`.
7. **Lights.**
   - Light colour filters object colour channel by channel. White or grey light keeps natural colours. A pure red light hides a pure blue object and turns purple dark red (p. 21; Help).
   - Point and spot lights fade by `1 / (kC + kL·d + kQ·d²)`; the property sheet exposes the constant and linear terms (Help).
   - A spot's *Cut off angle* is the half-angle of the cone, 0–90°. *Drop off rate* 0 gives an even cone.
   - A Light in an agent type moves with each agent, e.g. a car headlight. *Visible on upper agent* makes it shine in the container's scene (Help).

## Resources
n/a

## Key settings worth copying
- **Navigation constants (8.9.10 engine):** `WINDOW_3D_NAVIGATION_FULL`, `_LIMITED_TO_Z_ABOVE_ZERO`, `_ROTATION_ONLY`, `_NONE`. Agent code can use them unqualified. The Help's short names need the class prefix: `ShapeWindow3D.NAVIGATION_FULL`. Plain `NAVIGATION_FULL` is not a constant an agent inherits. The 8.9.10 examples use both prefixed and unprefixed forms *(checked in the engine jar)*.
- **Per-window default views.** Windows without a camera all open on the same view. Give each window its own Camera to start from different viewpoints (p. 15).
- **Scene settings are shared.** *Background*, *Grid color* and *Skybox* apply to every 3D window of that agent type. The grid lies on Z = 0 with 100 px spacing (Help; p. 12).
- **Imported objects.** *Internal lights* is Off, Illuminate the object, or Illuminate globally. *Ignore scene lights* detaches the object from scene lighting (Help *3D object*).
- **Switch lights by state.** Use the Light's *Enabled* expression, e.g. street lights on at night with `getHourOfDay() >= 19 || getHourOfDay() < 6`.

## KPIs instrumented
n/a (presentation).

## Pitfalls
- **Light limit.** The Big Book caps a scene at 6 lights, counting lights brought in by embedded agents *(not restated in Help 8.9.10)*. A headlight inside a `Car` type with a large fleet can exceed it. Light the scene globally, or light only a few showcase agents.
- **Coloured lights change what the viewer reads.** Colour-coded agents (state, priority) can become unreadable under coloured light. Keep scene lights white or grey when colour carries meaning.
- **Import formats.** "Collada only" (p. 11) is outdated; see the format list in `videos/3d-scene-z-order-and-lighting.md`.

## Reusable idea
- Draw flat, tilt with groups, lift coplanar items by a hair.
- Put cameras and lights inside agent types only when there are few instances.
- Switch windows between an agent's camera and fixed cameras with `setCamera(…, follow, ms)`.

## When the co-pilot should use this
- Stakeholder demos that follow a truck, AGV, patient or aircraft; signs, gates and ramps that must stand up; night or indoor lighting.
- **Symptoms:** a group errors after adding a curve or rounded rectangle; a label flickers; a camera button leaves the user unable to zoom; objects turn black or vanish under a coloured light.
- **Related:** `videos/3d-scene-z-order-and-lighting.md`, `videos/per-agent-3d-material-color.md`, `bigbook/click-handling-view-navigation-and-code-created-shapes.md` (camera and view buttons).
