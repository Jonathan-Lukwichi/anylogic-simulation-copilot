# Pattern card — Machine Optimizer
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES (static / no time-driven events; model time unit: Second)
- **Problem it solves:** Find the optimal mix of three machine types to minimise total production cost, subject to a fixed total-machines-built constraint, by calling a Python linear-programming solver at runtime from inside AnyLogic.

## Block chain
The model is non-process-flow; it has no Source→Sink chain. Instead:
1. A user fills in parameter fields in the model UI (costs per machine type, capacity contributions, allotted machines budget).
2. Clicking a button fires Java/AnyLogic code that calls **PyCommunicator** (from the Pypeline add-on library) to open a Python session.
3. The code pushes parameter values into Python, runs `scipy.optimize.linprog` to solve the linear programme, then pulls the optimal machine-count vector back out via Output objects.
4. Results are displayed on the model canvas — no simulation clock advance occurs.

## Resources
n/a — no AnyLogic ResourcePool or agent population. The "resources" in domain terms are three machine types whose quantities are the decision variables (x1, x2, x3).

## Key settings worth copying
- **Decision variables:** integer counts of three machine types summing to `allottedMachinesBuilt`.
- **Objective:** minimise `costProduceType1·x1 + costProduceType2·x2 + costProduceType3·x3`.
- **Constraint matrix:** equality constraint `A_eq · [x1, x2, x3] = allottedMachinesBuilt` (each machine type counted as 1 unit).
- **Python solver:** `scipy.optimize.linprog` with `numpy` array helpers; requires Python 3 + numpy + scipy on the host machine.
- **Pypeline bridge:** `PyCommunicator` block; check import success with `Attempt` and raise an `error()` if numpy/scipy are missing.
- **Model time unit:** Second (irrelevant here since no events fire, but must be set).

## KPIs instrumented
- Minimised total production cost (scalar, displayed on canvas after solve).
- Optimal number of each machine type (three output values pulled from Python result object).

## Reusable idea
Embed a Python mathematical optimisation call (scipy linprog, or any other solver) inside an AnyLogic button action via Pypeline's PyCommunicator; pass AnyLogic parameters in, retrieve the optimal solution out, and display results on the canvas — turning the AnyLogic UI into a lightweight front-end for Python-powered optimisation without leaving the simulation environment.
