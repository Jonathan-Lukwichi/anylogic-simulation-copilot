---
name: anylogic-2d
description: 2D modelling, animation and dashboard design in AnyLogic - presentation shapes, dynamic properties, space markup (nodes/paths), live agent animation in zones, colour-by-state, view-area navigation, and the design system for professional dashboards. Use for any visual/animation/UI work in an AnyLogic model.
---

# anylogic-2d

Everything on an AnyLogic canvas IS the 2D presentation. This skill covers making it live
(animation), navigable (tabs), and professional (design system). 3D is a camera on top of this —
see `anylogic-3d`.

## The two element families (never confuse them)
- **Presentation palette** (Rectangle, Oval, Line, Text, Image, Rounded Rect, View Area, Group):
  drawing + UI. Rendered at runtime.
- **Model elements** (variables, parameters, functions, blocks): logic. NEVER rendered at runtime —
  their editor icons are for the reader only. Organise them in labelled zones; don't try to "hide" them.

## Dynamic properties — the single most important 2D mechanic
Almost every visual property (Text, Fill color, Line color, X/Y, Rotation, Visible) has an `=`
toggle: **static value ↔ expression re-evaluated continuously**.
- Live KPI text: click `=`, write a Java expression returning String (`\n` = line breaks; ONE text
  block can render a whole card).
- State-coloured shapes: `Fill color =` `stock < s ? red : green`.
- Symptom of a missed `=`: the screen shows your code with quotes and `+` literally.
- Keep display logic OUT of expressions where possible — write a Main function
  (`kpiSummary()`) and call it; one audit point, reusable across cards.

## Live agent animation (dots moving through zones) — the 20-minute twin
1. Draw zone shapes (Rounded Rectangles + titles) laid out by flow.
2. **Space Markup → Rectangular Node** inside each zone (name them `nTriage`, `nWard`…).
3. Each process block (Service/Queue/Delay) → Properties → **Agent location (queue/delay)** → the node.
4. Give the agent type a small 2D shape (Oval ~8px) — colour it dynamically by state/acuity:
   `triage.equals("P1") ? red : triage.equals("P2") ? orange : green`.
5. Run: agents render as coloured dots inside the zones, accumulating and flowing. Add live counts
   per zone (`block.size()`, `queueSize()`) and you have a legible 2D digital twin — usually
   CLEARER than 3D for analysis and theses.
- **Path + Point Node** markup (Process palette) additionally animates travel along routes; use
  Rectangular Nodes alone when "which zone, how many" is the message.
- Attractors (inside a node) spread waiting agents so dots don't stack on one spot.

## Screens & navigation (the tab pattern)
- One big canvas, content in **separate regions** (e.g. Y=0 process, Y=700 dashboard, Y=1450 charts).
- **View Area** at each region's top-left (name `vaX`, set Width/Height to frame the region).
- Nav buttons: `vaX.navigateTo();` — create the View Area BEFORE the button (else "cannot be resolved").
- Duplicate the nav bar into every region (copy-paste the whole bar) so tabs are always visible.
- Open on a chosen screen paused: Timeout event at t=0 → `vaDashboard.navigateTo(); getEngine().pause();`
- Sim controls as buttons: `getEngine().run() / pause() / stop()`.

## Layering & protection
- Right-click → **Order → Send to Back** for any background shape (else it hides content).
- Right-click → **Locking → Lock** big backgrounds so clicks pass through to cards.
- **Grouping → Create a Group** works ONLY for presentation shapes; model elements can't join —
  rubber-band select to move mixed sets, then Lock.

## Design system (the difference between student and expert)
- **Page background** `#F5F7FA` behind everything (Send to Back + Lock); cards white `#FFFFFF`
  with 1px `#DDE3E8` border. Depth via contrast, not decoration.
- **Colour = meaning, never decoration.** One accent per semantic (AI purple `#5E35B1`,
  decision blue `#1E88E5`, outcome green `#2E7D32`, neutral `#546E7A`). Kill rainbows —
  use a thin coloured top-strip on white cards instead of full-colour fills.
- **Type scale:** 16 bold page title / 12 bold card header / 10 body. Nothing else.
- **Grid:** margin 40, gutter 24, card padding 16, 60px clear under the nav bar; set X/Y
  numerically in Properties — never eyeball. Uniform card sizes per row.
- Charts (Analysis palette): Plot = DataSet vs index; Time Plot = value vs sim time; Bar = few
  categories; match paired chart sizes exactly.

## Text-in-card discipline
Text is a separate element from its card: place at cardX+10 / cardY+10, left-aligned; overflow →
shrink font to ~10 or widen ALL cards of that row equally (uniformity beats fit).
