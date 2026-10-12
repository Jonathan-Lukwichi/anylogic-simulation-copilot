# Pattern card — Railway Track Reservation
- **Source:** AnyLogic example model "Railway Track Reservation" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Rail Library)
- **Problem it solves:** Keep trains of two lines apart at a level (diamond) crossing with the Rail Library's built-in track reservation, instead of a resource-pool interlocking.

## Block chain
Two independent lines, each its own railway network: entry track → switch → short **crossing track** → switch → exit track. The two crossing tracks cross geometrically but share no switch.
- Per line: `TrainSource` (arrivals by `inject()`, 5 cars, placed at a Position on track on the entry track) → `TrainMoveTo` (route calculated automatically, target = a Position on track on the exit track) → `TrainDispose`.
- `TrainSource` *On exit*: `reserveCrossingTracks(train)` — if **both** crossing tracks are available for this train, reserve both for it.
- A Position on track just past each line's exit switch, *On train exit*: `cancelReservations(train)` — cancel both reservations.
- `TrainDispose` *On enter* calls `injectTrains()`: when both disposes have counted the same number of trains, two events are restarted with `uniform(0, 5)` s delays, so the next pair arrives almost together.

## Resources
n/a — the reservation is the lock. Cars: first car a 14 m locomotive, then 27 m coaches (`carLength = carindex == 0 ? 14 : 27`; *Car setup* flags `car.isLocomotive` for index 0).

## Key settings worth copying
- **Railway track API (Help 8.9.10, *Railway track*):** `reserveFor(Agent... trains)` lets only the listed trains use the track; `reservations()` lists them; `cancelReservation()` frees it; `isAvailableFor(train)` checks blocking **and** reservation; `block()` / `unblock()` / `isBlocked()` close a track to everyone; `getTrains()`, `isEmpty()`, `nCars()` tell who is on it.
- **Reserve the other line's piece too.** Each train reserves its own crossing track and the other line's. Trains of the other line then find their crossing track unavailable and stop at the switch in front of it.
- **What a train does when a track becomes unavailable (Help):** not yet moving → the track is left out of its route; moving and following switches, or with that track in its route → it stops at the switch just before the track and waits; with automatic routing, `TrainMoveTo` may instead recalculate the route (`basicmodels/blocking-railway-tracks.md`). A train already on a blocked track may leave it but not come back.
- **Release by the tail:** a Position on track fires *On train enter* when the first car reaches it and *On train exit* when the last car leaves it. Release in *On train exit* of a position beyond the crossing. A reservation also ends by itself once all the trains it was made for have passed the track.

## KPIs instrumented
None (visual demo). Worth adding: wait time at the switch before the crossing, trains per hour through the diamond, and the number of reservation attempts that failed.

## Pitfalls
- **Errors, not queues (Help):** only one train at a time can hold a track's reservation; reserving an already-reserved track raises an error, and so does reserving a track while another train is passing through it. Check `isAvailableFor(train)` and `getTrains()` for **every** track first and reserve all-or-nothing.
- **No retry built in.** In the demo a train that finds the crossing reserved does not reserve later; it waits at its switch and crosses unreserved once the holder cancels. That is safe with two trains only. With more traffic, retry the reservation when the holder releases, or keep a waiting list per crossing (`models/level-junction.md`).
- **Diamonds are invisible to collision checks.** Tracks crossing without a switch are not checked (G52), so a crossing without reservation or a lock lets trains pass through each other silently.

## Reusable idea
Treat a route as the set of tracks it occupies: lock them all at once with `reserveFor` when the train is cleared to go, and free them from the tail-detection callback of a Position on track. The alternative with a capacity-1 `ResourcePool` per section, which queues waiting trains for you, is in `bigbook/rail-traffic-control-block-locking-and-lookahead.md`.

## When the co-pilot should use this
Level crossings between lines, single-track sections, route setting through a switch zone, and shunting moves that must hold a path. Prefer reservation when the lock must follow a specific train and be visible on the markup; prefer a resource pool when many trains queue for the same section.
