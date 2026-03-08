# Knowledge Update — 2026-03-07 (Evening)
**Cron:** pythagoras-knowledge-pm | Run time: 11:00 PM ET

---

## 1. Generalized Bayes for Causal Inference
**Paper:** arXiv:2603.03035 — *"Generalized Bayes for Causal Inference"* (Mar 2026, stat.ML)
**Authors:** Multiple, submitted ~March 5, 2026

**Core contribution:** A new framework that avoids the fundamental problem of standard Bayesian causal inference — having to specify a full probabilistic model for high-dimensional nuisance components (propensity scores, outcome regressions). Instead:

- **Priors are placed directly on causal estimands** (ATE, CATE), not on the data-generating process
- **Identification-driven loss function** replaces the likelihood — the posterior is updated using a loss derived from causal identification assumptions (e.g., Neyman-orthogonal meta-learners)
- **Turns any loss-based causal estimator into a fully uncertainty-quantified estimator** — existing pipelines (e.g., DML, R-learner) get Bayesian posteriors with no re-architecture
- For Neyman-orthogonal losses: generalized posteriors converge to oracle counterparts and are **robust to first-stage nuisance estimation error** even when nuisance models converge at sub-parametric rates
- Calibration step provides valid frequentist uncertainty coverage despite non-parametric nuisance

**Why this matters:** Supply chain causal attribution (e.g., "what is the causal effect of this policy on lead time?") is typically observational and noisy. Standard Bayesian approaches require specifying priors over high-dimensional propensity and outcome models — error-prone and brittle. This framework lets you place priors directly on what you care about (the effect) and use modern ML to handle the nuisance. First flexible framework of its type.

**Relevance to Dale's work:** High — any scoring or model that needs causal effect estimates with honest uncertainty bounds (not just point estimates) could use this. CATE (Conditional Average Treatment Effect) is directly applicable to supplier evaluation or intervention analysis.

---

## 2. Rulers: Locked Rubrics & Evidence-Anchored Scoring
**Paper:** arXiv:2601.08654 — *"Rulers: Rubric Unification, Locking, and Evidence-anchored Robust Scoring"* (Jan 13, 2026)
**Authors:** Yihan Hong (WashU), Huaiyuan Yao, Bolin Shen, et al. (ASU, FSU)
**Code:** https://github.com/LabRAI/Rulers

**Core contribution:** Reframes LLM-as-a-Judge alignment as a **criteria transfer problem** and identifies three failure modes:
1. **Rubric instability** — score changes with superficial prompt rephrasing
2. **Unverifiable reasoning** — no auditable evidence trail for score assignments
3. **Scale misalignment** — LLM scoring scales don't match human grading boundaries

**Rulers architecture:**
- **Compiler phase:** Transforms natural-language rubrics into versioned, immutable executable specifications ("locked rubrics")
- **Executor phase:** Structured decoding with deterministic evidence verification — the model must cite specific evidence tokens for each criterion score
- **Calibration phase:** Lightweight Wasserstein-based post-hoc calibration of the output distribution to human grading boundaries — no model fine-tuning required

**Results:** Significantly outperforms baselines in human agreement; maintains stability against adversarial rubric perturbations; enables smaller models to rival larger proprietary judges.

**Key insight:** Reliable LLM judging requires *executable rubrics* and *verifiable evidence*, not better prompt phrasing.

**Relevance to Dale's work:** Very High — this is directly applicable to any AI-in-the-loop scoring system. The "locked rubric + evidence verification" pattern is the mathematical formalization of what quality scoring needs. Wasserstein calibration is implementable with scipy.

---

## 3. Autorubric: Unified Framework for Rubric-Based LLM Evaluation
**Paper:** arXiv:2603.00077 — *"Autorubric: A Unified Framework for Rubric-Based LLM Evaluation"* (Mar 2026)
**Authors:** Delip Rao, Chris Callison-Burch (University of Pennsylvania)

**Core contribution:** Synthesizes scattered rubric evaluation techniques into a single open-source Python framework:

- **Criterion types:** Binary, ordinal, and nominal criteria with configurable weights
- **Aggregation modes:** Single-judge and multi-judge ensemble (majority, weighted, unanimous, any-vote)
- **Few-shot calibration** with verdict-balanced sampling (avoids class imbalance skewing calibration)
- **Bias mitigations:**
  - Position bias → option shuffling
  - Verbosity bias → length penalties
  - Criterion conflation → per-criterion atomic evaluation with natural language explanations
- **Reliability metrics:** Cohen's κ, weighted κ, correlation coefficients, distribution-level tests
- **Production infrastructure:** Response caching, checkpointing with resumable runs, multi-provider rate limiting, cost tracking

**New dataset:** CHARM-100 — 100-sample chatbot evaluation dataset with per-sample ground truth across binary, ordinal, and nominal criteria. Designed to stress-test rubric frameworks on heterogeneous criterion types.

**Key finding:** Combining few-shot calibration + ensemble judging + criterion-level atomicity outperforms any single mitigation in isolation.

**Relevance to Dale's work:** High — Autorubric provides the production infrastructure layer that Rulers provides the mathematical foundation for. Together they define the current state of the art for programmatic rubric-based scoring. Worth monitoring for direct implementation.

---

## 4. AutoSCORE: Multi-Agent Structured Rubric Scoring
**Paper:** arXiv:2509.21910 — *"AutoSCORE: Enhancing Automated Scoring with Multi-Agent LLMs via Structured Component Recognition"* (Sep 2025)

**Core contribution:** Two-agent architecture for automated short-answer scoring:
- **Agent 1 (Extraction):** Identifies rubric-relevant components in student responses, encodes them into a structured representation
- **Agent 2 (Scoring):** Uses the structured representation (not the raw text) to assign scores

**Results on ASAP benchmark:** Works across GPT-4o, LLaMA-3.1-8B, LLaMA-3.1-70B. Key finding: structured intermediate representation significantly improves interpretability and robustness vs. direct LLM scoring. Smaller open-source models perform competitively when given structured input.

**Relevance to Dale's work:** The two-agent extraction → scoring pattern generalizes beyond education assessment. Any supply chain quality checklist or SOW evaluation could use this decomposition.

---

## 5. Digital Twin AI: LLM → World Model Integration
**Paper:** arXiv:2601.01321 — *"Digital Twin AI: Opportunities and Challenges from LLMs to World Models"* (Jan 4, 2026)

**Key technical developments:**
- **Graph Neural Networks (GNNs) for supply chain DTs:** Learn representations over structured dependencies, enabling simulation of flow, fault propagation, and system-level optimization
- **LLMs as reasoning layers** on top of simulation models — not replacing physics-based simulation but providing natural-language interfaces and hypothesis generation
- **World models:** The next evolution — DTs that can simulate counterfactuals ("what happens if this supplier fails?") using learned world dynamics, not just physics equations

**Practical relevance:** Discrete event simulation (DES) embedded in a digital twin can now receive structured queries via LLM interface. DES generates the scenario; LLM interprets and recommends. This is the architectural direction for AI-in-the-loop supply chain simulation.

---

## 6. Optimization: DESGD — Dual Enhanced SGD
**Paper:** Nature Scientific Reports s41598-025-24689-y (Nov 2025)
**Title:** *"A dual enhanced stochastic gradient descent method with dynamic momentum and step size adaptation"*

**Core contribution:** DESGD addresses the main weaknesses of SGD-with-momentum (SGDM) — oscillation in ill-conditioned loss landscapes, poor adaptation to loss geometry:
- **Dynamic momentum adaptation:** Momentum coefficient adjusts based on local loss surface curvature (vs. fixed β in SGDM/Adam)
- **Dynamic step size adaptation:** Step size co-adapted on the same update rules as momentum — not independent like Adam's second moment estimate
- **Theoretical guarantee:** Stable descent behavior and convergence demonstrated for non-convex objectives

**Why this matters for supply chain optimization:** Inventory optimization, routing, and demand model training are typically non-convex. DESGD's co-adaptation of momentum and step size offers better convergence on the kinds of irregular loss surfaces common in supply chain ML models.

---

## 7. Compressed Sensing for MRI / Sparse Recovery (CS + Basis Pursuit)
**Paper:** MDPI Sensors 25(16):5137 (Aug 2025)
**Title:** *"Sparse Transform and Compressed Sensing Methods to Improve Efficiency and Quality in Magnetic Resonance Medical Imaging"*

**Most relevant finding for signal processing KB:**
- **Basis pursuit (BP)** satisfies formal CS theory requirements: incoherent sampling + sparse recovery via nonlinear reconstruction
- **Evaluation metrics that generalize:** PSNR, RMSE, SSIM, execution time, memory usage, compression efficiency — this is a clean evaluation rubric for any sparse signal recovery method
- At varying sampling rates: BP outperforms simpler methods (DCT + thresholding) on SSIM at low sample counts; classical methods remain competitive at higher sampling rates

**Signal processing implication:** The BP vs. threshold tradeoff has a crossover point. For heavily under-sampled data (IoT sensors with missing readings), basis pursuit's formal guarantees are worth the compute cost. Above ~40% sampling rate, simpler methods are competitive and much faster.

---

## Summary Table

| Domain | Finding | Relevance |
|--------|---------|-----------|
| Statistical Modeling | Generalized Bayes for Causal Inference — priors on estimands, not nuisance | High — observational supply chain causality |
| Scoring Frameworks | Rulers: locked rubrics + evidence verification + Wasserstein calibration | Very High — direct application to scoring systems |
| Scoring Frameworks | Autorubric: unified open-source rubric framework with bias mitigations | High — production implementation reference |
| Scoring Frameworks | AutoSCORE: two-agent extraction → scoring architecture | Medium-High — pattern generalizes to SC checklists |
| Simulation | Digital Twin AI: GNN + LLM + DES for supply chain counterfactuals | Medium — architectural direction for SC DT |
| Optimization | DESGD: dual adaptive momentum + step size for non-convex optimization | Medium — relevant to SC ML model training |
| Signal Processing | CS + Basis Pursuit tradeoffs: SSIM crossover at ~40% sampling rate | Medium — useful for IoT/sensor data contexts |

---

*Next scheduled update: 2026-03-08 (AM or PM cron)*
