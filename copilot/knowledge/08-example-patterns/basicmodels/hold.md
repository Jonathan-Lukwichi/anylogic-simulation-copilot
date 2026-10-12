# Pattern card — Hold
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Gate or throttle agent flow through a process — stopping agents until an external signal, a count threshold, or a logical condition releases them.

## Block chain
Three independent sub-flows share the same pattern skeleton:

1. **Count-based blocking** — Source → Queue → Hold (auto-blocks after N agents) → MoveTo → Sink. *Block automatically after N agents* lets N agents **through** and then closes until `unblock()` is called; with *Initially blocked* and N = 1, each `unblock()` releases exactly one agent — a one-per-signal gate. The Hold never holds agents inside; they wait in the Queue before it (Help 8.9.10, *Hold*; corrected 2026-10-01).

2. **Manual mode** — Source → Hold (manually controlled) → Delay → MoveTo → Sink. A button or timed event calls `hold.unblock()` / `hold.block()` from Java code, giving full programmatic control over when the gate opens and closes.

3. **Conditional mode** — Source → Hold (condition-based) → Queue → MoveTo → Sink. The field is a **Blocking condition**: each arriving agent is tested against it, and **true blocks** the agent. It is not polled — after anything the condition reads changes, call `hold.recalculateConditions()` so waiting agents are re-tested (Help 8.9.10, *Hold*; corrected 2026-10-01; gotcha G85).

All three variants include MoveTo blocks, indicating agents move through a 2-D space (pedestrian or material-handling context).

## Resources
n/a — no ResourcePool or Seize/Release blocks; capacity control is handled entirely by the Hold gate logic.

## Key settings worth copying
- **Auto-block count:** integer N on the Hold (`nEntitiesForSelfBlock`) closes the gate after N agents have passed.
- **Manual unblock call:** `holdBlock.unblock()` invoked from a button action or scheduled timeout; pair with `holdBlock.block()` to re-close.
- **Blocking condition:** a Boolean expression that reads "must wait" (e.g., `time() < openTime || queue.size() >= maxBatch`), evaluated for each arriving agent; call `recalculateConditions()` wherever its inputs change.
- **Time unit:** Seconds — keep consistent when specifying inter-arrival rates and delay durations.
- **Spacing distribution:** `uniform(1, 3)` seconds used for at least one arrival spacing, giving light random variability without heavy tails.

## KPIs instrumented
- Queue content (agents waiting behind each Hold gate)
- Throughput count at Sink
- Time agents spend blocked (implicit in queue statistics)

## Reusable idea
The Hold block is the cleanest way to implement any "traffic light" or "batch-release" logic in AnyLogic DES: rather than hacking a Delay with infinite time or abusing a Queue capacity, place a Hold and drive its open/closed state from a condition, a counter, or an explicit method call — keeping flow-control intent visible and auditable in the process diagram.
