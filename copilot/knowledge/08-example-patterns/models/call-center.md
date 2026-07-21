# Pattern card — Call Center
- **Source:** AnyLogic example (models) — distilled, original wording
- **Paradigm:** DES
- **Problem it solves:** Sizing a two-skill contact centre so that queue lengths and service levels stay within target for two independent call types.

## Block chain
Calls of two distinct types arrive independently following Poisson processes (rates ArrivalRate1, ArrivalRate2). Each type enters its own dedicated Service block backed by a separate agent pool (NAgents1, NAgents2). While waiting, a caller may abandon after an exponentially distributed patience time (mean AbandonmentTime1 or AbandonmentTime2). Once seized by an agent the actual handling time is drawn from a triangular distribution centred on the configured mean service time, with a lower bound of half that mean and an upper bound of 1.5× the mean — giving a realistic asymmetric spread without requiring historical fit. Service time also depends on which agent group handles the call (assignedAgent attribute checked at seize). Calls that complete service exit to a Sink; abandoners are also routed to a Sink and counted separately. A live visual shows the current queue depth for each type using layered indicator objects that become visible at thresholds (10, 40, 100, 200 callers).

## Resources
- **Agent pool 1:** NAgents1 operators (parameter, default configurable via experiment slider)
- **Agent pool 2:** NAgents2 operators (separate pool, same structure)
- No shared cross-skill routing — each pool serves only its call type

## Key settings worth copying
- **Arrival:** Poisson inter-arrival, rate = ArrivalRate1 / ArrivalRate2 (calls/second, model time unit = Second)
- **Patience / abandonment:** `exponential(1 / AbandonmentTime)` timeout on the queue inside each Service block — set via `onEnterDelay` action
- **Service duration:** `triangular(ServiceTime / 2, ServiceTime, ServiceTime * 1.5)` — easy to parameterise from a single mean value
- **Agent-type branching:** `call.assignedAgent` attribute set on entry; service-time function switches on this value so the same block can model skill-based handling differences
- **Experiment parameters:** ArrivalRate1, ArrivalRate2, AbandonmentTime1, AbandonmentTime2, NAgents1, NAgents2 all exposed as sliders for what-if runs

## KPIs instrumented
- **Queue length:** `service1.queueSize()` and `service2.queueSize()` plotted as time-series charts and shown as threshold-based visual indicators on the canvas
- **Service level:** fraction of calls answered within a target wait (tracked per call type; description text references "service level" as the primary output metric)
- Implicit throughput via Sink entry counts (abandoned vs served can be derived)

## Reusable idea
Encode caller patience as an exponential timeout *inside* the Service block's queue phase (the `onEnterDelay` hook) rather than with a separate SelectOutput/Delay/Sink bypass. This keeps the flowchart compact — one Service block handles waiting, abandonment, and service — while still letting you tune mean patience independently per call segment. The triangular service-time trick (half-mean to 1.5× mean) is a quick, parameter-free way to introduce realistic variability whenever you only know the target average handling time.
