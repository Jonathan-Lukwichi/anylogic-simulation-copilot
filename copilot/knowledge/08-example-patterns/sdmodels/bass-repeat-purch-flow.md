# Pattern card — Bass Repeat Purch Flow
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Models product diffusion including both first-time adoption and ongoing repeat purchasing by existing adopters.

## Block chain
Two stocks drive the model. PotentialAdoptersP drains into AdoptersA via a single adoption flow. The adoption flow sums two sub-flows: AdoptionFromAdvertising (proportional to the remaining potential adopter pool scaled by an advertising effectiveness constant) and AdoptionFromWordOfMouth (a nonlinear contagion term — contact rate × adoption fraction × potential adopters × current adopters / total population). Once someone becomes an adopter, two purchase flows run in parallel: InitialPurchaseRate fires at the moment of adoption (InitialSalesPerAdopter × AdoptionRateAR) and RepeatPurchaseRate runs continuously thereafter (AverageConsumptionPerAdopter × AdoptersA). Total sales volume is tracked as the sum of both purchase flows.

## Resources
No capacity pools or agent populations. The sole accumulating resource is the adopter stock, which starts at zero and grows until the potential-adopter pool is exhausted (ceiling = TotalPopulationN = 1,000,000).

## Key settings worth copying
- TotalPopulationN = 1,000,000 (market ceiling)
- AdvertisingEffectivenessA = 0.011 (fraction of potential adopters converted per time unit by advertising alone)
- ContactRateC = 100 (contacts per adopter per time unit for word-of-mouth)
- AdoptionFractionI = 0.015 (probability a contact converts a potential adopter)
- InitialSalesPerAdopter = 1 (units bought at first adoption)
- AverageConsumptionPerAdopter = 0.2 (units consumed and repurchased per adopter per time unit)
- Time unit: Day
- Converted from the Vensim reference model BASSREPE1.mdl (Sterman)

## KPIs instrumented
- Cumulative sales volume (initial + repeat purchase flows integrated over time)
- AdoptersA stock trajectory (S-curve shape)
- Split between advertising-driven vs word-of-mouth-driven adoption

## Reusable idea
Separate first-purchase from repeat-purchase flows so that a diffusion model captures both the market-penetration S-curve (adoption dynamics) and the ongoing revenue stream from the installed base simultaneously — without needing a DES agent or customer lifecycle object.
