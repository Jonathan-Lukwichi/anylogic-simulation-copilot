# Pattern card — Lorenz Weather Model - Pypeline
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Simulate and visualise the chaotic Lorenz attractor (a deterministic nonlinear system) while streaming live state data to an external Python/Matplotlib 3D plot via the Pypeline bridge.

## Block chain
Three coupled stock variables — X (convection rate), Y (horizontal temperature variation), and Z (vertical temperature variation) — evolve continuously through differential equations driven by three scalar parameters (S, B, R). Each stock's rate-of-change expression feeds directly into the other stocks, creating the feedback loops responsible for the system's signature butterfly-shaped attractor. At startup the Pypeline library spawns a separate Python process running Matplotlib; on every simulation step AnyLogic pushes the current (X, Y, Z) triple across the bridge, and Matplotlib redraws the 3D trajectory in real time. Sliders on the AnyLogic canvas let the user modify S, B, or R mid-run and immediately see the trajectory diverge or converge — a hands-on demonstration of sensitivity to initial conditions and parameter changes. The model is also designed to run correctly inside AnyLogic's parallel-experiment framework with no extra Pypeline configuration required.

## Resources
n/a — pure SD; no queues, resource pools, or agent populations.

## Key settings worth copying
- Stock X initial value: parameter `X0` (user-adjustable); Y₀ = 10; Z₀ = 20
- Parameters: S = 10 (Prandtl number), B = 8/3 (geometry factor), R = 28 (Rayleigh ratio) — the classic chaotic regime
- Model time unit: Day (dimensionless in practice; only the ODE coupling matters)
- Pypeline `PyCommunicator` object launches the Python subprocess and handles bidirectional data streaming; no manual socket code needed
- Parallel-simulation safe: Pypeline opens a distinct window per experiment replica automatically

## KPIs instrumented
- Live 3D phase-space trajectory of (X, Y, Z) rendered in Matplotlib — the visual KPI is the shape and divergence of the attractor
- No numeric throughput or wait-time KPIs; observation is qualitative (chaos onset, limit cycles, trajectory divergence)

## Reusable idea
The core trick is using Pypeline's `PyCommunicator` to stream simulation state to Python on every time step, enabling rich external visualisation (here, a live 3D Matplotlib plot) without any manual networking code — a pattern that can be repurposed to pipe AnyLogic output to any Python analytics, ML inference, or dashboard library in real time.
