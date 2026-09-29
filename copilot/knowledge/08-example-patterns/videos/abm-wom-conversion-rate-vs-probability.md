# Pattern card — Word-of-mouth conversion in ABM: per-contact probability vs per-day rate, and whose value it is
- **Source:** AnyLogic video "Part 3: Scenario 1 – ABM- What Agent Parameters Really Mean" (https://youtu.be/nKW8GG5og4U) — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Wire contact rate and adoption fraction so word of mouth has the strength and heterogeneity you intend, and spot the version that counts the contact rate twice.

## Mechanism
In Part 3 of this third-party series, the words are right:
- ads convert about 1.5 % of potential users a day (0.015 × 5,000 ≈ 75 on day 1);
- each user makes 1.2 contacts a day;
- a contacted potential user adopts with probability `adoptionFraction`, drawn per consumer from `uniform(0.1, 0.25)` (mean 0.175).

Word-of-mouth adoption is therefore about users × c × i per day, times the share of recipients who are still potential users (the law and the recipient choice are in `videos/abm-word-of-mouth-contact-targeting.md`).

Part 4 then wires it wrongly. The sender has an internal transition in `UserB` with Rate `contactRate` and Action `sendToRandom("buyB")`. The receiver has Guard `randomTrue(adoptionFractionB * contactRate)`. The contact rate c is applied twice.

**Two valid designs. Use exactly one:**

| Design | Sender (internal transition in UserX) | Receiver (PotentialUser → WantX, Message "buyX") | KB source |
|---|---|---|---|
| Receiver guard | Rate `c`, Action `sendToRandom("buyA")` | Guard `randomTrue(i)` | 3-days pp. 67–68 |
| Thinned sender | Rate `c * i`, same Action | no guard | Borshchev & Filippov 2004, pp. 10–11 |

With homogeneous parameters both give c·i·U·P/N. The thinned design simulates only successful contacts, so it creates a factor 1/i fewer events.

**Whose value it is.** A guard is evaluated in the receiver, so there `i` is the receiver's own draw: **susceptibility**. In the thinned design `i` belongs to the sender: **persuasiveness**. Borshchev & Filippov (p. 12) make it depend on time since purchase. With per-agent random draws, as in this series, the two are different models:
- Receiver-side: the most susceptible adopt first, so late word of mouth runs below what the mean 0.175 predicts.
- Sender-side: no such depletion.

This is a standard heterogeneity effect and is not discussed in the video. For per-sender persuasiveness with the receiver-guard wiring, decide at the sender with `if (randomTrue(persuasiveness)) sendToRandom("buyA");` and leave the receiver unguarded.

## Resources
n/a

## Key settings worth copying
- `randomTrue(p)` is defined as `uniform() < p` (Javadoc 8.9.9, `UtilitiesRandom`), so p ≥ 1 raises no error: it is simply always true.
  - The video's product 0.25 × 1.2 = 0.3 stays below 1 but inflates word of mouth by 20 %.
  - With the KB's Bass values (c = 100, i = 0.015; `basicmodels/bass-diffusion-phase-3.md`) the product is 1.5, and every contact converts.
- Units: c is per model time unit (the Rate field's unit); i is dimensionless. q = c·i is a rate.
- Population-wizard parameters with a distribution are drawn once per agent at creation (`videos/custom-empirical-distribution-agent-attributes.md`). Place the draw where the behaviour belongs: receiver or sender.

## KPIs instrumented
Count "buyX" messages received in PotentialUser per day, and conversions per day. Their ratio is the realised adoption fraction; with a receiver guard it should sit near the mean of i early in the run. Compare message volume with U·c·P/N.

## Pitfalls
- **The double count (the video).** Word of mouth runs c times too strong, and a calibrated q no longer reproduces the S-curve timing.
- **Sensitivity analysis on c.** In the double-counted wiring, varying c changes both contact frequency and per-contact probability, so its sensitivity result is meaningless.
- **Silent saturation.** Assert `p <= 1` on any computed probability. Use `min(1, p)` only if saturation is intended.

## Reusable idea
A rate belongs to a timer; a probability belongs to a decision at one event. When a rate and a probability meet in one expression, check whether the rate is already in some timer.

## When the co-pilot should use this
- Building or reviewing contact-based ABMs (word of mouth, infection, rumours, referrals) that use `randomTrue` guards.
- Calibrating to Bass p and q.
- Giving agents heterogeneous adoption or infection parameters.
- Related: `videos/abm-word-of-mouth-contact-targeting.md` (who receives); 3-days pp. 65–69; `knowledge/.pdf-text/00-method-selection/borshchev-filippov-2004-sds-to-abm.txt` pp. 6, 10–12.
