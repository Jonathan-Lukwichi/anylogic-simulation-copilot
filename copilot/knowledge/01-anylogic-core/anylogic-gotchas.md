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
| Only 7 decision variables / stops at 500 iterations; Cloud optimization differs; standalone export now paid | G14 |
| Dispatching rule (slack, critical ratio) serves jobs in odd order | G15 |
| Every replication gives the same number | G16 |
| Fixed seed but runs differ | G17 |
| Time-measure plot holds only ~100 points | G18 |
| Execution log missing or empty | G19 |
| Main's function/distribution "cannot be resolved" inside an agent | G20 |
| Agent stuck in a statechart state after its process finished | G21 |
| "Environment must be defined" when Main calls `sendToAll` / `sendToRandom` | G22 |
| `agent.<field>` undefined after an Enter block | G23 |
| `deliver()` / `receive()` marked deprecated | G24 |
| Lift ride time wrong or zero | G25 |
| Everything changed size after drawing a railway track | G26 |
| Cars drive through pedestrians | G27 |
| Train won't reverse; second train appears; `car … must fully be on one track` | G28, G29 |
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
| A rate or timeout acts per second although the model runs in days | G2 (note on units), G61, G62 |
| `set_rate(x)` or another one-argument setter floods or barely changes anything | G61 |
| Delay or timeout off by 60×, 24× or 7×, often after changing the model time unit | G62 |
| A daily 08:00 event drifts an hour twice a year | G63 |
| Wrong month from `toDate` / `getMonth()`; monthly lookup a month late; `getHour()` after noon | G64 |
| Results differ on another PC, in a new experiment, or a month later | G65, then G17 |
| `normal`, `weibull` or a truncated distribution gives the wrong mean | G66 |
| `meanConfidence()` interval looks too tight with few replications | G67 |
| Logged delay or timeout values differ from what agents got | G68 |
| Calibration's "best" values change every run with the same error | G69 |
| An age- or overdue-dependent failure rate has no effect | G70 |
| Agent stuck in a state whose Timeout has a guard | G71 |
| "msg cannot be resolved" in a branch | G72 |
| An agent-type event never fires for agents created mid-run | G73 |
| A Condition event fires once, or `restart()` freezes the model | G74 |
| A resumed phase restarts its full duration | G75 |
| A message from an agent that then removes itself never arrives | G76 |
| Two jobs, one idle vehicle: one job never served | G77 |
| Port-to-port model with no visible message code | G78 |
| An SD lookup goes negative outside its table | G79 |
| SD results change with the solver step | G80 |
| An SD variable set by a slider or event snaps back | G81 |
| A "10 %" outflow sends far more than 10 % | G82 |
| An SD pulse keyed on `time()` is missed or mis-sized | G83 |
| A hybrid model slows as the population grows | G84 |
| A conditional Hold opens when it should close, or never reopens | G85 |
| A SelectOutput condition is ignored | G86 |
| The whole Delay empties at once | G87 |
| Agent count grows when requests are cancelled | G88 |
| An urgent task never interrupts a busy resource | G89 |
| Blocks connected by code keep the old routing | G90 |
| A database-fed Source gives a fixed A, B, C rotation | G91 |
| A schedule built in code gives no arrivals | G92 |
| Retrieving from a deep rack lane errors | G93 |
| Pre-loaded storage items missing from stock counts | G94 |
| A tugger train leaves with one item | G95 |
| AGVs pause and then drive through each other | G96 |
| Closing one FluidSplit branch stops both | G97 |
| Train methods won't compile after TrainDecouple | G98 |
| `The switch … cannot be seized: another car is over it` | G99 |
| `reserveFor(train)` errors, or trains cross unreserved | G100 |
| A saturated road network never gridlocks | G101 |
| Cars vanish or the run stops at a full parking lot | G102 |
| Cars stop at a newly drawn junction | G103 |
| GIS trucks drive across fields or water | G104 |
| Pedestrian gates too few although utilisation looks fine | G105 |
| Pedestrian `traffic()` noisy or low at the start | G106 |
| Escalator directions differ; a turned-off escalator is still used | G107 |
| People stuck in a failed lift; a repaired lift ignores calls | G108 |
| A wind or heading effect is lopsided | G109 |
| NullPointerException from `getNeighbors()` | G110 |
| Hand-made contacts vanish; newborns never connected | G111 |
| Hiding some copies of a replicated shape hides all | G112 |
| "Index out of bounds" from a replicated control at startup | G113 |
| A parameter's On change never runs; a slider is out of sync | G114 |
| "cannot be resolved" after renaming an element | G115 |
| An Excel value is silently 0; `getCellType()` code won't compile | G116 |
| Query / Insert / Update / Key-Value element missing from the palette | G117 |
| A custom experiment's results differ from the Simulation experiment | G118 |
| A Python-driven sweep mixes up iterations | G119 |
| RL configuration ignored, or spaces rejected | G120 |
| A trained RL policy acts nonsensically in the model | G121 |
| A constant or property name from the Help won't compile | G122 |

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
- Pick the unit that matches your data's native resolution — e.g. a model driven by hourly
  arrival data should set this to **hours**, not seconds or days.
- The SD solver — numerical method and *Fixed time step* — is a model-level setting too: model
  properties → *System Dynamics solver* (8.9.10; the Big Book's "experiment → Advanced" is outdated).
- Read the unit in code with `getEngine().getTimeUnit()`. "Every 1 month" in a years model is 30/365 =
  0.0822 years, not 1/12; calendar positions need the date functions (G63, G64), durations the
  multipliers — but never a multiplier and a unit drop-down together (G62).

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

**Units (corrected 2026-10-01):** `lognormal(...)` returns a plain number. In a field that has a unit
drop-down (Delay time, Timeout, …) type the plain draw and set the drop-down to the data's unit (minutes,
days). Do **not** also multiply by `minute()`: it already returns minutes in model time units, and the
drop-down converts again — right only while the drop-down equals the model time unit (G62). Multipliers
such as `lognormal(2.079, 0.615, 0) * minute()` belong in code that has no drop-down (actions, `hold(...)`,
`restart(...)`).

**Sibling trap:** `normal(sigma, mean)` takes the standard deviation first; G66 lists this and the other
distribution argument orders that differ from textbooks.

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

**Genuine congestion gives the same message** — but after hours of model time, not in the first
minute. An all-default chain Source → Queue → Delay → Sink runs at ρ = 1 (1 arrival per second against a
mean service of 1 s at capacity 1 — Help 8.9.10 defaults; Big Book ch. 15 p. 11), so the 100-place default
Queue eventually fills. Replace every default and write down ρ = λ·E[S]/c < 1 for each station.

**Static vs Moving:** for **logic-only** building, use **Static** (seized in place, no spatial
setup, fewer bugs). For **animation with moving people** (Steve Biko Phase 8), use **Moving**
with a proper network — added as a separate layer ON TOP of the validated logic flowchart, with
no rewrite of the process logic. Build logic first (Static), animate later (Moving). Moving
resources are NOT inherently buggy; they just need spatial markup.

---

## G5 — Time-varying Source arrivals: *Arrival rate* is read once, and one-argument `set_rate()` is per second

**Context:** a non-homogeneous (time-varying) Poisson arrival rate `lambda(t)` driving a `Source` (e.g. a
dry-run NHPP). **Corrected 2026-10-01** from the 8.9.10 engine and Help: the
earlier version of this entry explained both symptoms wrongly.

**Symptom A — runaway flood (the PLE 50,000-agent cap within a few model hours):** a cyclic Event called
`arrival.set_rate(lambda(time()))` every hour in a model whose time unit was hours; about 50,000 agents
appeared in about 7 model hours.
- **Cause (engine 8.9.10):** the one-argument `set_rate(x)` stores `x` in the block's internal unit, which
  for `Source` is **per second** (`getUnitsOf_rate()` = PER_SECOND), whatever the model time unit or the
  unit shown in the field. λ ≈ 2 "per hour" became 2 per second = 7,200 per hour, which matches the flood.
  Other blocks use other internal units — see G61.
- **Fix:** always pass the unit: `arrival.set_rate(lambda(time()), PER_HOUR)`.

**Symptom B — under-counting:** with `lambda(time())` typed into *Arrival rate* and no event, the run
realised about 35/day against a theoretical ~76/day.
- **Cause:** *Arrival rate* is a static property: its expression is evaluated when the block is created and
  changes only through `set_rate(...)` (engine: `rate` is a field with a setter; Help 8.9.10 *Source*
  describes it without per-agent evaluation, while *Interarrival time* is "evaluated for each agent"). The
  rate therefore stayed at λ(0) for the whole run.
- *Modify rate* / *Rate expression* (with `baseRate`) exist only for *Rate schedule* arrivals, to scale the
  schedule; with a plain rate they are hidden (Help 8.9.10 *Source*, *PedSource*).

**Fix — in order of fidelity:**
1. *Arrivals defined by: Rate schedule* with a Schedule — exact non-homogeneous arrivals.
2. *Interarrival time* = `exponential(lambda(time()))`, with the field's unit set to the unit λ is
   expressed in — re-read at every arrival, so the rate lags by at most one gap. Guard λ = 0: an
   interarrival that evaluates to infinity stops the Source for good (Help 8.9.10 *Source*), so write
   `lambda(time()) > 0 ? exponential(lambda(time())) : timeToReopen`.
3. A constant *Arrival rate* plus a cyclic Event calling `set_rate(lambda(time()), PER_HOUR)` —
   piecewise constant, fine when λ changes slowly relative to the event period. A rate of 0 pauses
   arrivals until it becomes positive again (Help 8.9.10 *Source*).

**Rule:** never type a time-dependent expression into *Arrival rate*; never call `set_rate` without a unit.
For publication-grade arrival volume, use the Rate schedule.

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

**Addendum (Help 8.9.10, *SelectOutput*, *SelectOutput5*):** the route is computed when the agent finishes
the preceding block, **before that block's On exit runs** — so a routing value set in the immediately
preceding block's On exit is still too late. Set it in that block's *On at exit* (which runs before the
routing decision, where the block has one), further upstream, or behind a zero-time Delay. In probability
mode the volatile box is ignored: the route is drawn once, but the probability expressions are evaluated
twice and a change between the two raises the error. A condition typed while the block is in probability
mode is ignored entirely (G86).

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
`sim-opt-lucky-optimum-and-shortlist-reverification`. A live instance: the Big Book's *Field Service Phase 6*
optimization (8.9.10) runs with replications off and a random seed, so the optimum the book reports (ch. 4
p. 47) is one run per plan. Small-n confidence intervals from `meanConfidence()` are too narrow (G67).

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
**Fix:** set *Optimization engine* = **Genetic** (8.8.4+: no such cap, but a fixed
replication count only and a finite iteration count), shrink the problem (decompose, Pareto-aggregate
levers), or buy the add-on. AnyLogic Cloud optimization runs the Genetic engine only; per the Cloud
Help, without a subscription a Cloud optimization stops after 5 minutes, and its best run may not
reproduce exactly. **8.9.10:** *Export Model to Standalone Application* is now an additional paid option for
every model (release notes), so the Genetic engine no longer means a free standalone export.
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
**Cause:** each run's randomness restarts from the same point. Typical sources: a *Custom generator*
expression with a constant seed (`new MyRandom(1234)`) — Help 8.9.10 (*Random number generator*) says the
default generator is set up again from the experiment's Randomness settings before each simulation run, so
that expression is evaluated anew every run; model code drawing from its own `new Random(1234)` created in
an agent (rebuilt with every new root); `Random`-typed parameters with constant seeds
(`sdmodels/network-effect`); or a model with no randomness at all. The built-in *Fixed seed* is different:
the same Help page says the generator is initialised once when the model is created and not re-initialised
between replications, so replications differ while the whole experiment repeats exactly. *(The Help words
this inconsistently across pages — corrected 2026-10-01 from "re-initialised before every run"; the
3-replication test below settles it on your build.)*
**Fix:** for unique runs use Random seed or the generator's no-argument constructor; for replications
that are both reproducible and distinct, seed each stream from a parameter swept per replication
(`new Random(repSeed * 100 + k)`). Test with a 3-replication run before trusting any CI: put
`traceln(getCurrentReplication() + " " + time())` at the first Sink entry and compare the three lines.
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
**More causes (Help 8.9.10, *Reproducible model runs*; 8.9.10 example models):**
- pedestrian and free-space transporter models compute in several threads — set the runtime preference
  *Number of processors for parallel execution* to 1 (exported applications: `parallelWorkersCount`) when a
  run must repeat exactly;
- `Collections.shuffle(list)` and other Java utilities called without a `Random` — pass
  `getDefaultRandomGenerator()` (the Help checklist misnames it `getDefaultRandomNumberGenerator()`, G122);
- static variables survive between runs in one model window — only a fresh window repeats exactly;
- a start date set to "today" in code, or any `new Date()` (G65);
- Python called through Pypeline drawing from an unseeded NumPy generator — seed it from AnyLogic first;
- another PC with other locale (DST) rules; `hashCode()` / `identityHashCode()`; strings compared with
  `==`; dynamic shape properties that change model state;
- in multi-run experiments: an optimization with parallel evaluations, and values pasted from *Copy best*,
  which applies `format()` and can round them.

## Measurement and data export

## G18 — `TimeMeasureEnd` dataset (or a plot of it) holds only ~100 samples
**Cause:** *Dataset capacity* defaults to 100 (Help 8.9.9); older samples are dropped, so its mean
disagrees with the whole-run statistics.
**Fix:** read whole-run statistics from `tmEnd.distribution`; raise the capacity or use the execution
log when you need every sample. Card: `time-in-section-measurement-and-execution-log`.
The cap is general: every Data Set keeps only its latest *Keep up to … samples* (Help 8.9.10, *Data set*),
and SD variables have their own automatic datasets (agent type → Advanced → *Create datasets for dynamic
variables*; 100 samples in the Big Book models). Size a dataset's tail as run length ÷ recurrence + 1
before exporting it or calibrating against it — `difference()` fits only the overlap (G69).

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
For an agent nested deeper (a `Product` inside a `Firm`), reach the top level with
`((Main) getRootAgent()).x` or walk up with `getOwner()` (Help 8.9.10, *Agent API*), or pass the reference
down as a parameter *(that `main` exists only for agents living in Main is inferred from the shipped
Product Portfolio Management model)*. Card: `custom-empirical-distribution-agent-attributes`.

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
**Precision (Help 8.9.10, *Statechart queue*):** `receiveMessage()` does not queue. Messages forwarded from
the agent and `fireEvent()` calls go into a queue that lives only for the current instant: a matching
message is consumed together with every older one still queued, and the rest is dropped when time
advances. For a finite command set use an Option List message type, so a typo will not compile; when the
receiver may not be waiting yet, latch the notice in a variable and trigger by Condition — a Condition
already true on entry fires at once. Card: `bigbook/statechart-message-queue-and-safe-handoff`.

## G22 — "Environment must be defined" when Main broadcasts a message
**Cause (corrected 2026-10-01):** the broadcast and random message functions — `sendToAll`,
`sendToRandom`, `sendToAllNeighbors`, `sendToRandomNeighbor`, `send(msg, ALL | RANDOM | …)` and their
`deliver` twins — pick recipients from the sender's space, and the top-level agent lives in none.
Point-to-point `send(msg, agent)` and `deliver(msg, agent)` look up no space and work from Main (engine
8.9.10: `send(Object, Agent)` checks only for a null recipient; three 8.9.10 example models — *Epidemic and
Clinic*, *User Satisfaction*, Big Book multimethod model S — call it from flowcharts on Main). Help 8.9.10
(*Communication between agents*) says *any* message function called from Main raises the error; that
sentence is broader than the engine.
**Fix:** from Main, address a specific agent (`send("Promotion", randomFrom(people))`) or broadcast with
Main's own `sendToAllAgentsInside(msg)` / `sendToRandomAgentInside(msg)` (the *User Satisfaction*
Promotion button). Inside agents that live in Main's space the broadcasts work, but reach the whole space
(G57).

## G23 — `agent.<field>` will not compile in blocks after an `Enter`
**Cause:** Enter's *Agent type* defaults to `Agent`, and the blocks downstream inherit that type, so
custom fields are invisible.
**Fix:** set Enter → Agent type to the visiting type (e.g. `Vehicle`); downstream blocks follow.

## G24 — `deliver()` / `receive()` are deprecated since AnyLogic 8.9.2
**Cause:** the engine Javadoc deprecates every `deliver*` variant and `receive()` in favour of `send*`.
**Fix:** switch to `send(msg, dest)` and re-test: `deliver` acted inside the current event, `send`
acts in a separate zero-time event, so logic that relied on the immediate hand-off can change.
For an immediate hand-off use `agent.statechart.receiveMessage(msg)`, which returns whether a transition
took the message. Copied demo code is the usual source of the warning: 8.9.10 examples still call
`receive()` (*Wildfire*, the Big Book three-method *Epidemic*). When seeding an outbreak with
`people.random()` ten times, draw distinct agents — a repeat pick wastes a seed. The switch to `send` opens
the check-then-send window of G77.

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
pedestrian/CAD geometry was built for; re-measure one known dimension after any scale change. The Road
Traffic Library prompts the same way: the first Road offers 4 px per metre (Help 8.9.10, *Road*), the first
Railway Track 2 px per metre.
Card: `rail-shuttle-pedestrian-boarding`.

## G27 — Cars and pedestrians pass through each other
**Cause:** the Road Traffic, Pedestrian and Rail libraries do not perceive one another's agents; an
interaction exists only where the modeller codes it.
**Fix:** make each interaction explicit — a signal-gated crossing (pedestrian area toggled from the
Traffic Light's *On phase change* with `crossingArea.setOpen(...)`), or a ride (PedExit → Queue →
Pickup … Dropoff → PedEnter). Cards: `traffic-light-gated-pedestrian-crossing`, `rail-shuttle-pedestrian-boarding`.

## G28 — A train will not come back along the same track
**Cause:** `TrainMoveTo` only plans routes without a change of direction (Big Book ch. 9; Help 8.9.10,
*TrainMoveTo*, says the same).
**Fix:** one TrainMoveTo per direction change; on the return leg set *Direction* = Backward.

## G29 — A one-train shuttle gets a second train, or fails with `The car being created must fully be on one track`
**Cause:** `TrainSource` keeps generating trains on its default schedule unless limited; and a train
created closer to the track start than its own length does not fit.
**Fix:** tick *Limited number of arrivals* with maximum 1 (or drive it by a single `inject()`), and
make the entry offset at least cars × car length.
**Note (Help 8.9.10, *TrainSource*):** *Offset from* defaults to **End of the track** and *Orientation* to
Forward, so the train extends back from the offset point; "offset ≥ cars × car length" holds for *Offset
from: Beginning*. In general the stretch behind the first car, within the track, must hold the whole train.
Whether 8.9.10 needs the whole train or only each car on one track is *(unverified)* — the same page says
an over-long train occupies the next track through the nearest switch.

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
Related: 2D draw order does not carry into 3D, so flat shapes at the same Z flicker — give stacked flat
shapes slightly different Z (0, 0.1, 0.2) (Big Book ch. 12 p. 9); and in 8.9.10 a group shown in 3D may not
contain 2D-only shapes — the Problems view reports it (Help *Group*).

## G32 — The 3D scene goes dark or one-sided after adding a single Light
**Cause:** the scene's two default lights are dropped as soon as any Light element exists (Help 8.9.9).
**Fix:** add a complete set (e.g. ambient + directional) or none. Card: `3d-scene-z-order-and-lighting`.
Light colour filters object colours channel by channel — a red light hides a blue object — so keep lights
white or grey when colour carries meaning (Help 8.9.10, *Light*).

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
recomputed on every access and called with the original field's local variables, e.g.
`delay_delayTime(agent)` as *Create custom flowchart block* generates it (Help 8.9.9, Dynamic parameters;
8.9.10 Lead Acid Battery phase 7/8 models). Check the parameters after *Create custom flowchart block*.
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
**Fix (8.9.1+):** conveyors, stations, jib cranes and overhead cranes (triggers counted per bridge)
accept a `Downtime` block directly (release notes 8.9.1; Help 8.9.10 *Overhead crane*, *Downtime* —
corrected 2026-10-01); transfer tables, turntables, turn stations and lifts offer only `fail()` /
`repair()`, driven and timed by your own logic. A Downtime can be forced from code with
`downtime.startTask(unit)` (in the 8.9.10 class, missing from Help's function table). For a conveyor, pick the Downtime priority on purpose (negative: waits until
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
Hand-written "closest unit" rules using `distanceTo` in a Seize *Resource choice condition* are
straight-line too; a PML Seize has its own *Resource selection* (nearest, nearest by route for GIS,
comparison, rating) — whether its *Nearest to the agent* is straight-line is *(unverified)*. Card:
`basicmodels/choosing-closest-resource`.

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
Card: `excel-round-trip-results-and-cloud`. An *Occurs once* event at time 0 runs after all On startup
code (Help 8.9.10, *Event*) — a clean place for "after everything is initialised" logic.

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
Card: `gis-shapefile-to-rail-markup`. Help 8.9.10 (*RailSettings*) confirms that crossings without a
switch are not detected, while collisions at switches are (G99).

## Agent-based models, statecharts and controls

## G53 — A population statistic written `item.inState(...)` may not compile in AnyLogic 8.9+
**Cause:** 8.9.0 renamed the local variable of population *Statistics* conditions and expressions
from `item` to `agent` (release notes). Material written for 8.8 and earlier — including *AnyLogic
in 3 Days* (6th ed., pp. 54, 55, 77) and older course handouts — still shows `item`.
**Fix:** write `agent.inState(Consumer.PotentialUser)` (no trailing semicolon in these fields); in
code, `count(consumers, c -> c.inState(Consumer.PotentialUser))` works in any version.
**Nuance (8.9.10 example models):** ten shipped models still hold `item.…` in these fields, five of them
re-saved by 8.9.2–8.9.7, so `item` is probably still accepted as a legacy name or converted on load; the
error would then come from typing or pasting `item` into new fields *(inferred; not build-tested)*. Write
`agent` in new work either way.

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
More instances: Field Service's "typical 5-hour repair" `triangular(0.5*T, T, 2.5*T)` averages 1.33 T
(about 6.7 h); the Pedestrian tutorial's ticket machine `triangular(7, 12, 40)` s, called "average 12",
averages 19.7 s; the Bank tutorial's ATM `triangular(0.8, 1.5, 3.5)` min averages 1.93 min.

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
Cheaper than a cyclic event per agent (Help 8.9.10, *Event*, *Transition*): tick *Enable synchronous steps*
on the container and put `onChange();` in the On step of the agent that holds the conditions. Conditions
on a moving agent's position (`distanceTo(...) <= d`) are not re-tested en route — movement is two events —
so they need polling. With any SD in the model, every armed condition in every agent is re-tested at each
solver step *(engine 8.9.10 bytecode)*: some time-only conditions work in hybrid models for that reason and
fire late once the SD part is deleted. Rates that depend on time or age freeze the same way (G70).

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
order. Card: `abm-stock-gated-purchase-allocation-and-brand-tie`. The Big Book (ch. 8 pp. 3–4,
ch. 15 p. 19) still shows the removed FIFO/LIFO/Random dropdown; ignore it.

---

# Part 3 — Traps from the AnyLogic 8.9.10 install: Help, example models, Big Book (added 2026-10-01)

Same short format. Evidence labels: "Help 8.9.10" = the offline Help of the installed PLE (path in
`knowledge/INDEX.md`); "engine" = an 8.9.10 engine or library jar read with `javap` (bytecode read, not
run); "model" = an example model shipped with 8.9.10 (`.alp` read, not run); "Big Book" = *The Big Book
of Simulation Modeling*. "Card" = `knowledge/08-example-patterns/<folder>/<name>.md`. Items marked
*(inferred)* or *(unverified)* have not been confirmed on a build.

## Time, calendar and units

## G61 — A one-argument `set_…(v)` on a library block is off by a factor of 3,600 (or 3.6)
**Symptom:** after `source.set_rate(2)` in an hours model the Source floods (7,200 arrivals an hour); a
pedestrian source, road speed map or turntable reacts far too strongly or weakly after a setter call.
**Cause (engine 8.9.10):** a block property that carries units keeps its value in a fixed internal unit,
and the one-argument setter stores the number as-is in that unit — not in the model time unit, and not in
the unit shown in the property's drop-down. The two-argument form `set_…(v, UNIT)` converts first.
Internal units of the 89 one-argument setters in the Process Modeling, Pedestrian, Road Traffic, Rail,
Fluid and Material Handling libraries:

| Internal unit | One-argument setters |
|---|---|
| per second | `Source.set_rate` |
| per hour | `PedSource.set_rate`, `CarSource.set_rate`, `PedAreaDescriptor.set_throughput` |
| km/h | `set_greenSpeedLevel`, `set_redSpeedLevel` (RoadNetworkDescriptor, road density map) |
| rpm | `set_rotationSpeed` (conveyor turntable, turn station) |
| SI (s, m, m/s, m/s², m³, m³/s, rad) | all the others |

**Fix:** always write the unit — `source.set_rate(lambda, PER_HOUR)` — and read back the same way
(`source.rate(PER_HOUR)`). The Help example `source.set_rate( 100 )` (*Functions*) means 100 per second.
**Why:** the call compiles and the model runs; only the volume is wrong, by the ratio of the two units.
The shipped *Agent Moves Between Spaces* calls `pedSource.set_rate(2000)` correctly only because
PedSource's internal unit happens to be per hour, like its field. Origin of the finding: G5.

## G62 — A delay or timeout is off by 60×, 24× or 7× (often only after the model time unit changed)
**Cause:** `minute()`, `hour()`, `day()` and `week()` return that span **in model time units**, while a
field with a unit drop-down (Delay time, Timeout, Rate, …) reads its expression **in the selected unit**
and converts it to model time again. Multiplier plus drop-down converts twice; the result is right only
while the drop-down equals the model time unit, which stops being true when the model time unit changes.
Help 8.9.10 (*Time functions*) states the rule for `toTimeoutInCalendar()`, which also returns model time
units: choose the model's time unit in the drop-down beside the field. The same page, and Big Book ch. 16
p. 4, still call multipliers unit-proof — true only in code that has no drop-down.
**Fix:** one mechanism per field: a plain number with the drop-down on the data's unit (`14`, days), or the
multiplier with the drop-down on the model time unit. In actions, functions and `restart(...)`, use
multipliers or `toModelTime(x, DAY)`.
**Check (not yet run):** in a Day model, a Timeout of `day()` with the drop-down on HOUR should fire after
one hour. Shipped models that are right only by coincidence: *Statechart for Choice of Competing Products*
(`2 * week()`, drop-down DAY, Day model) and *Subway Entrance Hall - Phase 4* (`uniform(1.5, 3.0) *
second()`, drop-down minutes, minutes model).

## G63 — A daily 08:00 event (shift start, opening time) drifts to 07:00 or 09:00 twice a year
**Cause (Help 8.9.10, *Time functions*):** `day()` and a recurrence of "1 day" are always 24 hours, while
the model date follows the computer's time zone, daylight saving included; across a DST change a 24-hour
step lands one clock hour off.
**Fix:** recurrence `toTimeoutInCalendar(DAY, 1)` with the drop-down on the model time unit (G62); first
occurrence `getTimeoutToNextTime(8, 0, 0)`; rosters as a Schedule on calendar dates. Never initialise a
constant with `toTimeoutInCalendar` — it depends on the current date. DST rules come from the PC's locale
(Help *Reproducible model runs*), so record it with the results.
**Why:** hourly arrival profiles and shift KPIs are misaligned for half the year, silently.
Card: `bigbook/calendar-time-dst-safe-events-date-fields-and-run-speed`.

## G64 — A date lands in the wrong month, a monthly lookup peaks a month late, or "after 18:00" logic fails
**Cause (Help 8.9.10, *toDate*, *getMonth*, *Time functions*):** the date functions follow
`java.util.Calendar`:
- months are 0-based in `toDate(y, m, d, …)` and `getMonth()` (JANUARY = 0): `toDate(2026, 3, 1, 0, 0, 0)` is 1 April;
- `getDayOfWeek()` starts at SUNDAY = 1;
- `getHour()` is the 12-hour reading (22:20 gives 10); `getHourOfDay()` is the 24-hour one;
- `hour()` is a duration, not the clock.

A table function on arguments 1…12 read as `demand(getMonth())` with Out of range = *Nearest* gives
January its own row but February January's, March February's, and so on; December's row is never read.
The shipped *Bass Diffusion - Phase 4, 5 and 6* tutorial models do exactly this.
**Fix:** use the constants (`MARCH`, `SATURDAY`); `getMonth() + 1` for 1-based tables; `getHourOfDay()`
for clock tests; Out of range = *Error* while testing; plot each calendar lookup over one simulated year.
Cards: `bigbook/calendar-time-dst-safe-events-date-fields-and-run-speed`,
`videos/sd-calendar-seasonality-start-date-and-months`.

## G65 — The same model gives other results on another PC, in a new experiment, or a month later
**Cause (Help 8.9.10, *Model time*):** the start date defaults to the date the model was created, and each
experiment stores its own; everything that reads the calendar (`getMonth()`, `getDayOfWeek()`, calendar
events, schedules) moves with it. A start date set to "today" in code (the shipped *Simple Hospital (AI
Testbed)* does this) makes every day's run different.
**Fix:** set the start date explicitly in every experiment and print `date()` at startup; drive pure
seasonality by elapsed time (a *Repeating* table function) when the calendar itself does not matter. If
results still differ with a fixed seed, work through G17.
Card: `videos/sd-calendar-seasonality-start-date-and-months`.

## Distributions and statistics

## G66 — Distribution arguments that differ from the textbook (beyond `lognormal`, G3)
**Symptom:** a duration centres on the intended standard deviation, Weibull lifetimes are off by orders
of magnitude, or adding bounds moves the mean far more than expected — never an error.
**Cause (Help 8.9.10, distribution pages; Big Book ch. 15):**

| Call | Meaning | Trap |
|---|---|---|
| `normal(sigma, mean)` | standard deviation **first** | N(49, 5) pasted as `normal(49, 5)` gives mean 5, sd 49; Big Book ch. 7 (Fig. 7.19) writes its life-phase timeouts this way |
| `weibull(beta, alpha)` / `weibull(alpha, beta, min)` | 2 args = (scale, shape); 3 args = (shape, scale, min) | the order flips between overloads; fitting tools report (shape, scale) |
| `exponential(lambda)` / `exponential(min, max, shift, stretch)` | a rate / a scale (`stretch` = mean before truncation) | rewriting `exponential(0.2)` as `exponential(0, 20, 0, 0.2)` cuts the mean 25-fold |
| `normal(min, max, shift, stretch)` | `shift` = mean, `stretch` = sd, before truncation | bounds that bite pull the realised mean inward |
| `gamma(min, max, alpha, shift, stretch)` | truncated gamma | uses alpha = 1 whenever alpha < 1 |
| `pareto(alpha)` | minimum 1, not 0 | — |

Truncated forms redraw until the value lies in [min, max].
**Fix:** label arguments in a comment (`weibull(/*shape*/ 2, /*scale*/ 1000, /*min*/ 0)`); for a bounded
normal use the truncated form with shift = mean and stretch = sd; draw about 10⁵ samples in a scratch
experiment and compare mean, min and max with the source before trusting any input. Cards:
`bigbookmodels/probability-distributions` (verified signature table),
`bigbook/randomness-library-defaults-truncated-forms-and-area-placement`, `bigbookmodels/statechart-for-life-phases`.

## G67 — `meanConfidence()` reports an interval that is too narrow for a few replications
**Cause (engine 8.9.10, `StatisticsDiscrete.meanConfidence()`):** it returns 0 with no sample, +∞ with one,
otherwise t · `deviation()`/√n at a fixed 95 % — but it reads t one degree of freedom too high from a table
that starts at 4 degrees of freedom and ends at 100 (1.96 beyond). n = 2, 3 and 4 all get t = 2.776 instead
of 12.71, 4.30 and 3.18: half-widths 4.6×, 1.55× and 1.15× too small. n = 5–8 come out 2–7 % too small. The
formula also assumes independent samples, which successive within-run observations are not.
**Fix:** for small n compute `t * s.deviation() / Math.sqrt(s.count())` with the exact Student-t value
(4.303 for n = 3, 2.776 for n = 5) and state the level; build intervals over replications, or over batch
means after a warm-up, never over raw within-run samples; give any "stop when precise enough" rule a
minimum n.
**Why:** replication counts and sim-opt re-verification (G11) are only as honest as the interval.
Card: `bigbookmodels/simulation-terminates-when-confidence-is-reached`.

## G68 — Logging a block's random property shows values the model never used
**Cause (Help 8.9.10, *Dynamic parameters*):** per-agent block properties are generated as functions, so
every call re-evaluates the expression — for a random expression, a fresh draw. `traceln(self.delayTime(agent))`
in On enter prints a different number from the delay the agent actually gets.
**Fix:** draw once into an agent field upstream (`agent.serviceTime = triangular(…)`) and use that field
both in the block and in the log.
**Why:** it produces false validation evidence. Card: `basicmodels/execute-expression-from-database-value`.

## G69 — Calibration returns a different "best" pair every time, all with the same error
**Cause:** the two parameters reach the model only through a combination — a product, ratio or sum, such
as `ContactRate * Infectivity` in SIR — so the data pin down only the combination; the best pairs lie on a
curve.
**Fix:** fix one factor from independent data and calibrate the other, or calibrate and report the
combination (the shipped *Epidemic Model - Various Experiments* fixes ContactRate and calibrates
Infectivity and AverageIllnessDuration). Make the output dataset cover the whole run: `difference()`
compares only where the two curves overlap (Help 8.9.10, *Calibration experiment*), so a short dataset
tail drops the start of the run from the fit (G18).
**Why:** a "calibrated" contact rate that is really arbitrary misleads every policy that acts on contacts.
Card: `bigbookmodels/epidemic-model-various-experiments`.

## Statecharts, events and messages

## G70 — A failure or churn rate that should grow with age or overdue time changes nothing
**Cause (Help 8.9.10, *Transition*, *Agent API*):** a Rate trigger's expression is read on entering the
state and re-read only when that agent's `onChange()` runs — by default only when the agent itself
originates an event or receives a message; a Timeout is read once. In between, `time()`, an age or another
agent's data in the expression stay frozen. In both 8.9.10 *Field Service* models the overdue multiplier is
evaluated only at moments when the unit is not overdue *(inferred from Help and the model settings; not
run-tested)*.
**Fix:** give the agent a periodic refresh (a cyclic event, or synchronous steps with `onChange();` in On
step), or call `onChange()` whenever an input of the formula changes; replace a Timeout-drawn failure time
with a Rate; or thin — fire at an upper-bound rate and accept with probability λ(t)/λmax in a Branch (not a
guard, G71). Tag failures by overdue status to prove the effect is active.
**Why:** a central assumption switches off silently and biases policy comparisons (fewer crews look
cheaper). Card: `bigbook/abm-time-dependent-hazard-rate-refresh`. Related: G56.

## G71 — An agent waits forever in a state whose Timeout (or Rate) transition has a guard
**Cause (Help 8.9.10, *Transition*; Big Book ch. 7 p. 17):** a guard is checked once, when its trigger
fires. A Timeout that fires with a false guard is disarmed until the state is entered again; a Rate, until
its value changes. Condition, Message and Arrival triggers keep waiting instead. There is no error, and the
Events view no longer lists the transition.
**Fix:** test in a Branch after the Timeout, with a Default exit that loops back or waits elsewhere; if the
rule really is "wait until X", use a Condition trigger.
**Why:** the stranded agent keeps its resources and looks like a capacity problem.
Card: `bigbook/statechart-guards-branches-and-state-reentry`.

## G72 — "msg cannot be resolved" in a branch condition
**Cause (Big Book ch. 7 p. 18):** the received message is in scope only in the transition segment that
has the Message trigger, not in the branch exits after it.
**Fix:** store it in that segment's Action (`lastMsg = msg;`) and test the stored copy in the branches.
Card: `bigbook/statechart-guards-branches-and-state-reentry`.

## G73 — An event inside an agent type never fires for agents created later, or fires out of step
**Cause (Help 8.9.10, *Event*):** *Occurs once* times and the first occurrence of a *Cyclic* event are
**absolute** model times. An event created after its time never occurs; a late-born agent's cyclic event
is phased from time 0, not from its birth.
**Fix:** for a time relative to the agent's creation, enter `time() + N` as the first occurrence, or use a
*User control* event and call `restart(N)` in the agent's On startup.
**Why:** births, arrivals and replacements are exactly the agents whose timers matter, and the loss is
silent. Card: `bigbook/event-modes-condition-monitoring-and-lifecycle`.

## G74 — A Condition event fires only once, or `restart()` in its action freezes the run
**Cause (Help 8.9.10, *Event*):** a Condition event stops watching after it fires, by design; calling
`restart()` while the condition is still true makes it fire again at the same instant — an endless
zero-time loop.
**Fix:** in the action, first change the state so the condition becomes false, then `restart()`; for
"above / below" logic use two events that re-arm each other (hysteresis); compare continuous values with
`>=` / `<=`, never `==`. Card: `bigbook/event-modes-condition-monitoring-and-lifecycle`.

## G75 — A paused and resumed phase takes its full duration again
**Cause (Help 8.9.10, *Transition*, *History state*):** a Timeout counts from the moment its state is
entered, and resuming through a History state is a new entry — History restores which state is active, not
its clocks. In the shipped *Statechart for Product Lifecycle* a `uniform(3, 24)`-month phase paused at month
20 restarts with a fresh draw.
**Fix:** decide whether a pause keeps progress. If it does, end the phase with a *User control* event and
call its `suspend()` / `resume()` (Help *Event*: these keep the remaining time), or store the planned
duration and entry time and use the remainder as the timeout. If it does not, state it as an assumption.
**Why:** suspend/resume is how portfolio and project models test policies; a hidden reset penalises
pausing. Card: `bigbookmodels/statechart-for-product-lifecycle`.

## G76 — A message sent by an agent that removes itself in the same action never arrives
**Cause:** `send()` delivers in a separate zero-time event after the current one (Help 8.9.10,
*Communication between agents*), and the delivery is cancelled if the sender has been destroyed by then
(8.9.10 Help tutorial *Air Defense System*, phase 4).
**Fix:** deliver synchronously with `target.statechart.receiveMessage(msg)` (it returns `false` if no
transition took the message), or set a field on the target and call `target.onChange()` with a Condition
transition on it. Do not rely on removing the sender "one event later": simultaneous events run LIFO by
default (G60).
**Why:** outcome counts (hits, deliveries, completions) are biased with no trace.
Card: `videos/pursuit-intercept-agents-in-continuous-3d-space`.

## G77 — Two jobs dispatched in the same instant go to the same idle vehicle; one is never served
**Cause:** the dispatcher tests `inState(Idle)` and notifies with `send()`, which arrives in a later
zero-time event; until then the vehicle still looks idle, so a second dispatch picks it again. The second
message reaches a state that ignores it and is dropped (G21), and any field set at dispatch now points at
the second job. The 8.9.10 *Wind Turbine Maintenance* tutorial model has this structure and survives only
because its requests never coincide.
**Fix:** reserve in the same step as the check — a claim field, an idle list the dispatcher removes from,
or a ResourcePool/Seize; let the completion reply carry the job object and accept only the open job. Test
by raising two requests in one action with one vehicle idle, and check raised = completed + open.
**Why:** ties are rare under random arrivals but certain at start-up, in batches and at shift starts — the
peak scenarios. Card: `videos/dispatch-idle-check-then-send-double-booking`.

## G78 — Agents wired port to port clearly react, but no message code can be found
**Cause (Help 8.9.10, *Ports*, *Library developer mode*):** a port's *Message handling actions* (On
receive, On send) and its Advanced options (custom port class, message types) are shown only with
**Library developer mode** on.
**Fix:** Tools → Preferences → Development → *Library developer mode*; when auditing someone else's model,
also search the `.alp` (XML) for the handlers.
**Why:** code hidden behind a preference is easy to miss in a review, and it can hold a model's whole
wiring. Card: `models/petri-nets`.

## System dynamics

## G79 — A lookup returns negative or zero values once its input leaves the table
**Cause (Help 8.9.10, *Table function*):** *Out of range = Extrapolate* continues the table by its
interpolation rule — with Linear, the last segment's slope — so a declining effect curve crosses zero, and
used as a divisor gives Infinity. (The Big Book's crowding table is safe only because its last two points
are equal.)
**Fix:** effect lookups → *Nearest*, or end the table with a flat segment; keep divisors above zero; use
*Error* while testing to catch unexpected inputs.
**Why:** extreme scenarios are what decision models exist for, and this failure hides in the tail.
Card: `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step`.

## G80 — SD results change with the solver step, or random input behaves differently at another step
**Cause:** `uniform()`, `normal()` and other draws inside a flow or dynamic-variable formula are redrawn at
every solver evaluation, so the noise depends on the step and the method (Big Book ch. 5 p. 11 advises
against it). In 8.9.10 the step and method are model properties, section *System Dynamics solver*.
**Fix:** draw once per period in an event that writes a *Constant* variable, or use a pink-noise structure
scaled for the step (`sdmodels/pink-noise`). Verify any SD model by halving the step. Instance:
`sdmodels/adaptive-exp-random-walk` draws `normal(-100, 100, 0, 50)` inside a flow.
Card: `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step`.

## G81 — A value set on an SD variable by a slider, button or event snaps back
**Cause (Help 8.9.10, *Dynamic variable*; Big Book ch. 5 p. 47):** an ordinary dynamic variable or flow is
recomputed from its formula; only *Constant* variables (and parameters) keep an assigned value.
**Fix:** tick *Constant* on anything set from outside (or use a parameter) and let the formula part read
it. Cards: `bigbook/sd-instant-charts-and-step-pause-flight-simulator`,
`bigbook/event-modes-condition-monitoring-and-lifecycle`.

## G82 — An outflow written as "Stock × fraction" does not send that fraction of the people leaving
**Cause:** a residence-time outflow `Stock / T` and a second outflow `Stock * f` are competing first-order
exits: the share taking route 2 is `f / (f + 1/T)`, and both shorten the stay. In the shipped *Patient
Care Process Swimming Pool Metaphor* (T = 3 months, f = 0.1) about 23 % are misdiagnosed, not 10 %, and the
mean time seeking care falls from 3 to about 2.3 months.
**Fix:** when f is a share of those leaving, split one outflow: `Stock * f / T` and `Stock * (1 - f) / T`
(the shipped *Pharmaceutical Pipeline And Medicines Use* does this); when it really is a hazard per time
unit, give it time units and name it a rate.
**Why:** the parameter's name and its effect disagree silently; calibration then tunes the wrong knob.

## G83 — An SD pulse or sample keyed on `time()` equality is missed or mis-sized
**Cause (reasoned):** the idiom `(int)(time()/k) == time()/k ? X / TIME_STEP : 0` needs `time()` to land
exactly on multiples of k — safe for binary-exact steps such as 0.25 or 0.125, not for 0.1 — and the flow to
be evaluated once per step (Euler). RK4 also evaluates flows at intermediate stage times, so a one-step
pulse no longer weighs one full step. *(Floating-point and solver reasoning; not run-tested.)*
**Fix:** keep Euler with a binary-exact step, or compare with a tolerance
(`abs(time()/k - round(time()/k)) < TIME_STEP/2`), or add the amount to the stock from a cyclic event.
Instances: `sdmodels/sir-model-threshold`, the shipped *Summary Statistics* model, many Vensim imports.

## G84 — A hybrid model crawls once agent statistics feed SD formulas
**Cause:** a population statistic referenced by a flow or auxiliary is recomputed at every solver step —
with the Big Book's fixed step of 0.001, at least 1,000 full passes over the population per time unit.
With any SD in the model, every armed condition in every agent is also re-tested at each step *(engine
8.9.10 bytecode; not run-tested)*.
**Fix:** tick *Constant* on the SD variable and assign it from a cyclic event (`Demand =
consumers.NumberReadyToBuy();`) with a period well below the SD time constants, or keep the count as a
counter updated in the agents' state entry and exit actions.
Card: `bigbookmodels/multimethod-interface-catalogue`.

## Process Modeling Library blocks

## G85 — A conditional Hold opens when you meant it to close, or never reopens
**Cause (Help 8.9.10, *Hold*):** in *Conditional* mode the field is a **Blocking condition** — true = the
agent waits (the opposite of Wait, SelectOutput and guards, where true = go) — and it is tested when an agent
arrives, not polled. After the data it reads change, waiting agents are re-tested only when
`hold.recalculateConditions()` is called. The Hold stores no agents; they wait in the block before it.
**Fix:** write the condition as "must wait" (`hooksReady == 0 || platformsReady == 0`) and call
`recalculateConditions()` on every Hold that reads an input wherever that input changes (one `checkHolds()`
function keeps this in one place), or use *Manual* mode with `block()` / `unblock()`. *Block automatically
after N agents* lets N agents **through** and then closes until `unblock()`; with *Initially blocked* and
N = 1, each `unblock()` releases exactly one agent.
**Why:** a gate that never reopens looks like low demand or a slow resource.
Cards: `models/car-assembly-marriage`, `basicmodels/storage-with-initial-stock`, `basicmodels/hold`.

## G86 — A condition typed into a SelectOutput has no effect
**Cause (Help 8.9.10, *SelectOutput*):** *Select True output* defaults to *With specified probability*
(`conditionIsProbabilistic` = true). A condition typed earlier stays stored in the model but is never
evaluated — the shipped *Road Traffic Tutorial - Phase 6* holds `randomTrue(0.10) && parkingLot.nFree() > 0`
and routes by probability 0.1 alone.
**Fix:** switch the mode to *If condition is true*; if the condition draws random numbers or reads other
blocks, also tick *Condition is stochastic or volatile* (G6).
Card: `videos/road-destination-refusal-parking-bus-stop-outwaynotfound`.

## G87 — `stopDelay(null)` releases every agent in the Delay
**Cause (Help 8.9.10, *Delay*):** a null argument to `stopDelay(agent)` releases all delayed agents, and
`extendDelay` / `reduceDelay` with null act on all of them. A failed `findFirst(...)` or an unset reference
turns a targeted release into a global one, with no exception.
**Fix:** guard the argument (`if (a != null) delay.stopDelay(a);`); call `stopDelayForAll()` only when
"all" is meant; for per-agent release consider Wait + `free(agent)` (G7).
**Why:** it hits exactly the manual-release pattern the tutorials teach (Job Shop phase 4;
`models/product-delivery`'s `stopDelay(order)`).

## G88 — Agents removed from a Queue or Delay by code pile up in the model
**Cause (Help 8.9.10):** `queue.remove(a)` / `delay.remove(a)` only take the agent out of the block
(`remove` returns null if it is not there); an agent that never reaches a Sink or Exit stays in the model.
The shipped *Epidemic and Clinic* removes request tokens this way without disposing of them.
**Fix:** hand the removed agent to an `Enter` → `Sink` pair named, e.g., `cancelled`
(`cancelled.take(a)`), which also counts the cancellations.
**Why:** a silent leak and a lost renege count. Card: `bigbookmodels/request-tokens-into-a-shared-process`.

## G89 — An urgent Seize never interrupts a unit busy with a less urgent task
**Cause (Help 8.9.10, *Seize*):** *Task priority* only orders waiting requests. Whether a running task can be
interrupted is set on the block whose task may be interrupted, by *Task preemption policy*, whose default is
**No preemption**; *Task may preempt* (default true) matters only once that policy allows it.
**Fix:** choose *Wait for original resource*, *Seize any resource*, *Terminate serving* or *Continue without
resource* on the interruptible Seize or Service; keep *Auto suspend/resume agents* on unless you handle
suspended agents yourself. Card: `basicmodels/resources-task-priority`.

## G90 — Blocks reconnected by code still route the old way, or the connection is refused
**Cause:** an `out` port can be connected only while no agent has entered its block, and a connection that
agents have used cannot be removed (shipped model *Connecting Library Objects Dynamically*); the far-end
ports keep their start-up wiring until `refreshConnections()` is called on them (Help 8.9.10,
*Troubleshooting*).
**Fix:** wire in Main's On startup, before any agent moves; call `refreshConnections()` on every reconnected
end port; for decisions during the run use SelectOutput, Hold, or `Exit` → `enter.take()`.
**Why:** the failure is silent mis-routing. Card: `basicmodels/connecting-library-objects-dynamically`.

## G91 — A Source that reads agent parameters from a database delivers a fixed rotation of types
**Cause (Help 8.9.10, *Source creates agents with parameters read from DB*):** with arrivals by rate,
interarrival time or schedule, the Source reads the table row by row and, after the last record, starts
again at the first — A, B, C, A, B, C …
**Fix:** when the mix is random in reality, untick it and draw the type in On exit from a discrete
distribution, looking up per-type data in the table; to go through the table once, limit the number of
arrivals to the row count.
**Why:** a deterministic mix removes arrival-mix variability from every KPI.
Card: `basicmodels/execute-expression-from-database-value`.

## G92 — A schedule built in code gives no arrivals, or the wrong period
**Cause:** a `ScheduleWithUnits` built in code must be completed with `initialize()` after its setters and
intervals, and the Source must be switched to it — `set_rateSchedule(s)` **and**
`set_arrivalType(Source.RATE_SCHEDULE)`. `setPeriod(...)` is described two ways (schedule time units in
Help 8.9.10 *Schedule API*, milliseconds in the engine Javadoc), and the shipped *Schedule Created
Programmatically* never calls `setTimeUnits(...)`. The Schedule element was remastered in 8.9.10 (release
notes).
**Fix:** set the units explicitly, then the period, then `initialize()`, then attach the schedule; print
`getValue()` and `getTimeOfNextValue()` at startup to confirm the period *(the unit rule is unverified —
test once)*. For schedules held by a multi-run experiment, Help asks for `setSingleThreadMode(false)`.
Card: `basicmodels/schedule-created-programmatically`.

## Material handling, fluid and rail

## G93 — Retrieving a particular item from a deep rack lane stops the run with an error
**Cause (Help 8.9.10, *Storage*):** in deep-lane storages only the cell next to the aisle (for FIFO flow,
the retrieval side) can be emptied; asking for an item behind it is an error. Drive-in and selective racks
are LIFO per slot. In FIFO/LIFO flow storages `cell.setReservation(agent)` and `getRandomFreeCell()` must
not be used.
**Fix:** test `storage.getCell(item).isAvailableToRetrieve()` before sending a chosen item to Retrieve;
otherwise pick with `getRandomAccessibleAgent()` (8.9.5+), tick Retrieve's *Allow retrieving from deep
position* (8.9.5+) when an operator really digs items out, or model the re-handling explicitly.
**Why:** lane depth is what makes push-back and drive-in racks cheap; order logic written for "any item, any
time" is wrong for them. Cards: `basicmodels/push-back-rack`, `basicmodels/slotting-policies-in-drive-in-storage`.

## G94 — Items pre-loaded into a StorageSystem are missing from your stock bookkeeping
**Cause (Help 8.9.10, *Storage system*):** *On agent storage* (of the system and of each storage) does not
run for items created by the initial filling, a feature since 8.9.5.
**Fix:** do the bookkeeping in the *New agent* expression: a factory function that creates the item in your
population, sets its fields, sends the message the normal storage path would send, and returns it. Fill
with `INITIAL_PARTIAL` or `INITIAL_FULL`, by number of items or percent of capacity.
**Why:** a warm-started warehouse is warm for the KPIs only if the pre-loaded items went through the same
accounting. Cards: `basicmodels/storage-with-initial-stock`, `models/warehouse-conveyor`.

## G95 — A tugger train fed from a conveyor leaves with one item each trip
**Cause:** with *Delivery starts when* = *no available agents left*, the next item is still travelling to
the belt's end when the first is loaded, so "no agents left" is true at once (shipped *Tugger Train
Delivery Policies*, on-canvas note).
**Fix:** use *timeout ends* with a per-agent pickup timeout a little longer than the item spacing on the
belt, or *condition is met*.
**Why:** trips, empty travel and fleet size all come out wrong. Card: `basicmodels/tugger-train`.

## G96 — Two AGVs meet head-on, pause about 10 s, then drive through each other
**Cause (Help 8.9.10, *TransporterControl*):** with *Navigation: Automatic* and *Resolve collisions* on,
vehicles moving in opposite directions wait out the *Collision detection timeout* (default 10 s) and then
pass over each other at the node. With it off the run stops with an error; *Avoid collisions* only reserves
contested paths and does not guarantee avoidance.
**Fix:** one-way corridors, or *Navigation: Custom* with a passing bay and a *Can enter node* guard.
**Why:** the resolver breaks deadlocks; it is not a traffic rule, and its overlap hides real blocking.
Card: `basicmodels/passing-an-oncoming-transporter`.

## G97 — Closing one branch of a proportional FluidSplit stops the other branch too
**Cause (Help 8.9.10, *FluidSplit*):** *Proportional* mode keeps out1 / fraction1 = out2 / fraction2, so zero
flow on one side forces zero on the other, and upstream tanks fill.
**Fix:** when a branch can close, switch the split to `SPLITMERGE_NEUTRAL` (or re-set the fractions) at the
moment it closes, and back when it reopens. Card: `basicmodels/split-one-stream-into-multiple-streams`.

## G98 — Train methods or fields will not compile after a TrainDecouple (or a TrainSource)
**Cause (Help 8.9.10, *TrainDecouple*; Big Book ch. 9 p. 30):** trains created by TrainDecouple — and by a
TrainSource without a custom *New train* — have the type in its *New train* field, plain `Agent` by default,
so blocks downstream see no train API and no custom fields. The rail counterpart of G23.
**Fix:** create a Train type and select it in every block that creates trains; set TrainCouple's Advanced
*Train type (1)/(2)* to read fields in its actions. Card: `bigbook/rail-consist-coupling-decoupling-mechanics`.

## G99 — `The switch '…' cannot be seized: another car is over it` (often only in fast runs)
**Cause (Help 8.9.10, *Preventing train collisions*):** the Rail Library detects collisions at switches but
does not prevent them; random dwells make the conflict rare at animation speed and certain in virtual time.
Tracks that cross without a switch are not checked at all (G52).
**Fix:** lock each shared section with a capacity-1 ResourcePool — seize before the TrainMoveTo that enters
it, release once the train has cleared it (or Hold, RestrictedAreaStart/End); add a look-ahead point so
only trains facing a busy section brake; lock switchless crossings too.
Card: `bigbook/rail-traffic-control-block-locking-and-lookahead`.

## G100 — `track.reserveFor(train)` stops the run, or a second train crosses with no reservation of its own
**Cause (Help 8.9.10, *Railway track*):** a track can be reserved by one train at a time; reserving one
that is already reserved, or that another train is passing, is an error. A reservation is a lock without a
waiting list: a train that finds a track unavailable stops at the switch in front of it.
**Fix:** reserve all-or-nothing after checking every track of the set — `isAvailableFor(train)` and no
other train on it (`getTrains()` / `isEmpty()`); re-try for the trains that failed when the holder releases
(`cancelReservation()` from a Position on track after the section), or keep a queue of waiting trains.
**Why:** the shipped demo works because only two trains ever exist; with more traffic, check-then-reserve
without a retry lets unreserved trains cross. Cards: `basicmodels/railway-track-reservation`,
`models/level-junction`.

## Road traffic, pedestrians, lifts and GIS

## G101 — A saturated road network never gridlocks, and cars overlap at junctions
**Cause (Help 8.9.10, *RoadNetworkDescriptor*):** *Automatically resolve deadlocks* is on by default and
dissolves a detected deadlock by letting the cars pass through each other.
**Fix:** in capacity studies run once with it off (a frozen model then shows the gridlock), log long stops
with *On stop* / *On resume moving*, and report whether any deadlock was resolved.
**Why:** travel times and capacity come out optimistic exactly where they matter.
Cards: `videos/road-network-descriptor-callbacks-speed-map-deadlocks`, `basicmodels/displaying-traffic-jams`.

## G102 — Cars vanish, or the run stops, when a parking lot is full
**Cause (Help 8.9.10, *CarMoveTo*):** a car sent to a lot reserves a space only as it approaches; with none
free it leaves through the lower port `outWayNotFound` (so do cars with no route). The same Help page also
says a full lot raises an error, and the tutorial model stopped with one until the port was wired. A
CarSource or CarEnter into a full lot is an error.
**Fix:** always wire `outWayNotFound` (to a fallback CarMoveTo) and count refusals in *On way not found*;
use `parkingLot.nFree() > 0` only as a filter, never as a guarantee.
Cards: `videos/road-destination-refusal-parking-bus-stop-outwaynotfound`, `basicmodels/carmoveto`.

## G103 — After drawing a side road, cars stop at the new junction instead of driving on
**Cause:** joining a road to the middle of another creates an Intersection that splits the existing road
in two; blocks still name the old road, which now ends at the junction (8.9.10 Help tutorial
*Intersection*, phase 3).
**Fix:** draw all connections first, then name the resulting roads and re-select them in every CarSource
and CarMoveTo; re-check each block's road after any topology edit.
**Why:** the model still runs; only the routes are silently shorter.

## G104 — GIS vehicles drive straight across fields or water, and trips are too short
**Cause (Help 8.9.10, *GIS map*):** with *If route not found* = **Create straight route**, a route that cannot
be built is replaced by a straight line without notice — for a destination that is not road-connected (an
island, a site misplaced at sea, G51), or with *Routes are* = Straight lines. 21 of the 23 routing settings
in the 8.9.10 example models use *Create straight route*, the Supply Chain GIS tutorial's included.
**Fix:** set *Show error dialog* while verifying; place sites by coordinates near roads; freeze a PBF
routing graph for experiments and Cloud; compare `distanceByRoute(dest)` with `distanceTo(dest)` on long
legs — nearly equal values suggest a straight substitute.
**Why:** travel time drives fleet size and lead-time KPIs.
Card: `videos/gis-routing-source-caching-and-straight-line-fallback`.

## G105 — Pedestrian gates sized from their service time are too few, while utilisation looks fine
**Cause (Help 8.9.10, *Services*, *Service with Lines*):** a service point is occupied from assignment
through the walk in, the delay, the walk out and the *Recovery delay*, but `getUtilization()` counts only
the time at the point. In the Subway tutorial a 2–3 s gate at 4,000 passengers/h needed 8 gates where the
delay alone suggests about 3.
**Fix:** measure the effective hold per gate at saturation (open time × gates ÷ served) and size from it;
judge stability on a queue-length plot over a long run.
Card: `videos/pedestrian-service-occupancy-sizing-and-density-map`.

## G106 — Pedestrian flow `traffic()` jumps around, reads low at the start, or disagrees with an hourly count
**Cause (Help 8.9.10, *Ped Flow Statistics*):** `traffic()` is the number of crossings in the **last five
minutes** × 12; in the first five minutes, and after a reset, the same ×12 is applied to a shorter window.
The shipped demo's description says "last hour".
**Fix:** for KPIs take differences of `countPeds()` over your own window (an hourly cyclic event); use
`traffic()` only as a live indicator. Card: `basicmodels/pedestrian-flow-statistics`.

## G107 — Up and down escalators of equal speed carry different flows; a "turned off" escalator is still used
**Cause (Help 8.9.10, *Escalator group*, *Escalator*):** by default everyone stands going up, while going
down people walk on the left side with a walking share of 0.5; `turnOff()` stops the steps but people may
still walk on them — closing an escalator is `block()`, which shuts the gate in front of it.
**Fix:** set behaviour and walking share per direction from observation; use `block()` for closures and
`turnOff()` for a power cut.
**Why:** capacity and queue KPIs shift by direction without any error.

## G108 — People stay in a failed lift forever, `cancel()` throws, or a repaired lift ignores calls
**Cause (Help 8.9.10, *PedElevator*, *Elevator*):** a failure removes nobody; `cancel()` works only before
boarding, so riders need `remove()`; and `moveTo(level)` leaves the lift in manual mode.
**Fix:** `cancelAll()` for those waiting; `remove()` plus PedEnter for riders (or move to
`getNearestLevel()` and let them off before `fail()`); `deleteCallsOnLevel()` for stale calls;
`setManualMode(false)` after repair. The state enum is `ElevatorState.MOVING` etc., not Help's
`ELEVATOR_STATE_*` (G122). Card: `basicmodels/elevator-failure`.

## Agent space, networks, controls and editing

## G109 — A direction-dependent probability (wind, heading, slope) leans to one side
**Cause:** the angle between two directions computed as `abs(a - b)`, without wrap-around.
`CellDirection.getAngle()` is a compass angle in [0, 2π) — NORTH 0, EAST π/2, NORTHWEST 7π/4 (engine
8.9.10) — so NORTH vs NORTHWEST gives 7π/4 instead of π/4. The shipped *Wildfire with Wind* does this: with
its default north-west wind, spread to the north gets the 180° probability while spread to the west gets
the 45° one.
**Fix:** `double d = abs(a - b); d = min(d, 2*PI - d);` and threshold on d; check that the two directions 45°
either side of the wind get equal probabilities. Card: `bigbookmodels/wildfire-with-wind`.

## G110 — NullPointerException from `getNeighbors()` in a discrete space
**Cause (engine Javadoc 8.9.10, `Agent.getNeighbors`):** it returns **null, not an empty array**, when the
agent has no neighbours — common in sparse grids and at startup. `getAgentAtCell(r, c)` and
`getAgentNextToMe(dir)` return null for empty or border cells (Help *Discrete space*).
**Fix:** `Agent[] nb = getNeighbors(); if (nb != null) for (Agent a : nb) …`.
Card: `bigbookmodels/wildfire-with-wind`.

## G111 — Hand-made contacts vanish mid-run, or agents born later never get any
**Cause (Help 8.9.10, *Agent API*):** `applyNetwork()` discards every existing connection — hand-made ones
included — and rebuilds from the network settings (with the User-defined type it does nothing). The
standard network is built once at startup: agents added later join unwired, and distance-based links keep
the positions of the last build *(the Big Book demo re-applies its network every 5 minutes for this
reason)*.
**Fix:** apply the standard network once, before adding custom links; wire newborns in their On startup;
or skip stored links and ask `agentsInRange(r)` when the relation is plain proximity.
Card: `bigbookmodels/periodic-repair-of-a-standard-network`.

## G112 — Hiding some copies of a replicated shape hides all of them
**Cause (Big Book ch. 12 p. 34):** *Visible* is evaluated before *Replication*, so a false Visible hides
every copy, even with an `index`-dependent expression.
**Fix:** keep Visible true and return `null` as the line and fill colours of the copies to hide
(`occupied[index] ? red : null`). Card: `bigbook/replicated-shapes-and-group-pivots`.

## G113 — "Index out of bounds" at startup from a shape that reads a replicated control
**Cause (Help 8.9.10, *Replicated controls*):** an expression such as `slider.get(index).getValue()` can be
evaluated before the copies exist.
**Fix:** call `slider.createShapes();` in the container's On startup. Changing the replication count
rebuilds every copy, so keep per-copy state in an array, not on the copies.
Card: `bigbook/controls-link-direction-sync-and-replicated-controls`.

## G114 — A parameter's On change never runs, or a slider shows a value the model is not using
**Cause (Help 8.9.10, *Modifying parameters from code*, *Linking controls*, *Slider*):** On change — and
propagation to dependent parameters — runs only through `set_<name>(v)`; a plain assignment skips both, and
a call with the current value does nothing. A control's *Link to* writes only from control to parameter,
so the slider does not follow code or buttons; and `setValue` snaps to the slider's range and step (with a
Console warning), which silently bounds a linked parameter.
**Fix:** change parameters with `set_<name>(v)`; in the parameter's On change put `slider.setValue(p);`;
use the control's *Enabled* expression to keep inputs legal.
Card: `bigbook/controls-link-direction-sync-and-replicated-controls`.

## G115 — After renaming an element, other formulas report "… cannot be resolved"
**Cause (Help 8.9.10, *Renaming model elements*):** typing a new name and clicking away renames only the
element; references follow only with in-place smart renaming (Ctrl+Enter before leaving the field) or
Projects view → *Rename…*. Custom-mode stock formulas need the same refactoring (Help *Stock*).
**Fix:** rename back, then redo it with Ctrl+Enter or *Rename…* and accept the preview.
Card: `bigbook/sd-units-check-sectors-and-hierarchical-interfaces`.

## Data, experiments, Python and RL

## G116 — An Excel input silently becomes 0, or old cell-type code stops compiling
**Cause (Help 8.9.10, *Excel file*; release notes 8.9.1):** an empty cell is not an error — numeric 0,
string "", boolean false, date null; only a type mismatch throws. Since 8.9.1 `getCellType()` and
`getCellFormulaType()` return a `CellType` enum, not an int. `setCellValue` and `setCellFormula` do not
recalculate formulas.
**Fix:** check `cellExists(...)` and the cell type before reading, and stop with `error(...)` on missing
keys; echo the loaded values; replace int type codes with `CellType` (or `var`); call `evaluateFormulas()`
after writes that formulas depend on.
**Why:** a plausible default is worse than a crash, and nobody sees it in Cloud.
Card: `bigbookmodels/reading-model-parameters-from-excel-using-reflection`.

## G117 — The Query, Insert, Update or Key-Value table element a book or old model names is not in the palette
**Cause (release notes 8.9.5, 8.9.8):** these four connectivity elements were deprecated and removed from
the palette in 8.9.5; old models that use them still open (fixed in 8.9.8). Big Book model descriptions and
older course notes still describe a "Query" with a *Mapping* page, and one 8.9.10 example (*Loading Data
from a Database and Using ResultSet*) still contains one.
**Fix:** use the Database element API (`getResultSet`, `getValue`, `modify`, `getConnection()` for
prepared statements), or import into the built-in database and use QueryDSL.
Cards: `basicmodels/feeding-a-collection-from-access-database`,
`bigbookmodels/using-prepared-statement-when-writing-to-databases`.

## G118 — A custom experiment does not reproduce what the Simulation experiment shows
**Cause:** `createEngine()` gives a fresh engine whose stop time, seed and simultaneous-event order are
whatever you set, and a root built with `new Main(engine, null, null)` has exactly the parameter values you
assign *(inferred from the engine API; both shipped demos set these explicitly)*.
**Fix:** set `setStopTime`, `setDefaultRandomGenerator(new Random(seed))` and
`setSimultaneousEventsSelectionMode(...)` to match, and call `root.setParametersToDefaultValues()` before
overriding parameters. Custom experiments are a Professional feature (Help 8.9.10, *Editions*).
**Why:** a calibration fitted under other settings fits the wrong model.
Card: `basicmodels/calibration-from-within-simulation`.

## G119 — A Python-driven parameter variation mixes up iterations or loses its Python session
**Cause:** a `PyCommunicator` held by the experiment is one object and one Python process shared by every
run; its connection ends with a run (the shipped demo re-creates it in *Before simulation run*), and with
*Allow parallel evaluations* on, several runs use it at once.
**Fix:** untick parallel evaluations, create the communicator per run, and key every value and log row by
`getCurrentIteration()`. Card: `basicmodels/python-from-experiment-screen`.

## G120 — RL configuration values never reach the model, or the platform rejects the spaces
**Cause (Help 8.9.10, *Reinforcement Learning experiment*):** the Configuration code runs before the model
is initialised, so it must assign fields directly (`root.x = …`), not call `set_x(...)`; space fields must
be `int`, `double`, `double[]` or simple data objects, not agents; there is one RL experiment per model, and
it has no reward field — reward lives in the Python wrapper.
**Fix:** assign in Configuration, call `set_…` only in the Action code, keep observation fields primitive,
and test with `createConfiguration()` / `applyConfiguration()` / `getObservation()` (8.8.6+) before export.
**Why:** the RL experiment cannot run inside AnyLogic, so these mistakes surface only on the platform.
Card: `basicmodels/reinforcement-learning-example-abca-model`.

## G121 — A trained RL policy gives extreme or constant actions when queried from the model
**Cause:** training usually wraps the environment in rescaling layers (observations and actions mapped to
[-1, 1]); the saved policy expects scaled inputs and returns scaled outputs, and raw model values skip that
mapping. The shipped *Stock Management Game* querier applies the same affine maps by hand.
**Fix:** keep the scaling constants beside the policy file in one helper used for training and inference;
clip the returned action to its valid range; test the querier on a few known states before a run.
**Why:** the model runs, so "RL is worse than the heuristic" becomes a false finding.
Card: `basicmodels/stock-management-game-rl`.

## G122 — A name copied from the 8.9.10 Help does not compile ("cannot find symbol")
**Cause:** some Help pages print names that the 8.9.10 libraries do not define (checked with `javap`):

| Help page | Help says | 8.9.10 defines |
|---|---|---|
| *Store*, Slotting policy | `Store.SP_EXPLICIT` | `Store.SP_SPECIFIC_SLOT` |
| *Source*, Arrivals defined by | `Source.RATE_TABLE`, `Source.ARRIVAL_TABLE` | `Source.RATE_SCHEDULE`, `Source.ARRIVAL_SCHEDULE`, `Source.DATABASE_ARRIVAL_TABLE` |
| *TransporterFleet*, max trailers | `maxNumberOfTrailers` | `maximumNumberOfTrailers` |
| *MixTank*, total amount | `totalAmount`, `set_totalAmount()` | `capacity` (read with `capacity()`; no setter — drive the property from a variable, then `updateAmounts()` while the tank is empty) |
| *Elevator*, state tables | `ElevatorState.ELEVATOR_STATE_IDLE` … | `ElevatorState.IDLE`, `LOADING`, `MOVING`, `FAILED` |
| *Reproducible model runs* | `getDefaultRandomNumberGenerator()` | `getDefaultRandomGenerator()` |
| *3D window*, navigation constants | `NAVIGATION_FULL` … | `WINDOW_3D_NAVIGATION_FULL` … from agent code (or `ShapeWindow3D.NAVIGATION_FULL`) |

Help text that disagrees with itself: *CarMoveTo* (full lot: exit port or error, G102); *Displaying traffic
jams* vs *RoadNetworkDescriptor* (transparency 0 = transparent or opaque); the Randomness wording of the
experiment pages (G16).
**Fix:** take the name from the editor (code completion, or the value the property writes into the
`.alp`), or check with `javap -cp <library jar> <class>` or the library's `doc/member-search-index.js` (see
`knowledge/INDEX.md`).
**Why:** the Help is the KB's first authority for exact names; these rows are the known exceptions.
Cards: `basicmodels/slotting-policies-in-drive-in-storage`, `basicmodels/source-with-arrivals-from-database-table`,
`basicmodels/tugger-train`, `basicmodels/mixtank`, `basicmodels/elevator-failure`.
