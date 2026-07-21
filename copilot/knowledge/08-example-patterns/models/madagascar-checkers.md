# Pattern card — Madagascar Checkers
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Demonstrates how agent statecharts and inter-agent messaging can drive interactive, rule-based game logic entirely within AnyLogic, with no process-flow blocks required.

## Block chain
There are no Source/Sink/Service blocks here. Instead, two agent types — a game-controller (Main) and Stone pieces — each carry a statechart. The board is a 7×7 cross-shaped grid of 33 playable cells; 32 stones are placed at start, leaving only the centre empty. A player clicks a stone: the click fires a "moveToHereAvailable" event into the Main statechart, which checks whether the chosen stone can jump over an adjacent neighbour into an empty landing cell. If valid, the stone animates to the new position, the jumped stone is removed from the population, and Main fires a "MOVED" event back to itself to refresh which pieces are now eligible to move. Timeout transitions in the statechart handle the brief animation window before the model re-evaluates legal moves. An "UNDO" message rolls the board back one half-move by restoring the last removed stone and reversing positions. A "NEW GAME" message resets the entire stone population to the initial layout.

## Resources
- Stone agent population: starts at 32, decreases by one per successful jump; win condition = 1 stone remaining in the central cell.
- Board cells: 33 fixed positions encoded as index pairs (row = index / 7, col = index % 7).
- Agent links: each Stone holds a bidirectional COLLECTION_OF_LINKS connection, giving it access to the Main controller's statechart for event propagation.

## Key settings worth copying
- Time unit: Minute (essentially irrelevant — used only to time animation delays on state transitions).
- Statechart triggers: mix of `message` triggers (player click or game-event string) and `timeout` triggers (short animation pauses before state re-evaluation).
- ConnectionsPerAgent = 2 for Stone links (one up to Main, one to its board-cell position).
- OnArrival callback on Stone agent fires `main.statechart.fireEvent("MOVED")` to keep legal-move highlighting current after every animation.
- Click handler on board holes calls `statechart.fireEvent(moveToHereAvailable(row, col))` — a custom event object carrying grid coordinates.

## KPIs instrumented
- Stone count remaining (implicit win/loss condition; no explicit chart instrumented).
- Moves taken (tracked implicitly through state history for undo).
- n/a for throughput, utilisation, or wait-time metrics — this is a puzzle model, not a performance model.

## Reusable idea
Use a Main-level statechart as a finite-state machine game-controller and let child agents (Stone pieces) fire typed events upward via their parent link — this cleanly separates individual-piece logic from board-wide rule enforcement, and the same pattern applies to any IE scenario where individual entities must trigger global mode changes (e.g., a machine breakdown agent signalling a shop-floor controller to reroute jobs).
