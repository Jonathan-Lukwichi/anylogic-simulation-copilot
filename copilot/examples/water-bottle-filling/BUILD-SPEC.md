# BAN 780 — Assignment 2 "Water bottle filling" — Full Build Spec (AnyLogic 8.9.8 PLE)

This is the complete block-by-block recipe. I cannot click in AnyLogic for you, so **you build
each block and copy the exact values below.** Work top to bottom. Each stage maps to a rubric row.

**Libraries you'll use:** Process Modeling Library (PML) + Material Handling Library (conveyors).

**Fitted parameters (from `fit_parameters.R`, confirmed vs prior solution):**
- Bottle interarrival = `exponential(0.0814)`  (mean 12.28 s)
- Filling time = `normal(4.04, 11.89)`  ← AnyLogic order is **normal(sigma, mean)**
- Packing time = `normal(2, 9)` · Crate arrivals = Poisson **2.4/min** · Crate weight = `uniform(5.0, 6.2)`

---

## STAGE 0 — Project & files
1. `File ▸ New ▸ Model`. Name it **exactly** `SemA02_<YourSurname>_<StudentNo>` (rubric: file naming).
2. Copy `semA02-layout.png` and the dataset into the model folder.
3. Save now and often.

## STAGE 1 — Environment  → rubric: *Model runs*
On **Main**, click empty canvas → Properties. On the **Simulation: Main** experiment:
- **Model time units = seconds** (Main properties).
- Randomness → **Fixed seed**, seed value **1**.
- Model time → **Start date** = `2023-06-11 08:00:00`, **Stop = Stop date** `2023-06-11 18:00:00`
  (that's 36 000 s, a 10-hour run).

## STAGE 2 — Layout image + scale  → rubric: *Scaled*
1. Palette **Presentation ▸ Image** → drag onto canvas → import `semA02-layout.png`. Lock it.
2. Palette **Space Markup ▸ Scale** → draw the ruler along a feature of known length on the image,
   then set its value so model metres match reality. Calibrate using the given sizes:
   - bottle outer radius **0.0838 m** (Ø 0.1676 m), crate shorter side **0.18 m**,
   - thin conveyor width **0.10 m**, thick conveyor width **0.20 m**.
   Get scale right here — every later size depends on it.

## STAGE 3 — Agent types (the things that flow)
Create 3 agent types (`File ▸ New ▸ Agent type`), each with a simple 2D animation:
- **Bottle** — add a `boolean` variable `filled = false`. Animate as a small circle, radius `0.0838` m
  (blue when `filled`, grey when empty — set the shape Fill color = `filled ? blue : lightGray`).
- **Crate** — add a `double` variable `weight`. Animate as a rectangle, short side `0.18` m.
- **PackageFull** — the loaded crate (6 bottles in a crate). Add `double weight`. Rectangle `0.18` m.

---

## STAGE 4 — Bottle line  → rubric: *Bottle filling*
Drag these PML blocks onto Main, left→right, and rename them clearly (rubric: neatness):

| # | Block | Key properties |
|---|---|---|
| 1 | **Source** `bottleSource` | New agent = **Bottle**; Arrivals defined by **Interarrival time** = `exponential(0.0814)`; *Actions ▸ On at exit:* `bottlesArrived++;` |
| 2 | **Conveyor** `bottleConveyor1` | Material Handling; draw the belt on the thin path; **Width 0.1 m**, **Speed 1 m/s**; "Agents... spacing" so a **visible gap** shows |
| 3 | **Delay** `filling` | **Capacity = 3** (max 3 bottles at once); Delay time = `normal(4.04, 11.89)`; *On exit:* `agent.filled = true;` |
| 4 | **Delay** `holdAfterFill` | Capacity large; Delay time = **2** seconds (the "wait 2 s before release") |
| 5 | **Conveyor** `bottleConveyor2` | thin, 0.1 m, 1 m/s → leads to the packing area; into a **Queue** `bottleQueue` |

Add a top-level `int bottlesArrived = 0;` variable on Main (used by Q3).

## STAGE 5 — Empty crate arrivals (Poisson)
| # | Block | Key properties |
|---|---|---|
| 6 | **Source** `crateSource` | New agent = **Crate**; Arrivals defined by **Rate** = **2.4 per minute** (rate-based Source = a Poisson process); → **Queue** `crateQueue` |

## STAGE 6 — Packing 6→1  → rubric: *Packaging* + *Crate queuing*
| # | Block | Key properties |
|---|---|---|
| 7 | **Assembler** `packing` | Inputs: **6** from `bottleQueue` + **1** from `crateQueue`; Output agent = **PackageFull**; Assembly (delay) time = `normal(2, 9)`; this enforces "crate leaves only when 6 bottles are in" |

*(The Assembler waits until 6 bottles AND 1 crate are available — exactly the "max capacity 6"
rule. The two Queues give the visible crate queuing the rubric checks.)*

## STAGE 7 — Crate conveyor + Weighing  → rubric: *Scale weighing updates* / *light indicator*
| # | Block | Key properties |
|---|---|---|
| 8 | **Conveyor** `crateConveyor` | **thick: Width 0.2 m**, Speed 1 m/s; visible gap; → weighing |
| 9 | **Service** `weighing` | **Capacity = 1** (one crate at a time); Seize time/Delay = **2** seconds; *On enter:* `agent.weight = uniform(5.0, 6.2); currentWeight = agent.weight;` |

Animation for the weighing station:
- Add Main variable `double currentWeight = 0;`. Add a **Text** on the scale in the layout, set its
  text to `String.format("%.2f L", currentWeight)` → updates every crate (rubric: scale updates).
- Add a small **oval**, fill **orange**, near the machine = "functional" light (always on).

## STAGE 8 — Accept / reject + live counts  → rubric: *Accepted/rejected count*
| # | Block | Key properties |
|---|---|---|
| 10 | **SelectOutput** `weightCheck` | Condition (true port) = `agent.weight >= 5.4` |
| 11 | **Sink** `accepted` | *On enter:* `acceptedCount++;` |
| 12 | **Sink** `rejected` | *On enter:* `rejectedCount++;` |

Main variables: `int acceptedCount = 0;  int rejectedCount = 0;`
Add two **Text** displays: `"Accepted: " + acceptedCount` and `"Rejected: " + rejectedCount`
(rubric wants both updating in real time).

---

## STAGE 9 — Run & read the answers  → rubric: *Model runs without crashing*
1. Run. It should flow: bottles fill (turn blue), pack 6-per-crate, weigh, split accept/reject.
2. Let it run to **18:00** (it auto-stops).

**Question 2 — proportion rejected (4 dp):**
add a Main display or read at the end:
```
rejectedCount / (double)(acceptedCount + rejectedCount)
```
Report to 4 decimals (e.g. `0.1xxx`). It should be **> 0.10**, matching the stated problem.

**Question 3 — bottles arrived:** read `bottlesArrived` (or `bottleSource.countOfArrivals()` if you
didn't add the counter). That's your answer.

> Seed is fixed at 1, so your numbers are reproducible and gradeable.

## STAGE 10 — Submission  → rubric: *Submitted file*
Zip together: the **`.alp`** (renamed `SemA02_<Surname>_<StudentNo>.alp`), the **layout image**, and
your **`.R`** (`fit_parameters.R` + the two histogram PNGs). Upload on clickUP under
*Industrial Analysis / Predictive modelling*. Put the Q2 and Q3 answers where clickUP asks.

---

## Rubric self-check before you submit
- [ ] Runs to 18:00 without crashing  - [ ] Scaled (0.1/0.2 m conveyors, real agent sizes)
- [ ] Bottles arrive empty, become full  - [ ] Crates queue with a visible gap
- [ ] 6 bottles packed per crate  - [ ] Scale shows live weight  - [ ] Orange light on
- [ ] Accepted & rejected both count live  - [ ] Blocks named neatly  - [ ] File named correctly

## Where you'll likely get stuck (tell me and we pair on it)
1. **Conveyors** — drawing the belt path on the layout and linking the Conveyor block to it.
2. **Assembler ports** — wiring 6-from-bottleQueue + 1-from-crateQueue.
3. **Scale calibration** — making model metres match the image.
Say the word and I'll give a zoomed-in, click-by-click for any of these three.
