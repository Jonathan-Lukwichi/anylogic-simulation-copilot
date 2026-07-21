# Water-Treatment Twin — One-Hour Prototype Build Plan

Companion to [blueprint.md](./blueprint.md). Scope: a demonstrable **AnyLogic PLE**
prototype = steps 1–3 of the blueprint's §8 build sequence. NOT the production twin.

## Verified facts (July 2026)
- PLE **includes the Fluid Library** and all three methods (all standard libraries).
  Source: anylogic.help editions comparison; anylogic.com PLE download page.
- PLE caps that matter: **5 h sim-time limit** (all libs except Process Modeling — our
  ~1 h horizon is fine); ≤10 agent types; ≤200 blocks/agent; ≤200 SD variables/agent.
  Our skeleton is far under all caps.
- Phase 0 already settled by the blueprint: **multimethod** = Fluid (hydraulics) +
  System Dynamics (chemistry) + Statecharts (control). Agreed, not re-litigated.

## Confirmed Fluid Library blocks + fields (from knowledge/08-example-patterns)
FluidSource (rate m³/s, infiniteCapacity, inject(), amountPassed()) · Tank (capacity,
initialAmount, limitRateOut, maxRateOut, level(), customInitialBatch) · Pipeline ·
Valve · FluidExit/FluidEnter (flowRate(), programmatic rate control) · FluidDispose.

## 60-minute sequence (each segment has a GATE before the next)
| Time | Segment | Gate |
|---|---|---|
| 0–5   | Setup: units=Second, base=m³, fixed seed, ~1 h horizon | model opens, runs empty |
| 5–20  | Fluid train: Source→Pipeline→flashMix Tank→floc/clarifier Tank→clearwell Tank→Dispose | **mass balance closes** (in = out + Δstorage), no chemistry |
| 20–35 | System Dynamics: coagulant-mass stock + optimumDose & treatedTurbidity auxiliaries | treated-turbidity matches Phase 3 Python on same inputs |
| 35–50 | Dosing Statechart: Calm-Trim / Storm-Escalate / Fallback-Safe | states switch on storm threshold + sensor-health guard |
| 50–60 | Animation + KPIs: clearwell level colour bands, turbidity vs SANS 241, coagulant/hr | dashboard live, colour bands correct |

## Explicitly deferred (dependency-gated per blueprint §4, §5, §8)
Pypeline/ONNX ML bridge · OPC UA read/write · Stage-1 calibration. All coefficients
remain placeholders — the prototype demonstrates structure & behaviour, not plant physics.

## Placeholder plant parameters (illustrative only, pre-calibration)
- Inlet flow: 0.10 m³/s (≈360 m³/h)  · Flash-mix Tank: 20 m³ · Floc/clarifier Tank: 500 m³
- Clearwell: capacity 1000 m³, initial 300 m³, watched level · Demand outflow: 0.10 m³/s
- SANS 241 treated-turbidity target: ≤ 1 NTU (placeholder) · storm threshold: influent > 50 NTU
