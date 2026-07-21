# Pattern card — SIR Model Threshold
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Shows how a gradually rising contact rate pushes an epidemic past its tipping point, turning a smouldering outbreak into an explosive one.

## Block chain
Three stock variables hold the population compartments: SusceptiblePopulationS, InfectiousPopulationI, and RecoveredPopulationR. Two flow variables move people between them: InfectionRate drains Susceptible into Infectious, and RecoveryRate drains Infectious into Recovered. A third flow, InmigrationOfInfectious, seeds one new infectious individual every 50 simulated days to keep the disease from dying out naturally. Auxiliary variables compute ContactRateC (which starts at InitialContactRate and climbs via a ramp function driven by ContactRateRampSlope), InfectivityI (probability of transmission per contact), AverageDurationOfIllnessD, TotalPopulationP (constant), and the key diagnostic ReproductionRate (R0 proxy = ContactRateC × InfectivityI × AverageDurationOfIllnessD × S/N).

## Resources
n/a — pure compartmental SD model; no agent populations or resource pools.

## Key settings worth copying
- **Time unit:** Day; simulation runs long enough (horizon ~5 500 days) for the ramp to push R above 1.
- **Contact rate ramp:** `ContactRateC = InitialContactRate * ramp(ContactRateRampSlope, 1, 5500)` — a simple built-in ramp function lets you dial how fast social mixing grows.
- **Infection rate formula:** `ContactRateC * InfectivityI * S * I / N` — standard frequency-dependent transmission.
- **Recovery rate formula:** `I / AverageDurationOfIllnessD` — mean infectious period directly sets the drain rate.
- **Periodic seeding:** `(int)(time()/50) == time()/50 ? InfectiousAdded/TIME_STEP : 0` — pulse injection every 50 days prevents stochastic extinction.
- **Converted from Vensim** (SIRMODEL1.mdl) — demonstrates AnyLogic's import path for legacy SD models.

## KPIs instrumented
- Time-plot of S, I, R trajectories over the full run.
- ReproductionRate (R0 proxy) tracked as an auxiliary — threshold crossing at R = 1 is the visual "aha" moment.

## Reusable idea
Use a **ramp-driven parameter** (here, contact rate) to demonstrate a tipping-point: the model stays in a low-endemic regime until the ramp crosses the epidemic threshold (R0 > 1), after which an explosive outbreak becomes inevitable. This "threshold reveal" pattern is transferable to any SD model where a slowly drifting parameter governs a bifurcation — capacity limits, congestion collapse, supply-chain instability, etc.
