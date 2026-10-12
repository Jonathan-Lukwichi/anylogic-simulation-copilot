# Pattern card — Runtime controls: which way a link flows, keeping controls and parameters in step, replicated controls
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 13 "Designing interactive models: using controls" — distilled, original wording
- **Paradigm:** Method (interaction; any paradigm)
- **Problem it solves:** Sliders and buttons that disagree with the parameter they drive, *On change* code that never runs, bad typed input, and replicated controls that lose state or throw at startup.

## Mechanism
Checked against Help 8.9.10 (*Linking controls*, *Slider*, *Edit box*, *List box*, *File chooser*, *Replicated controls*, *Modifying parameters from code*).
- **A link writes one way only**, from the control to the parameter or variable. *Link to* can also target a parameter of a flowchart block on the same diagram: pick the block, then its *Parameter*. An edit box linked to a Source's rate calls the block's `set_rate()` on each valid entry (Big Book p. 6).
- **One source of truth: the parameter.** Keep controls in step in two moves (Big Book pp. 3–5; Help):
  1. Change the parameter only with `set_<name>(v)`. That call runs the parameter's *On change* (where `oldValue` is available) and passes the value to parameters bound to it. A plain assignment (`p = v`, `p--`) does neither. A call that leaves the value unchanged does not fire *On change* either.
  2. In *On change*, move the control back: `slider.setValue(p);`.
- **`setValue` details (Help *Slider*).** `setValue(v)` does not run the control's Action; `setValue(v, true)` does. A value outside Min/Max, or off the *Step* grid, is snapped to the nearest allowed value with a Console warning. When that happens on a linked slider, the linked parameter is set to the snapped value as well. The slider's range therefore quietly bounds the parameter.
- **At start-up** a linked slider shows the parameter's value. If that value lies outside the slider's range, the knob sits at the nearest end, but the parameter keeps its value until the user moves the knob (Big Book p. 3).
- **Guard ranges with *Enabled*, not with checks in the Action.** *Enabled* is re-evaluated continuously. Example: a "−1" button with Enabled `p >= 1` and Action `set_p(p - 1)` (Big Book p. 4).
- **"Default or custom" panel** (Big Book pp. 11–12):
  - radio buttons (values 0 and 1), plus a slider with Enabled `radio.getValue() == 1`;
  - radio Action `set_p(value == 0 ? 50 : slider.getValue())`. A disabled slider keeps its knob position, so re-apply it when custom mode returns.
- **Typed input.** An edit box linked to an `int` or `double` rejects non-numbers and values outside its Min/Max, and the old value stays (Big Book p. 6). In code, `getDoubleValue()` and `getIntValue()` throw on non-numeric text (Help).
- **Replicated controls** (Help; Big Book pp. 12–13):
  - *Replication* `N` may be a variable. `index` works in dynamic fields and in the Action, e.g. Action `shapes.get(index).setFillColor(blueViolet)` and label `"Paint " + index`.
  - When `N` changes, every copy is destroyed and rebuilt. Anything set on a copy through its API is lost, so keep per-copy state in an array or collection and draw from it.
  - A replicated text reading `slider.get(index).getValue()` can fail with an index-out-of-bounds error at start-up, because the control copies may not exist yet. The Help's fix is `slider.createShapes();` in the container agent's *On startup*.
- **Control actions are atomic.** A click runs between model events and never interleaves with one. In an SD model the solver stops before the action and resumes after it (Big Book p. 11; Help: user code is indivisible). Because the moment of the click is arbitrary, a run with clicks cannot be reproduced (G17).

## Resources
n/a

## Key settings worth copying
- **Reusable API** (every control is a `ShapeControl`, a subclass of `Shape`): `getValue()`, `setValue(v, callAction)`, `setValueToDefault()`, `action()`, `setEnabled(b)`, `setVisible(b)`. The getter per control type is in `videos/experiment-page-pre-run-controls.md`.
- **List box.** *Multiple selection* is available only while *Link to* is off. Read it with `getValues()` (`String[]`) or `getValuesIndices()`. `getValue()` returns only the first selected item.
- **Combo box.** The value is a `String`. Compare it with `value.equals("x10")`, not `==`. Example: a speed selector whose Action calls the engine speed API in `bigbook/calendar-time-dst-safe-events-date-fields-and-run-speed.md`.
- **File chooser (Help 8.9.10).**
  - *Upload* copies the chosen file into the model folder as a read-only file, and the Action's `value` is its relative name. The book's "full path" is outdated.
  - Read it with a Text File element: `file.setFile(value, TextFile.READ);`, then loop on `file.canReadMore()` and call `file.readString()`.
  - *Download* waits until the named file exists, then lets the user save it.
- **Progress bar.** Set *Progress value* to an expression such as `time()`, and *Determinated* to a boolean expression (false shows a busy animation). The progress string may use `value` and `percent`.

## KPIs instrumented
n/a. Echo the live settings on screen so screenshots record the scenario.

## Pitfalls
- **Name versus label.** Code uses the control's name (`slider`). The label is only the displayed text, and it may be dynamic.
- **Controls are painted above every shape,** whatever the Z-order or grouping. Keep them from overlapping each other or key graphics (Big Book p. 1; Help *Controls*).
- **Editions.** The Big Book restricts list box, file chooser and progress bar to Professional and University Researcher. The 8.9.10 Help lists Controls for every edition and tags none of those pages as Pro *(PLE palette not checked)*.
- **A control inside an agent type is drawn once per agent** on the container unless *Visible on upper agent* is off (`videos/agent-type-graphics-visible-on-upper-agent.md`).

## Reusable idea
Controls write through `set_…`, the parameter's *On change* writes back to the controls, and *Enabled* expressions keep inputs legal. Interactive models then never show one value while running another.

## When the co-pilot should use this
- Building stakeholder or digital-twin front ends with live levers, reset-to-default buttons, or file-driven inputs.
- **Symptoms:** a slider disagrees with the value in use; *On change* "never runs"; a replicated label throws at start-up; a list box can't be linked.
- **Related:**
  - `videos/experiment-page-pre-run-controls.md` (pre-run knobs);
  - `videos/statechart-live-controls-trigger-reevaluation.md` (agents reacting to a lever);
  - `bigbook/replicated-shapes-and-group-pivots.md`;
  - `bigbook/click-handling-view-navigation-and-code-created-shapes.md`.
