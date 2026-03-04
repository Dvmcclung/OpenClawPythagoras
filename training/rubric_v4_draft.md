# LinkedIn Rubric v4 — Calibration-Ready, Outcome-Anchored
_Drafted by Pythagoras (𝚷), 2026-03-03_
_Based on v3 (Iris) + first outcome data from Posts 4 and 5_

---

## Design Philosophy

v3 was expert intuition encoded as weights. v4 is expert intuition with a calibration mechanism.

The two data points we have already tell a directional story:
- Post 5 (59/70 v3) outperformed Post 4 (56/60 v2) on every metric: +19% impressions, +13% reach, 4x reactions, plus 1 repost and 1 comment
- Post 5's advantages: concrete action hook, direct challenge to a named assumption, personal quotable line ("Nobody else has your twenty years")
- This confirms v3's upweighting of Opinion Strength and Challenge Factor was directionally correct

**Confidence note:** n=2 is not calibration. It's a signal. Treat v4 weights as informed priors, not empirical facts. First real calibration at n=20-30.

---

## Factor Structure (Hypothesized, to be validated with PCA at n=20+)

Three underlying factors likely drive post performance:

**Factor A — Provocation** (predicts reposts and comments)
- Opinion Strength / Voice
- Challenge Factor
- Core Claim Clarity

**Factor B — Connection** (predicts reactions and saves)
- Hook
- Repost Identity Fit
- Human Signal

**Factor C — Execution** (predicts reach via algorithmic distribution)
- LinkedIn Mechanics
- AI Smell (penalty)
- Narrative Arc

When n=20+: run PCA on dimension scores. If three factors emerge as hypothesized, replace individual dimension scores with factor scores as the primary quality signal.

---

## Scoring Dimensions

**Total: 75 points + penalties**
**Current target: 58+/75**
**Repost-optimized target: Factor A score 30+/35**

---

### Factor A — Provocation (35 pts)

#### Opinion Strength / Voice (15 pts)
Does the post take a specific, committed position someone would amplify?

- 1-5: Information without stance. "On one hand..."
- 6-9: Has a point of view but hedges
- 10-13: Clear conviction, specific claim
- 14-15: Arguable claim at full commitment -- someone who disagrees would respond; someone who agrees shares immediately

_Post 5 example (14/15):_ "Models are commodities. The gap is the knowledge you bring." No hedge.

#### Challenge Factor (12 pts)
Does it name and push back on a real, widespread assumption?

- 1-4: Confirms existing beliefs
- 5-7: Nuance without confrontation
- 8-10: Names the assumption and argues against it
- 11-12: Directly confronts a widely-held behavior ("Everyone is focused on which AI model to use") with evidence and a specific alternative

_Post 5 example (11/12):_ Opens by naming the wrong question, then reframes it completely.

#### Core Claim Clarity (8 pts)
One defensible thesis the whole post orbits.

- 1-3: Collection of observations, no center
- 4-6: Main idea exists but diluted
- 7-8: Single sentence states the position; everything else is evidence

---

### Factor B — Connection (25 pts)

#### Hook (10 pts)
First 2-3 lines earn the read.

- 1-4: Generic, could be anyone
- 5-7: Creates curiosity but doesn't fully commit
- 8-9: Stops the scroll with a bold claim or concrete detail
- 10: Reader has no choice but to continue

_Post 5 example (9/10):_ "I built three specialist agents today. No vendor. No data science team. One day." Concrete, surprising, rhythm.

#### Repost Identity Fit (10 pts)
Does sharing this enhance the sharer's professional identity?

- 1-4: Too niche or too generic
- 5-7: Relevant but not distinctive
- 8-9: Specific enough to signal expertise, broad enough to travel
- 10: Supply chain exec, ops leader, or thoughtful generalist gains social capital by amplifying it

#### Narrative Arc (5 pts)
Setup, conflict, resolution -- reader feels the structure without seeing it.

- 1-2: Analytical essay, no narrative shape
- 3-4: Some tension, flat resolution
- 5: Clear tension-pivot-payoff

---

### Factor C — Execution (15 pts)

#### LinkedIn Mechanics (8 pts)
Format hygiene. Short paragraphs, mobile-readable, no structural crutches.

- 1-4: Wall of text, header-dependent
- 5-6: Mostly clean
- 7-8: Fully clean, closes with opinionated statement or resonant question

#### Narrative Efficiency (7 pts)
Every paragraph advances the argument. Nothing restates what was already said.

- 1-3: Repetitive, padding, meandering middle
- 4-5: Mostly efficient, one weak section
- 6-7: Every paragraph earns its place

---

### Penalties

**AI Smell: -5 to 0**
- 0: No red flags
- -2: Minor patterns (mild anaphora, over-structured transitions)
- -5: Obvious tells (em dashes, listicle headers, "it is worth noting," generic CTA)

**Hard rule violations (Dale): -3 each**
- Em dash used
- Double dash used
- Listicle header used

---

## Outcome Tracking Fields

Every scored post must have these fields logged in rubric_v4_outcomes_tracker.md:

| Field | Description |
|---|---|
| post_id | Sequential number |
| date_published | YYYY-MM-DD |
| topic | One-line description |
| v4_total | Total score /75 |
| factor_a | Provocation score /35 |
| factor_b | Connection score /25 |
| factor_c | Execution score /15 |
| impressions_7d | LinkedIn impressions at 7 days |
| reach_7d | Members reached at 7 days |
| reactions_7d | Total reactions at 7 days |
| comments_7d | Comments at 7 days |
| reposts_7d | Reposts at 7 days |
| engagement_rate | (reactions + comments + reposts) / impressions |
| repost_rate | reposts / impressions |
| notes | What worked, what didn't |

---

## Calibration Roadmap

**Now (n=2):** Use v4 as informed prior. Factor A weight is directionally supported.

**At n=10:** Check correlation between Factor A score and repost_rate. If r > 0.5, weight is confirmed. If not, investigate.

**At n=20:** Run PCA on 7 dimension scores. Validate or revise factor structure.

**At n=30:** Run regression of factor scores against engagement_rate and repost_rate. Replace assumed weights with regression coefficients. This is the first true empirical calibration.

**Ongoing:** Each new batch of outcome data is a Bayesian update. The weights are distributions, not constants. The rubric improves every time a post ships.

---

## v3 → v4 Changes

| Change | Reason |
|---|---|
| Added Factor structure | Organizes dimensions by what they predict |
| Opinion Strength stays 15 pts | Confirmed by Post 5 data |
| Challenge Factor raised to 12 pts | Post 5's key differentiator |
| Narrative Arc reduced to 5 pts | Execution detail, not primary driver |
| Added Narrative Efficiency (7 pts) | New -- redundancy kills posts |
| Outcome tracking fields added | Required for calibration |
| Calibration roadmap added | Rubric must learn |

