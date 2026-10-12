# Pattern card — Getting Mouse Coordinates
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Capturing and displaying the exact canvas coordinates of a user's mouse click at runtime, enabling interactive point-selection or click-driven logic in a simulation presentation.

## Block chain
No process-flow chain is present. The model uses a mouse-event listener attached to the presentation layer. When the user clicks anywhere on the model canvas during runtime, an event handler fires, reads the current pointer position in model coordinates, and writes those x/y values to visible text labels on the screen.

## Resources
n/a

## Key settings worth copying
- Mouse click event wired to the root agent's presentation shape (or a transparent rectangle covering the canvas)
- Coordinate retrieval through the local variables of the shape's *On click* action: `mouseX = clickx; mouseY = clicky;` (8.9.10 model and Help *How-to*). `clickx` / `clicky` are relative to the clicked shape — add `self.getX()` / `self.getY()` for coordinates in the container (corrected 2026-10-01; an earlier version named `getX()` / `getY()` as the source)
- Display updated immediately within the same action callback — no scheduling needed

## KPIs instrumented
n/a (the output is purely the live x/y coordinate display on screen)

## Reusable idea
Wire a mouse-click action to a transparent overlay shape and read `clickx` / `clicky` (plus the shape's own `getX()` / `getY()`) inside the handler to convert raw screen clicks into model-space coordinates — a lightweight way to add point-and-click interactivity (e.g., placing agents, selecting zones, or logging positions) without any external UI framework.
