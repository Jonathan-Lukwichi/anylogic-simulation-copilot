# Pattern card — Conveyor Singulator
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Merging multiple parallel conveyor feeds into one ordered single-file line without collisions, using priority-based spur merging.

## Block chain
Three independent Source blocks feed three separate Convey segments (feeder lanes). Each feeder lane connects to a magistral (main) conveyor line via a ConveyorSpur junction. The ConveyorSpur gates control which feeder is allowed to insert items onto the magistral belt at any moment, enforcing gap-based singulation. Items travel the magistral Convey segment to a shared Sink. A fourth injection path lets operators push a batch of high-priority items directly onto the magistral, overriding all feeder lanes. The model exposes interactive buttons to switch which feeder conveyor holds the higher merge priority, and an "equal priority" mode where the three lanes compete symmetrically.

## Resources
- Three feeder Convey segments (parallel input lanes)
- One magistral Convey segment (single-file output lane)
- Two ConveyorSpur merge points connecting feeders to magistral
- No human resource pools; capacity is governed by belt speed and item spacing

## Key settings worth copying
- **Time unit:** seconds
- **Merge priority on the incoming conveyors:** *(corrected 2026-09-28 against Help 8.9.9, markup/conveyor)* priority is a property of each conveyor that feeds the junction — not of the spur — and the conveyor with the **greater** Priority value wins the merge; ticking *Maximum priority* makes a conveyor beat all connected ones. Changing the values at runtime re-balances the merge without stopping the model
- **Rate (arrival rate):** configured per Source block; supports `rate`, `rateSchedule`, and `rateExpression` modes — use `rateExpression` to make arrival vary with simulation time
- **removeFromConveyor flag on Convey:** *(corrected 2026-09-28)* this is the Java name of Convey's *Leave conveyor on exit* — it takes the item off the conveyor network when it reaches that block's target (tick it on the final Convey before a Sink or a holding block, gotcha G42); it is not a feeder-to-main hand-off setting
- **sourcePositionOnConveyor / targetPositionOnConveyor:** specify the exact belt offset (metres) where a spur handoff occurs — set these to match the physical gap between belts

## KPIs instrumented
- Throughput count at the shared Sink (items processed per unit time)
- Visual observation of lane flow balance under different priority settings
- Queue build-up on feeder lanes visible via conveyor occupancy animation

## Reusable idea
The transferable trick is **runtime priority flipping at a merge**: by exposing one priority value per feeding conveyor (higher wins) and wiring it to a UI control or schedule, you can dynamically rebalance which feeder lane dominates the merge point without halting the simulation. This pattern applies any time you need to model a merging junction (assembly line confluence, port gate allocation, road on-ramp merging) where priority rules must change mid-run to test different policies.
