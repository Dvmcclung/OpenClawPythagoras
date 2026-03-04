# PAPERS_KB.md — Academic Papers Knowledge Base

Compiled by subagent on 2026-03-03. Papers ingested from:
`/home/dale/.openclaw/pythagoras-workspace/training/mathematics/papers/`

---

## Statistical Process Control Papers

### 1. Nonparametric SPC via Sequential Normal Scores (2019)
**File:** `1901.04443v1.pdf`
**Authors:** W.J. Conover (Texas Tech), V.G. Tercero-Gómez (Tec de Monterrey), A.E. Cordero-Franco (UANL)
**Source:** arXiv:1901.04443 [stat.ME]

**Core Contribution:**
Introduces 16 new nonparametric statistical tests for SPC based on Sequential Normal Scores (SNS). These tests work for univariate and multivariate data, detecting changes in location, scale, or both without requiring distributional assumptions.

**Key Methods:**
- Sequential Normal Scores (SNS): Transform observed data ranks into approximate normal scores sequentially, enabling distribution-free monitoring.
- Conditional SNS (CSNS): Variant conditioning on past observations for improved sensitivity.
- CUSUM on SNS: Apply cumulative sum charts to SNS-transformed values to detect sustained shifts.
- EWMA on SNS: Exponentially weighted moving average applied to SNS for smooth detection.
- Formula: Z_i = Phi_inv(R_i / (n+1)), where R_i is the rank of the i-th observation among all observations so far.

**Practical Applications:**
- Quality monitoring for manufacturing processes without assuming normality.
- Monitoring service process KPIs where distributions are unknown.
- Detecting both mean shifts and variance changes in real-time.

**Notable Findings:**
- SNS-based tests have comparable or better power than existing nonparametric methods.
- Phase I (reference dataset) and Phase II (online monitoring) frameworks both supported.
- 17 worked examples and 33 tables provided — highly operational.

---

### 2. Kernel-Based Multivariate SPC Optimization (2025)
**File:** `2505.01556v1.pdf`
**Authors:** Zina-Sabrina Duma, Victoria Jorry, Tuomas Sihvonen, Satu-Pia Reinikainen, Lassi Roininen (LUT University, Finland)
**Source:** arXiv:2505.01556

**Core Contribution:**
Optimizes Kernel MSPC parameters using Kernel Flows (KF), a Gaussian Process Regression kernel learning approach — replacing expensive cross-validation/grid search.

**Key Methods:**
- Kernel PCA (KPCA): Projects data into kernel-induced feature space; captures nonlinear variable relationships.
- Kernel PCR (KPCR): Used as a proxy to optimize kernel parameters.
- Kernel Flows: Minimizes ratio of kernel-based loss between full and sub-sampled data to learn optimal hyperparameters.
- Kernel types explored: RBF, Matern, polynomial, and combinations.
- Hotelling's T2 and Q (SPE) control charts computed in kernel space.

**Practical Applications:**
- Fault detection in chemical processes (Tennessee Eastman Process benchmark).
- High-dimensional industrial monitoring where linear PCA fails.

**Notable Findings:**
- All Tennessee Eastman faults detected, including those missed in original benchmark study.
- Individual per-variable kernel parameters outperform shared kernel parameters.
- Kernel combination learning yields most flexible models.

---

### 3. High-Dimensional SPC via Manifold Fitting and Learning (2025)
**File:** `2509.19820v1.pdf`
**Authors:** Ismail Burak Tas, Enrique del Castillo (Penn State)
**Source:** arXiv:2509.19820 [stat.ML]

**Core Contribution:**
Two complementary Phase II SPC monitoring frameworks for high-dimensional dynamic industrial data, exploiting the assumption that data lies on a lower-dimensional nonlinear manifold.

**Key Methods:**
- Manifold Fitting: Fit smooth manifold to in-control data; monitor signed distances via distribution-free control chart.
- Manifold Learning: Embed data into lower-dimensional space (UMAP, diffusion maps), then apply standard MSPC.
- Distribution-free chart: Derived from empirical quantiles of in-control distance distribution.
- Type I error probability provably controllable for both methods.

**Practical Applications:**
- High-dimensional sensor streams in manufacturing (Tennessee Eastman).
- Image-based quality inspection (electrical commutator surface anomalies).
- Small-n, large-p industrial monitoring.

**Notable Findings:**
- Manifold fitting achieves competitive or superior fault detection vs. manifold learning with lower complexity.
- Handles serially correlated (dynamic) data.
- Successfully detected real surface anomalies in commutator image dataset.

---

### 4. Distribution-Free SPC with Conformal Prediction (2024)
**File:** `2512.23602v1.pdf`
**Author:** Christopher Burger (University of Mississippi)
**Source:** arXiv:2512.23602

**Core Contribution:**
Hybrid framework integrating Conformal Prediction into SPC for distribution-free, model-agnostic quality control.

**Key Methods:**
- Conformal Prediction: Produces valid p-values and prediction intervals using a nonconformity measure (e.g., model residual).
- Conformal-Enhanced Control Charts: Replace 3-sigma limits with conformal prediction intervals; add "uncertainty spike" signals.
- Conformal-Enhanced Process Monitoring: Reframes multivariate monitoring as anomaly detection via p-value chart.
- Applicable with any underlying model — model-agnostic.

**Practical Applications:**
- Modern complex manufacturing with non-normal, high-dimensional data.
- Safety-critical processes requiring distributional guarantees.
- ML prediction pipelines combined with quality monitoring.

**Notable Findings:**
- Valid coverage under exchangeability without parametric assumptions.
- "Uncertainty spike" signals are proactive — fire ahead of hard failures.
- Maintains interpretability of classic Shewhart-style charts.

---

### 5. SPC via P-Value Charting (2026)
**File:** `2601.17319v1.pdf`
**Authors:** Hien Duy Nguyen (Kyushu University / La Trobe), Dan Wang (La Trobe / Northwest University)
**Source:** arXiv:2601.17319 [stat.ME]

**Core Contribution:**
Rigorous theoretical framework for SPC via charting sequences of p-values. Establishes universal ARL bounds under super-uniformity and proposes EWMA-like p-value merging for multivariate monitoring.

**Key Methods:**
- Super-uniform p-values: When in-control, p-values are stochastically >= Uniform(0,1) — no parametric assumption required.
- Shewhart p-value chart: Signal when P_t <= alpha; ARL >= alpha^-1 proven universally.
- k-ARL: Expected time to k-th false alarm >= k * alpha^-1 under conditional super-uniformity.
- EWMA-style p-value merging: Combines sequential p-values using merging functions (Fisher's method adapted for dependence).
- Closed Testing for multivariate localization: Controls FWER at alarm time for fault localization.

**Practical Applications:**
- Distribution-free SPC in nonparametric settings.
- Two-phase designs with Phase I calibration.
- Multivariate fault diagnosis — identifying which variable(s) triggered alarm.

**Notable Findings:**
- ARL bounds are universal (no temporal dependence assumption).
- EWMA p-value charts avoid ad hoc control limits entirely.
- Closed testing localizes faults with statistical validity.

---

## Vector Databases Papers

### 6. Vector DBMS: Fundamental Concepts, Use-Cases, Challenges (2023)
**File:** `2309.11322v2.pdf`
**Author:** Toni Taipalus
**Source:** Narrative literature review

**Core Contribution:**
Accessible introduction to vector DBMS concepts, use-cases, and challenges for practitioners and researchers entering the field.

**Key Concepts:**
- Vectorization: Converting unstructured data into fixed-dimensional numerical vectors via neural embeddings.
- Similarity Search: k-NN and approximate k-NN (ANN) as primary query paradigm.
- Distance Metrics: Euclidean, cosine similarity, dot product — choice affects recall and ranking.
- Indexing: Flat (brute force), HNSW, IVF, LSH.
- Challenges: Curse of dimensionality, recall-speed tradeoff, hybrid queries (ANN + scalar filter).

**Practical Applications:**
- Recommender systems, semantic search, chatbot memory (RAG), image retrieval.
- Supply chain: embedding SKU descriptions, carrier attributes, lane characteristics for similarity-based retrieval.

**Notable Findings:**
- No single indexing method dominates all use-cases; HNSW preferred for high recall + speed.
- Hybrid queries (ANN + scalar filters) remain an open engineering challenge.

---

### 7. Comprehensive Survey on Vector Database Storage and Retrieval (2023/2025)
**File:** `2310.11703v2.pdf`
**Authors:** Le Ma, Ran Zhang, Yikun Han, et al. (multi-institution)
**Source:** arXiv:2310.11703 [cs.DB]

**Core Contribution:**
Comprehensive technical review of VDB algorithms, architectures, and LLM integration covering storage design, indexing evolution, and comparison of major systems.

**Key Methods:**
- Graph-based ANNS: HNSW — hierarchical navigable small worlds; O(log n) query.
- Cluster-based: IVF — Voronoi cells via k-means; only top-k clusters searched.
- Tree-based: KD-trees, Ball-trees — effective in low dimensions.
- Hash-based: LSH — maps similar vectors to same buckets probabilistically.
- Product Quantization (PQ): Compresses vectors by splitting into sub-vectors and quantizing each; 8-32x memory reduction.
- Filtering strategies: Pre-filter, post-filter, in-graph filtering.

**Practical Applications:**
- RAG pipelines for LLM-backed applications.
- Large-scale similarity search over billions of vectors.
- Combining metadata filters with semantic similarity.

**Notable Findings:**
- HNSW achieves >95% recall at competitive query latency.
- LLM + VDB is the dominant emerging enterprise AI architecture.
- Incremental indexing at billion-scale is an open problem.

---

### 8. When LLMs Meet Vector Databases (2024/2025)
**File:** `2402.01763v4.pdf`
**Authors:** Zhi Jing, Yongye Su, Yikun Han, et al. (CMU, Purdue, U. Michigan, HIT, CAS)
**Source:** arXiv:2402.01763 [cs.DB]

**Core Contribution:**
Survey of LLM + VecDB integration — how VecDBs solve LLM limitations (hallucination, stale knowledge, cost) and how LLMs enhance VecDB usability.

**Key Methods:**
- RAG: Query VecDB to retrieve relevant context; inject into LLM prompt to ground generation.
- VecDB augments LLMs: External long-term memory, up-to-date knowledge, reduced hallucination.
- LLMs augment VecDBs: Natural language query parsing, semantic embedding generation.
- Embedding Models: text-embedding-ada-002, sentence-transformers, CLIP (multimodal).
- Chunking strategies: Fixed-size, semantic, recursive — affects retrieval granularity.
- Hybrid search: Dense (embeddings) + sparse (BM25) retrieval.

**Practical Applications:**
- Enterprise QA systems with private knowledge bases.
- Agent memory systems requiring persistent semantic retrieval.
- Supply chain: RAG over SOPs, contracts, lane data.

**Notable Findings:**
- Embedding model quality matters more than VecDB engine choice.
- Hybrid search outperforms pure dense retrieval for most enterprise use cases.
- VecDB is now considered standard infrastructure for production LLM deployments.

---

### 9. MicroNN: On-Device Updatable Vector Database (2025)
**File:** `2504.05573v1.pdf`
**Authors:** Jeffrey Pound, Floris Chabert, Arjun Bhushan, et al. (Apple)
**Source:** arXiv:2504.05573

**Core Contribution:**
MicroNN — embedded, disk-resident, updatable vector search library designed for on-device deployment with constrained memory. Supports continuous updates and hybrid queries.

**Key Methods:**
- Disk-resident HNSW: Graph stored on disk with LRU memory cache for hot nodes.
- Updatable index: Supports continuous inserts/deletes without full rebuilds.
- Hybrid search: Combines ANN with structured attribute filters in a single query.
- Resource budget: ~10 MB memory; <7 ms top-100 retrieval at 90% recall on million-scale.

**Practical Applications:**
- On-device semantic search (iOS, macOS, embedded systems).
- Edge deployments where cloud latency is unacceptable.
- Updatable product catalogs, local agent memory.

**Notable Findings:**
- On-device million-scale vector search is practical with right disk I/O optimization.
- Hybrid queries add minimal overhead with moderate filter selectivity.
- In production at Apple scale.

---

### 10. HARMONY: Scalable Distributed Vector Database (2025)
**File:** `2506.14707v1.pdf`
**Authors:** Qian Xu, Feng Zhang, Chengxi Li, et al. (Renmin University, MIT, Tsinghua)
**Source:** arXiv:2506.14707 [cs.DB]

**Core Contribution:**
HARMONY — distributed ANNS system addressing load imbalance and communication overhead via multi-granularity partition strategy.

**Key Methods:**
- Multi-granularity partitioning: Combines dimension-based partition (split vector dimensions) and vector-based partition (assign vectors by cluster).
- Early-stop pruning: Leverages monotonicity of partial distance computations to prune unpromising candidates early.
- Distributed HNSW: Local HNSW per node; routing layer coordinates cross-node queries.

**Practical Applications:**
- Billion-scale ANN search (Alibaba 500PB scale).
- Enterprise search and recommendation requiring horizontal scalability.
- Federated or multi-datacenter vector retrieval.

**Notable Findings:**
- 4.63x average throughput improvement over leading distributed VDBs (4-node cluster).
- 58% performance improvement on skewed workloads vs. traditional partitioning.
- Early-stop pruning reduces communication ~40%.

---

## Vector Calculus & Differential Equations

### 11. Vector Calculus and Differential Forms with Applications to Electromagnetism (2015)
**File:** `VectorCalculus.pdf`
**Author:** Sean Roberson (Texas A&M University - San Antonio)

**Core Contribution:**
Undergraduate exposition unifying multivariable calculus, linear algebra, and differential forms — culminating in Maxwell's equations in 2-line form.

**Key Methods/Formulas:**
- Differential k-forms: Generalize scalars (0-forms), 1-forms, area elements (2-forms), volume elements (3-forms).
- Exterior derivative d: Unifies gradient, curl, divergence: d(f) = grad f, d(omega_1) = curl, d(omega_2) = div.
- Generalized Stokes' Theorem: integral_M d(omega) = integral_{dM} omega — subsumes Green's, Stokes', and Gauss's theorems.
- Wedge product: Antisymmetric tensor product; captures orientation.
- Maxwell's equations in forms: dF = 0 and d*F = J (two lines vs. four vector equations).

**Practical Applications:**
- Foundation for coordinate-free formulations used in simulation and geometric deep learning.
- Framework for flux, circulation, and field integrals in engineering.

**Notable Findings:**
- Generalized Stokes' theorem is the master theorem — all classical integral theorems are special cases.
- Differential forms make dimensional analysis and orientation explicit.

---

### 12. Recovering Seldom-Used Theorems of Vector Calculus (2023)
**File:** `2312.17268v1.pdf`
**Author:** Antonio Perez-Garrido (Universidad Politecnica de Cartagena)
**Source:** arXiv:2312.17268 [physics.class-ph]

**Core Contribution:**
Proves several rarely-seen integral vector calculus identities using differential forms, including two apparently unpublished identities, with applications to computing forces and torques.

**Key Formulas:**
- Eq. 3: contour(A x dr) = surface integral [(div A)ds - grad(A dot ds)]
- Eq. 4: contour(f dr) = -surface integral [grad f x ds]
- Eq. 5: contour[(C dot dr)A] = surface integral [ds dot (curl C - C x grad)A]
- Gauss: surface integral(A dot ds) = volume integral(div A dv)
- Stokes: contour(A dot dr) = surface integral[(curl A) dot ds]

**Practical Applications:**
- Computing net electromagnetic forces and torques on arbitrary current distributions.
- Numerical integration of field quantities in simulation.

**Notable Findings:**
- Differential forms provide elegant proofs for identities cumbersome in coordinate notation.
- Two identities appear to be new contributions.

---

### 13. Differential Forms vs Geometric Algebra (2024)
**File:** `2407.17890v1.pdf`
**Authors:** Pablo Banon Perez, Maarten DeKieviet (University of Heidelberg)
**Source:** arXiv:2407.17890 [gr-qc]

**Core Contribution:**
Side-by-side comparison and translation between Differential Forms (Cartan calculus) and Geometric Algebra (Clifford algebra) — two competing coordinate-free geometric formalisms.

**Key Methods:**
- Differential Forms: Antisymmetric tensors; exterior derivative d, Hodge star, wedge product, interior product.
- Geometric Algebra (GA): Clifford algebra; geometric product ab = a.b + a^b unifies inner and outer products.
- Translation table provided for identities, integration theorems, and Maxwell's equations.
- Rotor techniques: GA encodes rotations as R = exp(B*theta/2) — intuitive vs. rotation matrices.
- Cartan's formalism for GR: Connection 1-forms and curvature 2-forms in both languages.

**Practical Applications:**
- Choosing formalisms for physics simulation, robotics (GA rotors), geometric ML.
- Reference for converting formulas between the two systems.

**Notable Findings:**
- GA more friendly for rotations and spatial reasoning; Differential Forms more natural for integration and topology.
- Both unify the classical div/grad/curl into a single operator.
- Neither is universally superior — application domain drives choice.

---

### 14. Parameter Estimation of ODEs via Nonparametric Estimators (2008)
**File:** `0710.4190v2.pdf`
**Author:** Nicolas J-B. Brunel (Universite d'Evry)
**Source:** Electronic Journal of Statistics Vol. 2 (2008) 1242-1267; arXiv:0710.4190

**Core Contribution:**
Two-step M-estimator for ODE parameter estimation avoiding repeated numerical ODE solves — replaces IVP solution with nonparametric regression estimate of state trajectory.

**Key Methods:**
- Problem: Given time series and ODE x_dot(t) = F(t, x(t), theta), estimate theta without repeatedly solving the IVP.
- Step 1: Estimate state trajectory x_hat(t) using spline regression or kernel smoothing.
- Step 2: Minimize mismatch between F(t, x_hat(t), theta) and x_hat_dot(t) over theta (M-estimation).
- Asymptotic properties: Consistency under general conditions; sqrt(n)-rate normality with spline estimators.
- Applicable to coupled nonlinear ODE systems.

**Practical Applications:**
- Fitting compartmental models (epidemiology, pharmacokinetics) to noisy time series.
- Calibrating dynamical systems models for industrial processes.
- ODE parameter inference without simulation budget.

**Notable Findings:**
- Avoids "inner loop" ODE solve that makes classical approaches expensive.
- Spline-based estimator achieves parametric sqrt(n) convergence rate.
- Applicable to any ODE structure F.

---

### 15. Ordinary Differential Equations and Dynamical Systems (Textbook)
**File:** `ode.pdf`
**Author:** Gerald Teschl (AMS publication, preliminary version)

**Core Contribution:**
Comprehensive graduate textbook covering classical ODE theory through modern dynamical systems — Picard-Lindelof to chaos theory.

**Key Topics:**
- Existence and Uniqueness: Picard-Lindelof (Lipschitz), Peano (continuous), extensibility theorems.
- Linear Systems: Matrix exponential exp(At); Jordan form; Floquet theory for periodic systems.
- Perturbation Theory: Regular and singular perturbation; asymptotic expansions.
- Stability: Lyapunov stability, asymptotic stability, Lyapunov functions; linearization theorem.
- Boundary Value Problems: Sturm-Liouville theory; eigenfunction expansions.
- Dynamical Systems: Poincare map, invariant manifolds, Hartman-Grobman theorem, chaotic dynamics.
- Phase plane analysis: Fixed points, limit cycles, Poincare-Bendixson theorem.

**Practical Applications:**
- Foundation for modeling continuous-time dynamical systems (supply chain dynamics, logistics flow models).
- Stability analysis of feedback control systems.
- Basis for numerical ODE solvers (Euler, Runge-Kutta).

**Notable Findings:**
- Covers both analytical and geometric/topological perspectives.
- Strong emphasis on qualitative analysis without explicit solutions.
- Includes Frobenius method for series solutions near singularities.

---

## Monte Carlo & Simulation

### 16. Monte Carlo Methods in Statistical Physics: Mathematical Foundations (2009)
**File:** `0906.0858v1.pdf`
**Author:** Michael Kastner (National Institute for Theoretical Physics, Stellenbosch)
**Source:** arXiv:0906.0858 [cond-mat.stat-mech]

**Core Contribution:**
Pedagogical review unifying MC mathematical foundations — presenting the algorithm zoo as realizations of a handful of core strategies identified by their free parameters.

**Key Methods:**
- Markov Chain Monte Carlo (MCMC): Ergodic Markov chain with target distribution pi as stationary distribution.
- Detailed Balance: pi(x)T(x->y) = pi(y)T(y->x) — sufficient condition for pi to be stationary.
- Metropolis-Hastings: Accept proposed move y from x with prob min(1, pi(y)q(x|y) / pi(x)q(y|x)).
- Convergence levers: Choice of proposal q, temperature scheduling, update scheme.
- Importance Sampling: Weight samples from q(x) by w(x) = pi(x)/q(x) to estimate expectations under pi.
- Simulated Annealing: MC with slowly decreasing temperature T — finds global optima.
- Cluster algorithms (Wolff, Swendsen-Wang): Update clusters of correlated variables simultaneously — reduces autocorrelation.

**Practical Applications:**
- Estimating intractable integrals and expectations (Bayesian inference).
- Optimization via simulated annealing.
- Simulation of stochastic processes in supply chain, finance, queueing theory.

**Notable Findings:**
- Most MC algorithms share the same mathematical skeleton — differ only in proposal and update scheme.
- Mixing time (convergence speed) is the central challenge; cluster methods achieve near-zero autocorrelation.
- Formally links statistical physics simulation with Bayesian computation.

---

## Skipped Papers (11 total)

| File | Reason |
|------|--------|
| 1.pdf | Minimal content ("Patterns") — insufficient text |
| 1204.1824v1.pdf | Web 2.0 / social networking security — not relevant |
| 1306.2859v1.pdf | Mathematics of music / Fourier for chord extraction — primarily music theory |
| 1407.5757v1.pdf | Group theory in music (Messiaen) — music theory |
| 1603.08904v4.pdf | Mathematical harmony analysis of chords — music theory |
| 1810.11372v3.pdf | Pattern avoidance and quasisymmetric functions — abstract combinatorics |
| 1907.11130v2.pdf | Percolating clusters in random networks — statistical physics, not computational methods |
| 2106.09750v2.pdf | Relativistic conformal symmetries (2D QFT) — theoretical physics |
| 2207.11035v5.pdf | Geometry of music perception — music/neuroscience |
| 2307.05604v3.pdf | Cartan calculus for C-infinity ringed spaces — abstract differential geometry |
| 2512.09956v1.pdf | Pythagorean musical scale mathematics — music theory |

---

*Total: 16 papers ingested, 11 papers skipped.*
