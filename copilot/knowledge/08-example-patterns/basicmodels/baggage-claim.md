# Pattern card — Baggage Claim
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (Pedestrian / DES)
- **Problem it solves:** Models the flow of arriving passengers and their luggage through an airport baggage-claim hall, coordinating two separate entity streams (people + bags) until each passenger picks up their own bag and exits.

## Block chain
Two parallel streams run simultaneously and must rendezvous:

**Passenger stream:** PedEnter → PedWait (waiting at carousel) → PedGoTo (walk to bag) → Pickup (grab matched bag) → PedGoTo (exit) → PedSink

**Baggage stream:** Enter → Delay (loading time, triangular 1–5 min) → Conveyor (carousel loop — two Conveyor segments form a closed belt) → Split (route bags toward waiting passengers) → Queue → Pickup (matched with owner passenger)

A Split block diverts bags either back onto the belt or toward the passenger queue depending on whether the owner is already waiting. The Pickup block is the synchronisation point: a bag stays in Queue until its paired passenger arrives, or vice versa.

## Resources
- Two closed-loop Conveyor belts (carousel segments) with configurable speed
- Pedestrian environment (2-D/3-D space) providing spatial layout and walking physics
- No explicit ResourcePool — capacity is governed by conveyor belt length and pedestrian area

## Key settings worth copying
- **Bag loading delay:** `triangular(1, 2, 5)` seconds — skewed toward short loads with rare long outliers
- **Conveyor speed:** `uniform(0.5, 0.7)` m/s — small random variation across belt segments
- **Passenger arrival position:** `uniform(10, 90)` — random lateral spread along the arrival zone
- **Time unit:** Seconds
- **Agent matching:** each Baggage agent carries a reference to its owner Passenger; Pickup uses this link to pair the two streams

## KPIs instrumented
- Passenger wait time at the carousel (time between PedWait entry and Pickup)
- Baggage carousel utilisation (how full the belt is at any moment)
- Overall throughput: passengers exiting per unit time

## Reusable idea
**Dual-stream rendezvous via agent reference:** the key transferable trick is assigning an owner-reference field on the secondary entity (bag → passenger) and using a Pickup block to hold whichever stream arrives first until its counterpart appears. This pattern applies to any scenario where two independently-paced flows must be matched one-to-one before proceeding (e.g., orders + delivery drivers, patients + test results, parts + workers on an assembly floor).
