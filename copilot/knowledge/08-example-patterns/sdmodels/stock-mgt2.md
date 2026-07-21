# Pattern card — Stock Mgt2
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models inventory replenishment dynamics where orders adjust a supply line to close gaps between desired and actual stock levels, capturing oscillation and delay effects.

## Block chain
Stock (units on hand) accumulates inflow from Acquisitions and loses outflow via Discards. Orders placed enter a Supply Line (pipeline stock) and flow out as Acquisitions after an average acquisition delay. Order Rate is calculated as Indicated Orders clamped to non-negative values. Indicated Orders = Expected Losses + gap correction for stock + gap correction for supply line. Pink Noise (first-order autocorrelated noise built from White Noise via exponential smoothing) drives a configurable Desired Stock signal that can switch among step, pulse, ramp, sine wave, or random-noise test inputs.

## Resources
- **Stock:** units on hand (initial value = Desired Stock Initial)
- **Supply Line:** pipeline of ordered-but-not-yet-received units
- **Average Life:** 8 years (constant discard rate = Stock / Average Life)
- **Acquisition Delay:** average lag between ordering and receiving; also tracked as an information delay (Expected Acquisition Delay)

## Key settings worth copying
- **Time unit:** Day
- **White Noise sampling:** `uniform()` drawn once per time step via a dedicated event, stored as `WhiteNoise_random`
- **Pink Noise:** first-order exponential smoothing of White Noise; correlation time constant is a user parameter
- **Desired Stock test inputs:** step (step time), pulse (pulse time), ramp (ramp start/end), sine (period ≈ 50 weeks), random noise — all selectable via an Input switch variable
- **Stock Adjustment Time** and **Supply Line Adjustment Time**: separate time constants governing how quickly each gap is corrected
- **Order Rate** floored at zero; cancellations modelled as a separate outflow (design note, not implemented here)
- Converted from Vensim STOCKMG2.MDL — parameters follow Sterman (2000) textbook §17.3

## KPIs instrumented
- Stock level over time (oscillation amplitude, settling time)
- Supply Line (on-order quantity)
- Order Rate (bullwhip visibility)
- Acquisition Rate
- No explicit cost or utilisation KPIs; focus is on dynamic behaviour patterns

## Reusable idea
The key transferable trick is the **dual-gap ordering policy**: order rate = expected losses + (desired stock − actual stock) / stock adjustment time + (desired supply line − actual supply line) / supply line adjustment time. Tracking and correcting *both* the inventory gap and the pipeline gap simultaneously dampens bullwhip oscillations compared to naive stock-only policies. Pair this with a Pink Noise demand driver (white noise → first-order smoothing) to stress-test any replenishment policy with realistic correlated demand fluctuations without needing empirical data.
