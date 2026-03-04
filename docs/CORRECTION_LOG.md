# CORRECTION_LOG.md — Signal Triage for Agent Learning
_Established 2026-03-03. Shared protocol across all agents._

## How It Works

Before any correction becomes a permanent rule or KB update, it gets logged here.

**Triage tags:**
- `durable` — repeatable pattern, applies broadly, should become a rule
- `contextual` — right call for that situation, not a general rule
- `evaluator-error` — the agent was actually correct; discard
- `ambiguous` — log it, watch for more instances

**Promotion threshold:** 2+ instances of the same pattern = promote to permanent rule/KB update.

One correction is a data point. Two is a signal.

---

## Log

| date | agent | correction | tag | instances | promoted | notes |
|---|---|---|---|---|---|---|
| 2026-03-03 | Iris | No em dashes in any writing | durable | 3+ | yes — SOUL.md | Dale's non-negotiable |
| 2026-03-03 | Iris | No double dashes in any writing | durable | 3+ | yes — SOUL.md | Dale's non-negotiable |
| 2026-03-03 | Iris | No listicle headers in LinkedIn posts | durable | 2+ | yes — rubric | Repeatedly flagged |
| 2026-03-03 | All | Opinion Strength + Challenge Factor are primary repost drivers | durable | 2 | yes — rubric v3/v4 | Post 5 confirmed via outcome data |
| 2026-03-03 | All | Subagent timeout for Pythagoras = 300s | durable | 2 | yes — AGENTS.md | Timed out twice at 120s |

---

## Calibration Schedule

- **Now:** Log all corrections before applying them
- **n=10 posts:** Pythagoras checks Factor A vs repost_rate correlation
- **n=30 posts:** Pythagoras runs full regression, replaces assumed rubric weights with empirical ones
- **30 days:** Review correction log — which single-instance tags got confirmed, which got overturned

---

## Notes

Keep this simple. The goal is data, not process.
If logging a correction feels like more work than just fixing it, the log is too complex.
