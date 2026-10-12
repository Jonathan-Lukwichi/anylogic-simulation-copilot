# Pattern card — Valve
- **Source:** AnyLogic example model "Valve" (basicmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** DES (Fluid Library)
- **Problem it solves:** Meter a continuous flow: open and close it on command, let an exact quantity through, and react every time a fixed portion has passed.

## Block chain
`FluidSource` (100 m³/s) → `Tank` → `Valve` (50 m³/s when open; recurrent action every 100 m³) → `FluidDispose`.
Controls: a button `valve.toggle()`; a button `valve.dispense(dispenseAmount)` (200 m³); a check box linked to
`valve.actionOnPortion`; *On portion passed* counts portions, *On dispense completed* adds `amount` to a total; the
tank's *On empty* resets a slider.

## Resources
n/a

## Key settings worth copying
- **Rate:** *Rate when open* (`openRate`, `set_openRate(...)`) or *Maximum rate when open* (unlimited — then something
  up- or downstream must limit it); *Initially closed* (`closed`). A zero-capacity block; rates below 1e-9 snap to 0.
- **Commands:** `open()`, `close()`, `toggle()`, `isClosed()`.
- **Dosing:** `dispense(amount)` / `dispense(amount, units)` opens the valve if needed, lets exactly that amount pass,
  closes it and fires *On dispense completed* (local `amount`). Progress: `amountBeingDispensed()`,
  `amountDispensedSoFar()`.
- **Portions:** *Recurrent action on portion* (`actionOnPortion`, `portionSize`) fires *On portion passed* each time that
  much has flowed; `amountPassedInPortion()` gives the part of the current portion. Counting continues during a dispense.
- **Statistics:** `amountPassed()`, `currentRate()`, `averageRate()`, `utilization()` (current rate ÷ open rate),
  `utilizationTotal()`, `resetStats()` (Help 8.9.10, *Valve*).

## KPIs instrumented
Portion count and total dispensed amount shown on screen.

## Pitfalls
- `dispense()` **closes the valve afterwards**, even if it was open before the call.
- A dispense lasts amount ÷ *actual* rate, which upstream stock and downstream capacity can hold below the open rate.
- When the end of a dispense coincides with a portion boundary, the order of *On portion passed* and *On dispense
  completed* is undetermined (Help) — do not chain logic on it.
- `utilizationTotal()` returns 0 once the open rate has ever been unlimited (Help).

## Reusable idea
Use the Valve as the metering point of a fluid network: `dispense()` for "load exactly X" (trucks, batches, doses),
portions for "do something every X" (tickets, samples, new batch labels), open/close for control logic from tank
events or statecharts.

## When the co-pilot should use this
Loading bays, batch charging of reactors or mixers, dosing lines, metering and sampling, and any "let exactly N units
through" request. Related: `tank.md` (level-driven valve switching), `pipeline.md` (new batch every portion),
`transporter-charging-system.md` (valves as charge/discharge switches), `fluidpickup.md`.
