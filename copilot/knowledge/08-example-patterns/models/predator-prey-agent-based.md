# Pattern card — Predator Prey Agent Based
- **Source:** AnyLogic example model "Predator Prey Agent Based" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Simulate hare and lynx populations as individual agents whose births, predation and crowding happen locally on a grid where **many agents share a cell up to a cap**, and see the stochastic, patchy cycles this gives next to the smooth SD version.

## Structure
- **Space.** An ordinary continuous 2D space, logically cut into a `Width × Width` grid of cells of `CellWidth` pixels.
  Each agent stores only an integer `cell` (index = row × Width + column). Its drawing position is the cell corner
  plus a random offset inside the cell (two helper functions convert cell and offset to x, y).
- **Per-cell index.** Main holds an array of `ArrayList<Hare>`, one list per cell. On startup the lists are created
  and every initial hare is added to its cell's list. After that, every birth adds to a list and every death removes
  from it.
- **Hare.** Statechart *Alive → Dead*, by a timeout equal to the life expectancy or by a message from a lynx (eaten).
  The final state's action first removes the hare from its cell list, then from the population. A **rate** event
  (natality) creates `NumberPerBirth` babies in the mother's cell. If that cell already holds `MaxPerCell` hares,
  each baby goes to a random neighbouring cell (of the 8) that is not full. If none is free, births stop: local
  carrying capacity.
- **Lynx.**
  - A *Hunt* transition fires every hunting period. It catches with probability
    `min(1, haresInCell / (0.5 × MaxPerCell))`, so success rises with local prey density and saturates at half the
    cell cap.
  - On a catch, it picks a random hare in its cell and sends it a message.
  - On a miss, it moves to a random neighbouring cell.
  - It dies of old age (timeout) or of hunger: a timeout in the "since last meal" state, which restarts after every
    catch.
  - A rate event creates cubs in the parent's cell.

## Resources
n/a.

## Key settings worth copying
- **Why not discrete space:** AnyLogic's discrete space allows **at most one agent per cell**, and moving into an
  occupied cell raises an error (Help 8.9.10 `anylogic/agentbased/discrete-space.html`, `movement-discrete.html`).
  To put several agents in one cell with a capacity, keep continuous space and index the cells yourself.
- The neighbour search is the 8 surrounding cells, clipped at the grid edge. It collects the free cells first and
  then draws one uniformly, so the choice is not biased by the scan order.
- Births are Poisson (rate events). Lifetimes are fixed timeouts, so every hare lives exactly its life expectancy
  unless eaten. Replace them with a distribution if age at death matters.
- Model time unit years; random seed per run (the cycles differ from run to run by design).

## KPIs instrumented
- Time plot of `hares.size()` and `lynx.size()`.
- Useful additions: period and amplitude of the cycles over replications, extinction time or probability, share of
  cells at the cap.

## Pitfalls
- **The index must match the population.** Every place that creates, kills or moves an agent has to update the cell
  lists. The Dead action removes the hare from its list *before* `remove_hares(this)`. A missed update gives lynx
  "ghost" prey or crowding that never clears.
- The cell grid is logical only: agents do not walk. If you add movement, move the agent between lists at the same
  moment you change `cell`.
- **One index convention.** In the 8.9.10 example, the "not-full neighbour" search builds the index as
  column × Width + row, while the rest of the model uses row × Width + column. Overflow babies therefore land in the
  *transposed* cell, which is a true neighbour only near the diagonal. The lynx's random-neighbour move uses the
  right order. Put the index formula in one helper and call it everywhere.

## Reusable idea
Many agents per location with local rules (capacity, contact, predation) → a hand-kept bucket index over continuous
space: an array of lists plus an int cell per agent. It is cheap to query ("who is in my cell?", "which neighbour has
room?") and has no one-per-cell limit. The same structure fits animals on pasture, customers per store zone, or
pallets per floor zone.

## When the co-pilot should use this
- A spatial ABM where local density drives births, contacts, infections or service, and cells must hold more than one
  agent.
- As the ABM counterpart of the SD *Predator Prey* model, to show how individual stochasticity and locality change
  the oscillations. The SD↔ABM comparison itself is covered in
  `00-method-selection/` (Borshchev & Filippov).
- Deciding between AnyLogic discrete space (one agent per cell, built-in neighbours) and continuous space with your
  own grid index.
