# Pattern card — 3D scene set-up: Z / Z-Height ordering, ground and floor slabs, lights that replace the defaults
- **Source:** AnyLogic video "How to add 3D animation in your models" (https://youtu.be/L5SD_QdUUKE) — distilled, original wording
- **Paradigm:** Method (3D presentation, any paradigm)
- **Problem it solves:** Fixes the recurring 3D defects: objects buried in or floating above the floor, a scene that goes darker after you add a light, and camera navigation that ignores its limit.

## Mechanism
**Already in the KB** (`01-anylogic-core/anylogic-in-3-days.pdf`, pp. 160–163, 190–191, 208):
- the 3D Window and the `[window3d]` view area it creates;
- Camera → *Copy camera location* → *Paste coordinates from clipboard*;
- Navigation type *Limited to Z above 0*;
- Alt+drag rotation;
- the 3D Objects palette;
- wall Z-Height.

This card adds the geometry and lighting rules. The floor-slab values come from "How to simulate multi-level facilities" (https://youtu.be/IpSr9CDVGz0).

1. **In 3D, geometry decides what covers what.** "Send to back" fixes overlap in the 2D view only. In 3D, only Z and Z-Height matter.
2. **Rectangles become boxes.** In 3D a Rectangle is drawn as a parallelepiped whose **Z-Height defaults to 10 px** (Help 8.9). A "ground" rectangle at Z = 0 is therefore a 10-px slab that swallows anything standing at Z = 0; in the video it hid the worker. Two fixes:
   - flat ground: Z-Height = 0 (video 3);
   - a slab of thickness t whose top is the floor: Z = −t, Z-Height = t (video 2 uses Z = −1, Z-Height = 1 for the new floor's rectangle).
3. **Raise what should float.** Give conveyors and paths a positive Z. The video sets the conveyor path to Z = 10 px, which is 1 m at 10 px/m. Z is always relative to the element's level.
4. **Lights replace the defaults; they do not add to them.** The scene is lit by two hidden default lights, one ambient and one directional. Adding **any** Light element removes both, so plan a complete set (the video adds two).
   - Predefined types: Street light, Car headlight, Daylight, Moonlight.
   - *Custom* offers Ambient, Directional, Point or Spot (Help 8.9).
5. **Navigation limits apply only to a free window.** Assign the Camera in the 3D Window's *Camera* field. *Full* and *Limited to Z above 0* work only when the window does **not** follow the camera. With *Follow camera*, only *Rotation only* or *None* apply (Help 8.9).

## Resources
n/a

## Key settings worth copying
- **Ground.**
  - Use a Rectangle: fill = texture (e.g. grass), line = no color, Z-Height = 0.
  - Send it to back so it doesn't cover other shapes in 2D.
- **Debugging Z.** In the 3D Window, set Scene → **Grid color** to show the Z = 0 plane at runtime. It is off by default.
- **Skybox (8.9).** The Scene section offers Skybox presets (Clear sky, Warehouse, City…) that add environment lighting for PBR materials. They are an alternative to hand-placed lights for a scene that is "too dark". *Beyond the video.*
- **Import formats.** Help 8.9 lists .dae, .gltf/.glb, .fbx and .obj among the supported formats. The video's X3D/VRML advice is outdated.

## KPIs instrumented
n/a (presentation).

## Pitfalls
- **Over-lit imports.** Imported 3D objects may carry their own lights and look over-lit once you add lights. Adjust lighting in the object's own properties (Help 8.9).
- **Far clipping.** Anything beyond the 3D Window's **Far clipping distance** (Advanced) is not drawn, so distant parts of a large site seem to vanish. *Beyond the video.*
- **Icon shapes.** Shapes flagged as part of the agent's *Icon* never appear in 3D.
- **Levels.** On multi-level models, the slab and object Z values are offsets from each level's Z (see `videos/multi-level-facility-lift-landings.md`).

## Reusable idea
Build 3D on one vertical datum:
- the floor plane at each level's Z = 0;
- slabs below it and equipment on it;
- overhead conveyors above it.

Check the result with the grid on *before* adding textures and lights, and add lights as a complete set.

## When the co-pilot should use this
- **Symptoms:** the user reports buried, floating or invisible 3D objects, a scene that got darker, or a camera going under the floor.
- **Demos:** when preparing stakeholder demos. This is build Phase 5, after the logic is verified.
- **Related cards:**
  - `videos/flowchart-block-animation-binding.md`: make agents appear at all.
  - `videos/per-agent-3d-material-color.md`: agent colours.
  - `videos/spiral-conveyor-per-point-z.md`: per-point Z.

## Additions (8.9.10 review, 2026-10-01)
- 2D draw order does not carry into 3D: flat shapes at the same Z interlace (flicker), so give stacked flat shapes slightly different Z values, e.g. 0, 0.1, 0.2 (Big Book ch. 12 p. 9).
- In 8.9.10 a group shown in 3D may not contain 2D-only shapes (curve, rounded rectangle, anything set to 2D only); the Problems view reports it (Help *Group*). The Big Book's "they just become invisible" is outdated.
- Light colour filters object colour channel by channel — a red light hides a blue object — so keep lights white or grey when colour carries meaning (Help *Light*).
- Imported 3D objects: *Internal lights* = Off / Illuminate the object / Illuminate globally, plus *Ignore scene lights* (Help *3D object*). Background, grid and skybox are shared by all 3D windows of an agent type (Help *3D window*). The Big Book caps a scene at 6 lights, counting lights inside embedded agents — not restated in Help 8.9.10 *(unverified)*.
