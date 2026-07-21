# Pattern card — Fulfillment Center Conveyor System
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulates multi-level order fulfillment where items travel through picking, packing, QA, and loading-dock stages on an interconnected conveyor network, letting engineers find bottlenecks and test layout configurations before physical build.

## Block chain
Orders are generated at a configurable arrival rate and enter the conveyor network at the main induction point. They ride conveyors through two distinct picking zones (a bottom picking area and an upper picking area), each modelled as a reusable sub-model connected to the shared network via NetworkPort markup elements. After picking, a SelectOutput block routes correctly-picked orders along one Convey path toward a carton-making area and then through package lines and quality-assurance inspection. Orders flagged as picking errors branch to a separate re-work or rejection Sink. Correctly packaged cartons continue on the dock conveyor sub-system, where a helper function `getRandomDockConveyor()` selects one of several outbound loading-dock lanes at random, distributing outbound load across dock doors. Each major zone (picking areas, smart racks, rack filling, rack outfeeding, carton making, package-and-QA lines, dock conveyors) is its own reusable agent type with exposed NetworkPort interfaces, so the overall model snaps them together like modules. A SmartRack sub-model handles automated rack storage and retrieval feeding the picking workplaces. Time unit is seconds.

## Resources
- Multiple conveyor paths (conveyor, conveyor1–conveyor4, conveyor7, dock conveyor lanes) — capacity governed by physical belt length and speed settings
- Picking workplaces per picking area — act as service resource points
- Smart rack storage — finite rack capacity modelled in the SmartRack sub-model
- Loading dock doors — pooled and randomly assigned via `getRandomDockConveyor()`

## Key settings worth copying
- **Arrival rate:** parameterised `rate` on the Source block; swap in a `rateSchedule` or `rateExpression` to model wave-picking demand
- **Picking time distribution:** `triangular(0.5, 1, 1.5)` seconds per item at picking workplaces — fast, realistic, easy to tune
- **Error routing:** `SelectOutput` with a probability condition splits correct vs. mis-picked orders — set the error-rate parameter at startup to stress-test QA capacity
- **Multi-level network stitching:** NetworkPort elements on each sub-model expose entry/exit connection points; the parent Main model wires them together without rewriting conveyor logic
- **Dock lane selection:** `randomFrom(docksConveyorSystem.loadingDockConveyors)` — one-liner load balancing across dock doors
- **Startup parameter:** number of conveyor parts / rack sections configurable at model initialisation, not hard-coded

## KPIs instrumented
- Throughput: orders reaching each Sink (correctly shipped, rejected)
- Conveyor utilisation: proportion of belt time carrying items vs. idle
- Picking workplace utilisation: inferred from time items spend at picking blocks
- Queue buildup: item count at each NetworkPort junction reveals bottleneck zones
- Dock lane balance: distribution of orders across loading dock conveyors

## Reusable idea
Decompose a large material-handling layout into independent sub-model agents (each zone is its own class) and stitch them together through NetworkPort interfaces — this lets you swap, replicate, or reconfigure any zone without touching the rest of the model, turning a single simulation into a reusable layout-design toolkit.
