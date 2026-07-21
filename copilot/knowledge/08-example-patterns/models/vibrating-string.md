# Pattern card — Vibrating String
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics — continuous differential equations via Finite Element Method)
- **Problem it solves:** Simulates the wave-like oscillation of a physical string under external periodic forcing, capturing distributed displacement and velocity along its length.

## Block chain
The model discretises the string into a series of finite elements. Each element carries two array-based stock variables — one for positional displacement and one for velocity — linked by custom differential equations that encode the wave PDE. A Flow variable drives the rate of change between displacement and velocity for every indexed node. Boundary conditions fix the endpoints, while interior nodes couple to their immediate neighbours so that forces propagate spatially step by step across the array.

## Resources
n/a — no process-flow resource pools; the "resources" are the N array slots (range-type dimensions) representing string nodes.

## Key settings worth copying
- **Array / range dimensions:** every stock and flow is subscripted over a Range dimension, letting a single equation template cover all nodes — copy this pattern for any spatially distributed SD model.
- **Custom equation style:** stocks use `EquationStyle = custom` rather than the built-in inflow/outflow wiring, giving full control over second-order ODE terms.
- **Solver:** Euler method selected (`DifferentialEquationsMethod = EULER`); RK45-Newton and Modified-Newton are also configured for algebraic/mixed systems.
- **Interactive sliders:** damping coefficient, stiffness, and external force frequency are runtime-adjustable parameters — ideal for parameter-sweep demos.
- **Model time unit:** Day (used as a neutral continuous time base; rescale to seconds/ms for real physical problems).

## KPIs instrumented
- Displacement profile along the string (spatial snapshot at each time step)
- Velocity profile along the string
- Visual animation showing wave propagation shape in real time

## Reusable idea
**Subscripted stocks over a Range dimension as a cheap spatial grid.** Instead of building separate agents or objects for each node, a single pair of array stocks (displacement[i], velocity[i]) with neighbour-referencing equations (`i-1`, `i+1`) turns AnyLogic SD into a 1-D finite-element solver. This same trick applies to heat diffusion, traffic flow on a road segment, or any PDE that can be spatially discretised on a line.
