# Brief — Mini emergency department (2D + 3D demo)

> A demonstration model, built on 2026-10-02 to show model generation (workflow/model-generation.md).
> The numbers are illustrative assumptions, not data from any hospital.

## Purpose
Show a complete AnyLogic model built from a written spec: process logic, a 2D floor plan, a 3D view and a live
dashboard — generated as a file, then opened and run in AnyLogic 8.9.10 PLE.

## Process
| Step | Who / what | Time (minutes) | Where |
|---|---|---|---|
| Arrive | Patients, Poisson, `arrivalRate` = 8 per hour | — | Entrance (left wall) |
| Wait for triage | queue for a nurse | — | Waiting room (triage) |
| Triage | 1 of `numNurses` = 2 nurses | triangular(4, 7, 12) | Triage room, 2 positions |
| Wait for a doctor | queue for a doctor | — | Waiting room (doctor) |
| Treatment | 1 of `numDoctors` = 4 doctors | triangular(10, 20, 40) | Treatment bays, 4 beds |
| Leave | admitted with `admitProbability` = 0.25, else home | walking | To wards (right) / Exit (left) |

Patients walk between areas at uniform(0.6, 0.9) m/s in straight lines. Staff stay at their stations.

## Layout (10 px = 1 m)
Building 47 m × 29 m: waiting rooms 14 × 12 m (two), triage 12 × 12 m, doctors' station 11.5 × 12 m, treatment
25.5 × 12 m with 4 beds; walls 1.2 m high with gaps at the entrance, the exit and the ward corridor.

## KPIs on screen
Arrived, waiting for triage, waiting for a doctor, in treatment, admitted, gone home, average time in the ED;
time plot of the two queues and patients in treatment (12-hour window); bar chart of nurse and doctor
utilisation; a day/clock display.

## Hand calculation (to check the run against)
- Nurses: ρ = 8/h × 7.67 min / (2 × 60 min) = 0.51.
- Doctors: ρ = 8/h × 23.3 min / (4 × 60 min) = 0.78.
- Admitted share ≈ 0.25. Average time in the ED ≈ 7.7 + 23.3 min of service + walking + queueing ≈ 35–45 min.

## Run settings
Time unit minutes; one day (1,440 min); real-time scale 0.5 (raise it with the speed control); fixed seed 1.
