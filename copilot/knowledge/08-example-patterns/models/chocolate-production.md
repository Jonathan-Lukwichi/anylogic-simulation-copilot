# Pattern card — Chocolate Production
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES (Fluid / Continuous-flow variant using the AnyLogic Fluid Library)
- **Problem it solves:** Models a multi-stage bulk-material production line where raw ingredients flow continuously through processing vessels, splits, and merges rather than moving as discrete units.

## Block chain
Cacao beans enter as a continuous fluid stream via a **FluidSource**. A **BulkConveyor** carries the liquor to a **FluidSplit**, which divides the stream into two branches: one feeds a **ProcessTank** (the press) that separates cocoa butter from cocoa cake; the other branch bypasses directly toward mixing. Separated cocoa butter drains into a dedicated **Tank** (storage). Sugar, milk, and additional cocoa butter each have their own storage **Tank** nodes. All ingredient streams converge through a **FluidMerge** into a mixer/conching **ProcessTank** (the Conch), where the blend is held for a set residence time. The finished chocolate exits through a **FluidSink** or is routed onward to molding. **BulkConveyors** connect every stage, enforcing realistic transfer rates and pipe capacities between vessels.

## Resources
- Multiple **Tank** vessels: chocolate-liquor holding tank, cocoa-butter storage tank, sugar tank, milk tank, finished-chocolate buffer tank
- **ProcessTank** nodes for the hydraulic press and the conching (refining) stage
- **BulkConveyor** segments linking every tank and process stage
- **FluidSplit** nodes (at least two) to divide the liquor stream; **FluidMerge** to recombine ingredient streams before conching
- **FluidSource** (raw cacao liquor input) and **FluidSink** (product output)

## Key settings worth copying
- **Time unit:** Minutes — appropriate for bulk food processing where residence times range from tens of minutes to hours
- **ProcessTank residence time:** set per stage (press, conch) — tune to replicate actual batch cycle or continuous throughput targets
- **BulkConveyor flow rate / capacity:** constrains the pipeline between vessels; bottleneck identification relies on these values
- **FluidSplit ratios:** define the cocoa-butter-to-cake yield split from the press stage — parameterise this to explore different bean grades
- **Tank capacities:** upper limits on each storage vessel expose inventory-buffer sensitivity

## KPIs instrumented
- Tank **level** over time for each storage vessel (inventory tracking, overflow / starvation risk)
- **Throughput** of finished chocolate leaving the FluidSink (kg/min or similar)
- **Utilisation** of the press and conching ProcessTanks (fraction of time actively processing vs. starved or blocked)
- Residence time inside the Conch (quality proxy — longer conching improves texture)

## Reusable idea
Model any multi-ingredient blending or refining process as a **fluid network of tanks connected by conveyors with split and merge nodes** rather than discrete entities. This lets you see inventory levels, starvation, and overflow in real time without creating thousands of individual agent objects — and the FluidSplit ratio becomes a single parameter knob for exploring yield or recipe changes across the entire pipeline.
