# 02-statistics-input-modeling

Distribution fitting + goodness-of-fit. NIST handbook, fitdistrplus, scipy.stats.

## Fitted vs empirical: decision rule

| Situation | Use | AnyLogic form |
|---|---|---|
| Enough data and a family passes KS/AD | Fitted parametric | e.g. `lognormal(mu, sigma, min)` (gotcha G3), `gamma(...)` |
| Categorical shares (class, route, sex) | Empirical | option-list parameter following an empirical distribution, or a Custom Distribution |
| Published bands (census age groups) | Empirical ranges | Custom Distribution → Ranges |
| No family fits, or the data are multimodal | Empirical | Custom Distribution → observed samples (continuous to interpolate; loaded from the database if large) |
| Almost no data, only expert min / likely / max | Triangular | `triangular(min, mode, max)` |

**Always state the caveat when an empirical form is chosen:** it cannot produce values beyond the
observed range, so it understates extremes. Keep the fitted form when one passes. Card:
`../08-example-patterns/videos/custom-empirical-distribution-agent-attributes.md`.

**Randomness in experiments:** fixed seed for building and demos, independent replications for
estimates; the traps are gotchas G16–G17 and card `videos/rng-seed-control-and-custom-generator.md`.

See SOURCES.md for the exact links and download/fetch-live status.
