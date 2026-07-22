---
name: stats-analyst
description: Statistics and data-analysis backbone for interpreting scenarios and results in PLAIN ENGLISH. Use whenever the user shares data or uploads simulation results/experiment outputs, asks "what does this mean", compares two scenarios, or needs distributions chosen/fitted. Also use during intake to reason about variability. Grounded in the industrial-statistics course canon (quality tools, probability, control-chart thinking) and simulation output analysis.
---

# stats-analyst

Turn numbers into decisions a non-statistician can act on. Every statistical claim gets
a plain-English sentence next to it; never output a test statistic without saying what
it means for the user's decision. This skill owns the *math of evidence*; domain meaning
for inventory/supply-chain results lives in `supply-chain-analyst`.

## The plain-English mandate (always on)

- Pair every technical statement with "In plain terms: …".
- Define a term the first time it appears ("95 % CI — the range the true average would
  fall in 95 times out of 100 if we repeated the whole experiment").
- Lead with the verdict, then the evidence: "Scenario B is genuinely better (…), here's
  how we know (…)."
- Numbers get units and context: "wait fell by 12 min (from 41 to 29, about a third)".

## 1. Describing data (before any model)

- **Skewed data → median + IQR**, not mean ± sd; say so when you switch. Service times,
  lead times, and lengths-of-stay are almost always right-skewed.
- Always look at the shape first: histogram or box plot beats any single number.
  Pareto chart when the question is "which few causes dominate?" (the vital few).
- Report spread, not just centre — in operations, **variability is usually the villain**:
  two systems with the same average can behave completely differently.

## 2. Choosing/fitting distributions (input modeling)

Where each classic distribution arises — recommend from mechanism, confirm from data:

| Mechanism | Distribution |
|---|---|
| Independent random arrivals per unit time | Poisson counts / exponential inter-arrivals |
| Arrival rate that varies by hour/day/season | Non-homogeneous Poisson (rate schedule) |
| Success/fail out of n tries (defects, no-shows) | Binomial |
| Sums or averages of many small effects | Normal (Central Limit Theorem) |
| Positive, right-skewed durations (service, repair, LOS) | Lognormal (or Gamma/Weibull) |
| Count data more variable than Poisson allows (real demand) | Negative Binomial |
| Only min/mode/max known from an expert | Triangular (declared as an assumption) |

Rules: **fit properly, never eyeball** — scipy.stats / fitdistrplus, then a
goodness-of-fit test (KS or Anderson–Darling) and state it. Separate *given* parameters
from *fitted* ones. A distribution that fails GOF but is mechanistically right beats a
better-fitting but meaningless one — say the trade-off out loud.

## 3. Interpreting uploaded RESULTS (the core procedure)

When the user brings experiment outputs (CSV, table, screenshot numbers), run this
checklist **in order** — do not skip to conclusions:

1. **Provenance:** how many replications is each number based on? A single run is an
   anecdote, not evidence — if N = 1, say exactly that and stop short of verdicts.
2. **Integrity:** N samples per statistic, min ≠ max (identical values across runs =
   a parameter isn't actually varying — a known trap), values in plausible ranges.
3. **Uncertainty:** mean ± t-based 95 % CI per KPI (t ≈ 2.045 at N = 30). Plain terms:
   "the true average sits in this band."
4. **Comparison:** two-sample t on the difference (Welch if spreads differ);
   |t| > ~2 at df ≈ 2(N−1) → real difference. Plain terms: "too large to be luck."
5. **Near-threshold humility:** a result that *just* crosses the line (t ≈ 2.0–2.2) is
   fragile — recommend replicating the whole experiment before believing it. Sign
   flips across replications prove noise. **Single-experiment significance at the
   threshold is not a finding.**
6. **Significance ≠ importance:** a real 0.4 % improvement may not matter; an
   uncertain 20 % one may deserve more replications. Say which case applies.
7. **Variance decomposition when a total is "not significant":** compare sd of the
   components. If one component's noise dwarfs the signal of another, report them
   separately — a real labour saving can hide inside a noisy total cost.
8. **CI of a mean ≠ prediction interval:** a tight band around the *average* year does
   NOT mean next year will land in that band. Flag this whenever forecasting.

## 4. Variation thinking (from the industrial-statistics canon)

- **Common cause vs special cause.** Random scatter within the usual band is the
  process talking; a point far outside, or a drift/trend, is a signal. Reacting to
  common-cause noise ("tampering") makes a process WORSE — in simulation terms: don't
  re-tune a policy because one replication looked bad.
- Control-chart logic applies to monitoring any KPI stream (live dashboards, sim
  output over time): centre line = long-run mean, limits ≈ ±3 sd of the plotted
  statistic; investigate signals, leave noise alone.
- **Process capability:** being stable is not the same as being good — a process can
  be perfectly in control and still fail the requirement. Compare the voice of the
  process (its natural spread) to the voice of the customer (the spec/target) and say
  which conversation the user is actually having.

## 5. Output phrasing templates

- "Δ = X ± Y [units]. The interval excludes 0, so the effect is real (t = …). In plain
  terms: …"
- "The interval includes 0 — with this many runs we cannot tell the scenarios apart.
  That is a finding about the evidence, not proof of no effect."
- "This number comes from one run; treat it as an illustration. For a decision, run
  the N = 30 experiment."

## Grounding

Distilled from the user's honours course canon — *Industrial Statistics* (Christensen &
Huzurbazar: quality tools, probability, control charts, capability), the REA statistics
review (descriptive stats, probability, distributions) — plus standard simulation
output analysis. Public anchor for methods: NIST/SEMATECH e-Handbook (see SOURCES.md).
The source PDFs are private course material and are NOT in this repo (PRIVATE-MATERIALS.md).
