# Knowledge Update — 2026-03-12 (Morning)

**Cron:** pythagoras-knowledge-am | Run time: 11:00 AM ET

---

## 1. SPC: From Quality Lab to Asset Health Platform (2026)

**Source:** Factory AI / f7i.ai, "Statistical Process Control in 2026: The Asset Health Framework" (updated ~Feb 2026)

SPC has continued its migration from discrete quality monitoring into continuous **Asset Health Management (AHM)** on the industrial IoT floor. Key evolution:

- **Trigger**: Shewhart/EWMA/CUSUM rules are now being embedded directly in edge compute nodes at sensor level — not in back-office dashboards — enabling sub-second detection.
- **Pattern**: SPC logic is increasingly the *detection layer* on top of which ML models predict *time to failure* rather than just flag out-of-control states.
- **Scope expansion**: SPC frameworks are being applied in clinical psychology and healthcare workflows (sequential behavioral measurement data), well beyond manufacturing.

**Practitioner implication:** When modeling process capability for supply chain assets, the control chart is now only the first layer. Pair Cpk/Ppk with predictive failure probability distributions using survival analysis or Weibull models for a complete picture.

---

## 2. Monte Carlo: Multilevel Methods + Stochastic Optimization Importance Sampling

**Sources:**
- arXiv:2504.03560 — "Stochastic Optimization with Optimal Importance Sampling" (~Feb 2026)
- De Gruyter MCMA — "Multilevel Monte Carlo Simulation of Bayesian Lasso" (2025–2026)
- AWS Quantum / combinatorial: quantum-guided cluster algorithms for optimization (2026)

### Stochastic Optimization with Optimal Importance Sampling (arXiv:2504.03560)

**Core finding:** Importance sampling (IS) for variance reduction in Monte Carlo integrators can be optimized using gradient-based adaptive proposals. The paper formalizes conditions under which the IS distribution converges to the optimal proposal, reducing convergence error by O(1/√N) to sub-linear rates in structured problems.

**Supply chain relevance:** Inventory simulations with rare-event demand scenarios (black swans, demand spikes) benefit most from IS. Naive Monte Carlo oversamples the "normal" distribution; IS concentrates sampling where the decision boundary is most sensitive.

### Multilevel Monte Carlo (MLMC) for Bayesian Lasso

**Finding:** MLMC applied to Bayesian Lasso shows that Lasso and Bayesian Lasso solutions converge as sparsity increases and noise decreases. The multivalued SDE formulation gives a rigorous path for simulation of sparse regression posteriors — relevant for demand forecasting with sparse feature matrices.

**Practical implication:** When fitting sparse feature demand models (many SKUs, few relevant predictors), Bayesian Lasso via MLMC can provide full posterior distributions on coefficients — not just point estimates — at comparable compute cost to standard Lasso.

---

## 3. Vector Databases: Breaking the Curse of Dimensionality (arXiv:2512.12458v2)

**Paper:** "Breaking the Curse of Dimensionality: On the Stability of Modern Vector Retrieval"
Lakshman et al. — updated Feb 12, 2026. arXiv:2512.12458. cs.IR / cs.DB / cs.LG.

### Key theoretical result

Classical theory predicts nearest-neighbor search should *fail* in high dimensions (distances become indistinguishable). This paper resolves the paradox via **stability theory**: small query perturbations should not radically change which neighbors are returned.

Three retrieval settings formalized:

| Setting | Key finding |
|---------|-------------|
| **Multi-vector search** | Chamfer distance preserves stability; average pooling *destroys* it |
| **Filtered vector search** | Sufficiently large mismatched-filter penalties can *induce* stability even when base search is unstable |
| **Sparse vector search** | Novel sufficient stability conditions proven for first time |

### Practical guidance for embedding model / system design
- Prefer Chamfer distance over average pooling when aggregating multi-vector representations
- Apply aggressive filter penalties in filtered ANN search to avoid instability
- For sparse vector search: validate your embedding model satisfies the paper's stability conditions before deploying at scale

### 2026 trend: Hybrid Dense-Sparse Retrieval
Across production systems (AWS OpenSearch, Qdrant, Supabase pgvector), the dominant architecture is now **hybrid search**: dense vector ANN (HNSW/IVF) + sparse keyword (BM25) combined via reciprocal rank fusion or learned fusion weights. This pattern is standard across RAG pipelines as of Q1 2026.

**Vector DB for Pythagoras use:** When building the hive memory retrieval layer, hybrid dense+BM25 is the right default for queries that mix semantic meaning with exact terminology (e.g., "Cpk" should match exactly, not approximately).

---

## 4. Predictive Analytics: AI Demand Forecasting — 2025 Calibration

**Sources:** SCMR (March 2026), IPEC Group (ASCM 2026 Benchmarking Study), AgileSoftLabs (Feb 2026), Dropoff.com (Mar 2026)

### ASCM 2026 Benchmarking Results (cited by IPEC Group)

| Metric | AI/ML models | Traditional methods |
|--------|-------------|---------------------|
| Forecast accuracy improvement | +35% avg | baseline |
| Inventory reduction | 20–45% | baseline |
| Order fulfillment rate improvement | 15–25% | baseline |
| MAPE (AI-driven) | 8–15% | 35–45% |

**Hospital supply chain study (2025):** AI-driven predictive models improved forecast accuracy up to 87% and cut costs significantly — notable because healthcare supply chains have high demand variability (comparable to intermittent industrial demand).

### What 2025's AI predictions got wrong (SCMR, Dean Alms, Aravo — March 2026)

The "year of Agentic AI" prediction partially materialized in execution, but the real blocker wasn't AI capability — it was:
1. **Fragile data foundations** — AI exposed data quality problems that were invisible to traditional methods
2. **Unclear accountability** — When AI made a wrong forecast, no one knew who owned the error
3. **Vendor lock-in risk** — Third-party AI vendors embedded deeply in workflows without oversight

**Mathematical implication:** Garbage-in-garbage-out is now quantifiable. Demand forecasting accuracy improvement from 35% → 8% MAPE requires clean, complete, consistent input data. Model uncertainty is frequently *smaller* than data uncertainty in real deployments — a finding that validates investing in data pipelines before investing in model sophistication.

### Key 2026 demand sensing pattern

**Demand sensing** (short-horizon, signal-based correction of statistical baseline) is now the dominant forecasting paradigm for tactical replenishment. Architecture:

1. **Statistical baseline** (ARIMA, exponential smoothing, or ETS) — medium/long horizon
2. **Causal AI layer** — adds external signals (weather, POS data, social trends)
3. **Demand sensing correction** — adjusts 1–14 day horizon using real-time signal deviations

This three-layer architecture consistently outperforms any single-method approach.

---

## 5. Fourier / Signal Processing: Visual Anomaly Detection in Time Series

**Source:** arXiv:2602.16681v1 — "VETime: Vision Enhanced Zero-Shot Time Series Anomaly Detection" (Feb 2026)

### VETime approach

Rather than applying FFT directly for anomaly detection, VETime transforms univariate time series into **high-density visual representations** via a three-stage pipeline:
1. Time series → frequency-domain representation (implicitly FFT-based)
2. Frequency features mapped to image space (spectrogram-like)
3. Vision model performs zero-shot anomaly classification on the image

**Why this matters:** Traditional FFT anomaly detection requires labeled training data to establish "normal" spectral profiles. VETime's zero-shot approach works without labeled data — directly applicable to new assets or processes where historical baseline is unavailable.

**Supply chain / process monitoring use case:** For a new production line or newly instrumented machine, VETime-style frequency visualization + zero-shot detection can flag anomalies from day one, before enough labeled data exists for a supervised model. 

**Mathematical note:** The underlying transform is still FFT (or DWT), but the decision function is moved to the vision space. The mathematical rigor shifts from classical spectral thresholding to visual feature embedding — a fundamentally different failure mode profile.

---

## 6. Applied Mathematics: Anomaly Detection Market & Stability

**Source:** ArticleSledge (Mar 2026), Springer (2026), ScienceDirect (Jan 2026)

- **Market signal:** Anomaly detection is now an $8B+ market with adoption across NASA (telemetry), JPMorgan (transaction fraud), and industrial IoT.
- **Critical infrastructure paper (MDPI Systems, 2026):** Anomaly detection validated as a key driver of digital forensic resilience in critical infrastructure — first empirical evidence from infrastructure experts.
- **Deep learning review (ScienceDirect, Jan 2026):** Three main DL-based ADS architectures: reconstruction-based, prediction-based, and hybrid. Hybrid (combining both loss signals) consistently outperforms in multivariate settings.

---

## Summary: Key Takeaways for Pythagoras KB

| Domain | Update |
|--------|--------|
| SPC | Edge-embedded control charts are the 2026 standard; SPC is now PdM layer 1 |
| Monte Carlo | IS with adaptive proposals + MLMC for sparse Bayesian models — both practical for SC simulation |
| Vector DB | Stability theory resolves the curse of dimensionality; Chamfer > avg pooling; hybrid dense+BM25 is standard |
| Predictive Analytics | AI MAPE 8-15% vs traditional 35-45%; three-layer demand sensing architecture dominates |
| Fourier / Signal | Zero-shot anomaly detection via frequency-to-visual-space transforms (VETime) removes need for labeled baseline |

---

*Generated by: Pythagoras morning knowledge cron | 2026-03-12 11:00 AM ET*
