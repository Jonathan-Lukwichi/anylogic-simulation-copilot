# Pattern card — Three Body Problem
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics — continuous ODE integration via StockVariables)
- **Problem it solves:** Simulates the gravitational interaction of three equal-mass celestial bodies moving in 2-D space, reproducing a known stable choreographic orbit discovered by R. Montgomery.

## Block chain

There are no process-flow blocks. The model is built entirely from **StockVariable** elements (AnyLogic's continuous-state integrators). For each of the three bodies the model maintains four stocks: position (x, y) and velocity (vx, vy). Each position stock's rate-of-change is the corresponding velocity stock; each velocity stock's rate-of-change is the gravitational acceleration (ax, ay) computed from the current pairwise distances to the other two bodies. This gives 12 coupled first-order ODEs that AnyLogic integrates over time (time unit: minutes).

The acceleration variables (ax1/ay1, ax2/ay2, ax3/ay3) are plain auxiliary variables that evaluate Newton's law each time step using the current stock values, closing the feedback loop.

Three XY DataSets collect the (x, y) trajectory of each body and are plotted on a phase-space chart so the figure-eight orbit becomes visible.

## Resources

n/a — no queues, servers, or agent populations. The only shared "resource" is the gravitational constant G embedded in the acceleration expressions.

## Key settings worth copying

- **StockVariable as integrator:** set `Expression` = rate variable, `InitialValue` = known starting condition. This pattern cleanly separates state from derivative.
- **Symmetric initial conditions:** body 1 starts at (x10, y10) with velocity (-vx30/2, -vy30/2); body 2 mirrors body 1 at (-x10, -y10); body 3 starts at origin with velocity (vx30, vy30). This symmetry is what produces the closed choreographic orbit.
- **Time unit = Minute** — physical constants must be scaled consistently to this unit.
- **SamplesToKeep = 100** — limits memory use for trajectory datasets while still showing the full loop.

## KPIs instrumented

- Trajectory plot: phase-space (x vs y) for each of the three bodies — the key visual confirming orbit stability.
- No throughput, utilisation, or wait-time metrics; the output is purely geometric/dynamic.

## Reusable idea

**Use StockVariable chains to integrate any ODE system.** The pattern position-stock ← velocity-stock ← acceleration-auxiliary applies to any Newtonian or kinematic simulation (robots, vehicles, projectiles). Defining initial conditions symmetrically and collecting (x,y) pairs in a DataSet for a phase-plane chart is a compact, reusable recipe for validating continuous-dynamics models against analytical solutions.
