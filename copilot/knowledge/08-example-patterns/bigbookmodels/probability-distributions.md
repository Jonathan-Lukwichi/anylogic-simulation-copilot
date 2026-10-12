# Pattern card — Probability Distributions
- **Source:** AnyLogic example model "Probability Distributions" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** Method (input modelling for DES / ABM / SD)
- **Problem it solves:** See what a distribution call really produces before it goes into a model, and get every argument in the right slot.

## Structure
One `Main`, no process logic. It is an interactive explorer.
- **Catalogue.** On startup, `descriptors` (an `ArrayList` of a small Java class `Descriptor`) is filled with one entry per distribution overload. Each entry holds the signature text and, per argument, its name, type (`int`/`double`), default value and help text. A combo box lists the signatures.
- **Generic argument form.** Choosing a signature sets `dindex`. A group of label, edit box and help text is replicated `descriptors.get(dindex).paramnames.length` times, so the form grows and shrinks with the argument count. Each row's frame turns red through `LineColorCode = valids[index] ? null : red` when its text will not parse.
- **Sampling.** The Show button parses the strings (`Double.parseDouble` / `Integer.parseInt`), then calls a `switch(dindex)` dispatcher `distribution()` 100 000 times into a HistogramData (100 intervals, auto range). Min, max and mean are shown next to the histogram. The combo box re-runs the button through `buttonShowDistribution.action()`.
- **Your data.** Numbers pasted into a text field are pulled out with a regular expression into a second HistogramData and overlaid for comparison.

## Resources
n/a

## Key settings worth copying
Overloads beyond Big Book ch. 15 pp. 3–6, G3 (`lognormal`) and G55 (`triangular`). All checked against Help 8.9.10, *Probability distributions*:

| Call | Argument order | Watch for |
|---|---|---|
| `weibull(beta, alpha)` | scale, shape | `weibull(alpha, beta, min)` is shape, scale, min: the order **flips** between overloads |
| `gamma(alpha, beta[, min])` | shape, scale | truncated `gamma(min, max, alpha, shift, stretch)` uses alpha = 1 whenever alpha < 1 |
| `erlang(beta, m[, min])` | scale, integer shape | scale first |
| `logistic(beta, alpha)` | scale, location | scale first |
| `cauchy(lambda[, theta])`, `laplace(phi, theta)` | scale, centre | scale first |
| `beta(p, q[, min, max])` | two shapes, range | range defaults to 0–1 |
| `binomial(p[, n])` | probability, trials | `binomial(p)` is a single trial |
| `negativeBinomial(p, n)` | success probability, successes wanted | `n` is a double |
| `hypergeometric(ss, dn, ps)` | sample size, defects, population | all int |
| `pareto(alpha[, min])` | shape, lower bound | min defaults to **1**, not 0 |
| `rayleigh(sigma[, min])`, `chi2(nu[, min])` | scale or shape, lower bound | min defaults to 0 |
| `pert(min, max, mode)` | as `triangular` | smoother than triangular with the same three numbers |
| `geometric(p)`, `logarithmic(theta)`, `gumbel1(a, b)`, `gumbel2(a, b)` | — | Help gives no meaning for the Gumbel `a`, `b` |

- **Truncated forms** exist for beta, binomial, exponential, gamma, negativeBinomial, normal, poisson, triangular and weibull. The bounds come first, then the shape parameters, then `shift` and `stretch`. The exception is `triangular(min, max, left, mode, right)`. Samples outside the bounds are thrown away and redrawn (Help), so a window deep in a tail costs many draws.
- **Normal** is `normal(sigma, mean)`, sigma first (KNOWN-KB: Big Book ch. 15 pp. 4, 6). The truncated form is `normal(min, max, shift, stretch)`, where shift is the mean and stretch the standard deviation. See `bigbookmodels/statechart-for-life-phases.md` for where the book's own notation misleads.
- Each function also has an overload with a trailing `java.util.Random` argument.

## KPIs instrumented
Sample min, max and mean against the values you intended. Compare the overlay with your data.

## Pitfalls
- **Eyeballing is not fitting.** Use the overlay to understand the parameters, not to choose a distribution. The KB rule still applies: fit, then report KS/AD (`02-statistics-input-modeling/README.md`).
- **The paste parser is naive.** Its pattern is an optional minus sign, digits and an optional decimal part. So `1e-3` becomes two numbers, `.5` loses its point and `1,234` splits in two. Check `userhistdata.count()` against your row count.
- **Stateful explorer.** Samples come from the model's default generator with a random seed, so every click differs slightly.

## Reusable idea
- Describe the options as data (descriptor objects), draw the form with replicated controls sized by the chosen option, and dispatch with a `switch`. One screen then serves any choose-a-function-and-fill-its-arguments task.
- Habit: before a distribution enters a model, draw about 1e5 samples and check their mean and range.

## When the co-pilot should use this
- Before writing any distribution call outside the core set: look its argument order up in the table.
- A user reports implausible durations or quantities, e.g. Weibull lifetimes off by orders of magnitude.
- A user wants to see what a distribution's parameters do.
- Related: G3, G55; proposed gotchas on `normal()` and `weibull()` in `.ingest/proposals/m-bigbook-3.md`.
