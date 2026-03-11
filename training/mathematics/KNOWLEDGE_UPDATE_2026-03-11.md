# Knowledge Update — 2026-03-11 (Morning)

*Pythagoras morning knowledge refresh.*
*Topics: SPC / Hybrid AI-SPC, Monte Carlo (PEMC), Vector Databases (GPU-ANN, Semantic Compression), Predictive Analytics (Supply Chain), Fourier / Spectral Methods.*

---

## 1. SPC + AI Hybrid: The 2026 Convergence Model

**Sources:** Quality Magazine (Dec 2025); ResearchGate — SPC for Real-Time Industrial Data Streams (Aug 2025); f7i.ai — SPC Asset Health Framework (Feb 2026)

**What's happening:**
The dominant emerging pattern in applied SPC is a two-layer architecture:
- **Layer 1 — SPC:** Provides real-time transparency, control limits, and day-to-day operational monitoring (Shewhart, EWMA, CUSUM)
- **Layer 2 — ML:** Analyzes historical + real-time data to predict *future* deviations before they breach control limits; recommends proactive interventions

**Key technical findings:**
- Combining EWMA with ML improves detection sensitivity in high-frequency data streams (Tsung & Shi, validated 1999, now being applied at IoT scale)
- Adaptive SPC methods (Zou & Tsung) adjust control limits dynamically based on streaming data characteristics — this is the hybrid core idea
- SPC is now positioned as the "mathematical engine behind predictive maintenance" — asset health scoring driven by control chart logic

**2026 industry context:**
- IoT sensors provide continuous streams to SPC engines without manual sampling — eliminates the traditional subgroup formation problem
- SPC is active in manufacturing, logistics, healthcare, food production, and service operations

**Clinical application note (new):**
A 2026 ScienceDirect paper extends SPC to clinical psychology for patient state monitoring:
- Shewhart: best for detecting abrupt state changes
- EWMA: better for gradual drift detection in patient trajectories
- Key challenge: phase I baseline estimation is hard with n-of-1 clinical data

**Relevance to Dale's work:** The hybrid SPC+ML architecture maps cleanly onto supply chain quality scoring rubrics. SPC handles process stability monitoring; ML handles predictive flagging. The two layers can be explicitly separated in rubric design.

**Knowledge tier:** DC (method framework) + mid-frequency (current deployment patterns)

---

## 2. Monte Carlo: Prediction-Enhanced Monte Carlo (PEMC)

**Source:** arXiv:2412.11257 (Prediction-Enhanced Monte Carlo: A Machine Learning View on Control Variate) — Published May/June 2025

**What it is:**
PEMC is a framework that uses ML models as *learned control variates* within Monte Carlo simulations. Core idea:

> Standard control variates require knowing the closed-form mean of a correlated quantity. PEMC removes this requirement by training an ML model on cheap, parallelizable simulations as features, then using it to output unbiased estimates with reduced variance.

**Formal framing:**
- PEMC is a generalization of the control variate method
- The ML model predicts E[Y|X_cheap] where X_cheap are inexpensive simulation runs
- The residual Y - ŷ has lower variance than Y alone
- Unbiasedness is preserved (the correction term is still MC-based)

**Applications demonstrated:**
1. Equity derivatives (variance swaps) under stochastic local volatility
2. Interest rate derivatives (swaptions) under HJM model
3. Ambulance dispatch / hospital load balancing (mortality rate estimation)

**Why it matters:**
- Eliminates the need for closed-form control variate means
- Consistent variance reduction across all three test cases
- Particularly valuable for nested / multi-level / path-dependent evaluations
- Subjects: stat.ML, cs.CE, cs.LG, q-fin.PR

**Companion work — Active Learning Variance Reduction (arXiv:2511.00563, Nov 2025):**
- Data-driven importance sampling using active learning
- Applied to nanodosimetry (highly non-uniform probability distributions)
- The importance sampling distribution is learned iteratively, not pre-specified
- Generalizes: anywhere the probability mass is highly concentrated, active learning can find it more efficiently than uniform sampling

**Relevance to Dale's work:** For supply chain risk Monte Carlo (demand uncertainty, lead time variability, disruption scenarios), PEMC's approach of using cheap simulations as features for a learned predictor could substantially cut runtime on high-fidelity models.

**Knowledge tier:** Mid-frequency (active research area, arxiv-stage)

---

## 3. Vector Databases: GPU-Native ANN and Semantic Compression

**Sources:** arXiv:2602.23999 (GPU-Native ANN with IVF-RaBitQ, Feb 2026); arXiv:2507.19715 (Semantic Compression + Graph-Augmented Retrieval, Jul 2025); arXiv:2310.11703v2 (Comprehensive VDB Survey, Jun 2025)

### 3a. GPU-Native IVF-RaBitQ (arXiv:2602.23999, Feb 2026)

**What it is:** A GPU-native approximate nearest neighbor search algorithm combining:
- IVF (Inverted File Index) for coarse-level partitioning
- RaBitQ: a binary quantization scheme with theoretical recall guarantees

**Why it matters:**
- Previous GPU-accelerated ANN methods sacrificed recall for speed; RaBitQ provides theoretical bounds on recall degradation
- Enables fast *index build* AND fast *search* natively on GPU — previous approaches optimized one or the other
- Directly relevant to enterprise RAG (Retrieval-Augmented Generation) where real-time query latency is critical

### 3b. Beyond Nearest Neighbors: Semantic Compression + Graph-Augmented Retrieval (arXiv:2507.19715)

**Problem:** Standard ANN top-k retrieval returns *semantically redundant* results — multiple vectors near the same concept. This degrades RAG quality.

**Solution proposed:**
1. **Semantic compression:** Cluster retrieved candidates; return one representative per cluster (diversity-aware retrieval)
2. **Graph-augmented retrieval:** Build a knowledge graph over the vector index; traverse graph edges to find semantically *related but non-redundant* results

**Why it matters:** Improves answer quality in RAG pipelines without changing the embedding model. The graph structure captures relationships that pure distance metrics miss.

### 3c. Filtering ANN: Attribute + Vector Hybrid Search (arXiv:2508.16263)

**What it is:** Combining attribute filtering (e.g., date range, category, supplier) with ANN search in a single operation.

**Key challenge:** Naively applying a post-filter on ANN results degrades recall when filters are selective. Solutions:
- Pre-filtering: apply filter to narrow the candidate set before ANN (fast but may over-exclude)
- In-graph filtering: encode attributes as graph node properties; filter during traversal (better recall, more complex index)
- Hybrid algorithms: select strategy adaptively based on filter selectivity

**2025–2026 trend summary (vector databases):**
- Hybrid search (vector + metadata filtering) is THE dominant enterprise pattern
- HNSW remains the go-to graph-based index; IVF-family for high-throughput GPU workloads
- Quantization (RaBitQ, PQ, SQ) allows billion-scale indexes to fit in GPU memory

**Knowledge tier:** High-frequency (active product development)

---

## 4. Predictive Analytics: Supply Chain Forecasting 2025–2026

**Sources:** IPEC Group / ASCM 2026 Benchmarking; datup.ai; PYMNTS (Nov 2025); GlobeNewswire market report (Jan 2026)

**Quantitative benchmarks now available (2025–2026 deployments):**
| Metric | Reported improvement range |
|---|---|
| Forecast accuracy | 30–40% (advanced ML vs. baseline) |
| Inventory cost reduction | 15–45% |
| Order fulfillment rate | +15–25% |
| ROI timeline | 6–12 months |

*Source tier: High-frequency / vendor-reported. Use directionally, not as precise targets.*

**Key 2025 development — Google DeepMind WeatherNext 2:**
- 100s of possible weather outcome scenarios from a single starting point
- Forecasts generated 8× faster than prior models
- Resolution: up to 1-hour time steps
- Single TPU, under 1 minute per forecast
- **Supply chain implication:** High-fidelity weather data, previously reserved for energy/science markets, is now accessible for supply chain resilience planning (disruption probability modeling, seasonal demand forecasting)

**Methodological trend:**
- Ensemble methods + ML (gradient boosting, LSTM, transformer-based) are displacing pure ARIMA/ETS in high-volume SKU environments
- Hybrid models (statistical base + ML correction layer) tend to outperform pure-ML when data is scarce for individual SKUs
- Probabilistic forecasting (prediction intervals, not just point estimates) is increasingly standard in enterprise tools

**Relevance to Dale's work:** The WeatherNext 2 development is directly actionable — external high-fidelity forecast signals can be incorporated into supply chain Monte Carlo simulations as exogenous shock distributions. The hybrid statistical+ML architecture mirrors the SPC+ML pattern above.

**Knowledge tier:** High-frequency (volatile — market data and product releases)

---

## 5. Fourier / Spectral Methods: ML Integration

**Sources:** Nature Scientific Reports (Nov 2025) — Fourier vs. Deep Learning for Equipment Failure Prediction; Springer Journal of Scientific Computing (Apr 2025) — Continuous Spectral Transform; Optica (Mar 2026) — Fourier Feature Networks

### 5a. Fourier vs. Deep Learning for Equipment Failure Prediction (Nature, Nov 2025)

**Study:** Direct comparison of Fourier series spectral analysis vs. deep learning on industrial sensor signals for predictive maintenance.

**Finding:** For periodic signals with known fundamental frequencies, Fourier series models remain competitive with deep learning and offer:
- Higher interpretability (dominant frequencies = physical failure modes)
- Lower data requirements (no training set needed for known periodicity)
- Reliable performance on signals with stable periodicity

Deep learning wins when: signals are aperiodic, multi-modal, or when the failure mode introduces frequency shifting (not just amplitude change).

**Practical rule:** Use Fourier/spectral methods as the baseline for any industrial sensor signal analysis. Switch to deep learning when spectral structure is insufficient.

### 5b. Continuous Spectral Transform on Arbitrary Data (Springer, Apr 2025)

**What it is:** Generalization of Fourier transforms to signals defined on arbitrary graph structures (not just regular grids/time series).

**Method:** Decomposes signals via eigenvectors of a graph Laplacian — extends Fourier convolution to graph-structured data (supply chain networks, logistics graphs).

**Why it matters:** Enables frequency-domain analysis of signals on network graphs. Example: detecting anomalous oscillation patterns in a supply chain network (e.g., bullwhip effect at specific network frequencies).

### 5c. Fourier Feature Networks for High-Frequency Learning (Optica, Mar 2026)

**Problem:** Standard neural networks exhibit *spectral bias* — they learn low-frequency components first and underfit high-frequency structure.

**Solution:** Fourier feature embedding as input transformation: map inputs through sin/cos functions before the network. This removes spectral bias and enables the network to resolve fine-grained periodic patterns.

**Application:** Learning transmission matrices in multimode fiber (optics), but the method is domain-general.

**Supply chain relevance:** Any ML model predicting signals with high-frequency seasonality (daily/weekly demand oscillations) should consider Fourier feature embeddings as a preprocessing step.

**Knowledge tier:** Mid-frequency (active research, increasingly applied)

---

## Summary of Key Actionable Findings

| Area | Key finding | Action priority |
|---|---|---|
| SPC | SPC+ML two-layer hybrid is now the industry standard pattern | High — directly applicable to rubric/scoring work |
| Monte Carlo | PEMC: ML-learned control variates reduce variance while preserving unbiasedness | Medium — evaluate for demand simulation models |
| Vector DB | Semantic compression + graph-augmented retrieval improves RAG quality | Medium — consider for knowledge base retrieval |
| Predictive Analytics | WeatherNext 2 enables high-fidelity weather shocks in SC models | Low-medium — future capability |
| Fourier | Fourier feature embeddings fix spectral bias in ML forecasting | Medium — apply to demand forecasting with seasonality |

---

*Update compiled: 2026-03-11 11:00 AM ET*
*Next scheduled update: 2026-03-12 AM*
