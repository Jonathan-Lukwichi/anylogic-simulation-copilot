# Pattern card — Multi-level facility: level Z from scale, lift landings, choosing the level-crossing element
- **Source:** AnyLogic video "How to simulate multi-level facilities" (https://youtu.be/IpSr9CDVGz0) — distilled, original wording
- **Paradigm:** DES (Material Handling Library, path-guided transporters)
- **Problem it solves:** Move AGVs between floors through a timed, capacity-limited lift, with the floors placed correctly in 3D and lift timing consistent with the building's real heights.

## Mechanism
In the video, an AGV fetches items from racks on `firstFloor` and delivers them to workstations on a new `groundFloor` 5 m below. The flowchart is unchanged except for a dynamic destination.
1. **Add the level.** Use the Levels widget along the editor's lower edge, and name the level `groundFloor`.
2. **Place it in Z.** Level Z (px) = floor-to-floor height (m) × scale (px/m), negative for floors below the reference. At 20 px/m, a floor 5 m below gives Z = −100. An element's own Z is *relative* to its level's Z (Help 8.9).
3. **Build the floor network** (paths and point nodes) on that level. Collect the target nodes in a collection `workstations`. Set MoveByTransporter's Node, as a dynamic value, to `randomFrom(workstations)`. One MoveByTransporter then reaches nodes on the other floor, and routing through the lift is automatic.
4. **Place one Lift element per level.** Each one is a *landing*.
   - `firstFloorLift`: tick **Main landing (defines lift properties)**.
   - `groundFloorLift`: set **Floor elevation** = −5 (m) and **Refers to** = `firstFloorLift`.
5. **Connect paths to the lift's port.** Drag the path end onto the port until it highlights green.

## Resources
The transporter fleet is unchanged. The lift is a resource in its own right: it carries **one** transporter or material item at a time, and the others queue (Help 8.9).

## Key settings worth copying
- **The main landing holds every lift parameter:** Lifting speed, Picking up time, Dropping off time, and Agent selection pattern (FIFO by default, or Priority-based / Agent comparison). The other landings inherit these.
- **Every landing needs a Floor elevation.** It is a length with units, measured from one reference plane you choose (here the first floor = 0). AnyLogic computes lift travel time from these values.
- **Landings on different agents' diagrams:** switch *Refers to* to the dynamic editor and type `<agent>.<lift>`. Paired network ports use the same trick. *Beyond the video.*
- **Runtime API** (Help 8.9): `fail()` / `repair()` / `isFailed()` for lift breakdowns, plus `setLiftingSpeed(v, units)`, `getLiftLandings()` and `getMainLanding()`.
- **Choosing the level-crossing element** (Help 8.9, *beyond the video*):

| Mover | Element to use |
|---|---|
| Path-guided transporter, or conveyor material item | **Lift** landings, or paired **Network ports** |
| Free-space transporter | Paired **Level gates** (`basicmodels/level-gate.md`), or a Lift (enterable from any side) |
| Pedestrian | PedChangeLevel + target lines, or the **Elevator** markup. A Lift cannot carry pedestrians. |

  Only Lift and Elevator model vertical travel time and car capacity. Ports and gates just join networks or levels. *(That they add no delay is unverified.)*

## KPIs instrumented
The video has none. Suggested:
- AGV time spent waiting for the lift, from the landing queue.
- Cross-floor trip time.
- A single shared shaft is a classic hidden bottleneck, so test the fleet size against lift capacity.

## Pitfalls
- **Level Z and Floor elevation are independent.** Level Z (pixels) only positions the drawing. Floor elevation (metres) drives lift timing. If you edit one and not the other, the 3D view and the travel times silently disagree. Keep them in step: −100 px ↔ −5 m at 20 px/m. The px↔m conversion is also in `videos/spiral-conveyor-per-point-z.md`.
- **A path that touches the lift is not connected to it.** Only the green port highlight means a join. A lift with no connected paths is unreachable.
- **Don't add levels for show.** Help 8.9 advises staying on one level unless floors really exist.
- **Walls here are decoration.** Path-guided AGVs follow the network. Walls obstruct only pedestrians and free-space transporters. So does the lift, but only when its *Is obstacle* option is on.

## Reusable idea
Model each floor as a level with a physically derived Z. Model each vertical transport as a small shared server: a lift when vertical contention matters, and ports or gates when it does not. A dedicated "navigation" level that holds the UI bar keeps controls out of the way while you edit floors, because elements on other levels cannot be selected.

## When the co-pilot should use this
- **Use cases:** warehouses with mezzanines, multi-storey hospitals or factories, and AGV or tote systems with vertical lifts.
- **Related cards:** `models/material-handling-in-hospital.md` (free-space transporters with lifts) and `basicmodels/level-gate.md`.
- **3D presentation:** for floor slabs and Z ordering, see `videos/3d-scene-z-order-and-lighting.md`.
