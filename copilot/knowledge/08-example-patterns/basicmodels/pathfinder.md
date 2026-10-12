# Pattern card — Pathfinder
- **Source:** AnyLogic example model "Pathfinder" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM (reinforcement-learning ready)
- **Problem it solves:** A minimal, fully worked template for making an AnyLogic model trainable by an external RL platform (ALPyne) — decision points, observation/action/configuration spaces, episode end — and for replaying the learned policy inside AnyLogic.

## Structure
- 8 × 8 **discrete space** of `Cell` agents (empty cells, `numHoles` hole cells, one goal cell) and one `MyAgent` walker; directions are an Option-List-like set `VALID_DIRECTIONS` (4 or 8 with `useMooreNeighbors`).
- **RL experiment `PathfindingBrain`** (ReinforcementLearningExperiment):
  - *Observation*: `cells` (`int[][]` grid coded 0 empty / −1 hole / 1 goal) and `pos` (`int[]` row, column of the walker);
  - *Action*: `dir` as a **String**, applied with `root.agent.tryMove(CellDirection.valueOf(dir))` — enum names travel safely across the platform boundary;
  - *Configuration*: `useMooreNeighbors`, `slipChance`, `slipChanceSeed` (Long), `numHoles`, `minStepsRequired`, `throwOnInvalidActions`; its code also sets `root.mode = 2`, so the same model switches itself into platform-driven mode;
  - *Episode stop condition*: the walker's cell is a hole or the goal (`instanceof CellHole || instanceof CellGoal`).
- **Decision point:** a cyclic event `stepEvent` calls `PathfindingBrain.takeAction(this)`; per Help the platform then pauses the model after zero model time, reads the observation, and applies the returned action.
- **Modes** (parameter `mode`, radio buttons): 0 = user plays with arrow buttons (`tryMove`), 2 = platform-driven (set by the Configuration code), 3 = **replay a learned Q-table** read at start-up from JSON (`new ObjectMapper().readValue(new File(qtableFile), double[][].class)`), with arrows drawn on each cell.
- **Solvable random instances:** holes are placed at random, then `validate(depth)` checks with a best-first search (`stepsToReach()`) that the goal is reachable in at least `minStepsRequired` steps and re-draws otherwise (gives up with an error after 100 tries).
- **Slippery moves:** with probability `slipChance` the move goes in a random valid direction, drawn from a **separate** `Random slipRNG` created on startup from the optional parameter `slipChanceSeed` (null → unseeded) via `randomTrue(p, rng)` / `randomFrom(list, rng)`.
- Output `score` = `getScore()`, computed at simulation end.

## Resources
n/a

## Key settings worth copying
- RL experiment test functions (Help 8.9.10) let you check the spaces before exporting: `createConfiguration()` / `applyConfiguration(root, cfg)`, `createObservation()` / `getObservation(root, obs)`, `createAction()` / `applyAction(root, act)`, `checkEpisodeStopCondition(root)` — the demo uses the last one to end user-controlled episodes.
- Configuration code runs after the root is created but before it starts: set static parameters only.
- `takeAction(agent)` may be called from any event/statechart/block action; repeated calls in one code field add nothing.
- Keep training randomness you want to control (slip) on its own `Random`, so changing it does not shift every other random draw.

## KPIs instrumented
Episode score (`getScore()`), steps to reach the goal.

## Pitfalls
- The RL experiment itself cannot be run in AnyLogic — it is an export interface for a platform (ALPyne, Azure ML); test with the functions above or a user/replay mode as this demo does.
- Some platforms (e.g. Azure ML) want the stop condition defined on the platform side; leave the field `false` there (Help).
- Random layouts can be unsolvable; without a validation step the agent is trained on impossible episodes.

## Reusable idea
Build every RL-ready model with three run modes — manual, trained-policy replay (policy loaded from a file) and platform-driven — plus instance validation and a dedicated RNG for the stochastic element being learned. It makes debugging the reward and dynamics possible before any training starts.

## When the co-pilot should use this
When a user wants to connect a model to ALPyne or another RL platform, needs the minimal decision-point/space set-up, or wants to run a learned policy inside AnyLogic. See `06-ai-ml-integration/README.md` for routes (Alpyne, Pypeline, Cloud API).
