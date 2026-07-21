# Pattern card — Emergency Department

- **Source:** AnyLogic example library, `models/Emergency Department` (PLE 8.9 built-in). Distilled in original wording — not a copy of the .alp/Java.
- **Paradigm:** DES (Process Modeling Library), with a 2D/3D facility layout driving movement.
- **Problem it solves:** how a patient flows through an ED across several specialised resource types (staff, rooms, portable equipment), and how long they stay (length of stay).

## Block chain
Source (patient arrivals, by **rate**) → register/wait → MoveTo (escorted to a triage room) →
Seize triage room + Nurse → Delay (triage) → Release → MoveTo (express-care room) → Seize EC room
→ SelectOutput (branch: X-ray vs ultrasound) → one of two **hierarchical sub-processes**
(`XRayProcess` / `USoundProcess`) → Release resources → Sink (discharge).
TimeMeasureStart/End wrap the whole stay to record **length of stay** as a histogram.

The two imaging paths differ in *who moves*: for X-ray the **patient travels** to the X-ray room;
for ultrasound the **portable device is moved** to the patient's EC room. This is the model's
signature teaching point.

## Resources
ResourcePools by behaviour type:
- **Moving** (can relocate themselves): Nurses, PAs, Technicians.
- **Static** (fixed location): Triage rooms, Express-care rooms, X-ray room.
- **Portable** (moved by a moving resource): Ultrasound devices.

Resources are handled with explicit **Seize / Release** pairs (not the all-in-one Service block),
which is what lets the model attach staff + room + equipment in different combinations per step.
Technicians run their own ResourceTaskStart/End sub-process to prep before and wrap up after an
ultrasound.

## Key settings worth copying
- Model time unit: **minutes**.
- Arrivals: Source set to **arrival rate** (rate-based, supports a rate schedule for day/night swing).
- Service durations: simple bounded distributions — e.g. `uniform(...)` and `triangular(min, mode, max)`
  in minutes (triage/imaging steps). Distilled examples seen: `triangular(0.5, 1, 1.5)`,
  `triangular(5, 8, 15)`, `uniform(2.5, 3.3)`.
- Movement is **markup-driven**: paths, nodes and attractors drawn on the facility layout define
  where Seize/MoveTo send agents — geometry, not abstract delays, produces walking time.
- Hierarchy: imaging logic lives in separate flowchart blocks (`XRayProcess`, `USoundProcess`),
  keeping `Main` readable — a clean template for any multi-station service.

## KPIs instrumented
- **Length of stay** (TimeMeasureStart→End histogram, Source→Sink).
- Implicit/extendable: resource utilisation per pool (staff, rooms, ultrasound), queue/wait at each
  Seize, throughput, % discharged within target.

## Reusable idea
Model **distinct resource behaviours** (moving / static / portable) with separate ResourcePools and
explicit Seize/Release, and let **layout markup drive movement** so travel time emerges from geometry.
Branch shared steps into **hierarchical sub-processes** instead of one flat flowchart — the same shape
scales to any clinic, workshop, or service hall where who-moves-to-whom matters.
