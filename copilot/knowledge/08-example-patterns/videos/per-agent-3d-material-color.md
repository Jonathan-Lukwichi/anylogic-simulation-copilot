# Pattern card — Per-agent colour on a 3D object via material setColor()
- **Source:** AnyLogic video "How to generate 3D objects of different colors" (https://youtu.be/WIU8-2hqyqM) — distilled, original wording
- **Paradigm:** Method (3D animation technique for agents in any paradigm)
- **Problem it solves:** All agents of a type share one 3D model, and so one colour. Give each agent (or each state) its own colour without creating one agent type per colour.

## Mechanism
- **Materials.** A 3D Object is made of named **materials**, listed in its *Colors* section. In the Gas Station example the car body is `Material__4__Surf`.
- **Runtime recolour.** The 3D Object shape (API class `Shape3DObject`) recolours one material with `setColor(String materialName, Color color)`.
- **One colour per agent.** Call it in the agent type's **On startup** so it runs once for each new agent: `car.setColor("Material__4__Surf", randomColor());`. Here `car` is the name of the 3D Object shape inside the `Car` type.

## Resources
n/a

## Key settings worth copying
- **Any standard colour.** `randomColor()` returns one of AnyLogic's 140 named colours. The result is bright and can look garish.
- **Curated palette.**
  - Create a Collection `colors` with Elements class `Color` and initial contents such as `{red, silver, black, white}`.
  - Then call `car.setColor("Material__4__Surf", randomFrom(colors));`.
- **Reset.** Pass `null` as the colour to restore the material's original colour. Source: AnyLogic API / Big Book ch. 14, not the video.
- **Recolour later.** The same call works from any action:
  - a statechart state's entry action, to show state;
  - a flowchart action in Main, e.g. `agent.car.setColor("Material__4__Surf", red)`.

  This is an extension of the video's technique.

## KPIs instrumented
n/a (visual only).

## Pitfalls
- **The material name is an exact, case-sensitive string.**
  - Copy it from the *Colors* section. Mesh-generated names such as `Material__4__Surf` are arbitrary, and swapping the 3D model changes them.
  - A wrong name leaves the colour unchanged. Whether it also raises an error is *(unverified)*.
- **3D only.** The recolour shows in the 3D scene only. The 2D view and the editor keep the original look.
  - For colour in 2D, colour a 2D shape's fill instead.
  - Alternatively, use one agent type per colour. That works in both views but multiplies agent types.
- **Choose the right material.** Models have several materials, and the video recolours only the body. Recolour only the materials meant to vary.
- **Typed agent needed.** `agent.car` compiles only where the block's Agent type is set to `Car` (or after a cast).
- **Colour that carries meaning.** When colour means something (type, priority, state), use a small, contrasting fixed palette rather than `randomColor()`.

## Reusable idea
Colour is a free visual channel for agent attributes. Randomise it for realism, or map an attribute or state (product type, triage level, battery low) to a small palette so viewers can read the 3D animation at a glance.

## When the co-pilot should use this
- **When to recommend it.** The user wants visual variety or colour-coded agents (vehicles, products, patients) in a 3D view. Prefer this over one-type-per-colour when only 3D matters, and state the 2D limitation.
- **Build phase.** This is presentation work (build Phase 5, animate & instrument). Do it after the logic is verified.
- **Related cards.**
  - `models/gas-station.md`: the source model.
  - `basicmodels/match.md`: palette plus `randomFrom`.
  - `basicmodels/agent-per-fluid-batch.md`: `randomColor()`.
  - `models/billiard-balls.md`: `spectrumColor()` for distinct hues.
  - `models/agent-based-population-model.md`: swapping 3D shapes by attribute, for when the shape and not just the colour must change.
