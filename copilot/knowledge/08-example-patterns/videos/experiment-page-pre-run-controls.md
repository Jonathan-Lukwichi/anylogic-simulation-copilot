# Pattern card — Pre-run controls on the experiment page (inputs the model consumes while it is built)
- **Source:** AnyLogic video "Setting up parameters from the experiment page" (https://youtu.be/pd8QMBL-ri4) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Let a user pick inputs that are read while the model is built (population size, layout or scenario id) before each run, without editing the model.

## Mechanism
- **Where the controls live.** On the Simulation experiment's own diagram — its start page — not on Main. The page is shown before Main exists; Main is created when Run is pressed, and Stop returns to the page for the next choice. Demo: a slider (maximum 250) choosing `numberOfElephants` (int) in the Wandering Elephants example (`models/wandering-elephants.md`).
- **Why *Link to* cannot reach Main from there.** A control's *Link to* lists only the parameters, variables and blocks of its own diagram (Help 8.9.9, *Slider*), and Main does not exist yet.
- **Two bindings**, both through the experiment's **Parameters** section, which sets Main's parameters once, when Main is created:
  1. The Help's way: type the control's getter in the parameter's field, e.g. `slider.getIntValue()`.
  2. The video's way: link the slider to an experiment-level Variable (`sliderValue`, int, initial value 50 — a linked slider starts at the variable's value) and type `sliderValue` in the field.
- **Show the page.** Untick *Skip experiment screen and run the model* in the Simulation experiment's properties. New models have it ticked by default since AnyLogic 8.6 (release notes).

## Resources
n/a

## Key settings worth copying
| Control | Getter for the Parameters field (Help 8.9.9) |
|---|---|
| Check box | `isSelected()` (boolean) |
| Edit box | `getText()`, `getDoubleValue()` or `getIntValue()` |
| Radio buttons | `getValue()` (int, first option = 0) |
| Slider | `getValue()` (double) or `getIntValue()` |
| Combo box, list box | `getValue()` (String) |

Overridden parameters appear in bold in the Parameters section.

**Pre-run or runtime knob?**
| Input | Where it belongs |
|---|---|
| Read once while the model is built: initial population size, layout or scenario id, which table to load, arrays sized at startup | Experiment page (desktop) or a Run Configuration input (Cloud) |
| A policy that may change mid-run: a service-time mean, a capacity whose On change calls `set_capacity()` | A control on Main with *Link to* (`models/airport.md`); for statechart agents see `videos/statechart-live-controls-trigger-reevaluation.md` |

**Cloud.** Desktop experiments, their pages and their Parameters overrides are not uploaded to Cloud (Help, *Exporting a model to AnyLogic Cloud*). There the knob is a Run Configuration input, and its label and control type come from the parameter's **Value editor** section — the same settings that drive Compare Runs' generated UI (*AnyLogic in 3 Days* p. 94). Set the Value editor once and every venue offers the same control.

## KPIs instrumented
n/a. Echo the chosen inputs on Main (a text shape or an `Output`) so every screenshot and export records its scenario.

## Pitfalls
- The page is skipped (the 8.6+ default) and the controls never appear.
- A slider on Main linked to a construction-time parameter changes the value after the population already exists, so nothing visible happens (unless its On change code adds or removes agents).
- A slider returns a double; an int parameter needs `getIntValue()`.
- Linking is one-way, control to variable (Help, *Linking controls*): code that changes the variable does not move the slider.
- Only this Simulation experiment reads the page. Parameter Variation, Monte Carlo, Optimization and Cloud set the parameters their own way.

## Reusable idea
Split the knobs by when the model reads them: structure before the run (experiment page or Cloud inputs), policy during the run (controls on Main). Changing inputs between runs rather than mid-run also keeps runs reproducible (G17).

## When the co-pilot should use this
- A demo, supervisor or client should "choose the number of X" or "pick the scenario" before pressing Run.
- "I moved the slider and the population didn't change."
- A deliverable that runs both on the desktop and in Cloud: configure each lever's Value editor first.
