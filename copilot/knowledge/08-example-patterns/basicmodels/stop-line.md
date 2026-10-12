# Pattern card — Stop Line
- **Source:** AnyLogic example model "Stop Line" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Road Traffic Library)
- **Problem it solves:** Impose speed zones, yield rules and signals at points along a road, and measure traffic at those points, with Stop Line markup instead of extra flowchart blocks.

## Block chain
`CarSource` (initial speed 80 km/h, preferred 60 km/h) → `CarMoveTo` (to the road's end) → `CarDispose`, on one road with
two lanes each way. Four stop lines sit along the road, in driving order:
- first (forward lanes): **Speed limit** 30 km/h — start of a slow zone;
- second: **End of speed limit** — cars return to their own preferred speed;
- third (forward) and fourth (backward direction): controlled by a `TrafficLight` in *Specified stop lines* mode,
  4 phases of 10 / 3 / 20 / 3 s.

## Resources
n/a

## Key settings worth copying
- **Road signs** on a stop line (Help 8.9.10, *Stop line*): *Speed limit* (value + units), *End of speed limit*,
  *Yield*; yield can be combined with either speed sign. Code equivalents: `addSpeedLimitSign(30, KPH)`,
  `addEndOfSpeedLimitSign()`, `addYieldSign()`, and the tests `isSpeedLimitSign()`, `getSpeedLimit(KPH)`, `isYieldSign()`.
- **Lane coverage:** a stop line spans a lane range — `getLaneIndexFrom()` / `getLaneIndexTo()` and the setters (lane 0
  is at the road side), so a turn lane can have its own line.
- **Sensors:** *On car passed* (locals `car`, `laneIndex`) acts as a loop detector; `queueSize()` or
  `queueSize(lane)` counts cars waiting before the line; `averageSpeed(KPH)` gives the speed at that spot.
- **Signal by code:** `setSignal(TrafficLightSignal.SIGNAL_RED / …_GREEN / …_NONE)` and `getSignal()` — only for a line
  that no Traffic Light controls. Useful for actuated or ramp-metering logic written as events.
- `CarMoveTo` can target a stop line (stop before it, or drive through it).

## KPIs instrumented
Visual only. With the sensors: flow per lane (counter in *On car passed*), queue length per approach over time, spot
speed inside and outside the zone.

## Pitfalls
- A speed-limit line only starts the zone; without a matching *End of speed limit* line the limit holds downstream
  *(inferred from the sign semantics)*.
- `setSignal()` does nothing useful on a line owned by a Traffic Light; drive signalised lines through the light's API
  (phases, `turnOn/turnOff`, `switchToNextPhase()`).
- Yield and signals stop cars only at the line; interactions with pedestrians still need explicit logic (G27).

## Reusable idea
Treat stop lines as the road network's programmable points: signs for rules, *On car passed* and `queueSize()` for
measurement, `setSignal()` for custom control. Most corridor studies need no extra blocks.

## When the co-pilot should use this
School or work zones, speed-reduction schemes, yield-controlled merges, detector-based counts, and home-made signal
logic (actuated, ramp metering). Related: `../videos/traffic-light-gated-pedestrian-crossing.md` (signalised line + crossing),
`../videos/road-network-descriptor-callbacks-speed-map-deadlocks.md` (network-wide callbacks),
`../models/traffic-light-phases-optimization.md`.
