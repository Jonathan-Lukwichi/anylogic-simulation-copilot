# Pattern card — Lorenz Weather Model
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD (System Dynamics — continuous ODE integration)
- **Problem it solves:** Demonstrates how a deterministic three-equation system produces unpredictable, chaotic trajectories, illustrating sensitivity to initial conditions in continuous-time models.

## Block chain
Three coupled stock variables — X (convective intensity), Y (horizontal temperature variation), and Z (vertical temperature variation) — evolve simultaneously through custom differential equations. Each stock's rate of change depends on the current values of the other two stocks and three scalar parameters (S, R, B). The solver advances all three stocks each time step using the Euler method, accumulating a trajectory through a three-dimensional state space. Because the equations are nonlinear, tiny differences in starting values cause paths to diverge exponentially, tracing the famous butterfly-shaped Lorenz attractor.

## Resources
No queues, agents, or resource pools. The model is purely continuous: three stock variables and four scalar parameters (S = Prandtl number, R = Rayleigh number, B = geometric factor, X0 = initial condition for X). Y and Z are initialised at fixed constants (10 and 20 respectively).

## Key settings worth copying
- **Parameters:** S (default ~10), R (default 28), B (default 8/3) — these classic values are the boundary at which chaos emerges; varying them away from this set collapses the attractor into a stable spiral.
- **Initial condition X0:** exposed as a parameter so experiments can test sensitivity — nudging X0 by even 0.001 eventually produces a completely different trajectory.
- **ODE solver:** Euler method; time unit is Days (purely nominal — the equations are dimensionless).
- **Visualisation:** a time-plot showing X, Y, Z over simulation time plus two phase-portrait plots (X vs Y and X vs Z) that together reveal the attractor shape.

## KPIs instrumented
- Time-series traces of all three state variables.
- Phase-portrait plots (XY plane, XZ plane) used as the primary diagnostic — the attractor shape itself is the output of interest rather than a scalar KPI.

## Reusable idea
Expose a single initial-condition parameter and run multiple replications with micro-perturbations to demonstrate chaos or, conversely, robustness. The same pattern applies to any nonlinear SD model (epidemic SIR, supply-chain oscillation, predator-prey) where you want to visualise how sensitive long-run behaviour is to starting state — just add a phase-portrait plot and a parameter slider for the initial value.
