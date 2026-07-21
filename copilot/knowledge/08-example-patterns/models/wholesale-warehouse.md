# Pattern card — Wholesale Warehouse
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-zone wholesale warehouse with distinct inbound and outbound flows, multiple staff types, and spatially-aware pallet movement so zone utilisation bottlenecks can be identified and resource counts tuned interactively.

## Block chain

**Inbound (supply truck) flow:**
Supply trucks arrive at a scheduled/random interarrival interval and enter a RestrictedAreaStart (dock gate). Workers seize to unload pallets onto a Queue (unloadingQueue). A Delay represents unloading activity; pallets then move through a SelectOutput that routes them to the Reception/Accepting zone. Registrar staff seize in the accepting zone (acceptingWaitQueue), mark/handle the pallet with a Delay, then release. Forklift resources seize, carry the pallet via MoveTo to the Storage zone, and release. Trucks exit via RestrictedAreaEnd to Sink.

**Outbound (order fulfilment) flow:**
Customer orders arrive on a uniform interarrival schedule and queue in orderQueue. A Seize block claims a forklift; custom Java code (`uniform_discr`) selects a random pallet from the in-memory storage list. The forklift transports the pallet via MoveTo to the Dispatch/Control zone. Controller staff seize for quality checking (Delay, triangular distribution). A smaller retail truck enters via RestrictedAreaStart, loads the pallet, and departs through RestrictedAreaEnd to Sink.

Key routing blocks: SelectOutput, Split, RestrictedAreaStart/End, MoveTo, Delay, Queue, Seize, Release, Source, Sink.

## Resources

| Pool | Parameter | Default |
|---|---|---|
| Forklift trucks | `forkliftsNumber` | user-configurable via text input |
| Controllers (dispatch checkers) | `controllersNumber` | user-configurable via text input |
| Servicing/unloading staff | implicit in zone queues | zone capacity parameters |

Zone capacity parameters (all runtime-editable): Unloading zone, Accepting zone, Accepting wait zone, Control zone, Dispatch zone, Placement zone.

## Key settings worth copying

- **Time unit:** Minutes
- **Supply truck interarrival:** uniform between configurable min and max (parameters exposed as labeled sliders)
- **Order interarrival:** uniform between configurable min and max
- **Controller check duration:** `triangular(0.5, 1, 1.5)` minutes
- **Unloading/handling duration:** `triangular(5, 10, 15)` minutes
- **Pallet selection from storage:** `uniform_discr(0, palletsInStorage.size() - 1)` — random pick from live collection
- **Capacities changed dynamically** at runtime through text-input widgets (no recompile needed)

## KPIs instrumented

- Forklift utilisation: `forklift.busy() / forkliftsNumber` displayed as time-series chart
- Controller utilisation: `controller.busy() / controllersNumber` displayed as time-series chart
- Zone utilisation shown as bar charts positioned spatially next to each warehouse zone
- Queue lengths: unloadingQueue, acceptingWaitQueue, orderQueue, waitForLoadingQueue
- A dedicated resource utilisation screen provides over-time views separate from the 2D/3D warehouse layout

## Reusable idea

Expose all resource capacities and interarrival bounds as labeled runtime parameters connected to text-input widgets, so a non-technical operator can run what-if scenarios by typing new values mid-simulation without touching model logic — the pattern cleanly separates "knobs" from process flow.
