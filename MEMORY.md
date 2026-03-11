# MEMORY.md — Long-Term Memory (Curated)
_Initialized 2026-03-03._

## Identity
- **Agent name:** Pythagoras (𝚷)
- **Human:** Dale McClung (he/him), America/New_York
- **Role:** Team mathematics expert. Modeling, simulation, SPC, Fourier analysis, Monte Carlo, vector analysis.

## Purpose
Build next-generation rubric and checklist systems grounded in mathematical rigor. Bring quantitative backbone to agent learning and quality scoring.

## Key Decisions
- Plain language first, derivation on request
- Useful math only -- simplest method that solves the problem
- Uncertainty must be quantified, not hedged

## Research Findings (Active)

### Scoring & Rubric Architecture
- **Rulers** (arXiv:2601.08654, Jan 2026): Locked executable rubrics + evidence-anchored scoring + Wasserstein post-hoc calibration. Best current framework for AI-in-the-loop scoring. Directly applicable to Dale's work. Code: https://github.com/LabRAI/Rulers
- **Autorubric** (arXiv:2603.00077, Mar 2026): Unified Python framework for rubric-based LLM evaluation. Handles binary/ordinal/nominal criteria, multi-judge ensembles, Cohen's κ reliability, position/verbosity bias mitigations.
- **Key principle:** Reliable LLM judging requires *executable rubrics + verifiable evidence*, not better prompt phrasing.

### Causal Inference
- **Generalized Bayes for Causal Inference** (arXiv:2603.03035, Mar 2026): Place priors directly on causal estimands (ATE, CATE), not data-generating process. Turns any loss-based causal estimator (DML, R-learner) into fully uncertainty-quantified estimator. Robust to nuisance estimation error. Applicable to supplier evaluation and intervention analysis.

### Vector Search / Living Memory (2026-03-06)
- First real Living Memory Architecture validation: clean domain separation confirmed; vector universality holds despite corpus bias in initial testing.

## Team Roster (as of 2026-03-10)
- **Thea** (main): orchestration, research, writing, PM
- **Iris**: communications, editorial, writing coach
- **Supply Chain Guru**: APICS, LSS, Gartner domain knowledge
- **Pythagoras (me)**: math, modeling, simulation, SPC, Fourier, Monte Carlo, vector analysis
- **Forge 🔧** (added 2026-03-10): programmer/engineer agent; workspace ~/.openclaw/forge-workspace; model openai/gpt-5.1-codex; agent ID: forge
- **Luma 🎨** (added 2026-03-10): visual artist/design agent; workspace ~/.openclaw/luma-workspace; model claude-sonnet-4-6; agent ID: luma

## Task History (Significant)
| Date | Task | Output |
|------|------|--------|
| 2026-03-06 | Living Memory Architecture validation addendum v1 | papers/living_memory_addendum_v1.md |
| 2026-03-07 | PM knowledge update: optimization, signal processing, statistical modeling, simulation, scoring frameworks | training/mathematics/KNOWLEDGE_UPDATE_2026-03-07.md |
