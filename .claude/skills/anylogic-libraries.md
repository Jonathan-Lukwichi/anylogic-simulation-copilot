---
name: anylogic-libraries
description: Map of every AnyLogic 8.9 library and palette - Process Modeling, Pedestrian, Material Handling, Fluid, Rail, System Dynamics, Agent components, Statecharts, Analysis, Controls, Presentation - what each is for, its key blocks, the properties that matter, and how to configure any block correctly. Use when choosing a library or configuring an unfamiliar block.
---

# anylogic-libraries

The library map + the universal configuration method. Pick the library by WHAT MOVES in your
system; configure any block with the same 5-step routine.

## The universal block-configuration routine (works on every block)
1. **Name it meaningfully immediately** (`triage`, not `service1`) — names become code references.
2. **Identify which properties are code fields**: most accept Java expressions; fields evaluated
   per-agent expose the keyword `agent` (e.g. Delay time `agent.triage.equals("P1") ? ... : ...`).
3. **Check the `=`/expression toggle** on each property you set — static value vs dynamic expression.
4. **Open ALL sections** (Advanced, Priorities/preemption, Actions, Specific): defaults hide
   behaviour (Task priority defaults 0 = FIFO; Forced pushing on Source floods models).
5. **Wire the Actions** (On enter / On exit / On seize…): the safe pattern is *write state
   upstream (On exit), read downstream* — conditions are evaluated at preview, before On enter.

## Library selector — by what moves
| What moves | Library |
|---|---|
| Generic entities through queues/services (patients, orders, calls) | **Process Modeling** |
| People walking with physics (corridors, crowding, evacuation) | **Pedestrian** |
| Goods via conveyors/AGVs/cranes/storage | **Material Handling** |
| Liquids/bulk (tanks, pipes, blending) | **Fluid** |
| Trains on tracks | **Rail** |
| Aggregate stocks & feedback (no individuals) | **System Dynamics** |
| Road vehicles on networks | **Road Traffic** |

## Process Modeling Library (the DES workhorse — see anylogic-des for method)
- Core: **Source** (arrivals: rate/interarrival/inject; Forced pushing OFF), **Sink** (`count()`),
  **Queue** (capacity, priority), **Delay** (time expr; "Until stopDelay()"), **Service**
  (queue+seize+delay+release in one; Resource sets; Task priority), **SelectOutput / 5** (routing —
  decide upstream), **Hold** (gate), **Match/Split/Combine/Assembler** (synchronise/join),
  **MoveTo** (travel along markup), **ResourcePool** (capacity, shifts, `utilization()`).
- Space markup: Point/Rectangular/Polygonal Node, Path, Attractor — set blocks' Agent location
  for animation (2D dots / 3D people).
- Properties that bite: queue capacity defaults, priority defaults (0), resource "units of same
  pool" vs "alternative resource sets", Agent type of each block's flow.

## Pedestrian Library
- Physical walking with collision/density — corridors, malls, stations, evacuation.
- Blocks: Ped Source / Ped Go To / Ped Service (with lines/areas) / Ped Wait / Ped Sink.
- Markup: Walls (also used for 3D buildings), Target Lines, Service With Lines, Areas,
  Escalators, Pathways; **Density Map** for congestion heat.
- Choose it only when walking/space itself is the question — it is much heavier than Process
  blocks. A hospital FLOW study = Process library; a hospital CORRIDOR-design study = Pedestrian.

## Material Handling Library
- Factories/warehouses: **Conveyor** (+spurs, transfer tables, turntables), **Station**
  (processing on conveyor), **AGV/Transporter** with Move By Transporter, **Storage/Racks**
  (place/retrieve), Jib/Overhead **Cranes**, **Lift**.
- Use with Process blocks (Convey, Store, Retrieve bridge them). Markup defines the physical
  network; transporters need speeds, capacities, dispatching policy.

## Fluid Library
- Continuous quantities: **Tank** (level), **Valve** (rate control), **Pipeline**, Fluid
  Source/Dispose, Fluid Select/Split/Merge, **Agent↔Fluid converters** (batch a flow into
  entities and back). For refineries, water, grain, high-volume "counting is pointless" goods.

## Rail Library
- Train Source/MoveTo/Couple/Decouple, railyard track/switch markup. Niche; combine with
  Process blocks for loading logic.

## System Dynamics palette (see anylogic-sd for method)
- **Stock, Flow, Dynamic Variable (auxiliary), Link, Parameter, Table Function, Loop label,
  Shadow, Dimension** (array SD). Flows are per-model-time-unit — rescale rates to your time unit
  or results are silently wrong ×24.

## Agent palette (the glue of every model)
- **Parameter** (config; supports value-editor controls: slider, edit box, radio, combo),
  **Variable** (state), **Collection** (lists/maps), **Function** (returns + args — the reuse
  unit), **Event** (cyclic/timeout/condition — the workhorse for periodic logic),
  **Dynamic Event** (many scheduled instances), **Table Function** (empirical curves),
  **Schedule** (calendar patterns: shifts, opening hours), **Custom Distribution** (empirical
  sampling), **Port/Connector** (block wiring), **Link to agents** (agent communication).
- Population sizes accept parameters — the key to reusable/framework models.

## Statechart palette
- Statechart Entry Point, State, Transition (triggers: timeout, rate, condition, message,
  arrival), Branch, Initial/Final/History state.
- Use for genuinely event-driven mode changes (machine Idle→Busy→Failed, patient
  deteriorating), message-driven behaviour, interrupts. For "update everyone daily", a cyclic
  Event loop is simpler (see anylogic-abm).

## Analysis palette
- Data: **Data Set** (x,y pairs; construct via the palette element, not `new DataSet(int,bool)` —
  PLE lacks that constructor), **Statistics** (mean/deviation/count; NO `confidence()` in PLE —
  compute t·s/√n manually), **Histogram Data**, **Output**.
- Charts: **Plot** (DataSet vs index), **Time Plot** (value vs sim time), **Bar/Stack/Pie**,
  **Histogram**, Time Stack/Color. Match chart type to data shape; uniform sizes per row.

## Controls palette
- **Button** (Label + Action code), **Slider / Edit Box** (link to parameter; edit box = typed
  numeric input for frameworks), **Check Box, Radio Buttons** (policy selectors), **Combo Box**,
  **Text Field**. Parameter value-editor "Control type" can generate these automatically.

## Presentation palette
- Rectangle/Rounded/Oval/Line/Polyline/Curve, **Text**, **Image**, **Group**, **View Area**
  (navigation bookmarks), **3D Window**, **Camera**, **Scale**, CAD drawing import.
- Full method: `anylogic-2d` (design system) and `anylogic-3d` (3D layer).

## Cross-library gotchas
- Every library block ultimately holds Java expressions — the `agent.` keyword, the `=` toggles,
  and the upstream-write rule apply everywhere.
- Experiments override Main parameter defaults (set scenario values in the experiment).
- PLE caps: 50k agents; some constructors/methods absent (DataSet, confidence()).
- Mixing libraries is normal and intended: Process + Material Handling + SD in one model is a
  standard hybrid — bridge via shared functions and variables on Main.
