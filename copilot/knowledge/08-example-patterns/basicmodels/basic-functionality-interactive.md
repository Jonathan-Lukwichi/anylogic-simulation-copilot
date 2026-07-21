# Pattern card — Basic Functionality (Interactive)
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** Hybrid (SD fluid sub-model driven by Python-computed values; interactive demo harness)
- **Problem it solves:** Teach how to call Python scripts and expressions from a live AnyLogic model using the Pypeline add-on, and feed the results back into simulation logic at runtime.

## Block chain
The model is organised as a gallery of interactive demos rather than a single linear flow. A central `PyCommunicator` object manages the Java-to-Python bridge. Each demo panel lets the user type a command or fill a form; the model passes that input to Python via `pyCom.run(...)` or `pyCom.runFile(...)`, captures the `Attempt` return object, and uses `attempt.getFeedback(SomeClass.class)` to pull the result back into Java/AnyLogic.

One concrete sub-demo drives a small fluid network: `FluidSource` injects an amount computed by Python into a `Tank`; `Valve` blocks regulate outflow through `BulkConveyor` belts; a `FluidDispose` drains overflow. The injection amount is obtained by executing a bundled Python script (`my_distribution.py`) that draws from a triangular-like custom distribution parameterised by min, mode, and max values the user sets interactively.

## Resources
- `PyCommunicator` — the single add-on object that spawns and communicates with the Python process (configurable as `python`, `python3`, a named alias, or an explicit executable path).
- `FluidSource / Tank / Valve / BulkConveyor / FluidDispose` — AnyLogic fluid library objects used as a live visualisation target for Python-generated numeric inputs.
- External Python environment with `numpy` and `scipy` installed.

## Key settings worth copying
- **Python command type:** selectable at runtime from four options (PYTHON, PYTHON3, PYTHON_OTHER with alias, PYTHON_PATH with full path) — makes the model portable across environments without recompilation.
- **`pyCom.run(format, args...)`** — executes an inline Python snippet; auto-generates readable sample code shown on screen so learners can copy the pattern.
- **`pyCom.runFile("my_distribution.py", arg1, arg2, arg3)`** — runs an external `.py` file co-located with the `.alp`; arguments are passed as command-line strings.
- **`attempt.getFeedback(double.class)`** — typed extraction of a Python return value back into Java; use the correct Java class (double, int, String, etc.).
- **Model time unit:** Second.
- **Fluid flow rate unit:** CUBIC_METER_PER_SECOND (used for Tank capacity and Valve throughput).

## KPIs instrumented
- Live fluid level in the Tank (visual gauge) reflects Python-computed injection amounts.
- Console/log panel displays raw stdout from each Python call for debugging.
- No formal statistical KPIs (throughput, wait time) — this is a learning/demo model, not a production analytics model.

## Reusable idea
The transferable trick is the **runtime-configurable Python bridge pattern**: bundle a `PyCommunicator` with four selectable invocation modes, call `.run()` for inline snippets or `.runFile()` for script files, and always inspect the `Attempt` object before extracting feedback. This lets any AnyLogic model off-load heavy numeric work (distributions, ML inference, optimisation) to Python without requiring a fixed Python installation path — the end user picks the right command type from a dropdown at startup.
