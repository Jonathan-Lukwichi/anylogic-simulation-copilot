# Pattern card — AnyKitchen
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Discrete-Event Simulation — Process Modeling Library)
- **Problem it solves:** Models ingredient-gathering and multi-step cooking workflows where a process cannot start until a specific, possibly unordered, collection of parts arrives — demonstrated through soup and pizza preparation scenarios.

## Block chain

Two parallel cooking sub-processes share a common structure:

**Soup line:**
Multiple ingredient Sources (one per ingredient type) → individual Delay blocks (ingredient prep time) → Wait block (holds each ingredient until the required count for that recipe is assembled) → Delay block (cooking/simmering) → Sink

**Pizza line:**
Multiple ingredient Sources → individual Delay blocks → Wait block with preemption logic (tracks which ingredients are present, can displace lower-priority items when a slot is needed) → Delay block (oven cooking) → Sink; a separate Sink drains displaced/rejected ingredients.

The Wait block is the architectural centrepiece: it acts as a conditional accumulator that releases its contents only when a programmer-defined predicate over the current queue contents becomes true.

## Resources

n/a — no ResourcePool, Seize, or Release blocks are used. Capacity constraints are handled implicitly by the Wait block's release condition and the fixed number of ingredient slots defined per recipe (ingredientsInPizza, ingredientsInSoup parameters).

## Key settings worth copying

- **Time unit:** Minutes — appropriate for kitchen-scale operations.
- **Ingredient arrival:** Each ingredient type has its own Source with an independent interarrival rate expression, allowing different supply frequencies per ingredient.
- **Recipe parameters:** Integer parameters (e.g., `ingredientsInPizza`, `ingredientsInSoup`) control how many items the Wait block must collect before releasing; changing one number rescales the entire recipe.
- **Wait — orderless retrieval mode:** Soup scenario uses a simple count-based release: trigger fires when `waitSoupIngredients.size() == ingredientsInSoup`.
- **Wait — preemption mode:** Pizza scenario uses a multiset check (`prepareIngredients()` tallies ingredient types via a LinkedHashMap) to detect when the correct combination is present, and preempts (removes) the wrong ingredient if a better one arrives.
- **Delay durations:** Defined as fixed numeric constants per stage (prep delay, cook delay); trivially replaced with distribution calls (e.g., `uniform(a, b)`) for stochastic extensions.
- **No random distributions** are used in the base model — all timing is deterministic, making it easy to verify correctness before adding variability.

## KPIs instrumented

n/a — the base model uses `traceln` console output to log cooking events (e.g., which ingredient combination triggered a pizza cook) rather than formal KPI dashboards. Throughput can be inferred by counting Sink arrivals over simulated time; no built-in charts or statistics objects are present.

## Reusable idea

**The Wait block as a recipe gate:** Whenever a process requires a specific combination or count of heterogeneous inputs before it can proceed — assembly, kitting, batch filling, multi-reagent lab steps — replace a simple Queue+Service pair with a Wait block whose `free agent` condition inspects the entire current contents. The pizza preemption variant extends this further: if a higher-priority item arrives and the slot is occupied by a suboptimal item, the Wait block can be programmed to eject the inferior item and re-evaluate, avoiding deadlock when ingredient supply is competitive or variable.
