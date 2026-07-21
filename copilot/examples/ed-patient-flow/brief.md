# Example brief — Emergency Department patient flow

Build a DES model: patients arrive, are triaged (nurse), treated (doctor), then discharged or admitted.
Decision lever: staffing capacity (doctors/nurses), parameterised.
Goal: compare static staffing (baseline) vs ML-forecast-driven dynamic staffing.
KPIs: average wait time, length of stay, resource utilisation, throughput, % seen within target, cost.
Data: arrival log (see sample-data.csv placeholder); fit interarrival + service distributions.
