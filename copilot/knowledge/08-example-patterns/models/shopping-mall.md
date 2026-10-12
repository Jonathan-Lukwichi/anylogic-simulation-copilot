# Pattern card — Shopping Mall
- **Source:** AnyLogic example model "Shopping Mall" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Pedestrian Library + PML auxiliary blocks, custom replicated blocks)
- **Problem it solves:** Route thousands of visitors through personal shop itineraries across 150 destinations and two levels with a readable flowchart, then close the mall cleanly at a fixed hour.

## Block chain
- **Entrances:** seven `PedSource` entrances (100–200/h each) with *On exit* `generateTasks(ped)`. They lead into custom level-change blocks and then into the loop.
- **The loop:**
  1. `PedSelectOutput chooseActivity` (conditions on `ped.tasks.getFirst().type`).
  2. A `SelectOutputIn` per activity with `choice = shops.get(agent.tasks.getFirst().id).inBlock`. Anchor shops and WCs are handled the same way.
  3. The replicated custom block `AreaDelay`. The ice rink (`Skate`) and food court (`Eat`) are single custom blocks.
  4. `SelectOutput exitOrContinue`: `agent.tasks.isEmpty() || isClosed`.
  5. Loop back, or go to the exits: `PedSelectOutput` → `UseStairsOrEscalator` down → `PedGoTo` → `PedSink`.
- **`AreaDelay`** (replicated: `shops` ×138, `anchorShops` ×9, `WCs` ×3):
  1. `SelectOutputOut inBlock` (its `selectOutputIn` is a parameter).
  2. `PedGoTo` to the shop entrance.
  3. `PedExit`: the visitor leaves the floor, and the shop interior is not modelled spatially.
  4. `Delay` (shopping time, max capacity).
  5. `SelectOutput` (`!agent.canceled` → *On exit true*: `tasks.removeFirst()`).
  6. `PedEnter` at the same entrance line.

  The cancelled branch goes through a short `Delay` to `PedEnter`, and PedGoTo's `ccl` port is wired straight to the block's exit.
- **`Eat`:** `PedService` (a service-with-lines markup), then `PedWait` at a random attractor of one of three food areas: `attractor = self.getRandomAttractor(foodAreas[ped.selectedIndex])`.
- **`Skate`:** Queue → `Delay` (capacity 20, moving along the rink path for 1.5 min) → another round while `nRound < 15 && !main.isClosed`.
- **Levels:**
  - `UseStairsOrEscalator`: a `SelectOutput` (stairs with probability 0.3 up, 0.6 down) splits between `UseStairs` (`PedGoTo` + `PedChangeLevel` between target lines on two levels) and `PedEscalator` (group and direction as parameters).
  - `UseElevatorGroup`: `PedElevator` with `elevator = randomFrom(elevators)` and a target level.

## Resources
Service-with-lines counters at the food court. Escalator groups, two elevators, and the rink capacity of 20.

## Key settings worth copying
- **Itinerary as data.**
  - `tasks` is a `LinkedList<Task>`, where each Task holds a type enum and an index.
  - It gets 1–10 random shops, 1–2 anchor shops, food (p 0.35), WC (p 0.35) and skating (p 0.05).
  - The list is then shuffled with the **model's** generator: `Collections.shuffle(visitor.tasks, getEngine().getDefaultRandomGenerator())`.
- **Replicated block addressed by index.** Per-copy parameters use `index` (`areaEntrance = shopEntrances.get(index)`, `visitorCounter = shopCounters.get(index)`, `name = anchorShopNames.get(index)`). The collections of TargetLines and texts are filled in their *Initial contents* (Help *Replicated block*, *Collection variables*).
- **Closing at 10 h** (a one-time event runs `close()`):
  - set `isClosed = true`;
  - on every area block, `goToEntrance.cancelAll()`, flag `canceled = true` on the agents in the delay, then `stopDelayForAll()`;
  - on the food court, `PedService.cancelAll()` + `PedWait.freeAll()`;
  - set every `PedSource.set_rate(0)`.

  The `PedSink` notices the last visitor with `countInTheMall() == 1` and calls `getExperimentHost().showMessageDialog(...)`.
- **Occupancy:** `countInTheMall()` sums the `size()` of all blocks, and each block exposes its own `size()`. Entry and exit totals come from `countPeds()`, and elevators from `nTransportedPeds()`.

## KPIs instrumented
People entering, shopping and exiting; live counters per shop, WC and rink queue; a density map (hidden at start); elevator throughput.

## Pitfalls
- **Don't rely on the rate expression.** The sources set *Modify rate* with `isClosed ? 0 : baseRate`, but Help 8.9.10 documents that option only for *Rate schedule* arrivals, where `baseRate` is the schedule value. These sources use a plain rate, and the explicit `set_rate(0)` is what closes them *(runtime effect of the expression in Rate mode unverified)*. Use a rate schedule with *Modify rate* if you want an expression to govern arrivals.
- **Wire every `ccl` port.** `PedGoTo` / `PedService` `cancelAll()` push pedestrians out through `ccl`, so wire it to a sensible exit (here, the block's exit).
- **Shuffle with the model's generator.** `Collections.shuffle(list)` without the engine generator breaks fixed-seed reproducibility; Help's reproducibility checklist warns against it (see G17 and the proposals).
- **Fixed seed is not enough.** Pedestrian models compute in several threads, so exact repeats need the preference *Number of processors for parallel execution* set to 1 (Help *Reproducible experiments*).
- **Nobody walks inside the shops.** Shop interiors are abstract (PedExit … PedEnter), so in-store crowding is not simulated; only corridors and entrances are.
- **SelectOutputIn is evaluated early.** It picks the route when the previous block finishes, so the choice must not depend on changes made in that block's *On exit* (Help; gotchas on volatile routing).

## Reusable idea
When agents visit many identical destinations:
- hold the itinerary in the agent as a list of typed tasks;
- make one replicated custom block per destination type, configured per copy through `index` and collections;
- dispatch with `SelectOutputIn` → `copy.inBlock` (a `SelectOutputOut` inside the block);
- loop until the list is empty.

For a curfew, give every custom block a `cancelAll()` that drains it, and set the arrival rates to zero.

## When the co-pilot should use this
- **Use cases:** malls, airports (shops and gates), hospitals (departments), campuses, and theme parks with rides.
- **Warning signs:** any flowchart that would otherwise need dozens of hand-wired branches, and models that must empty a facility at closing time.
- **Related cards:** `models/evacuation.md` (PedChangeLevel), `basicmodels/group-behavior-in-services.md` (random appearance), and `videos/rail-shuttle-pedestrian-boarding.md` (`freeAll` / `cancelAll`).
