# Pattern card — Nonlinear Population
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a population grows and declines nonlinearly as it approaches a finite carrying capacity, using density-dependent birth and death rates.

## Block chain
A single stock (Population) is driven by two flows: Births and Deaths. Both flows are computed from fractional rates that depend on the ratio of current Population to CarryingCapacity. As that ratio rises toward 1, the fractional birth rate falls (logistic S-curve) and the fractional death rate rises (power function), producing an S-shaped growth curve that self-limits at equilibrium. A derived variable (NetFractionalBirthRate = FractionalBirthRate − FractionalDeathRate) summarises the net growth signal.

## Resources
No resource pools or agent populations — pure SD stock-and-flow structure:
- Stock: `Population` (initial value = `InitialPopulation`)
- Flows in: `Births = FractionalBirthRate × Population`
- Flows out: `Deaths = FractionalDeathRate × Population`
- Parameters: `InitialPopulation`, `CarryingCapacity`

## Key settings worth copying
- **Fractional birth rate (logistic):** `1 − 1 / (1 + exp(−7 × (PopRelCC − 1)))` — switches smoothly from high to low as population saturates capacity
- **Fractional death rate (power law):** `0.25 + 0.25 × PopRelCC⁴` — accelerates sharply when overcrowded
- **Time unit:** Day
- **ODE solver:** Euler (fast; suitable for smooth nonlinear SD); mixed-mode fallback uses RK45-Newton
- Converted from Vensim NONLINEA.MDL — validates cross-tool portability

## KPIs instrumented
- Population level over time (stock trajectory)
- Net fractional birth rate (growth vs. decline signal)
- Population relative to carrying capacity (saturation ratio)

## Reusable idea
Pair a logistic (S-shaped) birth-rate function with a power-law death-rate function, both driven by a single saturation ratio (stock ÷ capacity). This two-curve trick produces realistic S-shaped growth and natural overshoot/collapse without any external forcing — the nonlinearity is entirely endogenous and can be transplanted into any SD model that needs density-dependent feedback.
