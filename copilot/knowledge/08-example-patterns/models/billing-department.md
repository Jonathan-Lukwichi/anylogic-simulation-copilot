# Pattern card — Billing Department
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-resource invoice-processing workflow where two bill types follow divergent paths, share a bottleneck printer, and are subject to random supervisory audits.

## Block chain

Two independent arrival streams feed the system: normal invoices arrive with exponentially distributed inter-arrival times (rate `billsPerMinute`), while contact/contract invoices arrive at a separate rate (`contactBillsPerHour`). After arrival, each stream enters a SelectOutput block that probabilistically routes a fraction of bills to an audit step handled by a senior biller; the remainder bypass the audit. Post-audit (or post-bypass), bills converge on account billers or billing clerks depending on type, then queue for the shared printer (a single-resource Service block with adjustable capacity). The final step — stuffing and mailing — is handled by billing clerks before bills exit through a Sink. Stats are reset at run-start so the warm-up period is discarded cleanly.

## Resources

| Pool | Parameter | Default capacity |
|---|---|---|
| Senior biller | `seniorBillerCapacity` | 3 |
| Account biller | `accountBillerCapacity` | 3 |
| Billing clerk | `billingClerkCapacity` | 3 |
| Printer | `printerCapacity` | (slider-controlled) |

All capacities are exposed as interactive sliders so experiments can be run without stopping the simulation.

## Key settings worth copying

- **Arrival distributions:** `exponential(billsPerMinute)` for normal bills; separate rate parameter for contact bills — two sources, one model.
- **Service time distributions:** `triangular(min, mode, max)` used throughout (values range from triangular(0.3, 0.9, 2) for fast steps up to triangular(10, 15, 20) for longer operations), all in minutes.
- **Audit routing:** `SelectOutput` block with a probability condition — no agent attribute needed; the block itself encodes the branching logic.
- **Shared printer:** a single Service block referenced by multiple upstream paths, capacity controlled by a runtime slider.
- **Time unit:** Minutes throughout.
- **Startup inject:** `normalBillsArrive.inject(1)` at model start to seed the first arrival immediately.

## KPIs instrumented

- Utilization of each resource pool: `seniorBiller.utilization()`, `billingClerk.utilization()`, `accountBiller.utilization()`, `printer.utilization()` — all displayed as live gauges.
- Distribution of bill processing times (histogram charts).
- Throughput visible via Sink counts per bill type.

## Reusable idea

**Expose all capacity parameters as runtime sliders and reset stats on demand.** This lets a practitioner run what-if capacity experiments interactively during a single simulation run — no recompile, no parameter sweep setup — making it ideal for rapid stakeholder demonstrations where you want to show "what happens if we add one more printer" live on screen.
