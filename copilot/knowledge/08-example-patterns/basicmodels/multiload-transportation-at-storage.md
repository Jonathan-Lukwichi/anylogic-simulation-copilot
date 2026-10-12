# Pattern card — Multiload Transportation at Storage
- **Source:** AnyLogic example model "Multiload Transportation at Storage" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Material Handling Library)
- **Problem it solves:** Warehouse pickers (or AGVs) that collect several items per trip — for put-away and for order picking — instead of one item per trip.

## Block chain
- **Put-away:** `Source` *itemsArrival* (6/h; several items per arrival = `min(20, storage.nFreeCells())`, created at `itemsArrivalZone`) → `Store` (fleet `pickerGroup`, storage `storage`) → `Exit`.
- **Picking:** a cyclic event *orderGenerated* (every `uniform(3, 5)` s) picks 1–7 stored SKUs from a list `notOrdered`, pushes each into `Enter` *orderArrival* with `take(sku)` → `Retrieve` *pickFromRack* (fleet `pickerGroup`, deliver to `orderProcessingZone`) → `Sink`. If the list is short, it takes what is left and injects a replenishment of 10 into the Source (only when more than 10 cells are free).
- `StorageSystem` with *initial filling* = partial (`INITIAL_PARTIAL`) and random slotting; a one-off event copies `storageSystem.getAgents()` into `notOrdered`, because the initial stock is created by the StorageSystem, not by the Source.

## Resources
`TransporterFleet pickerGroup`: 2 pickers, free-space navigation, homes `pickerHome`, `pickerHome1`, **`maxNumberOfLoads = 5`**, **`deliveryStartPolicy = NO_AVAILABLE_AGENTS`**; cargo offset set per picker with `setCargoPosition(...)`.

## Key settings worth copying
- **Max number of loads** (`maxNumberOfLoads`, default 1) — items one transporter carries at once. New in **AnyLogic 8.9.9** (release notes), together with tugger trains; on older versions the usual route is Batch → move the batch → Unbatch *(workaround, unverified)*.
- **Delivery starts when** (`deliveryStartPolicy`): `FULL_LOAD` (may wait forever for more items), `TIMEOUT` (leave after *Pickup timeout per agent* with no new item; timer resets on each new item), `NO_AVAILABLE_AGENTS` (leave when nothing more is available or full — used here), `CONDITIONAL` (condition true or full, optional timeout). `startDelivery()` (8.9.10) forces a tugger train that is picking to deliver now.
- **Prefer partially filled transporters** (`preferPartiallyFilledTransporters`) — fill a vehicle already on a round before starting another.
- **Pick sequence by priority:** Retrieve *priority* = `1000 - agent.distanceTo(pickerHome.getX(), pickerHome.getY())` → items nearest the depot are collected first; `transporterTaskPreemptionPolicy = TPP_SEIZE_ANY_RESOURCE`.
- Guard arrivals against a full store: items per arrival = `min(batch, storage.nFreeCells())`.

## KPIs instrumented
Visual only (logic/3D views; ordered items highlighted per order colour).

## Pitfalls
- `FULL_LOAD` with irregular demand strands a half-full picker indefinitely; prefer `NO_AVAILABLE_AGENTS`, `TIMEOUT` or `CONDITIONAL`.
- The distance-from-home priority is a static proxy for routing — it does not re-sequence from the picker's current position. For real pick-path optimisation compute the order in code.
- Items created by *initial filling* never passed through your Source, so any list, counter or attribute set there is missing for them — collect them from `storageSystem.getAgents()`.

## Reusable idea
Batch picking and batch put-away are fleet settings, not flowchart changes: raise `maxNumberOfLoads`, choose the delivery-start rule, and let Retrieve/Store priorities shape the collection sequence. Compare trips, travel distance and order lead time for loads 1 vs k in a parameter variation.

## When the co-pilot should use this
Multi-item picking carts, milk-run pickers, AGVs with several slots, put-away rounds — and any user on 8.9.8 or older asking for this (explain the version gate). Tugger-train variants: see the `tugger-train*` cards (batch m-basic-4).
