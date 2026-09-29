# Knowledge-base manifest

`type` = how the co-pilot should consume it.
**download** = pull a clean copy into `knowledge/` (stable, version-independent).
**fetch-live** = read on demand via web fetch (changes per version / frequently updated).
**local (install)** = read in place from the user's AnyLogic installation; never copied into the KB.

| Category | Source | URL | type | Notes / licence |
|---|---|---|---|---|
| 00 method-selection | Borshchev & Filippov — Reasons, Techniques, Tools | https://www.anylogic.com/resources/articles/from-system-dynamics-and-discrete-event-to-practical-agent-based-modeling-reasons-techniques-tools/ | download | Free, AnyLogic-hosted. The approach-choice paper. |
| 01 anylogic-core | AnyLogic Help (block reference, RL, Alpyne) | https://anylogic.help/ | fetch-live | Version-specific; do not freeze. Blocks automated fetches (HTTP 403, seen 2026-09); fallback = the archived page `https://web.archive.org/web/2025id_/https://anylogic.help/<path>` fetched with `curl --compressed`. Prefer the offline Help below when an install is reachable. |
| 01 anylogic-core | AnyLogic offline Help + Javadoc (ships with every install, PLE included) | `<install>\plugins\com.anylogic.ui_<version>\resources\help\en\` | local (install) | Exact to the installed version; ~2,700 HTML pages mirroring anylogic.help, engine Javadoc under `plugins\com.anylogic.engine_<version>\javadoc\`. How to search it: `knowledge/INDEX.md`. |
| 01 anylogic-core | AnyLogic in 3 Days (free PDF) | https://www.anylogic.com/resources/books/free-simulation-book-and-modeling-tutorials/ | download | Free. |
| 01 anylogic-core | Big Book of Simulation Modeling (Borshchev) | https://www.anylogic.com/resources/books/ | download | Free chapters. Covers DES+ABM+SD. Single chapters resolve as direct PDFs, e.g. ch. 15 (randomness): https://www.anylogic.com/upload/books/new-big-book/15-randomness-in-anyLogic-models.pdf |
| 01 anylogic-core | Cloud model library (examples by industry) | https://cloud.anylogic.com/models | fetch-live | Dissect example models. |
| 02 statistics | NIST/SEMATECH e-Handbook of Statistical Methods | https://www.itl.nist.gov/div898/handbook/ | download | Free. Distributions + goodness-of-fit. |
| 02 statistics | fitdistrplus (R) | https://cran.r-project.org/package=fitdistrplus | fetch-live | MLE/MME + KS/AD/CvM fits. |
| 02 statistics | scipy.stats (Python) | https://docs.scipy.org/doc/scipy/reference/stats.html | fetch-live | Fitting in Python. |
| 03 supply-chain | Ivanov — Operations & Supply Chain Sim w/ AnyLogic (free) | https://www.anylogic.com/upload/pdf/Ivanov_AL_book_2017.pdf | download | Free, official. |
| 03 supply-chain | anyLogistix supply-chain guide (free) | https://www.anylogistix.com/resources/books/alx-textbook/ | download | Free PLE guide. |
| 04 manufacturing | AnyLogic job-shop tutorial | https://anylogic.help/tutorials/job-shop/ | fetch-live | Manufacturing DES. |
| 05 healthcare | DES in the ED — systematic review (open access) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5406177/ | download | Free. ED modeling framework. |
| 05 healthcare | DES in Healthcare — comprehensive review (IJERPH/MDPI) | search title (MDPI, open access) | download | Free. Efficiency-metric focus. |
| 06 ai-ml | AnyLogic AI / RL / Alpyne | https://www.anylogic.com/features/artificial-intelligence/ | fetch-live | RL experiment + Alpyne + Azure ML. |
| 06 ai-ml | FlexSim Reinforcement Learning docs | https://docs.flexsim.com/ (Reinforcement Learning) | fetch-live | Alternative tool; Gym + SB3. |
| 07 optimization | AnyLogic Optimization experiment / OptQuest | https://anylogic.help/ (Optimization) | fetch-live | Parameter optimisation. |
| 07 optimization | Winter Simulation Conference proceedings | https://informs-sim.org/ | fetch-live | Free tutorials: DES, ABM, sim-opt, input modeling. |
| 07 optimization | AnyLogic 8.8.4 release notes (Genetic engine, OptQuest limits, export licensing) | https://www.anylogic.com/blog/anylogic-8-8-4-genetic-optimization-and-pedestrian-elevators/ | fetch-live | Source of the "bundled OptQuest: 7 variables / 500 iterations" limit (gotcha G14); limits and licensing change by version — re-check each release. |

## AnyLogic videos distilled into the KB (2026-09)

Transcripts are fetched with the skill `../.claude/skills/youtube-transcript/` into
`knowledge/transcripts/` (**gitignored** — the publisher's text stays local). Only the
novelty-gated, own-words result is committed: cards in `knowledge/08-example-patterns/videos/` and
entries G7–G60 in `knowledge/01-anylogic-core/anylogic-gotchas.md`. Every candidate fact was checked
against the KB, the text of its local PDFs and the AnyLogic 8.9.9 Help first: across both rounds 675
items were checked: 295 were new and added; 380 were already known and skipped.

| Video | Title | Result |
|---|---|---|
| 88D95QYtduM | How to use agents in a process flow | `statechart-agent-through-hosted-flowchart` |
| IpSr9CDVGz0 | How to simulate multi-level facilities | `multi-level-facility-lift-landings` |
| L5SD_QdUUKE | How to add 3D animation in your models | `flowchart-block-animation-binding`, `3d-scene-z-order-and-lighting` (camera/navigation steps were already in *AnyLogic in 3 Days*) |
| YyDJDqMqYng | Webinar: Simulation-Based Optimization in AnyLogic | `sim-opt-dual-formulations-and-bounds`, `sim-opt-lucky-optimum-and-shortlist-reverification`, `sim-opt-search-space-reduction`, `dispatching-rule-as-optimizable-policy`, `optimizer-engine-and-venue-choice` |
| pY44q0g3LAE | Webinar: Fundamentals of the AnyLogic Material Handling Library | `mhl-convey-routing-offsets-leave-on-exit`, `mhl-conveyor-types-spur-priority-transfer-elements`, `mhl-conveyor-station-processing-and-reassembly`, `mhl-conveyor-control-sensors-and-breakdowns`, `mhl-agv-dispatch-choice-and-cargo-position`, `mhl-crane-reach-safe-height-movement-mode` |
| uyVqhY-aZSo | Supply Chain Management Twin for Pharmaceutical Using AnyLogic | `pharma-supply-chain-twin-hybrid`, `oee-instrumentation-in-des` |
| UVppYf_O4H8 | Webinar: How Simulation-Driven Insights Strengthen Strategic Decision-Making | `boundary-extension-bottleneck-migration`, `cloud-decision-tool-for-stakeholders`, `forecast-driven-staffing-optimization`, `layout-candidates-and-design-time-api` |
| iJYW24Yk170 | How to simulate a shuttle train | `rail-shuttle-pedestrian-boarding` |
| JcFqegObRK8 | How to measure the agents' time in the system | `time-in-section-measurement-and-execution-log` |
| 3pM30wQfxV8 | How to run optimization experiment | `optimization-requirement-on-time-averaged-kpi` |
| 0Nu1a9Te6ac | How to create concise process flowcharts | `custom-flowchart-block-from-repeated-chain` |
| m96PLSEIALg | How to run reproducible and unique experiments | `rng-seed-control-and-custom-generator` |
| Wjx2xnFTj8I | How to simulate a spiral conveyor | `spiral-conveyor-per-point-z` |
| tjbS9FcuT2A | How to convert CAD drawings to walls | `cad-drawing-to-pedestrian-walls` |
| LHcu91DxE4g | How to simulate a pedestrian crossing | `traffic-light-gated-pedestrian-crossing` |
| YniPxHYfbrc | Custom probability distributions | `custom-empirical-distribution-agent-attributes` |
| WIU8-2hqyqM | How to generate 3D objects of different colors | `per-agent-3d-material-color` |
| F93iENzUcWc | AnyLogic Cloud | `cloud-run-semantics-and-access`, `cloud-api-programmatic-runs` |
| AdvSDuvk78U | Reading agent attributes from a database | **no card — already known** (*AnyLogic in 3 Days* teaches the same flow) |
| UKCd6BFwdlg | Placing agents on the GIS map | `gis-agent-placement-from-table` (G51) |
| pd8QMBL-ri4 | Setting up parameters from the experiment page | `experiment-page-pre-run-controls` (G50) |
| LVoEVGHKHZk | Using files as inputs and outputs in AnyLogic Cloud | `excel-round-trip-results-and-cloud` (G46–G49) |
| N3p2_BMVUJE | Converting GIS shapefiles to AnyLogic rail markup | `gis-shapefile-to-rail-markup` (G52) |
| ImC_ZVHs3tc | Simulation Basics Explained (third-party course) | **no card — already known** (general simulation basics) |
| UT38puq5VP4 | ABM Tutorial Part 1 — consumer market problem | **no card** — follows *AnyLogic in 3 Days* (Market model); prompted the G2 note on time units |
| InF63gDYLk4 | ABM Tutorial Part 2 — consumer population | **no card — already known** |
| k69Ow9q8gBc | ABM Tutorial Part 3 — statecharts | `agent-type-graphics-visible-on-upper-agent` (G54) |
| V_wPH3O0Wb0 | ABM Tutorial Part 4 — statistics and charts | gotcha G53 (`item` → `agent`) |
| sAQ0BOf5XgM | ABM Tutorial Part 5 — word of mouth | `abm-word-of-mouth-contact-targeting` (G57) |
| t1VDziRGpco | ABM Tutorial Part 6 — product discard | **no card — already known** |
| E_ik0KFA_Sk | ABM Tutorial Part 7 — delivery time | gotcha G55 (`triangular`: mode is not the mean) |
| iVOqcz5iZTw | ABM Tutorial Part 8 — consumer impatience | `statechart-live-controls-trigger-reevaluation` (G56) |
| tgS0flXRM4E | ABM Tutorial Part 9 — comparing runs | **no card — already known** |
| pDpw9h09gss | Complete 2.5-hour ABM tutorial | **no card** — 94% identical to Parts 1–9; the remaining lines were reviewed and held nothing new |
| HBd_dKNVrSU, 63V7dBGjb14, nKW8GG5og4U, QocfkYnwSYw, UgH7g5PhG90 | "Scenario 1" ABM market-competition series (Parts 1–5) | `abm-adoption-flow-counters-vs-state-counts`, `abm-wom-conversion-rate-vs-probability`, `abm-stock-gated-purchase-allocation-and-brand-tie` (G58–G60) |

