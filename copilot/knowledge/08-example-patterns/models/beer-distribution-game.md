# Pattern card — Beer Distribution Game
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM (agent-based multi-player supply chain)
- **Problem it solves:** Demonstrates how local, rational ordering decisions at each supply chain tier amplify demand variability upstream — the classic bullwhip effect.

## Block chain
Four player agents — Retailer, Wholesaler, Distributor, Factory — form a linear chain. End-consumer demand arrives at the Retailer; each stage fulfils downstream orders from on-hand inventory and passes unmet orders to a backlog. Each player places replenishment orders upstream after observing their own stock level against a min/max target. Delivery of goods travels downstream with a configurable processing-time delay per link (Wholesaler order time, Distributor order time, Factory order time). The Factory produces to order rather than pulling from a supplier. Because each player can only see their local stock and incoming orders — not true end demand — small demand fluctuations cascade into large upstream order swings over time. The model can run in standalone (all four agents simulated) or cloud/multiplayer mode where human participants control individual roles in real time.

## Resources
- Four `Player` agent instances (Retailer, Wholesaler, Distributor, Factory), each carrying:
  - `minStock` — reorder point
  - `maxStock` — order-up-to level
  - `timeService` — internal service/processing time
- Agent links connect each Player to its upstream and downstream neighbours (bidirectional, collection-of-links topology)

## Key settings worth copying
- **Time unit:** Day
- **Ordering policy:** min-max (s, S) inventory strategy — order enough to bring stock back to `maxStock` whenever stock falls below `minStock`
- **Delay parameters:** `timeWhoOrder`, `timeDisOrder`, `timeFacOrder` — each controls inter-stage lead time and can be tuned independently to show the effect of lead-time reduction
- **Cost parameters per Player:** `storageCost` (per unit per day) and `backlogCost` (per unit per day) — set separately, allowing asymmetric penalty structures
- **Multiplayer flag:** boolean switches (`cloudRetailer`, `cloudWholesaler`, `cloudDistributor`, `cloudFactory`) let each role be handed to a human via AnyLogic Cloud

## KPIs instrumented
- `totalStorageCost` — cumulative holding cost across the chain
- `totalBacklogCost` — cumulative backlog penalty cost across the chain
- `totalCosts` = storageCostTotal + backlogCostTotal — the single optimisation target
- Implicitly: inventory level over time and order quantity over time per stage (visible via dashboards to illustrate bullwhip amplification)

## Reusable idea
**Encode information asymmetry as agent scope.** Each Player agent only reads its own stock and incoming order signals — it has no global demand variable. This structural information restriction is what generates emergent bullwhip behaviour without any special code. When building any multi-echelon supply or service model, restricting each agent's observable state to its local neighbourhood is the correct way to study coordination failures and test information-sharing policies (e.g., shared POS data) as interventions.
