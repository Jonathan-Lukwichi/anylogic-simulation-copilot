# Pattern card — Counting adoptions in an ABM: count flows at the event, never by differencing state counts
- **Source:** AnyLogic video "Part 1: Scenario 1 – ABM Market Competition Intro" (https://youtu.be/HBd_dKNVrSU) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Report current users, adoptions over time and distinct people reached per product correctly once users can discard, switch or re-adopt.

## Mechanism
The source is a third-party five-part series: two products A and B, 5,000 consumers, AnyLogic PLE. Part 1 explains a tracker on Main and Part 5 builds it:
- four `int` variables, `currentUsersA/B` and `cumulativeUsersA/B`;
- a cyclic Timeout event `trackAdoptions` that runs every day;
- each day it subtracts yesterday's count of agents in `UserA` from today's, adds `max(0, difference)` to the cumulative variable, and stores today's count.

**Why it is wrong.** A day-to-day change in a level equals inflow minus outflow. As soon as `UserA` has an exit (the series' 6-week discard, a switch, churn), the difference nets adoptions against exits. The `max(0, …)` clamp then discards every day on which exits won. In steady state adoptions roughly equal discards, so the "cumulative" figure creeps up on noise alone.
- *Illustration (my arithmetic, not from the video):* 3,000 users with a 42-day life give about 70 adoptions and 70 discards a day. The clamp adds only about 5 a day.
- The tracker is right only while nothing leaves the state. That holds in the built Scenario 1 only because Part 4 never draws a discard transition, although Part 2 defines `discardA/B`. There, "current" and "cumulative" are the same curve.

**Count at the event.** These are three different metrics:
1. **Current users (a level).** Population statistic, type count, condition `item.inState(Consumer.UserA)` (3-days p. 54), read as `consumers.nUserA()`.
2. **Adoptions (a flow, repeat purchases included).** Put `main.adoptionsA++;` in `UserA`'s **Entry action**. It runs once for every external entry, whichever transition entered (`buyA` from WantA, `buyA1` from WantAnything). It never runs for the internal `contactA` loop (Help 8.9.9, *Transition*).
3. **Distinct reach (people ever reached).** Give Consumer a `boolean everA`. In the same entry action write `if (!everA) { everA = true; main.reachA++; }`, or count `item.everA` with a population statistic.

For a daily adoptions plot, difference the **monotone** counter in the daily event: `adoptionsToday = adoptionsA - adoptionsAtLastTick; adoptionsAtLastTick = adoptionsA;`. Differencing a cumulative counter is exact; differencing a level is not.

## Resources
n/a

## Key settings worth copying
- Counters live on Main as `int` or `long`. Agents reach them with `main.` (G20).
- Count the outflow the same way: `main.exitsA++` in `UserA`'s **Exit action**. Exit actions run on every external exit, including discard and switch.
- Conservation identity, checked in the daily event: `consumers.nUserA() == initialUsersA + adoptionsA - exitsA`. On a mismatch call `error("...")` or `traceln(...)`.
- A per-state entry counter is the ABM analogue of a DES block's `count()`.

## KPIs instrumented
- Current users per product (level).
- Adoptions per day and cumulative adoptions (flow).
- Distinct reach, and repeat share = 1 − reach / adoptions.
- Ad-driven vs word-of-mouth adoptions, counted on the respective transitions (compare the `adAdopter` flag in `models/bass-diffusion-agent-based-animated.md`).

## Pitfalls
- **Counting in one transition's action.** That misses the other entry paths, since `UserA` is entered from both WantA and WantAnything. Use the state's entry action.
- **A self-loop drawn outside the state.** It is an external transition, so it exits and re-enters and re-runs the entry action, which double-counts. Draw contact loops inside the state (3-days p. 67).
- **Sampling a level.** A daily difference of a level also misses round trips inside the day (adopt and discard between two samples).
- **Warm-up.** If statistics are reset after a warm-up, reset these counters at the same moment.

## Reusable idea
Levels come from state counts. Flows come from counters at the events that move agents. Difference a level only when you really want the net change. SD has the same split: a stock's inflow is not its day-to-day difference.

## When the co-pilot should use this
- Any ABM KPI phrased as "how many adopted, churned, got infected, ever used": cumulative incidence vs prevalence.
- Reviewing trackers that difference `count()` snapshots, or KPI code with `max(0, …)` applied to a difference.
- ABM verification: check state-count conservation, the ABM counterpart of DES `source.count()` = exits + WIP (G37).

## Additions (8.9.10 review, 2026-10-01)
- Performance side: population statistics scan every agent at every call (Help 8.9.10 *Collecting statistics on agents*); for large N the entry/exit counters of this card are also the fast option. Per-period snapshots (age pyramids, family sizes) are rebuilt with a Histogram Data's `reset()` + `add()` each period (`bigbookmodels/kinship-model-with-customized-statistics.md`).
