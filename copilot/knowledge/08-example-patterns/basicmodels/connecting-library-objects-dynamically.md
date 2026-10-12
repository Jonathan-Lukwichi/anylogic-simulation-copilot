# Pattern card — Connecting Library Objects Dynamically
- **Source:** AnyLogic example model "Connecting Library Objects Dynamically" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Join (or split) flowchart blocks from code at runtime instead of drawing connectors — e.g. to assemble a flowchart whose shape comes from data.

## Block chain
Two islands, deliberately left unconnected on the canvas: `Source` (arrivals: *Calls of inject()*) → `Queue`, and `Delay` (triangular 0.5 / 1 / 1.5 min) → `Sink`.
- Button *Connect two blocks*: `queue.out.connect(delay.in)`; the model then shows the connector line only if the queue has never received an agent (`queue.in.count() == 0`), otherwise a warning text.
- Button *Inject an agent*: `source.inject(1)`.
Press Inject before Connect and the join is refused — that is the lesson.

## Resources
n/a

## Key settings worth copying
- Port API: `outPort.connect(inPort)` and `disconnect(...)`; composite blocks expose `map()` / `unmap()` for their inner ports (Help 8.9.10, *How-to* and *Troubleshooting*).
- **Rules (model description):** an `out` of block A may be joined to an `in` of block B only while no agent has yet entered A; a connection cannot be removed once an agent has passed through it.
- **Refresh the far ends.** After any runtime rewiring, the ports at the other ends keep the connections they had at start-up until you call `refreshConnections()` on them, e.g. `myService.release.out.refreshConnections()` (Help, *Troubleshooting → Ports of flowchart blocks fail to connect dynamically*).
- Do the wiring in Main's *On startup* (it runs before any event is executed), before the first agent can reach the port.

## KPIs instrumented
n/a

## Pitfalls
- Treating `connect()` as a routing switch during the run: it fails once agents have used the block. For run-time routing, keep a static topology and decide with `SelectOutput`/`SelectOutput5`, `Hold`, or `Exit` → `target.enter.take(agent)` (`videos/statechart-agent-through-hosted-flowchart.md`).
- Forgetting `refreshConnections()`: agents keep following the start-up wiring with no error.
- An `out` port left unconnected until too late: the first agent that must leave through it stops the model (see G4/G37 for the port errors).

## Reusable idea
Build flowchart topology once, at start-up, from data (for example, N stations read from a table become N replicated blocks joined by `connect()`), and keep all run-time decisions in routing blocks.

## When the co-pilot should use this
- A user generates a line or network of blocks from a spreadsheet and needs to wire them without the canvas.
- Someone asks how to "switch a connector" at runtime — steer them to routing blocks, and cite the two rules above.
