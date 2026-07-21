# Pattern card — Border Checkpoint Optimization
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Determine the right number of car and bus inspectors, per shift, at a border crossing to minimise vehicle wait times without overstaffing.

## Block chain
Vehicles of two types — private cars and buses — arrive at the border at rates that vary by time of day. Cars feed into multi-lane car checkpoint blocks (CarCheckpointLanes); buses enter a dedicated bus lane with its own queue (queueOnBusStop → BusCheckpointLane). Each lane holds a pool of inspectors; once a vehicle clears all checkpoints in sequence the lane releases it and opens for the next. Arrival rates and inspector counts are driven by Excel-sourced schedules, but every schedule can be overridden at run time via a slider, enabling what-if experiments for any single shift without restarting the model.

A companion RLOptimization agent (importing Action and Observation classes) wraps the simulation so a reinforcement-learning policy can adjust nCarInspectors and nBusInspectors dynamically and observe the resulting mean wait time, closing the loop between staffing decision and queue outcome.

## Resources
- **Car inspectors:** integer pool size controlled by `nCarInspectors`; default override value 4; adjustable 0–100 via slider.
- **Bus inspectors:** integer pool size controlled by `nBusInspectors`; default override value 2; adjustable 0–100 via slider.
- Two traffic-light objects gate entry to car and bus lanes independently.

## Key settings worth copying
- **Time unit:** Minute.
- **Arrival rates:** sourced from Excel schedules (`carRateSchedule`, `busRateSchedule`), expressed per hour; sliders allow live override during a run.
- **Inspector schedules:** `carInspectorsSchedule` and `busInspectorsSchedule` also from Excel; checkbox lets the user switch between schedule-driven and constant staffing mid-run.
- **Override pattern:** a boolean flag (`useCarInspectorsSchedule`) selects schedule vs. constant, making it trivial to freeze one shift's staffing while experimenting.
- **RL hook:** Action/Observation interfaces separate the optimisation logic from the simulation model — the same .alp runs in manual, schedule-driven, or RL-driven mode.

## KPIs instrumented
- Mean wait time per vehicle type (plotted on `meanWaitTimePlot`).
- Queue length at car and bus queues (`carQueueToCheckpoint`, `queueOnBusStop`).
- Inspector utilisation inferred from pool occupancy across both checkpoint types.

## Reusable idea
Wrap schedule-driven resource counts in a boolean override flag and expose both the schedule value and the override constant through sliders. This single pattern lets a model serve three audiences simultaneously: operational planners who trust the historical schedule, managers who want to test a fixed staffing level, and optimisation algorithms (including RL) that need to set the value programmatically — all without changing model structure.
