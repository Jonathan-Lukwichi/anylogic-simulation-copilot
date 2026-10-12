# Pattern card — Tugger Train
- **Source:** AnyLogic example model "Tugger Train" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Move many items per trip with a tow train (tugger pulling trailers) — with a fixed train or with trailers added per item — and decide when a partly loaded train sets off.

This card also covers the sister example "Tugger Train Delivery Policies" (basicmodels, 8.9.10).

## Block chain
- **Parts supply (Tugger Train):** `Source` (5 parts every `uniform(3, 5)` min, each with a random target buffer) →
  `MoveByTransporter` (fleet `partsTuggerTrain`, to `stationsBuffers.get(agent.targetBufferNumber)`, load/unload 10 s)
  → `Delay` 15 s → `Sink`.
- **WIP transfer (Tugger Train):** `Source` (50/h, pull) → `SelectOutput` → `Convey` along line A or B to a random exit
  → `MoveByTransporter` (fleet `productTuggerTrain`, to the processing area, load/unload 5 s) → `Sink`.
- **Policy lab (Delivery Policies):** `Source` (manual) → `Convey` (to the conveyor end) → `MoveByTransporter` (to a
  random station; *Pickup location is* = **Node**, a fixed pickup node) → `Delay` 30 s → `Sink`. Radio buttons call
  `tuggerTrain.set_deliveryStartPolicy(...)` during the run; 20 % of items are urgent (`urgentOrder`, drawn red).

## Resources
- `partsTuggerTrain`: path-guided, *Tugger train* ticked, **fixed** 5 trailers, delivery starts when **full**.
- `productTuggerTrain`: free-space, *Number of trailers* = **equals number of agents** (a trailer appears when an item is
  loaded and disappears when it is unloaded; up to 5), delivery starts on **timeout**.
- Both tick *Recognize all transporters* (mixed navigation types) and put trailers in custom populations. Trailer and
  tugger are ordinary agent types you can draw.

## Key settings worth copying
- TransporterFleet (Help 8.9.10; tuggers exist since **8.9.9**): `isTugger`, *New trailer* (type),
  `trailersNumberType` = `SPECIFIED_EXPLICITLY` (`initialNumberOfTrailers`) or `EQUALS_NUMBER_OF_AGENTS`
  (`maximumNumberOfTrailers`), `tuggerTrailerGap`, `preferPartiallyFilledTransporters`.
- *Delivery starts when* (`deliveryStartPolicy`): `FULL_LOAD`, `TIMEOUT` (with *Pickup timeout per agent*, reset by every
  new item), `NO_AVAILABLE_AGENTS`, `CONDITIONAL` (*Condition*, e.g. `checkPriority((Item) agent)` returning
  `agent.urgentOrder` — an urgent item makes the train leave at once). Policy details: `multiload-transportation-at-storage.md`.
- Tugger type On startup: `setTrailerCargoPosition(0, 0, 0.15, METER)` puts loads on the trailer beds.
- Runtime API (Help, *Transporter API*): `startDelivery()` (8.9.10) forces departure; `getNumberOfTrailers()`,
  `setNumberOfTrailers(n)` (never below loaded + reserved), `nFreeTrailers()`, `getTrailer(agent)`,
  `getControllingAgent()`, `nTransportedAgents()`; state `TransporterState.WAITING` while it waits for more items.

## KPIs instrumented
Visual only. Add: items per trip (`nTransportedAgents()` at departure), time in `WAITING`, trips per hour, empty travel
(`GOING_TO_AGENT`), and wait of the first item loaded until departure.

## Pitfalls
- **Conveyor feed + *no available agents left*:** the next item is still on the belt when the check runs, so the train
  leaves with one item (on-canvas note in the Delivery Policies model). Use *timeout ends*, timeout ≈ item spacing.
- **`FULL_LOAD` can wait for ever** when demand is irregular; the fixed parts train only works because parts come 5 at a time.
- **Delivery order is nearest destination first** (Help, *Tugger trains*), not load order; far stations can wait for
  several stops. Use the route pattern in `tugger-train-operating-on-a-predefined-route.md` for a fixed milk run.
- **Reservations:** while a train is en route, new items reserve trailer space and wait; a reservation is dropped if a
  higher-priority item takes it, capacity shrinks or the tugger enters downtime (Help). With *After cycle* downtime,
  one whole trip counts as one cycle.
- **Help name error:** the Help calls the property `maxNumberOfTrailers`; 8.9.10 defines `maximumNumberOfTrailers` /
  `set_maximumNumberOfTrailers()` (`javap`).
- In racks the train stays in the aisle, and a train longer than a lift platform still enters it with only a warning.

## Reusable idea
A tugger is a transporter with capacity > 1 whose trips are formed by a departure rule. Model the rule explicitly
(full, timeout, condition), measure load per trip and waiting-to-depart time, and compare rules before resizing the fleet.

## When the co-pilot should use this
Line-side supply milk runs, kitting deliveries, WIP shuttles between areas, airport baggage tractors — any "one vehicle,
many loads" transport. Related: `multiload-transportation-at-storage.md`, `tugger-train-operating-on-a-predefined-route.md`,
`../videos/mhl-agv-dispatch-choice-and-cargo-position.md`.
