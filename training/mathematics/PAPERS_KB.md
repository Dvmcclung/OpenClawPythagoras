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

---

## Previously Skipped Papers (Music Theory, Abstract Algebra, Physics)

*These papers were skipped in the initial ingestion pass. All are now included per updated scope: music theory provides mathematical frameworks relevant to signal analysis and structural modeling; abstract algebra/combinatorics connects to enumeration and symmetry in processes; physics papers contribute mathematical methods with broad applicability.*

---

### S1. "Patterns" (1.pdf)
**File:** `1.pdf`
**Authors:** Unknown
**Source:** Single-page document

**Core Contribution:**
This document contains only the word "Patterns" — no extractable mathematical content. Single-page stub with 9 characters total.

**Key Methods:** None (insufficient content).

**Potential Applications:** N/A — document is essentially empty.

**Note:** Likely a placeholder or corrupted/incomplete PDF. No useful knowledge can be extracted.

---

### S2. Web 2.0 Technologies and Social Networking Security Fears in Enterprises (2012)
**File:** `1204.1824v1.pdf`
**Authors:** Fernando Almeida (INESC TEC / University of Porto)
**Source:** International Journal of Advanced Computer Science and Applications, Vol.3 No.2, 2012

**Core Contribution:**
Surveys common security risks introduced by Web 2.0 and social networking technologies in enterprise environments. Catalogs threat vectors and proposes mitigation best practices.

**Key Methods / Frameworks:**
- Risk taxonomy for Web 2.0 threats: phishing, malware, data leakage, insider threats, unauthorized access.
- Security governance framework: policy layers, employee awareness, technical controls (firewalls, DLP, access controls).
- No novel mathematical framework — primarily empirical/policy research.

**Potential Applications to Mathematical Modeling:**
- Risk quantification models: probability × impact matrices for enterprise security risk.
- Network topology modeling: how information propagates through social graphs within enterprises.
- Bayesian threat modeling: updating threat probabilities based on observed incidents.
- Although not a math paper, its risk taxonomy could inform stochastic models of information security in supply chain / logistics networks.

---

### S3. On the Mathematics of Music: From Chords to Fourier Analysis (2013)
**File:** `1306.2859v1.pdf`
**Authors:** Nathan Lenssen and Deanna Needell
**Source:** arXiv:1306.2859 [math.HO]

**Core Contribution:**
Demonstrates how Fourier analysis underlies chord detection and audio processing. Bridges music theory and signal processing, motivating the Fourier transform through musical examples and showing how harmonic structure is encoded in frequency-domain representations.

**Key Methods / Formulas:**
- Continuous Fourier Transform: F(ω) = ∫ f(t) e^{-2πiωt} dt
- Discrete Fourier Transform (DFT): X[k] = Σ_{n=0}^{N-1} x[n] e^{-2πikn/N}
- Frequency-to-pitch mapping: pitch p = 69 + 12·log₂(f/440) (MIDI convention)
- Chord detection: compute DFT of audio signal → identify dominant frequency components → map to pitch classes → match against chord templates.
- Windowing (Short-Time Fourier Transform / spectrogram) for time-varying harmonic analysis.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Signal decomposition in any domain:** The Fourier framework is foundational for decomposing periodic/quasi-periodic signals in logistics (demand seasonality), finance (price cycles), and sensor data (vibration, temperature).
- **Frequency-domain feature extraction:** Applied to time series from supply chains, IoT sensors, or economic indicators.
- **Chord detection → pattern recognition analogy:** The template-matching approach is a prototype of classification by spectral similarity, applicable to anomaly detection in manufacturing processes.
- **Audio quality / noise filtering** in industrial monitoring.

---

### S4. Mathematics and Group Theory in Music (2014)
**File:** `1407.5757v1.pdf`
**Authors:** Athanase Papadopoulos
**Source:** arXiv:1407.5757 [math.HO]; Handbook of Group Actions, Vol. II

**Core Contribution:**
Shows through the work of composer Olivier Messiaen how group theory — specifically symmetry groups, modes of limited transposition, and non-retrogradable rhythms — is embedded in musical composition. Provides a rigorous mathematical analysis of the structures Messiaen consciously employed.

**Key Methods / Frameworks:**
- **Cyclic group Z₁₂:** The 12 pitch classes in equal temperament form Z₁₂; transposition is addition mod 12; inversion is negation mod 12.
- **Modes of Limited Transposition:** Subsets of Z₁₂ whose interval structure is preserved under fewer than 12 distinct transpositions — i.e., their stabilizer subgroup (under the transposition action) is non-trivial.
- **Non-retrogradable rhythms:** Palindromic rhythmic patterns that are invariant under time-reversal — the symmetry group is Z₂ (identity and reversal).
- **Symmetrical permutations:** Permutation groups acting on note sequences — specifically permutations that are their own inverses (involutions).
- **Dihedral group D₁₂:** Combined transpositions and inversions of pitch classes.
- Relation to broader group actions theory: orbits, stabilizers, fixed-point theorems.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Symmetry in scheduling and combinatorial optimization:** Group-theoretic symmetry reduction can dramatically prune the search space in scheduling and assignment problems.
- **Cyclic structure in periodic processes:** Z_n group structure models any system with discrete periodic states (shift scheduling, cyclic supply patterns).
- **Pattern classification by symmetry:** Identifying when a data pattern is "essentially the same" up to a symmetry transformation — useful in quality control and process monitoring.
- **Invariant feature design:** Features preserved under group actions are naturally robust — applicable to machine learning on structured data.

---

### S5. Mathematical Harmony Analysis: Measuring Structure, Properties, and Consonance of Harmonies, Chords, and Melodies (2017)
**File:** `1603.08904v4.pdf`
**Authors:** Dr. David Ryan (Edinburgh, UK)
**Source:** Self-published draft (Draft 04, January 2017), 51 pages

**Core Contribution:**
Develops a rigorous mathematical framework for measuring the consonance, complexity, and harmonic structure of musical chords and melodies. Introduces ComplexitySpace lattices, invariant functions on chords, and otonality/utonality measures as quantitative tools for harmonic analysis.

**Key Methods / Formulas:**
- **Invariant functions on chords:** Functions f(chord) that are unchanged under transposition and inversion — the mathematical analogue of perceptual invariants.
- **Complexity of a chord:** Defined via the prime factorization structure of frequency ratios — simpler ratios (lower primes) yield lower complexity (greater consonance). E.g., octave = 2/1 (complexity 1), perfect fifth = 3/2, major third = 5/4.
- **ComplexitySpace lattice:** A lattice structure over the factor space of frequency ratios, where nodes represent harmonic relationships and edges represent interval steps. Complexity is a lattice height function.
- **Otonality and Utonality (Partch):** Otonality = chord built on overtone series (harmonic series); Utonality = chord built on undertone series. Defined formally via ratio direction in ComplexitySpace.
- **Ratio invariants:** Functions on ordered interval ratios between chord tones — used to characterize chord quality independent of voicing.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Complexity metrics for hierarchical systems:** The complexity measure (via prime factorizations) can model cost/complexity of product variants, BOM (bill of materials) hierarchies, or supply network structures.
- **Lattice-based optimization:** ComplexitySpace lattice structures parallel lattice models used in scheduling, inventory, and combinatorial optimization.
- **Consonance as fitness function:** The concept of consonance (low-complexity ratio) is analogous to measuring "fit" or "compatibility" in constraint satisfaction problems.
- **Signal ratio analysis:** The framework for analyzing ratios between frequencies applies directly to any domain where ratios of measurements matter (yield ratios, exchange rates, load factors).

---

### S6. Pattern Avoidance and Quasisymmetric Functions (2018)
**File:** `1810.11372v3.pdf`
**Authors:** Zachary Hamaker (U Michigan), Brendan Pawlowski (USC), Bruce E. Sagan (Michigan State)
**Source:** arXiv:1810.11372 [math.CO]

**Core Contribution:**
Establishes a deep connection between permutation pattern avoidance (a combinatorial property) and quasisymmetric/symmetric functions (algebraic objects). Characterizes which sets of forbidden patterns Π ⊆ S₃ yield generating functions Qₙ(Π) that are symmetric or Schur-nonnegative — bridging enumerative combinatorics and algebraic combinatorics.

**Key Methods / Frameworks:**
- **Pattern avoidance:** Permutation σ avoids pattern π if no subsequence of σ standardizes to π. Sₙ(Π) = set of permutations of [n] avoiding all π ∈ Π.
- **Descent set:** Des(σ) = {i : σᵢ > σᵢ₊₁}; fundamental quasisymmetric function Fₛ = Σ xᵢ₁···xᵢₖ over weakly increasing chains with strict increase at descent positions.
- **Generating function:** Qₙ(Π) = Σ_{σ ∈ Sₙ(Π)} F_{Des σ} — a quasisymmetric function encoding the distribution of descents in pattern-avoiding permutations.
- **Symmetric and Schur-nonneg:** Qₙ(Π) is symmetric if it equals a symmetric function; Schur-nonneg if its Schur expansion has non-negative coefficients (combinatorial positivity).
- **Robinson-Schensted correspondence:** Bijection between permutations and pairs of Young tableaux — key to linking pattern avoidance with Schur functions.
- **Knuth classes and shuffles:** Equivalence classes of permutations sharing the same recording tableau; shuffle products of quasisymmetric functions.
- **Arc permutations** (Elizalde-Roichman): Related class connecting to the main results.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Counting constrained sequences:** Pattern avoidance counts sequences satisfying ordering constraints — directly applicable to scheduling (forbidden orderings of tasks), routing (forbidden subsequences of nodes), and inventory management (forbidden reorder patterns).
- **Generating function methods:** Quasisymmetric generating functions provide closed-form enumeration tools for complex combinatorial structures.
- **Symmetry detection in data:** Schur-nonnegativity is a positivity certificate — analogous to verifying that a model's output is a valid probability distribution.
- **Combinatorial optimization:** Understanding the structure of S_n(Π) enables efficient enumeration of feasible solutions in constrained combinatorial problems.

---

### S7. Structure of Percolating Clusters in Random Clustered Networks (2020)
**File:** `1907.11130v2.pdf`
**Authors:** Takehisa Hasegawa, Shogo Mizutaka (Ibaraki University, Japan)
**Source:** arXiv:1907.11130 [physics.soc-ph]

**Core Contribution:**
Analyzes the structural properties (clustering coefficient, assortativity) of the giant percolating cluster (PC) that emerges in random clustered network models under site percolation. Shows analytically that highly clustered networks retain clustering even at the percolation threshold, and that assortativity of the PC depends sensitively on network structure.

**Key Methods / Formulas:**
- **Random Clustered Network (RCN) model:** Nodes assigned joint degree (s, t) = (edge count, triangle count); networks generated by pairing stubs and triangle corners randomly.
- **Generating function formalism:**
  - G₀(x,y) = Σ_{s,t} p_{s,t} x^s y^t (degree-triangle distribution PGF)
  - G₁, G₂ derived generating functions for branching processes along edges/triangles
  - PC size: S = 1 − G₀(u,v) where (u,v) satisfy fixed-point equations from G₁, G₂
- **Percolation threshold f_c:** Value of site occupation probability f where giant component first appears — found by linearizing the fixed-point equations.
- **Clustering coefficient of PC:** C_PC = (triangles in PC) / (potential triangles in PC) — computed analytically via generating functions.
- **Assortative coefficient r (Pearson):** r = [Σ_{jk} jk(e_{jk} − q_j q_k)] / σ_q² where e_{jk} is the joint degree distribution of connected node pairs.
- **Fractal vs. non-fractal:** At threshold, PC is fractal (self-similar under renormalization); renormalization reveals disassortative nature even when raw r > 0.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Supply chain network resilience:** Percolation models directly apply to supply network disruption — f_c is the "critical fraction" of node failures that collapses the network.
- **Epidemic/cascade modeling:** RCN percolation models spread of disruptions, diseases, or information through clustered social/business networks.
- **Logistics hub network design:** Clustering coefficient and assortativity characterize robustness to targeted vs. random failures — informs which nodes (hubs) to protect.
- **Internet and communication network reliability:** The generating function formalism has been applied to router failure models.
- **Phase transitions in complex systems:** The percolation threshold framework is a universal tool for understanding tipping points in interconnected systems.

---

### S8. Mapping Relativistic to Ultra/Non-Relativistic Conformal Symmetries in 2D and Finite √TT̄ Deformations (2021)
**File:** `2106.09750v2.pdf`
**Authors:** Pablo Rodríguez, David Tempo, Ricardo Troncoso (CECs Valdivia; U. de Los Lagos; U. Católica de Temuco, Chile)
**Source:** arXiv:2106.09750 [hep-th]

**Core Contribution:**
Shows that the 2D conformal algebra Diff(S¹) ⊕ Diff(S¹) maps to its ultra/non-relativistic version (BMS₃ ≈ GCA₂) through an exact nonlinear map — without taking limits. Demonstrates that BMS₃ symmetry emerges naturally when a CFT₂ is deformed by a √TT̄ term in the Hamiltonian.

**Key Methods / Formulas:**
- **Virasoro algebra (CFT₂):** [Lₘ, Lₙ] = (m−n)Lₘ₊ₙ + c/12·m(m²−1)δₘ₊ₙ,₀ (centrally extended)
- **BMS₃ algebra:** [Jₘ, Jₙ] = (m−n)Jₘ₊ₙ; [Jₘ, Pₙ] = (m−n)Pₘ₊ₙ; [Pₘ, Pₙ] = 0
- **Nonlinear generator map:** BMS₃ generators expressed as composites of chiral stress-energy tensor components T and T̄: Jₘ ∼ contraction of T, T̄; Pₘ ∼ other composite — closes under Poisson brackets.
- **√TT̄ deformation:** Hamiltonian H → H + λ·√(TT̄); deformation parameter λ controls departure from CFT₂ toward BMS₃-symmetric theory.
- **Deformed conformal Killing equations:** BMS₃ symmetries arise as diffeomorphisms preserving the deformed metric and stress-energy tensor up to local scalings.
- **Cardy formula mapping:** The modular S-transformation of the torus maps to its BMS₃ (flat space) analog — relating density of states in CFT₂ to BMS₃ theory.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Symmetry algebra methods for PDEs:** The BMS₃/Virasoro mapping provides algebraic tools for solving certain classes of nonlinear PDEs (relevant in fluid dynamics and continuum mechanics).
- **Deformed symmetry in statistical mechanics:** TT̄ deformations modify how systems respond to scale changes — applicable to renormalization group flow models.
- **Fluid dynamics in 2D:** BMS₃ algebra appears in 2D fluid models; this paper provides a systematic way to derive BMS₃-symmetric theories from better-understood CFT₂ systems.
- **Mathematical framework for horizon dynamics:** BMS symmetries characterize near-horizon geometry — potentially useful in thermodynamic modeling of black holes and analogous systems.
- **Integrable systems:** The algebraic map connects CFT₂ (widely used in integrable field theory) to BMS₃ theories — extending integrability tools to a broader class of models.

---

### S9. Geometry of Music Perception (2022)
**File:** `2207.11035v5.pdf`
**Authors:** Benjamin Himpel (Reutlingen University, Dept. Computer Science)
**Source:** arXiv:2207.11035

**Core Contribution:**
Constructs a rigorous geometric model for music perception by combining neuroscientific theories of pitch perception with acoustic observations. Models the space of all chords as a Whitney stratified space (a union of Riemannian manifolds), yielding a natural geodesic distance compatible with voice-leading. Enables rigorous study of psychoacoustic quantities (roughness, harmonicity) as geometric height functions.

**Key Methods / Frameworks:**
- **Whitney stratified space:** The chord space = ⊔ Mₖ (disjoint union of strata Mₖ by chord size k), each stratum a Riemannian manifold. Allows calculus on a space with singularities.
- **Geodesic distance across strata:** Defined by minimizing path length (voice-leading = minimal motion of individual voices) — satisfies the triangle inequality.
- **Riemannian metric on chord space:** Inherited from pitch space (R or torus T¹) via quotient construction.
- **Roughness as height function:** Roughness R(chord) = Σᵢ<ⱼ r(|fᵢ − fⱼ|) summed over critical band interactions — a smooth function on each stratum.
- **Harmonicity as height function:** H(chord) = measure of alignment with harmonic series — related to virtual pitch perception (Terhardt model).
- **Chord resolution geometry:** Tension/resolution modeled as gradient flow on the roughness/harmonicity landscape — chords "resolve" toward local minima.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Stratified space methods in optimization:** Many real-world configuration spaces are stratified (robot arm configurations, option spaces in combinatorial problems) — this geometric framework provides a calculus for such spaces.
- **Geodesic distance in high-dimensional data:** The voice-leading metric is a minimum-cost matching distance — equivalent to Earth Mover's Distance (Wasserstein distance), used in supply chain cost modeling, demand distribution comparison.
- **Height functions on manifolds for optimization:** Modeling objective functions as height functions on geometric spaces enables gradient-based and topological optimization methods.
- **Psychoacoustic-inspired feature spaces:** Roughness and harmonicity-style features can be extracted from any signal with frequency content — applicable to sensor data quality and anomaly detection.

---

### S10. Cartan Calculus for C∞-Ringed Spaces (2024)
**File:** `2307.05604v3.pdf`
**Authors:** Eugene Lerman (University of Illinois)
**Source:** arXiv:2307.05604 [math.DG]

**Core Contribution:**
Extends the classical Cartan calculus (vector fields, differential forms, Lie derivatives, interior products, exterior derivative) from smooth manifolds to the broader category of local C∞-ringed spaces — which includes manifolds with corners, differential spaces, affine C∞-schemes, and stratifolds. The goal is to enable coordinate-free geometric mechanics (Euler-Lagrange equations, Hamiltonian mechanics) on singular/non-manifold spaces.

**Key Methods / Formulas:**
- **C∞-ringed space (X, O_X):** A topological space X with a sheaf O_X of C∞-rings (rings closed under all smooth functions, not just polynomials).
- **Tangent sheaf:** Vector fields defined as sheaf derivations of O_X: χ(X) = Der(O_X) — derivations v: O_X → O_X satisfying the Leibniz rule.
- **Differential forms:** Ω•(X) = graded-commutative DGA with exterior derivative d, extending de Rham complex to ringed spaces.
- **Cartan calculus identity (Cartan magic formula):** Lᵥ = d ∘ ıᵥ + ıᵥ ∘ d where ıᵥ = contraction by v, Lᵥ = Lie derivative along v.
- **Interior product:** ıᵥ: Ωⁿ(X) → Ωⁿ⁻¹(X), degree −1 derivation of exterior algebra.
- **Lie derivative on forms:** Lᵥω = [d, ıᵥ]ω — the graded commutator of d and ıᵥ.
- Applications to C∞-schemes, differential spaces (Sikorski), stratifolds (Kreck).

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Geometric mechanics on configuration spaces with constraints:** Robot arms, mechanical linkages, and constrained logistics systems have configuration spaces that are singular (e.g., with corners or bifurcations) — this framework enables Lagrangian/Hamiltonian mechanics on them.
- **Euler-Lagrange equations on non-smooth domains:** Supply network flows, piecewise-linear cost structures, and logistics problems with inequality constraints produce non-smooth state spaces — Cartan calculus on ringed spaces provides rigorous tools.
- **Hybrid dynamical systems:** Systems that switch between modes (e.g., trucks switching between routes, warehouses switching between modes) have phase spaces naturally described as stratified spaces.
- **Sheaf-theoretic modeling:** The sheaf-of-rings framework has been applied to network flows, sensor fusion, and topological data analysis.

---

### S11. The Two-Step Property and the Mathematics of Musical Scale Size (2024)
**File:** `2512.09956v1.pdf`
**Authors:** Emily Clader and Vanessa Jelmyer
**Source:** arXiv:2512.09956

**Core Contribution:**
Gives a complete mathematical characterization of which n-note Pythagorean scales (generated by powers of 3/2, reduced to the octave [1,2]) satisfy the "2-step property" — a precise measure of even spacing. Proves that the 5-note (pentatonic), 7-note (diatonic), and 12-note (chromatic) scales are distinguished by this property, connecting number theory to music.

**Key Methods / Formulas:**
- **Pythagorean scale:** n-note scale = {3^k / 2^⌊k·log₂3⌋ : k = 0, 1, …, n−1} ⊂ [1,2], sorted in increasing order.
- **Step sizes:** Intervals between consecutive scale tones. A scale has the 2-step property if all step sizes take only 2 distinct values.
- **2-step characterization theorem:** An n-note Pythagorean scale has the 2-step property iff n satisfies a Diophantine condition related to the continued fraction expansion of log₂3 (an irrational number). Specifically, n must be a denominator of a convergent (or semi-convergent) in the continued fraction of log₂3 = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, …].
- **Three distance theorem (Steinhaus):** For irrational α, the sequence {kα mod 1}_{k=0}^{n-1} partitions [0,1) into intervals of at most 3 distinct lengths — equality of 2 lengths gives the 2-step property. Scale sizes n satisfying this: 1, 2, 3, 5, 7, 12, 17, 29, 41, 53, …
- **Connection to best rational approximations:** The "good" scale sizes correspond to denominators of best rational approximations to log₂3 — explaining why 12-tone equal temperament is so accurate.

**Potential Applications to Mathematical Modeling of Real-World Processes:**
- **Optimal discretization and quantization:** The 2-step property characterizes maximally even discrete samplings of a continuous interval — directly applicable to optimal bin/grid sizing in numerical methods and histogram design.
- **Three-distance theorem in scheduling:** The spacing of events {kα mod 1} models cyclic scheduling with irrational frequency ratios — the theorem guarantees at most 3 gap sizes, useful in analyzing cyclic inventory replenishment.
- **Continued fraction methods in optimization:** Best rational approximations (convergents) minimize approximation error — applicable to finding optimal integer parameters in periodic scheduling, gear ratios, and sampling rates.
- **Number-theoretic structure in periodic processes:** The framework reveals why certain cycle lengths (5, 7, 12, …) are structurally optimal — generalizable to any system seeking maximally uniform periodic spacing.

---

*Total: 16 papers (original ingestion) + 11 previously skipped papers = 27 papers total in knowledge base.*
