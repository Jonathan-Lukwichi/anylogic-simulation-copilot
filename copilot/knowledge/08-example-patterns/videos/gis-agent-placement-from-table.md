# Pattern card — GIS placement from a table: store coordinates, don't re-search place names
- **Source:** AnyLogic video "Placing agents on the GIS map" (https://youtu.be/UKCd6BFwdlg) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Put a population of real sites (stores, depots, clinics, turbines) at their true map positions straight from a spreadsheet, in a way that stays correct and repeatable.

## Mechanism
- **The video's route.** The table-driven population wizard (*Use database table*; already in *AnyLogic in 3 Days* pp. 237–238) proposes one parameter per column. In its *Agent parameters mapping* table, the address column is pointed at the built-in target **GIS location name** instead of a new parameter. The demo placed 12 bookstores from a one-column Excel sheet of street addresses.
- **What that target means** (Help 8.9.9, *Placing agents in GIS space*, *Agent population*): *Initial position → Place agent(s) = in the first result of map search*, with the column as the *Location name*. At every start the text goes to an online search, and the agent lands on the **first** hit.
- **The coordinate route.** Map two numeric columns to **GIS location latitude** and **GIS location longitude** (*Place agent(s) = in the latitude/longitude*). No search is involved.
- **Placement happens when the run starts.** In the editor every agent of the population sits at the map centre; that is normal.

## Resources
n/a

## Key settings worth copying
- Coordinates: decimal degrees, latitude −90…90, longitude −180…180, on the WGS 84 datum (the map cannot convert other datums — Help, *GIS models*).
- GIS Map → **Search** (Help): searches at startup cover the area visible at launch (default) or a fixed **Custom search bounds** box. If nothing matches inside, the search widens; with custom bounds the closest same-name place outside is taken.
- Code: initialise with `setLatLon(lat, lon)` or `setLocation(gisPoint)` (initial placement only, per the Help); relocate later with `jumpTo(...)`, which also takes a place name to search, e.g. `jumpTo("Leeds, UK")`. Map API: `map.searchFirst(query)` returns a `GISPoint` (`getLatitude()`, `getLongitude()`); `map.search(query, area, visibleAreaOnly)` returns all hits.
- PML blocks that create or move agents (Source, Enter, MoveTo…) offer the same three choices: Network / GIS node, Latitude/Longitude, or *Name of place* (again the first search hit).
- **Geocode once.** For a handful of sites: search in the editor, then GIS Search Results → *Convert To GIS Points*; the points are saved with the model. For a list: keep the address as a parameter too (e.g. `address`, so each agent can find its row), add empty `lat` / `lon` columns, run once with name placement, write the resolved coordinates back from Main's On startup, then switch the mapping to latitude/longitude *(suggested, not tested)*:
  ```java
  for (Store s : stores)
      update(store_sites).where(store_sites.address.eq(s.address))
          .set(store_sites.lat, s.getLatitude()).set(store_sites.lon, s.getLongitude()).execute();
  ```

## KPIs instrumented
n/a (a set-up step). Add a placement check at startup: count agents whose `getLatitude()` / `getLongitude()` fall outside the study region's bounding box and stop with `error(...)` if any do.

## Pitfalls
- **First hit, searched region.** With only Paris in view, the Help's GIS tutorial got a Paris metro station for "Rennes". Frame the whole region (or set Custom search bounds) and make names unambiguous: street, city, country.
- **Messy addresses fail silently** (the video's warning): typos, abbreviations or a missing town put agents in the wrong place, and the model still runs.
- **Online and version dependent.** A tiled map searches an online server, so it needs a network (Help). The search server was replaced in 8.8.5, and search was broken until a fix in 8.9.5 (release notes). The same table can therefore land differently on another machine or version. Each run searches again, which is slow for big populations *(inferred)*. Whether Cloud runs reach the search service is *(unverified)*.
- **Swapped or text coordinates.** Latitude and longitude in the wrong columns, or degree-minute-second strings, put agents in the wrong hemisphere or the sea.

## Reusable idea
Geocode once, simulate many times. Resolve names to coordinates a single time, keep the numbers in the input table, and let every run read numbers — the same rule as freezing any other input (G17).

## When the co-pilot should use this
- Phase 0 item 8: sites are real places (retail or depot networks, service areas, field assets). Ask for coordinates first; accept addresses only with a geocode-once step.
- A user reports agents in the wrong city or in the sea, or results that differ between machines.
- Before promising an offline, standalone or Cloud deliverable that uses a GIS map.
- Related: supply-chain network cards `videos/pharma-supply-chain-twin-hybrid.md`, `models/corporate-education.md`.

## Additions (8.9.10 review, 2026-10-01)
- Routing has its own silent fallback: with *If route not found* = Create straight route, an unroutable trip becomes a straight line (gotcha G104; `gis-routing-source-caching-and-straight-line-fallback.md`). Map tiles and routes are cached in the model folder; offline runs need both.
