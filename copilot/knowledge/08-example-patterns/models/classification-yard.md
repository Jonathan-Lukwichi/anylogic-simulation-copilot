# Pattern card — Classification Yard
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulate the sorting and re-assembly of mixed-consist freight trains in a rail classification yard, measuring throughput and switch utilisation.

## Block chain
Incoming trains (each carrying a locomotive plus cars of three mixed types — boxcar, hopper, tank) arrive at the entry track via a TrainSource. Each train travels to a set of disassembly tracks where repeated TrainDecouple blocks separate the locomotive from the freight cars. A SelectOutput router then directs each car to a type-specific staging track based on its RailCarType enum value. Once enough cars of the same type have accumulated, a TrainCouple block assembles them into a new homogeneous consist. The rebuilt train then moves via TrainMoveTo blocks to a departure track and is removed by TrainDispose. Queue blocks hold locomotives while their cars are being sorted, preventing the locomotive from blocking the inbound lead.

## Resources
- Rail tracks and switches defined as geometric objects in the Rail Library yard layout (no pooled resource blocks; capacity is determined by physical track length)
- Locomotive staging queue (locoToWait) holds one locomotive per disassembly operation
- Three typed assembly tracks, one per car type (boxcar, hopper, tankcar)

## Key settings worth copying
- **Car-type assignment:** `uniform_discr(0, 2)` picks a RailCarType at random for every non-locomotive car, producing balanced but stochastic mixed consists
- **Train size:** replication count of 100 cars per train agent controls consist length; offset spacing of `trainSizeWithLoco * 15 + 15` meters sets physical buffer between cars on track
- **Speed units:** MPS (metres per second) on all TrainMoveTo blocks — convert to km/h when configuring cruiseSpeed and initialSpeed parameters
- **Time unit:** Minutes — all interarrival and delay values should be expressed in minutes
- **RailCarType enum:** {Locomotive, Boxcar, HopperCar, TankCar} — extend this list to model additional car classes

## KPIs instrumented
- Classification yard performance statistics collected at runtime (stated in model description)
- Car speed at any moment readable via `selectedCar.getSpeed()` (used in on-screen display)
- Implicit throughput: number of homogeneous trains departed per simulation hour

## Reusable idea
The key transferable trick is the **decouple-sort-recouple pipeline**: use TrainDecouple to atomise an incoming mixed batch into individual entities, route each entity by attribute to a typed accumulator, then fire TrainCouple only when a full homogeneous batch is ready. This pattern applies anywhere you need to sort a heterogeneous arrival stream and re-batch by category (e.g., parcels by destination zone, pallets by SKU family, hospital samples by test type).
