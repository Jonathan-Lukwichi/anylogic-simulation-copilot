# Pattern card — Flexible Manufacturing Supply Chain
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (SD stocks/flows inside ABM agents)
- **Problem it solves:** Shows how a multi-tier supply chain self-regulates through decentralised reorder logic and congestion-aware supplier selection when downstream demand is stochastic.

## Block chain
The model is structured as a network of **Producer** agents arranged in tiers, from raw-material suppliers up to finished-goods producers, all feeding a single **Consumer** agent. Each Producer embeds two continuous SD stocks: `rawMaterialInventory` (depleted by production) and `finishedGoods` (filled by production). The connecting auxiliary `productionRate` is computed as `capacity × utilization × oneIfPositive(rawMaterialInventory)`, so production halts automatically on stockout. A `utilizationScheme` function drives `utilization` to zero whenever finished goods exceed a safety threshold and no orders are pending — preventing overproduction. Downstream orders arrive as messages and are queued in `ordersQueue`; the Producer ships when its finished-goods stock covers the head-of-queue order. Replenishment fires when `rawMaterialInventory` drops below `orderThreshold` and no in-flight order exists (the `onOrder` flag blocks duplicates). The Producer then scores each upstream supplier by `(finishedGoodsOrdered − finishedGoods + orderSize) / capacity` and places the order with the lowest-scoring (least congested) one. Time unit is **minutes**.

## Resources
- **Producer agents** across multiple tiers; each carries a `capacity` parameter (integer units/min, varies by tier: `uniform_discr` ranges from 50–200 up to 100–1000)
- `rawMaterialInventoryInitial` parameter sets the starting stock per Producer
- `ordersQueue` (LinkedList of Order objects) per Producer buffers unfulfilled demand
- `orderFrom` (AgentList) wires a Producer to one or more upstream suppliers

## Key settings worth copying
- **Order quantities:** sampled as `uniform_discr(low, high)` per tier — discrete uniform avoids fractional units while introducing realistic variability
- **Reorder threshold:** `orderThreshold` parameter; triggers restocking before stockout, not after
- **Guard flag `onOrder`:** prevents duplicate upstream orders while one is in transit, damping bullwhip oscillations
- **`finishedGoodsThreshold`:** Producer refuses new downstream orders until this safety level is maintained
- **Supplier selection heuristic:** pick the supplier with the lowest `(finishedGoodsOrdered − finishedGoods + orderSize) / capacity` — a one-line congestion score needing no central coordinator

## KPIs instrumented
- `finishedGoods` and `rawMaterialInventory` stocks per Producer, aggregated and displayed as bar heights in a 3-D view
- `productionRate` and `utilization` per Producer tracked as continuous datasets
- `ordersQueue.size()` implicitly tracks unfulfilled demand depth
- `rawMaterialOnOrder` exposes pipeline inventory in transit

## Reusable idea
Embed a minimal SD stock-and-flow core inside each ordering agent so continuous inventory accumulation is modelled without spawning discrete events for every unit; use agent messaging only for the discrete order and shipment handshakes between tiers. The capacity-weighted congestion score for supplier selection is a self-contained, drop-in routing rule for any multi-supplier procurement model.
