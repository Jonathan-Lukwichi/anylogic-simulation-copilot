# Pattern card — Bank Office - Phase 3
- **Source:** AnyLogic example (basicmodels) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Models a multi-channel bank with two service streams (tellers and a self-service ATM path), probabilistic routing, and a shared teller resource pool to analyse queue build-up and staff utilisation.

## Block chain
Customers arrive at a fixed rate and immediately hit a **SelectOutput** router that probabilistically splits them between two lanes. One lane leads to a waiting **Queue** then into a **Service** block backed by the shared teller **ResourcePool**; the other lane routes customers to a self-service area modelled with a standalone **Delay**. A second **SelectOutput** downstream handles any further branching (e.g. re-join or exit). Both lanes eventually drain into a **Sink**. A separate **Delay** block (with triangular duration) represents the ATM transaction time, and the teller **Service** block uses its own triangular service-time distribution. The entity type flowing through the network is a **Customer** agent.

## Resources
- **ResourcePool `tellers`**: capacity = 4 (teller agents of type `Teller`)
- Customer agent population pre-allocated up to 100 instances (array-list backed)

## Key settings worth copying
- **Arrival rate:** 0.3 per minute (constant; no schedule attached)
- **Time unit:** Minutes
- **Teller service time:** `triangular(2.5, 6, 11)` minutes — captures the wide spread of real counter transactions
- **ATM/self-service delay:** `triangular(0.8, 1.5, 3.5)` minutes — faster and narrower spread
- **Routing:** `SelectOutput` with `choiceIsVolatile = true` and a probability parameter, allowing the split ratio to be changed at runtime without restarting the model
- **Queue capacity:** explicit capacity parameter (finite buffer before tellers)

## KPIs instrumented
- Queue length and waiting time at the teller queue
- Teller resource utilisation (busy fraction of the 4-unit pool)
- Throughput (customers reaching Sink per unit time)
- Mean time in system (implicitly tracked via entity statistics on Sink)

## Reusable idea
The key transferable trick is pairing **`choiceIsVolatile = true`** on `SelectOutput` with a runtime-editable probability parameter: this lets you experiment with different self-service adoption rates during a live simulation run without resetting, making it easy to sweep scenarios interactively. Combine this with triangular distributions (min, mode, max) instead of exponential for service times whenever subject-matter experts can estimate best/worst/typical values — a far more defensible input than assuming memoryless service.
