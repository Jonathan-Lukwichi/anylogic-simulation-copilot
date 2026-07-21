# Pattern card — Ward Medication Management
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (SD + ABM)
- **Problem it solves:** Evaluating hospital medication-error-reduction interventions across interacting yearly, weekly, and hourly time scales.

## Block chain
The model couples two sub-models with bidirectional feedback. The SD layer tracks slow-moving system stocks over years: drug formulary complexity (Drugs_under_Consideration conveyor → Drugs_on_List stock), staff headcount (hires/quit flows driven by turnover rate and adverse-effect burden), staff knowledge (Actual_Known_Info stock fed by inc_info/decr_info flows), incident reporting maturity (Reported_Incidents → Unanalysed_reports → Analysed_reports pipeline), and implemented preventative strategies accumulating at a rate governed by how many analysed reports exist relative to a complexity-scaled threshold. The AB layer runs at daily resolution: doctor, nurse, pharmacist, and specialist agent types move through a stylised medication management workflow; prescribing and administration checks act as "Swiss cheese" layers that intercept errors before they reach the patient. Outcomes from the AB layer (ADEs, intercepted errors) feed back into the SD stocks (total_ADEs, Actual_Reporting_fraction) which in turn reshape agent error-generation probabilities via lookup tables.

## Resources
- **Agent populations:** Doctor (Junior/Registrar/Senior), Nurse, ClinicalNurseConsultant, NurseUnitManager, Pharmacist — counts driven by SD Staff stock and turnover parameters.
- **SD stocks acting as capacity proxies:** Staff (headcount), IT_Communications_Status (0–1 index), Implemented_Preventative_strategies (integer count).
- No explicit ResourcePool/Seize/Release blocks; resource constraints are implicit through agent availability and ward bed counts.

## Key settings worth copying
- **Time unit:** Day; SD equations are scaled to years internally (flows divided by 365 or multiplied by `year()` helper).
- **Complexity growth:** `Complexity_growth_rate_% = 5` — formulary complexity grows 5% per year, compounding the information gap.
- **Error-rate multipliers:** Two lookup tables modulate error generation — `impact_of_info_gap_on_error_rate(Information_gap)` and `Impact_of_drug_mix_on_error_rate(Ave_drugs_per_patient)` — multiplied together with a calibration coefficient.
- **Strategy implementation delay:** Conditional: 5 time units when strategies are still lagging, 2 when caught up (`if Possible > Implemented then 5 else 2`).
- **Reporting fraction:** Modelled as a stock (`Actual_Reporting_fraction`) with a gradual adjustment flow (`chg_report_frac`), capturing cultural inertia in incident reporting.
- **Info decay:** `decr_info` flow removes staff knowledge at a rate combining turnover and information obsolescence (Ave_useful_life parameter).

## KPIs instrumented
- `total_ADEs` (cumulative adverse drug events stock)
- `Intercepted_SMes` and `Non_Intercepted_SMEs` (significant medication errors, split by interception stage)
- `ADEs` variable (current rate)
- `adverse_event_%` (proportion of patients harmed)
- `Staff_Trained_%` and `Information_gap` (leading indicators of future error risk)
- Animated "Swiss cheese" panel showing real-time interception layers

## Reusable idea
Bidirectional SD–ABM coupling with table-driven multipliers: define slow system-level stocks (staff knowledge, reporting culture, formulary complexity) in an SD layer, then use lookup tables to translate those aggregate stocks into per-agent error probabilities in the ABM layer, and route aggregated ABM outcomes back into SD flows. This lets a single model span policy-horizon (years) and operational (daily) questions without duplicating logic at either scale.
