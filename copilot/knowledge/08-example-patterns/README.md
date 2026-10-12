# 08-example-patterns

Distilled "pattern cards" extracted from AnyLogic's built-in example models (525 `.alp` files
ship with 8.9.10: `basicmodels/`, `models/`, `sdmodels/` and the Big Book companions in
`bigbookmodels/`), from *The Big Book of Simulation Modeling* chapters (`bigbook/`), from AnyLogic
videos (`videos/`) and from the AnyLogic Cloud model library. The full list is `INDEX.md`.

A pattern card captures, in YOUR OWN words: the modeling paradigm, the block chain, the key
settings, the resources, and the KPIs of a worked model. Cards make the co-pilot give
AnyLogic-idiomatic answers grounded in how experts actually build.

IMPORTANT (IP): the bundled example models are AnyLogic's copyrighted content. Read them for
your own learning, but do NOT copy their .alp/.java verbatim into this (shareable) kit.
Write original, distilled cards. See ../../scripts/generate-pattern-cards.md to build them
with Claude Code from your local install.

**Markup built by code** — every space library can be built in Java at start-up: transporter
networks (`basicmodels/create-transporter-network-by-code.md`), roads (`create-road-network-by-code.md`),
conveyors (`create-conveyor-network-by-code.md`), GIS routes (`create-gis-network-by-code.md`) and rail
yards (Help 8.9.10 *Create rail yard by code*). Common rules: every element needs its owner, the
network is frozen once its level (or GIS elements) is initialised, and shapes must be added to
`presentation` to be drawn. For editable, saved markup use the design-time API instead
(`videos/layout-candidates-and-design-time-api.md`). Structure from data — assets per site, cars per
train — loads as nested *Loaded from database* populations
(`basicmodels/feeding-populations-from-anylogic-database.md`, `create-trains-from-database.md`); add a
start-up check that every parent has children.
