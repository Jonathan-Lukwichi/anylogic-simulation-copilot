# Pattern card — Adaptive Supply Chain
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + DES)
- **Problem it solves:** Simulates a multi-echelon US consumer goods supply chain where every tier (supplier, producer, distributor, retailer, consumer) is an autonomous agent that independently applies an (s, S) reorder policy and selects trading partners dynamically.

## Block chain
The model has five agent types arranged in a classic supply chain hierarchy: Supplier → Producer → Distributor → Retailer → Consumer. Each tier is populated from an Excel data file; consumers are geo-placed across US territory using population statistics (roughly 30,000 consumer agents, each representing 10,000 people). Inside each Producer and Distributor a DES sub-model handles the physical processing: orders arrive through a Source block, flow through a Service block (representing manufacturing or warehouse handling with a ResourcePool), and fulfilled shipments exit via a Sink. The Shipping sub-model bridges agent-to-agent message passing with the DES pipeline using Enter/Exit connectors and its own Service block. Agents communicate by passing order and delivery messages; on receiving a message an agent re-evaluates its inventory position and triggers a reorder if stock falls below the reorder point s, targeting the order-up-to level S. Partner selection at each tier is randomised via uniform_discr, giving the network adaptive rerouting behaviour when a supplier is busy or out of stock. Time unit is Days.

## Resources
- **ResourcePool** inside each Producer's DES process (manufacturing capacity)
- Fleet size parameter per distributor tier (delivery vehicle capacity)
- No shared global resource pool; each agent owns its own capacity

## Key settings worth copying
- **(s, S) inventory policy:** every tier tracks on-hand + in-transit inventory; orders when position < s, orders up to S
- **Partner selection:** `uniform_discr(0, list.size()-1)` picks a random upstream partner each cycle — simple adaptive routing
- **Delivery times:** `normalDeliveryTime = 3.5` days (distributor), `1.5` days (retailer); passed as agent parameters at population creation
- **Production batch sizes:** `uniform(600, 700)` units upper bound, `uniform(200, 400)` lower bound
- **Consumer reorder timeout:** `uniform(300, 700)` days between purchase events; initial stagger `uniform(0, 500)`
- **Consumer location scatter:** `triangular(0, 0, 20)` radius around city centroid for geographic placement
- **Seed data:** Excel file (Data.xlsx) drives city locations, populations, and initial agent counts
- **Time unit:** Day

## KPIs instrumented
- On-hand inventory level per agent (displayed in agent tooltip/log string)
- Expected incoming stock (in-transit orders tracked per agent)
- Backlog (unfulfilled orders accumulating when stock is zero)
- Implied throughput visible via Sink count in Producer DES sub-model

## Reusable idea
Embed a lightweight DES processing pipeline (Source → Service → Sink with ResourcePool) *inside* each supply chain agent so that manufacturing or warehousing capacity constraints are modelled accurately without a separate process model — the agent's stateful inventory logic and the DES flow share the same agent scope, letting you read inventory variables directly from block callbacks.
