# Pattern card — Stock Mgt1
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models inventory and supply-line management under uncertain demand, showing how ordering policy choices drive oscillation or stability in stock levels.

## Block chain
Three coupled stock variables drive the model:

1. **StockS** — the physical inventory; grows via AcquisitionRateAR and drains via LossRateLR (first-order decay based on average lifetime).
2. **SupplyLineSL** — units on order but not yet received; fills from OrderRateOR and empties as AcquisitionRateAR delivers them after an acquisition lag.
3. **PinkNoise** — autocorrelated noise stock that smooths white-noise input into realistic demand fluctuation.

Ordering logic:
- DesiredAcquisitionRateDAR = ExpectedLossRate + AdjustmentForStock (gap between desired and actual stock / StockAdjustmentTime).
- IndicatedOrdersIO = DesiredAcquisitionRateDAR + AdjustmentForSupplyLine (gap between desired and actual supply line / SupplyLineAdjustmentTime).
- OrderRateOR = max(0, IndicatedOrdersIO) — cancellations are excluded; negative orders are floored at zero.
- AcquisitionRateAR = SupplyLineSL / AcquisitionLag.

Demand signal (Input) can be switched between step, pulse, ramp, sine wave, or pink-noise modes, enabling stress-testing of the ordering policy under multiple test inputs.

## Resources
- No agent populations or process-library resource pools — pure SD stocks and flows.
- Key parameters: AverageLifetimeL (default ~8 years / 2920 days), AcquisitionLagAL, StockAdjustmentTimeSAT, SupplyLineAdjustmentTimeSLAT, NoiseCorrelationTime.

## Key settings worth copying
- **uniform()** sampled once per time step (Day) via a timed event to produce WhiteNoise, then first-order smoothed into PinkNoise — a clean pattern for injecting autocorrelated noise into any SD model.
- DesiredSupplyLineSL = ExpectedAcquisitionLag * DesiredAcquisitionRate — anchors the supply-line target to the ordering delay, a standard Sterman anchor formula.
- AdjustmentForStock and AdjustmentForSupplyLine both use proportional gap-closing (gap / adjustment-time), making the policy tunable by changing two time constants.
- Input multiplier on InitialDesiredStock allows all test waveforms to share a single parameter without restructuring the model.

## KPIs instrumented
- StockS trajectory over time (inventory level).
- SupplyLineSL trajectory (pipeline visibility).
- OrderRateOR (ordering behaviour and oscillation amplitude).
- Gap metrics: DesiredStock − ActualStock, DesiredSupplyLine − ActualSupplyLine (implicitly tracked through adjustment flows).

## Reusable idea
The **dual-gap ordering heuristic** — separately correcting for stock gap and supply-line gap, then summing both adjustments into the order rate — is the transferable trick. It prevents the common modelling error of anchoring orders only to the inventory shortfall while ignoring already-in-transit units, which is the root cause of bullwhip oscillations in SD supply-chain models.
