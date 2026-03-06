# SIMULATION_KB.md
# Knowledge Base: Simulation Methods for Operations and Risk Analysis
# For use by Pythagoras AI — Quantix Supply Chain Solutions
# Last updated: 2026-03-04

## Pre-flight Checklist

Before selecting a statistical method or running analysis, answer these 5 questions:

1. **What type of data?** Continuous, ordinal, categorical, binary, count data?
2. **What is the sample size?** n < 30 triggers non-parametric or Bayesian considerations
3. **What distributional assumptions apply?** Normality? Independence? Homoscedasticity?
4. **What decision follows from this analysis?** If unclear, clarify scope before proceeding
5. **What is the acceptable error rate?** Alpha level, confidence interval width, Type I vs Type II tradeoff?

> Choosing the wrong method because assumptions weren't checked is correctable — but expensive.

---


---

## TABLE OF CONTENTS

1. Introduction to Simulation
2. Monte Carlo Simulation — Fundamentals
3. Monte Carlo in Supply Chain and Operations
4. Sampling Methods and Variance Reduction
5. Latin Hypercube Sampling
6. Discrete Event Simulation (DES)
7. System Dynamics
8. Risk Quantification and Analysis
9. Simulation Output Analysis
10. Python Implementation
11. Quick Reference

---

## 1. INTRODUCTION TO SIMULATION

Simulation is the process of creating a computational model of a real system
and running experiments on that model to understand system behavior, test
alternatives, or estimate performance metrics under uncertainty.

### 1.1 Why Simulate?

Many real-world problems cannot be solved analytically:
- Too many interacting variables
- Stochastic (random) inputs
- Complex, nonlinear relationships
- System constraints that create feedback loops
- Need to evaluate "what-if" scenarios without real-world experiments

### 1.2 Types of Simulation

| Type                        | Characteristics                         | Use Cases                         |
|-----------------------------|------------------------------------------|------------------------------------|
| Monte Carlo                 | Probabilistic, aggregated outcomes       | Risk analysis, option pricing      |
| Discrete Event Simulation   | Events occur at discrete time points     | Queuing, logistics, manufacturing  |
| System Dynamics             | Continuous differential equations        | Supply chain bullwhip, policy      |
| Agent-Based Modeling        | Individual agents follow rules           | Market dynamics, traffic           |
| Continuous Simulation       | Differential equations, smooth           | Fluid dynamics, chemical processes |

### 1.3 The Simulation Workflow

1. **Problem formulation:** Define objectives, scope, performance measures
2. **Conceptual model:** Document system logic, assumptions, boundaries
3. **Data collection:** Gather input distributions, parameters
4. **Model construction:** Build computational model
5. **Verification:** Confirm model runs as intended (debugging)
6. **Validation:** Confirm model represents reality (compare to known outcomes)
7. **Experimentation:** Design and run scenarios
8. **Analysis:** Interpret outputs, confidence intervals, sensitivity
9. **Documentation and deployment:** Report findings, operationalize

---

## 2. MONTE CARLO SIMULATION — FUNDAMENTALS

### 2.1 History and Overview

Monte Carlo simulation was developed by John von Neumann and Stanislaw Ulam
during World War II to model neutron diffusion in the Manhattan Project.
Named after the Monte Carlo Casino in Monaco (randomness as core element).

**Definition:** A computational algorithm that uses repeated random sampling
to estimate the probability distribution of outcomes for a system with uncertain inputs.

**Core idea:**
- Replace uncertain variables with probability distributions
- Sample from those distributions thousands/millions of times
- Aggregate results to estimate output distribution

Unlike deterministic forecasting (single point estimate), Monte Carlo produces
a probability distribution of outcomes: P(outcome ≤ x) = ?

### 2.2 The Three Steps (IBM Framework)

1. **Set up the model:** Identify dependent variable (outcome) and independent
   variables (inputs/drivers with uncertainty).

2. **Specify input distributions:** For each uncertain input, assign:
   - Distribution type (normal, lognormal, uniform, triangular, etc.)
   - Parameters (mean, std, min, max, mode)
   - Correlations between inputs

3. **Run simulations:** Sample random values for each input, compute outcome.
   Repeat N times (N = 1,000 to 100,000+). Analyze output distribution.

### 2.3 Common Input Distributions

**Normal (Gaussian):** Mean and standard deviation. Symmetric. Good for:
measurement errors, natural variations in processes, aggregated effects.

**Lognormal:** Log of variable is normally distributed. Skewed right.
Good for: prices, costs, time durations (can't be negative). 

**Uniform:** Equal probability across [min, max]. Good for:
true ignorance about distribution shape, bounded parameters.

**Triangular:** Min, most likely (mode), max. Good for:
expert estimates when data is scarce. Simple and interpretable.

**PERT (Beta-PERT):** Smooth version of triangular with heavier weight at mode.
Common in project risk analysis (critical path method).

**Exponential:** Memoryless inter-arrival times. Good for:
time between events (failures, arrivals), service times.

**Poisson:** Count of events in fixed interval. Good for:
demand per day/hour, defect counts, order arrivals.

**Beta:** Flexible bounded distribution on [0,1]. Good for:
proportions, probabilities, completion percentages.

**Weibull:** Models time-to-failure with aging. Good for:
reliability engineering, equipment maintenance intervals.

### 2.4 Random Number Generation

Monte Carlo depends on high-quality pseudo-random number generators (PRNGs):

**Mersenne Twister (MT19937):** Default in Python/NumPy.
Period = 2^19937 − 1. Passes most statistical randomness tests.

**PCG (Permuted Congruential Generator):** NumPy's default since v1.17.
Faster and statistically superior to MT for simulation.

**Quasi-random (Low-discrepancy sequences):** Halton, Sobol, Faure.
More uniform coverage of the sample space than pseudo-random.
Used in financial simulation and numerical integration.

```python
import numpy as np

rng = np.random.default_rng(seed=42)  # modern NumPy PRNG

# Sample from distributions
normal_samples = rng.normal(loc=100, scale=15, size=10000)
lognormal_samples = rng.lognormal(mean=4.6, sigma=0.3, size=10000)
uniform_samples = rng.uniform(low=80, scale=40, size=10000)   # [80, 120]
triangular_samples = rng.triangular(left=80, mode=100, right=140, size=10000)
```

### 2.5 Convergence and Sample Size

Monte Carlo estimates converge at rate O(1/√N):
- 100 samples: ~10% error
- 1,000 samples: ~3% error
- 10,000 samples: ~1% error
- 100,000 samples: ~0.3% error

For tail risk (VaR at 99th percentile), need more samples to estimate tails accurately.
Rule of thumb: need at least 100/p samples for p-quantile estimation.
For 99th percentile VaR: at least 10,000 samples.

### 2.6 Seed Control and Reproducibility

Always set a random seed for reproducibility:
```python
rng = np.random.default_rng(seed=2026)  # reproducible results
```

For parallel simulation, use independent streams via `spawn()`:
```python
seed_sequence = np.random.SeedSequence(2026)
child_seeds = seed_sequence.spawn(4)  # 4 independent RNG streams
```

---

## 3. MONTE CARLO IN SUPPLY CHAIN AND OPERATIONS

### 3.1 Inventory and Safety Stock

**Problem:** Determine safety stock needed to achieve target service level
given uncertain demand and uncertain lead time.

**Classic analytical approach:**
Safety Stock = z × σ_d × √LT  (only valid for normally distributed demand, fixed LT)

**Monte Carlo approach:**
1. Fit demand distribution from historical data (may not be normal)
2. Fit lead time distribution (may be multimodal)
3. Include demand-lead-time correlation if present
4. Simulate 10,000+ demand-during-lead-time realizations
5. Set safety stock = P(stockout) ≤ target
6. Full probability distribution of SS requirements

This handles:
- Non-normal demand (heavy tails, intermittent)
- Variable lead times with non-normal distribution
- Demand-lead-time correlation
- Compound uncertainty

### 3.2 Project Risk and Schedule Analysis

**PERT network + Monte Carlo:**
1. Define work breakdown structure (WBS)
2. Assign PERT distributions to each task duration
3. Identify task dependencies (critical path network)
4. Simulate 10,000 project completions
5. Output: distribution of project completion date, P(complete by date X)

Critical path can shift between simulations — purely analytical CPM misses this.

### 3.3 Transportation and Network Risk

**Lane reliability simulation:**
1. Sample transit time distribution for each lane
2. Sample capacity availability (carrier rejection rates)
3. Simulate order flow through network
4. Output: on-time delivery probability, expected cost distribution

**Port disruption scenario:**
1. Define disruption probability (P = 0.05 per month)
2. Define disruption duration distribution
3. Simulate year of operations 10,000 times
4. Output: annual stockout probability, expected revenue impact

### 3.4 Financial Risk in Supply Chain

**Revenue at Risk:**
Simulate sales volume × price × fulfillment rate → revenue distribution.
Report 5th percentile as "Revenue at Risk" (VaR equivalent).

**Cost at Risk:**
Simulate input costs (fuel, materials, labor) → total cost distribution.
Report 95th percentile as "maximum likely cost."

**NPV Monte Carlo:**
For capital investment decisions:
1. Uncertain inputs: demand growth, capex, opex, discount rate
2. Simulate 10,000 NPV calculations
3. Output: P(NPV > 0), expected NPV, NPV distribution
4. Better than single-point NPV which hides uncertainty

---

## 4. SAMPLING METHODS AND VARIANCE REDUCTION

### 4.1 Why Variance Reduction Matters

Standard Monte Carlo has estimation error proportional to σ/√N.
To halve the error, you must quadruple sample size.
Variance reduction techniques achieve the same accuracy with fewer samples.

### 4.2 Stratified Sampling

Divide the probability distribution into K strata of equal probability.
Sample exactly n/K observations from each stratum.

Ensures coverage of the full distribution without gaps or clustering.
Variance reduction: eliminates between-stratum variance from estimates.

For K strata, stratified sampling reduces variance by factor proportional to:
Var(stratified) ≤ Var(simple MC) − [between-strata variance]

### 4.3 Control Variates

Use a correlated "control" variable with known expected value to reduce error.

Estimator: θ̂_cv = θ̂_mc − c(Ŷ − E[Y])

where Ŷ is the control estimate, E[Y] is its known mean, c is chosen to minimize variance.

Optimal c = -Cov(θ̂, Ŷ) / Var(Ŷ)

Variance reduction factor ≈ 1/(1-ρ²) where ρ is correlation between θ and Y.
High correlation (|ρ| close to 1) gives large variance reduction.

### 4.4 Antithetic Variates

For each random number u ∈ [0,1], also use 1-u (the "antithetic" value).
Run pairs of simulations: one with u, one with 1-u.
Average the pair.

This introduces negative correlation between paired runs:
Var((X + X') / 2) = (Var(X) + Var(X') + 2Cov(X,X')) / 4

If Cov(X, X') < 0 (which antithetic ensures), variance is reduced.

Implementation: simply flip the random uniform: u → 1-u.
Works best for monotone functions of the inputs.

### 4.5 Importance Sampling

Shift the sampling distribution toward important regions (tails).
Useful for rare event simulation (probability < 0.01).

Instead of sampling from f(x), sample from g(x) concentrated near the event.
Correct with likelihood ratio: weight = f(x)/g(x).

Result: same answer, but much lower variance because more samples fall in the
region that matters (the rare event region).

### 4.6 Quasi-Monte Carlo (QMC)

Replace pseudo-random points with low-discrepancy sequences.
These fill the sample space more uniformly than random sampling.

**Sobol sequences:** Each new point fills the largest gap in existing points.
**Halton sequences:** Based on prime number base representations.

Convergence rate for QMC: O(log(N)^d / N) vs O(1/√N) for MC.
QMC is dramatically faster for low-dimensional (d ≤ 10) problems.
For high dimensions (d > 20), advantage diminishes.

```python
from scipy.stats import qmc

# Sobol sequence
sampler = qmc.Sobol(d=5, scramble=True, seed=42)
sample = sampler.random(n=1024)  # must be power of 2 for Sobol

# Scale to input ranges
l_bounds = [0, 100, 50, 0.02, 0.8]
u_bounds = [1, 200, 150, 0.10, 1.2]
scaled = qmc.scale(sample, l_bounds, u_bounds)
```

---

## 5. LATIN HYPERCUBE SAMPLING (LHS)

### 5.1 Concept

Latin Hypercube Sampling (LHS) is a stratified sampling method for multiple
simultaneous input variables. Named after "Latin square" statistical designs.

For N samples and k variables:
1. Divide each variable's range into N equal-probability strata
2. Sample once from each stratum for each variable
3. Randomly pair the stratum samples across variables

This guarantees that each stratum of every variable is sampled exactly once,
ensuring full coverage across all dimensions simultaneously.

### 5.2 LHS vs Simple Monte Carlo

**Simple Monte Carlo:** Random points can cluster; some regions over-sampled,
others under-sampled. Wastes computational budget.

**LHS:** Guaranteed uniform marginal coverage. No clustering.
With N samples, LHS provides coverage equivalent to N^(1/k) points
per dimension where k = number of variables.

**Practical comparison:**
For 5 uncertain inputs with 100 samples:
- Simple MC: uneven coverage, possible gaps
- LHS: each input variable covered in 100 equal strata

### 5.3 When to Use LHS

- Multiple correlated uncertain inputs (supply chain risk models)
- Limited computation budget (LHS is more efficient than MC)
- Need good coverage of input space for sensitivity analysis
- Engineering simulation: structural analysis, circuit tolerances

LHS is the default sampling method in many commercial risk tools
(Crystal Ball, @Risk, Analytica, ModelRisk).

### 5.4 LHS with Correlation

Basic LHS ignores correlations between input variables.
To impose correlations, use the Iman-Conover method:
1. Generate LHS samples (uncorrelated)
2. Reorder ranks to match target correlation matrix
3. Back-transform to original distributions

This preserves marginal distributions while introducing desired correlations.
Critical when inputs are physically correlated (e.g., fuel price and freight rate).

### 5.5 Orthogonal Sampling

Extension of LHS: divide into N² equally-probable orthogonal cells.
Sample once per row AND column of the multi-dimensional grid.
Provides stronger uniformity guarantees than basic LHS.

### 5.6 Python Implementation

```python
from scipy.stats import qmc
import numpy as np

# Generate LHS samples
sampler = qmc.LatinHypercube(d=4, seed=42)  # 4 uncertain inputs
samples_unit = sampler.random(n=1000)  # 1000 samples in [0,1]^4

# Scale to physical distributions using percent-point function (inverse CDF)
from scipy.stats import norm, lognorm, uniform, triang

# Input 1: Demand - Normal(mu=500, sigma=80)
demand_samples = norm.ppf(samples_unit[:, 0], loc=500, scale=80)

# Input 2: Lead time - Lognormal(mean=7 days, sigma=2)
lt_samples = lognorm.ppf(samples_unit[:, 1], s=0.27, scale=7)

# Input 3: Unit cost - Triangular(low=45, mode=50, high=65)
cost_c = (50 - 45) / (65 - 45)  # peak location parameter
cost_samples = triang.ppf(samples_unit[:, 2], c=cost_c, loc=45, scale=20)

# Input 4: Fill rate target - Uniform(0.92, 0.99)
fill_samples = uniform.ppf(samples_unit[:, 3], loc=0.92, scale=0.07)

print(f"Demand: mean={demand_samples.mean():.1f}, std={demand_samples.std():.1f}")
print(f"Lead time: mean={lt_samples.mean():.2f}, std={lt_samples.std():.2f}")
```

### 5.7 Discrepancy Measures

Discrepancy quantifies how uniformly samples cover the space.
Lower discrepancy = better coverage.

**Star discrepancy D*:** Classical measure, hard to compute.
**Centered L2 discrepancy:** Computationally tractable.

```python
disc = qmc.discrepancy(samples_unit)
print(f"L2 discrepancy: {disc:.6f}")  # lower is better
```

---

## 6. DISCRETE EVENT SIMULATION (DES)

### 6.1 Concept

A Discrete Event Simulation (DES) models a system as a sequence of events
that occur at specific points in simulated time.

**Key principle:** The system state changes only at event times.
Between events, nothing happens — the simulation "jumps" from event to event.

**Contrast with continuous simulation:** Differential equations model smooth
evolution; DES models instantaneous state changes.

### 6.2 Core Components

**Entity:** An object that flows through the system.
Examples: shipment, pallet, work order, customer, truck.

**Resource:** A capacity-constrained facility or capability.
Examples: dock door, forklift, worker, machine, lane.

**Queue:** Where entities wait when resources are unavailable.
Examples: staging area, appointment backlog, printer queue.

**Event:** A discrete occurrence that changes system state.
Examples: arrival, service start, service complete, departure.

**Event list (Future Event List):** Ordered list of scheduled events by time.
The simulation engine processes events in chronological order.

**Clock:** Simulated time counter. Advances to next event time.

### 6.3 Event Processing Logic

```
Initialize: set clock = 0, create event list, set initial conditions

Loop:
  1. Remove next event from event list (smallest scheduled time)
  2. Advance clock to event time
  3. Execute event logic:
     - Update system state (queues, resources, statistics)
     - Schedule new future events as needed
  4. Collect statistics
  5. Repeat until termination condition

End: compute performance statistics, output reports
```

### 6.4 Queueing Theory Context

DES is the computational counterpart to analytical queueing theory (M/M/1, M/G/k etc.).

**M/M/1 queue:**
- Arrivals: Poisson process (rate λ)
- Service: Exponential distribution (rate μ)
- 1 server
- Analytical: L = λ/(μ-λ), W = 1/(μ-λ), ρ = λ/μ

DES can model M/G/k (general service, multiple servers), priority queues,
finite buffers, customer abandonment, reneging — all intractable analytically.

### 6.5 Supply Chain DES Applications

**Warehouse operation simulation:**
- Model receiving dock, inbound flow, putaway, pick lines, packing, shipping
- Identify bottlenecks: which resource has highest utilization?
- Test staffing scenarios: 8-hour vs 10-hour shifts, automation ROI
- Validate throughput under peak demand (holiday season)

**Port / terminal simulation:**
- Model vessel arrivals, berth assignments, crane operations, yard trucks
- Analyze vessel turnaround time distribution
- Test investment in new berths or cranes

**Last-mile delivery simulation:**
- Model vehicle routing, stop service times, customer availability
- Estimate delivery completion time distributions
- Test effects of time window changes or vehicle mix

**Manufacturing simulation:**
- Model production line with machines, buffers, operators
- Identify constraint (Theory of Constraints application)
- Test batch size, machine scheduling, maintenance intervals

### 6.6 DES vs System Dynamics

| Dimension            | DES                         | System Dynamics             |
|----------------------|-----------------------------|-----------------------------|
| Time treatment       | Discrete event jumps        | Continuous (differential)   |
| Resolution           | Individual entity tracking  | Aggregate flows/stocks      |
| Randomness           | Stochastic by default       | Often deterministic         |
| Insight focus        | Operational detail          | Policy/strategic feedback   |
| Bullwhip analysis    | Possible but complex        | Natural fit                 |
| Throughput/queuing   | Natural fit                 | Possible but aggregated     |

### 6.7 SimPy — Python DES Library

SimPy is a process-based DES framework for Python.
Processes are Python generators (using `yield`).

```python
import simpy
import numpy as np

def warehouse_order(env, order_id, dock, rng):
    """Simulates a single order flowing through a warehouse dock."""
    arrival_time = env.now
    print(f"Order {order_id} arrives at t={arrival_time:.1f}")
    
    # Request dock resource
    with dock.request() as req:
        yield req  # wait for dock
        wait_time = env.now - arrival_time
        print(f"Order {order_id} starts processing at t={env.now:.1f}, waited {wait_time:.1f}")
        
        # Processing time ~ Lognormal(mean=30min, sigma=10min)
        process_time = rng.lognormal(mean=np.log(30), sigma=0.3)
        yield env.timeout(process_time)
        
    print(f"Order {order_id} complete at t={env.now:.1f}")

def order_generator(env, dock, rng, arrival_rate):
    """Generates orders at Poisson arrival rate (orders/hour)."""
    order_id = 0
    while True:
        # Inter-arrival time ~ Exponential
        inter_arrival = rng.exponential(scale=60/arrival_rate)  # minutes
        yield env.timeout(inter_arrival)
        order_id += 1
        env.process(warehouse_order(env, order_id, dock, rng))

# Run simulation
rng = np.random.default_rng(seed=42)
env = simpy.Environment()
dock = simpy.Resource(env, capacity=3)  # 3 dock doors

env.process(order_generator(env, dock, rng, arrival_rate=8))  # 8 orders/hour
env.run(until=480)  # simulate 8-hour shift
```

---

## 7. SYSTEM DYNAMICS

### 7.1 Concept

System dynamics (SD) models systems as stocks (accumulations) and flows
(rates of change), connected by feedback loops.
Originated by Jay Forrester at MIT in the 1950s–60s.

**Stock:** A quantity that accumulates over time (e.g., inventory, backlog).
dStock/dt = inflow − outflow

**Flow:** Rate of change of a stock (e.g., shipment rate, order rate).

**Feedback loops:**
- Reinforcing (+): growth or collapse (compound interest, viral spread)
- Balancing (-): goal-seeking behavior (inventory replenishment)

### 7.2 The Bullwhip Effect

The Bullwhip Effect (Forrester Effect) is amplification of demand variability
as you move upstream in the supply chain:

Consumer demand → Retailer orders → Distributor orders → Manufacturer orders
(small variation)     (amplified)      (more amplified)   (most amplified)

**Causes:**
1. Order batching (weekly/monthly ordering creates lumpy signals)
2. Price fluctuations and forward buying
3. Shortage gaming (inflating orders during allocation)
4. Demand signal processing (exponential smoothing creates phantom trends)
5. Lead time variability

**System dynamics captures this** because it models the feedback loop:
Observed demand → Forecast → Order policy → Replenishment → Inventory → Order decision

---

## 8. RISK QUANTIFICATION AND ANALYSIS

### 8.1 Key Risk Metrics

**Value at Risk (VaR):**
VaR_α = F^{-1}(α) where F is the loss distribution CDF.
VaR at 95% confidence: the loss exceeded only 5% of the time.
VaR answers: "What is the maximum loss at a given confidence level?"

**Conditional Value at Risk (CVaR) / Expected Shortfall:**
CVaR_α = E[Loss | Loss > VaR_α]
Average of losses in the worst (1-α) scenarios.
Better than VaR because it considers the severity of tail events.
Required by Basel III for banking; increasingly adopted in supply chain.

**Probability of Ruin:**
P(Loss > Capital) — probability that losses exceed available resources.

### 8.2 Sensitivity Analysis

**Tornado diagram:** Bar chart ranking inputs by their contribution to output variance.
Most influential inputs at top ("tornado" shape).
Generated by varying each input by ±1 or ±2 standard deviations while holding others fixed.

**Spider diagram:** Lines showing output response to % changes in each input.
Steep slope = high sensitivity.

**Global sensitivity analysis (Sobol indices):**
Decomposes output variance into contributions from each input and interactions.
First-order Sobol index S_i: fraction of variance explained by input i alone.
Total-order Sobol index T_i: includes all interactions involving input i.
Computationally intensive; requires N×(k+2) model evaluations for k inputs.

### 8.3 Monte Carlo for Supply Chain Risk

**Step-by-step process:**

1. **Identify risk factors:**
   - Demand uncertainty (volume, mix)
   - Supply disruption risk (supplier failure, port congestion)
   - Price volatility (fuel, raw materials)
   - Lead time variability
   - Capacity constraints

2. **Quantify distributions:**
   - Fit historical data to distributions (chi-square or KS test)
   - Expert elicitation for low-frequency/high-impact risks
   - Use triangular when data is scarce

3. **Build correlation structure:**
   - Demand and competitor actions (negative correlation)
   - Fuel price and freight rate (positive correlation)
   - Economic conditions across product categories

4. **Run simulation:**
   - N = 10,000 to 100,000 scenarios
   - For each scenario: sample all inputs, compute financial outcome

5. **Analyze output:**
   - Revenue distribution, profit distribution, service level distribution
   - VaR, CVaR at relevant confidence levels
   - Identify dominant risk factors via sensitivity analysis

6. **Decision support:**
   - Compare risk mitigation strategies (hedging, dual sourcing, buffer stock)
   - Compute expected cost of each strategy
   - Select strategy with best risk-return tradeoff

---

## 9. SIMULATION OUTPUT ANALYSIS

### 9.1 Warm-Up Period (Transient Phase)

DES models start in an arbitrary initial state (often empty).
Early simulation results are not representative of steady-state behavior.
The warm-up period (transient phase) must be discarded.

**Welch's method:** Plot moving average of performance metric over time.
Warm-up ends when the moving average stabilizes.

### 9.2 Run Length and Replications

**Terminating simulations:** Fixed-length runs (e.g., one 8-hour shift).
Multiple independent replications (different seeds) provide statistical estimates.

**Steady-state simulations:** Run until convergence.
One long run is preferred over many short replications to reduce start-up bias.
Use batch means to estimate confidence intervals.

### 9.3 Confidence Intervals

For N independent replications with results X_1, ..., X_N:

Mean: X̄ = (1/N) Σ X_i
Std dev: S = √[(1/(N-1)) Σ (X_i - X̄)²]
95% CI: X̄ ± t_{N-1, 0.025} × S/√N

### 9.4 Comparing Scenarios

**Paired comparison:** Run same random seeds across scenarios.
Variance of difference is reduced because correlated random variation cancels.

**Common random numbers (CRN):** Synchronize random streams across scenarios.
Ensures differences are due to scenario changes, not random fluctuation.

**Statistical tests:**
- t-test: compare means of two scenarios
- ANOVA: compare multiple scenarios simultaneously
- Bonferroni correction: adjust significance level for multiple comparisons

---

## 10. PYTHON IMPLEMENTATION

### 10.1 Monte Carlo Safety Stock Example

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def monte_carlo_safety_stock(n_simulations=50000, target_service_level=0.95, seed=42):
    """
    Monte Carlo simulation to determine safety stock requirements.
    
    Inputs:
      - Daily demand: Normal(mu=100 units, sigma=25 units)
      - Lead time: Discrete distribution [3, 4, 5, 6, 7 days]
                   with probabilities [0.05, 0.20, 0.50, 0.20, 0.05]
      - Lead time demand = sum of daily demands during lead time
    """
    rng = np.random.default_rng(seed=seed)
    
    demand_mu, demand_sigma = 100, 25
    lt_values = [3, 4, 5, 6, 7]
    lt_probs = [0.05, 0.20, 0.50, 0.20, 0.05]
    
    demand_during_lt = np.zeros(n_simulations)
    
    for i in range(n_simulations):
        lt = rng.choice(lt_values, p=lt_probs)
        daily_demand = rng.normal(demand_mu, demand_sigma, size=lt)
        daily_demand = np.maximum(daily_demand, 0)  # no negative demand
        demand_during_lt[i] = daily_demand.sum()
    
    # Safety stock = quantile - expected demand during lead time
    expected_demand_lt = np.mean(demand_during_lt)
    safety_stock = np.quantile(demand_during_lt, target_service_level) - expected_demand_lt
    
    print(f"Expected demand during lead time: {expected_demand_lt:.1f} units")
    print(f"95th percentile demand during LT: {np.quantile(demand_during_lt, 0.95):.1f} units")
    print(f"99th percentile demand during LT: {np.quantile(demand_during_lt, 0.99):.1f} units")
    print(f"Safety stock at {target_service_level*100:.0f}% SL: {safety_stock:.1f} units")
    
    # Compare with analytical formula
    avg_lt = sum(v*p for v,p in zip(lt_values, lt_probs))
    var_lt = sum(p*(v-avg_lt)**2 for v,p in zip(lt_values, lt_probs))
    analytical_ss = stats.norm.ppf(target_service_level) * np.sqrt(
        avg_lt * demand_sigma**2 + demand_mu**2 * var_lt
    )
    print(f"Analytical safety stock (approx): {analytical_ss:.1f} units")
    
    return demand_during_lt, safety_stock

demand_dist, ss = monte_carlo_safety_stock()
```

### 10.2 LHS Risk Simulation for Project Schedule

```python
import numpy as np
from scipy.stats import qmc, norm, triang, lognorm

def project_risk_lhs(n_samples=5000, seed=42):
    """
    LHS-based project completion time simulation.
    4 work packages with uncertain durations.
    Critical path = max of two parallel paths.
    """
    sampler = qmc.LatinHypercube(d=4, seed=seed)
    u = sampler.random(n=n_samples)
    
    # Task durations (weeks): triangular distributions
    # Task A: PERT(8, 10, 15) weeks
    # Task B: PERT(6, 8, 12) weeks
    # Task C: PERT(4, 5, 8) weeks -- sequential after A
    # Task D: PERT(10, 14, 20) weeks
    
    def pert(u, a, m, b):
        """PERT distribution via scaled triangular."""
        c = (m - a) / (b - a)
        return triang.ppf(u, c=c, loc=a, scale=b-a)
    
    task_A = pert(u[:, 0], 8, 10, 15)
    task_B = pert(u[:, 1], 6, 8, 12)
    task_C = pert(u[:, 2], 4, 5, 8)
    task_D = pert(u[:, 3], 10, 14, 20)
    
    # Path 1: A → C (sequential)
    path1 = task_A + task_C
    
    # Path 2: B + D (parallel, both must complete)
    path2 = np.maximum(task_B, task_D)
    
    # Project completes when BOTH paths complete
    project_duration = np.maximum(path1, path2)
    
    p50 = np.percentile(project_duration, 50)
    p80 = np.percentile(project_duration, 80)
    p95 = np.percentile(project_duration, 95)
    
    print(f"P50 completion: {p50:.1f} weeks")
    print(f"P80 completion: {p80:.1f} weeks")  
    print(f"P95 completion: {p95:.1f} weeks")
    print(f"P(complete by week 30): {np.mean(project_duration <= 30)*100:.1f}%")
    
    return project_duration

durations = project_risk_lhs()
```

### 10.3 Sensitivity / Tornado Analysis

```python
import numpy as np
import matplotlib.pyplot as plt

def tornado_analysis(base_inputs, output_fn, input_names, delta=0.1):
    """
    Simple one-at-a-time sensitivity analysis (tornado chart).
    
    Args:
        base_inputs: dict of {name: base_value}
        output_fn: function(inputs_dict) -> scalar output
        input_names: ordered list of input names
        delta: fractional change (10% by default)
    """
    base_output = output_fn(base_inputs)
    swings = []
    
    for name in input_names:
        inputs_low = dict(base_inputs)
        inputs_high = dict(base_inputs)
        inputs_low[name] = base_inputs[name] * (1 - delta)
        inputs_high[name] = base_inputs[name] * (1 + delta)
        
        out_low = output_fn(inputs_low)
        out_high = output_fn(inputs_high)
        swing = out_high - out_low
        swings.append((name, out_low, out_high, swing))
    
    # Sort by absolute swing
    swings.sort(key=lambda x: abs(x[3]), reverse=True)
    
    # Plot tornado
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (name, lo, hi, swing) in enumerate(swings):
        ax.barh(i, hi - base_output, left=base_output, color='steelblue', alpha=0.8)
        ax.barh(i, lo - base_output, left=base_output, color='coral', alpha=0.8)
    
    ax.set_yticks(range(len(swings)))
    ax.set_yticklabels([s[0] for s in swings])
    ax.axvline(base_output, color='black', linewidth=1)
    ax.set_xlabel("Output Value")
    ax.set_title("Tornado Diagram — Sensitivity Analysis")
    plt.tight_layout()
    plt.show()
    
    return swings
```

---

## 11. QUICK REFERENCE

### Distribution Selection Guide

| Situation                              | Distribution         |
|----------------------------------------|----------------------|
| Physical measurement, aggregated       | Normal               |
| Cost, price, time (skewed, >0)         | Lognormal            |
| Expert estimate with min/mode/max      | Triangular or PERT   |
| Complete ignorance, bounded            | Uniform              |
| Time between events (memoryless)       | Exponential          |
| Count of events in fixed interval      | Poisson              |
| Proportion, probability                | Beta                 |
| Equipment failure / aging              | Weibull              |
| Binary event (success/failure)         | Bernoulli/Binomial   |

### Variance Reduction Technique Selection

| Technique              | Best Used When                           | Reduction Factor     |
|------------------------|------------------------------------------|----------------------|
| Latin Hypercube        | Multiple inputs, limited samples         | 2–10×                |
| Stratified Sampling    | Single input, need tail coverage         | 2–5×                 |
| Antithetic Variates    | Monotone function, symmetric noise       | Up to 2×             |
| Control Variates       | Correlated control variable known        | 2–50× (high ρ)       |
| Importance Sampling    | Rare event (p < 0.01)                    | 100–1000×            |
| Quasi-Monte Carlo      | Low dimensions (d ≤ 10), smooth function | O(log N/N) vs O(1/√N)|

### Key Risk Metrics

| Metric     | Definition                              | Supply Chain Application          |
|------------|-----------------------------------------|-----------------------------------|
| VaR(95%)   | Loss exceeded only 5% of time           | Maximum likely freight cost       |
| CVaR(95%)  | Avg loss in worst 5% of scenarios       | Expected cost in disruption       |
| P(stockout)| P(demand > inventory)                   | Service level risk                |
| P(delay)   | P(project/order late)                   | On-time delivery probability      |

### Python Libraries for Simulation

| Library          | Purpose                                         |
|------------------|-------------------------------------------------|
| numpy            | Random sampling, array operations               |
| scipy.stats      | Distributions (PPF, CDF, fit)                   |
| scipy.stats.qmc  | LHS, Sobol, Halton sequences, discrepancy       |
| simpy            | Process-based discrete event simulation         |
| salabim          | Advanced DES with animation                     |
| SALib            | Sobol sensitivity analysis (global)             |
| pymc             | Bayesian Monte Carlo (MCMC)                     |
| mesa             | Agent-based modeling                            |

---
*End of SIMULATION_KB.md*
*Sources: IBM Think, AWS, Investopedia, Wikipedia (DES), scipy documentation,*
*Packham (2015) Wilmott, INFORMS Operations Research, Law & Kelton "Simulation Modeling"*

---

## Knowledge Update — 2026-03-06

### Prediction-Enhanced Monte Carlo (PEMC)
**Source:** arXiv:2412.11257v2 — Published / updated May 26, 2025
**URL:** https://arxiv.org/abs/2412.11257

A new ML-augmented framework that treats control variate construction as a **machine learning prediction problem**:
- Core idea: use cheap, parallelizable simulations as *features* for a learned ML predictor, which outputs **unbiased estimates with reduced variance and runtime**
- PEMC generalizes classical control variates — where traditional methods require analytically known expected values for the control, PEMC learns the predictor from data
- Demonstrated on: Asian options, variance swaps (stochastic local vol), swaptions (HJM models), ambulance diversion policy evaluation
- Bias analysis and variance reduction proofs are provided via learning theory estimates (approximation error + statistical error decomposition)

**Key properties:**
| Property | Classical CV | PEMC |
|---|---|---|
| Control function | Must be analytically tractable | Learned from simulations |
| Unbiasedness | Yes | Yes (preserved by design) |
| Variance reduction | Depends on correlation | Quantified by learning theory |
| Scalability | Limited | Parallelizable |

**Supply chain relevance:** PEMC is applicable wherever you run many MC replications to estimate an expected cost, service level, or lead time distribution. The ML predictor learns from early simulation runs and improves subsequent estimates — useful for demand uncertainty modeling or safety stock optimization when simulation is expensive.

### Multilevel Monte Carlo and Hybrid Sampling — State of Practice
**Source:** analytica.com (Oct 2025), ScienceDirect (Aug/Jan 2026)

Current best-practice tier for variance reduction in MC:
1. **Multilevel Monte Carlo (MLMC):** Use a hierarchy of resolution levels; coarse simulations are cheap, fine simulations are few. Computational cost scales as O(ε⁻²) vs. O(ε⁻³) for standard MC at tolerance ε.
2. **Stratified sampling:** Partition the probability space into strata; sample each stratum proportionally. Eliminates between-stratum variance entirely.
3. **Control variates:** Classic method — subtract a correlated quantity with known expectation. PEMC extends this to learned predictors.
4. **Quasi-Monte Carlo (QMC):** Replace pseudo-random sequences with low-discrepancy sequences (Sobol, Halton). Convergence rate O(N⁻¹(log N)^d) vs. O(N⁻½) for standard MC in d dimensions.

*Sources: arXiv:2412.11257 (2025), analytica.com (2025-10), ScienceDirect (2025-08, 2026-01)*
