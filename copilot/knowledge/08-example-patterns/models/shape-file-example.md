# Pattern card — Shape File Example
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Demonstrates how to place and move autonomous agents across a real-world geographic map loaded from a shapefile, with interactive selection and routing.

## Block chain
A population of Airplane agents lives inside a GIS Environment. On startup, each airplane is created and immediately sent to a randomly chosen latitude/longitude via `moveTo()`. A recurring timer periodically checks every airplane and, if it has finished its previous flight, dispatches it to a new random global coordinate. A click handler on the GIS map lets the user select any airplane and redirect it to any clicked point on the globe. Agents travel great-circle (minimum-distance arc) paths automatically. A text panel shows the selected airplane's name, heading, and distance to destination.

## Resources
- **Agent population:** `airplanes` — replicated embedded Airplane agents (count set at startup)
- **GIS Environment:** single environment with `SpaceType = GIS`, backed by the shapefile
- **No capacity-constrained resources** (no queues, pools, or seize/release)

## Key settings worth copying
- `uniform(-50, 50)` for random latitude; `uniform(-180, 180)` for random longitude
- GIS map tile URL: `http://a.tile.openstreetmap.org/[zoom]/[x]/[y].png` (OpenStreetMap)
- Shapefile assets: `world_borders.shp` + `.dbf` + `.shx` + `.ssx` bundled as model resources
- `ModelTimeUnit = Hour`
- Airplane color switches between `green`/`lime` (idle/moving) and `brown`/`red` (selected) using a conditional color expression
- `gisMap.getDistance(x1, y1, x2, y2)` used to compute and log great-circle distance before each flight
- `formatGeoHeading(getGISHeading())` displayed on the agent label

## KPIs instrumented
- Distance of each flight segment logged to console via `traceln`
- Selected airplane's real-time heading displayed in the UI panel
- No aggregated throughput, wait-time, or utilisation KPIs

## Reusable idea
Bundle a shapefile (`.shp`/`.dbf`/`.shx`) directly as model resources and attach it to a GIS Environment — agents then gain automatic great-circle movement, heading, and geo-distance APIs with zero external dependencies. This pattern is the minimal scaffold for any geospatial ABM that needs real country/region boundaries without a paid map service.
