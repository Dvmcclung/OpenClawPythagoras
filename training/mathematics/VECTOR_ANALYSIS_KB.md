# VECTOR_ANALYSIS_KB.md
# Knowledge Base: Vector Mathematics, Embeddings, and AI Search Systems
# For use by Pythagoras AI — Quantix Supply Chain Solutions
# Last updated: 2026-03-04

---

## TABLE OF CONTENTS

1. Vector Mathematics Fundamentals
2. Linear Algebra for Machine Learning
3. PCA and Dimensionality Reduction
4. SVD (Singular Value Decomposition)
5. Text Embeddings and Semantic Representations
6. Similarity Metrics
7. Vector Databases
8. HNSW Indexing
9. RAG (Retrieval Augmented Generation) Architecture
10. Vector Search in Supply Chain Applications
11. Python Code Examples
12. Quick Reference

---

## 1. VECTOR MATHEMATICS FUNDAMENTALS

### 1.1 Vectors

A vector is an ordered array of numbers representing a point or direction in n-dimensional space.

**Notation:**
v = [v₁, v₂, ..., vₙ]ᵀ  (column vector in R^n)

**Operations:**
Addition:       u + v = [u₁+v₁, u₂+v₂, ..., uₙ+vₙ]
Scalar mult:    αv = [αv₁, αv₂, ..., αvₙ]
Dot product:    u · v = Σᵢ uᵢvᵢ = |u||v|cos(θ)

**Norms (vector lengths):**
L1 norm (Manhattan):  ||v||₁ = Σ|vᵢ|
L2 norm (Euclidean):  ||v||₂ = √(Σvᵢ²)
Lp norm:              ||v||_p = (Σ|vᵢ|^p)^{1/p}
L∞ norm:              ||v||_∞ = max|vᵢ|

**Unit vector:** v̂ = v / ||v||₂  (normalized to length 1)

### 1.2 Distance Metrics

**Euclidean distance:**
d_E(u, v) = ||u - v||₂ = √(Σᵢ (uᵢ - vᵢ)²)

**Manhattan distance:**
d_M(u, v) = ||u - v||₁ = Σᵢ |uᵢ - vᵢ|

**Cosine distance:**
d_cos(u, v) = 1 - cos(θ) = 1 - (u·v)/(||u||·||v||)
Range: [0, 2]. Value 0 = identical direction. Value 1 = orthogonal. Value 2 = opposite.

**Note:** Cosine similarity measures angle between vectors, not magnitude.
Two vectors can be far apart in Euclidean space but have cosine similarity = 1
if they point in the same direction.

**Hamming distance:** Number of positions where two binary vectors differ.
Used for: binary embeddings, hash codes.

**Minkowski distance:** Generalization: d(u, v) = (Σ|uᵢ - vᵢ|^p)^{1/p}
p=1: Manhattan; p=2: Euclidean; p→∞: Chebyshev

### 1.3 Inner Product Spaces

An inner product <u, v> generalizes the dot product:
Properties: bilinearity, symmetry, positive definiteness.

The standard Euclidean inner product: <u, v> = uᵀv = Σ uᵢvᵢ

**Orthogonality:** u ⊥ v iff <u, v> = 0
**Gram-Schmidt process:** Construct orthogonal basis from arbitrary basis.

---

## 2. LINEAR ALGEBRA FOR MACHINE LEARNING

### 2.1 Matrices

Matrix A ∈ R^{m×n}: m rows, n columns.

**Key operations:**
Matrix multiply: (AB)_{ij} = Σ_k A_{ik} B_{kj}    requires A ∈ R^{m×n}, B ∈ R^{n×p}
Transpose:       (Aᵀ)_{ij} = A_{ji}
Inverse:         AA⁻¹ = I   (only for square, non-singular matrices)

**Special matrices:**
Symmetric:       A = Aᵀ
Orthogonal:      QᵀQ = QQᵀ = I  (columns are orthonormal)
Positive definite: xᵀAx > 0 for all x ≠ 0  (implies all eigenvalues > 0)
Diagonal:        Off-diagonal elements = 0

### 2.2 Eigendecomposition

For square matrix A: eigenvalue λ and eigenvector v satisfy:
Av = λv

**Eigenvalue properties:**
- For symmetric matrix A: all eigenvalues are real, eigenvectors are orthogonal
- Trace(A) = Σ λᵢ
- det(A) = Π λᵢ
- If any λᵢ = 0: matrix is singular (non-invertible)

**Spectral decomposition (for symmetric A):**
A = QΛQᵀ  where Q = orthogonal matrix of eigenvectors, Λ = diagonal eigenvalue matrix

Geometric interpretation: A stretches space along eigenvector directions by eigenvalue factors.

### 2.3 The Covariance Matrix

For data matrix X ∈ R^{n×d} (n samples, d features):
Centered: X̃ = X - μ (subtract column means)
Covariance: Σ = (1/(n-1)) X̃ᵀX̃  ∈ R^{d×d}

Diagonal elements: variances of each feature
Off-diagonal: covariances (strength of linear relationship)

**Correlation matrix:**
C_{ij} = Σ_{ij} / (σᵢ σⱼ)  ∈ [-1, 1]

The covariance matrix is always symmetric positive semidefinite.
Its eigenvalues are variances along principal component axes.

---

## 3. PCA AND DIMENSIONALITY REDUCTION

### 3.1 Principal Component Analysis (PCA)

PCA finds the orthogonal directions of maximum variance in data.
Projects high-dimensional data to a lower-dimensional subspace.

**Algorithm:**
1. Center data: X̃ = X - μ
2. Compute covariance matrix: Σ = X̃ᵀX̃ / (n-1)
3. Eigendecompose: Σ = QΛQᵀ
4. Sort eigenvectors by descending eigenvalue
5. Select top k eigenvectors as principal components W ∈ R^{d×k}
6. Project: Z = X̃W  (scores, n×k)

**Principal components:**
- PC1: direction of maximum variance (largest eigenvalue)
- PC2: direction of maximum variance orthogonal to PC1
- Each PC is orthogonal to all others

### 3.2 Explained Variance

Variance explained by PC_i: λᵢ / Σ λⱼ

Cumulative explained variance: Σ_{i=1}^k λᵢ / Σ λⱼ

**Elbow method:** Plot cumulative explained variance vs. k.
Choose k where adding more components gives diminishing returns.

**Kaiser criterion:** Retain PCs with eigenvalue > 1 (explain more variance than a single variable).

### 3.3 PCA in Practice

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np

# Standardize (PCA is scale-sensitive)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit PCA
pca = PCA(n_components=0.95)  # retain 95% of variance
X_pca = pca.fit_transform(X_scaled)

print(f"Original dimensions: {X.shape[1]}")
print(f"Reduced dimensions: {X_pca.shape[1]}")
print(f"Explained variance: {pca.explained_variance_ratio_.cumsum()[-1]:.3f}")

# Loadings: contribution of each original feature to each PC
loadings = pca.components_  # shape: (n_components, n_features)
```

### 3.4 Applications in Supply Chain

**Customer segmentation:** Reduce many behavioral features to 2-3 PCs for visualization.
**Product clustering:** Reduce SKU attribute space for similarity search.
**Anomaly detection:** Fit PCA to normal operations; high reconstruction error = anomaly.
**Demand pattern analysis:** Reduce 365-day demand vectors to low-dimensional representations.

### 3.5 t-SNE and UMAP

For **visualization** (2D or 3D only, not general dimensionality reduction):

**t-SNE (t-Distributed Stochastic Neighbor Embedding):**
- Preserves local neighborhood structure
- Non-linear: captures clusters that PCA misses
- Stochastic and non-deterministic (different runs give different results)
- Computationally expensive: O(N²) → use Barnes-Hut approximation for large N
- **Warning:** Global structure (distances between clusters) not preserved

**UMAP:**
- Generally faster than t-SNE, more scalable
- Better preserves global structure
- Can be used for actual dimensionality reduction (not just visualization)
- Deterministic with fixed seed

---

## 4. SVD (SINGULAR VALUE DECOMPOSITION)

### 4.1 Definition

Every matrix A ∈ R^{m×n} can be decomposed as:
A = UΣVᵀ

where:
U ∈ R^{m×m}: orthogonal matrix (left singular vectors)
Σ ∈ R^{m×n}: diagonal matrix of singular values σ₁ ≥ σ₂ ≥ ... ≥ 0
V ∈ R^{n×n}: orthogonal matrix (right singular vectors)

### 4.2 Truncated SVD (Low-Rank Approximation)

Best rank-k approximation to A (Eckart-Young theorem):
A ≈ A_k = U_k Σ_k V_kᵀ

where U_k, Σ_k, V_k retain only the top k singular vectors/values.

**Frobenius error:** ||A - A_k||_F = √(Σ_{i>k} σᵢ²)

This is the optimal low-rank approximation in both Frobenius and spectral norm.

### 4.3 Relationship to PCA

If X is centered:
PCA = eigendecomposition of XᵀX
SVD of X gives: X = UΣVᵀ
Then: XᵀX = VΣ²Vᵀ → V = PCA eigenvectors, σᵢ² = (n-1) × eigenvalues

**Practical:** Use `sklearn.decomposition.TruncatedSVD` for sparse matrices
(e.g., TF-IDF document-term matrices) where centering is impractical.

### 4.4 SVD Applications

**Latent Semantic Analysis (LSA):** Apply SVD to TF-IDF matrix.
Rows = documents, columns = terms, values = TF-IDF weights.
U_k V_kᵀ: documents and terms in shared "concept" space.
Similar documents → similar U rows. Similar terms → similar V rows.

**Matrix factorization for recommendation:**
User-item matrix R ≈ U_k Σ_k V_kᵀ
U: user latent factors, V: item latent factors.
Used in Netflix Prize winner; scales to millions of users/items.

**Image compression:** Truncated SVD compresses images by retaining top k singular values.

---

## 5. TEXT EMBEDDINGS AND SEMANTIC REPRESENTATIONS

### 5.1 What Are Embeddings?

An embedding is a dense, fixed-length vector representation of an entity
(text, image, product, location) in a continuous vector space.

**Key property:** Semantically similar entities have vectors that are geometrically close.

"King" - "Man" + "Woman" ≈ "Queen"  (Word2Vec famous example)

### 5.2 Word2Vec

Two architectures (Mikolov et al., 2013):
**CBOW:** Predict center word from context → good for common words.
**Skip-gram:** Predict context from center word → better for rare words.

Training: maximize probability of observed context words given center word.
Embeds each word as d-dimensional vector (typically d = 100-300).
Captures syntactic and semantic relationships as vector arithmetic.

### 5.3 Transformer-Based Embeddings

Modern embeddings from transformer models (BERT, GPT, etc.) are contextual:
the same word gets a different vector depending on context.

**Sentence transformers (SBERT):** Optimized for sentence/paragraph-level similarity.
Train on semantic textual similarity (STS) tasks.
Output: fixed-length embedding for any input text.

**Popular embedding models:**
- `all-MiniLM-L6-v2`: Fast, small (22M params), d=384. Good for search.
- `all-mpnet-base-v2`: Higher quality, d=768. Better for complex queries.
- OpenAI `text-embedding-3-small`: d=1536. Excellent general-purpose.
- OpenAI `text-embedding-3-large`: d=3072. State-of-the-art quality.

### 5.4 Embedding Properties

**Dimension:** d = 128 to 3072 depending on model.
Higher d → more expressive but more storage and slower search.

**Normalization:** Most embedding models output L2-normalized vectors.
||e||₂ = 1 for all embeddings.
Consequence: for normalized vectors, cosine similarity = dot product.
cos(u, v) = u·v / (||u||·||v||) = u·v  (since ||u|| = ||v|| = 1)

**Embedding space geometry:**
- Nearby vectors: semantically similar
- Distant vectors: semantically unrelated
- Vector arithmetic: meaningful (analogy reasoning)
- Clustering reveals semantic groupings

### 5.5 How to Generate Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed texts
documents = [
    "Freight rates increased due to port congestion",
    "Carrier capacity is constrained this quarter",
    "Weather delays are affecting delivery times",
    "Inventory levels are critically low",
    "Demand spike expected for holiday season"
]
embeddings = model.encode(documents, normalize_embeddings=True)
print(f"Shape: {embeddings.shape}")  # (5, 384)
```

---

## 6. SIMILARITY METRICS

### 6.1 Cosine Similarity

cos(u, v) = (u · v) / (||u||₂ × ||v||₂)

Range: [-1, 1]
- 1: identical direction (same content)
- 0: orthogonal (unrelated)
- -1: opposite direction (antonyms)

**Why cosine for text:** Documents of different lengths have different vector magnitudes.
Cosine normalizes by length, comparing angle (topic) rather than magnitude (length).

```python
import numpy as np

def cosine_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# Vectorized (all pairs)
def cosine_similarity_matrix(embeddings):
    # Assumes L2-normalized embeddings
    return embeddings @ embeddings.T  # dot product = cosine similarity

sim_matrix = cosine_similarity_matrix(embeddings)
print(f"Similarity between doc 0 and doc 1: {sim_matrix[0,1]:.4f}")
```

### 6.2 Dot Product Similarity

For L2-normalized vectors: dot product = cosine similarity.
Many vector databases and ML frameworks use dot product internally
because it's faster (no division needed after normalization).

**OpenAI embeddings are L2-normalized:** Use dot product for speed.

### 6.3 Euclidean Distance vs Cosine Similarity

For normalized vectors: d_E(u,v)² = 2(1 - cos(u,v))
They are monotonically related for normalized vectors.
Choice depends on implementation (HNSW supports both).

### 6.4 Choosing the Right Metric

| Use Case                        | Recommended Metric    |
|---------------------------------|-----------------------|
| Text semantic similarity        | Cosine                |
| Document retrieval              | Cosine / Dot product  |
| Image similarity                | Euclidean or Cosine   |
| Geographic distance             | Haversine (spherical) |
| Sparse binary vectors           | Hamming / Jaccard     |
| Dense numerical features        | Euclidean             |
| Recommendation (collaborative)  | Dot product           |

---

## 7. VECTOR DATABASES

### 7.1 What Is a Vector Database?

A vector database is a specialized database designed to store, index, and
efficiently search high-dimensional embedding vectors.

**Core capabilities:**
- Store millions to billions of embedding vectors
- Perform fast approximate nearest neighbor (ANN) search
- Return top-k most similar vectors to a query
- Support metadata filtering (e.g., "find similar documents from 2025")
- Handle real-time upserts and deletes

**Why not use a traditional database?**
SQL SELECT with exact similarity would require O(N × d) operations for N vectors.
ANN indexes reduce this to O(log N) or O(√N) with acceptable recall trade-off.

### 7.2 Approximate Nearest Neighbor (ANN) vs Exact Search

**Exact k-NN:** Find the true k most similar vectors.
- Requires scanning all N vectors: O(N × d) per query
- Scales poorly: N=10M vectors, d=1536, 10K queries/sec → not feasible

**ANN:** Find k vectors that are very likely to be the nearest neighbors.
- Typical recall@k = 0.95–0.99 (95–99% of true nearest neighbors returned)
- Query time: O(log N) to O(√N) depending on algorithm
- Acceptable trade-off for most real-world applications

### 7.3 Vector Database Landscape

**Dedicated vector databases:**
- **Pinecone:** Fully managed cloud service. High performance, easy scaling.
- **Weaviate:** Open source, multi-modal, GraphQL API.
- **Qdrant:** Open source, Rust-based, fast, self-hosted or cloud.
- **Chroma:** Lightweight, developer-friendly, good for prototyping.
- **Milvus:** Open source, production-grade, cloud-native.

**Vector search extensions for traditional DBs:**
- **pgvector** (PostgreSQL extension): Adds ivfflat and HNSW index types.
- **Redis VSS:** Vector Similarity Search in Redis.
- **Elasticsearch dense_vector:** KNN search in Elasticsearch.
- **SQLite-vss:** SQLite extension (local, embedded use cases).

**FAISS (Facebook AI Similarity Search):**
Library (not a database) for efficient ANN. C++/Python.
Used internally by many vector databases.
Index types: IVFFlat, IVFPQ, HNSW, ScaNN.

### 7.4 Index Types Overview

**Flat (Exact):**
- No indexing; brute-force scan
- Recall = 1.0 always
- Use for: small datasets (< 100K), when recall must be exact

**IVF (Inverted File Index):**
- Cluster vectors into nlist cells using k-means
- Query: probe nprobe nearest cells, search within them
- Trade-off: nprobe ↑ → recall ↑, speed ↓
- Use for: large datasets when moderate speed/recall is acceptable

**PQ (Product Quantization):**
- Compress vectors: split into M subvectors, quantize each to 256 codes
- Reduces storage by 8–96× vs float32
- Use for: memory-constrained scenarios

**IVF+PQ (IVFPQ):** Combine clustering + compression.

**HNSW:** Graph-based, top-performing algorithm. See Section 8.

---

## 8. HNSW INDEXING

### 8.1 Background: Two Foundational Ideas

HNSW (Hierarchical Navigable Small World) builds on two prior concepts:

**1. Probability Skip List (Pugh, 1990):**
- Multi-layer linked list structure
- Top layers: long-range "skip" links for fast traversal
- Bottom layers: short-range links for precise search
- Search starts at top (coarse), descends to bottom (precise)
- Analogous to express vs local subway trains

**2. Navigable Small World (NSW) Graphs:**
- Proximity graph: connect each vector to M nearest neighbors
- "Small world" property: most vectors reachable in log(N) hops
- Greedy search: start at entry point, always move to nearest neighbor
- Natural stopping point: local minimum (no nearer neighbor in friend list)
- Limitation: gets stuck in local minima for large N

### 8.2 HNSW Construction

HNSW combines these ideas:

**Structure:** Multi-layer graph (like skip list).
Each vector is inserted at a randomly assigned maximum layer.
Assignment probability: P(layer ≥ l) = e^{-l/m_L}  (exponential, controlled by m_L)
Most vectors appear only in layer 0 (dense); fewer in higher layers (sparse).

**Insertion algorithm:**
1. Randomly assign new vector's maximum layer level
2. For each layer from top down to layer 0:
   - Find M nearest neighbors at this layer using greedy search
   - Add bidirectional edges between new vector and its neighbors
3. If new vector's level > current entry point level, update entry point

**Key parameter M:** Number of connections per vector per layer.
Higher M → better recall but more memory and slower construction.
Typical: M = 16–64.

### 8.3 HNSW Search

Query vector q, find k nearest neighbors:

1. Start at entry point (highest layer)
2. Greedy search: move to whichever connected neighbor is closest to q
3. Repeat until local minimum found at this layer
4. Descend to next layer, continue from last position
5. At layer 0: collect ef_search candidate neighbors (ef_search ≥ k)
6. Return top-k from candidates

**Key parameter ef_search:** Size of dynamic candidate list during search.
Higher ef_search → better recall but slower search.
Minimum: ef_search ≥ k.

### 8.4 HNSW Parameters

| Parameter  | Effect                              | Typical Range |
|------------|-------------------------------------|---------------|
| M          | Edges per node per layer            | 16–64         |
| ef_construction | Search quality during build   | 100–200       |
| ef_search  | Search quality at query time        | 50–500        |
| m_L        | Layer probability multiplier        | 1/ln(M)       |

**M and ef_construction** are set at index build time (cannot change without rebuild).
**ef_search** can be tuned at query time for recall/speed trade-off.

### 8.5 HNSW Complexity

**Build:** O(N log N)
**Query:** O(log N)
**Memory:** O(N × M × layers × d) — grows linearly with N

**Performance benchmarks** (approximate, hardware-dependent):
- 1M vectors, d=128: query in ~0.1ms with recall@10 > 0.99
- 100M vectors, d=768: query in ~1-5ms with recall@10 > 0.95

### 8.6 Databases Using HNSW

All major vector databases support HNSW:
- PostgreSQL (pgvector): `CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64)`
- Qdrant, Weaviate, Milvus, Chroma: native HNSW support
- FAISS: `IndexHNSWFlat`, `IndexHNSWSQ`
- Oracle DB 23ai: AI Vector Search with HNSW

### 8.7 FAISS HNSW Implementation

```python
import faiss
import numpy as np

d = 384          # embedding dimension
M = 32           # HNSW M parameter
ef_construction = 200

# Build index
index = faiss.IndexHNSWFlat(d, M)
index.hnsw.efConstruction = ef_construction

# Add vectors
vectors = np.random.rand(100000, d).astype(np.float32)
faiss.normalize_L2(vectors)  # L2 normalize for cosine similarity
index.add(vectors)

# Search
query = np.random.rand(1, d).astype(np.float32)
faiss.normalize_L2(query)
index.hnsw.efSearch = 64  # query-time parameter

k = 10
distances, indices = index.search(query, k)
print(f"Top-{k} nearest neighbors: {indices[0]}")
print(f"Distances (cosine): {distances[0]}")
```

---

## 9. RAG (RETRIEVAL AUGMENTED GENERATION) ARCHITECTURE

### 9.1 What Is RAG?

RAG is an AI architecture that connects a Large Language Model (LLM) with
an external knowledge base (vector database), enabling the LLM to generate
responses grounded in specific, up-to-date, or proprietary information.

**Definition (IBM):** "An architecture for optimizing the performance of an
AI model by connecting it with external knowledge bases."

**Definition (AWS):** "The process of optimizing the output of an LLM so it
references an authoritative knowledge base outside of its training data sources
before generating a response."

**Key benefits:**
- Reduces LLM hallucinations (grounded in retrieved facts)
- Provides access to proprietary/current information (no retraining needed)
- Citable sources (verifiable, like footnotes in research papers)
- Easily updatable: add documents to KB without retraining the model
- Cost-effective vs. fine-tuning for knowledge-intensive tasks

### 9.2 RAG Architecture Components

```
                    ┌─────────────────────────────────────┐
  INDEXING PHASE    │  Knowledge Base Documents            │
  (offline)         │  (PDFs, emails, database records)    │
                    └──────────────┬──────────────────────┘
                                   │
                              [Chunking]
                                   │
                              [Embedding Model]
                                   │
                            [Vector Database] ←── index stored
                    ┌─────────────────────────────────────┐
  RETRIEVAL PHASE   │  User Query                          │
  (online)          └──────────────┬──────────────────────┘
                                   │
                              [Embed Query]
                                   │
                         [ANN Search in VectorDB]
                                   │
                         [Top-k Relevant Chunks]
                                   │
                              [Prompt Assembly]
                              (query + chunks)
                                   │
                                  [LLM]
                                   │
                            [Generated Answer]
```

### 9.3 Step-by-Step RAG Process

**Phase 1: Indexing (offline, run once or periodically)**

1. **Load documents:** PDFs, Word docs, emails, HTML, database exports.
2. **Chunk documents:** Split into smaller segments (typically 256–1024 tokens).
   - Fixed-size: simple, consistent, may split mid-sentence
   - Sentence/paragraph: preserves semantic units
   - Recursive character: smart splitting preserving structure
3. **Embed chunks:** Generate embedding vector for each chunk.
4. **Store in vector database:** Each record = (id, embedding, text, metadata).

**Phase 2: Retrieval and Generation (online, per query)**

1. **Receive user query.**
2. **Embed query** using same embedding model.
3. **ANN search:** Find top-k most similar chunks in vector database.
4. **Optional reranking:** Use cross-encoder to rerank retrieved chunks.
5. **Build prompt:** Combine query + retrieved chunks as context.
6. **LLM generation:** Model generates answer using context as reference.
7. **Return answer** (optionally with source citations).

### 9.4 Chunking Strategies

**Chunk size considerations:**
- Too small: loss of context; fragments may be semantically incomplete
- Too large: retrieves too much irrelevant content; hits context limits
- Rule of thumb: 512–1024 tokens for most use cases

**Chunk overlap:**
Add 10–20% overlap between adjacent chunks to avoid context split at boundaries.

**Semantic chunking:**
Split at semantic boundaries (paragraph, section) detected by embedding similarity.
Computationally heavier but higher quality.

**Hierarchical chunking:**
Store both document-level and chunk-level embeddings.
Use document-level for broad recall, chunk-level for precise extraction.

### 9.5 Retrieval Quality Improvements

**Hybrid search:** Combine vector search (semantic) + BM25 (keyword).
Use Reciprocal Rank Fusion (RRF) to merge ranked lists.
Improves recall for specific terms that embeddings might miss.

**HyDE (Hypothetical Document Embedding):**
For ambiguous queries: LLM generates a hypothetical document answering the query.
Embed that document and search. Often improves retrieval quality.

**Query expansion:**
Generate multiple phrasings of the query, search with each, merge results.

**Cross-encoder reranking:**
After ANN retrieval, use a cross-encoder model (more accurate but slower)
to rerank top-k candidates. Typical pattern: retrieve 50, rerank to 5.

### 9.6 Evaluation Metrics

**Retrieval metrics:**
- Recall@k: fraction of relevant docs in top-k
- Precision@k: fraction of retrieved docs that are relevant
- MRR (Mean Reciprocal Rank): average of 1/rank of first relevant doc
- NDCG@k: normalized discounted cumulative gain (ranking quality)

**End-to-end RAG metrics (RAGAS framework):**
- **Faithfulness:** Does the generated answer actually follow from the context?
- **Answer relevancy:** Is the answer relevant to the question?
- **Context precision:** Are the retrieved chunks relevant?
- **Context recall:** Are all relevant facts in the retrieved chunks?

### 9.7 RAG for Supply Chain Applications

**Logistics knowledge assistant:**
Index: carrier contracts, rate cards, SOPs, exception policies, historical data.
Use case: "What is our surcharge policy for fuel over $4/gal on LTL lanes?"
Without RAG: LLM would hallucinate your company's policy.
With RAG: retrieves the relevant contract clause and cites the source.

**Procurement negotiation support:**
Index: past contracts, market benchmarks, supplier performance data.
Use case: "What concessions did we win from Supplier X last renewal?"

**Incident response:**
Index: incident logs, root cause analyses, corrective actions.
Use case: "What was the resolution for the similar carrier failure in 2024?"

**Customer service:**
Index: product catalog, order history, shipping policies.
Use case: automated response to customer inquiries grounded in real data.

---

## 10. VECTOR SEARCH IN SUPPLY CHAIN APPLICATIONS

### 10.1 SKU Similarity Search

Embed product descriptions and attributes. Use vector search to find similar SKUs.
Applications:
- Substitute product recommendations when a SKU is out of stock
- Consolidation analysis: are these two SKUs redundant?
- Demand transfer modeling: if SKU A runs out, how much demand shifts to B?

### 10.2 Customer Behavior Embeddings

Embed customer purchase patterns (sequence embeddings from Transformer models).
Applications:
- Customer segmentation without manual feature engineering
- Churn prediction: find customers similar to past churners
- Upsell/cross-sell: find customers similar to those who bought product X

### 10.3 Supplier Risk Profiling

Embed supplier characteristics: industry, geography, financial health indicators.
Applications:
- Find suppliers with similar risk profiles
- When qualifying new suppliers, find analogous historical suppliers

### 10.4 Document Search at Scale

For large organizations with millions of documents:
- Contracts, purchase orders, invoices
- Vector search finds semantically relevant documents faster than keyword search
- Powers internal knowledge management and compliance search

---

## 11. PYTHON CODE EXAMPLES

### 11.1 Simple Vector Store with FAISS

```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SimpleVectorStore:
    """Minimal vector store using FAISS + sentence-transformers."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.d = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.d)  # Inner Product (cosine for normalized)
        self.documents = []
    
    def add(self, texts):
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        self.index.add(embeddings.astype(np.float32))
        self.documents.extend(texts)
    
    def search(self, query, k=5):
        q_embedding = self.model.encode([query], normalize_embeddings=True)
        scores, indices = self.index.search(q_embedding.astype(np.float32), k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append({"text": self.documents[idx], "score": float(score)})
        return results

# Usage
store = SimpleVectorStore()
store.add([
    "Freight rates rose 15% due to Pacific lane congestion",
    "Driver shortage is impacting truckload capacity",
    "Fuel surcharge index reached 28% this week",
    "Rail intermodal capacity is improving in Q4",
    "Customer service level targets: 98% OTIF"
])

results = store.search("What is affecting carrier capacity?")
for r in results:
    print(f"  [{r['score']:.3f}] {r['text']}")
```

### 11.2 PCA on Demand Vectors

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Synthetic: 500 SKUs, each with 52 weeks of demand
np.random.seed(42)
n_skus, n_weeks = 500, 52
demand_matrix = np.random.poisson(100, (n_skus, n_weeks)).astype(float)

# Add seasonal patterns
seasonal = 20 * np.sin(2 * np.pi * np.arange(n_weeks) / 52)
demand_matrix += seasonal

# PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(demand_matrix)
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_scaled)

# Explained variance
cumvar = np.cumsum(pca.explained_variance_ratio_)
print("Cumulative explained variance:")
for i, cv in enumerate(cumvar):
    print(f"  PC{i+1}: {cv:.3f}")

# Visualize in 2D
plt.figure(figsize=(8,6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5, s=20)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("SKU Demand Patterns in PCA Space")
plt.show()
```

### 11.3 Cosine Similarity Heatmap

```python
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

docs = [
    "Supply chain disruption at Port of Los Angeles",
    "West coast port congestion impacting imports",
    "Q4 inventory buildup strategy",
    "Holiday season demand planning",
    "Carrier contract renewal negotiations",
    "Freight rate market outlook"
]

embeddings = model.encode(docs, normalize_embeddings=True)
sim_matrix = embeddings @ embeddings.T

fig, ax = plt.subplots(figsize=(8,7))
im = ax.imshow(sim_matrix, cmap='RdYlGn', vmin=0, vmax=1)
ax.set_xticks(range(len(docs)))
ax.set_yticks(range(len(docs)))
short_labels = [d[:30] + "..." for d in docs]
ax.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=8)
ax.set_yticklabels(short_labels, fontsize=8)
plt.colorbar(im)
plt.title("Document Cosine Similarity Matrix")
plt.tight_layout()
plt.show()
```

---

## 12. QUICK REFERENCE

### Distance / Similarity Cheat Sheet

| Metric           | Formula                            | Range      | Notes                        |
|------------------|------------------------------------|------------|------------------------------|
| Cosine similarity| u·v / (||u||·||v||)                | [-1, 1]    | Angle-based, scale-invariant |
| Dot product      | u·v = Σuᵢvᵢ                        | (-∞, +∞)   | = cosine if L2-normalized    |
| Euclidean dist   | √(Σ(uᵢ-vᵢ)²)                       | [0, +∞)    | Sensitive to magnitude       |
| Manhattan dist   | Σ|uᵢ-vᵢ|                           | [0, +∞)    | Robust to outliers           |
| Hamming dist     | Σ(uᵢ ≠ vᵢ)                         | [0, d]     | Binary vectors               |

### Vector Database Comparison

| Database    | Type           | Index       | Hosted? | Language   |
|-------------|----------------|-------------|---------|------------|
| Pinecone    | Dedicated      | HNSW        | Cloud   | Python/REST|
| Qdrant      | Dedicated      | HNSW        | Both    | Python/Rust|
| Weaviate    | Dedicated      | HNSW        | Both    | Python     |
| Chroma      | Dedicated      | HNSW        | Both    | Python     |
| Milvus      | Dedicated      | HNSW/IVF    | Both    | Python     |
| pgvector    | Extension      | HNSW/IVFFlat| Self    | PostgreSQL |
| FAISS       | Library        | Many        | Self    | Python/C++ |

### HNSW Parameter Guide

| Parameter        | Meaning                    | Increase if...                    |
|------------------|----------------------------|-----------------------------------|
| M                | Edges per vector           | Recall too low, memory available  |
| ef_construction  | Build-time search width    | Build recall quality is poor      |
| ef_search        | Query-time search width    | Recall too low in production      |

### RAG Architecture Decision Points

| Decision               | Options                        | Trade-offs                       |
|------------------------|--------------------------------|----------------------------------|
| Chunk size             | 256 / 512 / 1024 tokens        | Precision vs. context            |
| Embedding model        | MiniLM / mpnet / OpenAI        | Speed vs. quality vs. cost       |
| k (top-k retrieved)    | 3 / 5 / 10 / 20                | Context window vs. coverage      |
| Search type            | Semantic / Keyword / Hybrid    | Recall vs. precision             |
| Reranking              | None / cross-encoder           | Latency vs. quality              |

### Python Libraries for Vector Work

| Library                  | Purpose                                     |
|--------------------------|---------------------------------------------|
| faiss                    | Fast ANN search library (Facebook)          |
| sentence_transformers    | Embed text with transformer models          |
| openai (embeddings API)  | OpenAI embedding API                        |
| chromadb                 | Simple embedded vector store (local dev)    |
| qdrant-client            | Qdrant vector database client               |
| sklearn.decomposition    | PCA, TruncatedSVD, NMF                      |
| sklearn.manifold         | t-SNE, UMAP (via umap-learn)                |
| numpy.linalg             | SVD, matrix operations                      |
| scipy.spatial.distance   | cdist, cosine, euclidean, etc.              |

---
*End of VECTOR_ANALYSIS_KB.md*
*Sources: Pinecone HNSW guide, Wikipedia (HNSW, RAG), IBM Think (RAG, Gradient Descent),*
*AWS (RAG), Medium (@wtaisen HNSW), FAISS documentation, sentence-transformers docs,*
*Malkov & Yashunin (2018) HNSW paper (arXiv:1603.09320)*
