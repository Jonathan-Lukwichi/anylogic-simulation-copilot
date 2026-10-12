# Pattern card — Interactive what-if tools: instant re-run charts and a step-pause management game
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 5 "System dynamics" (§5.5, Examples 5.4–5.5) — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Stakeholders want to move a lever and see the whole trajectory redrawn at once, or to run a policy period by period like a game, without a modeller driving the IDE.

## Mechanism
Checked against the 8.9.10 book models *Epidemic Model - Various Experiments* and *Stock Management Game*, Help 8.9.10
(*Compare runs experiment*, *Engine API*) and the engine Javadoc.

**A. Instant charts** (a Compare Runs experiment named `InstantCharts`):
1. On Main, give each stock to show an auto-updating dataset (e.g. `InfectiousDS`).
2. Create a Compare Runs experiment over the levers. Each lever's parameter uses a *Slider* in its Value editor, with
   ranges.
3. In each slider's Action, set the parameter and start a run: `Infectivity = value; run();`. The book notes this run
   goes at full speed with animation off (p. 43).
4. In the experiment, add datasets with the same names, using time rather than the run number on the x-axis.
5. In *After simulation run*, copy the run's data across: `InfectiousDS.fillFrom(root.InfectiousDS);`, one line per
   dataset. `fillFrom` makes an exact copy (Javadoc 8.9.10). A Plot with its items set to *Data set* shows them.
6. Result: every slider move re-simulates the whole horizon and redraws. This suits models that run in well under a
   second.

**B. Step-pause game** ("flight simulator"):
1. **Inputs from outside.** The player's lever (`OrderRate`) and the exogenous driver (`Demand`, a daily random walk
   written by a Cyclic event) are Constant dynamic variables. The sales flow is gated by the stock.
2. **Player screen.**
   - Place a view area below the model frame (y = frame height) holding only the chart and the controls.
   - Show it from Main's On startup: `viewUserScreen.navigateTo();`.
   - In the experiment's *Window* section, untick *Enable zoom and panning* and *Enable developer panel*.
3. **Period end.** A Cyclic event, first at 50 days and then every 50 days, runs `pauseSimulation();`.
4. **Decision.** Enable the slider and a "Done" button only when `getEngine().getState() == Engine.PAUSED`. The
   button's action is `runSimulation();`.
5. **Pace.** Use Virtual time for step-pause play. For continuous play, use real time with a scale; the book uses
   50 (p. 46).

## Resources
n/a

## Key settings worth copying
- `pauseSimulation()` acts only while RUNNING, and `runSimulation()` only while PAUSED. Both are Agent functions
  (Javadoc 8.9.10). `Engine.PAUSED` is an `Engine.State` constant.
- The Compare Runs `run()` starts the experiment, creating the model if none exists (Help). *After simulation run*
  executes when the engine finishes a run, but not when a run is terminated from the toolbar.

## KPIs instrumented
The player's stock trajectory, plus (suggested) a dataset of each decision logged at every pause for the debrief.

## Pitfalls
- **A slider linked to an ordinary dynamic variable does nothing.** Its formula overwrites the value. Link to a
  Constant variable or a parameter (`bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`).
- **Stochastic models:** each slider move is one run. Fix the seed for the instant view, and use replicated experiments
  for any number you report (G16, G17).
- **Mid-run play is not reproducible** (G17). Log the decisions if the session is to be analysed.
- **Web delivery:** Cloud does not upload desktop experiment pages and does not run their set-up code (G49). Keep the
  game logic on Main, as here; Cloud's own experiment comparison covers the instant-chart use.

## Reusable idea
Separate what the player sees (a view area with a few controls) from the model, gate every control on the engine
state, and re-run a fast model on each change when the whole trajectory is the message.

## When the co-pilot should use this
- Management flight simulators and teaching games (stock management, beer-game style); stakeholder workshops on
  feedback and delays; exploring SD parameters live.
- Not for estimates. Use Parameter Variation or Monte Carlo experiments with replications for those.
- Related: `videos/cloud-decision-tool-for-stakeholders.md`, `videos/experiment-page-pre-run-controls.md`.
