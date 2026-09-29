# AnyLogic gotchas & conventions (beginner traps)

Small, high-frequency mistakes that confuse beginners. Each entry: the symptom, the
cause, the fix, and the reason. Append new ones as they come up during builds.

## Quick lookup — find the entry by what you see

| You see… | Entry |
|---|---|
| "Java type names usually start with an uppercase letter" warning | G1 |
| Can't find *Model time units* | G2 |
| `lognormal(...)` won't compile or gives absurd values | G3 |
| "An agent was not able to leave the port …out" | G4, then G37 |
| Arrival volume floods or runs low with a time-varying rate | G5 |
| "The choice for agent N changed before the agent transmission" | G6 |
| Need to hold agents until something else releases them | G7 (Wait block) |
| Optimizer's best plan breaks a service target | G8, G11 |
| Optimization objective/requirement won't compile; Bound won't take `root.x` | G9 |
| Optimization runs but no iteration ever completes | G10 |
| Best value sits on a parameter's Min/Max | G12 |
| Every optimization iteration infeasible | G13 |
| Only 7 decision variables / stops at 500 iterations; Cloud optimization differs | G14 |
| Dispatching rule (slack, critical ratio) serves jobs in odd order | G15 |
| Every replication gives the same number | G16 |
| Fixed seed but runs differ | G17 |
| Time-measure plot holds only ~100 points | G18 |
| Execution log missing or empty | G19 |
| Main's function/distribution "cannot be resolved" inside an agent | G20 |
| Agent stuck in a statechart state after its process finished | G21 |
| "Environment must be defined" on `send()` | G22 |
| `agent.<field>` undefined after an Enter block | G23 |
| `deliver()` / `receive()` marked deprecated | G24 |
| Lift ride time wrong or zero | G25 |
| Everything changed size after drawing a railway track | G26 |
| Cars drive through pedestrians | G27 |
| Train won't reverse; second train appears; "car … must fully be on one track" | G28, G29 |
| Queue animation backwards or agents stacked on one point | G30 |
| 3D object vanished under a floor; scene dark after adding a light | G31, G32 |
| `setColor` on a 3D object does nothing | G33 |
| Scenario cut capacity but the drawing still shows it | G34 |
| Custom block gives every agent the same random time; can't open it at runtime | G35, G36 |
| Fewer agents downstream than the Source created, no error | G37 |
| Cloud re-run returns the identical result | G38 |
| Lever, file or KPI missing/greyed out in Cloud | G39 |
| Cloud animation plays but outputs stay empty | G40 |
| OEE performance always 100 %, or OEE tracks utilisation | G41 |
| PML Conveyor / RackSystem / RackStore / RackPick not in the palette | G7 (deprecated since 8.9.5 — use the Material Handling Library) |
| Conveyor stops filling behind a point after a Convey | G42 |
| Conveyor stopped but no MTBF/MTTR, `isFailed()` false | G43 |
| "Nearest" AGV is far away by route | G44 |
| Jib crane stuck or run errors after enabling Blocked zone | G45 |
| An agent's On startup finds Main's data empty; rows written at startup vanish | G46 |
| A results table or exported sheet grows with every run | G47 |
| A new input workbook (Cloud upload or edited file) changes nothing | G48 |
| Set-up that works on the desktop is missing in Cloud | G49 |
| Experiment-page slider never shows; *Link to* can't find Main's parameter | G50 |
| GIS agents in the wrong town or in the sea | G51 |
| Converted rail network: trains vanish at track ends or pass through each other | G52 |
| `item.inState(...)` in a population statistic won't compile (8.9+) | G53 |
| A picture, note, chart or button from an agent type is repeated on Main | G54 |
| A `triangular` delay runs far longer than its stated average | G55 |
| Slider moved mid-run, agents don't react or react late | G56 |
| Word of mouth slower after adding another population to Main | G57 |
| Word of mouth far too fast, or every contact converts | G58 |
| Cumulative adopters flat, or equal to current users | G59 |
| "Either brand" buyers all pick the same brand | G60 |
| A rate or timeout acts per second although the model runs in days | G2 (note on units) |

---

## G1 — Naming: type names vs variable/parameter names

**Symptom:** A ⚠️ warning tooltip appears on a `Name:` field:
*"By convention, Java type names usually start with an uppercase letter."*

**Cause:** That warning only fires on a **type (agent class) Name field**. Seeing it
while trying to add an attribute means you typed the attribute name (e.g. `triage`) into
the **agent type's own Name field** — i.e. you renamed the *type*, instead of adding a
*Variable* inside it.

**Fix:**
- Keep the **type** name UpperCamelCase: `Patient`, `WardBed`, `PharmacyItem`, `Nurse`.
- Add the attribute as a **Variable** element (drag from the Agent palette onto the agent
  canvas), and name *that element* in lowerCamelCase: `triage`, `specialty`, `arrivalTime`.

**Naming convention (because AnyLogic generates Java):**

| Element | Maps to (Java) | Convention | Examples |
|---|---|---|---|
| Agent type | a class | UpperCamelCase | `Patient`, `Nurse`, `WardBed` |
| Variable / Parameter / Function / port / block | a field/method | lowerCamelCase | `triage`, `arrivalTime`, `lambda()`, `source`, `triageService` |

**Reason:** types become Java classes (uppercase by Java norm), members become fields
(lowercase). It's a *warning*, not an error — the model still runs — but following it keeps
generated code clean and examiner-readable, and prevents the "I renamed my whole agent type
by accident" confusion.

**Also avoid in any name:** spaces, leading digits, hyphens, and Java keywords
(`class`, `new`, `int`, `double`, `for`). Use `arrivalTime`, never `arrival time` or `2ndVisit`.

**How to tell which field you're in:** the bold title at the top of the Properties panel
names the currently selected element. If it shows the agent type (e.g. "Patient") and you
edit its Name box, you are renaming the *type*. A Variable's Name box only appears after you
select a Variable element you dropped on the canvas.

---

## G2 — "Model time units" is set on the MODEL ROOT (topmost item), not the agent or experiment

**Symptom:** Looking for the "Model time units" dropdown and not finding it on the `Main`
agent or on the `Simulation` experiment.

**Cause / correct location:** It lives on the **model itself** — the topmost item in the
Projects tree (e.g. `Hospital DigitalTwin`). Select it; the Properties title reads
"<ModelName> - Model" and shows the **Model time units** drop-down.

**Verified by AnyLogic Help (quote):** *"In the Project view located in the left sidebar,
select the model (the topmost item). In the model's Properties, select the required time
units from the Model time units drop-down list… we recommend that you select the model time
units when you create the model."*
Sources: https://anylogic.help/9/anylogic/running/model-time.html ,
https://help.anylogic.com/topic/com.anylogic.help/html/experiments/Setting%20Time%20Units.html

**Notes:**
- Default is `seconds`. Units available: ms, seconds, minutes, hours, days, weeks, months, years.
- Can be changed any time, but best set at creation.
- New timed elements (a transition's timeout or rate, an event's timing, a chart's update period)
  take the model time unit in force when they are created and keep it as an explicit unit;
  changing *Model time units* later appears not to convert them *(inferred from the editor, not
  tested)*. Set the unit first, and re-check every timeout, rate and recurrence after a change —
  a word-of-mouth rate drawn while the model is still in seconds stays "per second" unless you
  pick "per day" explicitly.
- Units longer than a week are non-constant: a "month" = 30 days, a "year" = 365 days in model time.
- For the Steve Biko digital twin set it to **hours** (data is hourly).

**Process rule for the co-pilot:** for AnyLogic UI locations, verify against anylogic.help
(or the user's screenshot) BEFORE asserting where a setting lives. Do not guess UI paths.

---

## G3 — `lognormal()` argument order: it is `lognormal(mu, sigma, min)`, NOT `lognormal(sigma, mu)`

**Symptom:** Service/LOS/lead-time draws are wildly wrong, or the expression won't compile.

**Verified signature (the ONLY overloads — no 2-arg version exists):**
```java
lognormal(double mu, double sigma, double min)
lognormal(double mu, double sigma, double min, Random r)
```
- `mu`  = mean of the **included normal** (1st arg)
- `sigma` = standard deviation of the included normal (2nd arg)
- `min` = minimum x value / lower shift — use **0** for a standard lognormal (3rd arg, REQUIRED)

Sources: https://anylogic.help/advanced/functions/lognormal.html ,
https://anylogic.help/api/com/anylogic/engine/UtilitiesRandom.html

**Conflict with the thesis spec:** `ANYLOGIC_SIMULATION_SPECIFICATION.md` Part 17 states
`lognormal(sigma, mu)` and writes 2-arg calls like `lognormal(0.615, 2.079)`. That is
**reversed and missing `min`**. The spec's *numeric values* (mu, sigma) are correct; only the
call form is wrong.

**Correction rule:** a spec call `lognormal(A, B)` (spec order = sigma, mu) becomes the
AnyLogic call **`lognormal(B, A, 0)`** (mu, sigma, min).

**Parameterisation from median m and 95th percentile p95:**
`mu = ln(m)`, `sigma = (ln(p95) - ln(m)) / 1.6449`, `min = 0`.

**Verified corrected calls (ED service + LOS + lead time):**

| Use | median, p95 | AnyLogic call |
|---|---|---|
| Triage | 8, 22 min | `lognormal(2.079, 0.615, 0)` |
| P1 consultation | 45, 120 min | `lognormal(3.807, 0.596, 0)` |
| P2 consultation | 25, 70 min | `lognormal(3.219, 0.626, 0)` |
| P3 consultation | 15, 45 min | `lognormal(2.708, 0.668, 0)` |
| Medicine LOS | 5, 18 d | `lognormal(1.609, 0.779, 0)` |
| Bed cleaning | 90, 240 min | `lognormal(4.500, 0.597, 0)` |
| Routine lead time | 21, 90 d | `lognormal(3.045, 0.886, 0)` |

**Units:** `lognormal(...)` returns a plain number. Interpret it via the field's unit selector
(set the Service "Delay time" unit to minutes/days) OR convert explicitly by multiplying by a
time-unit function, e.g. `lognormal(2.079,0.615,0) * minute()`, which is robust regardless of the
model's base unit. (Verify the field's unit selector before relying on it.)

**Action:** recommend the user fix the lognormal calls in the thesis spec so the examiner sees
the correct AnyLogic form.

---

## G4 — "An agent was not able to leave the port …out" → usually a **Moving** resource with no network

**Symptom (runtime, not compile):**
```
Model logic error: root.<source>: An agent was not able to leave the port
root.<source>.out at time … Consider increasing capacities and/or throughputs of the
subsequent object(s) or using PULL protocol
```
Often fires within the first simulated minute (the first patient), which rules out genuine
congestion.

**VERIFIED cause (Steve Biko build, 2026-06-23):** the real culprit was **`Forced pushing`
CHECKED on the `Source` block** (Advanced section). With it on, a rate Source shoves each agent
out the instant it's created; if the next block isn't ready that same instant → crash. The fix
was **unchecking Forced pushing** on the Source. Switching resources Moving→Static did NOT fix
it — the crash persisted until Forced pushing was off. So **check Forced pushing FIRST.**

**Other possible cause (not confirmed here):** a downstream `Service` seizing from a **Moving**
`ResourcePool` with no network/home-location can deadlock the seize (resource can't path to the
agent), filling the queue. This is plausible but was NOT the cause in this build.

**Fix priority:**
1. **Uncheck `Forced pushing`** on the Source (the verified fix) — **and** set the property that
   then appears, *Agents which can't exit*, to **wait in this block**. Its default is *are destroyed*
   (8.9.9 Help: `discardHangingEntities` = true), so unticking push alone silently throws away
   every arrival the next block can't take — see **G37**. Check conservation afterwards.
2. Confirm downstream Queue capacity > 0 and the connector lands on the input port.
3. Only if using **Moving** resources: ensure a network + home locations + Service "Agent
   location" are set.

**Static vs Moving:** for **logic-only** building, use **Static** (seized in place, no spatial
setup, fewer bugs). For **animation with moving people** (Steve Biko Phase 8), use **Moving**
with a proper network — added as a separate layer ON TOP of the validated logic flowchart, with
no rewrite of the process logic. Build logic first (Static), animate later (Moving). Moving
resources are NOT inherently buggy; they just need spatial markup.

---

## G5 — Time-varying Source arrival rate: `set_rate()` can flood; the rate-field expression under-samples

**Context:** a non-homogeneous (time-varying) Poisson arrival rate `lambda(t)` driving a
`Source` (e.g. the Steve Biko dry-run NHPP, spec Part 19.1).

**Symptom A — runaway flood (hits the PLE 50,000-agent cap in a few sim-hours):** observed when
the `Source` had **both** a time-varying expression `lambda(time())` in its Arrival-rate field
**and** a cyclic Event calling `arrival.set_rate(lambda(time()))` every hour. The model created
~50,000 agents in ~7 sim-hours while emitting only ~150 (rest buffered), then terminated. Model
time unit was correctly `hours`, so it was not a units issue — the `set_rate` path itself was
pathological in combination with the field expression.
- **Fix:** drive the time-varying rate with the **Arrival-rate field expression alone**
  (`lambda(time())`), and **delete the `set_rate` event.** A rate-based Source re-evaluates its
  rate expression each time it schedules an arrival, so the rate follows `lambda(t)` natively.
  This produced a clean, conservation-correct run.

**Symptom B — under-counting:** the field-expression method **under-samples** a rising rate
(it samples the rate at the start of each (long) inter-arrival gap and holds it). For the Steve
Biko dry-run, `lambda` averages ~3.26/hr (theoretical ~76/day) but the field method realised
only ~35/day — roughly half. Flow logic is unaffected; only arrival *volume* is biased low.
- **Accurate fix (when volume must match, e.g. spec Part 19.5's 65–75/day invariant):** use
  **"Arrivals defined by: Rate schedule"** with a `Schedule` object (proper NHPP), not the
  field expression. Defer this until validation; it is moot once real hourly data replaces
  `lambda` (Steve Biko Phase 7).

**Rule:** for a quick dry-run, field expression alone is fine (logic-correct, volume-low). For
publication-grade arrival volume, use a Rate Schedule. Never pair a field expression with a
`set_rate` event — that is what floods.

---

## G6 — `SelectOutput`/`SelectOutput5` "the choice for agent N changed before the agent transmission: it was X, but became Y"

**Symptom (runtime):**
```
root.<selectOutput>: The choice for agent N changed before the agent transmission:
it was 1, but became 5.
```

**Cause:** a `SelectOutput`/`SelectOutput5` evaluates its routing conditions **twice** — once when
the agent finishes the *preceding* block (a preview), and again at the actual exit. If the chosen
port differs, it errors. This happens when the value the conditions depend on is **set in the
SelectOutput's own `On enter` action** (which fires *between* the two evaluations) or when a
condition uses a stochastic call (`uniform()`, `randomTrue()`).

**Steve Biko instance (2026-06-23):** `disposition` set `agent.dispo = drawDisposition(...)` in its
**On enter**; the conditions `agent.dispo == 0..3` read the default `0` on the first eval (→ port 1)
and the freshly-drawn value on the second (→ out5) → "was 1, became 5".

**CORRECT fix — set the routing variable UPSTREAM (verified 2026-06-24):** compute the routing value
*before* the agent reaches the SelectOutput — at the earliest block where its inputs are known. For
Steve Biko, `dispo = drawDisposition(specialty, triage)` only needs `specialty` + `triage` (both set
at arrival), so it goes in the **`arrival` Source's On exit**, and `disposition`'s On enter is left
empty. Then both evaluations read the same fixed value → no error AND correct routing.

**Why the volatile checkbox ALONE is NOT enough here (important):** ticking
**`Choice is stochastic or volatile`** (SelectOutput5) suppresses the *error*, but AnyLogic then
commits the route at the **preview** evaluation — which happens **before** the On-enter action runs.
If the routing variable is set in On enter, at preview it is still its **default (0)**, so **every
agent routes out port 1** (the `== 0` branch). Observed exactly: after ticking the box, 273/273
patients went to `dischargeSink` and 0 everywhere else. The checkbox traded a crash for silently-wrong
routing.

**Rule:** set the routing variable in an **upstream** block's action, never in the SelectOutput's own
On enter. Use the volatile flag only when a condition is *genuinely* stochastic/volatile by design
(e.g. `randomTrue()` directly in the condition) — not as a fix for an On-enter timing bug.

---

## G7 — The PML **does** have a `Wait` block — use it for "hold until signalled" (corrected 2026-09-28)

**Correction:** an earlier version of this entry, based on a look at the 8.9 palette during the ED
build, said AnyLogic 8.x has no Wait block. That was wrong. The Help installed with the maintainer's
AnyLogic 8.9.9 PLE documents it (`library-reference-guides/process-modeling-library/wait.html`, see
the offline-Help note in `knowledge/INDEX.md`), and eight cards in this KB use it (e.g.
`08-example-patterns/basicmodels/anykitchen.md`, `models/distribution-center.md`,
`basicmodels/agent-moves-between-spaces.md`). The palette list in the old entry was not a complete
inventory either (it missed e.g. Resource Attach / Resource Detach). Why Wait was not spotted in the
palette is unknown; look again before concluding a block is absent.

**The opposite trap — blocks that really did leave the palette:** the PML **Conveyor** and the PML
**RackSystem / RackStore / RackPick** blocks are deprecated and were removed from the Process
Modeling Library palette in **8.9.5** (Help 8.9.9, "Deprecated blocks"); they may disappear
entirely later. Use the Material Handling Library instead: `Convey` / `ConveyorEnter` /
`ConveyorExit` on conveyor markup, and Storage / Storage System markup with `Store` / `Retrieve`.
Older example models and cards may still show the deprecated blocks.

**What Wait does (8.9.9 Help, in brief):** it stores agents with no internal ordering, and an agent
leaves only when code releases it — `waitBlock.free(agent)` for one, `waitBlock.freeAll()` for all.
Capacity defaults to 100 (or tick Maximum capacity). Two optional extras, both off by default:
*Enable exit on timeout* (agents that wait too long leave through the extra `outTimeout` port) and
*Enable preemption* (agents are kept in priority order and a displaced agent leaves through
`outPreempted`).

**Pick the hold construct by what releases the agent:**

| Need | Construct |
|---|---|
| Hold for a known or sampled duration | `Delay` |
| Hold until another process or event says so; release chosen agents | `Wait` + `free(agent)` / `freeAll()` |
| Same need, older idiom (still valid) | `Delay` with Type = "Until stopDelay() is called" + `stopDelay(agent)` / `stopDelayForAll()` |
| Close or open the connection for everyone at once | `Hold` (a gate, not a per-agent release) |
| Ordered line in front of a resource | `Queue` |

**Why:** "wait until signalled" is one of the most common hybrid idioms — a patient waiting for a
ward bed, a customer held while their order runs through a kitchen flowchart, walkers waiting for a
train. Telling a user that a documented block does not exist sends them into workarounds and makes
the KB contradict itself.

---

# Part 2 — Traps distilled from AnyLogic videos + the 8.9.9 Help (added 2026-09-28)

Short entries: symptom → cause → fix → why. "Help 8.9.9" = the offline Help installed with the PLE
(location in `knowledge/INDEX.md`). "Card" = `knowledge/08-example-patterns/videos/<name>.md`, which
holds the full mechanism. Items marked *(unverified)* were not confirmed on a build or in the Help.

## Optimization experiments

## G8 — An outcome target entered as a **Constraint** instead of a **Requirement**
**Symptom:** the optimizer's best plan breaks a service target the user believed was enforced
(customers lost, SLA missed).
**Cause:** Constraints are tested *before* each run and may involve only the optimization
parameters — they prune the search. Requirements are tested *after* each run on model outputs
(against the mean over replications when replications are on); a candidate that fails is marked
infeasible (Help 8.9.9, Optimization experiment). Intake notes tend to call both "constraints".
**Fix:** limits on the levers themselves → Constraints (`morningStaff + lunchStaff <= 20`). Promises
about results → Requirements (`root.lostCustomers <= 0`, `root.meanWait() <= 10`). With
replications, also report the worst replication or the share of replications that fail.
**Why:** this single mapping decides whether the optimizer solves the problem the stakeholder
actually posed. Cards: `forecast-driven-staffing-optimization`, `sim-opt-dual-formulations-and-bounds`.

## G9 — Optimization expressions: the `root.` rules
**Symptom:** the objective or a requirement will not compile ("cannot be resolved"), or a
requirement's Bound cell will not accept a model value such as `root.slTarget`.
**Cause:** objective, requirement and constraint expressions are compiled inside the *experiment*,
where the top-level agent is reachable only as `root`. The Bound cell takes a literal, and
Constraints are evaluated before any run exists, so neither can read model state.
**Fix:** prefix model members with `root.` (`root.throughput()`, `root.queue.mean()`). To keep a
target as a model parameter, fold it into the expression: `root.serviceLevel() - root.slTarget`,
type `>=`, Bound `0`. Keep literal constraint coefficients (e.g. unit costs) annotated with their
source and re-check them whenever the model's cost parameters change.
**Why:** the same scoping is why only top-level parameters can be decision variables (and why agent
code needs `main.`, see G20).

## G10 — The optimization never completes its first iteration
**Symptom:** model time advances but no iteration ever appears on the optimization chart.
**Cause:** Stop = *Never* and nothing calls `finishSimulation()`; the objective is evaluated only
when a run ends. (Also: the Genetic engine does not accept an infinite number of iterations —
Help 8.9.9.)
**Fix:** set a finite stop time/date or a model-side stop condition; set a Number of iterations.
**Why:** every iteration is one complete run (times the replications). Card:
`optimization-requirement-on-time-averaged-kpi`.

## G11 — The "best" plan is a lucky one and fails when re-simulated
**Symptom:** the reported optimum is cheaper than expected, sits just above a requirement bound, and
often misses it when run again.
**Cause:** each candidate was scored on a single run, so the search picks the luckiest of many noisy
estimates — an optimistic bias that is largest exactly where a requirement binds. In the source
webinar a single-run search chose a plan costing 225; a 50-replication search chose one costing 235
because the cheaper plan did not reliably meet the service target.
**Fix:** turn replications on with distinct seeds (fixed count sized from a pilot, or OptQuest's
varying count with a confidence level); re-run the top 3–5 plans with many more replications before
recommending one; add a margin to a bound that must hold nearly always. Report "best found" with a CI.
**Why:** the maximum of noisy estimates is biased upward. Card:
`sim-opt-lucky-optimum-and-shortlist-reverification`.

## G12 — A decision parameter's best value equals its Min or Max
**Cause:** the window is too narrow or the step too coarse; the engine never proposes values outside
the bounds, so an edge optimum is an artefact of the bounds.
**Fix:** widen or shift the window (keeping the old edge inside) and re-run; then refine
coarse-to-fine. Card: `sim-opt-search-space-reduction`.

## G13 — Every iteration is infeasible
**Cause:** a requirement cannot be met inside the constraints and ranges — or the bound is on the
wrong scale (0.9 vs 90).
**Fix:** untick the requirement, run the dual formulation (maximise that KPI under the constraint) to
learn what is attainable, then set a reachable bound or relax the constraint/ranges.
Card: `sim-opt-dual-formulations-and-bounds`.

## G14 — Engine limits: OptQuest caps, Genetic trade-offs, Cloud = Genetic only
**Symptom:** only 7 parameters can be optimized, or the search stops at 500 iterations.
**Cause:** AnyLogic's 8.8.4 release notes state that the bundled OptQuest is capped at 7 decision
variables and 500 iterations (lifting the caps, or exporting an OptQuest optimization as a
standalone app, is a paid option). The 8.9.9 Help's *Limitations in AnyLogic PLE* page (Editions) lists the
same caps for the Personal Learning Edition: 500 iterations and 7 decision variables per experiment.
**Fix:** set *Optimization engine* = **Genetic** (8.8.4+: no such cap, free export, but a fixed
replication count only and a finite iteration count), shrink the problem (decompose, Pareto-aggregate
levers), or buy the add-on. AnyLogic Cloud optimization runs the Genetic engine only; per the Cloud
Help, without a subscription a Cloud optimization stops after 5 minutes, and its best run may not
reproduce exactly.
**Why:** "optimize ~100 levers" advice assumes an uncapped engine. Card: `optimizer-engine-and-venue-choice`.

## G15 — Least-slack / critical-ratio dispatching in a priority `Queue` serves jobs in the wrong order
**Cause:** a `Queue` places an agent when it enters and does not re-rank the agents already waiting
(no re-sort call was found — *unverified*). Slack computed at different entry times uses different
clocks, and critical ratios genuinely change while jobs wait.
**Fix:** least slack → rank by the static key `-(dueDate - remainingWork)` (the `time()` term is common
to all waiting jobs and cancels). Critical ratio → decide at dispatch time: hold waiting jobs in a
`Wait` block (G7) and, when a machine frees, `free()` the job with the lowest current ratio.
Compute `remainingWork` from nominal, not sampled, times.
**Why:** static and dynamic priorities need different mechanics. Card: `dispatching-rule-as-optimizable-policy`.

## Randomness and replications

## G16 — Every replication returns the same value (zero spread)
**Cause:** AnyLogic re-initialises its default generator from the experiment's Randomness settings
before **every** run (Big Book ch. 15). So a *custom generator* built with a constant seed
(`new MyRandom(1234)`), or model code drawing from its own `new Random(1234)`, restarts identically
each run — as does a model with no randomness at all.
**Fix:** for unique runs use Random seed or the generator's no-argument constructor; for replications
that are both reproducible and distinct, seed each stream from a parameter swept per replication
(`new Random(repSeed * 100 + k)`). Test with a 3-replication run before trusting any CI.
**Why:** identical replications give a zero-width confidence interval that means nothing. Card:
`rng-seed-control-and-custom-generator`.

## G17 — Fixed seed, yet two runs still differ
**Cause:** something draws randomness or ordering from outside AnyLogic's stream: `Math.random()` or
an unseeded `new Random()`; iterating a `HashMap`/`HashSet` of agents (order follows identity
hashes); reading the wall clock; input files or tables that changed; clicking controls mid-run;
custom threads.
**Fix:** route every draw through AnyLogic's distribution functions (or a seeded `Random` passed as
their last argument), iterate ordered collections (`ArrayList`, `LinkedHashMap`), freeze inputs, and
don't interact mid-run. Fingerprint test: `traceln(time())` in the Sink's On enter, compare two runs.
**Why:** the seed controls only AnyLogic's own stream.

## Measurement and data export

## G18 — `TimeMeasureEnd` dataset (or a plot of it) holds only ~100 samples
**Cause:** *Dataset capacity* defaults to 100 (Help 8.9.9); older samples are dropped, so its mean
disagrees with the whole-run statistics.
**Fix:** read whole-run statistics from `tmEnd.distribution`; raise the capacity or use the execution
log when you need every sample. Card: `time-in-section-measurement-and-execution-log`.

## G19 — "Log model execution" is ticked but the log is missing or empty
**Cause:** execution logging works for the **Simulation experiment only** (Help 8.9.9); logs appear
only after the model is stopped; the element's *Log to database* box may be off, or that log type
switched off.
**Fix:** run a Simulation experiment, stop it, open Database → Log. For multi-run experiments collect
outputs through the experiment, or use *Export tables at the end of model execution*.

## G20 — Something defined on Main "cannot be resolved" inside an agent
**Symptom:** `ageDistribution()` works in the population's properties on Main but not in a default
value or action inside `Person`.
**Cause:** code inside an agent type compiles in that agent's own class; Main's members are not in scope.
**Fix:** call it through the reference to the top-level agent: `main.ageDistribution()`.
Card: `custom-empirical-distribution-agent-attributes`.

## Hybrid wiring and messages

## G21 — An agent is stuck forever in a state that waits for a message
**Cause (check in order):** (1) the statechart is not ticked under the receiving type's connections →
Communication → *Forward message to*; (2) the text does not match — *On particular message* compares
with `equals()`, so `"unloaded"` ≠ `"Unloaded"` and it still compiles; (3) timing — a message that
arrives while no matching transition is active is **discarded, not queued** (Help 8.9.9).
**Fix:** tick Forward message to; keep the message in one shared constant; hand the agent to the
process in the transition *into* the waiting state and notify it with `send()`, which is delivered in
a separate zero-time event.
**Why:** a lost message parks the agent silently and corrupts throughput and utilisation instead of
crashing. Card: `statechart-agent-through-hosted-flowchart`.

## G22 — "Environment must be defined" when Main's process calls `send()`
**Cause:** message functions must be called from agents that live in a space; the top-level agent is
not inside one (Help 8.9.9, Communication between agents).
**Fix:** host the process in an agent type that lives in Main's space, or notify the statechart
directly with `agent.statechart.fireEvent("msg")` *(inferred workaround)*.

## G23 — `agent.<field>` will not compile in blocks after an `Enter`
**Cause:** Enter's *Agent type* defaults to `Agent`, and the blocks downstream inherit that type, so
custom fields are invisible.
**Fix:** set Enter → Agent type to the visiting type (e.g. `Vehicle`); downstream blocks follow.

## G24 — `deliver()` / `receive()` are deprecated since AnyLogic 8.9.2
**Cause:** the engine Javadoc deprecates every `deliver*` variant and `receive()` in favour of `send*`.
**Fix:** switch to `send(msg, dest)` and re-test: `deliver` acted inside the current event, `send`
acts in a separate zero-time event, so logic that relied on the immediate hand-off can change.

## Space markup, levels and movement

## G25 — The lift works but floor-to-floor time is wrong (or near zero)
**Cause:** ride time comes from each landing's **Floor elevation** (a length), not from the level's
**Z** (pixels) (Help 8.9.9, Lift); editing one does not update the other.
**Fix:** derive both from one height *h*: level Z = −h × scale (px per m); landing Floor elevation = −h
(m). Set speed and pick-up/drop-off times on the **main landing**. Card: `multi-level-facility-lift-landings`.

## G26 — Accepting the Rail scale prompt changes the real size of markup already drawn
**Cause:** drawing the first Railway Track offers to switch the diagram Scale; markup geometry stays in
pixels, so every existing wall, path and conveyor now represents a different length.
**Fix:** settle the scale first — draw the track first and accept, or decline and keep the scale your
pedestrian/CAD geometry was built for; re-measure one known dimension after any scale change.
Card: `rail-shuttle-pedestrian-boarding`.

## G27 — Cars and pedestrians pass through each other
**Cause:** the Road Traffic, Pedestrian and Rail libraries do not perceive one another's agents; an
interaction exists only where the modeller codes it.
**Fix:** make each interaction explicit — a signal-gated crossing (pedestrian area toggled from the
Traffic Light's *On phase change* with `crossingArea.setOpen(...)`), or a ride (PedExit → Queue →
Pickup … Dropoff → PedEnter). Cards: `traffic-light-gated-pedestrian-crossing`, `rail-shuttle-pedestrian-boarding`.

## G28 — A train will not come back along the same track
**Cause:** `TrainMoveTo` only plans routes without a change of direction (Big Book ch. 9).
**Fix:** one TrainMoveTo per direction change; on the return leg set *Direction* = Backward.

## G29 — A one-train shuttle gets a second train, or fails with "The car being created must fully be on one track"
**Cause:** `TrainSource` keeps generating trains on its default schedule unless limited; and a train
created closer to the track start than its own length does not fit.
**Fix:** tick *Limited number of arrivals* with maximum 1 (or drive it by a single `inject()`), and
make the entry offset at least cars × car length.

## Animation and 3D

## G30 — Queue animation runs backwards, or a crowd collapses onto one spot
**Cause:** on a path, a queueing block draws its head at the path's **end point**, spaced by
length ÷ (capacity − 1) fixed at startup; a point node draws every agent on the same point (Help
8.9.9, Animating agents in flowcharts).
**Fix:** draw queue paths from the tail toward the server; size capacity to the drawn line; use a
rectangular node with the *Arranged* layout for buffers. Card: `flowchart-block-animation-binding`.

## G31 — A 3D object disappears after you add a floor rectangle
**Cause:** in 3D a Rectangle is a box whose Z-Height defaults to 10, so objects standing at Z = 0 end
up inside it; *Send to back* only affects 2D draw order.
**Fix:** flat ground → Z-Height 0; a slab of thickness t → Z = −t, Z-Height = t. Turn on the 3D
window's grid to see the Z = 0 plane. Card: `3d-scene-z-order-and-lighting`.

## G32 — The 3D scene goes dark or one-sided after adding a single Light
**Cause:** the scene's two default lights are dropped as soon as any Light element exists (Help 8.9.9).
**Fix:** add a complete set (e.g. ambient + directional) or none. Card: `3d-scene-z-order-and-lighting`.

## G33 — `setColor(...)` on a 3D object "does nothing"
**Cause:** the material-name string must match a name in the 3D object's *Colors* section exactly
(case-sensitive); the change shows only in the 3D view; or it recolours a material you did not intend.
**Fix:** copy the material name verbatim and check in a 3D window; for 2D, colour a 2D shape's fill.
Card: `per-agent-3d-material-color`.

## G34 — A scenario removes capacity but the animation still shows it
**Cause:** `set_capacity()` and other parameter changes alter the logic only; drawn shapes are static.
**Fix:** bind each station/dock shape's visibility or colour to the capacity parameter, or print the
active scenario's capacities on screen.
**Why:** stakeholders read the animation literally; a mismatch costs the model its credibility.
Card: `boundary-extension-bottleneck-migration`.

## Custom flowchart blocks

## G35 — Every agent through a custom block gets the *same* "random" time
**Cause:** a plain parameter is evaluated once, when the block instance is created. Library blocks
avoid this because their per-agent fields are re-evaluated for each agent.
**Fix:** make any custom-block parameter that feeds a per-agent field **Dynamic** — it is then
recomputed on every access and read as `loadingTime()` (Help 8.9.9, Dynamic parameters). Check the
parameters after *Create custom flowchart block*.
**Why:** silent — the model runs and animates normally, only the spread of results collapses.
Card: `custom-flowchart-block-from-repeated-chain`.
The same once-only draw applies to a plain parameter of any agent type: a distribution in its
default value is sampled once per agent, at creation. Used as a timeout (e.g. patience), every visit
of that agent then waits the same time — the wait becomes a personal trait. Type the distribution
into the Timeout field itself when each wait should be independent (a timeout is computed on every
state entry — Help 8.9.9, *Transition*).

## G36 — A custom block cannot be opened while the model runs
**Cause:** icon shapes react to the mouse only if they have an *On click* action.
**Fix:** put `return true;` in one icon shape's On click; also show `in.count()` / `out.count()` on
the icon so WIP inside is visible.

## Source, Cloud and KPIs

## G37 — Unticking Source *Forced pushing* silently destroys arrivals
**Symptom:** after the G4 fix the "not able to leave the port" error is gone, but fewer agents reach
the next blocks than the Source generated — no error, no warning.
**Cause:** with Forced pushing off, *Agents which can't exit* decides what happens to an agent the
next block refuses; its default is **are destroyed** (Help 8.9.9, `discardHangingEntities` = true).
**Fix:** set it to **wait in this block** (or put a Queue straight after the Source), then check
conservation once: `source.count()` = exits + agents still inside.
**Why:** otherwise arrivals are lost exactly when the system is congested, biasing load and waits
low. Models copied from AnyLogic demos are prone to this — at least one official webinar model sets
*are destroyed* on a Source feeding a conveyor. Card: `spiral-conveyor-per-point-z`.

## G38 — AnyLogic Cloud returns the identical result when a run is repeated
**Cause:** Cloud stores each experiment's inputs and results and recalls the stored result when the
same inputs are submitted again (AnyLogic exempts stochastic multi-run experiments); stored results
are kept per model version.
**Fix:** get variability from a replications or Monte Carlo experiment, not by re-clicking a single run.
Cards: `cloud-decision-tool-for-stakeholders`, `cloud-run-semantics-and-access`.

## G39 — A lever, input file or KPI is missing (or greyed out) in Cloud's Run Configuration
**Cause:** Cloud exposes only what the model's **Run Configuration** lists, and it accepts only:
- *Inputs:* static (non-dynamic) parameters of the chosen top-level agent, of type int, double,
  boolean, String, Date or a unit type; files the model uses that sit in the model folder and are
  referenced by a relative path. Flagged (invalid) items block the export.
- *Outputs:* Analysis elements (Output, datasets, statistics) placed on the top-level agent. Statistics
  inside a sub-agent are not offered, and an `Output` is calculated *On simulation end* by default.

**Fix:** lift each lever to a top-level static parameter of an allowed type and pass it down (encode
option lists as int or String); move input files into the model folder with relative paths; surface a
nested KPI through a top-level `Output` whose value reaches into the sub-agent
(`distributor.tmEnd.distribution.mean()`), pooling a population's samples into one top-level
statistics object rather than averaging per-node means; for a live value set *Calculated* = User
control and call `update_<name>()` from an event. Re-export.
**Why:** Cloud dashboards, Monte Carlo distributions and API results are all built from these scalar
outputs — a KPI they cannot see drops out of every experiment. Cards:
`cloud-decision-tool-for-stakeholders`, `cloud-run-semantics-and-access`.

## G40 — The Cloud animation plays fine but the Outputs pane stays empty
**Cause:** *Play* starts an animated run that produces no output values; outputs come only from the
headless experiment started with **Run** (Cloud Help, Running experiments).
**Fix:** press Run (or the run link in the Outputs pane); compare scenarios with a replicated
experiment type, never two single runs. Card: `cloud-run-semantics-and-access`.

## G41 — OEE shows 100 % performance in every scenario, or moves in lockstep with utilisation
**Cause:** the process time equals the nameplate (ideal) cycle time, so the model cannot run slow;
or `utilization()` was reported as OEE.
**Fix:** keep `idealCycleTime` as its own parameter; model speed loss explicitly (a process-time
distribution with mean above the ideal, or micro-stops); compute availability, performance and quality
from state-time accumulators and counts; sanity-check OEE = `goodCount * idealCycleTime / plannedTime`.
**Why:** a false loss split sends improvement effort to the wrong loss. Card: `oee-instrumentation-in-des`.

## Material Handling Library

## G42 — Items pile up behind a point on a conveyor after a `Convey` hands them to Batch, Queue, Service or Hold
**Cause:** by default an item that exits `Convey` **stays on the conveyor** at its target point and
keeps taking up belt space while it waits in the next block — with Batch/Combine it can sit there for
good as an invisible obstacle. (The label *Leave conveyor on exit* means "depart"; its Java name is
`removeFromConveyor`.)
**Fix:** when the item really leaves the line, tick **Leave conveyor on exit** on that `Convey` (or
follow it with `ConveyorExit`); to put an assembled or new item back, use `ConveyorEnter` at a
downstream position on the conveyor. Don't change the item's agent type at stations, turntables or
turn stations — the conveyor expects the same type afterwards (Help 8.9.9).
**Why:** only `Convey` moves items along a network; any other block that holds an item on the belt
freezes it in place. Card: `mhl-conveyor-station-processing-and-reassembly`.

## G43 — A stopped conveyor shows no MTBF/MTTR and `isFailed()` stays false
**Cause:** `conveyor.stop()` / `run()` is an operational halt, not a failure. Only `fail()` /
`repair()`, or a PML `Downtime` block attached in the markup's *Maintenance, failures, breaks*
section, put the equipment in a failed/maintenance state and feed its reliability statistics.
**Fix (8.9):** conveyors, stations and jib cranes accept a `Downtime` block directly; transfer tables,
turntables, turn stations, lifts and overhead cranes offer only `fail()` / `repair()`, driven and
timed by your own logic. For a conveyor, pick the Downtime priority on purpose (negative: waits until
the belt is empty; positive with preemption: stops at once; zero: drains, then goes down). Keep
`stop()` for e-stops and control logic.
**Why:** the older trick (a stand-in resource pool whose failure calls `stop()`) animates correctly
but leaves the equipment's own statistics blank. Card: `mhl-conveyor-control-sensors-and-breakdowns`.

## G44 — "Nearest" AGV dispatching sends a vehicle that is far away by route
**Cause:** *Nearest to agent* measures **straight-line** distance and ignores walls, one-way loops and
route length (Help 8.9.9).
**Fix:** on constrained networks use *Shortest path*; for business rules use *The most preferred*
(`transporterComparison(...)`) or *Transporter with top rating* (`transporterRating(...)`, larger
wins), after filtering with `transporterChoiceCondition(...)`.
**Why:** the dispatch policy is a hidden rule that shifts empty-travel time and therefore fleet-size
results. Card: `mhl-agv-dispatch-choice-and-cargo-position`.

## G45 — The jib crane never moves, or the run errors at start, once *Blocked zone* is enabled
**Cause:** the jib's initial angle lies inside the blocked sector, which makes movement impossible
(Help 8.9.9).
**Fix:** rotate the *Initial jib angle* out of the sector before enabling it (or move the sector with
`setBlockedZone(...)`); keep every pick-up and drop point inside the jib's reach and below the crane
height.
**Why:** crane feasibility is geometric — check reach, height and blocked sector before tuning
speeds. Card: `mhl-crane-reach-safe-height-movement-mode`.

## Model data, startup order and Cloud set-up

## G46 — Main's data is missing in the agents' On startup, or rows the agents write at startup vanish
**Cause:** On startup runs from the innermost agents up the tree; the top-level agent's On startup
runs **last**, after every agent in the model has been created and initialised (Help 8.9.9,
*Initialization order*). Anything Main's On startup builds — or deletes — happens after the agents'
own startup code.
**Fix:** give shared structures their value where they are declared (initial values are set while
the model is built, before any On startup), or run the per-agent step from Main's On startup as a
loop placed after the shared set-up. For a results table, purge and then write, both from Main.
**Why:** it fails either as a crash at time 0 or as a silently empty output file.
Card: `excel-round-trip-results-and-cloud`.

## G47 — A results table (or its exported sheet) holds several runs' rows
**Cause:** rows inserted into the model's built-in database during a run stay there after it ends.
**Fix:** make `deleteFrom(results).execute();` the first statement of Main's On startup and insert
after it (G46), or tag each row with a run id. Test: two runs in a row leave one run's rows.
**Why:** the duplication is invisible inside the model and inflates every total computed downstream.

## G48 — A replaced input workbook (Cloud upload or edited file) changes nothing
**Cause:** the model reads database tables copied from the workbook at import; they are refreshed
from the file at start only if *Autoupdate imported tables on model startup* is ticked, and a failed
refresh (renamed sheet or column, changed type) is reported only in the console while the run
continues on the old data (Help 8.9.9, *Importing database tables*).
**Fix:** tick Autoupdate; ship a template with fixed sheet names, column names and types; show what
each run read (row count, a key column's sum) as an `Output`; close the workbook in Excel before local
runs. **Why:** nobody sees the console in Cloud, so the stakeholder's plan silently isn't simulated.
Card: `excel-round-trip-results-and-cloud`.

## G49 — Set-up that works on the desktop is missing in AnyLogic Cloud
**Cause:** Cloud runs the model under its own experiment framework, so the experiment's
initialisation code (*Initial experiment setup*, *Before each experiment run*, …) does not run
there (Help 8.9.9, *Initialization order*), and desktop experiment pages are not uploaded.
**Fix:** move every set-up step into the top-level agent's On startup; expose each desktop override
as a Run Configuration input. Cards: `excel-round-trip-results-and-cloud`,
`experiment-page-pre-run-controls`.

## G50 — Controls on the experiment page never appear, or their *Link to* offers no Main parameter
**Cause:** new models skip the Simulation experiment screen by default (option *Skip experiment
screen and run the model*, release notes). A control's *Link to* lists only elements of its own
diagram, and Main does not exist before the run.
**Fix:** untick the option; bind the control through the experiment's Parameters section by typing
its getter (e.g. `slider.getIntValue()`) into the parameter's field. Use pre-run controls for inputs
read while the model is built (population size, layout id); live controls on Main only for runtime
policy levers. Card: `experiment-page-pre-run-controls`.

## G51 — GIS agents land in the wrong place (another town, a same-name street, the sea)
**Cause:** mapping a table column to *GIS location name* (likewise "first result of map search", a
block's place name, or `jumpTo("…")`) runs an online search at startup and takes the first hit,
searching first inside the map area visible at launch. The search server changed in 8.8.5 and search
was fixed again in 8.9.5 (release notes), so results also differ between versions and machines.
**Fix:** store coordinates and map *GIS location latitude / longitude* (decimal degrees, WGS 84);
geocode names once, offline. If names must stay, set custom search bounds to the study region and
stop at startup when an agent lands outside it. Card: `gis-agent-placement-from-table`.

## G52 — After converting a shapefile to rail markup, trains vanish at track ends or pass through each other
**Cause:** a track end without a switch is open, and a car leaving it leaves the rail model; tracks
that cross without a switch are not treated as crossings; before 8.9.8 converted ends joined only when
their coordinates matched exactly (8.9.8 joins ends less than 30 cm apart — release notes).
**Fix:** after conversion inspect the boundary and every junction: trim stubs, add missing switches,
check switch types, block real diamond crossings in code; compare track and switch counts with the
source map. **Why:** conversion delivers geometry, not an operating network.
Card: `gis-shapefile-to-rail-markup`.

## Agent-based models, statecharts and controls

## G53 — A population statistic written `item.inState(...)` will not compile in AnyLogic 8.9+
**Cause:** 8.9.0 renamed the local variable of population *Statistics* conditions and expressions
from `item` to `agent` (release notes). Material written for 8.8 and earlier — including *AnyLogic
in 3 Days* (6th ed., pp. 54, 55, 77) and older course handouts — still shows `item`.
**Fix:** write `agent.inState(Consumer.PotentialUser)` (no trailing semicolon in these fields); in
code, `count(consumers, c -> c.inState(Consumer.PotentialUser))` works in any version.

## G54 — Pictures, notes, charts or buttons drawn inside an agent type appear on Main, once per agent
**Cause:** a container draws every element of an embedded agent type whose *Visible on upper agent*
box is ticked, at the agent's position (Help 8.9.9, *Agent presentation*). In 8.9.9 the box starts
ticked for new images, text, shapes, groups, charts and controls, and unticked for statechart
elements, events, functions, variables and statistics (editor defaults).
**Fix:** untick *Visible on upper agent* on anything meant only for the agent's own view; keep the
agent's body at the axis origin; put model-wide notes on Main. **Why:** with 5,000 agents one pasted
note becomes 5,000 copies and slows the animation. Card: `agent-type-graphics-visible-on-upper-agent`.

## G55 — `triangular(...)`: the argument order forgives you, the "typical" value does not
**Cause (Help 8.9.9):** the documented form is `triangular(min, max, mode)`, but AnyLogic also
accepts `(min, mode, max)` and takes the larger of the last two as the maximum — so if a
parameterised maximum drops below the mode, the two swap roles silently. `triangular(min, max)` puts
the mode at the midpoint (symmetric). `triangularAV(avg, var)` is symmetric around `avg` with `var` a
fraction (0.15, not 15). The truncated form is `triangular(min, max, left, mode, right)`, where min
and max only truncate.
**The trap:** experts quote the most likely value, but the mean is (min + mode + max)/3. The market
tutorial's delivery time `triangular(1, 25, 2)`, described as "average 2 days", averages about 9.3
days; no triangular on [1, 25] can average 2.
**Fix:** write the documented order; when a source gives an *average*, set mode = 3·mean − min − max
if that lands inside the range, otherwise use a right-skewed family with that mean; document each
triangular with its mean. Face-check competing timeouts against their race probability.

## G56 — A slider moved mid-run changes nothing (or only much later) for agents already in a state
**Cause (Help 8.9.9, *Transition*, *Agent API*):** a Timeout is computed once, when the state is
entered; a Rate is re-read only when that agent's `onChange()` runs (the engine calls it when the
agent itself originates an event or receives a message); a Condition is tested only when something
changes in that agent. Changing a parameter on Main notifies no agent.
**Fix:** for Rate and Condition triggers add `for (Consumer c : consumers) c.onChange();` to the
control's action (or the parameter's On change); for Timeouts, say the change applies to new entrants,
or use a re-armable event. Agents waiting on a stock held by Main (`main.stockA >= 1`) likewise sleep
through a restock — let the owner of the stock allocate it and wake the buyer (G60 card). For analysis,
change inputs between runs. Card: `statechart-live-controls-trigger-reevaluation`.

## G57 — Word of mouth slows, with no error, after another agent type is added to Main
**Cause:** `sendToRandom()` / `sendToAll()` address the sender's whole **space** — every population
and single agent embedded in Main — not the sender's own population (Help 8.9.9, *Communication
between agents*). Adding retailers or trucks dilutes the contacts to c·N/(N+M).
**Fix:** `send("Buy", randomFrom(main.consumers))`. Don't switch to a filtered target (only potential
users) unless targeted referrals are intended — that drops the Bass saturation factor.
Card: `abm-word-of-mouth-contact-targeting`.

## G58 — Word of mouth is far too strong, or every contact converts
**Cause:** the contact rate is applied twice — the sender's transition already fires at rate c and
the receiver's guard multiplies by it again (`randomTrue(adoptionFraction * contactRate)`). And
`randomTrue(p)` with p ≥ 1 raises no error: it is simply always true.
**Fix:** put c in exactly one timer and the adoption fraction in exactly one decision (sender rate c
+ receiver guard `randomTrue(i)`, or sender rate c·i + unguarded receiver); assert probabilities
≤ 1. Card: `abm-wom-conversion-rate-vs-probability`.

## G59 — "Cumulative users" stalls, or grows on noise, once users can leave the state
**Cause:** it is built by differencing a level (today's count in the user state minus yesterday's,
clamped with `max(0, …)`). That difference is adoptions minus exits, and the clamp drops every day
exits win — it is right only while nobody ever leaves.
**Fix:** count at the event (`main.adoptions++` in the target state's Entry action), keep a per-agent
flag for distinct reach, and assert users = initial + adoptions − exits.
Card: `abm-adoption-flow-counters-vs-state-counts`.

## G60 — A buyer who would take either brand always buys the same one
**Cause:** two Condition transitions out of one state that are both true at once are simultaneous
events; the engine picks by its internal order (LIFO by default since 8.6, when the experiment's
selection-mode setting was removed — release notes), not by any modelled preference.
**Fix:** make the choice explicit in one place — route into a Branch with the rule on one exit and
Default on the other, or let the stock owner apply the rule. Never let results depend on event
order. Card: `abm-stock-gated-purchase-allocation-and-brand-tie`.
