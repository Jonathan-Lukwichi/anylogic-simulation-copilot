# Phase 5 — AnyLogic Digital Twin: Build Blueprint

**Engagement phase:** 5 of 7
**Deliverable nature:** a build blueprint. I cannot run AnyLogic and do not deliver a finished `.alp` file. What follows is the library-by-library, block-by-block specification an AnyLogic engineer follows to build the twin, plus the machine-learning bridge and the live PLC link. Every coefficient is a placeholder until the Stage 1 calibration on plant data (Phase 2), and the twin propagates its assumptions exactly as the Phase 3 simulation does; it does not prove plant physics.

**Vendor facts, verified against AnyLogic documentation, June 2026 (re-check before procurement):**
- The Fluid Library is included in AnyLogic Professional (and University Researcher for academic use). The free Personal Learning Edition has limited library access, a capped model size, and a five-hour simulation-time limit, so it is fine for a prototype but not for a production twin.
- Pypeline is a free, open-source, third-party connector from The AnyLogic Company. It runs on any licence, calls a local Python 3 installation through a PyCommunicator element, and the vendor explicitly offers no support or compatibility guarantee and notes it adds runtime overhead.
- AnyLogic has no native drag-and-drop OPC UA block. OPC UA is implemented in AnyLogic's Java environment using an OPC UA Java client SDK such as the open-source Eclipse Milo or the commercial Prosys SDK. Verify the SDK and JDK version compatibility for your AnyLogic build.

---

## 1. The one correctness rule that governs the whole build

A water-treatment train is continuous flow and mass balance. Do not model the hydraulic train with the Process Modeling Library (Source, Queue, Delay, Sink). That library moves discrete entities through queues and is the wrong abstraction for water; using it here is the single most common modelling error and it produces a plausible-looking model that is physically meaningless.

The correct method mapping, which the rest of this document follows:

| Concern | Method | Why |
|---|---|---|
| Tanks, pipes, levels, flow, backwash | Fluid Library | Linear flow network solved by an LP solver; fast and accurate for hydraulics |
| Coagulation chemistry, dose-response, mass balance | System Dynamics (stocks and flows) | The dose-response is a non-linear continuous relationship; AnyLogic itself recommends System Dynamics over the Fluid Library for non-linear feedback |
| Control loops, alarms, safe-state, backwash sequencing | Statecharts | Discrete control states with guarded transitions |
| Calling the trained model | Pypeline or ONNX-in-Java | See Section 4 |
| Live PLC link | OPC UA via a Java SDK | See Section 5 |

The Fluid Library and System Dynamics meet at one point: the Fluid Library gives the flow and tank levels, those feed the System Dynamics equations that compute treated turbidity from dose and influent, and the Statechart controller reads both and sets the dose.

---

## 2. The four layers

```
 LAYER 1  PHYSICAL PLANT (real)
 raw intake -> flash mix -> flocculation -> clarifier -> filters -> clearwell -> distribution
        |          ^ coagulant dosing pump            |                |
   turbidity,    (actuator)                       backwash         level, outflow
   pH, flow                                                            
        |  sensors                                                     
        v
 LAYER 2  PLC / EDGE I/O (real control)
 PLC reads sensors -> exposes OPC UA server -> enforces hard dose limits ->
 actuates dosing pump and valves -> interlocks and safe-state on fault/power loss
        |  OPC UA (read tags)                         ^ OPC UA (write setpoint, supervised only)
        v                                             |
 LAYER 3  EDGE AI BRAIN (real, on-prem edge node)        |
 cleaning + features -> ONNX predictor -> dose optimiser -> storm escalation /
 fallback -> explainability -> recommended dose ---------+
        |  same live tags
        v
 LAYER 4  ANYLOGIC TWIN (simulation mirror)
 Fluid Library (hydraulics) + System Dynamics (chemistry) + Statecharts (control)
 role A: online shadow, fed by OPC UA, compares twin and AI against the real plant
 role B: offline what-if and operator training, runs faster than real time
```

| Layer | Real-world component | Representation in this blueprint |
|---|---|---|
| 1 Physical plant | Tanks, pumps, dosing line, sensors | Mirrored by the Fluid plus System Dynamics model in Layer 4 |
| 2 PLC edge I/O | PLC, OPC UA server, hard limits, interlocks | The OPC UA tags the twin and the AI both read; the write path the AI uses in the supervised stage |
| 3 Edge AI brain | The Phase 3 predictor and optimiser on the edge node | Called from the twin by Pypeline or embedded as ONNX (Section 4) |
| 4 AnyLogic twin | The simulation itself | Fluid Library, System Dynamics, Statecharts (Sections 3) |

---

## 3. The AnyLogic build, by method

### 3.1 Fluid Library: the hydraulic train

Build the water path as a Fluid flow network. Amounts in cubic metres, rates in cubic metres per second (the library converts internally; keep every block in the same unit type to avoid the inconsistent-units error).

| Block | Represents | Key parameters (plant-calibrated) |
|---|---|---|
| FluidSource | Raw-water intake | Inflow rate driven at run time by the measured inlet flow tag |
| Pipeline | Inter-stage transfer and hydraulic delay | Length, capacity, maximum rate |
| Tank (flash mix) | Rapid-mix chamber where coagulant enters | Volume, the point where the System Dynamics dose mixes in |
| Tank (flocculation, clarifier) | Floc growth and settling residence | Volume, retention time |
| Tank (clearwell) | Treated-water storage, the level the operator watches | Working volume, the level mapped to the Phase 4 colour bands (red below 15 percent, amber 15 to 30 and 85 to 95, green 30 to 85, red above 95) |
| Valve | Flow control, backwash isolation | Open and closed rates |
| FluidSplitOutput / FluidSelectOutput | Diverting filtered water to backwash | Split ratio, driven by the backwash Statechart |
| FluidDispose | Plant outflow to distribution | Outflow rate driven by demand |

The Fluid Library uses a discrete-rate, linear-programming solver, so flows are piecewise constant and change only at discrete events. That is correct and fast for hydraulics. Do not try to encode the non-linear coagulation chemistry inside Fluid blocks; that belongs in System Dynamics.

### 3.2 System Dynamics: chemistry and mass balance

Model the coagulation outcome as stocks, flows, and auxiliary equations, because the dose-response is non-linear and has continuous feedback, which is exactly the case AnyLogic says to use System Dynamics for.

- Stock: coagulant mass in the flash-mix tank, fed by the dosing-pump flow and drained by outflow.
- Auxiliary: optimum dose as a function of influent turbidity, pH, and temperature, the same relationship used in the Phase 3 twin (dose rises non-linearly with turbidity, with pH and cold-water penalties).
- Auxiliary: treated turbidity as a function of how far the delivered dose sits from optimum, the Phase 3 residual relationship (under-dosing penalised more steeply than over-dosing, then a filter-polishing factor). This auxiliary is the model's prediction of compliance and is what the twin compares against the real effluent turbidity tag.
- Flow: chemical consumption per hour equals dose times flow, which is the quantity the chemical-saving benefit acts on.

Keep these equations in one System Dynamics diagram wired to the Fluid tank levels and flows. When the real trained model is embedded (Section 4), the predictor can replace this analytic auxiliary for the treated-turbidity estimate, with the System Dynamics version retained as the physically based fallback that Dunnington et al. showed is more reliable when the model is asked to extrapolate.

### 3.3 Statecharts: control, alarms, safe-state

Three statecharts carry the control logic, each mirroring a behaviour already specified in earlier phases.

The dosing controller, mirroring Phase 3:
- Calm-Trim: the optimiser sets the least dose predicted to hold treated turbidity below the SANS 241 target with a small buffer.
- Storm-Escalate: entered when sensed influent turbidity crosses the storm threshold; the controller stops trimming and commands a conservative safety dose.
- Fallback-Safe: entered on a sensor-health or power-health failure; the controller holds the last-good or a conservative dose and raises an alarm.
- Manual-Override: the operator takes control at any time; the model advises but does not act.

The alarm manager, mirroring Phase 4: per-parameter trigger evaluation with a debounce counter (a condition must persist for several cycles before firing) and a latch (an alarm stays raised until acknowledged), with Info, Warning, and Critical severities. In the twin this drives the same alert behaviour the demo console shows; in production the historian or edge service owns it.

The backwash sequencer: a timed or headloss-triggered cycle that drives the FluidSelectOutput diversion and the relevant valves, so the twin captures the hydraulic disturbance backwash causes.

### 3.4 What not to build

Do not place Source, Queue, Delay, and Sink blocks to represent the water path. If you find yourself modelling water as entities in a queue, stop and move that section to the Fluid Library. The only legitimate use of Process Modeling Library blocks here is at the boundary, through AgentToFluid or FluidToAgent, if discrete items such as dosing batches or lab samples ever need to enter the fluid network.

---

## 4. Machine-learning integration: the bridge

The trained model from Phase 3 is a gradient-boosted-tree predictor of treated turbidity, wrapped by a dose optimiser. There are two ways to call it from AnyLogic, and the right answer depends on the stage.

**Option A, Pypeline, for development and shadow mode.** Add the Pypeline library, drop a PyCommunicator element, and call the Phase 3 Python functions directly (the predictor and the dose search) through runResults, passing the feature vector and receiving the recommended dose. This gives exact parity with the research code and is the fastest way to iterate. The honest trade-offs, from the vendor's own documentation: Pypeline is third-party and unsupported, it requires a local Python 3 installation on the node, and it adds runtime overhead, so it is not the best choice when inference latency matters.

**Option B, ONNX-in-Java, for the production edge node.** Export the trained predictor to ONNX, load it in AnyLogic's Java environment with the ONNX Runtime Java API, build the feature vector each control step, run the dose search in Java, and apply the storm-escalation and fallback rules in the Statechart. This runs natively on the JVM, needs no Python on the plant node, is deterministic, and is low latency. One caveat to verify rather than assume: confirm that the chosen exporter supports the specific estimator (skl2onnx coverage varies by scikit-learn version and model type); if the gradient-boosted variant does not export cleanly, either retrain as an ONNX-exportable model or keep that node on Pypeline.

Recommendation: develop and run shadow mode with Pypeline for parity, then embed ONNX for the supervised closed loop where latency and the no-Python-dependency property matter. In both cases the System Dynamics analytic relationship from Section 3.2 stays in the model as the physically based fallback for out-of-range conditions.

---

## 5. The live PLC link: OPC UA

The twin and the edge AI both read the plant through OPC UA. Implement it in AnyLogic's Java environment using an OPC UA Java client SDK (Eclipse Milo is the open-source option; Prosys is a commercial one). There is no native AnyLogic OPC UA block, so this is custom Java wired into the model's startup and a recurring event.

- Read path, always: subscribe to the sensor tags (influent turbidity, pH, temperature, flow, clearwell level, dosing-pump feedback, effluent turbidity) and feed them into the Fluid and System Dynamics inputs each cycle. This is what lets the twin run as an online shadow.
- Write path, supervised stage only: in the closed loop the AI writes the coagulant setpoint back through OPC UA, and the PLC, not the model, enforces the hard dose limits and the interlocks. The model never bypasses the PLC's limits. This is the Phase 2 and Phase 7 rule made concrete: the AI advises, the PLC acts within hard limits, the operator can override.

Verify the OPC UA SDK and JDK version compatibility against your AnyLogic build before committing; older Java SDK builds have specific JDK constraints.

---

## 6. The two roles the twin plays

**Online shadow.** Fed by the OPC UA read path, the twin runs in parallel with the plant. It compares its own predicted treated turbidity against the measured effluent, and the AI's recommended dose against what the operator actually did. Divergence between twin and plant is the signal that the model needs recalibration; divergence between AI recommendation and operator action is the evidence base for the Phase 2 shadow-mode gate. This is the twin earning trust before anything is automated.

**Offline what-if and operator training.** Decoupled from the live feed, the twin runs faster than real time to answer questions that are unsafe or impossible to test on the plant: what a one-in-five-year storm does to compliance, how the controller behaves when the turbidimeter freezes, what happens to the dosing loop when a load-reduction block cuts power to the edge node. It is also a safe operator-training sandbox, where staff see the controller's reasoning and practise overrides without touching real water. This is where the storm-escalation and fallback logic from Phase 3 is stress-tested before it is allowed near the closed loop.

---

## 7. What the twin demonstrates about the process improvement

Run on plant-calibrated parameters after Stage 1, the twin reproduces the Phase 3 before-versus-after comparison inside AnyLogic: baseline fixed dosing against the AI closed loop, on chemical use and SANS 241 compliance, with the calm-versus-storm split made visible through the Fluid Library's tank and flow animation. It validates that the closed loop holds compliance while trimming the calm-water over-dose margin, and it exercises the failure modes safely, the extrapolating predictor, the frozen sensor, the power loss, so that each is shown to trigger the right safe-state before the loop is trusted on the plant. The defensible benefit remains the literature-anchored 10 to 20 percent coagulant reduction (Yang et al., 15.7 percent), not the simulation's upper-bound figure.

---

## 8. Build sequence and verification

A practical order for the engineer:
1. Build the Fluid hydraulic network and confirm the mass balance closes (inflow equals outflow plus storage change) with no chemistry.
2. Add the System Dynamics chemistry and check the analytic treated-turbidity auxiliary against the Phase 3 Python outputs on the same inputs.
3. Add the three Statecharts and confirm the controller reproduces the Phase 3 calm, storm, and fallback behaviours.
4. Wire Pypeline and reproduce the Phase 3 numbers end to end inside AnyLogic (parity check).
5. Add the OPC UA read path and run as an online shadow against historian playback.
6. Only then consider ONNX embedding and, in a later supervised stage with the plant's agreement, the OPC UA write path.

Verification gate before the twin is trusted for decisions: the twin's predicted effluent must track the measured effluent within an agreed error band across a representative period including a storm, the same evidence standard as the Phase 2 shadow gate. Until it clears that gate the twin is a design and training tool, not a decision authority.

---

## 9. Honest limitations

I cannot run AnyLogic, so this is a specification, not a tested model, and there is no `.alp` to hand over. The chemistry coefficients are placeholders until Stage 1 calibration. The Fluid Library's linear solver is correct for hydraulics but is not where chemistry belongs, and mixing the two up is the standard failure. Pypeline is unsupported and adds overhead; ONNX export must be verified for the specific estimator; the OPC UA integration is custom Java with version constraints to check. None of these is a blocker, but each is a real task with a real risk, and the build sequence above is ordered so that each is retired before the next depends on it.

---

## 10. Bridge to Phases 6 and 7

Phase 6 evaluates nanobubbles and the dissolved-oxygen and energy extensions, which would enter this blueprint as additional System Dynamics stocks (dissolved oxygen, oxidation) and a Fluid or energy accounting layer, only once an instrumented pilot justifies them. Phase 7 turns the Layer 2 PLC and OPC UA integration and the sensor-scarcity workarounds into the concrete commissioning plan: the minimum viable sensor set per parameter, the soft-sensor and lab-fusion options, and the staged cutover from shadow to advisory to supervised closed loop.

---

## Sources

Vendor facts verified against AnyLogic documentation and repositories, June 2026:
- AnyLogic editions and the Fluid Library (anylogic.com/downloads, anylogic.com/features/libraries/fluid-library): Fluid Library in Professional and University Researcher; PLE limited in libraries, model size, and a five-hour run limit.
- Fluid Library mechanics (anylogic.help Fluid Library reference): LP solver, discrete-rate piecewise-constant flows, recommendation to use System Dynamics for non-linear feedback.
- Pypeline (anylogic.com/features/artificial-intelligence/pypeline, anylogic.help, GitHub the-anylogic-company/AnyLogic-Pypeline): free, open-source, third-party, any licence, local Python 3, runtime overhead, no support guarantee.
- OPC UA in AnyLogic via a Java SDK (Prosys forum integration report; Eclipse Milo as the open-source alternative): no native block, custom Java, JDK and SDK version constraints to verify.

Evidence and method carried from earlier phases:
- Yang et al. (2026), doi:10.2139/ssrn.6330967 (coagulant saving range).
- Dunnington et al. (2021), doi:10.1021/acsestengg.0c00053 (machine-learning models extrapolate poorly; keep a physically based fallback).
