# Pattern card — Population Model with Connections and Disease Spread
- **Source:** AnyLogic example model "Population Model with Connections and Disease Spread" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Build an agent-based population in layers (demography → social network → disease) by **agent-type inheritance**, so each layer reuses and overrides the one below, and all three variants live in one model with their own top-level agent and experiment.

## Structure
- **Inheritance ladder** (Help 8.9.10 `anylogic/agentbased/inheritance.html` uses this model as its demo):
  1. `Person` — sex, birth time, `age()`, `lifeExpectancy()`, death event.
  2. `PersonWithBirths` extends Person — reproductive-age statechart for females, births, `mother` / `children`
     links.
  3. `PersonWithConnections` extends PersonWithBirths — contact network that changes as people move.
  4. `PersonWithDisease` extends PersonWithConnections — exposure-driven infection and recovery.

  Each subtype overrides `onBirth()`: it calls `super.onBirth()` and then adds its own layer (inherit some of the
  mother's nearby contacts; pass the mother's infection to the baby). `lifeExpectancy()` is overridden the same way
  (× 0.75 when infected).
- **Three top-level agents** (`MainBasic`, `MainConnections`, `MainDiseaseByYears`), each with its own Simulation
  experiment, share one reusable `PopulationPyramid` agent.
- **Age and death:**
  - `birthTime` = minus a sampled initial age for agents that exist at time 0, else `time()`; `age() = time() − birthTime`.
  - The death event's timeout is the **remaining** life. The function draws a sex-specific life expectancy (custom
    distribution), subtracts the current age, and draws again while the result is negative. That samples lifetime
    given survival to the current age.
- **Network dynamics:**
  - Each person relocates now and then with `moveToInTime(x, y, 1)` (one year of travel, for animation).
  - On arrival, each contact now farther than `connectionRange` is dropped with a given probability
    (`disconnectFrom`), and agents within range are added with a given probability (`agentsInRange(range)` +
    `connectTo`).
  - Babies inherit nearby maternal contacts with a given probability.
- **Disease:**
  - While infected, a person repeatedly adds one unit of exposure to a random contact (`getRandomConnectedAgent()`),
    driven by an internal transition in *Infected*.
  - `expose()` adds to `totalExposure` and calls `onChange()`, so the condition "exposure > critical" is re-tested.
  - Entering *Infected* or *Recovered* restarts the death event, so the new life expectancy applies at once.
  - Initial prevalence applies only at time 0.

## Resources
n/a.

## Key settings worth copying
- **Factory through a dynamic parameter.** `PersonWithBirths` has a parameter `newPerson` whose value on each Main is
  `add_people()`, and the base class calls `newPerson()` to create a baby. The agent can then create siblings in
  whatever population it lives in, without knowing which Main type owns it. Dynamic parameters are re-evaluated on
  each call and are used with call syntax (Help `anylogic/data/dynamic-parameters.html`).
- **Reusable chart agent with per-item expressions.** `PopulationPyramid` takes a generic population
  (`AgentArrayList<T>`) plus dynamic parameters **with an argument** (`person` of type `T`): `age = person.age()`,
  `isMale = person.sex == MALE`, and up to four `isInGroupN` colour groups (infected, recovered, …). A dynamic or
  Action parameter can declare *Parameter arguments* (Help `anylogic/data/parameters.html`). The pyramid refreshes
  from an event, uses 2-year bins, and rescales to 1/2/5 × 10ⁿ.
- **Removing links while iterating:** loop by index over `getConnectionsNumber()` / `getConnectedAgent(i)` and step
  the index back after `disconnectFrom(a)`. A for-each loop over a list that is changing breaks.
- Time unit years; random seed per run.

## KPIs instrumented
Population pyramid by sex and 2-year age band (with infected and recovered highlighted in the disease variant),
totals by sex, and a selectable age band.

## Pitfalls
- **A subtype's statechart cannot be reached through inherited message forwarding.** The model's own comment says
  the inherited `connections` link could not be set to forward messages to the subtype's statechart. The workaround is
  a direct method call plus `onChange()` instead of `send()` *(author's note in the model; not stated in the Help)*.
- In a subtype diagram, base-type elements are shown greyed out and cannot be edited (Help, inheritance). Delete or
  change a shape in the base type if it does not suit every subtype.
- Restart any timer derived from a state-dependent quantity (here the death event) when that state changes. Otherwise
  the old draw stays in force.

## Reusable idea
Grow an ABM in tested layers. Put shared behaviour in a base agent type, add each concern in a subtype that overrides
hooks and calls `super`, and keep one top-level agent plus experiment per layer, so every earlier layer stays runnable
for verification. Pass creation and chart inputs as dynamic parameters so the types stay independent of their
container.

## When the co-pilot should use this
- Demographic, epidemiological or workforce ABMs with births, ageing and deaths (e.g. an age pyramid of staff or
  equipment fleets).
- Contact networks that change as agents move (link churn by distance).
- Structuring a large ABM for reuse and step-by-step verification, or building a reusable chart or statistics agent.
- Related (parallel batch): the Big Book kinship models (custom mother/children links, dynamic histograms) in
  `m-bigbook-1`.
