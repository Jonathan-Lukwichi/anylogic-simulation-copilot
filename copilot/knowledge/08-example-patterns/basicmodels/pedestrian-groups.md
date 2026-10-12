# Pattern card — Pedestrian Groups
- **Source:** AnyLogic example model "Pedestrian Groups" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM/DES (Pedestrian Library)
- **Problem it solves:** Model people who walk together (families, tour groups, friends) — three ways to form groups, change their formation on the way, and split them up again.

## Block chain
A radio button picks one of three group-creation modes (the other sources get rate 0):
1. `PedSource` with **Create groups** (`groupSize = uniform_discr(5, 10)`, members arrive `exponential(5)` s apart, formation *front*); its rate is `pedRateToGroupRate(defaultRate)` = peds/h ÷ 7.5 (mean group size).
2. Individual `PedSource` → `PedGroupAssemble` (groups of 5–10 formed in `areaAssemble`, formation *front*; its `ccl` port routes cancelled pedestrians straight to the exit).
3. Process-Modeling `Source` + `MoveTo` (agents outside pedestrian space) → `PedEnter` with **Create groups** (groups formed on entering pedestrian space).
Then all: `PedGoTo` → `PedGroupChangeFormation` → `PedSelectOutput` (conditions) → either directly to the exit, or `PedGoTo` → `PedGroupDisassemble` → `PedGoTo` exit → `PedSink`. A `PedSettings` block is used to highlight one group leader (`configuration.selectPed(group.getLeader())` in *On end grouping*).

## Resources
n/a

## Key settings worth copying
- Formations: `GROUP_FORMATION_FRONT` (walk abreast), `…_CHAIN` (single file), `…_SWARM` (loose cluster); change mid-route with `PedGroupChangeFormation` (e.g. chain in corridors, front in halls).
- `PedGroupAssemble` forms a group when the size is reached, when a timeout expires, or when the gap between arrivals exceeds a threshold (Help); `cancel` sends members out through the emergency `ccl` port.
- With *Create groups* on, the PedSource **rate counts groups** — divide the pedestrian rate by the mean group size to keep throughput comparable (as `pedRateToGroupRate` does).
- *On end grouping* gives the `group` (e.g. `group.getLeader()`); `PedSettings.selectPed(ped)` / `deselectPed()` highlight one pedestrian for tracing.

## KPIs instrumented
Visual only.

## Pitfalls
- Forgetting the rate conversion multiplies the crowd by the group size (here ×7.5).
- Group members do not keep social distance from each other (Help, *PedSettings*) — density and distancing KPIs inside groups are not comparable with singles.
- Groups must be disassembled before blocks that should treat members individually; place `PedGroupDisassemble` where the group really breaks up.

## Reusable idea
Represent social groups explicitly when they change bottleneck behaviour (wider fronts, slower chains, joint waiting); choose the creation point by data: at arrival (PedSource), when people gather (PedGroupAssemble), or when they enter the modelled space (PedEnter).

## When the co-pilot should use this
Visitor attractions, airports (families), stadium ingress, evacuation studies where groups move together, and whenever a user's pedestrian counts look ×N too high after turning groups on.
