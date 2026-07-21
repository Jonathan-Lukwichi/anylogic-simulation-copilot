# Pattern card — Consumer Credit
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a bank's consumer credit approval pipeline, measuring staff utilisation and finding the optimal headcount for clerks, analysts, and security specialists.

## Block chain
Applications arrive according to a schedule-driven rate (`clientIntensity` rate schedule attached to the Source). Each entity first hits a **smallAmount** SelectOutput that immediately fast-tracks small-loan requests while larger ones queue for a full in-branch or online path. Applicants who have no existing account pass through a **noAccount** branch before entering the main scoring stage.

Verification proceeds in three sequential gates:

1. **Scoring** — automated credit-score check (Service/Delay); failure exits to a `scoringFailure` Sink; success continues.
2. **Personal review (meeting)** — a `waitingHall` Queue feeds a `toMeeting` Delay where an analyst ResourcePool is seized; returning `checkedClient` flag on the agent entity is set to `true` after this stage.
3. **Credit-rating inspection** — a `scoringInspection` function is called at the `scoringResult` SelectOutput; a security specialist ResourcePool (`securitySpecialist`) handles the inspection Delay.

A Hold block (`openBank`) gates the in-branch sub-flow so that walk-in customers only proceed during opening hours. Online applicants bypass this gate via `onlineAppSubmit` and `ifOnlineApplication` SelectOutput routing.

The `checkedClient` boolean flag on each agent drives conditional service times: already-reviewed clients receive a shorter triangular delay than first-time visitors, implementing a fast-lane for returning applicants.

## Resources
- **Bank clerks** — ResourcePool, quantity set via slider parameter ("Bank clerks qty")
- **Analyst** — ResourcePool, quantity configurable; seized during the personal-review stage
- **Security specialist** — ResourcePool; seized during credit-rating inspection

## Key settings worth copying
- Arrival driven by a **rate schedule** (`clientIntensity`) rather than a fixed exponential — lets you model morning/lunch/closing peaks without changing the block chain
- Service times use **triangular distributions** throughout:
  - Small-amount fast-track: `triangular(2, 4)` minutes
  - Meeting delay: `triangular(5, 8)` min for checked clients vs. `triangular(50, 80)` min for new clients
  - Scoring stage: `triangular(10, 30)` minutes
  - Rating inspection: `triangular(60, 90)` minutes
  - Online submission: `triangular(1, 1.5)` minutes
- **Model time unit:** Minute
- `agent.checkedClient` boolean attribute set at the noAccount and online paths; read downstream to branch routing and set service-time expressions

## KPIs instrumented
- Utilisation of each ResourcePool tracked as `analyst.utilization() * 100` and `securitySpecialist.utilization() * 100`; displayed on dedicated time-series plots and bar charts
- Queue size and delay size inside `scoring` block displayed live
- Throughput counters on `smallAmount.outT.count()` (fast-tracked) and `smallAmount.outF.count()` (full process)
- Failed-scoring count via `scoringFailure` Sink

## Reusable idea
Stamp a **boolean flag on the entity** (`checkedClient`) the first time it completes a key stage, then use that flag to select a drastically shorter service-time distribution for any re-entry path — a clean way to implement "returning customer" fast-lanes inside a single process model without duplicating the entire block chain.
