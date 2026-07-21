# Pattern card — Border Checkpoint
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Sizing lanes, inspection bays, and inspector staffing at a mixed-traffic border crossing to minimise vehicle wait times without over-resourcing.

## Block chain
Two independent arrival streams — cars and buses — each feed their own Source block with exponential inter-arrival times (cars: `exponential(2)` minutes, buses at a lower separate rate). Vehicles join a typed Queue before a MoveTo block physically places them on the road network. A SelectOutput routes vehicles to whichever checkpoint lane is available (separate CarCheckpointLanes and BusCheckpointLane sub-models). Inside each checkpoint lane a second SelectOutput dispatches vehicles to one of three InspectionArea sub-models. Each InspectionArea runs a Delay representing the document/luggage check (`triangular(7, 10, 15)` minutes), after which another SelectOutput sends the rare secondary-inspection case to an extended hold (`triangular(0.5, 1, 3)` minutes) while the majority exit. Processed vehicles reach a Dispose (carDispose / busDispose). The number of passengers per bus is sampled with `uniform_discr(1, 4)` and bus length with `triangular(30, 35, 45)` to drive space allocation on the road.

## Resources
- **Inspector pools:** one pool per InspectionArea; capacity configurable (parameter `capacity` on each area).
- **Inspection areas:** three instances (`inspectionArea1`, `inspectionArea2`, `inspectionArea3`) shared across car lanes.
- **Lane capacity:** each Queue and lane block carries its own `capacity` parameter.

## Key settings worth copying
| Setting | Value |
|---|---|
| Time unit | Minute |
| Car inter-arrival | `exponential(2)` min |
| Inspection delay | `triangular(7, 10, 15)` min |
| Secondary hold | `triangular(0.5, 1, 3)` min |
| Bus length | `triangular(30, 35, 45)` units |
| Passengers/bus | `uniform_discr(1, 4)` |
| Secondary-inspection probability | `uniform(0.3, 0.5)` range across lane types |

## KPIs instrumented
- **Inspector utilisation** — live plot (`inspectorsUtilizationPlot`)
- **Throughput** — `throughput` statistic on each InspectionArea
- **Queue length** — virtual counters on carQueueToCheckpoint and busQueueToCheckpoint track vehicles waiting off-screen
- **Lane capacity utilisation** — implicit from Queue size vs. capacity

## Reusable idea
Separate the physical road network (MoveTo + space) from the logical service model (Queue → SelectOutput → Delay) so you can scale inspection bays independently of lane geometry. The three-InspectionArea array (`{ inspectionArea1, inspectionArea2, inspectionArea3 }`) referenced via `agent.checkpoint.inspectionArea` lets each vehicle carry a pointer to its assigned bay, making resource lookup O(1) and trivially extensible to N bays.
