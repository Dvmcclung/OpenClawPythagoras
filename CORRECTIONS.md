# CORRECTIONS.md — Signal Triage Log
**Agent:** Pythagoras (mathematics/statistics specialist)  
**Purpose:** Track errors, calibrate defaults, and decide what to promote to training files.

---

## How to Use This File

### Feedback Classification (Signal vs. Noise)

| Tag | Meaning | Action |
|-----|---------|--------|
| `[CARRIER]` | Permanent signal — recurring error in method selection or statistical reasoning | Promote to training file after 2-3 confirmed recurrences |
| `[MODULATION]` | Task-local — specific adjustment for this problem only | Do NOT propagate |
| `[CALIBRATION]` | Updates an analytical default — significance threshold, visualization choice, etc. | Update default after 2-3 recurrences |

### Category Tags

| Tag | Covers |
|-----|--------|
| `[METHOD]` | Wrong statistical method or test chosen |
| `[FRAMEWORK]` | Wrong analytical framework (frequentist vs Bayesian, etc.) |
| `[FORMAT]` | Output presentation — tables, charts, precision level |
| `[SCOPE]` | Wrong level of mathematical depth for the audience |
| `[INTERP]` | Misread the data question or decision context |
| `[TONE]` | Too technical/academic, not practical enough |
| `[STRUCTURE]` | Analysis flow, assumption checking order |

### Promotion Rule

Only promote after 2-3 independent recurrences of same category + type.
Cite which KB file the update was applied to.

---

## Pending (< 3 occurrences — hold, do not promote)

---

## Confirmed (>= 3 occurrences — promote to training file)

---

## Weekly Frequency Tally
_Rolling 2-week window._

| Category | Week 1 | Week 2 | Notes |
|----------|--------|--------|-------|
| [METHOD] | 0 | 0 | |
| [FRAMEWORK] | 0 | 0 | |
| [FORMAT] | 0 | 0 | |
| [SCOPE] | 0 | 0 | |
| [INTERP] | 0 | 0 | |
| [TONE] | 0 | 0 | |
| [STRUCTURE] | 0 | 0 | |

---

## Noise Archive (one-offs, not recurring)
