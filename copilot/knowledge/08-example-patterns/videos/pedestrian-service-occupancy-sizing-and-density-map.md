# Pattern card — Pedestrian services: a gate is blocked far longer than its delay, and `getUtilization()` does not show it
- **Source:** AnyLogic 8.9.10 Help tutorial "Subway Entrance (Pedestrian Library)" — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Size fare gates, ticket machines or check-in counters in a Pedestrian Library model without trusting a delay-only queueing estimate or a flattering utilization figure.

## Block chain
`PedSource` (at `entryLine`, 4,000 per hour) → `PedSelectOutput` (0.9 straight on, 0.1 to buy a ticket; unused exits 0)
→ [`PedService` `atTVM`: ticket machines] → `PedService` `atFareGates` → `PedGoTo` (`targetLine`) → `PedSink`.
- Ticket machines: *Service With Lines*, type **Point**, 7 services and 7 queues, delay `triangular(7, 12, 40)` s.
- Fare gates: *Service With Lines*, type **Linear**, 8 services and 8 queues. The tutorial text gives a delay of 2–3 s;
  the shipped 8.9.10 *Subway Entrance Hall - Phase 4* uses `uniform(1.5, 3.0) * second()` with the field in minutes.
- A Density Map element over the hall.

## Resources
Service points only. *Number of services* and *N of queues* are set together, one queue per gate.

## Key settings worth copying
- **What occupies a service** (Help 8.9.10, *Services*): a service counts as occupied from the moment a pedestrian
  heads for it. The occupancy covers:
  - the walk from the queue head;
  - the delay (at a linear service's start point, or at a point on a point service);
  - for a linear service with *Wait for exit*, the walk to the end of the line;
  - the *Recovery delay* set in `PedService`.
- **What `getUtilization()` counts** (Help, *Service with Lines*): only the time a pedestrian is being served at the
  point. The walk to the service and the recovery time are excluded, so a low utilization can sit beside a growing queue.
- **The tutorial's evidence:** at 4,000 per hour, 6 gates gave long lines, 7 gates still let the queues grow in a long
  virtual-time run, and 8 gates coped. A delay-only estimate is 1.11 per s × 2.5 s ≈ 2.8 busy gates, which puts 6 gates
  near 46 % load. The runs imply an effective hold per passenger per gate of about 6.3–7.2 s: 7 gates too few means at
  least 7 ÷ 1.11 ≈ 6.3 s, 8 enough means below 8 ÷ 1.11 ≈ 7.2 s. That is roughly 2.5–3 times the delay *(inferred
  from the tutorial's numbers)*.
- **Pick the markup type:** *Service With Lines* for physical queue lines (plain or serpentine); *Service With Area* for
  ticket-number systems where people wait in an area (bank, information desk). *Linear* for walk-through gates
  (*Bidirectional* optional; *Wait for exit*: yes for a security check, no for a turnstile). *Point* for machines and
  counters.
- Queue selection: `PedService` *Queue choice policy* is Shortest, Closest or Other. The service's *Serve pedestrians
  from* is Longest, Closest (strict), Closest not empty, Round robin, Priority or Other.
- `PedSource` defaults set the walking share (Help): comfortable speed `uniform(0.5, 1)` m/s, initial speed
  `uniform(0.3, 0.7)` m/s, diameter `uniform(0.4, 0.5)` m.

## KPIs instrumented
- Queue length on a time plot over a long run in virtual time: judge the trend, not the animation.
- Throughput per gate at saturation, giving the effective hold = open time × gates ÷ passengers served.
- **Density Map (8.9.10):**
  - *Based on* Space (pedestrian maps are space-based only); *Type* Pedestrian;
  - red from *Critical density*, 1.5 per m² by default; Logarithmic colours by default;
  - *Time period*: Complete model run (default) or Sliding window; *Displayed density value*: Maximum or Mean;
  - only one density map of each type may sit on a level, otherwise an error is raised.

## Pitfalls
- **The machine's "average 12 s" is a mode.** `triangular(7, 12, 40)` averages 19.7 s (G55). An estimate built on 12 s
  makes each machine look about 1.6 times faster than it is.
- **A maximum map remembers one surge.** With attenuation off the map keeps the maximum ever seen, so one crowd wave
  paints a zone red for the rest of the run. Use a sliding window with Mean for typical conditions.
- Keep target lines and services inside the walls, and chain blocks through their side ports only.

## Reusable idea
In pedestrian models a server's capacity is set by movement as much as by service time. Measure the effective hold in
the model, then size, and confirm the choice with a long run.

## When the co-pilot should use this
- Stations, airports, stadium gates, security lanes, ticket halls: any Pedestrian Library service sized by count.
- Symptoms: queues grow although utilization looks moderate, or a delay-based calculation says half the gates would do.
- Related: G55; `models/subway-platform.md`; `videos/cad-drawing-to-pedestrian-walls.md`.

## Additions (8.9.10 review, 2026-10-01)
- Queue selection policies (Help 8.9.10 *Service with Lines*): *Closest queue (strict)* makes each point serve only its nearest queue even when that queue is empty — a dedicated-lane rule that can leave a point idle while other lines wait; *Priority queue* evaluates its expression (local `queue`) for every non-empty queue each time a point frees; *Other* evaluates an expression with local `serviceUnit` that returns the `QueueUnit` to serve.
- A Queue Line can *Extend queue to the free space* when the drawn line is full: the queue continues along the line's last segment until it meets a wall. This is separate from the logical cap *Maximum number of people in the queue* (Help 8.9.10 *Queue line*); the shipped *Subway Entrance Hall - Phase 4* uses it on every line.
