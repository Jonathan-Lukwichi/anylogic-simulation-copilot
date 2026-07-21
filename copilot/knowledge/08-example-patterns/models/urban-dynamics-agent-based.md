# Pattern card — Urban Dynamics Agent Based
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Captures how individual households and businesses co-evolve in a small city across five spatial zones, accounting for commuting mode, living costs, salaries, and CO2 emissions.

## Block chain
Two agent types drive the model. **Person** agents start with a randomly assigned age (`uniform_discr(20,80)`) and a home zone, then cycle through a statechart with states: *Happy*, *Waiting*, *Recovery*, and *Extreme*. Each day they travel home-to-work and back via private car or public transport; travel time on each road segment is capacity-constrained and perturbed by `uniform` noise. When cumulative dissatisfaction (tracked as `dissatisfied_time`) exceeds a `uniform(500,1500)` day threshold and a 5 % random trigger fires, a person either seeks a new job (scans enterprise vacancy lists) or migrates to a better-scoring zone. Car ownership unlocks when prosperity crosses a threshold. **Enterprise** agents start in a zone chosen with `uniform_discr`, grow through states *Starting → Grow → Working → Lesser*, and post vacancies to a shared job-request list. Zones carry editable parameters (rent, comfort score) that can be changed while the simulation is running; the model re-evaluates zone attractiveness on every decision event.

## Resources
- Five city zones, each with configurable rent and comfort rating.
- Road network modelled as Road agents; each road stores a travel-time function driven by throughput limits and `exponential()*80`-style random noise.
- Public transport lines modelled as PublicTransportLine agents.
- A shared vacancy list (`job_request list`) that enterprises populate and persons consume.

## Key settings worth copying
- **Time unit:** Day.
- **Age initialisation:** `uniform_discr(20, 80)` at startup.
- **Job-search trigger:** dissatisfaction window `uniform(500, 1500)` days combined with `randomTrue(0.05)` — decouples the structural threshold from a stochastic trigger.
- **Enterprise revenue shocks:** `exponential() * 80`, `exponential() * 50`, `exponential() * 100` for different cost/revenue categories.
- **Living cost drift:** incremented each step by `uniform(0, 200)`.
- **Zone migration utility:** weighs trip time, trip cost, and zone rent; a `uniform() < 0.75` branch adds a preference bias toward current zone (inertia).
- **Car purchase delay:** `uniform(4, 20)` days after prosperity threshold is crossed.
- **Road travel times:** base `600 + uniform_discr(300)` ticks with congestion scaling.

## KPIs instrumented
- **Person state counts:** Happy / Waiting+Recovery / Extreme tallied each tick.
- **Enterprise state counts:** Growing+Starting / Working / Lesser tallied each tick.
- **CO2 emissions:** computed from car trips vs. public-transport trips.
- **Zone-level satisfaction score:** drives migration decisions and is visible in dashboard panels.
- **Household financial balance:** tracked per Person agent.

## Reusable idea
Combine a **dual-threshold trigger** (a deterministic patience window drawn from a wide uniform range *plus* a small random-true gate) to generate realistic, spread-out behavioural change events without synchronised agent herding — agents all have different patience lengths and still face an independent coin flip, so zone migrations and job changes stay gradual and plausible rather than occurring in simultaneous waves.
