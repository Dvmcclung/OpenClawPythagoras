# LinkedIn Post Outcomes Tracker
_For rubric v4 calibration. Update at 7 days post-publish._

## Posts Log

| post_id | date | topic | v4_total | factor_a | factor_b | factor_c | impressions | reach | reactions | comments | reposts | eng_rate | repost_rate | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P04 | 2026-03-02 | Data quality / confident bad results | TBD | TBD | TBD | TBD | 93 | 47 | 1 | 0 | 0 | 1.1% | 0.0% | Lower engagement; v2 score 56/60 but weaker hook and challenge |
| P05 | 2026-03-03 | AI knowledge gap / "Nobody else has your twenty years" | 59 | ~30 | ~20 | ~12 | 111 | 53 | 4 | 1 | 1 | 5.4% | 0.9% | Best performer so far. Hook concrete, challenge named directly, quotable line landed |

_Note: P04 needs v4 rescoring. v2 score listed as placeholder._

---

## Calibration Notes

**2026-03-03 (n=2):**
- Post 5 outperformed Post 4 on all metrics despite similar or lower v2 rubric score
- Engagement rate: P05 = 5.4% vs P04 = 1.1% (5x difference)
- Repost rate: P05 = 0.9% vs P04 = 0.0%
- Key differentiators in P05: concrete action hook, named assumption challenged, personal quotable line
- Directionally supports v3/v4 upweighting of Opinion Strength and Challenge Factor
- **Confidence: LOW** (n=2). Monitor closely.

**Next calibration checkpoint: n=10**
- Check: does Factor A score correlate with repost_rate? (target r > 0.5)

**First empirical weight calibration: n=30**
- Run regression of factor scores vs engagement_rate and repost_rate
- Replace assumed weights with regression coefficients

---

## How to Log a New Post

1. Score the post with Iris using rubric v4
2. Add a row immediately with scores and publication date
3. Return at 7 days and fill in the outcome columns
4. Add a notes entry under Calibration Notes with key observations
5. At n=10 and n=30 checkpoints, trigger Pythagoras to run the calibration analysis

