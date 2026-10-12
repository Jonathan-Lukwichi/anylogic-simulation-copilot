# Pattern card — Rail consist operations: decouple by content, couple on contact, and the port that keeps its identity
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 9 "Rails and trains" — distilled, original wording
- **Paradigm:** DES (Rail Library)
- **Problem it solves:** Split a train according to what its cars carry, shunt the parts, and couple them again with the right car order, orientation and surviving train object.

## Block chain
The book's example 9.3 is a small classification yard on the passing-loop layout. Trains arrive as locomotive + tank cars + box cars.
1. **Split.** `toMain` → `decoupleTanks` (TrainDecouple, number of cars = `nCarsToDecouple(train)`).
   - The front part, locomotive plus tanks, leaves via `outDecoupled`: `tanksToC` (forward onto trackC) → `tanksToD` (Backward onto trackD, *Check free space on target track*).
   - The box cars leave via `out` and stay on trackB.
2. **Loco run-around.** `decoupleLoco` (1 car) → `locoToC` (target: an offset on trackC of `train.getLength() + 10`, which scales with the train's own length; check which end *Offset from* counts from, since Help gives End of the track as the default) → `locoToBoxes` (Backward, towards the start of trackB, *Check free space*). The locomotive stops on touching the box cars and exits via **`outHit`**, then goes into `coupleBoxes` (TrainCouple) → `boxesToExit` → TrainDispose.
3. **Accumulate and clear.** On trackD, tank cuts couple to each other through `coupleTanks`. SelectOutput `tanksNotReady` tests `agent.size() < 8`.
   - Its false exit's action calls `locoSource.inject()`. `locoSource` is a TrainSource in *Calls of inject() function* mode, creating one car with *Orientation on track: Backward* so that the locomotive couples at its rear.
   - The locomotive then hauls the cut away, backwards.

The decouple → sort → couple pipeline is already in the KB (`models/classification-yard.md`, `basicmodels/hump-yard-phase-2..4.md`). This card adds the mechanics.

## Resources
n/a. Track space is the capacity.

## Key settings worth copying
- **Decouple by content.** A function `int nCarsToDecouple(Train train)` counts from car 1 while `train.getCar(n) instanceof TankCar` and returns n, which includes the locomotive.
  - TrainDecouple's *Decouple* setting chooses *First cars* or *Last cars* (Help).
  - A count of 0 sends the whole train to `out`; a count equal to the train length sends it all to `outDecoupled`.
- **A custom Train type is required** for `size()`, `getCar(i)` and your own fields in later blocks.
  - Set it in *New train* of **every** block that creates trains: TrainSource, and TrainDecouple, whose default is plain `Agent` (Help).
  - To read those fields in TrainCouple's actions, also set its Advanced *Train type (1)/(2)*.
  - The book's `agent.size() < 8` compiles only because `decoupleTanks` creates `Train` objects.
- **TrainCouple ports decide which train survives** (Help). The cars of the `in2` train are added to the `in1` train, and the `in2` train object is disposed. The `in1` train keeps its orientation, speed and other properties, and no car moves. Put the train whose identity and attributes must carry on (order id, statistics) on `in1`.
- **Coupling needs contact.** Bring one part in with *Check free space on target track*, so it stops at the first car it meets. That check reads the target track only when the train enters the TrainMoveTo; later changes on the track are ignored (Help). A train that touches another leaves via `outHit`, otherwise via `out`, so wire both ports.
- **Zero-time operations.** Coupling and decoupling take no time; add a Delay after them for the real duration (Help).

## KPIs instrumented
- Per-car dwell in the yard: see `bigbook/rail-car-types-callbacks-and-yard-statistics.md`.
- Cuts waiting on each side of a coupling block: `coupleTanks.size1()` and `size2()` (Help).

## Pitfalls
- **Direction changes need separate blocks.** B → C runs forward and C → D backward, because TrainMoveTo does not reverse within a route (G28).
- **Physical and logical queues differ.** Cars standing on track D are, in the flowchart, waiting inside TrainCouple's queues. Count them there as well as with the track API.
- **Orientation after coupling follows `in1`.** The book's departing cut therefore leaves in the *Backward* direction.
- **Decoupling cuts only at an end.** To take cars out of the middle, decouple twice.

## Reusable idea
Treat a consist as an ordered list with a head: decoupling splits the list at an index computed from its contents, and coupling appends the `in2` train to the `in1` train. Decide which part keeps its identity before choosing the ports.

## When the co-pilot should use this
- Shunting, classification, hump or train-formation models; locomotive run-arounds; any "split by type, then re-assemble" rail task.
- Related: G28, G29; `models/classification-yard.md`; `basicmodels/hump-yard-phase-2.md` to `-phase-4.md`; `bigbook/rail-traffic-control-block-locking-and-lookahead.md`.
