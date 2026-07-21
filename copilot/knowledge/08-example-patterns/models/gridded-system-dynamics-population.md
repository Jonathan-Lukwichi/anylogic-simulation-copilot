# Pattern card — Gridded System Dynamics Population
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Models spatially distributed population dynamics where each geographic patch evolves via continuous stock-flow equations and animals migrate between neighbouring patches based on density gradients.

## Block chain

The study area is divided into a 2D rectangular grid of Patch agents. Each Patch is an autonomous agent that internally runs a two-stock System Dynamics sub-model: an **Immature** stock and a **Mature** stock. Animals are born into Immature at a rate driven by the Mature population multiplied by a per-capita BirthRate. They graduate to Mature after spending an average of MaturationAge years (flow = Immature / MaturationAge). Mature animals die at a rate derived from the remaining lifespan after maturation (flow = Mature / (AverageLifetime - MaturationAge)). A fourth flow, **NetMigration**, moves mature animals between a patch and its neighbours: the flow magnitude equals the sum of maturity differences with all neighbours multiplied by a MigrationDiffusionCoefficient, so animals diffuse from crowded patches toward sparse ones. Initial stock values for each patch are seeded with `uniform(100)`, giving each patch a random starting population up to 100. The top-level Main agent holds the grid population and exposes sliders for BirthRate, MaturationAge, and MigrationDiffusionCoefficient so users can interactively tune dynamics at runtime.

## Resources

- **Agent population:** `patches` — a 2D grid of Patch agents; grid size set at model level
- **Neighbour links:** fraction = 0.95 (near-full neighbourhood connectivity used in diffusion sum)
- **No external resource pools** — capacity is implicit in the continuous stocks within each patch

## Key settings worth copying

- `BirthRate` — per-capita annual birth rate (per year), applied as `Mature * BirthRate`
- `MaturationAge` — years spent in immature stage before joining mature stock
- `MigrationDiffusionCoefficient` — scales the net cross-patch flow; increase for faster spatial spreading
- `uniform(100)` — random initial stock seeding across all patches to avoid uniform initial conditions
- `NeighborLinkFractionCode = 0.95` — controls what fraction of neighbourhood links are active
- Time unit: **Year**; rates expressed as PER_YEAR throughout

## KPIs instrumented

- Count of mature population per patch (displayed as a dynamic colour-coded grid cell)
- Aggregate mature count across all patches (top-level dataset/chart)
- Patch cell fill colour computed via `lerpColor(countMature/100, paleGoldenRod, sienna)` — a continuous heatmap from low (pale) to high (dark) density

## Reusable idea

Embed a full SD stock-flow model inside each cell of an ABM grid and couple cells through a diffusion flow that reads neighbour state — this "SD-in-every-agent" pattern lets you capture spatially heterogeneous continuous dynamics (population ecology, pollutant spread, heat diffusion, inventory propagation) without discrete events, while still getting the spatial resolution of an agent grid.
