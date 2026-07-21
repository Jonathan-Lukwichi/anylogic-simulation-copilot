# Pattern card — Airport
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (Pedestrian / Agent-Based)
- **Problem it solves:** Sizing airport terminal staffing and layout so that check-in, security, customs, and gate queues stay within service-level targets across a full departure day.

## Block chain
Passengers are generated in four arrival waves that mirror a real flight schedule read from Excel. Each agent enters the terminal via one of four transport modes (bus, fixed-route taxi, personal car/taxi, or coach), then navigates a sequential corridor of service stages: entrance security screening → services before check-in → check-in desks → intermediate security control → customs control → passport control → gate control → exit/boarding. At each stage a `PedGoTo` block moves the pedestrian agent to the physical service zone; a dedicated sub-model (e.g., `SecurityControl`, `CheckIn`, `ServicesBeforeCheckIn`, `ServicesAfterCheckIn`, `CustomsControl`) handles queuing and service. `SelectOutput` blocks route agents to the correct desk or lane based on flight type or passenger category. The simulation clock runs in **minutes** over one full 24-hour departure cycle.

## Resources
- Entrance security control desks: quantity controlled by `entranceSecurityControlsQuantity` parameter; service time mean set via `entranceSecurityControlTimeMean` (seconds).
- Intermediate security control desks: quantity via `intermediateSecurityControlsQuantity`; service time mean via `intermediateSecurityControlTimeMean`.
- Check-in desks: collection `checkInDesks`; opening/closing windows driven by `timeFromCheckInOpeningToDeparture` and `timeFromCheckInClosureToDeparture`.
- Gate and passport control: handled inside sub-agent classes (not parameterised at top level).

## Key settings worth copying
- **Model time unit:** Minute — keeps schedule arithmetic readable while pedestrian speeds stay in m/s.
- **Flight schedule from Excel:** `generateRandomSchedule()` at startup populates a timetable, making it easy to swap in real data without changing model logic.
- **Arrival intensity intervals:** `setIntensitiesIntervals()` shapes the passenger arrival rate into realistic surge/lull patterns around each departure wave.
- **Per-desk propagation:** when a slider changes `entranceSecurityControlTimeMean`, an `OnChange` handler loops over every desk agent and pushes the new mean — a clean pattern for synchronising parameter arrays.
- **Check-in time windows:** `timeFromHighDensityArrivalsStartToCheckInStart` and `timeFromCheckInStartToHighDensityArrivalsFinish` encode the operational window as offsets from the departure time, making schedule sensitivity analysis trivial.

## KPIs instrumented
- Registration (check-in) completion time relative to departure.
- Personnel utilisation at each control stage.
- Queue length and wait time at security, customs, and check-in desks (inferred from `PedWait` blocks and desk-level statistics).
- Throughput per transport-arrival cohort.

## Reusable idea
**Schedule-driven intensity + per-resource parameter propagation:** define arrival intensity as a function of a timetable loaded at startup, then expose every resource's capacity and service-time mean as a top-level slider that automatically pushes its new value to every member of the resource array via an `OnChange` loop. This decouples the "what-if on staffing" experiment from the model structure, so a decision-maker can explore dozens of staffing scenarios without touching any logic block.
