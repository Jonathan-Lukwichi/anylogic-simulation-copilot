# Pattern card — Bass with Discards
- **Source:** AnyLogic example (sdmodels) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Extends the classic Bass diffusion model to account for product obsolescence, where discarded units return owners to the potential-adopter pool and sustain long-run market cycles.

## Block chain
Two stocks drive the system. PotentialAdoptersP loses population through adoption and gains it back through discards. AdoptersA gains from the adoption rate and loses through the discard rate. Adoption has two channels: advertising-driven adoption (proportional to potential adopters and an advertising-effectiveness constant) and word-of-mouth adoption (proportional to the product of potential adopters, active adopters, a contact rate, and an adoption fraction, all normalised by total population). The discard rate is first-order: active adopters divided by the average product life, meaning each unit eventually wears out and its owner re-enters the market.

## Resources
n/a (SD model — no agent pools or discrete-event resource pools; population is a continuous stock)

## Key settings worth copying
- **TotalPopulationN** — fixed market ceiling; initialises PotentialAdoptersP as (TotalPopulationN − initial AdoptersA)
- **AdvertisingEffectivenessA** — constant multiplier on advertising-driven adoption flow
- **ContactRateC** — frequency at which active adopters encounter potential adopters
- **AdoptionFractionI** — probability a contact converts a potential adopter
- **AverageProductLifeL** — mean product lifetime; DiscardRate = AdoptersA / AverageProductLifeL (first-order decay)
- **ModelTimeUnit:** Day
- Converted from Vensim BASSWITH1.mdl (Sterman textbook reference)

## KPIs instrumented
- AdoptionRateAR over time (adoption wave shape)
- AdoptersA stock trajectory (peak and plateau)
- DiscardRate over time (obsolescence pulse)
- PotentialAdoptersP replenishment from discards (second-wave potential)

## Reusable idea
Adding a first-order discard flow back into the potential-adopter stock transforms a one-shot diffusion curve into a repeating market cycle; the average product lifetime becomes the key lever controlling how quickly the replacement market regenerates — directly applicable to any durable-goods or technology-refresh scenario.
