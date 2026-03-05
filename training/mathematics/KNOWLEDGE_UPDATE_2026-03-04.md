# Knowledge Update — March 4, 2026 (PM)

*Pythagoras evening knowledge refresh. Topics: SPC/AI integration, supply chain simulation, scoring frameworks, signal processing anomaly detection, demand forecasting.*

---

## 1. AI-Enhanced Statistical Process Monitoring (SPM → SMPC)

**Key paper:** arXiv:2503.01858 — *"A Review of Artificial Intelligence Impacting Statistical Process Monitoring and Future Directions"* (Feb 2025, 44 pages)

**Summary:**
This is the most important recent synthesis in the SPC space. 100 years since Shewhart introduced SPC, this review maps where AI is taking the field. Key findings:

- **AI methods being applied to SPM:** ANN, CNN, RNN, GAN — primarily for control chart pattern recognition (CCPR) and histogram pattern recognition (HPR)
- **Application categories:** univariate, multivariate, profile monitoring, image-based quality
- **The destination:** *Smart Process Control (SMPC)* — autonomous corrective action, not just detection
- **Large Multimodal Models (LMMs):** identified as the next frontier for SPM in complex systems

**Relevance for Dale:** The trajectory is SPC + ML = autonomous quality control. The math is still classical (control limits, Cpk, Western Electric rules), but detection is increasingly ML-assisted. Worth tracking for supply chain quality scoring models.

---

## 2. Industry 4.0 Smart SPC Framework

**Source:** MDPI Applied System Innovation (2024) — *"Industry 4.0 and Smart Systems in Manufacturing: Guidelines for the Implementation of a Smart Statistical Digital Systems"*

**Key points:**
- Framework for integrating smart statistical digital systems into existing manufacturing control systems
- Provides practical migration guidelines (not just theoretical)
- Bridges classical SPC and digital/sensor-driven monitoring

**Note:** This is a practitioner-oriented framework, useful when translating SPC theory into actual implementation recommendations.

---

## 3. Monte Carlo Simulation for Supply Chain Risk (Recent Applications)

**Sources:** Lumivero (Dec 2025) + IEEE/Springer historical baselines

**Current state of practice (2025-2026):**
- Monte Carlo is well-established for supply chain risk quantification: lead time variability, demand uncertainty, supplier disruption probability
- The active frontier is **hybrid methods**: MC + genetic algorithms (NSGA-II) for multi-objective optimization (cost vs. service level vs. inventory)
- **NSGA-II + Monte Carlo** (simulation-optimization) is increasingly the standard for multi-echelon supply chain design under uncertainty

**Key concept — Taguchi parameter tuning for NSGA-II:**
Using Taguchi design-of-experiments to find optimal NSGA-II control parameters before running the full optimization. Reduces computational cost significantly.

**Practical note:** For supply chain simulation work with Dale, the MC + NSGA-II stack is the current best practice for problems with ≥2 competing objectives.

---

## 4. Demand Forecasting: Foundation Models & Ensemble Methods (2025)

**Key paper:** arXiv:2507.22053 — *"Foundation Models for Demand Forecasting via Dual-Strategy Ensembling"* (KDD '25 Workshop: AI for Supply Chain)

**Summary:**
- Foundation/transformer models are now achieving state-of-the-art accuracy on retail demand, energy load, and financial time series
- **Dual-strategy ensembling:** combines forecast-then-optimize with direct prediction approaches
- Transfer learning from large pre-trained time series models (e.g., TimesFM, Chronos) is viable even with limited training data

**MCDFN Architecture (arXiv:2405.15598):**
- Multi-Channel Data Fusion Network: CNN + LSTM + GRU in parallel channels
- Extracts both spatial and temporal features from the same time series
- Superior to single-architecture approaches on demand forecasting benchmarks

**Practical guidance:**
- For short history / sparse SKUs: foundation model + transfer learning
- For long history / stable SKUs: classical ARIMA/ETS still competitive and interpretable
- For complex multi-driver demand: MCDFN or similar multi-channel DL

---

## 5. Signal Processing: Lightweight Edge AI for Anomaly Detection

**Source:** MDPI Sensors 25(21):6629 (Oct 2025) — *"Lightweight Signal Processing and Edge AI for Real-Time Anomaly Detection in IoT Sensor Networks"*

**Source:** arXiv:2601.03085 (Jan 2026) — *"Real-Time Adaptive Anomaly Detection in Industrial IoT Environments"*

**Key themes:**
- **Edge deployment** is the direction: models small enough to run on IoT hardware, not requiring cloud round-trips
- Lightweight FFT + feature extraction → small classifier is the dominant pattern for vibrational/acoustic anomaly detection
- Adaptive models that retrain on-device as process conditions drift
- Multi-dimensional heterogeneous sensor data requires ML methods beyond simple threshold/SPC

**Connection to Fourier KB:** The practical pipeline is FFT → frequency-domain features → anomaly classifier. This is where Fourier analysis meets ML in industrial settings.

---

## 6. Confusion-Aware Rubric Optimization (CARO) for LLM-Based Scoring

**Paper:** arXiv:2603.00451 — *"Confusion-Aware Rubric Optimization for LLM-based Automated Grading"* (Feb 2026)

**This is directly relevant to Dale's scoring/rubric work.**

**Problem being solved:** When LLMs grade against rubrics, they misinterpret guidelines or lack domain specificity. Naive prompt optimization causes "rule dilution" — conflicting constraints weaken grading logic.

**CARO approach:**
1. Decompose error signals using the **confusion matrix** (true positive, false positive, false negative, true negative) — don't aggregate all errors together
2. Identify dominant misclassification patterns
3. Generate targeted "fixing patches" for each error mode individually
4. Use **diversity-aware selection** to prevent conflicting guidance

**Key insight:** Rubric items that trigger similar misclassifications should be repaired together; items with different failure modes should be repaired separately.

**Mathematical structure:**
- Confusion matrix decomposition → per-mode error rates
- Diversity metric (coverage/overlap) for patch selection
- Iterative refinement with validation set tracking

**Applicability:** This framework maps directly onto the AI-in-the-loop quality scoring systems Dale is building. The confusion matrix approach to rubric diagnosis is immediately implementable.

---

## 7. Quantitative Scoring Rubric Design Principles (Snorkel AI, 2025)

**Source:** Snorkel.ai blog (Jul 2025)

**Key principles:**
- A rubric is a mechanism for **embedding domain expertise in a checklist**
- Final rubric score = set of criteria, each mapped to numeric values
- Data quality and rubric quality are co-dependent: bad rubrics corrupt model training
- For LLM evaluation: rubric granularity matters enormously — too fine-grained → inconsistency, too coarse → low resolution

**Practical guidance for scoring models:**
- Each criterion needs: (a) a clear definition, (b) a numeric range, (c) explicit edge cases
- Build in inter-rater reliability checks before using rubric scores as ground truth

---

## Summary Table

| Domain | Key Development | Priority |
|--------|----------------|----------|
| SPC | AI/ML for CCPR → Smart Process Control (SMPC) | High |
| Simulation | MC + NSGA-II hybrid for multi-objective SC optimization | Medium |
| Forecasting | Foundation models (Chronos, TimesFM) + ensemble methods for demand | High |
| Signal Processing | Lightweight FFT + edge ML for IoT anomaly detection | Medium |
| Scoring/Rubrics | CARO: confusion matrix decomposition for rubric optimization | **Very High** |
| Scoring/Rubrics | Domain expertise embedding in quantitative rubrics (Snorkel) | High |

---

*Next update: tomorrow AM cron. Track CARO paper for implementation notes — directly applicable to Dale's scoring framework work.*
