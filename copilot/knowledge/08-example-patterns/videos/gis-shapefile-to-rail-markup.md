# Pattern card — Rail yard (or road grid) from a GIS shapefile: convert, then curate
- **Source:** AnyLogic video "Converting GIS shapefiles to AnyLogic rail markup" (https://youtu.be/N3p2_BMVUJE) — distilled, original wording
- **Paradigm:** Method (space-markup workflow for Rail Library models)
- **Problem it solves:** Get the track layout of an existing rail yard into a Rail Library model without drawing every track and switch by hand.

## Mechanism
1. **Start clean.** Put a GIS Map on an agent diagram that has no rail (or road) markup yet; the map cannot be added once such markup exists.
2. **Load the railway layer.** GIS Map → *Shapefiles* → `+` → the `.shp` of the railways theme (a regional package, like the video's Dresden set, has one file per theme). The files are copied into the model folder.
3. **Frame the yard.** Edit the map and zoom until exactly the tracks you need are in view.
4. **Convert.** Right-click the map → *Convert Shapefile to Space Markup* → Convert to = **Railway**, Conversion boundaries = **Visible only** → confirm.
5. **Result.** The GIS map is replaced by a static image, with Railway Track and Switch elements drawn over it. Continue with Rail Library blocks (TrainSource, TrainMoveTo…; `basicmodels/hump-yard-phase-1.md`).

## Resources
n/a

## Key settings worth copying
- **Coordinates.** The video says the shapefile must be "in Mercator projection". The Help's GIS notes are more exact: the map (OpenMap) translates decimal-degree latitude/longitude, assumes the WGS 84 datum with no datum conversion, and does not easily handle Cartesian (metre) grids; it then draws that data in Mercator. Reproject UTM or national-grid data to EPSG:4326 first (QGIS *Save Features As*, or `ogr2ogr -t_srs EPSG:4326 out.shp in.shp`). Whether metre-based Web Mercator (EPSG:3857) loads correctly is *(unverified)*. The Help's suggested sources (diva-gis.org railroads by country, geofabrik.de extracts) are already latitude/longitude.
- **Names** (Help 8.9.9): set *Name column index* in the map's Shapefile settings to the attribute column that holds track names; otherwise tracks come out as `track145`, `track146`…
- **Other targets** (Help, same steps): Roads for the Road Traffic Library (every road comes out two-way with two lanes each way, and speed limits are not read — fix lanes and speeds by hand), GIS network, network of paths, and pedestrian walls. Building plans usually come as CAD instead: `videos/cad-drawing-to-pedestrian-walls.md`.
- **Version** (release notes): since 8.9.8 converted track ends less than 30 cm apart are joined with a switch; earlier versions joined only exactly coincident ends, and before 8.8.0 switches could be missing altogether.
- **Topology count:** the railway network's `getTracks().size()` and `getSwitches().size()`, compared with the source map.

## KPIs instrumented
n/a (a geometry-preparation step).

## Pitfalls
- **Open ends leave the model.** A track end without a switch is open, and a car that runs off it leaves the rail yard model (Help, *Railway track*). The visible-only boundary cuts lines and leaves such stubs; trim them, or end them where trains really stop.
- **Crossings are invisible.** Tracks that cross without a switch are not detected as crossings, and collisions are signalled only at switches (Help, *Railway network*). Real diamond crossings need explicit blocking logic (`models/level-junction.md`).
- **Junction types.** Check each generated switch: all-to-all (the default type), single slip or double slip. Slip types need two opposite acute angles or the run errors (Help, *Switch*). Which type the converter assigns is *(unverified)*.
- **Too much area.** Converting a city-wide view is slow and yields thousands of tracks; zoom first.
- **No GIS space afterwards.** The agent that held the map now shows an image. A model that also needs a country-scale GIS layer keeps it in another agent (`basicmodels/agent-moves-between-spaces.md`).
- **Mapped data is not the operating yard.** Shapefiles hold centrelines of what someone mapped; sidings may be missing or already removed. Compare with a site plan or aerial image, and measure one known track length after conversion (and again after any scale change, G26).

## Reusable idea
Import the topology, then curate it: trim to the boundary, name, connect, set the switch types and block the crossings. Conversion gives geometry, not a verified operating network.

## When the co-pilot should use this
| Question | Route |
|---|---|
| Trains or wagons between cities or terminals; travel time matters, track occupancy does not | GIS agents routed over OSM rail (GIS Map → Routing → Road type = Rail); no Rail Library |
| Yard operations: switching, occupancy, coupling, humping, collisions | Rail Library markup: converted from a shapefile (this card), drawn by hand, or scripted with the Python design-time API (Professional / University Researcher; `videos/layout-candidates-and-design-time-api.md`) |
| A real street grid for Road Traffic | The same conversion with Convert to = Roads |

Trigger: Phase 0 item 8 turns up an existing yard, port rail terminal, mine or plant rail network.
