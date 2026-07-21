# Pattern card — Supply Chain
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES (Discrete-Event Simulation with agent-based tier actors)
- **Problem it solves:** Model a multi-echelon supply chain (retailer → wholesaler → factory) to track inventory levels, backlog, and total cost over a one-year horizon.

## Block chain
Three tier agents — Retailer, Wholesaler, and Factory — each maintain their own inventory variable `I` and a queue of pending orders. A cyclic demand generator fires at an exponential rate (mean 0.1 day) and sends Demand messages to the Retailer with sizes drawn from a custom discrete probability distribution. Each tier's `checkOrders` event runs once per day: it walks its order queue, ships as many units as inventory allows, and then applies an (s, S) reorder policy — calculating the net inventory position (on-hand minus backlog) and placing an upstream order if the position falls below the reorder point. Shipment deliveries are modelled as timed Delivery agents whose travel time is drawn from `uniform(0.5, 1)` day (Wholesaler→Retailer) or `uniform(0.25, 0.5)` day (Factory→Wholesaler). On arrival a delivery credits the receiving tier's inventory and triggers another `checkOrders` pass. The simulation runs for 365 days.

## Resources
- Retailer inventory: integer variable `I`, governed by (s, S) policy parameters set via UI sliders
- Wholesaler inventory: same structure, independent (s, S) parameters
- Factory inventory: same structure; factory also has a production lead-time delay
- No ResourcePool blocks — capacity is modelled as inventory integers, not server queues

## Key settings worth copying
- **Demand interarrival:** `exponential(10 / day())` — rate parameter expressed in model time units so it stays correct regardless of unit choice
- **Demand size:** custom discrete probability distribution built from a histogram widget (`demandSizeDitsribution`)
- **Delivery transit times:** `uniform(0.5, 1) * day()` and `uniform(0.25, 0.5) * day()` — multiplying by `day()` keeps units explicit
- **Review period:** all tiers fire `checkOrders` synchronously once per simulated day via a shared cyclic event, ensuring no tier acts on stale neighbour state
- **Time unit:** Day
- **Run length:** 365 days

## KPIs instrumented
- **Holding cost:** integral of on-hand inventory over time × holding cost rate per item per day
- **Shortage cost:** integral of backlog × `ShortageCostPerItemPerDay` (tracked by `shortageCost` statistics object)
- **Ordering cost:** sum of fixed ordering fees each time an upstream order is placed (`orderingCost.sum()`)
- **Total supply chain cost:** sum of holding + shortage + ordering costs across all tiers
- **Backlog size:** number of unfulfilled order units at each tier at any point in time

## Reusable idea
Synchronise all tier reviews with a single shared cyclic event fired once per review period. This prevents the "phantom order" artefact where an upstream tier processes a downstream order before the downstream tier has received its own incoming shipment — a common modelling error in multi-echelon inventory systems. The pattern is: fire one global "end-of-day" event, let each tier receive any in-transit deliveries first (via Delivery agent arrivals earlier in the same time step), then call `checkOrders` on every tier in downstream-to-upstream sequence.
