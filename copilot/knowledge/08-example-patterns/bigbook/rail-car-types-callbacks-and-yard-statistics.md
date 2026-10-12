# Pattern card — Rail car types, per-car setup, and yard-wide statistics through RailSettings callbacks
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 9 "Rails and trains" — distilled, original wording
- **Paradigm:** DES (Rail Library)
- **Problem it solves:** Give cars their own types, lengths and data, and measure per-car KPIs (dwell, distance run, passes over a point) without threading every car through extra blocks.

## Mechanism
Checked against Help 8.9.10 (*TrainSource*, *RailSettings*, *RailCar*, *Train*, *Switch*).
- **Car type by position in the train.** TrainSource's *New rail car* field (dynamic):
  `carindex == 0 ? new Locomotive() : (carindex < 3 ? new TankCar() : new BoxCar())`.
  Create the types with the *Rail Car Type* element; its wizard offers ready 3D models (e.g. Locomotive 14.1 m, Passenger Car 27 m).
- **Car length by position.** *Car length*: `carindex == 0 ? 14 : 27`. It must match the 3D objects: custom animation is not rescaled to the car length (Help), so the default 14 m makes longer models overlap. A longer train also needs a new entry offset so it fits when created (G29).
- **Per-car data at creation.** *Car setup* runs once per car, with `car`, `carindex` and `train` in scope:
  `if (car instanceof TankCar) ((TankCar)car).timeEntered = time();`
  Help advises initialising cars here rather than in the car type's On startup, whose order is not guaranteed. `setLength()` works only before the car enters the yard; car length cannot change afterwards.
- **Yard-wide callbacks.** RailSettings is one detached block with these actions: *On enter yard*, *On exit yard*, *On enter track*, *On exit track*, *On at switch* (the switch can still be changed there), *On car hit car*, *On car clicked* and *On at callback*.
  - Set its Advanced *Car type* to your class to read fields without casts.
  - Dwell example (book): *On exit yard* `if (car instanceof TankCar) lengthOfStay.add(time() - ((TankCar)car).timeEntered);`, where `lengthOfStay` is a Histogram Data element with 20 intervals.
- **Point sensors on a track.** `car.callbackAt(track, offsetMetres, info)`, or `callbackAt(track, positionOnTrack, info)`, runs *On at callback* when the car's leading side reaches the point. A car holds one request at a time: each new request replaces the previous one, and a request is cleared just before it fires, so re-arm it inside the callback when needed (Help).

## Resources
n/a

## Key settings worth copying
- **Train API** (Help *Train*):
  - `getDistanceDriven()` / `resetDistanceDriven()`, `getSpeed(KPH)`;
  - `setCruiseSpeed(v, KPH)` (must be > 0);
  - `accelerateTo(v)`: only while moving, and it cannot stop the train;
  - `setSpeed(v)`: immediate, and not 0 while moving;
  - `pauseTrain()` / `resumeTrain()`, `getAllOccupiedTracks()`, `distanceToTrain(other, frontSide)`.
- **Track and switch API:**
  - track `nCars()`, `getCar(i)`, and `getFreeSpace(fromStart)`, which returns infinity on an empty track and a negative value when a car straddles that end (Big Book p. 5);
  - switch `getToggleCount()`, `toggle()`, `connectTracks(from, to)` (Help *Switch*).
- **No locomotive concept** in the Rail Library: any car can lead, and speed and acceleration belong to the train (Help).

## KPIs instrumented
- Per-car length of stay (histogram).
- Car-km per type: sum `getDistanceDriven()` in *On exit yard*.
- Switch operations: `getToggleCount()`.
- Cars on a track: `nCars()`.

## Pitfalls
- **A deterministic yard gives a lumpy histogram** (the book's four spikes). Add variability in arrivals, shunting times or speeds before reading distributions.
- **`getCar(i)` on a plain `Agent` train will not compile.** It needs a custom Train type (`bigbook/rail-consist-coupling-decoupling-mechanics.md`).
- **RailSettings callbacks run for every car.** Put a cheap type test first.
- **Guard comparisons against the infinity** that `getFreeSpace` returns on an empty track.

## Reusable idea
Instrument the yard at the infrastructure level (RailSettings callbacks and `callbackAt` sensors) and the cars at birth (Car setup), instead of adding timing blocks to every branch of the train flowchart.

## When the co-pilot should use this
- Rail models that need per-car or per-type KPIs (dwell, detention, car-km), mixed consists with real 3D lengths, or point events (axle counters, signals, level-crossing triggers).
- Related: G29; `bigbook/rail-traffic-control-block-locking-and-lookahead.md`; `bigbook/rail-consist-coupling-decoupling-mechanics.md`.

## Additions (8.9.10 review, 2026-10-01)
- Random consists: `randomlyCreate(OpenCar.class, BoxCar.class, …)` or `randomlyCreate(OpenCar::new, …)`, each with an optional leading `Random` (Help 8.9.10 *Selecting random…*); it returns null if given nothing, and Help does not state the weights *(equal chance — unverified)*. The Hump Yard's *New rail car* uses `carindex == 0 ? new Locomotive() : randomlyCreate(...)`; set *Car length* per type through the local `car`, since custom 3D shapes are not rescaled.
