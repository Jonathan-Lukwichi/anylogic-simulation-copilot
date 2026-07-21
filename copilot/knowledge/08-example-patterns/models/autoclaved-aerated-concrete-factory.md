# Pattern card — Autoclaved Aerated Concrete Factory
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Identify the binding constraint in a multi-stage batch manufacturing line so plant managers know which asset to scale for maximum throughput.

## Block chain
Raw slurry is prepared in a mixing station and poured into moulds (MouldProcessing). Each mould undergoes a precure/rising phase (Delay), then moves on a tilt-crane (TiltCrane) to the CuttingLine where the aerated cake is cross-cut into blocks. A LiftingCrane picks up the cut cake and places it onto bogeys that are loaded into one of several autoclaves (Autoclaving — modelled as a parallel set of chambers). After steam-curing the finished blocks are transported by an unloading crane to the finished-goods area. Two cutting lines run in parallel; a SelectOutput block routes cakes to whichever line is free. A Hold block gates flow when all autoclaves are occupied, creating back-pressure that reveals where queues form. Equipment states (idle / moving / loading / processing / broken) are tracked with statecharts on every crane and autoclave object, and their time-in-state is streamed live to dashboard charts.

## Resources
- Moulds — quantity configurable via `mouldQuantity` parameter
- Cutting Lines — 2 parallel lines (CuttingLine1, CuttingLine2)
- Multifunctional Crane — 1 unit with configurable speed and load time
- Standard/Tilt Crane — 1 unit
- Lifting Crane — 1 unit
- Autoclave traverse — 1 unit
- Autoclaves — count controlled by `autoclaveN` parameter (shown in combo-box selector)

## Key settings worth copying
| Parameter | Purpose |
|---|---|
| `precureTime` | Rising/pre-cure dwell time before cutting (minutes) |
| `crossCuttingTime` | Time for the cutting line to slice a cake |
| `autoclavingTime` | Steam-cure cycle duration per autoclave load |
| `mouldBrushingTime` | Mould cleaning time before re-use |
| `multifunctionalCraneSpeed` / `multifunctionalCraneLoadTime` | Travel and pick-up time for the main crane |
| `autoclaveTraverseSpeed` | Speed of the in-autoclave transfer car |
| `standartCraneSpeed` / `standartCraneLoadTime` | Parameters for the secondary crane |
| `autoclaveN` | Number of autoclaves — key lever for capacity sensitivity analysis |
- Time unit: **Minute**
- No stochastic distributions; all delays are deterministic parameters — making it a pure capacity/timing study rather than a variability study.

## KPIs instrumented
- Equipment utilisation by state (idle, moving, loading, processing) — live statechart charts for every crane and every autoclave
- Autoclave occupancy — per-chamber state visible in a chart array indexed by autoclave number
- Implicit throughput: completed mould cycles trackable via `toUnloadCraneCount` counter
- Process timing end-to-end: state-change timestamps logged (POURED → CUTTING_STARTED → CUTTING_FINISHED → PLACED_TO_BOGEY → AUTOCLAVING_STARTED → AUTOCLAVING_FINISHED)

## Reusable idea
**Statechart-per-resource + live state dashboard**: attach a statechart directly to each shared resource object (crane, autoclave chamber) and feed all statecharts into a single multi-series chart. This gives an instant Gantt-style utilisation overview without post-processing — you can see at a glance which resource is the bottleneck and how often it is starved vs. blocked, which is the core insight needed before investing in additional capacity.
