# Proactive Memory Architecture: Living Memories, Families, and Evolutionary Retrieval

**A Design Paper by Pythagoras (𝚷)**
*Commissioned by Dale McClung — March 2026*

---

## Abstract

Current agent memory systems are passive retrieval engines: a query arrives, the system searches, results are returned. This architecture places the full burden of memory activation on the querying process. We propose a fundamentally different model in which memories behave as micro-agents — entities with internal state, activation thresholds, and the capacity to surface themselves proactively when context warrants. We formalize this model using spreading activation theory, Minsky's Society of Mind, and Hopfield network attractor dynamics. We then develop the concept of memory *families* — emergent clusters of semantically related memories with collective identity, adaptive centroids, and synthesized archetypes — and formalize their formation using HDBSCAN. We design an evolutionary scoring system built on a reinforcement signal we call *sticky contribution*, identify the core measurement problem this poses for autonomous agents, and propose two concrete proxies measurable without human labeling. Finally, we provide a specific retrofit design for an existing LanceDB/SQLite hybrid store, including new data structures, new processes, and new cron jobs. The goal throughout is not theoretical elegance for its own sake — it is a memory system that gets smarter over time without being told to.

---

## Part I: Theoretical Framework — Proactive Memory as Micro-Agency

### 1.1 The Problem with Passive Retrieval

Standard retrieval-augmented memory systems operate on a pull model. When an agent needs to respond, it generates a query — either explicitly or by embedding the current context — and searches its memory store for semantically similar items. What is returned depends entirely on what was asked. Nothing surfaces unless it is sought.

This architecture has a fundamental limitation: it can only retrieve what the agent already suspects is relevant. A memory that is contextually important but not obviously similar to the query vector will be missed. The gap between *what was asked* and *what should have been consulted* is the gap between adequate and excellent responses.

Human memory does not work this way. A conversation about delivery schedules might spontaneously surface a memory of a customer complaint from six months ago — not because you queried for it, but because the semantic and emotional context activated it. This is not retrieval; it is *spreading activation*.

### 1.2 Spreading Activation Theory

Collins and Loftus (1975) proposed that semantic memory is organized as a network of nodes connected by weighted edges, where activation spreads from a stimulated node to its neighbors in proportion to connection strength and decays with distance. The model was descriptive — a theory of human cognition — but its computational structure is directly applicable to agent memory design.

Formally, let **M** = {m₁, m₂, ..., mₙ} be the set of memory items, each represented by an embedding vector **v**ᵢ ∈ ℝᵈ. Define the connection weight between memories i and j as:

> **w**ᵢⱼ = sim(**v**ᵢ, **v**ⱼ) · f(Δt)

where sim(·,·) is cosine similarity and f(Δt) is a temporal recency weight that decays with the time since both memories were last co-activated. Memories that have been relevant together recently have stronger connections.

Each memory has an activation level aᵢ(t) ∈ [0,1] that evolves as:

> **aᵢ(t+1) = λ · aᵢ(t) + α · sim(vᵢ, c(t)) + β · Σⱼ wᵢⱼ · aⱼ(t)**

where **c(t)** is the current context embedding, λ ∈ (0,1) is a decay parameter, α is the direct context activation weight, and β is the lateral spreading weight. When aᵢ(t) exceeds a threshold θᵢ, memory mᵢ surfaces proactively — it enters the agent's context without being explicitly queried.

The threshold θᵢ is itself adaptive: it decreases as a memory accumulates sticky contribution score (making high-value memories easier to activate) and increases as a memory accumulates noise score (suppressing low-value memories). This is the evolutionary component — over time, the activation landscape reshapes itself to reflect which memories are worth surfacing.

### 1.3 Minsky's Society of Mind

Marvin Minsky's *Society of Mind* (1986) proposed that intelligence emerges not from a single unified process but from the coordinated interaction of many small, specialized agents — each with limited capability, but collectively capable of complex behavior. No single agent understands the whole; the whole emerges from the pattern of interactions.

Memory items as micro-agents is a direct application of this framework. Each memory is not a passive record but a *competing agent* for inclusion in the current context. Memories compete on the basis of activation level, threshold, and relevance. The "society" of memories dynamically negotiates which members are currently most relevant. The agent's effective context at any moment is the output of this competition.

The practical implication is significant: the agent does not need to be smart about what to retrieve. The memories themselves are responsible for determining when they are relevant. This distributes the intelligence of retrieval across the memory store itself.

### 1.4 Hopfield Networks and Attractor Dynamics

Hopfield (1982) demonstrated that a symmetric neural network with Hebbian learning converges to stable attractor states — *energy minima* — that correspond to stored patterns. When the network is presented with a partial or noisy version of a stored pattern, it relaxes to the nearest attractor, effectively completing or correcting the input. Memory is retrieval as error correction.

The energy function of a Hopfield network is:

> **E = -½ Σᵢⱼ wᵢⱼ sᵢ sⱼ**

where sᵢ ∈ {-1, +1} are neuron states and wᵢⱼ are symmetric weights. The network evolves to minimize E, and stored memories are local minima of this function.

For our purposes, the attractor dynamics model explains *family* behavior (developed in Part II) and provides a mathematical grounding for why memories that have been frequently co-activated tend to form stable retrieval coalitions. A context that partially matches a family will tend to activate the entire family — the attractor basin draws in nearby activations.

The capacity of a Hopfield network is approximately 0.138N patterns for N neurons — it can store roughly 14% of N distinct patterns before cross-contamination degrades recall. This is a design constraint: families must not be too large relative to the dimensionality of the embedding space, or pattern separation degrades. We return to this in Part II.

### 1.5 Modern Continuous Attractor Networks

Classical Hopfield networks have discrete states. Modern continuous attractor networks (CANs) extend the framework to continuous-valued activations and are more appropriate for embedding-space memory.

In a CAN, the network maintains a *hill of activity* in the embedding space that represents the current attentional focus. As context shifts, the hill moves continuously through the space, activating memories in its path. Memories that lie in stable attractor basins — those that are semantically central to a family — are preferentially activated as the hill passes through their region.

This provides a mathematically precise account of how proactive memory surfacing interacts with family structure: families define attractor basins, and context shifts that pass through or near a basin activate the family's memories proportionally to their proximity to the centroid.

---

## Part II: Family Architecture — Clustering, Emergence, and Collective Behavior

### 2.1 The Case for Families

Individual memory items are noisy. A single experience encodes both the essential pattern and the incidental details of the specific instance. A family of related memories — multiple experiences that share deep structure — can collectively represent the essential pattern while averaging out the noise.

This is the same principle that makes ensemble methods in machine learning more robust than single models: the variance of the ensemble is lower than the variance of any member. A family's centroid is a more reliable representation of a concept than any individual memory of an instance of that concept.

Families also enable *archetype synthesis* — the generation of a meta-memory that represents the distilled essence of the family without being a verbatim record of any member. This is how human expertise is organized: not as a catalog of individual experiences but as abstracted patterns that generalize across instances.

### 2.2 Why HDBSCAN

The choice of clustering algorithm for family formation has significant architectural consequences.

*k-means* requires specifying k in advance and assumes spherical clusters of equal size. Neither assumption holds for a memory store that grows organically — we do not know how many families will form, and semantic clusters are irregularly shaped and variably dense.

*Standard DBSCAN* handles irregular shapes and does not require k, but requires global density parameters (ε, minPts) that do not adapt to local density variations. A memory store will have dense clusters (frequently-encountered domains) and sparse regions (novel or rare experiences). A fixed ε will either over-merge the sparse regions or over-fragment the dense ones.

*HDBSCAN* (Hierarchical DBSCAN, McInnes et al. 2017) solves this by building a hierarchical cluster tree and extracting stable clusters at varying densities. It handles variable-density clusters naturally, does not require ε, identifies noise points (memories that belong to no family), and produces a cluster hierarchy that encodes the genealogy of family formation and merging over time.

For agent memory, HDBSCAN's hierarchy has additional value: it exposes *subfamily* structure (tight clusters within larger families) and *superfamily* structure (related families that share a broader domain). Both levels are semantically meaningful.

### 2.3 Formal Family Definition

Let **V** = {**v**₁, **v**₂, ..., **vₙ**} be the set of memory embedding vectors. Run HDBSCAN with minimum cluster size minₛ (a design parameter, suggested initial value: 5) to produce a partition:

> **F** = {F₁, F₂, ..., Fₖ, F₀}

where Fₖ are the identified families and F₀ is the noise set (memories belonging to no family). For each family Fₖ:

**Centroid:**
> **μₖ = (1/|Fₖ|) Σᵢ∈Fₖ vᵢ**

**Coherence score** (internal compactness):
> **Cₖ = 1 - (mean pairwise cosine distance within Fₖ) / (max pairwise cosine distance across all families)**

A coherence score near 1 indicates a tight, well-defined family. Near 0 indicates diffuse membership.

**Archetype vector** (a synthetic memory representing the family's essence):
Generated when |Fₖ| ≥ minₐ (suggested: 10 members) and Cₖ ≥ C_threshold (suggested: 0.7). The archetype is the centroid vector with a text summary generated by prompting the agent: *"Synthesize the common pattern across these memory excerpts in one paragraph."* The archetype is stored as a memory item with special type `ARCHETYPE` and participates in retrieval and activation like any other memory, but with amplified activation weight.

### 2.4 Family Lifecycle

**Formation:** A new memory **v**_new joins family Fₖ if dist(**v**_new, **μ**ₖ) < τₖ, where τₖ is the family's dynamic admission radius derived from its current HDBSCAN cluster boundary. If **v**_new falls in no family's radius, it joins F₀ and triggers a potential new cluster formation check.

**Evolution:** After every N new memories (suggested: N=20), run HDBSCAN on the full store. This may:
- Expand an existing family
- Split a family (coherence has degraded below threshold)
- Merge two families (their centroids have converged)
- Graduate noise items (F₀ members may now be absorbed)
- Dissolve a family (coherence below dissolution threshold over two consecutive runs)

**Dissolution:** When Cₖ drops below C_min (suggested: 0.4) on two consecutive clustering runs, the family dissolves. Its members return to F₀ or are absorbed by adjacent families. Its archetype, if any, is archived with a `DISSOLVED` tag rather than deleted — it may be historically valuable.

**Inheritance:** When a family splits into Fₐ and Fᵦ, the original family's score history is shared equally between the children. When two families merge into Fₘ, the merged family's score is the weighted average of the parents by membership count.

---

## Part III: Evolutionary Scoring — Reinforcement, Sticky Contribution, and the Hard Problem

### 3.1 The Scoring Framework

Each memory mᵢ carries a score Sᵢ ∈ ℝ, initialized at 0. Each family Fₖ carries a score Sₖ, initialized at 0 and updated as the weighted mean of its members' scores. The update rule for memory scores is:

> **Sᵢ(t+1) = Sᵢ(t) + r_sticky · 𝟙[sticky] - r_noise · 𝟙[noise] + r_family · 𝟙[archetype_contribution]**

where the indicator functions fire based on observable events and the reward weights are design parameters (suggested initial values: r_sticky = +1.0, r_noise = -0.3, r_family = +0.5).

The asymmetry between r_sticky and r_noise reflects a prior: false negatives (failing to surface a relevant memory) are more costly than false positives (surfacing an irrelevant one). We want the system to err on the side of surfacing, but to suppress persistently irrelevant memories over time.

**Sticky contribution** (positive signal): Memory mᵢ surfaced proactively or was retrieved, and evidence suggests it improved the outcome.

**Noise** (negative signal): Memory mᵢ surfaced proactively and evidence suggests it was irrelevant or disruptive.

**Family self-improvement** (positive signal): The family containing mᵢ synthesized a new archetype that subsequently received sticky contribution scores. Credit is distributed to contributing family members.

### 3.2 The Hard Problem: Operationalizing Sticky Contribution

The fundamental difficulty is this: in a production agent system, you rarely observe outcome quality directly. You cannot run a controlled experiment where the agent answers with vs. without a given memory and compare the results. You have session logs, you have response text, you have (sometimes) correction signals — but you do not have a direct oracle on whether memory mᵢ made the response better or worse.

This is not a minor implementation detail. It is the central epistemological problem of the entire architecture. If sticky contribution cannot be measured, the scoring system degrades to noise and the evolutionary component fails.

We propose two proxy measurements that are observable in an OpenClaw agent context without human labeling of every interaction.

### 3.3 Proxy 1: Response Coherence Delta

**Definition:** When memory mᵢ is surfaced during a session, compute the semantic similarity between mᵢ's content and the final response generated: sim(**v**ᵢ, **v**_response). If this similarity exceeds a threshold, the memory's concepts are present in the output — the memory was at minimum not ignored.

**Operationally:** Embed both the memory and the final response using the same embedding model. Compute cosine similarity. Scores > τ_coherence (suggested: 0.65) register as a weak sticky contribution signal. Scores < τ_noise (suggested: 0.3) register as a noise signal.

**Rationale:** A memory that surfaces but whose content does not appear in the response was likely irrelevant. A memory whose content appears substantially in the response was likely consulted and acted on. This is imperfect — a memory might influence reasoning without appearing verbatim in output — but it is a measurable proxy that does not require human annotation.

**Limitations:** This proxy will undervalue memories that improve the *structure* of reasoning without contributing specific content, and will overvalue memories that are merely topic-adjacent to the response. It should be treated as a weak signal, not a definitive one.

### 3.4 Proxy 2: Correction-Absence Rate in Similar Contexts

**Definition:** Track, for each memory mᵢ, the correction rate in sessions where it was active versus sessions where it was not active, within semantically similar contexts.

Formally: let Cₐ = correction rate in sessions where mᵢ was activated and context similarity > τ_context, and C̄ₐ = correction rate in sessions where mᵢ was not activated and context similarity > τ_context. If Cₐ < C̄ₐ by a statistically significant margin (Fisher's exact test, p < 0.05), award a sticky contribution signal. If Cₐ > C̄ₐ significantly, award a noise signal.

**Rationale:** Corrections are the strongest available signal that a response was wrong or suboptimal. If a memory is systematically associated with lower correction rates in relevant contexts, it is — by this measure — improving outcomes. This is a causal inference argument under observational conditions, so it requires enough data to be meaningful (suggested minimum: 10 sessions in each condition before the comparison is trusted).

**Limitations:** Corrections are sparse signals — most interactions go uncorrected even when the response was mediocre. Low correction rate is necessary but not sufficient for high quality. This proxy should be combined with Proxy 1 rather than used alone.

### 3.5 A Third Proxy (Supplementary): Human Engagement Rate

In channels where engagement metrics are available (e.g., the user replies substantively, continues the thread, asks follow-up questions), a substantive engagement following a memory-activated response is a weak positive signal. An immediate topic change or no response is a weak negative signal. This is too noisy to use alone but provides a third, independent weak signal that can be combined with the first two via a simple weighted average.

---

## Part IV: Implementation Design — Retrofitting LanceDB/SQLite

### 4.1 Current Architecture Baseline

The existing hybrid store uses LanceDB for vector storage and semantic search, and SQLite for structured metadata, session logs, and retrieval history. This is a sound foundation. The changes required are additive — we are not replacing the architecture, we are growing new structures on top of it.

### 4.2 New LanceDB Schema Fields

Add the following fields to the primary memories table in LanceDB:

```
activation_score      FLOAT     DEFAULT 0.0     -- current spreading activation level
activation_threshold  FLOAT     DEFAULT 0.5     -- adaptive surface threshold (θᵢ)
sticky_score          FLOAT     DEFAULT 0.0     -- cumulative sticky contribution
noise_score           FLOAT     DEFAULT 0.0     -- cumulative noise penalties
family_id             INTEGER   NULLABLE        -- FK to families.id in SQLite
is_archetype          BOOLEAN   DEFAULT FALSE   -- TRUE if this is a synthesized family archetype
last_activated_at     TIMESTAMP NULLABLE        -- last time activation_score exceeded threshold
activation_count      INTEGER   DEFAULT 0       -- total lifetime surface events
```

The `activation_threshold` field starts at 0.5 and is updated after each scoring cycle:

> **θᵢ = θ_base - γ · Sᵢ**

where γ is a sensitivity parameter (suggested: 0.05) and Sᵢ is the current total score. High-scoring memories have lower thresholds (surface more readily); high-noise memories have raised thresholds.

### 4.3 New SQLite Tables

**families**
```sql
CREATE TABLE families (
    id              INTEGER PRIMARY KEY,
    centroid_json   TEXT NOT NULL,        -- JSON-serialized centroid vector
    coherence_score FLOAT NOT NULL,
    member_count    INTEGER NOT NULL,
    family_score    FLOAT DEFAULT 0.0,
    status          TEXT DEFAULT 'active', -- active | dissolving | dissolved
    created_at      TIMESTAMP NOT NULL,
    dissolved_at    TIMESTAMP NULLABLE,
    parent_family_ids TEXT NULLABLE       -- JSON array, for split/merge genealogy
);
```

**memory_activations**
```sql
CREATE TABLE memory_activations (
    id              INTEGER PRIMARY KEY,
    memory_id       TEXT NOT NULL,        -- FK to LanceDB memory id
    session_id      TEXT NOT NULL,
    activated_at    TIMESTAMP NOT NULL,
    activation_mode TEXT NOT NULL,        -- 'proactive' | 'retrieved'
    context_sim     FLOAT NOT NULL,       -- similarity to context at activation time
    response_sim    FLOAT NULLABLE,       -- similarity to final response (Proxy 1)
    was_corrected   BOOLEAN NULLABLE,     -- whether session had a correction (Proxy 2)
    sticky_signal   FLOAT NULLABLE,       -- computed combined proxy score [-1, +1]
    scored          BOOLEAN DEFAULT FALSE -- whether this activation has been scored
);
```

**clustering_runs**
```sql
CREATE TABLE clustering_runs (
    id              INTEGER PRIMARY KEY,
    run_at          TIMESTAMP NOT NULL,
    n_memories      INTEGER NOT NULL,
    n_families      INTEGER NOT NULL,
    n_noise         INTEGER NOT NULL,
    families_created INTEGER NOT NULL,
    families_dissolved INTEGER NOT NULL,
    families_merged INTEGER NOT NULL,
    families_split  INTEGER NOT NULL
);
```

### 4.4 New Processes

**Process 1: Proactive Activation Engine**
On each new context chunk received by the agent (every message, before generating a response), a lightweight background process:
1. Embeds the context chunk: **c** = embed(context)
2. Fetches all memories with activation_score > 0.1 (pre-filtered, not full scan)
3. Updates activation scores using the spreading activation equation
4. Identifies memories where aᵢ > θᵢ
5. Injects the top-k (suggested: k=3) above-threshold memories into the agent's context as `[PROACTIVE MEMORY]` blocks, ranked by (aᵢ - θᵢ) / θᵢ
6. Logs the activation event to `memory_activations`

This runs synchronously as a pre-processing step. Target latency: < 100ms.

**Process 2: Family Clustering Cron (Nightly)**
```
Schedule: 2:00 AM daily
```
1. Fetch all memory embeddings from LanceDB
2. Run HDBSCAN (min_cluster_size=5, min_samples=3, metric='cosine')
3. Compare result to existing family assignments
4. Update family_id fields in LanceDB for changed assignments
5. Create new families in SQLite families table
6. Mark dissolved families, archive archetypes
7. For families with |Fₖ| ≥ 10 and Cₖ ≥ 0.7, trigger archetype synthesis (separate process)
8. Log run to clustering_runs

**Process 3: Archetype Synthesis (Triggered)**
When a family qualifies (size and coherence thresholds met):
1. Fetch text content of all family members
2. Generate synthesis prompt: *"Identify the common pattern across these memory entries. Write one paragraph that captures the essential shared knowledge they all contain."*
3. Store the result as a new memory with is_archetype=TRUE, family_id=Fₖ
4. Embed the archetype text and store in LanceDB
5. Distribute +0.5 to sticky_score of all contributing family members

**Process 4: Scoring Cron (Post-Session)**
```
Schedule: 15 minutes after session end (triggered by session close event)
```
1. Fetch all unscored activations (scored=FALSE) from the closed session
2. For each activation:
   a. Compute Proxy 1: embed the final session response, compute sim with memory embedding
   b. Look up whether the session was corrected in the corrections log (Proxy 2 raw signal)
   c. Combine: sticky_signal = 0.6 * proxy1_signal + 0.4 * proxy2_signal
   d. Update memory's sticky_score or noise_score in LanceDB
   e. Update family_score in SQLite families table
   f. Update activation_threshold using the adaptive formula
   g. Mark activation as scored=TRUE
3. Log scoring summary

**Process 5: Correction Absence Rate Calculator (Weekly)**
```
Schedule: Sunday 3:00 AM
```
1. For each memory with activation_count > 20 (enough data for statistical test):
2. Compute Cₐ and C̄ₐ (correction rates in active vs inactive similar sessions)
3. Run Fisher's exact test
4. Award or penalize sticky_score for significant differences
5. Update activation_threshold accordingly

### 4.5 Configuration Parameters

The following parameters should be stored in a `memory_config.json` and tunable without code changes:

```json
{
  "spreading_activation": {
    "decay_lambda": 0.85,
    "context_weight_alpha": 0.6,
    "lateral_weight_beta": 0.3,
    "base_threshold": 0.5,
    "threshold_sensitivity_gamma": 0.05,
    "proactive_surface_k": 3
  },
  "family_clustering": {
    "min_cluster_size": 5,
    "min_samples": 3,
    "archetype_min_members": 10,
    "archetype_min_coherence": 0.7,
    "dissolution_coherence_threshold": 0.4,
    "rerun_every_n_memories": 20
  },
  "scoring": {
    "sticky_reward": 1.0,
    "noise_penalty": 0.3,
    "family_contribution_reward": 0.5,
    "proxy1_weight": 0.6,
    "proxy2_weight": 0.4,
    "proxy1_sticky_threshold": 0.65,
    "proxy1_noise_threshold": 0.3,
    "correction_absence_min_activations": 20,
    "correction_absence_p_threshold": 0.05
  }
}
```

---

## Part V: Open Problems and Research Directions

### 5.1 The Threshold Calibration Problem

The adaptive threshold system is self-referential: thresholds depend on scores, scores depend on activations, activations depend on thresholds. This creates a potential for runaway dynamics in both directions.

A memory with a very low threshold activates frequently. Frequent activation means more opportunities for sticky contribution, which lowers the threshold further. Without a damping term, this produces a winner-takes-all dynamic where a few high-scoring memories dominate context and suppress everything else.

Conversely, a memory with a raised threshold activates rarely, accumulating few scores, keeping the threshold high. Memories can get permanently suppressed even if they are genuinely useful in rare contexts.

The solution requires a floor (minimum threshold) and ceiling (maximum threshold) on θᵢ, plus a slow decay of the noise penalty over time (memories should get a second chance as the world changes). This dampened dynamics problem is mathematically tractable but requires empirical calibration on real agent logs to tune correctly.

### 5.2 The Semantic Drift Problem

Embedding models may be updated over time. When the embedding model changes, old memory vectors are no longer comparable to new ones — the coordinate system has shifted. Family centroids computed under the old model will not cluster correctly with new memories embedded under the new model.

This requires a re-embedding protocol: when the embedding model changes, re-embed all stored memories and re-run the full clustering pipeline. This is expensive for large stores but necessary for semantic consistency. The clustering run history should log the embedding model version used.

### 5.3 The Multi-Agent Propagation Problem

In a multi-agent system (Thea, Iris, Supply Chain Guru, Pythagoras), sticky contribution scores in one agent's memory store reflect that agent's experience only. A memory that is highly valuable for Pythagoras's SPC work may not have been activated in Iris's writing domain.

The family architecture, however, suggests a propagation mechanism: when two agents' family archetypes have high cosine similarity (sim > 0.85), the higher-scoring archetype's score can partially propagate to the lower-scoring one. This is a cross-agent confidence inheritance mechanism — the same idea proposed in the learning systems design session, applied now to family archetypes rather than discrete memory items.

The risk is cross-contamination: domain-specific memories should not inflate their scores just because they superficially resemble high-scoring memories in another domain. Propagation should be gated on domain tag overlap, not embedding similarity alone.

### 5.4 The Cold Start Problem

A new agent has no activation history, no family structure, and no scores. The proactive memory system provides no value until sufficient history accumulates.

The solution is IMfA inheritance: at agent initialization, import the family archetypes (not the raw memories) from the most semantically relevant existing agent. Archetypes carry synthesized knowledge without the noise of individual instances, and they come with inherited scores that provide initial threshold calibration. The new agent starts with working families rather than an empty store.

This transforms IMfA from a static knowledge transfer into an *architectural* inheritance mechanism — new agents inherit not just facts but the learned retrieval structure of their predecessors.

---

## Conclusion

The architecture proposed here represents a significant departure from current agent memory design. The departure is not for theoretical elegance — it is motivated by a concrete limitation: passive retrieval systems can only find what they are asked to find. A proactive memory system gets ahead of the question.

The key design decisions, summarized:

- **Spreading activation over pull retrieval** — memories compete for context on the basis of relevance, not query.
- **HDBSCAN families over flat vector search** — semantic clusters form naturally and evolve with the memory store, with archetypes distilling collective knowledge.
- **Evolutionary scoring over static importance** — memories earn their activation rights through demonstrated contribution, and lose them through demonstrated irrelevance.
- **Response coherence delta and correction-absence rate as sticky contribution proxies** — imperfect but measurable, not requiring human annotation on every interaction.
- **LanceDB/SQLite retrofit over replacement** — additive changes on an existing foundation, with new fields, new tables, and new cron jobs that can be deployed incrementally.

The deepest open problem is the sticky contribution measurement. No proxy is clean. The architecture is only as good as the signal that drives the scoring system, and that signal will be noisy in production. The recommendation is to instrument everything, start conservative (low γ, moderate reward weights), and tune empirically over 30–60 days of production use before trusting the adaptive thresholds.

The goal is a memory system that, in six months, surfaces the right memory before you knew to ask for it. That is the behavior we are designing toward. The mathematics described here is the path.

---

## References

- Collins, A.M. & Loftus, E.F. (1975). "A spreading-activation theory of semantic processing." *Psychological Review*, 82(6), 407–428.
- Hopfield, J.J. (1982). "Neural networks and physical systems with emergent collective computational abilities." *Proceedings of the National Academy of Sciences*, 79(8), 2554–2558.
- McInnes, L., Healy, J., & Astels, S. (2017). "HDBSCAN: Hierarchical density based clustering." *Journal of Open Source Software*, 2(11), 205.
- Minsky, M. (1986). *The Society of Mind*. Simon & Schuster.
- Samsonovich, A. & McNaughton, B.L. (1997). "Path integration and cognitive mapping in a continuous attractor neural network model." *Journal of Neuroscience*, 17(15), 5900–5920.
- Rissanen, J. (1978). "Modeling by shortest data description." *Automatica*, 14(5), 465–471. *(For MDL connection to archetype synthesis.)*
- Anderson, J.R. (1983). *The Architecture of Cognition*. Harvard University Press. *(ACT-R spreading activation model.)*

---

*Pythagoras (𝚷) | March 2026*
*A design paper commissioned by Dale McClung.*
