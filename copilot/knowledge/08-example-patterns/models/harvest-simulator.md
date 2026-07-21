# Pattern card — Harvest Simulator
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + Fluid)
- **Problem it solves:** Orchestrate three interdependent harvest machines (combine, grain cart, truck) whose grain-transfer connections form and break dynamically, with optional manual or automatic dispatch control.

## Block chain
The model centres on three mobile agent classes — **Combine**, **Cart**, and **Truck** — each carrying its own Fluid Library tank (hopper/bin) and governed by a multi-state statechart. The Combine harvests continuously via a FluidSource whose rate is set by `harvestRate()`; when its hopper Tank reaches capacity the statechart fires a transition that stops the source and signals the Cart. The Cart drives to the Combine, dynamically connects a Pipeline between the two tanks (FluidExit on the Combine side, FluidEnter on the Cart side), drains the hopper, then disconnects and shuttles to the Truck. The Truck similarly connects its own Pipeline to receive grain from the Cart, then travels to a static storage bin (another Tank) to offload through a final FluidEnter. All three statecharts run in parallel; transitions are triggered by tank-level thresholds (`amount()` vs `capacity`), proximity checks, and user/auto-mode flags. In interactive mode the user manually triggers Cart and Truck dispatch; in automatic mode the statecharts self-dispatch based on fill levels. Vegetation is seeded with `uniform()` across the field grid at startup for visual fidelity.

## Resources
- **Combine hopper** — Tank with parameterised capacity; filled by FluidSource at `harvestRate()` bu/min  
- **Cart hopper** — Tank with parameterised capacity; intermediate buffer  
- **Truck bin** — Tank with parameterised capacity; transport vessel  
- **Storage bin** — Static Tank (on Main); final destination  
- **Pipelines** — dynamically connected/disconnected FluidEnter–FluidExit pairs on each machine pair

## Key settings worth copying
- Time unit: **Minute**  
- Harvest fill rate: controlled by `harvestRate()` method on the Combine (set on statechart entry action: `grainIn.set_rate(harvestRate())`, cleared on exit)  
- Cart/Truck speed synchronised to Combine speed during unload-on-the-go  
- Vegetation units placed with `uniform(field.getWidth()-2)` / `uniform(field.getHeight()-2)` at startup  
- Tank capacity checked via `amount()` / `capacity` ratio, used both for KPI bars and transition guards  
- Dual control modes: interactive (user button) vs automatic (statechart self-dispatch) toggled at runtime

## KPIs instrumented
- Hopper fill level displayed as a proportional bar: `height = amount()/capacity * 91` px  
- Transfer-flow visibility indicator: `grainIn.out.rate() > 0` drives a visible animation element  
- Implicit throughput: grain reaching the storage bin (bin.amount()) tracks cumulative harvest

## Reusable idea
**Dynamic fluid-connection pattern** — Pipeline objects between agent-carried tanks can be connected and disconnected at runtime (attach FluidExit to FluidEnter when agents meet, detach on departure). This lets you model any intermittent bulk-transfer scenario (refuelling, tanker docking, bin-tipper exchange) without fixed topology, simply by wiring the connection in the statechart entry action and severing it on exit.
