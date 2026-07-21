# Pattern card — Nonlinear Smoothing
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how workers perceive and remember layoffs asymmetrically — adapting quickly to bad news but forgetting it slowly — using a nonlinear adjustment time inside a first-order smoothing stock.

## Block chain
A single stock (`MemoryOfLayoffs`) is driven by one flow (`ChangeInLayoffMemory`). The flow implements classic first-order exponential smoothing: `(LayoffFraction - MemoryOfLayoffs) / MemoryAdjustmentTime`. The nonlinearity comes from `MemoryAdjustmentTime`, an auxiliary that switches between two constants depending on whether the current layoff fraction exceeds the remembered value. If actual layoffs are worse than memory, adjustment is fast (TimeToIncrease = 1 week); if actual layoffs have eased below memory, adjustment is slow (TimeToDecrease = 25 weeks). The exogenous input `LayoffFraction` is a pulse created with `step(0.1, 0) - step(0.1, 4)` — a shock that rises at week 0 and drops at week 4.

## Resources
n/a — pure SD equations, no agent populations or resource pools.

## Key settings worth copying
- **TimeToIncrease = 1 week** — fast upward adaptation (bad news travels fast)
- **TimeToDecrease = 25 weeks** — slow forgetting (anxiety lingers)
- **Switching condition:** `LayoffFraction >= MemoryOfLayoffs ? TimeToIncrease : TimeToDecrease`
- **Exogenous pulse:** `step(0.1, 0) - step(0.1, 4)` — clean way to inject a temporary shock
- **Time unit:** Week; dataset sampling every 0.25 weeks for smooth charts
- **Initial stock value:** 0 (no prior layoff memory at simulation start)
- **Converted from Vensim** using AnyLogic import — illustrates cross-tool portability

## KPIs instrumented
- `MemoryOfLayoffs` over time — plotted against `LayoffFraction` to visualise the lag and asymmetry
- No explicit throughput or cost KPIs; the insight is qualitative (shape of the memory curve)

## Reusable idea
Replace a fixed smoothing constant with a **conditional (nonlinear) adjustment time** — one value for the rising direction, another for the falling direction. This single-line trick captures asymmetric perception or adaptation in any SD model (e.g., price expectations, inventory targets, customer sentiment) without adding extra stocks or complex sub-models.
