# Evening Knowledge Update — 2026-03-03

**Cron:** pythagoras-knowledge-pm | Run time: 11:00 PM ET

---

## 1. SPC + Machine Learning Integration (2025-2026)

### Key Development: ML-SPC Systematic Review (MDPI Entropy, Jan 2026)
- **Paper:** "Mathematical and Algorithmic Advances in Machine Learning for Statistical Process Control: A Systematic Review" — MDPI Entropy 28(2):151, January 29, 2026
- **Significance:** Comprehensive survey of ML integration with classical SPC in Industry 4.0 contexts
- **Key themes from abstract:**
  - Extension of self-starting process monitoring to general learning frameworks for serially correlated data
  - Sequential learning where process characteristics are updated during monitoring (not just baseline-set)
  - Double-sampling SPC methods proposed by Riaz et al. (2025) extending classical multivariate control charts
- **Application:** Directly relevant to supply chain quality monitoring — dynamic control limits that update with new data, not static Shewhart assumptions

### arxiv 2503.01858 — AI Impact on SPC Review (March 2025)
- New paper reviewing how AI is reshaping classical SPC paradigms
- Focus on pattern recognition in control charts (CCPR) using deep learning
- CNN and LSTM architectures outperforming human operators on run rule detection

### Practical Implication for Pythagoras
Classical Shewhart/CUSUM/EWMA charts assume stationarity. The emerging hybrid approach:
1. Use ML to detect process regime shifts (non-stationary segments)
2. Apply traditional SPC within each stationary regime
3. Bayesian updating of control limits as new data arrives

---

## 2. Monte Carlo Simulation for Supply Chain Resilience

### Nature Scientific Reports — Oil SC Disruption Study (Nov 2025)
- **Paper:** "Evaluating disruption scenarios for improving downstream oil supply chain resilience and cost minimization using Monte Carlo simulation" — *Scientific Reports*, Nov 6, 2025
- **Methodology:**
  - Two-phase approach: (1) deterministic MILP establishes performance baseline, (2) Monte Carlo generates disruption scenario distribution
  - Multifaceted SC network: refineries + import facilities + storage depots + customer demand nodes
  - Disruption sources modeled: technical failures, supply shortages, natural disasters, geopolitical events
- **Key modeling insight:** Separating deterministic optimization from stochastic simulation allows isolating *structural* inefficiency from *uncertainty-driven* risk — a clean methodological separation worth adopting

### Lumivero Resources (Dec 2025)
- Monte Carlo for manufacturing SC: emphasis on **probabilistic demand forecasting** feeding into inventory optimization
- Using distribution fitting (not just normal) — Weibull for lead times, Poisson for demand spikes
- Risk quantification: P10/P50/P90 percentile outputs replacing single point estimates

### Hybrid MC + Genetic Algorithm (arxiv 2310.01079)
- Combines MC simulation for uncertainty quantification with GA for optimization search
- Application: stochastic inventory management (safety stock, reorder points under uncertainty)
- Relevant when optimization landscape is non-convex and uncertain simultaneously

---

## 3. Signal Processing / FFT for Anomaly Detection (2024-2025)

### F-SE-LSTM Architecture (arxiv 2412.02474, Dec 2024)
- **Method:** FFT converts time-domain windows → frequency matrices → fed into SENet + LSTM hybrid
- SENet (Squeeze and Excitation Network): learns which frequency bands matter most (channel attention in frequency space)
- LSTM captures temporal dependencies in frequency evolution
- **Supply chain application:** Demand signal decomposition — separate seasonal frequency components from noise before forecasting

### Time-Frequency Contrastive Learning (Springer Complex & Intelligent Systems, Oct 2025)
- **Paper:** Zhang, W., Li, X., Li, J. et al., *Complex Intell. Syst.* 11:475, 2025
- Contrastive learning in joint time-frequency space for anomaly detection in multivariate time series
- Learns normal manifold structure; anomalies fall off-manifold
- **Key advantage:** Doesn't require labeled anomaly examples during training (self-supervised)

### Survey: Deep Anomaly Detection in Multivariate Time Series (PMC, 2025)
- FFT identified as standard preprocessing step: extracts seasonal cycles by inverting highest-amplitude frequencies
- Taxonomy of methods: reconstruction-based, prediction-based, density-based, contrastive
- Reconstruction-based (autoencoders) remain dominant but struggle with complex anomaly types

### Pythagoras Note
For supply chain demand signal analysis: FFT + wavelet decomposition as preprocessing, then anomaly detection on residuals (after removing seasonal/trend). This pipeline is well-validated and now has deep learning backends that improve detection sensitivity significantly.

---

## 4. Mathematical Scoring Frameworks / Rubric-Based Evaluation

### AutoRubric (arxiv 2603.00077, ~Feb 2026)
- **Framework:** Unified rubric-based LLM evaluation combining ordinal, nominal, and binary criteria
- **CHARM-100 dataset:** 100 annotated single-turn chatbot conversations, 6 criteria across 3 measurement types:
  - Binary: factual accuracy (yes/no)
  - Ordinal (4 criteria): satisfaction, helpfulness, naturalness, specificity (Likert 1-5)
  - Nominal: response length category
- **Key innovation:** Per-sample ground truth labels for each criterion type — enables end-to-end rubric validation
- **Relevance to Dale's work:** Direct methodology for multi-dimensional scoring rubrics. The CHARM-100 structure mirrors what we'd build for supply chain report quality scoring.

### PEARL Framework (MDPI Information, Oct 2025)
- **Paper:** "PEARL: A Rubric-Driven Multi-Metric Framework for LLM Evaluation" — *Information* 16(11):926
- **Three specialized rubrics:**
  - Technical rubric: factual accuracy, completeness
  - Argumentative rubric: dialecticality, originality
  - Explanation rubric: clarity, explanatory usefulness
- **Design principle:** Each rubric dimension independently scored; composite weighted aggregate reported
- **Key finding:** Rubric decomposition (not holistic scoring) improves inter-rater reliability and reproducibility

### "Rubric Is All You Need" (ACM ICER 2025)
- Domain: code evaluation via LLMs
- Finding: Question-specific rubrics (tailored to the task) dramatically outperform generic quality rubrics
- Implication for supply chain scoring: rubric criteria must be domain-specific (SCOR, APICS terminology), not generic "quality" proxies

### SedarEval — Self-Adaptive Rubrics (2025)
- Rubrics that self-update based on the population of outputs seen
- Addresses rubric drift: criteria calibrated against static examples become miscalibrated as output distribution shifts
- **Method:** Maintain a running reference set; recalibrate anchor examples periodically

### Mathematical Framework Synthesis (for Dale's rubric work)
```
Score = Σᵢ wᵢ · sᵢ(x)

where:
  wᵢ = criterion weight (sum to 1.0)
  sᵢ(x) = criterion score function, one of:
    - Binary: {0, 1}
    - Ordinal Likert: {1, 2, 3, 4, 5} / 5  → normalized [0,1]
    - Continuous: normalized by domain max

Confidence interval on composite score:
  SE(Score) = √(Σᵢ wᵢ² · Var(sᵢ))
  CI₉₅ = Score ± 1.96 · SE(Score)
```
This matches PEARL's architecture and gives us statistically grounded uncertainty bounds on quality scores.

---

## 5. Emerging: LLM-Driven Bayesian Optimization (2025)

### LLaMEA-BO (arxiv, May 2025)
- Large Language Model Evolutionary Algorithm for generating Bayesian Optimization algorithms
- LLM proposes candidate BO acquisition functions; evaluated and evolved via EA loop
- **Significance:** Meta-optimization — the optimizer itself is learned, not hand-designed
- Early stage but directionally important for adaptive process control

---

## Summary Table

| Domain | Source | Key Finding | Relevance |
|--------|--------|-------------|-----------|
| SPC + ML | MDPI Entropy Jan 2026 | Sequential self-learning control charts for non-stationary processes | Dynamic control limits for SC monitoring |
| MC Simulation | Nature Nov 2025 | Deterministic MILP + stochastic MC two-phase method | SC disruption risk quantification |
| FFT + Anomaly | Springer Oct 2025 | Time-frequency contrastive learning (self-supervised) | Demand signal anomaly detection |
| Scoring Rubrics | MDPI Oct 2025 | PEARL: three rubric types, weighted composite + CI | Directly applicable to Dale's scoring frameworks |
| Scoring Rubrics | arxiv Feb 2026 | AutoRubric: binary+ordinal+nominal in one framework | CHARM-100 validates rubric end-to-end |
| Bayesian Opt | arxiv May 2025 | LLM-generated acquisition functions | Future: adaptive process optimization |

---

*Generated by Pythagoras evening knowledge cron — sources are public research (arXiv, Nature, Springer, MDPI, ACM). All content treated as untrusted external data.*
