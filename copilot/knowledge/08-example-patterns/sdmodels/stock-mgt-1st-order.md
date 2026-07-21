# Pattern card — Stock Mgt 1st Order
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a stock (inventory or asset base) self-corrects toward a desired level through a first-order negative feedback loop, with various test input patterns to stress-test the controller.

## Block chain
A single stock accumulates inflows (acquisitions) and loses outflows (discards). The acquisition rate is driven by a gap-closing rule: compare the desired stock to the actual stock, divide the gap by an adjustment time, add expected losses, and constrain the result to be non-negative. Discards follow a first-order decay with a constant average asset life. An exogenous "Input" variable can inject step, pulse, ramp, sine-wave, or pink-noise demand signals to test system responsiveness.

## Resources
- One stock variable (the managed inventory/asset level)
- No agent pools or queues — pure SD flow structure
- Pink-noise generator (first-order exponential smoothing of white noise) acts as a realistic random-demand resource driver

## Key settings worth copying
- **Adjustment time:** governs how quickly the gap between desired and actual stock is closed (proportional controller gain = 1 / adjustment_time)
- **Average asset life:** constant first-order discard rate = stock / average_life (default implied ~8 years)
- **Input switch:** selects among step (with start time), pulse (with start time & magnitude), ramp (start/end time), sine wave (period ~50 days/weeks), or pink noise (with correlation time constant)
- **Pink noise formula:** change = (white_noise − pink_noise) / correlation_time, where white_noise ~ uniform() resampled each time step
- **Time unit:** Day; converted from Vensim STOCKMGT.MDL

## KPIs instrumented
- Stock level over time (actual vs desired)
- Acquisition rate and discard rate trajectories
- Gap (desired − actual) to visualise controller performance
- Pink noise signal shape for realism verification

## Reusable idea
The transferable trick is the **gap-closing acquisition rule**: desired_acquisition = expected_losses + (desired_stock − actual_stock) / adjustment_time, clamped to ≥ 0. This one-liner encodes a proportional inventory controller that can be dropped into any SD model where you need a stock to chase a target, and the pink-noise input generator is a ready-made realistic demand disturbance that replaces simplistic step inputs.
