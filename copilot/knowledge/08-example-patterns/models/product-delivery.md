# Pattern card — Product Delivery
- **Source:** AnyLogic example model "Product Delivery" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Hybrid
- **Problem it solves:** Deliver distributor orders from production sites by truck on a GIS road network. Production is continuous, orders are processed as discrete jobs, and each truck is an autonomous agent that also counts as a pooled resource, so fleet size, stock and waiting time can be read together.

## Block chain
- **Agents on a GIS map:** 3 manufacturing centers, 15 distributors, trucks (`Vehicle`), and orders (a small agent
  type used as the message). On startup each distributor is tied to the center nearest **by road**
  (`getNearestAgentByRoute(manufacturingCenters)`).
- **Distributor:** a cyclic event every 1–2 days creates an order for 500–1000 units and `send`s it to its center.
- **Center (inside the agent):**
  - The receive action of the center's `connections` link object passes each message into its own flowchart with
    `processOrder.take(msg)`.
  - `Enter` → `Queue` (orders) → **`Delay` "wait for products"** (capacity 1). Its delay is 0 if stock covers the
    order, otherwise shortfall ÷ production rate. On exit it deducts the amount from the stock.
  - → `Seize` a truck from the center's `ResourcePool`. *On seize unit* runs `send(order, unit)`.
  - → **`Delay` "delivering"**, *Until stopDelay() is called*, maximum capacity → `Release` → `Sink`.
- **SD inside the center:** stock `products`, filled by `productionRate = capacity` (50–80 units per hour), starting
  at 1000–2000 units.
- **Truck statechart:**
  1. *idle* → message received (keeps the order).
  2. Loading, 1–2 h → `moveTo(order.distributor)` along the roads.
  3. Unloading, 1–2 h → `moveTo(center)`.
  4. On arrival home, calls `center.delivering.stopDelay(order)` → *idle*.

  The order leaves the manual Delay only then, and `Release` frees the truck. The whole round trip therefore counts as
  busy time.

## Resources
One `ResourcePool` per center: *New resource unit* = `Vehicle`, 1–3 units (random per center), speed 90 km/h, units
added to Main's custom population `vehicles`. *On new unit* stores the home center and places the truck there with
`setLocation(this)`.

## Key settings worth copying
- **Resource unit that does its own work:** `Seize` → *On seize unit* `send(agent, unit)` → `Delay` type
  *Until stopDelay() is called* → the unit's statechart runs the trip and calls `stopDelay(order)` → `Release`.
  The pool keeps the queueing, priorities and utilisation statistics. The agent keeps the movement and the
  multi-step behaviour (Help 8.9.10 `seize.html` On seize unit, `delay.html` `Delay.MANUAL`, `resourcepool.html`
  New resource unit / On new unit / custom population).
- **Wait computed, not polled:** the delay equals the time the constant inflow needs to cover the shortfall. It is
  exact only because the Delay admits one order at a time (so orders draw on the stock in FIFO order) and the
  production rate is constant.
- **Message into flowchart:** the receive action of `connections` runs `enterBlock.take(msg)`, the bridge from ABM
  messages to the DES process.
- Randomised per-center parameters at population level: `uniform_discr(1, 3)` trucks, `uniform_discr(50, 80)`
  rate, `uniform(1000, 2000)` initial stock.

## KPIs instrumented
- Fleet utilisation per center (`fleet.utilization()`, bar chart, %).
- Stock of products per center (time stack chart).
- Time orders wait for product (`waitingForProduct` statistics on Main).

## Pitfalls
- **The computed wait goes stale** if the rate varies, the Delay admits more than one order, or something else
  withdraws stock. In those cases hold orders in a `Wait` or `Hold` and release them when stock suffices.
- **The order must be released by the same object.** The truck keeps the order reference and passes it to
  `stopDelay`. If a truck is removed or its statechart never reaches that transition, the order waits forever
  without an error.
- The nearest-by-road assignment is fixed at startup: it ignores backlog and fleet size, so there is no load
  balancing between centers.
- Contrast with sending an order straight to "the nearest idle truck" (the AnyLogic *Supply Chain GIS* tutorial,
  step 4). That returns `null` when every truck is busy. Seize and ResourcePool queue the orders instead.

## Reusable idea
Split duties: the **flowchart owns queueing and resource accounting**, and the **resource agent owns physical
behaviour**. Connect the two with *On seize unit* → `send`, plus a manual Delay released by the agent. Where stock is
continuous (SD) and consumers are served one at a time, compute the wait instead of polling a condition.

## When the co-pilot should use this
- Delivery or field-service fleets whose vehicles drive real roads (GIS) or have multi-step behaviour, while you still
  want pooled-resource statistics.
- Hybrid supply-chain models: SD production, DES order handling and ABM vehicles in one agent.
- Sizing trucks per depot against order waiting time and stock levels.

## Additions (8.9.10 review, 2026-10-01)
- `stopDelay(order)` with a null argument releases every agent in the Delay; guard the reference (gotcha G87).
