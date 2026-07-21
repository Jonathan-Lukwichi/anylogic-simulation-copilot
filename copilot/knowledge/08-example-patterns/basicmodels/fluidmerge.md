# Pattern card — FluidMerge
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous)
- **Problem it solves:** Combining two continuous fluid streams into one outlet under switchable merging policies (neutral, proportional, or priority-based).

## Block chain
Two independent FluidSource blocks (each pumping at 100 m³/s) feed into a single FluidMerge block, which blends the incoming flows according to the selected mode. The merged stream exits through a FluidDispose block that absorbs all outflow without accumulation.

## Resources
No discrete resource pools. The "capacity" concept is replaced by flow rates on both input ports of FluidMerge. Each source operates at a fixed rate of 100 cubic metres per second; the merge block's output rate is the combined total subject to the active mode.

## Key settings worth copying
- **Flow rate:** 100 CUBIC_METER_PER_SECOND per source (constant, no distribution)
- **Time unit:** Second
- **Merge modes (switchable at runtime via radio buttons):**
  - `SPLITMERGE_NEUTRAL` — both inputs contribute freely up to available capacity
  - `SPLITMERGE_PROPORTIONAL` — output is split proportionally between the two sources
  - `SPLITMERGE_PRIORITY` — one input is fully satisfied before the other receives any flow; priority can be set to input1 or input2, or delegated to custom per-batch priorities via `customPriorities` flag
- Runtime controls (radio buttons, checkbox) call `fluidMerge.set_mode()` and `fluidMerge.set_priorityInput1()` so the user can compare policies mid-run without restarting.

## KPIs instrumented
- `fluidMerge.in1.rate()` — live flow rate arriving on port 1 (displayed in a TimeStackChart)
- `fluidMerge.in2.rate()` — live flow rate arriving on port 2

## Reusable idea
The key transferable trick is **runtime policy switching on a merge/split node**: by wiring UI controls directly to `set_mode()` and `set_priorityInput1()`, a single model lets the analyst compare all three merging strategies on identical inputs without rebuilding the experiment — a pattern equally useful for split nodes, conveyor junctions, or any flow-routing decision point.
