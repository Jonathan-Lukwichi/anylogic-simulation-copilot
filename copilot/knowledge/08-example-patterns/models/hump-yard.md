# Pattern card — Hump Yard
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Simulate rail-car classification in a gravity hump yard to measure how long each car spends waiting for its departure train to fill.

## Block chain

Incoming trains arrive at the yard and are immediately broken apart (TrainDecouple) so that individual rail cars can be sorted. Each car carries a type attribute drawn at random from 15 equally likely categories (uniform_discr(1, 15)). Cars then travel via a series of MoveTo blocks — representing movement along tracks — toward their assigned classification track (one of 15 departure tracks, each mapped to a specific car type). Cars wait on their track inside a Delay block until exactly 20 cars of the same type have accumulated. A SelectOutput block guards departure: cars that do not yet meet the threshold loop back to wait, while the full batch of 20 is coupled into a new train (TrainCouple) and moved out of the yard. The locomotive handling around the hump is modelled as additional Delay + MoveTo steps with a fixed 15-minute shunting allowance. Time in system for each car (from arrival to departure as part of a new train) is recorded and displayed as a histogram.

## Resources

No explicit ResourcePool or staff resources. Capacity is track-based: each of the 15 departure tracks holds cars indefinitely until the batch threshold of 20 is reached. The hump itself is a sequential Delay (15 minutes) acting as a single-track bottleneck.

## Key settings worth copying

- Car-type assignment: `uniform_discr(1, 15)` — equal probability across 15 classes
- Train size parameter: `trainSizeWithLoco` controls how many cars arrive per inbound train; departure trains are always exactly 20 cars of the same type
- Hump delay: fixed 15 minutes (model time unit = Minute)
- 15 departure tracks, each with a named stop-line (`stoplineN1` … `stoplineN15`) for spatial placement of MoveTo targets
- Simulation seeded for reproducible results

## KPIs instrumented

- Distribution of time each rail car spends in the yard (histogram displayed in the UI)
- Implicitly: throughput of fully formed departure trains

## Reusable idea

The key transferable trick is the **batch-threshold gate**: use a Delay block as a staging area and a SelectOutput to recirculate cars that have not yet completed a batch, only releasing the group once a count condition is satisfied. This pattern cleanly models any "collect N identical items then release as one unit" logic — applicable to manufacturing kitting, container-load consolidation, or order batching in a warehouse.
