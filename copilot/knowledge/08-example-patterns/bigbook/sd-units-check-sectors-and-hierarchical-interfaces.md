# Pattern card — Structuring and checking SD models in AnyLogic: units check, stock modes, sectors vs agent interfaces
- **Source:** AnyLogic "The Big Book of Simulation Modeling", ch. 5 "System dynamics" — distilled, original wording
- **Paradigm:** SD
- **Problem it solves:** Large or reusable stock-and-flow models become unreadable, go unverified, or get coupled across agents by Java references that bypass the structure checks.

## Mechanism
Checked against Help 8.9.10 (*Units*, *Stock*, *Shadow*, *Layout of large SD models*, *Hierarchical SD modeling*,
*Connecting system dynamics variables*, *Renaming model elements*).
1. **Run a units pass as verification.**
   - Tick *System dynamics units* (Advanced section) on stocks, flows, dynamic variables, parameters, table functions and
     functions. `time` means the model time unit, and an empty field means dimensionless.
   - Then run Tools > *Check System Dynamics Units*; conflicts go to the Problems view.
   - Rules that catch most slips (ch. 5 pp. 27–28): a flow is stock unit / time; a per-capita rate that multiplies a
     stock is 1/time; lifetimes and delays are time; a lookup effect multiplier is dimensionless.
   - Units never change results. They only expose formulas that cannot be right.
2. **Know the stock equation modes.**
   - *Classic* (the default) is inflows minus outflows and cannot be edited.
   - *Custom* takes any derivative expression, meant for physical or ODE models. Links are still checked against it.
     After renaming an element used in a Custom formula, refactor so the formula follows (Help *Stock*).

   Links run only between variables; table functions and Java functions are called without links (ch. 5 p. 21). The
   link-equation check itself ("… is used but not expected") is in 3-days pp. 108–110.
3. **Two ways to split a large model:**

   | | Sectors in one agent | Components as agent types |
   |---|---|---|
   | How | view areas per sector; a shadow (right-click, *Create Shadow*) stands in for a variable owned elsewhere | each sector is an agent type; outputs are ticked *Visible on upper agent*; inputs are ticked *Dependent*; connectors join them on Main |
   | How to spot it | a shadow's name is in `<…>`, and its icon is grey | variables sit on the agent icon's border |
   | Use when | a one-off model, a Vensim-style layout | reuse, parameterised copies, several instances |

   Connection rules (Help):
   - only dynamic variables and flows can be connected, never plain variables;
   - connect like with like, flow to flow and dynamic variable to dynamic variable;
   - one source per dependent variable, although a source may feed many;
   - the dependent side only copies, so writing to it does not flow back;
   - two variables of the same agent cannot be connected.
4. **Don't wire SD diagrams in different agents through Java references** such as `other.X` inside a formula (ch. 5
   p. 11). Use the interface connection, which keeps the coupling visible and checked. The book calls these "external
   variables"; in 8.9.10 the mechanism is *Dependent*. Java in formulas remains the normal way to read the discrete
   parts: `Level < 10 ? MaxRate : NormalRate` (Vensim IF THEN ELSE), a double-returning function reused in many
   formulas, a population statistic, or a block's queue size. See `models/ab-market-and-sd-supply-chain.md`.
5. **Rename safely.** Type the new name in the *Name* field and press Ctrl+Enter before leaving it, or use the Projects
   view's *Rename…*. Both update every reference, with a preview (Help). Clicking away renames only the element, and
   formulas that use the old name stop compiling (ch. 5 p. 10).

## Resources
n/a

## Key settings worth copying
- Agent type, Advanced: *Create datasets for dynamic variables*, with *Recurrence time* and *Limit the number of data
  samples*. The 8.9.10 book models keep 100 samples at 1 time unit. The inspect-window plot of a stock shows only
  these latest samples (compare G18). For whole-run history, add your own dataset or chart.
- Names: mixed case with no spaces (underscores allowed); names are case-sensitive, so `Stock` and `stock` differ
  (ch. 5 p. 5).

## KPIs instrumented
n/a (structure and verification)

## Pitfalls
- **Partial unit coverage.** A unitless variable used inside a variable with units raises only a warning (ch. 5
  p. 13). Finish the pass, or the check proves little.
- **Shadow colour.** Re-colouring a variable re-colours all its shadows, so they can no longer be told apart by colour
  (Help). Rely on the `<…>` brackets.
- **Several sources for one input.** Connecting two sources to one Dependent variable is not allowed. Add the sources
  in a variable first.

## Reusable idea
Structure an SD model the way you structure code: typed units, explicit interfaces between components, and
tool-supported renames. Let the checker, not your eyes, find the inconsistencies.

## When the co-pilot should use this
- Any SD model with more than one sector, or one reused in several places (regions, products, plants).
- Before trusting an SD model built by someone else.
- When converting a Vensim model with sectors.
- Related: `bigbook/sd-numerical-hygiene-lookups-noise-and-solver-step.md`;
  `models/agent-population-and-sd-housing.md` (SD inside agents, arrays).
