# Evening Knowledge Update — 2026-03-08
**Cron:** pythagoras-knowledge-pm | Run time: 11:00 PM ET

---

## 1. Stochastic Optimization: Inventory at Scale (C3 AI / arXiv 2502.11213)

**Source:** arXiv:2502.11213 — *"Stochastic Optimization of Inventory at Large-scale Supply Chains"* — Zhaoyang Larry Jin et al. (C3 AI), Feb 2025

**Key contribution:**
MRP systems fundamentally fail to handle modern supply chain uncertainty because they treat inventory settings as deterministic. This paper reformulates MRP safety-stock decisions as a **constrained stochastic optimization**:

- Minimizes holding cost + stockout cost subject to a pre-defined service-level constraint
- Finds optimal reorder parameters via simulation-optimization (not closed-form)
- Optimal params can feed back into existing MRP systems — no rip-and-replace required
- **Reported results:** 10–35% inventory reduction, hundreds of millions in economic benefit at global enterprise scale

**Method scaffold:**
```
Stochastic Sim-Opt:
  Decision vars: reorder point (r), order quantity (Q)
  Objective: min E[holding cost + backorder cost]
  Subject to: P(service level ≥ target)
  Solver: simulation-based gradient or stochastic decomposition (SD)
```

**Relevance (high):** Directly applicable to supply chain work. The service-level constraint formulation is more defensible than ad-hoc safety stock rules.

---

## 2. Stochastic Optimization: Capacity Markets with Storage (arXiv 2603.02404)

**Source:** arXiv:2603.02404 — *"Stochastic Optimization for Resource Adequacy in Capacity Markets with Storage and Renewables"* — Baptiste Rabecq et al. Accepted IEEE PES General Meeting 2026.

**Key contribution:**
Storage assets couple decisions across time, which invalidates traditional time-independent capacity demand curves. The paper formulates capacity procurement as a **two-stage stochastic program**:

- Stage 1: capacity decision (first stage, before uncertainty resolves)
- Stage 2: dispatch problem (second stage, conditional on realized uncertainty)
- Uncertainty sources: generator failures (Markov chain), temporally correlated renewable output, stochastic load
- Solved via **stochastic decomposition (SD)** algorithm with up to 20,000 Monte Carlo samples

**Methodological insight:**
> "Convergence for the stochastic program happens faster than reliable estimation of the reliability metrics, which require more samples than are used in typical stochastic programs."

This is a subtle and important point: **the optimization converges before the reliability estimate converges.** More samples are needed for KPI accuracy than for solution stability. Directly applicable when using Monte Carlo to estimate tail risk alongside optimization.

**System scale:** 305 generators on New England grid. Validates tractability at real-world scale.

---

## 3. Monte Carlo Acceleration: Neural-Guided Importance Sampling (arXiv 2602.12294)

**Source:** arXiv:2602.12294 — *"Accelerated Markov Chain Monte Carlo Simulation via Neural Network-Driven Importance Sampling"* — Feb 2026

**Key contribution:**
MCMC is bottle-necked by rare transitions between metastable states. This paper introduces:

1. **Neural network bias potential** — a learned function that amplifies sampling of rare transition events while preserving relative probabilities
2. **Branching random walk (BRW)** technique — further reduces variance
3. Validated on 2D and 14D systems; claims accuracy and scalability

**Why it matters for simulation practice:**
- Traditional importance sampling requires expert-designed proposals; neural net replaces this
- The BRW + neural bias combination is a 2026 standard variance reduction pattern to watch
- Material science context, but the method generalizes to any rare-event Monte Carlo (supply chain disruption simulation, financial tail risk)

**Status:** New pattern, not yet validated in supply chain context — flag as **provisional**

---

## 4. Scoring & Rubric Frameworks: RULERS (arXiv 2601.08654)

**Source:** arXiv:2601.08654 — *"RULERS: Rubric Unification, Locking, and Evidence-anchored Robust Scoring"* — Hong et al., Jan 2026. GitHub: https://github.com/LabRAI/Rulers.git

**Problem framing:**
LLM-as-Judge scoring fails due to three recurrent failure modes:
1. **Rubric instability** — prompt sensitivity causes inconsistent scores
2. **Unverifiable reasoning** — no auditable evidence trail
3. **Scale misalignment** — LLM grade boundaries don't match human standards

**RULERS solution:**
- **Compile rubrics** into versioned, immutable bundles ("locked rubrics")
- **Structured decoding** with deterministic evidence verification (each score point requires a text evidence match)
- **Wasserstein-based calibration** — lightweight post-hoc scale alignment, no model fine-tuning

**Benchmark results:** Outperforms baselines on human agreement; smaller models rival larger proprietary judges when RULERS is applied.

**Practical implication for Dale's scoring work:**
If building rubric-based scoring systems, the "locked rubric + evidence anchor" pattern is the current best practice for reproducibility. Wasserstein calibration is the right tool for aligning LLM probability outputs to human-scale scoring distributions.

---

## 5. Scoring & Rubric Frameworks: Autorubric (arXiv 2603.00077)

**Source:** arXiv:2603.00077 — *"Autorubric: A Unified Framework for Rubric-Based LLM Evaluation"* — Feb 2026. Open-source Python.

**What it unifies:**
Autorubric is the first framework to collect and implement all known rubric evaluation techniques under one API:

| Feature | Detail |
|---------|--------|
| Criterion types | Binary, ordinal, nominal |
| Weights | Configurable per criterion |
| Judge modes | Single, majority-vote ensemble, weighted ensemble, unanimous, any-vote |
| Calibration | Few-shot with verdict-balanced sampling |
| Bias mitigations | Option shuffling (position bias), length penalties (verbosity bias), per-criterion atomic eval (conflation) |
| Reliability metrics | Cohen's κ, weighted κ, correlation coefficients, distribution-level tests |
| Infrastructure | Caching, checkpointing, multi-provider rate limiting, cost tracking |

**CHARM-100 benchmark:** New 100-sample chatbot evaluation dataset with per-sample ground truth across binary + ordinal + nominal criteria. First dataset designed to stress-test heterogeneous rubric frameworks.

**Relevance (very high):** Autorubric is the production-ready toolkit for Dale's rubric scoring system work. The psychometric reliability metrics (Cohen's κ, weighted κ) provide the statistical rigor to validate that rubric scores are meaningful.

---

## 6. Signal Processing: Two-Step Bandpass + Deep Learning for Time Series Anomaly Detection (MDPI Applied Sciences, Jun 2025)

**Source:** MDPI Applied Sciences 15(11):6254 — *"Time Series Anomaly Detection Using Signal Processing and Deep Learning"* — Jun 2025

**Method:**
1. Apply **bandpass filter** to reduce noise (classic signal processing, not ML)
2. Pass filtered signal to deep learning model for anomaly classification

**Why this matters:**
Traditional DL anomaly detection treats all frequency components equally. Bandpass filtering is a principled pre-processing step that:
- Removes DC offset and high-frequency noise
- Focuses DL on the signal band of interest
- Reduces model complexity and false positive rate

**Supply chain application:** IoT sensor data for equipment monitoring, cold chain compliance signals, demand signal filtering before forecasting.

---

## 7. Vector Embeddings in 2026: Multi-Index Pattern

**Source:** Encord — *"Complete Guide to Embeddings in 2026"* — Dr. Andreas Heindl, Dec 2025

**Key 2026 architectural pattern: "Multi-index embeddings"**
- Keep multiple embeddings per item (global image embedding + object crop embeddings + caption/text embedding + domain-specific embedding)
- Build separate FAISS/vector DB indices per embedding type
- Retrieval: query across indices, then rerank

**Workflow paradigm for 2026:**
```
Indexing + storage → Retrieval + ranking → Monitoring + drift detection → Refresh cycle
```

**Monitoring note:** "Detect drift, measure retrieval quality, refresh embeddings when models/data change" — embedding drift is now a first-class operational concern, not an afterthought.

**Practical note:** Multi-index requires careful namespace management in the vector DB. LanceDB (in use here) supports this natively with table-per-embedding-type.

---

## Summary Table

| Domain | Finding | Relevance | Confidence |
|--------|---------|-----------|------------|
| Stochastic Opt | Sim-opt for inventory (C3 AI): 10-35% reduction at scale | Very High | High |
| Stochastic Opt | Two-stage SCP: convergence faster than reliability estimation | High | High |
| Monte Carlo | Neural-guided MCMC importance sampling + BRW variance reduction | Medium | Provisional |
| Scoring/Rubric | RULERS: locked rubrics + evidence anchors + Wasserstein calibration | Very High | High |
| Scoring/Rubric | Autorubric: unified framework with psychometric reliability metrics | Very High | High |
| Signal Processing | Bandpass pre-filtering before DL anomaly detection | Medium | High |
| Vector Analysis | Multi-index embeddings as 2026 standard pattern; drift monitoring | High | High |

---

*Update generated: 2026-03-08 23:00 ET by pythagoras-knowledge-pm cron*
