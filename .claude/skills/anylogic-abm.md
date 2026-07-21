---
name: anylogic-abm
description: Build agent-based models in AnyLogic 8.9 - agent populations sized by parameters, per-agent state loaded from CSV, daily-update loops, agent-to-Main scope, hybrid DES+ABM coupling. From the Steve Biko nurses/pharmacy build. Use when individuals with their own state drive system behaviour.
---

# anylogic-abm

When individuals matter (each nurse's fatigue, each item's stock), model them as an agent
population, not aggregates. These are the working idioms from a real hybrid DES+ABM build.

## When ABM (vs DES vs SD) — the 60-second test
- Entities FLOW through shared steps, individuality is just attributes → **DES**.
- Individuals carry evolving STATE that changes system behaviour (fatigue → absence → capacity;
  per-item (s,S) → orders) → **ABM population**.
- Only aggregates matter (total stock as one number) → System Dynamics / plain variables.
Hybrids are normal: our hospital = DES patient flow + ABM nurses + ABM pharmacy items.

## Population setup
- Create the agent type (Nurse, PharmacyItem…), then a **population** on Main.
- **Size the population with a parameter** (`numNurses`) — hard-coded sizes kill reusability.
- Per-agent fields: use **Parameters** for loaded-once config (salary, lead time), **Variables**
  for evolving state (stock, fatigueDaysRemaining).

## Loading per-agent data from CSV (the standard loop)
In Main → On startup:
```java
java.io.BufferedReader br = new java.io.BufferedReader(new java.io.FileReader(path));
br.readLine();                              // skip header
int i = 0; String line;
while ((line = br.readLine()) != null && i < agents.size()) {
    String[] c = line.split(",");
    Agent a = agents.get(i);
    a.field = Double.parseDouble(c[k]);     // match columns BY INDEX from the actual header
    i++;
}
br.close(); traceln("Loaded " + i + " agents");
```
Rules learned the hard way:
- **Open the CSV first** and map column indexes from the real header — never guess.
- Load EVERY field you'll display (we lost item names by loading only numerics; `c[1]` had them).
- If population > CSV rows, cycle: `rows.get(i % rows.size())`.
- Always `traceln` the load count — silent partial loads corrupt results invisibly.

## Behaviour: cyclic-event loops beat statecharts for simple dynamics
For daily/weekly agent updates, ONE cyclic Event on Main iterating the population is simpler and
faster to debug than per-agent statecharts:
```java
for (Nurse n : nurses) {
    if (n.isVacant) continue;
    if (n.sickDaysRemaining > 0) { n.sickDaysRemaining--; continue; }
    if (randomTrue(p(n))) { n.sickDaysRemaining = draw(); continue; }
    available++;
}
```
Use statecharts only when transitions are genuinely event-driven and interleaved (message-driven
behaviour, interrupts) — not for "once a day, update everyone".

## Scope (the recurring compile errors)
- Agent code referencing Main: `main.field` (every agent has the `main` reference in a Main-owned
  population).
- Main code referencing agents: `agents.get(i).field` or `for (A a : agents)`.
- Inside Main's own actions: bare names — `main.` there does NOT compile.
- Agent functions can read their own fields bare: `probabilityOfUse * main.baselineDailyArrivals`.

## Coupling ABM with the DES flow
- DES entity consumes agent resources: on service events call a Main function that iterates the
  population (e.g. `consumeForPatient()` decrements item stocks probabilistically).
- Agent state constrains DES capacity: the daily loop counts available agents; the weekly
  scheduler converts that to hours/capacity. Keep the coupling in named Main functions — one
  place to audit, one place the dashboards read.
- Aggregate KPIs over the population: write small Main functions
  (`itemsOutOfStock()`, `kpiLocumShare()`) instead of inlining loops in display texts.

## Reuse checklist (turning a model into a framework)
1. Population sizes ← parameters, edit-box controls.
2. All per-agent data ← CSVs with documented schemas.
3. Site facts (paths, capacities, names) ← one config file read FIRST in On startup.
4. Policy variants ← an int parameter + radio buttons + one switch in the policy function
   (never duplicate blocks per policy).
5. `traceln` every load with counts — your future self debugs a new site's data with these lines.
