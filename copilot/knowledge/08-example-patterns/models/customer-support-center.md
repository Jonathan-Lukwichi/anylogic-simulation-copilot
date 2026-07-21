# Pattern card — Customer Support Center
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** Hybrid (DES + ABM)
- **Problem it solves:** Staff a multi-tier technical support operation handling three contact channels (phone, email, fax) with skill-based escalation and agent career progression.

## Block chain
Requests arrive on three channels — phone calls, emails, and faxes — each with its own exponential inter-arrival rate modulated by a monthly seasonality factor and an optional night-shift multiplier. Priority is strict: calls are answered first, emails second, faxes last.

Every incoming request enters at Level 1 support. If unresolved, it escalates to Level 2 (split into software and hardware specialisations) and then to Level 3 if needed. A request classified as Level 3 complexity jumps directly from Level 1 to Level 3, bypassing Level 2. A phone call waiting for escalation cannot be placed on hold in a queue; the Level 1 agent must stay on the line until a higher-level agent becomes free, then hand off.

Employees are modelled as agents with a career-level attribute (0–3). Level 0 agents are trainees who study for a configurable period before promoting to Level 1. Each level has its own retirement rate, and newly hired agents can start at any configured level. The model tracks how many agents sit at each level and specialisation at any moment, enabling what-if staffing experiments.

## Resources
- Employee agents at four levels: Level 0 (trainee), Level 1 (generalist), Level 2-SW (software), Level 2-HW (hardware), Level 3 (senior)
- Initial headcount per tier is a configurable parameter
- No shared ResourcePool block; capacity is managed through agent population counts per level

## Key settings worth copying
- Arrival rate formula: `exponential(baseRate * nightMultiplier * monthRate(month))` — combines a Poisson process with a seasonal index and a binary schedule toggle
- Service times: `uniform(0.5, 0.7)` hours for some handling steps
- Promotion delay per level: "time studying" parameter (hours)
- Retirement rates differ per level — higher turnover at lower levels
- Time unit: Hour

## KPIs instrumented
- Requests resolved at each level (counters per level)
- Queue lengths at each support tier (bar charts)
- Number of employees per level over time (time plots)
- Arrival rate datasets for email and fax channels across the year

## Reusable idea
Modulate a Poisson arrival rate with a pre-computed monthly index array (`monthRate(month)`) multiplied by a schedule-driven scalar. This single compound expression gives realistic seasonality and shift-based demand variation without needing separate Source blocks per time period — one Source per channel is enough.
