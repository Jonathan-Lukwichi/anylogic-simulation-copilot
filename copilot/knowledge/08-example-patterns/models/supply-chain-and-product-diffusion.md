# Pattern card — Supply Chain and Product Diffusion
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (SD + ABM)
- **Problem it solves:** Models how Bass-diffusion market demand drives orders through a three-tier supply chain (Retailer → Wholesaler → Factory), letting you see how word-of-mouth adoption dynamics couple with inventory oscillations.

## Block chain
The SD layer holds three stocks — PotentialUsers, Demand, and Users — connected by two flows: an AdoptionRate (driven by advertising effectiveness plus word-of-mouth contact among existing users) and a DiscardRate (product lifetime decay). The ABM layer has three active agent types: Retailer, Wholesaler, and Factory. Each agent keeps a local inventory stock (I) and a FIFO order queue. A daily event triggers every agent to review its inventory, fill what it can from stock, and send backlogged orders upstream. Shipment delivery is modelled with a timed message carrying the goods; transit time is uniform(0.5, 1) day for downstream links and uniform(0.25, 0.5) day for factory output. The Factory agent contains its own mini SD diagram where manufacturing rate responds to an inventory policy comparing on-hand plus in-transit stock against target levels. The interface between the two paradigms: the Retailer reads the SD Demand stock directly; when it fulfils an order it calls back into Main to decrement Demand and increment Users, so the SD model evolves in response to actual supply.

## Resources
- Retailer agent: 1 instance, inventory stock I, order queue
- Wholesaler agent: 1 instance, inventory stock I, order queue
- Factory agent: 1 instance, inventory stock I (SD sub-model controls replenishment)
- No explicit ResourcePool blocks; capacity is purely inventory-level logic

## Key settings worth copying
- Time unit: Day
- Adoption flow formula: `PotentialUsers * AdEffectiveness + Users * ContactRate * Fraction * PotentialUsers / (PotentialUsers + Users)` — classic Bass diffusion
- Discard flow: `Users / ProductLifetime`
- Retailer → Wholesaler delivery delay: `uniform(0.5, 1) * day()`
- Factory → Wholesaler delivery delay: `uniform(0.25, 0.5) * day()`
- Inventory reorder policy: order enough to bring (I + expected_arrivals − backlog) up to target; checked once per day via a scheduled event
- SD and ABM clocks share the same Day time unit — critical for consistent coupling

## KPIs instrumented
- Supply vs. Demand chart over time (per retailer and system-wide)
- PotentialUsers, Users stocks plotted over simulation horizon
- Order backlog size at each tier
- Inventory level (I) at Retailer, Wholesaler, Factory

## Reusable idea
Expose an SD stock as a readable variable that an ABM agent can both read and mutate: the Retailer polls the Demand stock for pending consumers, fulfils what inventory allows, then calls back to decrement Demand and increment Users. This two-way SD↔ABM handshake lets market adoption dynamics and supply-chain logistics co-evolve without a separate coupling layer.
