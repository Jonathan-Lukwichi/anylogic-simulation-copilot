# Pattern card — Custom (empirical) distributions for agent attributes and inputs
- **Source:** AnyLogic video "Custom probability distributions" (https://youtu.be/YniPxHYfbrc) — distilled, original wording
- **Paradigm:** ABM (the same element serves DES inputs)
- **Problem it solves:** Draw attribute values (sex, age, salary) or any stochastic input from observed data or published tables when none of the roughly 40 built-in distributions fits.

## Mechanism
- **Categorical attribute.**
  - In the population wizard, give `Person` a parameter of type **Option list** (e.g. `Sex` with MALE and FEMALE).
  - Choose **Follow empirical distribution** and enter the shares (48 / 52).
  - The wizard generates the distribution and wires the population's parameter to call it (named like `people_sex_distribution()`).
- **Numeric attributes.**
  - Put one **Custom Distribution** element (Agent palette) on Main for each attribute.
  - Call it like a function in the population's parameter fields: age = `ageDistribution()`, salary = `salaryDistribution()`.
  - Each agent gets its own draw when it is created.

## Resources
n/a

## Key settings worth copying
- **Type:**
  - `Discrete` returns only listed values or whole numbers. The video uses it for age in whole years.
  - `Continuous` interpolates linearly between points (N points give N−1 sloped intervals). Any value inside the data range can come out.
- **Define using:**
  - **Ranges** takes one row per interval with a weight. It suits published bands, e.g. six age groups with population shares, children 25 %. The video pairs it with Discrete. Some Help versions list Ranges under Continuous only, so check your version.
  - **Observed samples** takes raw observations. Type them or paste tab-separated values from a spreadsheet, and AnyLogic counts how often each value occurs.
  - **Frequency table** takes value + weight rows.
- For large sets, import the data into the model database, tick **Loaded from database** and pick the table and column. The video uses a 100-row salary table.
- Open the **Preview** section and check the auto-generated histogram before running.
- Entries act as weights. Percentages that add up to 100 are simply convenient (normalisation unverified).

## KPIs instrumented
n/a. To check the result, double-click the population at runtime and step through agents, or histogram the attribute.

## Pitfalls
- **Scope.** The element lives on Main. From the population's properties on Main, `ageDistribution()` resolves. From inside `Person` (a default value, an event), call `main.ageDistribution()`.
- **No tails.**
  - A Continuous custom distribution never goes beyond the observed minimum and maximum.
  - A Discrete one built from observed samples never returns an unseen value.
  - Both understate extremes, and a small sample reproduces its own quirks.
- **Salary-type data.** Discrete observed samples on a continuous quantity return only the exact recorded amounts. Choose Continuous if in-between values should occur.
- **Random shares.** A 48/52 split in 1,000 agents is still random, so the realised shares wobble around the target. Assign deterministically if the exact counts matter.

## Reusable idea
A Custom Distribution is a data-built function you can call anywhere a distribution call is allowed. Use bands for published tables, observed samples for raw logs, and the database for large sets.

## When the co-pilot should use this
- The data are categorical or banded (census, age groups), multimodal, or fail every parametric goodness-of-fit test (KS/AD). Use an empirical distribution and state its tail limitation.
- If a parametric family does fit, keep it. It extrapolates tails, so the KB's fit-and-test rule stays the default.
- Related cards: `models/agent-population-and-sd-housing.md` (`createCustomDistribution()` from a table function) and `models/alcohol-use-dynamics.md` (turning a rate table into a distribution).
