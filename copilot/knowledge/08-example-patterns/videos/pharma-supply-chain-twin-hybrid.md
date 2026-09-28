# Pattern card — Pharma supply-chain twin: hybrid echelons, GMP plant chain and a per-node KPI panel
- **Source:** AnyLogic video "Supply Chain Management Twin for Pharmaceutical Using AnyLogic" (https://youtu.be/uyVqhY-aZSo) — distilled, original wording
- **Paradigm:** Hybrid
- **Problem it solves:** Laying out a supplier → pharma plant → distributor → hospital/pharmacy → patient network as one GIS model whose plant internals and dashboards answer pharma questions, not generic ones.

## Mechanism
- **The case:** an AnyLogic Conference talk (HCLTech) about a pilot for a US pharma client. It is a demo walk-through only: no data, policies or results are given.
- **Structure (known pattern):** each echelon is an agent type on a GIS map with a legend.
  - Delivery vehicles are agents whose statechart cycles moving → loading → unloading.
  - Order handling, queuing, loading, delivery and stock tracking are DES flowcharts inside the agents.
  - SD is kept for slow strategic drivers: demand growth, replenishment, capacity expansion.
  - This is the `models/adaptive-supply-chain.md` structure; reuse its (s, S) logic.
- **Plant internals (the pharma-specific part):**
  1. Raw material arrives.
  2. QC tests it for quality and compliance, and approves or rejects it.
  3. Compounding mixes the formula once every ingredient is present.
  4. Filling forms tablets, capsules or liquid batches.
  5. Drying and sterilisation run under controlled conditions.
  6. Packaging and labelling.
  7. Dispatch to distributors.
- **Suggested PML mapping** (supplementary; the video shows animation, not blocks):
  1. `Enter` (lot off a supplier vehicle) → `Queue` "quarantine" → `Service` "QC test" (QC-analyst pool) → `SelectOutput` on the lot pass rate, with rejects to a `Sink`.
  2. `Assembler` with each ingredient's formula quantity → `Service` "compounding" (mixer). The Assembler is the "start only when all ingredients are in" gate of `basicmodels/anykitchen.md`.
  3. `Service` "filling" → `Batch` up to chamber load → `Delay` "dry/sterilise" with capacity = chamber count → `Unbatch`. This reuses the autoclave idiom of `models/autoclaved-aerated-concrete-factory.md`.
  4. `Service` "pack & label" → QA release, e.g. a `Delay` in "until stopDelay()" mode (gotcha G7) → finished-goods stock → `Exit` to shipping.
- **Twin layers around the model** (context): operations/IoT feed → IoT hub → twin graph with one node per supplier, warehouse, truck and DC → data lake and databases (live and history) → AnyLogic what-if layer → web/mobile app (dashboards, alerts, 3D, forecasts). AnyLogic supplies only the simulation layer.

## Resources
QC analysts; mixers; filling lines; dryer and steriliser chambers (batch capacity); packaging lines; each node's delivery fleet; each node's storage capacity, split into refrigerated and ambient.

## Key settings worth copying
- **Flow unit = lot or batch agent** with an integer `units` attribute, never one agent per tablet. Per-tablet agents would break the PLE 50,000-agent cap (gotcha G5).
- An `Order` agent with a `status` field (pending → in progress → confirmed → delivered) feeds the "recent orders" panel directly.
- Build the KPI panel once, inside each node's agent type. Every instance then shows its own panel when opened.
- **Energy per node** (supplementary): an SD `Stock` whose inflow is the current power draw in kW integrates to kWh, provided the model time unit is hours.
  - Heating and lighting: base loads.
  - Refrigeration: scales with cold-store occupancy.
  - EV charging: energy per charge event.
  - Emissions: kWh × grid factor, plus km × vehicle factor.

## KPIs instrumented
- **Every node:** location, storage capacity vs stock, stock per product, pending orders.
- **Orders:** ordered quantity per product; recent orders with status.
- **Maintenance and quality:** disruptions, delays, failures; lost units at the distributor.
- **Energy by end use:** heating, EV charging, refrigeration, lighting.
- **Plant:** OEE with units/hour, throughput and defect rate (`videos/oee-instrumentation-in-des.md`).
- **Retailer:** quantity received per product.
- **Network:** logistics cost, chosen route, pollution per route.

## Pitfalls
- The demo names no replenishment policy and no decision. A twin without intake item A1 is only a dashboard, so settle the lever first.
- The demo skips several pharma realities; ask about them at intake (domain knowledge, not in the video):
  - shelf life, with first-expiry-first-out (FEFO) issue and expiry write-offs;
  - QA batch-release lead time;
  - cold-chain excursions, the cause behind "lost units";
  - GMP rejects and rework.
- Aggregate patients into one demand stream per hospital or pharmacy, unless patient behaviour is the question.
- The video shows no live-data mechanism. Two routes:
  - MQTT, as in AnyLogic's blog "Connecting AnyLogic to the physical world via MQTT (part 1)": add the Eclipse Paho JAR under the model's Dependencies, subscribe to topics, and act in `messageArrived`.
  - Polling a database.
- An "OEE predicted with Python" (Pypeline; `basicmodels/basic-functionality-interactive.md`) is a forecast. Show it beside the simulated OEE on the same definition, never instead of it.

## Reusable idea
Agents for echelons, DES inside each agent for orders and processing, one KPI panel per agent type. The pharma value lies in the plant chain (quarantine → QC → compound → fill → sterilise → pack → release) and in modelling lots rather than units.

## When the co-pilot should use this
- The intake mentions pharma, medical or hospital supply, or a "supply-chain digital twin".
- Use it at Stage 1 as the structural skeleton. Then fix the policy lever and pick KPIs from the panel list above.
- Ask which kind of "twin" is meant: offline what-if, initialised from a live snapshot, or live-synced. Only the last needs a data interface.
