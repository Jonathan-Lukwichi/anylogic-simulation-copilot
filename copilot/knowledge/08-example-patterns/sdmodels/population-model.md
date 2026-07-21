# Pattern card — Population Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models exponential population growth and decline using two competing first-order feedback loops — birth inflow and death outflow — converted from a classic Vensim reference model.

## Block chain
A single Stock (`Population`) accumulates people. Two Flows modify it continuously:
- **Birth Rate** (inflow) = Population × Fractional Birth Rate — a positive reinforcing loop that drives growth proportional to current size.
- **Death Rate** (outflow) = Population / Average Lifetime — a negative balancing loop that drains the stock at a rate set by lifespan.

Two Auxiliary constants parameterise the flows. Causal arrows link each constant to its respective flow, making the feedback structure explicit on the diagram.

## Resources
n/a — no agents, queues, or resource pools; pure continuous stock-and-flow structure.

## Key settings worth copying
- **Initial population:** 1,000,000 (1e+006)
- **Fractional Birth Rate (FBR):** 0.04 per day (4 % daily birth fraction)
- **Average Lifetime (AL):** 80 days
- **Time unit:** Day
- **Integration method:** Euler (first-order explicit); RK45+Newton available for mixed/algebraic equations
- **Net growth condition:** model grows when FBR > 1/AL (i.e., 0.04 > 0.0125), producing exponential increase

## KPIs instrumented
- Population stock level over time (chart on experiment canvas)
- Implicit net growth rate (Birth Rate − Death Rate) readable from flow values at any time step

## Reusable idea
The transferable trick is the **two-loop SD skeleton**: one reinforcing inflow proportional to the stock, one balancing outflow inversely proportional to a lifetime constant. This pattern is the foundation of any exponential growth/decay model (inventory replenishment, disease spread, customer churn, battery charge) — just rename the stock, swap the constants, and the causal structure is immediately reusable.
