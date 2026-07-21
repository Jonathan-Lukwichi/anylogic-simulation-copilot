# Pattern card — Trauma Center
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Evaluate staffing levels, triage routing, and care-pathway alternatives in a dual-track (Express Care + Emergency Department) hospital to reduce patient length of stay.

## Block chain
Patients arrive via a time-of-day-scheduled Source and are immediately split by a SelectOutput acting as an acuity/triage gate. Lower-acuity patients route into the Express Care (EC) track; higher-acuity patients enter the Emergency Department (ED) track. Each track contains its own chain of Seize → MoveTo → Delay/Service → Release steps representing registration, triage assessment, room assignment, examination, diagnostic procedures (X-ray, lab, CAT, ultrasound), treatment, and discharge or admission. Multiple SelectOutput blocks handle conditional branching (e.g., needs X-ray vs. does not, discharged vs. admitted). A Sink absorbs patients at the end of each path.

## Resources
Multiple named ResourcePools, each with schedule-driven capacity:
- EC staff (physicians assistants, specialists, nurses)
- ED staff (doctors, specialists, nurses)
- Diagnostic equipment pools (X-ray, portable X-ray, CAT, ultrasound)
- Bed attractors used for spatial MoveTo steps
All pools support capacity schedules so shift changes alter available headcount dynamically during a run.

## Key settings worth copying
- **Time unit:** Minutes (fine-grained enough for clinical workflows)
- **Arrival rate:** Schedule-based (varies by hour of day to reflect the known 40,000+ visits/year pattern)
- **Service durations:** Parametric `triangular(min, mean, max)` distributions for every step — triage, registration, room prep, examination, each diagnostic modality, treatment, and discharge — driven by named parameters so experiments can sweep them without touching logic
- **Routing probabilities:** SelectOutput conditions read patient attributes (acuity class, required diagnostics) set at arrival
- **Experiment variants:** Bedside registration toggle, EC operating hours extension, staffing schedule redesign — each is a separate scenario parameter set

## KPIs instrumented
- Length of Stay in EC (minutes) — histogram + statistics
- Length of Stay in ED (minutes) — histogram + statistics
- Resource utilisation per pool
- Queue lengths at each Seize block
- Throughput (patients discharged vs. admitted)

## Reusable idea
**Parametric triangular distributions as a scenario lever:** Every service step stores its min/mean/max as named model parameters rather than hard-coded literals. Switching between baseline and optimistic staffing scenarios then requires only a parameter table change, not logic edits — making the model ideal for rapid "what-if" experimentation across clinical process redesigns.
