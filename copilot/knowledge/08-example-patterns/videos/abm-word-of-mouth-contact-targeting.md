# Pattern card — Word-of-mouth contacts in ABM: who `sendToRandom` reaches, and how the recipient choice sets the adoption law
- **Source:** AnyLogic video "AnyLogic ABM Tutorial Part 5 | Adding Word of Mouth Effect" (https://youtu.be/sAQ0BOf5XgM) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Make an agent-based word-of-mouth mechanism produce the aggregate law you intend (the Bass imitation term), and keep it correct when more agent types join the model.

## Mechanism
The wiring is already in the KB (3-days Market model, Phase 4, pp. 65–69):
- **Parameters** in `Consumer`: `ContactRate` = 1 per day and `AdoptionFraction` = 0.01.
- **Contact:** an internal transition inside `User`, with Rate `ContactRate` and Action `sendToRandom("Buy")`.
- **WOM:** a transition from `PotentialUser` to `User`, Triggered by the Message `"Buy"`, with Guard `randomTrue(AdoptionFraction)`.
- A message that reaches an agent in any other state is dropped (G21).

**The aggregate law it implies.** Write U for users, P for potential users and N for all consumers:
1. Each of the U users sends c contacts a day to consumers chosen uniformly at random.
2. A share P/N of those contacts lands on potential users.
3. Each one converts with probability i.

Word-of-mouth adoption therefore runs at c·i·U·P/N per day. That is the SD Bass term in `basicmodels/bass-diffusion-phase-1.md`, with the Bass imitation coefficient q = c·i (not i alone). The dropped messages are what create the P/N saturation factor.

The recipient call decides the law (Help 8.9.9, *Communication between agents*):

| Call (inside `Consumer`) | Who can receive | Word-of-mouth adoption flow |
|---|---|---|
| `sendToRandom("Buy")` | any agent in the sender's **space**, i.e. every population and single agent embedded in Main; the Help documents `send(msg, RANDOM)` as including the sender itself | c·i·U·P/(all agents in the space), diluted as soon as Main holds other agents |
| `send("Buy", randomFrom(main.consumers))` or `send("Buy", randomFrom(getPopulation()))` | own population only | c·i·U·P/N (Bass), whatever else lives in Main |
| `send("Buy", randomWhere(main.consumers, x -> x.inState(Consumer.PotentialUser)))` | potential users only | c·i·U while any are left: adoption does not slow as the pool empties and then stops abruptly. This is a targeted-referral law, not Bass. |
| `sendToRandomConnected("Buy")` | agents linked by the network | network diffusion; depends on the layout |
| `sendToRandomNeighbor("Buy")` | neighbouring cells; discrete space only (runtime error elsewhere, Help *Troubleshooting*) | local diffusion |

## Resources
n/a

## Key settings worth copying
- **Calibrating from a fitted Bass curve** (p and q per time unit): the ad rate is p, and `ContactRate × AdoptionFraction` is q. Fix one of the two from data and derive the other.
- **Where to put the conversion check.** A Guard on the receiver (`randomTrue(AdoptionFraction)`, as in the video) gives the same law as a check on the sender before sending, as long as the parameters are the same for everyone (with per-agent values, a receiver-side guard models susceptibility and a sender-side check persuasiveness — see `abm-wom-conversion-rate-vs-probability.md`). The receiver-side guard also lets persuadability vary by potential user.
- **`randomWhere(...)` returns `null`** when nothing matches (Help). Test for it before calling `send(...)`.

## KPIs instrumented
The video charts the state counts on a stack chart. A cheap check is to count `"Buy"` messages received in `PotentialUser` per day and compare the count with c·U·P/N.

## Pitfalls
- **Silent dilution.** Adding retailers, a competitor's agents or trucks to Main slows word of mouth under `sendToRandom`, and the model reports no error. The new agent types also receive `"Buy"` messages. The 3-days book says the recipient is chosen "from the same population" (p. 66). That holds only while consumers are alone in the space.
- **An innocent-looking efficiency change.** Filtering the recipients to potential users (the Help's own example) changes the model's law, not just its speed.
- **Sending from Main.** Message functions called from Main fail with "Environment must be defined" (G22).

## Reusable idea
Every contact mechanism implies an aggregate rate law. Write it down (for example c·i·U·P/N) before you choose the send call. As face validation, run the SD Bass model (`sdmodels/bass-model.md`) with the same p and with q = c·i. With a large population, the ABM's mean curve over replications should track it.

## When the co-pilot should use this
- Building or reviewing diffusion, epidemic, rumour or referral ABMs that use messages.
- Extending a single-population ABM with more agent types (supply chain, competitors, retailers).
- Calibrating an ABM to a Bass fit, or explaining why an ABM and an SD version of the "same" model diverge.
