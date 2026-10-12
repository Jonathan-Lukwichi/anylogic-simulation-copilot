# 02-statistics-input-modeling

Distribution fitting + goodness-of-fit. NIST handbook, fitdistrplus, scipy.stats.

## Fitted vs empirical: decision rule

| Situation | Use | AnyLogic form |
|---|---|---|
| Enough data and a family passes KS/AD | Fitted parametric | e.g. `lognormal(mu, sigma, min)` (gotcha G3), `gamma(...)` |
| Categorical shares (class, route, sex) | Empirical | option-list parameter following an empirical distribution, or a Custom Distribution |
| Published bands (census age groups) | Empirical ranges | Custom Distribution → Ranges |
| No family fits, or the data are multimodal | Empirical | Custom Distribution → observed samples (continuous to interpolate; loaded from the database if large) |
| Timestamped history of arrivals, used to validate | Trace-driven replay | Source → *Arrivals defined by: Arrival table in Database* (count and attributes from columns) — card `../08-example-patterns/basicmodels/source-with-arrivals-from-database-table.md` |
| Several inputs that move together over time | Multivariate time series (VAR) fitted offline | arrays + a cyclic step event — card `../08-example-patterns/basicmodels/vector-autoregression.md` |
| A bounded version of a fitted family | Truncated form | `normal(min, max, shift, stretch)`, `exponential(min, max, shift, stretch)`, … — redraws until inside [min, max], and `stretch` is a scale, not a rate (gotcha G66) |
| Almost no data, only expert min / likely / max | Triangular | `triangular(min, max, mode)` — AnyLogic's documented order (it also accepts min, mode, max and finds the maximum itself). The expert's "likely" value is the **mode**; the mean is (min + mode + max)/3 — gotcha G55 |

**Argument orders differ from textbooks** — `normal(sigma, mean)`, `lognormal(mu, sigma, min)`,
`weibull` flipping between overloads: check every call against the verified table in
`../08-example-patterns/bigbookmodels/probability-distributions.md` (gotchas G3, G55, G66). Fitting
tools that export AnyLogic call syntax (e.g. Stat::Fit) avoid transcription errors (Big Book). Validate
against history with the trace and run what-ifs with the fitted form; keep both behind one switch so
every downstream block is shared.

**Always state the caveat when an empirical form is chosen:** it cannot produce values beyond the
observed range, so it understates extremes. Keep the fitted form when one passes. Card:
`../08-example-patterns/videos/custom-empirical-distribution-agent-attributes.md`.

**Randomness in experiments:** fixed seed for building and demos, independent replications for
estimates; the traps are gotchas G16–G17 and card `videos/rng-seed-control-and-custom-generator.md`.

See SOURCES.md for the exact links and download/fetch-live status.
