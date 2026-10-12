# Pattern card — Create Conveyor Network by Code
- **Source:** AnyLogic example model "Create Conveyor Network by Code" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Build a complete conveyor network at start-up — conveyors (straight and arc), turntable, station, spur, transfer table, turn station, custom station and a position sensor — from code rather than drawn markup.

## Block chain
Markup is built in Main's *On startup*. Flow: `Source` (pull) → `SelectOutput5` (probabilities on three exits) → one of three `Convey` blocks — to the end of `conveyor3` (through the station), to `conveyor4`, or to the custom station — → `Sink`. The flowchart refers to Main variables typed `ConveyorPath<Box>`, `ConveyorTurntable<Box>`, `ConveyorCustomStation<Box>`, etc.

## Resources
n/a

## Key settings worth copying (Help 8.9.10, *Create conveyor network by code*)
- **Conveyor:** `new ConveyorPath<Box>()` — the generic argument is the material item type (`Agent` if you have none) — then `setOwner(this)`, `setObstacle(true)` (blocks transporters), `setWidth(1.0, METER)`. Geometry: `MarkupSegmentLine(...)` or `MarkupSegmentArc(x1, y1, z1, x2, y2, z2, startAngle, endAngle, ratio)` (tangent angles in radians; ratio splits the arc between its two ends), added in order from the start point.
- **Turntable:** place with `setXYZ`, then connect from the conveyors' side: `conveyorIn.setTarget(turnTable)`, `conveyorOut.setSource(turnTable)` — only once those conveyors exist.
- **Transfer table / turn station / custom station:** `addConnection(conveyor, PathEndType.END or BEGIN)`. Transfer table `setSwitchingDelay(5, SECOND)`; turn station `setMode(TURN_STATION_MODE_ORIENTATION or …_ANGLE)`, `setSpeed(…, SpeedUnits.MPS)`, `setRotationSpeed(…, RotationSpeedUnits.RPM)`; custom station outline by `addVertex(x, y)`.
- **Station timing has no setter:** create `ConveyorSimpleStation` on its conveyor as an anonymous subclass that overrides `processTime(Agent agent, List allAgents, TimeUnits tu)`; then `setCapacity`, `setOffset`, `setLength(4, METER)`.
- **Position on conveyor:** anonymous subclass of `PositionOnConveyor(conveyor, offset)` overriding `onLeadingEdgeEnter(Agent agent)` — the signature uses `Agent`, not the item type.
- **Spur:** `new ConveyorSpur(hostConveyor, SHAPE_DRAW_2D3D, true, offset, rightSide, lineColor, fillColor)`; the joining conveyor is attached with `conveyor5.createPort(PathEndType.BEGIN, spur)` **after** `level.initialize()` — Help allows this call only at that stage.
- **Network and level:** `new ConveyorNetwork(this, "codeNetwork")`, `addAll(...)` every element, `new Level(this, "myLevel", SHAPE_DRAW_2D3D, 0)`, `add`, `initialize()`.
- **Draw:** `presentation.insert(0, …)` for the spur and the position; in bulk from `level.getConveyorNetworks().get(0)` via `paths()`, `nodes()`, `getStations()`.

## KPIs instrumented
Console trace from the position sensor only.

## Pitfalls
- The network cannot be modified after `initialize()` (Help): no adding conveyors or stations mid-run.
- A station's time is fixed by the override: read a model parameter inside it if scenarios must change the time.
- Joint geometry: turn stations and transfer tables have size — end the conveyors at the element's edge, not its centre (the demo stops 5 px short).
- Every element needs `setOwner(this)` and a place in `addAll(...)` (Help repeats the owner step for each shape); after start-up, compare the counts of `paths()`, `nodes()` and `getStations()` with your input table.

## Reusable idea
Generate long or repetitive conveyor systems (sorters with dozens of chutes, loops per zone) from a table of segments and junction types with this recipe; keep per-element behaviour in overrides so that it can read scenario parameters.

## When the co-pilot should use this
When a conveyor layout must be created from CAD/table data or varied per scenario at run start; when a user asks for the Java names of MHL markup classes. For editable generated markup use the design-time API (`videos/layout-candidates-and-design-time-api.md`). Related: `create-road-network-by-code.md`, `create-transporter-network-by-code.md`, `videos/mhl-conveyor-types-spur-priority-transfer-elements.md`.
