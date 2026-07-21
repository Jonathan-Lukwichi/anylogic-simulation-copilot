# Pattern card — Agent Population and SD Housing
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (ABM + SD)
- **Problem it solves:** Show how individual agents (residents) and aggregate system-dynamics stocks (housing supply) co-exist in one model, with agents both reading from and writing to SD variables to create emergent price feedback loops.

## Block chain
The model contains a population of resident agents distributed across several geographic districts. Each agent carries an income value drawn from a custom empirical distribution table. At the SD layer, every district holds two stocks — AvailableHouses and OccupiedHouses — and a derived variable Occupancy (ratio of occupied to total units). A lookup function converts Occupancy into a base rent price, which is then smoothed through a third-order delay (delay3) with a configurable PriceReactionDelayTime parameter to mimic the lag between market tightening and landlord response. When a resident moves into a district the agent directly decrements AvailableHouses and increments OccupiedHouses, coupling ABM events to SD stocks. Agents inspect the RentPrice variable for their district when choosing where to move, closing the feedback loop: high demand raises occupancy, occupancy raises rent, rent deters future in-migration. Districts vary in area fraction, which sets their initial house count as TotalPopulation * AreaFraction * HousesRedundancy. A Comfort/attractiveness slider per district lets analysts explore how non-price preferences shift population distribution.

## Resources
- Agent type: Person (resident), population size proportional to TotalPopulation parameter
- SD stocks per district: AvailableHouses, OccupiedHouses (array-dimensioned by District enum)
- Districts: enumerated geographic zones, each with its own area, shape polygon, and comfort rating
- Connections per agent: 2 (network links)

## Key settings worth copying
- `IncomeDistribution` — built from an empirical table (IncomeDistributionTable.createCustomDistribution()), not a named parametric distribution; lets modelers load real income data
- `RentPrice[d] = delay3(PriceLookup(Occupancy[d]), PriceReactionDelayTime)` — third-order information delay prevents instantaneous price jumps
- `HousesRedundancy` scalar — controls the vacancy buffer above population; tune this to represent tight vs. loose markets
- Initial agent placement uses `uniform(0,600)` / `uniform(0,700)` random XY then checks whether the point falls inside a district polygon (`sh.contains(x,y)`)
- Time unit: Day; rate flows expressed in PER_DAY units

## KPIs instrumented
- Occupancy rate per district (continuous SD variable, plotted over time)
- RentPrice per district (lagged market signal)
- Income histogram of residents in the selected district (reset and rebuilt on district-select events)
- AvailableHouses count per district (tracks supply depletion or recovery)

## Reusable idea
Agents write directly to SD stocks during discrete events (move-in/move-out), and SD variables are readable by agents as environmental signals. This bidirectional ABM-SD coupling — where individual decisions aggregate into stock changes that then feed back as price signals shaping future decisions — is the core transferable pattern for any model combining discrete individual choices with continuous aggregate markets (labor markets, energy grids, healthcare capacity, etc.).
