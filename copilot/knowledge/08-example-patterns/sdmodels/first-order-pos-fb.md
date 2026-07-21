# Pattern card — First Order Pos FB
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Demonstrates pure exponential growth driven by a single positive feedback loop — stock generates its own inflow at a constant fractional rate.

## Block chain
One Stock (`SStateOfTheSystem`) accumulates a net inflow. A Flow (`NetInflowRate`) feeds back into that same stock. An Auxiliary parameter (`AFractionalGrowthRate`) scales the flow: `NetInflowRate = AFractionalGrowthRate × SStateOfTheSystem`. Because the stock drives its own inflow, every unit already in the stock produces more units — the classic self-reinforcing (positive) feedback loop producing J-curve growth.

## Resources
n/a — no resource pools or agent populations; purely continuous stock-and-flow structure.

## Key settings worth copying
- **Time unit:** Day
- **Flow formula:** `NetInflowRate = AFractionalGrowthRate * SStateOfTheSystem`
- **Fractional growth rate** exposed as a slider parameter so users can explore sensitivity interactively
- **Initial stock value** set via a dedicated AuxVariable (labeled "initial quantity"), making it easy to override in experiments
- Model converted from Vensim FIRSTOR2.MDL — structure is the canonical first-order positive feedback archetype from Sterman's textbook (section 8.2)

## KPIs instrumented
- Time-series plot of `NetInflowRate` over the simulation horizon
- Interactive slider for `AFractionalGrowthRate` allowing real-time comparison of multiple growth-rate runs overlaid on the same chart

## Reusable idea
Expose the fractional growth rate as a slider and overlay multiple runs on one chart — this single trick turns a trivial one-stock model into an intuitive teaching tool showing how sensitive exponential growth is to even small changes in the growth fraction.
