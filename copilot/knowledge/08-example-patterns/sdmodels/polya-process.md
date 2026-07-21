# Pattern card — Polya Process
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Demonstrates path dependence — how early random outcomes lock in long-run proportions through a self-reinforcing feedback loop

## Block chain
Two stocks (BlackStones, WhiteStones) each accumulate one stone per period. Which color is added is decided by drawing a single uniform(0,1) random number each time step: if the draw falls at or below the current proportion of black stones, a black stone is added; otherwise a white stone is added. Because proportions update after every addition, the probability of each color winning the next draw shifts in favour of the colour that has already won more — classic positive feedback. Auxiliary variables track ProportionOfBlackStones, ProportionOfWhiteStones, and TotalNumberOfStones; a timed event fires every time step to refresh RandomDraw.

## Resources
- Two stocks initialised to 1 stone each (InitialBlackStones = 1, InitialWhiteStones = 1)
- StonesAddedPerPeriod controls how many stones enter per tick (default 1)
- No agents or resource pools — pure SD stocks and flows

## Key settings worth copying
- Time unit: Day
- Random draw: `uniform(0, 1)` refreshed by a cyclic event every model time step
- Flow logic: `StonesAddedPerPeriod * (RandomDraw <= ProportionOfBlackStones ? 1 : 0)` for black; complement for white
- Equal initial conditions (1,1) ensure the starting proportion is 0.5 — any drift is purely stochastic
- Model converted from Vensim POLYAPRO1.mdl (Sterman textbook §10.2)

## KPIs instrumented
- ProportionOfBlackStones and ProportionOfWhiteStones over time (converge to a fixed value that varies across runs)
- TotalNumberOfStones (grows linearly, confirming the addition rate is constant)

## Reusable idea
Embed a single per-step uniform draw inside a stock-and-flow model to make a stochastic branching rule whose probabilities are themselves state-dependent — this is all you need to simulate any preferential-attachment or market lock-in scenario inside an SD paradigm without switching to ABM.
