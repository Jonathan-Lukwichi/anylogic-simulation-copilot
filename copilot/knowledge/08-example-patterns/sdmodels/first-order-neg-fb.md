# Pattern card — First Order Neg FB
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models exponential decay of a quantity through a single stock that drains at a rate proportional to its own level (first-order negative feedback loop).

## Block chain
A single **Stock** (`SStateOfTheSystem`) accumulates the quantity of interest. One **Flow** (`NetOutflowRate`) drains the stock. An **Auxiliary variable** (`DFractionalDecayRate`) holds the constant fractional decay rate. The flow formula closes the feedback loop: `NetOutflowRate = DFractionalDecayRate × SStateOfTheSystem`, so as the stock falls, the outflow shrinks proportionally—producing classic exponential decay.

## Resources
n/a — no agent populations or resource pools; the model is a pure stock-and-flow structure with one stock, one flow, and two auxiliary parameters.

## Key settings worth copying
- **Time unit:** Day
- **Flow formula:** `DFractionalDecayRate * SStateOfTheSystem` — the entire feedback mechanism in one line
- **Initial stock value** stored in a separate auxiliary (`DInitialQuantity`) so it can be adjusted via a slider without editing the stock directly
- Converted from a Vensim `.MDL` file, demonstrating AnyLogic's import path from Vensim models

## KPIs instrumented
- Stock level over time (plotted on a time-series chart)
- Net outflow rate over time (plotted alongside the stock to show the coupled decay)

## Reusable idea
Isolate the fractional rate as a named auxiliary rather than embedding it in the flow formula — this makes the rate an exposed parameter that sliders or sensitivity experiments can sweep without touching the structural equations. The same one-stock / one-drain pattern is the building block for inventory depletion, radioactive decay, loan amortisation, and any SD model where the drain speed is proportional to what remains.
