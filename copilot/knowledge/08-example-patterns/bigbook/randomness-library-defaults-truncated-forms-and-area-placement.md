# Pattern card — Randomness you did not ask for, truncated distribution forms, and random placement inside a drawn area
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 15 "Randomness in AnyLogic models" — distilled, original wording
- **Paradigm:** Method (input modelling; DES and ABM)
- **Problem it solves:** Flowcharts that are random, and overloaded, because blocks keep their defaults; truncated draws whose arguments mean something unexpected; agents that must start at random points inside an irregular boundary.

## Mechanism
Checked against Help 8.9.10 (block reference pages, *normal (truncated)* and the other truncated forms, shape API) and the 8.9.10 book demos (batch m-bigbook-3). The RNG, seeds and custom generators are in `videos/rng-seed-control-and-custom-generator.md` and G16–G17. Why draws must not sit inside SD formulas is in `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`.
1. **Library blocks are random out of the box** (Big Book p. 11; Help reference pages):

   | Block | Default |
   |---|---|
   | Source | rate 1 per second; switched to interarrival time, `exponential(1)` s |
   | Source, multiple agents per arrival | `uniform_discr(3, 5)` |
   | Delay *(Big Book)*, Service *(Help)* | `triangular(0.5, 1, 1.5)` s |
   | MHL MoveByTransporter (a handling time), Store | `triangular(0.5, 1, 1.5)` s |
   | SelectOutput | 0.5, or condition `randomTrue(0.5)` |
   | SelectOutput5 | 0.2 per exit, or `uniform_discr(1, 5)` |

   **Consequence.** An all-default Source → Queue → Delay → Sink has mean interarrival 1 s and mean service 1 s at capacity 1, so ρ = 1. It has no steady state. The queue drifts upward until the 100-place default Queue is full. After that the Source cannot push new agents, and the run should stop with G4's "not able to leave the port" error *(expected; the book says only that the queue overflows)*.
2. **Truncated ("Vensim-style") forms** (Big Book p. 6; Help 8.9.10):
   - The forms are `normal(min, max, shift, stretch)`, `exponential(min, max, shift, stretch)`, `gamma(min, max, alpha, shift, stretch)`, `poisson(min, max, mean, shift, stretch)` and `triangular(min, max, left, mode, right)`. Beta, binomial, negative binomial and Weibull have similar forms.
   - Each draw takes the standard shape, multiplies it by `stretch`, adds `shift`, and redraws until the result falls inside [min, max]. Use `-infinity` / `infinity` for no bound.
   - **What that means:**
     - For `normal`, shift and stretch are the mean and sd *before* truncation. A one-sided cut moves the realised mean inward.
     - For `exponential`, `stretch` is a scale, i.e. the mean of the untruncated part, 1/λ. In `exponential(lambda)` the argument is a rate. Swapping forms without inverting it changes the mean by a factor of λ².
     - A window deep in a tail makes every draw loop many times.
3. **Random start points inside a boundary** (Big Book pp. 14–16; Help shape API; 8.9.10 demos):
   - **Closed polyline:** in Main's *On startup*, for each agent `p.setLocation(area.randomPointInside());`. The call uses the model's default RNG, so a fixed seed reproduces the layout. It returns null for a polyline with no points. A shape built in code and not added to a group throws; use `randomPointInside(rng)`.
   - **Closed curve:** the book says curves lack `randomPointInside()` (p. 15). In the 8.9.10 engine, however, `ShapeCurve` itself defines `randomPointInside(Random)` and `contains(x, y)`, although the Help's curve page lists neither. Try `curve.randomPointInside(getDefaultRandomGenerator())` *(untested)*. The book's fallback works in any version:
     - draw `uniform` x and y in the bounding box until `curve.contains(x, y)` is true, as the 8.9.10 demo does;
     - the expected number of tries is the box area divided by the enclosed area;
     - the same rejection loop is in `models/agent-population-and-sd-housing.md`.
   - **Markup:** polygonal nodes and GIS regions offer their own `randomPointInside` (Help markup pages).
4. **Random attributes of resource units** (p. 12): in a ResourcePool's *On new unit* with a custom unit type, e.g. `unit.skill = uniform(5, 7)`. Give each pool its own band. The *On new unit* mechanism itself is in `models/product-delivery.md`.

## Resources
n/a

## Key settings worth copying
- **Face check before the first run:** replace every default rate, time and probability, then compute ρ = λ·E[S] / c per station.
- **A bounded service time around 20 min with sd 5:** `normal(5, 40, 20, 5)`. State that the realised mean differs from 20 when a bound bites.
- **Argument orders that bite:**
  - `normal(sigma, mean)`, sigma first (*AnyLogic in 3 Days* p. 83);
  - `lognormal(mu, sigma, min)` (G3);
  - triangular (G55);
  - `uniform_discr(3, 7)` includes both 3 and 7.

## KPIs instrumented
n/a. The ρ table and the realised mean of each truncated input, from a quick histogram or `traceln` of 10,000 draws, belong in the verification log.

## Pitfalls
- **Outdated experiment setting.** The Randomness section no longer offers "Selection mode for simultaneous events" (Big Book p. 19). It was removed in 8.6 (G60, rng card).
- **Help and book disagree on re-seeding.** The Help 8.9.10 RNG page says the generator is set up once and not re-initialised between replications. The Big Book (pp. 21–22) and G16 say it is re-seeded before every run. The Help's experiment pages are self-contradictory on this, so test with three replications before relying on either wording *(unverified)*.
- **Hidden draws.** A newly added block can take numbers from the generator when it is initialised, even if it is not connected (Help *Reproducible model runs*). Adding one shifts all later draws under the same seed.

## Reusable idea
Treat every default as an unvalidated input. Know what each distribution argument means before you truncate. Place agents with the area's own sampler so a fixed seed reproduces the layout.

## When the co-pilot should use this
- Building or reviewing any flowchart: run the defaults check.
- Converting Vensim or Stat::Fit outputs that use `(min, max, shift, stretch)`.
- Initial agent placement in a city limit, site or ward outline.
- **Symptoms:** "my first model crashes after a few minutes", "a truncated normal's mean is off", "agents start outside the area".
- **Related:** G3, G4, G16, G17, G55; `02-statistics-input-modeling/README.md`.
