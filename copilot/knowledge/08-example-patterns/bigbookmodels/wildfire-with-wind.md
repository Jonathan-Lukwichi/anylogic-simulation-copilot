# Pattern card — Wildfire with Wind
- **Source:** AnyLogic example model "Wildfire with Wind" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Spread over a large grid (fire, lattice epidemic, contamination) at a cost that follows the active front rather than the grid size, with the grid coupled to agents that move in continuous space.

## Structure
Read with its Big Book companions: *Wildfire* (no wind, grid directly on Main), *Schelling Segregation Model* and *Conway's Game of Life* (the stepped style).
- **Grid.** 200 × 200 = 40,000 `GridCell` agents fill the discrete space of a small container type `Grid`. A second container, `SkySpace`, has its own continuous space and holds one `Airplane`. Both are embedded in Main.
- **Each cell is a statechart; there are no time steps.**
  - Normal → Burning on the message `"Ignition"` (guard `Fuel > 0`).
  - Burning → BurnedOut after a timeout of `Fuel` minutes, so a richer cell burns longer.
  - Inside Burning, an internal Rate transition (5 per minute) loops over `CellDirection.values()`. For each direction it takes the neighbour from `getAgentNextToMe(dir)` and sends it `"Ignition"` with probability `fireTransmissionProbability(dir)`.
  - A message that reaches a burning or burnt cell matches no transition and is dropped. That is the whole "already on fire" rule.
- **Wind.** `Wind` is a `CellDirection` parameter on Main. The spread probability is 0.5 along the wind, then 0.3, 0.1, 0.05 and 0.03 as the angle to the wind opens in 45° steps. Eight clickable arcs set `Wind`, and an arrow group is rotated by `Wind.getAngle()`.
- **Ignition sources.**
  - A click on the map.
  - The airplane: Wait → message `"Take off"` → Fly (`moveTo(EndX, EndY)`), with an internal 5-minute Timeout calling `bomb()`; arrival leads to a final state.
  - `bomb()` divides the plane's x and y by the cell size to get (row, column) and messages that cell.
- **Drawing.** Cells have no agent shapes. `setGridCellColor()` paints one square on a Canvas, and only when a cell changes state (mechanics in `bigbook/animation-dynamic-properties-and-frame-cost.md`).
- **Fuel map at startup** (`makeUpInitialFuel()`):
  1. 200 random seeds, each scattering 1,000 increments of 0.25 with `triangular(-50, 0, 50)` offsets, wrapped with `% N`;
  2. ten passes of averaging each cell with its `getNeighbors()`;
  3. a linear rescale to [−0.2, 1.3].

  The negative tail makes patches that cannot burn — fire breaks for free.

## Resources
n/a. No Process Modeling Library blocks; each cell's fuel is its only "resource".

## Key settings worth copying
Discrete-space API (Help 8.9.10 *Discrete space*, *Movement in discrete space*; Javadoc 8.9.10):
- `getAgentAtCell(row, col)` takes the **row first** and returns null for an empty cell.
- `getAgentNextToMe(dir)` returns null at the border.
- `getNeighbors()` returns `Agent[]` following the neighbourhood type (Moore = 8 cells; "Euclidean" = N, S, E, W). It returns **null, not an empty array,** when there are none. Cast the elements.
- Size queries: `spaceRows()`, `spaceColumns()`, `spaceCellWidth()`; the agent's cell: `getR()`, `getC()`.
- `jumpToRandomEmptyCell()` returns false when no cell is free. Help calls the pick "pseudo-random": crowded grids give unequal odds.
- More agents than cells is a runtime error.

`CellDirection.getAngle()` is a compass angle: NORTH 0, NORTHEAST π/4, EAST π/2, SOUTH π, WEST 3π/2, NORTHWEST 7π/4 (printed from the 8.9.10 engine).

- **Click → cell:** in the canvas's On click, `getAgentAtCell((int)(clicky / s), (int)(clickx / s))`, where `s` is the cell size in pixels.
- **Deliver without queueing:** `cell.statechart.receiveMessage("Ignition")` is consumed at once or discarded, and returns whether any transition matched (Javadoc). The model's `receive()` is deprecated since 8.9.2 (G24); use `send("Ignition", cell)`.

## KPIs instrumented
None; the map is the output. Worth adding: burnt area (count on entry to BurnedOut), cells currently Burning (the front), and time to extinction.

## Pitfalls
- **Wrap angle differences.** The model uses `abs(dir.getAngle() - Wind.getAngle())`. With the default NORTHWEST wind (7π/4), spread to NORTH (0) gets a raw difference of 7π/4 and so the 180° value 0.03, while WEST gets 0.3. The fire leans to one side. Fix: `d = abs(a - b); d = min(d, 2*PI - d);`, then apply the thresholds.
- **One cell size everywhere.** In this version `Grid` keeps the default 500-px width, so its `spaceCellWidth()` is 2.5 px, while the canvas and `bomb()` use `canvasScale = 3`. Painting, clicking and position mapping must share one constant. Clamp indices to `0 … spaceColumns() - 1`: a mover exactly at the far edge maps one column too far.
- **Stepped or event-driven?**
  - *Enable synchronous steps* (Game of Life, Schelling) makes every cell run On before step, then On step, every tick. That fits rules defined per generation; the two phases stop early movers from changing what later agents see.
  - When activity is sparse, like a fire front, ticks waste work on idle cells. Event-driven cells cost nothing until something happens to them.
- **Schelling's threshold** compares same-colour neighbours with `neighbors.length * Preference`. Only occupied cells count, so agents on edges or in sparse areas are judged on fewer neighbours. An isolated agent (null neighbours) is treated as happy.

## Reusable idea
Give each cell its own statechart and let neighbours talk by message: run time follows activity, not grid size. Draw the grid on a canvas. Keep movers in a separate continuous container and convert their positions with the cell size.

## When the co-pilot should use this
- Spatial spread on a lattice: wildfire, epidemics, contamination, flooding, land-use change, grid diffusion.
- A cellular model that slows down as the grid grows: move from ticks to event-driven cells, and draw with a Canvas.
- A drone, aircraft or vehicle in continuous space that must act on grid cells.
- Related: `models/the-game-of-life.md` (stepped version), `bigbook/synchronous-tick-transition-from-probability-table.md`, `bigbook/statechart-message-queue-and-safe-handoff.md`, G21, G24.
