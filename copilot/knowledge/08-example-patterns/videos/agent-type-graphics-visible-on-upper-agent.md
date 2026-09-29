# Pattern card — Agent-type graphics: what an agent type draws on its container (Visible on upper agent)
- **Source:** AnyLogic video "AnyLogic ABM Tutorial Part 3 | Defining Agent Behaviour with Statecharts" (https://youtu.be/k69Ow9q8gBc) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Notes, pictures, charts or controls placed inside an agent type turn up on Main (once in the editor, once per agent at runtime), cluttering and slowing the animation.

## Mechanism
- **What the video shows.** To keep his build steps in view, the presenter pastes a screenshot of them onto the `Consumer` diagram. It then appears on Main as well; he calls it a duplication and deletes it (and does the same again in Part 5). This is documented behaviour, not a glitch.
- **The rule (Help 8.9.9, *Agent presentation*).** A container draws each embedded agent's presentation: every element on the agent type's diagram whose *Visible on upper agent* box is ticked. In the editor that is one copy, inside the population's presentation shape on Main. At runtime it is one copy per agent, placed at the agent's position plus the element's offset from the agent type's axis origin. That is why the wizard puts the agent's body at the origin: anything drawn elsewhere is shifted by its offset.
- **The defaults decide what leaks.** Editor defaults for new elements in 8.9.9 (read from `com/anylogic/objectmodel/factory/ame_initialization_plan.json` inside `plugins/com.anylogic.objectmodel8impl_<ver>.jar`):

| *Visible on upper agent* when created | Element types |
|---|---|
| ticked | image, text, rectangle, rounded rectangle, oval, line, polyline, group; every chart (time stack chart, time plot, bar, pie, histogram, plot…); every control (button, slider, check box, edit box, combo box, radio buttons) |
| unticked | statechart entry point, states, transitions, branches; events; functions; plain, collection and dynamic variables; stocks; datasets, histogram data, statistics |

  So a statechart never shows on Main, but a pasted picture, a debug chart or a test slider does.

## Resources
n/a

## Key settings worth copying
- Element → Properties → General → **Visible on upper agent**: untick it for everything that is the agent type's "workbench" — instruction screenshots, notes, diagnostic charts, test buttons. They stay visible in the agent type's editor and, at runtime, when you dive into one agent through the developer panel's Model Navigation (it has an index selector for populations).
- Keep what should represent the agent (its body shape, a state-coloured marker) ticked and at the axis origin (0, 0).
- Deliberate per-agent overlays (an ID label, a small status bar) are fine: keep them small and near the origin, and gate them with a *Visible* expression such as `main.showLabels` so large runs can switch them off.
- Notes meant for the whole model belong on Main, outside the model-window frame.

## KPIs instrumented
n/a

## Pitfalls
- **Scale.** A 600 × 400 px screenshot left in `Consumer` becomes 5,000 overlapping images on Main. A chart or control left in an agent type is replicated for every agent in the same way, which costs rendering time for nothing.
- **Positioning is a separate setting.** Moving the population's icon on Main does not move the agents' space. The space stays anchored at (0, 0) unless the embedded presentation draws agents with offset to its position (3-days p. 38–39) or sits in a group that you move (Help 8.9.9). The Part 2 presenter simply dragged the icon clear of that area.

## Reusable idea
Treat each agent type's canvas as two layers. The **body** is ticked, sits at the origin, stays minimal and is drawn N times. The **workbench** holds logic, notes and diagnostics, is unticked, and is drawn only when you look inside one agent. Logic elements default to the workbench; graphics, charts and controls default to the body, so move them over deliberately.

## When the co-pilot should use this
- A user reports stray or repeated images, text, charts or buttons on Main, or a slow animation after decorating an agent type.
- Adding notes, screenshots, per-agent debug charts or controls inside agent types, or designing per-agent labels.
- Reviewing an ABM's presentation before it goes to stakeholders.
