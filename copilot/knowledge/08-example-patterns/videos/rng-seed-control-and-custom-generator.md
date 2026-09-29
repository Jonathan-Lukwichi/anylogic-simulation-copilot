# Pattern card — Controlling the RNG: reproducible vs unique runs, custom generators, dedicated streams
- **Source:** AnyLogic video "How to run reproducible and unique experiments" (https://youtu.be/m96PLSEIALg) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Choose, and prove, whether a stochastic model repeats itself exactly (for debugging, demos and grading) or gives independent runs (for statistics), and replace the default generator when needed.

## Mechanism
One default generator feeds all AnyLogic randomness:
- distribution functions;
- the default draws inside library blocks (Source gaps, Delay times);
- random transitions and layouts;
- the engine's ordering of simultaneous events.

The experiment's **Randomness** section seeds it when the experiment starts and again before **every** run or replication:
- **Fixed seed** (Seed value) gives the same trajectory every time, including in an exported model, on another PC and on AnyLogic Cloud.
- **Random seed** makes AnyLogic build Java's no-arg `new Random()`, so every run differs.
- **Custom generator (subclass of Random)** takes an expression that returns your generator, e.g. `new MersenneTwister()`.

The video's fingerprint test:
1. Build Source → Queue → Delay → Sink.
2. In the Sink's **On enter**, put `traceln(time());`.
3. Stop the model at a short fixed time.
4. Run twice and compare the Console output in the model window's developer panel.

## Resources
n/a

## Key settings worth copying
- The default RNG is `java.util.Random`, a linear congruential generator with modulus 2^48, so its period is at most 2^48. That is fine for typical models. Consider a stronger generator for very long runs or huge numbers of draws, or when a reviewer asks.
- To use a custom RNG:
  1. Add the library jar to the model's **Dependencies**.
  2. Add its import.
  3. Select **Custom generator (subclass of Random)** and enter the constructor call.
  The class must extend `java.util.Random`.
- Dedicated streams: every distribution function has an overload that takes a trailing `Random`, e.g. `triangular(5, 10, 25, svcRng)`. G3 shows the lognormal one. The most complete overload always has it.
- `setDefaultRandomGenerator(Random r)` swaps the generator mid-run. The Randomness setting is re-applied before the next run, though.
- Simultaneous events: since 8.6 the experiment has no selection-mode setting and the engine runs them LIFO by default (release notes); an Engine API call to change it remains but is marked experimental. Never let results depend on that order (G60). *(Corrected 2026-09-29.)*

## KPIs instrumented
n/a. This is a verification and experiment-design technique.

## Pitfalls
- The custom-generator expression is re-evaluated before each run. A constant seed such as `new MyRandom(1234)` therefore makes every replication identical. The same happens with a `new Random(1234)` created in Main.
- A fixed seed does not protect randomness that bypasses the AnyLogic RNG or ordering that isn't deterministic. General Java causes:
  - `Math.random()`, or an unseeded `new Random()` in model code;
  - iterating a `HashMap` or `HashSet` of agents (the order follows identity hashes);
  - clock reads;
  - input files or databases that have changed;
  - clicking controls during the run;
  - your own threads.
- With one shared stream, a structural change (an extra server, new routing) shifts every later draw. Two scenarios run on the same fixed seed are therefore not compared under the same arrivals and service times.
- One fixed-seed run is one sample. Never report a KPI from it alone.
- AnyLogic Cloud returns the stored result for identical inputs. See `videos/cloud-decision-tool-for-stakeholders.md`.

## Reusable idea
*Beyond the video; standard simulation practice.* This is common random numbers (CRN), a way to reduce variance:
- Give each random process (arrivals, each service, routing) its own `Random` seeded from a model parameter, e.g. `new Random(repSeed * 100 + 1)`, and pass it to every draw.
- Sweep `repSeed` across replications but keep it equal across scenarios.
- Paired scenarios then see the same demand and service sequences, so their difference reflects the design change rather than noise.

## When the co-pilot should use this
- Phase 4, configuring the environment: use a fixed seed while building, verifying and demoing, and a random seed or per-replication seeds for any estimate.
- Questions like "my results change every run", "all my replications are identical" or "can I use a better RNG?".
- Scenario comparisons where small differences must be detected. Recommend dedicated streams.
