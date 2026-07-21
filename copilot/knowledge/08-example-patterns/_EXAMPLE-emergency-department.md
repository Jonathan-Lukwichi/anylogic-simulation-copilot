# Pattern card — Emergency department patient flow

- **Source:** AnyLogic examples, Healthcare category (distilled, original wording)
- **Paradigm:** DES (discrete-event)
- **Problem it solves:** how staffing levels affect patient waiting time and length of stay

## Block chain
Source (patient arrivals) -> Service (triage, seizes a nurse) -> Service (treatment, seizes
a doctor) -> SelectOutput (discharge vs admit) -> two Sinks (counts).

## Resources
ResourcePool for nurses and ResourcePool for doctors; capacities held in variables so they
can be driven by a schedule (the decision lever).

## Key settings worth copying
Interarrival as a rate schedule (captures day/night swing); service times as fitted
distributions; SelectOutput by probability or patient attribute; TimeMeasure pairs around
treatment (wait) and Source->Sink (length of stay).

## KPIs instrumented
Average wait time, length of stay, doctor/nurse utilisation, treatment queue length,
throughput per hour, % seen within target, cost per shift.

## Reusable idea
Parameterise the decision lever (staffing) so the same model serves baseline, ML-driven, and
RL-driven scenarios without a rebuild.
