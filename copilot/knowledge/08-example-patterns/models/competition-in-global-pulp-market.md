# Pattern card — Competition in Global Pulp Market
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (agent-based with market-clearing price mechanism)
- **Problem it solves:** Models how competing pulp companies expand or contract their mill networks across global regions in response to a floating market price, revealing how industry-wide capacity decisions drive boom-bust price cycles.

## Block chain
Five company agents (A–E) each own a dynamic collection of Mill agents. Each week every company scans its mills, tallies weekly profit or loss, and decides whether to build a new mill in the cheapest available region or suspend/destroy an unprofitable one. Mill agents carry individual state (WORKING / SUSPENDED) plus a capacity (K tonnes/week) that grows by a uniform 20–50 % multiplier when a capacity-expansion event fires. The global market price is set by a merit-order rule: mills are sorted ascending by their unit pulp cost; the market price is pegged to the cost of the last (most expensive) mill needed to satisfy total demand. That single price clears the whole market — cheap mills earn large margins while the marginal mill breaks even. Because every company reacts to the same price signal, investment waves are self-reinforcing: high prices trigger parallel mill construction across all companies, oversupply drives the price below the marginal cost, mills suspend en masse, prices recover, and the cycle repeats. Time step is one week.

## Resources
- **Agent populations:** 5 Company agents; dynamic population of Mill agents (added/removed at runtime via deferred-event trick to avoid concurrent-modification during iteration)
- **Regions (5):** NorthAmerica, SouthAmerica, Eurasia, Africa, Australia — each carries a `pulpWoodPrice` parameter that determines a mill's variable cost in that region
- **Capacities:** per-mill `capacity` (K tonnes/week); grows stochastically on expansion; drives the merit-order supply curve width

## Key settings worth copying
- **Time unit:** Week
- **Capacity expansion distribution:** `uniform(1.2, 1.5)` multiplier applied to existing mill capacity on invest decision
- **Price signal:** merit-order sort — mills ranked ascending by total unit cost; market price = cost of the marginal (last needed) mill
- **Deferred agent add/remove:** new mills and destroyed mills are created via zero-delay events (`create_MillCreation(0, ...)` / `create_MillDestruction(0, ...)`) so the agent list is never mutated inside an active `for(Mill m : mills)` loop
- **Demand parameter:** slider-controlled `demand` (default 100 K tonnes); a second parameter `demand2` allows scenario switching
- **Suspended mill cost:** per-company fixed weekly cost charged even when a mill is idle — makes suspension painful and creates hysteresis

## KPIs instrumented
- **Market price** ($/tonne) — time-series plot, colour-coded blue below $500, red above
- **Company capital** ($ millions) — stacked line chart for all five companies
- **Mill count** — live count of active vs. suspended mills displayed on canvas
- **Weekly profit/loss** — computed each step per company: `volumePerWeek × 1000 × (price − totalCost())` for working mills; minus `suspendedMillCost` for idle mills

## Reusable idea
The **deferred agent creation/destruction pattern**: never add or remove agents while iterating over the population. Instead, schedule a zero-delay custom event (`create_EventType(0, args)`) that fires after the current step completes. This is the standard AnyLogic workaround for ConcurrentModificationException in agent-population loops and is directly transferable to any ABM where agent decisions trigger births or deaths of other agents.
