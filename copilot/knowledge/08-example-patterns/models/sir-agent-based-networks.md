# Pattern card — SIR Agent Based Networks
- **Source:** AnyLogic example model "SIR Agent Based Networks" (models), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (with a Monte Carlo experiment and an SD reference curve)
- **Problem it solves:** Show how the contact-network topology (distance-based, random, ring lattice, small world, scale-free) changes an epidemic that has the same per-person parameters, and compare it with the mass-action SD curve.

## Structure
- **`Person` statechart:**
  - The initial branch sends a person to Infectious with `randomTrue(FractionInitiallyInfected)`, otherwise to Susceptible.
  - Susceptible → Infectious on the message "Infection".
  - While Infectious, an internal Rate transition at `ContactRate * Infectivity` runs `send("Infection", RANDOM_CONNECTED)`.
  - Recovery at Rate `1 / AverageIllnessDuration`.
- **Main:**
  - The layout and network are set in *On startup* from two enum parameters, `TypeOfLayout` and `TypeOfNetwork`.
  - Count statistics `NSusceptible`, `NInfectious` and `NRecovered` use `agent.inState(...)`.
  - Output `maxPrevalence = NInfectiousDS.getYMax()`.
- **Monte Carlo:** 100 runs, random seed, fixed parameters. *After simulation run* calls `ABOutputHistogram2D.add(root.NInfectiousDS)`, a 2D histogram of all runs' infectious curves (as in `models/sir-agent-based-calibration.md`). *Initial experiment setup* calls `SDOutputDS.fillFrom(SDOutput)` and draws the result on top as a reference. `SDOutput` is a 101-point table function named as the SD model's infectious curve; that it was precomputed from the SD version is inferred from its name.

## Resources
n/a. Defaults: 500 people, contact rate 5/day, infectivity 0.05, illness 15 days (c·i·D = 3.75), 1 % initially infected, 10 links per agent, link distance 50, 5 % long links, M = 2.

## Key settings worth copying
- **Build order** (the startup code encodes it):
  1. If the layout is spring-mass and the network is distance-based, fall back to a random layout, because the two are incompatible.
  2. `setLayoutType(...)`, then `applyLayout()` unless the layout is spring-mass.
  3. Pick the network with a `switch`, then `applyNetwork()`.
  4. Only then `applyLayout()` for spring-mass.

  Why (Help 8.9.10): distance-based links need positions first; spring-mass positions need links first; and the two together are circular.
- **Setter semantics** (Help 8.9.10, *Agent API*):
  - `setNetworkRandom(k)`: an **average** of k links, not exactly k.
  - `setNetworkRingLattice(k)` and `setNetworkSmallWorld(k, p)`: **even** k.
  - In `setNetworkSmallWorld`, p is the probability that a link goes to a **neighbour**, so the model passes `1 - PercentOfLongLinks`.
  - `setNetworkAllInRange(r)` works in continuous space only.
  - `setNetworkScaleFree(m)`: Help describes m loosely (as M or M0, the starting hubs).
- **Contacts only along links.** `RANDOM_CONNECTED` does nothing for an agent with no connections (Help: "if any").

## KPIs instrumented
S/I/R counts over time, peak prevalence (Output), and the Monte Carlo distribution of the infectious curve against the SD curve.

## Pitfalls
- **Local saturation.** On clustered networks (lattice, low-rewiring small world), many contacts hit neighbours who are already infected or recovered. The epidemic is then slower and smaller than the SD curve with the same c·i·D. The gap is a network effect, not a bug.
- **Same parameters, different effective R.** Degree heterogeneity (scale-free hubs) changes the effective reproduction number. Compare topologies at equal mean degree and report the degree distribution alongside the results *(general network-epidemiology knowledge)*.
- **Noise from a fresh network every run.** Each replication builds a new random network, so topology noise mixes with epidemic noise. `applyNetwork(Random r)` (Help; release notes) lets you build the same structure in every replication when you want to separate the two sources.
- **Existing KB card errors.** `basicmodels/agent-network-and-layouts-demo.md` describes `setNetworkRandom(k)` as exactly k and p as a rewiring probability. Both are wrong per Help; see the proposals file.

## Reusable idea
Choose the topology from a parameter at startup, following the dependency order of layout and network. Keep per-contact parameters fixed across topologies, and overlay the mass-action SD trajectory on the ABM Monte Carlo fan chart. The difference between the two curves is the value the network structure adds.

## When the co-pilot should use this
- **Use cases:** word-of-mouth, contagion or rumour models where who-meets-whom matters; checking whether an SD (random-mixing) model is good enough; sensitivity to network type.
- **Related cards:** `basicmodels/agent-network-and-layouts-demo.md` (API gallery), `sdmodels/sir-model.md` (SD form), and `videos/abm-word-of-mouth-contact-targeting.md`.
