# Pattern card — SI Innovation Model
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD (System Dynamics)
- **Problem it solves:** Models how a new product or idea spreads through a fixed population by word-of-mouth contact between adopters and potential adopters.

## Block chain
Two stock variables partition the total population: **PotentialAdoptersP** (those who have not yet adopted) and **AdoptersA** (those who have). A single **Flow** named AdoptionRate drains PotentialAdoptersP and fills AdoptersA. The flow formula mirrors an epidemiological SI (Susceptible-Infected) contagion structure: encounters between the two groups, filtered by a contact rate and an adoption probability, drive the transfer. As AdoptersA grows, the adoption rate accelerates until potential adopters are exhausted, producing an S-shaped diffusion curve.

## Resources
- **TotalPopulationN** — fixed scalar (total community size, treated as a conserved quantity)
- **ContactRateC** — average number of people one person contacts per time unit (Day)
- **AdoptionFractionI** — probability of adoption per contact with an adopter (analogous to disease infectivity)
- **InitialAdoptersPopulation** — seed adopters at t = 0

n/a (no queues, pools, or agent populations)

## Key settings worth copying
- **AdoptionRate formula:** `(PotentialAdoptersP * AdoptionFractionI * ContactRateC) * AdoptersA / TotalPopulationN`  
  — the A/N term is the key: it scales infection pressure by current adopter prevalence.
- **Time unit:** Day
- **InitialAdoptersPopulation** seeds the stock so the flow is non-zero from t = 0.
- Model was imported from a Vensim .MDL file, demonstrating AnyLogic's cross-tool import path.

## KPIs instrumented
- **AdoptersA over time** — S-curve of cumulative adoption (stock plot)
- **PotentialAdoptersP over time** — complementary decay curve
- Both tracked together on a single time-series chart to visualise the crossover point.

## Reusable idea
The core transferable trick is the **bilinear interaction term** `(susceptible × infected) / total`: by dividing by total population, the contact pressure stays dimensionally consistent regardless of population size, making the same formula reusable for any word-of-mouth, viral-marketing, or epidemic SD model simply by re-labelling stocks and tuning ContactRateC and AdoptionFractionI.
