# Pattern card — Rail traffic control: resource-locked track sections and look-ahead braking
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 9 "Rails and trains" — distilled, original wording
- **Paradigm:** DES (Rail Library + Process Modeling Library)
- **Problem it solves:** The Rail Library detects collisions but does not prevent them. The modeller has to supply the signalling rule that keeps trains apart at merges and shared sections.

## Block chain
The book's example 9.2 has a main line A → B → C and a passing loop D.
- Every third train goes into the loop: `notEachThird` is a SelectOutput with condition `self.in.count() % 3 != 0`, and its false exit leads to the loop.
- That train waits there for `uniform(3, 10)` min, while a train arrives every 5 min. Trains from B and D merge at `switchCBD`.

Controlled version (Big Book pp. 22–24):
1. `trainSource` → `notEachThird`.
   - True exit: `moveToCheck` (to `pointCheck`, no braking) → `exitIsBusy` (SelectOutput, condition `resourcePool.idle() == 0`).
   - False exit: `moveToBranch` (Decelerate and stop at `pointBranch`) → `delay`.
2. From `exitIsBusy`: if busy, go to `moveToMain` (Decelerate and stop at `pointMain`, the "signal"); if free, go straight on to step 3.
3. `moveToMain`, `delay` and the free exit all feed `seize` (1 unit of `resourcePool`) → `moveToExit` (Start: Accelerate/decelerate to cruise speed) → `release` → `trainDispose`.

Without the Seize/Release pair, a run in virtual time soon stops with the runtime error `The switch '<name>' cannot be seized: another car is over it` (exact message, so it can be searched).

## Resources
One `ResourcePool` of capacity 1 per section that only one train may occupy: the merge and the track beyond it. It acts as a block token. The book also names a Hold block, or RestrictedAreaStart/RestrictedAreaEnd around the section, as alternatives.

## Key settings worth copying
- **Seize before the conflict, release after the whole train has cleared it.** Wrap the TrainMoveTo that crosses the shared switch. For a finer release, use TrainMoveTo's *On exit track* callback when the tail leaves the last track of the section *(suggested; the callback is in Help)*.
- **Look-ahead point.** Add a Position on Track ahead of the signal. Trains run to it without braking and test the section there. Only a train that finds the section busy decelerates and stops at the signal; a train that finds it free seizes at once and runs through at cruise speed.
- **One continuous run, several blocks.** Keep speed across the seam between TrainMoveTo blocks (Help *TrainMoveTo*):
  - first block: *Finish at current speed*;
  - next block: *Continue at current speed*, or *Accelerate/decelerate to cruise speed*. The latter leaves a train already at cruise speed alone and accelerates a stopped one.

  A single TrainMoveTo can take trains from different positions (signal, loop, look-ahead point) to one target.
- **Beyond the book (Help 8.9.10, *TrainMoveTo*):**
  - Start/Finish options *Accelerate if condition is true* and *Decelerate if condition is true*, evaluated when the train enters the block, can replace the extra SelectOutput;
  - *Route should not contain* keeps listed tracks out of an automatic route;
  - *Limit distance to move* stops a train a set distance past a switch;
  - *If the track gets blocked* offers Stop before this track or Recalculate route (`basicmodels/blocking-railway-tracks.md`).
- **`self` in a block's dynamic field is the block itself,** so `self.in.count()` counts the agents that have entered it.

## KPIs instrumented
The book has none for this example. Suggested:
- section occupancy: `resourcePool.utilization()`;
- waiting time at the signal: TimeMeasureStart before `seize`, TimeMeasureEnd after it;
- share of trains that had to brake;
- switch operations: `switchCBD.getToggleCount()`.

## Pitfalls
- **Crossings are not checked.** Collisions are detected only at switches and between trains on the same track. Tracks that cross without a switch are not checked (Help *RailSettings*), so lock a diamond crossing with a resource as well (G52).
- **Test in virtual time.** At animation speed the first trains pass by luck; the random dwell overlaps with arrivals only later. The book's run fails only in fast mode.
- **Release too early.** Release when the tail has cleared the fouling point, not when the head reaches the target.
- **Deadlock.** Two trains each hold one section and request the other's. Seize sections in a fixed global order, or merge conflicting sections into one pool *(general signalling practice)*.
- **No reversing inside one block.** TrainMoveTo routes only without a change of direction (G28).

## Reusable idea
Map each interlocking rule onto process-modeling resources: a block section is a capacity-1 pool, a red signal is a pending Seize, and "line clear" is a Release. Add a look-ahead point so that braking depends on the signal state.

## When the co-pilot should use this
- Any rail model with merges, single-track sections, passing loops, crossings or shared platforms.
- Symptoms: the switch-seizing runtime error quoted above, or collision errors that appear only in fast runs.
- Related: G26, G28, G29, G52; `videos/rail-shuttle-pedestrian-boarding.md`; `basicmodels/blocking-railway-tracks.md`.

## Additions (8.9.10 review, 2026-10-01)
- Admission control at the source: TrainSource can *Leave as logical agent (will use TrainEnter later on)*, so a `Seize` → `TrainEnter` chain lets a train onto the track only once a resource (a path, a crew) is granted. TrainExit's *Exiting trains* are *removed from the space* (default) or *stay where they are* (Help 8.9.10 *TrainSource*, *TrainExit*, *TrainEnter*).
- Track reservations (`reserveFor`, `isAvailableFor`, `cancelReservation`) are a second locking tool, with its own traps (gotcha G100; `basicmodels/railway-track-reservation.md`).
