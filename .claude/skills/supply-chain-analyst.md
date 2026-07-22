---
name: supply-chain-analyst
description: Supply-chain and inventory domain knowledge for interpreting scenarios and results in PLAIN ENGLISH. Use when the scenario or uploaded results involve inventory, safety stock, service levels, lead times, stockouts, ordering policies, distribution networks, forecasting value, or the bullwhip effect. Pairs with stats-analyst (which owns the math of evidence); this skill owns what the numbers MEAN for the operation.
---

# supply-chain-analyst

Domain brain for supply-chain scenarios and results. Grounded in the supply-chain
course canon (Simchi-Levi et al., *Designing and Managing the Supply Chain*, and the
BVK780 lecture sequence: inventory & risk pooling, network planning, contracts, value
of information, distribution strategies). Every interpretation ends in plain English:
what should the operation DO differently.

## 1. Inventory fundamentals (the workhorse formulas)

- **EOQ** `Q* = √(2KD/h)` — balances ordering cost against holding cost. Plain terms:
  order more per order when ordering is expensive; less when holding is expensive.
  Total cost is FLAT near the optimum — being 20 % off Q* barely hurts, so don't
  over-engineer it.
- **(s, S) / reorder-point policy** — order up to S when stock falls to s. The reorder
  point protects against demand DURING the replenishment wait:

  `s = D̄·L̄ + z·√(L̄·σ_D² + D̄²·σ_L²)`

  The safety-stock term has TWO parts: demand noise over the lead time, and **lead-time
  noise scaled by average demand**. Always ask which term dominates — it decides what
  can help (see §4).
- **Service level ↔ z:** 90 % ≈ 1.28, 95 % ≈ 1.64, 99 % ≈ 2.33. Raising service level
  costs *increasingly* more stock per extra point — the last 1 % is the expensive one.
- **Review period:** with periodic review the protection window is L + R, not L —
  slower reviews silently demand more safety stock.

## 2. Risk pooling (why aggregation is magic)

Centralising stock (or pooling across products/regions) reduces total safety stock,
roughly by √n for n similar independent locations — the highs of one location cancel
the lows of another. The benefit GROWS with demand variability and SHRINKS when
locations' demands move together (positively correlated). Plain terms: one shared
buffer beats several private ones, most strongly when demands are jumpy and unrelated.
Same logic underlies postponement (delay differentiation, pool at the generic stage).

## 3. Bullwhip effect (value of information)

Order variability AMPLIFIES as you move upstream (retailer → wholesaler → factory).
Four classic causes: demand-signal processing (each stage forecasts from the orders it
sees, not real demand), order batching, price promotions, and shortage gaming. Longer
lead times amplify it further. Mitigations, in order of power: **share point-of-sale
demand data, shorten lead times, smooth batches, everyday-low-pricing, allocate
scarce supply on past sales not on orders.** Plain terms: the factory suffers chaos the
shop never sees; the cure is letting everyone see real demand — this is the "value of
information" argument for integration/VMI.

## 4. Interpreting simulation/experiment results (the procedure)

When results about inventory or staffing-vs-inventory come back, walk this list:

1. **Which cost dominates?** Decompose: holding vs ordering vs stockout vs expiry.
   A stockout cost that dwarfs holding+ordering means the policy is under-protected
   (s too low / lead-time risk underestimated) — not that "inventory is expensive".
2. **Which safety-stock term dominates?** Compute both terms of the formula. If
   `D̄²·σ_L²` (lead-time variance) ≫ `L̄·σ_D²` (demand variance), then **better demand
   forecasts CANNOT reduce safety stock much** — the buffer exists for supplier
   unreliability, not demand uncertainty. Forecasting value lands where demand
   variance dominates: short, reliable lead times. Check this BEFORE promising
   inventory savings from ML.
3. **Policy assumptions vs simulated reality:** does the policy's assumed lead-time
   mean/variance match what the model actually generates (disruptions, multipliers,
   truncation)? A policy fed understated lead-time variance under-provisions stock and
   shows up as chronic stockouts. This is a modelling bug wearing a domain costume.
4. **Service level: achieved vs promised.** Compare measured fill rate / coverage to
   the z the policy was designed for; a gap points at the same assumption mismatches.
5. **Where does forecast value land?** Test workforce/scheduling and inventory
   SEPARATELY — forecast-driven staffing can win while inventory stays flat (short
   "lead time" for staffing decisions vs long supplier lead times). Never report only
   the total.
6. **Hand the arithmetic of proof to `stats-analyst`** (CIs, t-tests, replication
   discipline); this skill supplies the WHY behind the numbers.

## 5. Network & strategy (for scenario framing)

- **Network planning trade-off triangle:** facilities vs transport vs inventory —
  fewer/bigger warehouses cut fixed cost and pool risk but raise transport distance
  and response time. State which corner the scenario is testing.
- **Distribution strategies:** classic warehousing (hold stock) vs **cross-docking**
  (flow through, needs volume + tight coordination) vs direct shipment (no middle
  stage, loses pooling). Match to volume, variability, and lead-time need.
- **Push vs pull boundary:** push (forecast-driven) upstream of the boundary, pull
  (demand-driven) downstream; postponement moves the boundary later. Many "should we
  make-to-stock or make-to-order?" scenarios are really asking where this boundary sits.
- **Supply contracts:** buy-back and revenue-sharing exist to fix newsvendor
  misalignment — the party bearing overstock risk orders too little for the chain;
  risk-sharing contracts move the order toward the chain-optimal quantity.

## 6. Plain-English verdict templates

- "Your buffer stock is protecting you against **supplier unreliability**, not demand
  surprises — that's why better forecasting didn't cut inventory cost."
- "Stockouts cost you R…, several times what holding more stock would cost — the data
  says the reorder point is set too low for the lead times you actually experience."
- "Centralising these n depots would cut total safety stock by roughly …% (risk
  pooling) — at the price of longer delivery distance; that's the trade to weigh."

## Grounding

Distilled in original wording from the supply-chain course canon (Simchi-Levi et al.
3e; BVK780 lecture sequence) — the source PDFs are private course material and are NOT
in this repo (see PRIVATE-MATERIALS.md). Free public anchor: Ivanov, *Operations and
Supply Chain Simulation with AnyLogic* (SOURCES.md). The §4 procedure also encodes
lessons paid for in a real hospital digital-twin study (lead-time variance dominance,
labour-vs-inventory separation).
