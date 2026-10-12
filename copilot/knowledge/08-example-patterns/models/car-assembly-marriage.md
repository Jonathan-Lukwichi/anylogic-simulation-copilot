# Pattern card — Car Assembly Marriage
- **Source:** AnyLogic example model "Car Assembly Marriage" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model the "marriage" station of a car final-assembly line, where a body carried by an overhead hanger is joined to the powertrain while both carriers keep moving, and pace the carrier loops so none of them starves or collides.

## Block chain
Four closed loops of carriers plus a consumable feed, all built from PML blocks on Material Handling conveyors
(time unit minutes, delays in seconds).
1. **Body infeed.** One floor skid, one lifter module and one body at a time, each made by a Source set to *Calls of
   inject()*. The lifter picks up the body and the skid picks up the lifter (`Pickup`). A `Hold` in *Conditional*
   mode admits the skid only when a hanger **and** a marriage platform are ready. `Convey` takes it to the lifting
   point; that block's *On exit* injects the next skid, lifter and body, so exactly one body is in the infeed at a
   time. A 2-minute `Delay` tells the lifter to raise the body.
2. **Overhead hanger loop (3 hangers).** `ConveyorEnter` → `Convey` to the hand-over point → `Pickup` of the raised
   body → `Match` (port 2) → `Convey` through the marriage zone → `Hold` (block after N) → `Dropoff` of the body →
   back to base.
3. **Marriage platform loop (3 platforms, each carrying a lift table).** `Pickup` mounts the table → `ConveyorEnter` →
   `Queue` (capacity 3) → `RestrictedAreaStart` (capacity 2) → `Match` (port 1) pairs the platform with a loaded
   hanger → `Convey` to the assembly point → **`Split`**: the platform itself continues by `Convey` to the end of
   the zone, while the copy picks up a powertrain and runs two `Delay`s (fit exhaust 3–7 s, marry 30–60 s,
   triangular) → **`Combine`** keeps the platform (agent1) once both have arrived → `RestrictedAreaEnd` → `Convey`
   back to the start.
4. **Powertrain feed.** A manual Source pre-stocked with five units on a feeder conveyor; each pickup injects one
   replacement.
5. **Exit.** The married car is lowered onto the exit conveyor by `MoveTo` blocks timed by trip time. When it has
   moved 6 m along the exit conveyor, that `Convey`'s *On exit* unblocks the two block-after-N Holds, which lets the
   next hanger unload and the next car lower.

## Resources
- No ResourcePool. Capacity lies in the **carrier counts**: 3 hangers, 3 platforms, 1 skid set in the infeed, 5
  powertrains on the feeder. On top of that, a restricted area caps the marriage zone at 2 platforms, and a queue
  holds up to 3 more.
- Workers on the platforms are 3D decoration only; labour is inside the Delay times.

## Key settings worth copying
- **Readiness-gated release:** Hold *Conditional* with the **Blocking** condition `hooksReady == 0 || platformsReady == 0`
  (true = wait). The counters go up in *On enter* and down in *On exit* of the hangers' Pickup and of Match port 1.
  Each increment is followed by `stop.recalculateConditions()`, because the Hold never re-tests on its own
  (Help 8.9.10 `hold.html`).
- **One-per-signal gates:** Holds in *Block automatically after N agents*, reopened together by `unblock()` from the
  exit Convey's *On exit*.
- **Work while moving:** `Split` (default copy) → the original is conveyed and the copy runs the work → `Combine`
  with *The resulting agent is* = agent1 (`Combine.ENTITY1`). The zone takes max(travel time, work time) and the
  conveyor never stops.
- **Mounting modules on a carrier:** the Pickup's *On pickup* calls a function of the container that stores a
  reference and `take()`s the module into an `Enter` block **inside the carrier type**. The module then lives in the
  carrier's space and moves with it. That Enter's `Exit` clears the network with `setNetwork(null)`.
- **Handing an agent back to Main:** Dropoff *On dropoff* runs `agent.setSpace(this)` and then `agent.setXYZ(...)` at
  the container's position plus a z offset. `setSpace` keeps the old coordinates and must not be called on a moving
  agent (Javadoc 8.9.10), so always set the position right after it.
- **Vertical lift inside a module:** an embedded flowchart Enter → Delay *until stopDelay()* → `MoveTo` to (x, y, z+20)
  with *Movement defined by: Trip time* = 2 min → Exit. The host starts it with a function that calls
  `stopDelayForAll()`.
- **Fixed fleets:** On startup injects 3 hangers, 3 platforms with tables, one infeed set and 5 powertrains.
  Everything after that is one-out-one-in.

## KPIs instrumented
n/a — the example has no datasets or charts (it is an animation-led demo). Natural measurement points: interval
between cars on the exit conveyor (line takt), time a skid waits at the Hold (carrier starvation), `readyToMarriage`
queue length, and occupancy of the restricted zone.

## Pitfalls
- **Combine pairs by arrival order, not identity.** It works here because the copy branch keeps the order (one copy
  per original, capacity-1 Delays). If copies can overtake each other, rejoin with `Match` on an id (Help 8.9.10
  `split.html`).
- **Forgetting `recalculateConditions()`** leaves the infeed blocked after a hanger or platform becomes ready, and
  nothing reports an error.
- **Reading the Blocking condition as "go"** reverses the logic.

## Reusable idea
Use a Split/Combine fork-join to model any work done **during** transport (moving assembly lines, work on a moving
platform, in-transit inspection). Pace coupled carrier loops with readiness counters feeding a conditional Hold, plus
one-per-signal Holds released by the downstream "clear" event. That is a pull system with no resource pools.

## When the co-pilot should use this
- Automotive or other final-assembly lines with overhead and floor carriers, and marriage/decking stations.
- Any station where work happens while the product moves (overlap of travel and process time).
- A fixed number of pallets, skids or hangers circulating (carrier-count sizing questions).
- As the reference for Hold's conditional and block-after-N modes, and for moving agents between an embedded carrier's
  space and Main.
