# AnyLogic gotchas & conventions (beginner traps)

Small, high-frequency mistakes that confuse beginners. Each entry: the symptom, the
cause, the fix, and the reason. Append new ones as they come up during builds.

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
1. **Uncheck `Forced pushing`** on the Source (the verified fix).
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

## G7 — There is NO "Wait" block in AnyLogic 8.x PML — use `Delay` in "Until stopDelay() is called" mode

**Symptom:** can't find a "Wait" block in the Process Modeling Library palette.

**Cause:** older AnyLogic had a `Wait` block; AnyLogic 8.x removed it. The palette holds agents via
**Hold**, **Queue**, and **Delay**.

**To hold agents indefinitely and release specific ones on command** (the "wait until signalled"
pattern, e.g. boarding patients waiting for a ward bed): use a **`Delay`** block with
**Type = "Until stopDelay() is called"** and **Maximum capacity** checked. Release individuals with
`delayBlock.stopDelay(agent)`; release all with `stopDelayForAll()`; count with `size()`.

**Verified 8.9 PML block names (from the palette):** Source, Sink, Delay, Queue, Select Output,
Select Output5, Hold, Match, Split, Combine, Assembler, Move To, Resource Pool, Seize, Release,
Service, Resource Send To, Resource Task Start/End, Downtime, Schedule, Enter, Exit, Batch, Unbatch,
Dropoff, Pickup, Restricted Area Start/End, Time Measure Start/End. **No "Wait".**

**Rule:** for "hold and release on signal", reach for `Delay` ("Until stopDelay()") + `stopDelay()`,
not a non-existent Wait block. `Hold` is a *gate* (blocks/unblocks a connection for ALL agents), not a
per-agent release mechanism.
