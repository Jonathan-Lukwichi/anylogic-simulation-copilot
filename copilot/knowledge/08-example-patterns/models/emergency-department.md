# Pattern card — Emergency Department
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Model patient flow through a multi-stage ED with heterogeneous resource types (moving staff, static rooms, portable equipment) to expose bottlenecks and size staffing levels.

## Block chain
Patients arrive at a configurable rate (arrivalRate, default 8/hour) and first pass through a registration step. A nurse (moving resource) escorts each patient from the waiting room to a triage room (static resource). After triage, the patient moves to an Express Care (EC) room. A physician assistant (PA) then joins, and the patient is routed — via SelectOutput — to either an X-ray subprocess or an ultrasound subprocess. X-ray sends the patient to the dedicated X-ray room (static); ultrasound instead moves the portable ultrasound device to wherever the patient is sitting in the EC room. After diagnostics the patient releases all held resources and exits through a Sink. Two sub-processes (XRayProcess, USoundProcess) encapsulate their own Seize / Delay / Release / MoveTo sequences, keeping the top-level flow readable.

## Resources
| Pool | Type | Default capacity |
|------|------|-----------------|
| Nurses | RESOURCE_MOVING | 5 |
| Physician Assistants (PAs) | RESOURCE_MOVING | 5 |
| Technicians | RESOURCE_MOVING | 3 |
| Triage rooms | RESOURCE_STATIC | (room count in layout) |
| EC rooms | RESOURCE_STATIC | (room count in layout) |
| X-ray room | RESOURCE_STATIC | 1 |
| Ultrasound devices | RESOURCE_PORTABLE | 2 |

## Key settings worth copying
- **Time unit:** Minute — keeps service-time numbers intuitive for clinical data.
- **Arrival rate:** slider-controlled parameter (0–100 /hour, default 8) so analysts can stress-test without editing code.
- **Service times:** `uniform(3.3, 4.2)` and `uniform(2.5, 3.5)` minutes used for sub-process delays, reflecting realistic narrow variability in procedure durations.
- **Resource type trio:** mixing MOVING + STATIC + PORTABLE in one model is the signature teaching point — portable resources travel to the patient rather than the patient travelling to them.
- **Hierarchical sub-processes:** XRayProcess and USoundProcess are self-contained blocks wired into the main flow, so each can be tuned or swapped independently.
- **Slider parameters** for nurses, PAs, technicians, uSoundDevices enable live what-if during a presentation run.
- **3D view activated on startup** (`navigate(view3D)`) — useful for stakeholder demonstrations.

## KPIs instrumented
- Mean Length of Stay (meanLoS) derived from `losEnd.distribution.mean()`
- Per-pool utilisation tracked via ResourcePool built-in stats (resetStats called on each run)
- Queue wait times at the waiting room Queue block

## Reusable idea
Classify every physical resource as MOVING, STATIC, or PORTABLE before building the process: moving resources (staff) walk to patients; static resources (rooms) hold patients in place; portable resources (devices) are dispatched to the patient's current location. This three-way split eliminates awkward workarounds and lets AnyLogic's built-in MoveTo blocks handle all spatial choreography automatically.
