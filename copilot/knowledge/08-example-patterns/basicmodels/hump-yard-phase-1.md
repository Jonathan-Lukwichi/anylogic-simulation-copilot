# Pattern card — Hump Yard - Phase 1
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models the physical track layout and movement logic of a rail hump yard, where inbound trains are pushed over a hump and individual cars roll down into sorting tracks.

## Block chain
Inbound train enters via **trackEntry** and halts at **stopLineEntry**. A locomotive pushes the cut over the hump via **railwayTrack** / **trackArrival**, stopping at **stopLineArrival**. Cars are uncoupled and roll past **railwaySwitch** (ALL_TO_ALL) through **railwayTrack2** toward the classification bowl, halting at **stopLineHump**. A second ALL_TO_ALL switch (**railwaySwitch1**) routes individual cars onto designated sorting tracks. All tracks are modelled as bidirectional **RailTrack** path objects inside a **Railyard** network.

## Resources
- Two ALL_TO_ALL **RailroadSwitch** elements controlling diverging routes
- Three **RailStopline** signals: entry hold, arrival/pre-hump hold, and post-hump classification stop
- One **Railyard** (rail network container) housing all tracks and switches
- Agent speed default: 10 m/s (overridden per rail segment by track physics)

## Key settings worth copying
- **ModelTimeUnit:** Minute — keeps delay values human-readable for rail operations
- **RailroadSwitchType: ALL_TO_ALL** — any track can connect to any other track at the switch node; use this when cars fan out to many classification tracks
- Track path type set to `railroad` with 2 m width — activates AnyLogic rail kinematics
- Run duration: 100 minutes (wall-clock scaled 1:1) — enough for several complete humping cycles
- Bidirectional tracks throughout allow the locomotive to pull back after pushing cars over the hump

## KPIs instrumented
- n/a (Phase 1 is a layout/geometry foundation; throughput and queue KPIs are added in later phases)

## Reusable idea
Use **ALL_TO_ALL RailroadSwitch** nodes as fan-out hubs: a single switch object handles N-to-M track connections without manual wiring of every pair. This eliminates the need for individual SelectOutput logic and lets the routing condition live at the car-agent level (e.g., car.destinationTrack), making it straightforward to scale the classification bowl from a handful of tracks to dozens.
