# Pattern card — Level Junction
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates multi-directional train traffic converging on a shared rail junction, detecting and resolving track conflicts so trains do not collide.

## Block chain
Four directional streams of trains (North, South, West, East) each have their own `MovementManager` agent. Every manager owns a `Source` block that injects trains onto railroad tracks. Trains travel across a central switching zone built from `RailTrack` segments and an `ALL_TO_ALL` `RailroadSwitch`. When a train claims a crossing segment, it blocks that track for all competing directions. On exit from a stop-line (`RailStopLineDescriptor`), the departing train calls `cancelBlockAndRunNextTrains()` on its manager, releasing the crossing for the next queued train. A `waitingTrains` map (keyed by direction pair) holds trains that were blocked mid-route. A startup timer event (`injectTrains`) fires once per second to seed the four directions simultaneously.

## Resources
- 4 `MovementManager` sub-agents (one per cardinal direction): North, South, West, East
- 3D visual assets: locomotive (`locomotive.dae`) + passenger cars (`passenger_car_1.dae`)
- `RailCar` agent type (individual car unit); `Train` agent type (locomotive + cars composite)
- Crossing track sets: 10 directional pairs (NS, SN, NW, SW, SE, EW, WE, WS, WN, ES)

## Key settings worth copying
- Time unit: **seconds**
- Speed units: **MPS** (metres per second) — set on both Train and RailCar agent types
- Injection: periodic `inject()` call into each manager's source, fired at 1 per second (`Rate = 1 PER_SECOND`)
- Conflict map: `crossingTracksMap` is a `Map<RailTrack, List<RailTrack>>` — for each destination track you list the tracks that must be blocked; populated once at model startup in `fillCrossingTracksMap()`
- `RailroadSwitch` type: `ALL_TO_ALL` — allows any-to-any routing through the junction node
- `InitializationDatabaseType`: `ONE_AGENT_PER_DATABASE_RECORD` used to initialise stop-line descriptors from embedded tables
- Agent links: bidirectional `COLLECTION_OF_LINKS` between train units (2 connections per agent)

## KPIs instrumented
- Implicit throughput: number of trains successfully traversing the junction (observable via animation and `waitingTrains` map size)
- Blocking events: size of `waitingTrains` per direction pair indicates congestion hotspots
- No explicit chart-based KPIs in this model — the value is visual 3D demonstration of deadlock-free operation

## Reusable idea
The transferable trick is the **crossing-tracks map pattern**: instead of hard-coding pairwise conflict logic, each `MovementManager` holds a map from "my intended destination track" to "the list of tracks belonging to other directions that must be atomically blocked." On train entry into the junction you lock all tracks in that list; on exit you release them and immediately unblock the next waiting train. This separation of conflict declaration (the map) from conflict enforcement (the enter/exit callbacks) makes it trivial to add new directions or routes without touching existing logic.
