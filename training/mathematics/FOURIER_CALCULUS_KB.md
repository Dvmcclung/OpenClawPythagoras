# FOURIER_CALCULUS_KB.md
# Knowledge Base: Fourier Analysis, Calculus, and Mathematical Optimization
# For use by Pythagoras AI — Quantix Supply Chain Solutions
# Last updated: 2026-03-04

---

## TABLE OF CONTENTS

1. Fourier Series
2. Discrete Fourier Transform (DFT)
3. Fast Fourier Transform (FFT)
4. Spectral Analysis Applications
5. Signal Processing and Filtering
6. Differential Calculus Review
7. Gradient Descent Optimization
8. Advanced Gradient Methods
9. Lagrange Multipliers and Constrained Optimization
10. Ordinary Differential Equations (ODEs)
11. Mathematical Optimization in Operations
12. Python Code Examples
13. Quick Reference

---

## 1. FOURIER SERIES

### 1.1 Core Idea

Any periodic function can be expressed as an infinite sum of sine and cosine
functions of increasing frequency. Named after Jean-Baptiste Joseph Fourier (1822).

**Fourier Series for a periodic function f(t) with period T:**

f(t) = a₀/2 + Σ_{n=1}^∞ [aₙ cos(2πnt/T) + bₙ sin(2πnt/T)]

**Coefficients:**
a₀ = (2/T) ∫₀ᵀ f(t) dt                (DC component / mean)
aₙ = (2/T) ∫₀ᵀ f(t) cos(2πnt/T) dt   (cosine coefficients)
bₙ = (2/T) ∫₀ᵀ f(t) sin(2πnt/T) dt   (sine coefficients)

**Complex exponential form (Euler's formula):**
f(t) = Σ_{n=-∞}^∞ cₙ exp(2πi·n·t/T)
cₙ = (1/T) ∫₀ᵀ f(t) exp(-2πi·n·t/T) dt

### 1.2 Physical Interpretation

Each term represents a sinusoidal wave at frequency n/T (cycles per unit time).

**Frequency:** f = n/T  (cycles per second = Hz when t is in seconds)
**Angular frequency:** ω = 2πf = 2πn/T  (radians per second)
**Period:** T = 1/f
**Amplitude of nth harmonic:** Aₙ = √(aₙ² + bₙ²)
**Phase of nth harmonic:** φₙ = arctan(bₙ/aₙ)

### 1.3 Parseval's Theorem

Total power in the time domain equals total power in the frequency domain:
(1/T) ∫₀ᵀ |f(t)|² dt = Σ |cₙ|²

This is conservation of energy across representations.

### 1.4 Convergence

The Fourier series converges to f(t) at points of continuity.
At jump discontinuities, it converges to the midpoint of the jump.
**Gibbs phenomenon:** Overshoot of ~9% near discontinuities that persists
no matter how many terms are included.

---

## 2. DISCRETE FOURIER TRANSFORM (DFT)

### 2.1 Definition

For a finite sequence of N complex numbers {x₀, x₁, ..., x_{N-1}}, the DFT is:

X_k = Σ_{n=0}^{N-1} x_n · exp(-2πi·k·n/N)   for k = 0, 1, ..., N-1

The inverse DFT (IDFT):
x_n = (1/N) Σ_{k=0}^{N-1} X_k · exp(2πi·k·n/N)

### 2.2 Interpretation of Output

**X_0:** Sum of all values (N × mean). DC component.
**|X_k|²:** Power at frequency k/N cycles per sample (power spectrum).
**|X_k|:** Amplitude of frequency component k.
**arg(X_k):** Phase of frequency component k.

**Frequency resolution:** Δf = 1/(N·Δt) where Δt is the sampling interval.
**Nyquist frequency:** f_max = 1/(2Δt) — maximum detectable frequency.
**Total frequency range:** [0, 1/(2Δt)] (positive frequencies only for real signals).

### 2.3 Aliasing

If signal contains frequencies above the Nyquist limit, they "fold" into
lower frequencies, corrupting the spectrum. This is called aliasing.

**Nyquist-Shannon Sampling Theorem:**
A signal must be sampled at least twice the highest frequency component
to be perfectly reconstructed: f_sample ≥ 2 × f_max

In practice, use anti-aliasing filter to remove frequencies > f_Nyquist
before sampling.

### 2.4 DFT in Supply Chain Context

For a daily demand time series sampled at Δt = 1 day (N = 365 days):
- Frequency resolution: Δf = 1/365 cycles/day = 1 cycle/year
- Nyquist frequency: 0.5 cycles/day = ~2-day period
- To detect weekly seasonality (7-day period): need f = 1/7 ≈ 0.143 cycles/day
  → k = N × f = 365 × (1/7) ≈ k = 52 (52nd frequency bin)
- To detect annual seasonality (365-day period): k = 1

---

## 3. FAST FOURIER TRANSFORM (FFT)

### 3.1 Computational Complexity

**DFT directly:** O(N²) operations — prohibitively slow for large N.
**FFT algorithm (Cooley-Tukey, 1965):** O(N log N) — dramatically faster.

For N = 1,000,000:
- DFT: 10^12 operations
- FFT: ~2×10^7 operations  (50,000× faster)

The FFT recursively divides the DFT into smaller DFTs.
Most efficient when N is a power of 2 (e.g., 512, 1024, 2048).

### 3.2 Cooley-Tukey Algorithm (Radix-2)

For N = 2^m:
X_k = Σ_{n=0}^{N/2-1} x_{2n} e^{-2πik(2n)/N} + e^{-2πik/N} Σ_{n=0}^{N/2-1} x_{2n+1} e^{-2πik(2n)/N}

= DFT_even(k) + W_N^k × DFT_odd(k)   where W_N = e^{-2πi/N} (twiddle factor)

Recursively apply until base cases (N=1). This is a "divide and conquer" approach.

### 3.3 FFT Variants

**RFFT (Real FFT):** Optimized for real-valued input.
Output has Hermitian symmetry: X_{N-k} = X_k*
Only N/2 + 1 unique values needed (not N).
2× faster and 2× less memory than complex FFT for real signals.

**STFT (Short-Time Fourier Transform):**
Apply FFT to sliding windows of the signal.
Produces time-frequency representation (spectrogram).
Trade-off: frequency resolution vs. time resolution.
Window size W: frequency resolution = 1/(W·Δt), time resolution = W·Δt

**Wavelet Transform:**
Better time-frequency localization than STFT.
Uses variable-length windows (narrow for high frequencies, wide for low).

---

## 4. SPECTRAL ANALYSIS APPLICATIONS

### 4.1 Periodicity Detection in Demand Data

**Problem:** Detect dominant seasonal periods in a demand time series.

**Method:**
1. Compute FFT of the detrended demand series
2. Compute power spectrum: P_k = |X_k|²
3. Identify dominant peaks in the power spectrum
4. Convert frequency to period: T_k = N/(k × sampling_rate)

**Supply chain periodicities to detect:**
- Weekly (7-day): k ≈ N/7
- Bi-weekly (14-day): k ≈ N/14
- Monthly (~30-day): k ≈ N/30
- Quarterly (90-day): k ≈ N/90
- Annual (365-day): k = 1 (if N=365 days)

```python
import numpy as np
import matplotlib.pyplot as plt

def detect_seasonality(demand_series, sampling_rate_days=1):
    """Detect dominant seasonal periods using FFT."""
    n = len(demand_series)
    
    # Detrend: remove linear trend to isolate seasonality
    t = np.arange(n)
    trend_coeff = np.polyfit(t, demand_series, 1)
    trend = np.polyval(trend_coeff, t)
    detrended = demand_series - trend
    
    # FFT
    fft_vals = np.fft.rfft(detrended)
    power = np.abs(fft_vals)**2
    frequencies = np.fft.rfftfreq(n, d=sampling_rate_days)  # cycles per day
    
    # Find top 5 peaks (ignore DC component at k=0)
    peak_idx = np.argsort(power[1:])[-5:][::-1] + 1
    
    print("Top seasonal periods detected:")
    for idx in peak_idx:
        if frequencies[idx] > 0:
            period = 1 / frequencies[idx]
            print(f"  Period: {period:.1f} days, Frequency: {frequencies[idx]:.4f} cycles/day, "
                  f"Power: {power[idx]:.2f}")
    
    return frequencies, power

# Example usage
np.random.seed(42)
t = np.arange(365*3)  # 3 years of daily data
# Synthetic demand: trend + weekly + annual seasonality + noise
demand = (500 + 0.1*t 
          + 50*np.sin(2*np.pi*t/7)       # weekly
          + 120*np.sin(2*np.pi*t/365)    # annual
          + np.random.normal(0, 30, len(t)))
freq, power = detect_seasonality(demand)
```

### 4.2 Signal Filtering

**Low-pass filter:** Remove high-frequency noise, keep trend.
In frequency domain: zero out high-frequency components, apply IFFT.

**High-pass filter:** Remove trend, keep high-frequency variations.

**Band-pass filter:** Keep only frequencies in a specific range.
Useful for isolating specific seasonal cycles.

```python
def lowpass_filter(signal, cutoff_period_days):
    """Low-pass filter: keep periods longer than cutoff."""
    n = len(signal)
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0)  # d=1 day
    
    # Zero out frequencies above cutoff
    cutoff_freq = 1.0 / cutoff_period_days
    fft_vals[freqs > cutoff_freq] = 0
    
    filtered = np.fft.irfft(fft_vals, n=n)
    return filtered

# Extract trend (periods > 90 days)
trend_signal = lowpass_filter(demand, cutoff_period_days=90)
```

### 4.3 Power Spectral Density (PSD)

For stochastic processes, PSD describes how power is distributed across frequencies.

**Welch's method (scipy.signal.welch):**
Averages periodograms from overlapping windows.
Reduces variance of the spectral estimate at the cost of frequency resolution.

```python
from scipy import signal as sp_signal

# Compute PSD using Welch's method
f, Pxx = sp_signal.welch(demand, fs=1.0,  # fs = 1 sample/day
                          nperseg=256,      # window size
                          noverlap=128)     # 50% overlap

# Convert frequency to period
periods = 1.0 / f[1:]  # skip DC (f[0]=0)
plt.semilogx(periods, Pxx[1:])
plt.xlabel("Period (days)")
plt.ylabel("Power spectral density")
plt.title("Demand Seasonality: Power Spectrum")
```

---

## 5. SIGNAL PROCESSING AND FILTERING

### 5.1 Moving Average as Low-Pass Filter

A simple moving average is equivalent to a low-pass filter in the frequency domain.
The MA(k) filter has frequency response:
H(f) = sin(πfk) / (k · sin(πf))

Longer windows: stronger attenuation of high frequencies.
Sharp transitions preserved: shorter windows.

### 5.2 Savitzky-Golay Filter

Fits a polynomial to a sliding window; equivalent to a smoothing filter
that preserves higher moments (peaks, valleys) better than MA.
Used for demand signal smoothing while preserving local structure.

```python
from scipy.signal import savgol_filter
smoothed = savgol_filter(demand, window_length=15, polyorder=3)
```

### 5.3 Autocorrelation and Cross-Correlation via FFT

Autocorrelation can be computed efficiently using FFT:
R_xx(τ) = IFFT(|FFT(x)|²)  (Wiener-Khinchin theorem)

Cross-correlation between two signals:
R_xy(τ) = IFFT(FFT(x)* · FFT(y))

This is O(N log N) vs O(N²) for direct computation.

---

## 6. DIFFERENTIAL CALCULUS REVIEW

### 6.1 Derivatives

The derivative of f at x: f'(x) = lim_{h→0} [f(x+h) - f(x)] / h

**Chain rule:** d/dx f(g(x)) = f'(g(x)) · g'(x)
**Product rule:** d/dx [f·g] = f'g + fg'
**Quotient rule:** d/dx [f/g] = (f'g - fg') / g²

### 6.2 Partial Derivatives

For f(x, y): ∂f/∂x = limit holding y constant.

**Gradient:** ∇f = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)ᵀ
The gradient points in the direction of steepest ascent.
Magnitude |∇f| gives rate of change in that direction.

**Hessian matrix:** H_{ij} = ∂²f/(∂x_i ∂x_j)
Second-order information: curvature of the function.
- H positive definite → local minimum
- H negative definite → local maximum
- H indefinite → saddle point

### 6.3 Taylor Series Expansion

f(x + Δx) ≈ f(x) + ∇f(x)ᵀ Δx + ½ ΔxᵀH(x)Δx + O(|Δx|³)

First-order (linear) approximation: f(x) + ∇f(x)ᵀ Δx
Second-order (quadratic) approximation: adds curvature term.

Gradient descent uses first-order; Newton's method uses second-order.

### 6.4 Convexity

A function f is convex if:
f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y)  for all x, y and λ ∈ [0,1]

Equivalently: H(x) is positive semidefinite for all x.

**Key property:** For convex functions, any local minimum is a global minimum.
All gradient-based methods are guaranteed to find the global optimum for convex f.

**Strictly convex:** H(x) positive definite → unique minimum.

**Examples:**
- Convex: x², e^x, |x|, max(x, 0)
- Non-convex: sin(x), x³, deep neural network loss surfaces

---

## 7. GRADIENT DESCENT OPTIMIZATION

### 7.1 Algorithm

Gradient descent minimizes f(θ) by iteratively moving against the gradient:

θ_{t+1} = θ_t - α · ∇f(θ_t)

where α > 0 is the learning rate (step size).

**Intuition:** Stand on a hillside. Gradient points uphill. Take a step downhill.
Repeat until you reach the valley floor (local minimum).

**Convergence:** For convex f with Lipschitz gradient, GD converges at O(1/T).
For strongly convex f: exponential (linear) convergence.

### 7.2 Learning Rate Selection

**Too small:** Slow convergence; may take thousands of iterations.
**Too large:** Oscillation, divergence; overshoots minimum.
**Just right:** Stable, fast convergence.

**Lipschitz condition:** If |∇f(x) - ∇f(y)| ≤ L|x-y|, then optimal step size = 1/L.
This is the maximum step that guarantees convergence.

**Line search:** At each step, find optimal α by minimizing f(θ_t - α ∇f) over α.
Exact line search: expensive but optimal step size.
Backtracking: start with large α, reduce by factor until Armijo condition satisfied.

### 7.3 Variants

**Batch Gradient Descent:**
Use all N training examples to compute gradient.
∇f(θ) = (1/N) Σᵢ ∇fᵢ(θ)
Stable but slow for large datasets (one update per full pass).

**Stochastic Gradient Descent (SGD):**
Use single random example for gradient estimate.
θ_{t+1} = θ_t - α · ∇fᵢ(θ_t)  (i randomly chosen)
Noisy but fast; good for large datasets. Noise can help escape local minima.
Requires diminishing learning rate for convergence: α_t = α₀/(1 + decay·t).

**Mini-batch SGD:**
Use batch of B examples (typically B = 32, 64, 128).
Best of both worlds: lower variance than SGD, faster than batch GD.
Standard in deep learning (each "epoch" = one pass through data).

### 7.4 Momentum

Momentum accumulates gradient direction across iterations:
v_{t+1} = β v_t + (1-β) ∇f(θ_t)     (velocity)
θ_{t+1} = θ_t - α v_{t+1}

**β** (momentum coefficient, typically 0.9): how much of past velocity to retain.
Effect: smooths oscillations in narrow valleys, accelerates in consistent directions.
Named after "heavy ball" rolling down a landscape with momentum.

**Nesterov Accelerated Gradient (NAG):**
"Look ahead" before computing gradient:
θ_lookahead = θ_t - β v_t
v_{t+1} = β v_t + α ∇f(θ_lookahead)
θ_{t+1} = θ_t - v_{t+1}
Theoretically optimal first-order method for convex problems: O(1/T²) convergence.

### 7.5 Adaptive Learning Rate Methods

**AdaGrad:**
Accumulate sum of squared gradients G_t = Σ_{s=1}^t ∇f(θ_s)²
θ_{t+1} = θ_t - α/√(G_t + ε) · ∇f(θ_t)  (element-wise)

Per-parameter adaptive rates. Good for sparse features.
Weakness: G_t grows monotonically → learning rate shrinks to 0.

**RMSProp:**
Exponentially decaying average of squared gradients:
G_t = γ G_{t-1} + (1-γ) ∇f(θ_t)²
θ_{t+1} = θ_t - α/√(G_t + ε) · ∇f(θ_t)

Solves AdaGrad's vanishing learning rate problem.

**Adam (Adaptive Moment Estimation):**
Most popular optimizer in deep learning.
Combines momentum (first moment) and RMSProp (second moment):

m_t = β₁ m_{t-1} + (1-β₁) ∇f(θ_t)          (first moment / momentum)
v_t = β₂ v_{t-1} + (1-β₂) ∇f(θ_t)²          (second moment / variance)
m̂_t = m_t / (1-β₁ᵗ)                           (bias correction)
v̂_t = v_t / (1-β₂ᵗ)                           (bias correction)
θ_{t+1} = θ_t - α · m̂_t / (√v̂_t + ε)

Defaults: β₁=0.9, β₂=0.999, ε=1e-8, α=0.001

### 7.6 Newton's Method (Second-Order)

Uses Hessian (curvature) information:
θ_{t+1} = θ_t - H(θ_t)⁻¹ ∇f(θ_t)

**Advantages:** Much faster convergence near minimum (quadratic).
**Disadvantages:** Computing and inverting H is O(n³) — too expensive for large n.

**Quasi-Newton (L-BFGS):**
Approximate H⁻¹ using gradient history. O(n) per step.
Very effective for moderate-scale optimization (thousands of parameters).
Used in statsmodels ARIMA fitting, scipy.optimize, scikit-learn.

### 7.7 Gradient Descent in Supply Chain ML

**Model training:** All gradient boosting (XGBoost, LightGBM) uses a form
of gradient descent — fits each new tree to the negative gradient of the loss.

**Hyperparameter optimization:** Gradient-free methods typically used
(Bayesian optimization, grid/random search) since gradients w.r.t.
hyperparameters are unavailable.

**Parameter fitting in statsmodels:** ARIMA uses L-BFGS-B to minimize
log-likelihood (equivalent to nonlinear least squares).

---

## 8. ADVANCED GRADIENT METHODS

### 8.1 Coordinate Descent

Minimize one variable at a time, cycling through all variables:
θᵢ_{t+1} = argmin_{θᵢ} f(θ₁, ..., θᵢ, ..., θₙ)  holding others fixed.

Used in: LASSO regression (glmnet, scikit-learn ElasticNet).
Effective when per-coordinate minimization has closed form.

### 8.2 Projected Gradient Descent

For constrained optimization: project back to feasible set after each step.
θ_{t+1} = Proj_C(θ_t - α ∇f(θ_t))
where Proj_C(x) = argmin_{y ∈ C} ||x - y||

Used for: box constraints (variable bounds), simplex constraints.

### 8.3 Subgradient Methods

For non-differentiable functions (|x|, max(x, 0)):
Use any subgradient g_t ∈ ∂f(θ_t) in place of gradient.
Convergence is slower: O(1/√T) vs O(1/T) for smooth problems.

---

## 9. LAGRANGE MULTIPLIERS AND CONSTRAINED OPTIMIZATION

### 9.1 Problem Formulation

**General constrained optimization:**
min f(x)
subject to:
  g_i(x) = 0   for i = 1, ..., m  (equality constraints)
  h_j(x) ≤ 0   for j = 1, ..., p  (inequality constraints)

### 9.2 Lagrange Multipliers — Equality Constraints

**Key insight (Lagrange, 1788):** At a constrained optimum, the gradient of f
must be a linear combination of the gradients of the active constraints.

∇f(x*) = Σᵢ λᵢ ∇gᵢ(x*)

**Lagrangian function:**
L(x, λ) = f(x) - Σᵢ λᵢ gᵢ(x)

**Optimality conditions (Lagrange conditions):**
∂L/∂x = 0    → ∇f = Σ λᵢ ∇gᵢ
∂L/∂λ = 0    → g(x) = 0  (constraints satisfied)

Solve this system of equations to find candidate optima.

**Interpretation of λ:** The Lagrange multiplier λᵢ represents the sensitivity
of the optimal objective value to the constraint: dF*/dcᵢ = λᵢ where gᵢ(x) = cᵢ.
In economics: shadow price (value of relaxing the constraint by 1 unit).

### 9.3 Example: Portfolio Optimization

**Minimize portfolio variance** subject to target return:
min σ²_p = wᵀΣw
subject to: μᵀw = r_target, 1ᵀw = 1

Lagrangian: L = wᵀΣw - λ₁(μᵀw - r) - λ₂(1ᵀw - 1)

First-order conditions:
∂L/∂w = 2Σw - λ₁μ - λ₂1 = 0
→ w* = Σ⁻¹(λ₁μ + λ₂1) / 2

Substitute back to find λ₁, λ₂ from constraints.
This gives the minimum-variance frontier portfolio.

### 9.4 KKT Conditions — Inequality Constraints

The **Karush-Kuhn-Tucker (KKT) conditions** extend Lagrange to inequality constraints.

For min f(x) s.t. g_i(x) = 0, h_j(x) ≤ 0:

1. **Stationarity:** ∇f(x*) + Σ μᵢ ∇gᵢ(x*) + Σ νⱼ ∇hⱼ(x*) = 0
2. **Primal feasibility:** gᵢ(x*) = 0, hⱼ(x*) ≤ 0
3. **Dual feasibility:** νⱼ ≥ 0
4. **Complementary slackness:** νⱼ hⱼ(x*) = 0

Complementary slackness: either νⱼ = 0 (constraint inactive) or hⱼ = 0 (active).
This means multiplier is 0 for inactive constraints, positive for binding ones.

KKT conditions are necessary for optimality; sufficient when f is convex and
constraints are convex.

### 9.5 Applications in Supply Chain

**Resource allocation:** Maximize output subject to budget and capacity constraints.
**Transportation:** Min cost subject to flow conservation constraints.
**Inventory:** Minimize holding + ordering cost subject to service level constraint.
**Facility location:** Minimize total distance subject to site capacity constraints.

The KKT multipliers on capacity constraints = shadow prices:
they tell you the marginal value of adding one unit of capacity.

### 9.6 Linear Programming Connection

Linear Programming (LP):
min cᵀx  s.t.  Ax ≤ b, x ≥ 0

KKT conditions for LP are equivalent to LP duality:
Primal: min cᵀx s.t. Ax ≥ b, x ≥ 0
Dual:   max bᵀy s.t. Aᵀy ≤ c, y ≥ 0

At optimality: cᵀx* = bᵀy* (strong duality)
Dual variables y* = Lagrange multipliers = shadow prices of constraints.

---

## 10. ORDINARY DIFFERENTIAL EQUATIONS (ODEs)

### 10.1 Classification

**ODE:** Equation involving derivatives of a function of one variable.
dy/dt = f(t, y)  (first-order)
d²y/dt² + p(t) dy/dt + q(t)y = r(t)  (second-order linear)

**System of ODEs:**
dx₁/dt = f₁(t, x₁, x₂, ..., xₙ)
...
dxₙ/dt = fₙ(t, x₁, x₂, ..., xₙ)

In vector form: dx/dt = f(t, x)

### 10.2 Key ODE Types

**Exponential growth/decay:** dy/dt = ky → y(t) = y₀ e^{kt}
Supply chain: demand decay after product launch, inventory depletion.

**Logistic growth:** dy/dt = ry(1 - y/K) → S-curve toward carrying capacity K.
Models: market penetration, product adoption, capacity utilization.

**Harmonic oscillator:** d²x/dt² + ω²x = 0 → x(t) = A cos(ωt + φ)
Models: inventory oscillations, bullwhip effect cycles.

**Damped oscillator:** d²x/dt² + 2γ dx/dt + ω²x = 0
Underdamped (γ < ω): decaying oscillations → inventory overshoot that stabilizes
Overdamped (γ > ω): smooth return to equilibrium

### 10.3 System Dynamics ODEs

The bullwhip effect as a system of ODEs:

Let I(t) = inventory level, D(t) = demand rate, O(t) = order rate.
Inventory: dI/dt = O(t - L) - D(t)     (orders arrive after lead time L)
Orders: O(t) = D(t) + (I_target - I(t)) / τ  (reorder policy with time constant τ)

Small τ (aggressive ordering) → large inventory oscillations (bullwhip amplified)
Large τ (patient ordering) → smooth inventory, longer adjustment time

### 10.4 Numerical ODE Solving

Analytical solutions exist for few ODEs. Numerical methods:

**Euler's method (first-order):**
x(t + Δt) ≈ x(t) + Δt · f(t, x(t))
Simple but low accuracy. Error O(Δt).

**Runge-Kutta 4 (RK4):**
Standard method. Uses 4 evaluations per step.
k₁ = f(t, x)
k₂ = f(t + Δt/2, x + Δt k₁/2)
k₃ = f(t + Δt/2, x + Δt k₂/2)
k₄ = f(t + Δt, x + Δt k₃)
x(t + Δt) = x(t) + (Δt/6)(k₁ + 2k₂ + 2k₃ + k₄)
Error O(Δt⁴).

```python
from scipy.integrate import solve_ivp
import numpy as np

def bullwhip_model(t, state, demand_rate=100, lead_time=5, adj_time=2, target_inv=500):
    """
    Simple inventory-order ODE system (stock management).
    state = [inventory, pipeline_order]
    """
    I, P = state
    D = demand_rate * (1 + 0.1 * np.sin(2*np.pi*t/52))  # seasonal demand
    
    dI_dt = P/lead_time - D  # inventory change
    dP_dt = D + (target_inv - I)/adj_time - P/lead_time  # order rate
    
    return [dI_dt, dP_dt]

# Solve ODE system over 104 weeks (2 years)
solution = solve_ivp(
    bullwhip_model,
    t_span=(0, 104),
    y0=[500, 500],  # initial inventory, pipeline
    t_eval=np.linspace(0, 104, 1000),
    method='RK45'
)

import matplotlib.pyplot as plt
plt.plot(solution.t, solution.y[0], label='Inventory')
plt.axhline(500, linestyle='--', label='Target')
plt.xlabel('Week')
plt.ylabel('Units')
plt.title('Inventory Dynamics (ODE Model)')
plt.legend()
```

---

## 11. MATHEMATICAL OPTIMIZATION IN OPERATIONS

### 11.1 Unconstrained Optimization

**scipy.optimize.minimize:**
```python
from scipy.optimize import minimize
import numpy as np

def objective(x):
    return (x[0] - 3)**2 + (x[1] - 4)**2 + 0.5*x[0]*x[1]

result = minimize(objective, x0=[0, 0], method='L-BFGS-B')
print(f"Optimal x: {result.x}")
print(f"Optimal f: {result.fun:.4f}")
```

### 11.2 Constrained Optimization

```python
from scipy.optimize import minimize

# Minimize total cost subject to service level constraint
def total_cost(x):
    q, ss = x  # order quantity, safety stock
    holding_cost = 0.2 * (q/2 + ss) * 50  # 20% holding cost, $50 unit value
    ordering_cost = 1200 * (500 / q)       # $1200 order cost, 500 units/year
    return holding_cost + ordering_cost

def service_level_constraint(x):
    q, ss = x
    # Simplified: service level increases with safety stock
    sl = 1 - np.exp(-ss / 100)
    return sl - 0.95  # must be >= 0 (SL >= 95%)

constraints = [{'type': 'ineq', 'fun': service_level_constraint}]
bounds = [(50, 2000), (0, 500)]

result = minimize(total_cost, x0=[200, 100],
                  method='SLSQP',
                  constraints=constraints,
                  bounds=bounds)
print(f"Optimal order qty: {result.x[0]:.0f}")
print(f"Optimal safety stock: {result.x[1]:.0f}")
```

### 11.3 Economic Order Quantity (EOQ) — Analytical Optimization

EOQ minimizes total annual inventory cost:
Total cost = (D/Q) × S + (Q/2) × H

where D = annual demand, Q = order quantity, S = ordering cost, H = holding cost/unit.

dTC/dQ = -DS/Q² + H/2 = 0
→ Q* = √(2DS/H)  (EOQ formula)

Second derivative: d²TC/dQ² = 2DS/Q³ > 0 → confirmed minimum.

This is gradient descent solved analytically.

---

## 12. PYTHON CODE EXAMPLES

### 12.1 FFT Seasonality Analysis

```python
import numpy as np
import matplotlib.pyplot as plt

# 3 years of daily demand data
np.random.seed(42)
n_days = 365 * 3
t = np.arange(n_days)
demand = (1000 
          + 0.2*t                             # slight upward trend
          + 200*np.sin(2*np.pi*t/7)          # weekly cycle
          + 400*np.sin(2*np.pi*t/365.25)     # annual cycle
          + np.random.normal(0, 80, n_days))  # noise

# Detrend
p = np.polyfit(t, demand, 1)
detrended = demand - np.polyval(p, t)

# FFT
fft = np.fft.rfft(detrended)
freqs = np.fft.rfftfreq(n_days)  # cycles per day
power = np.abs(fft)**2

# Find top periods
top_k = np.argsort(power[1:10*365])[-8:][::-1] + 1
print("Dominant periods (days):")
for k in top_k:
    if freqs[k] > 0:
        print(f"  {1/freqs[k]:.1f} days (power={power[k]:.0f})")
```

### 12.2 Gradient Descent from Scratch

```python
import numpy as np

def gradient_descent(grad_fn, x0, learning_rate=0.01, n_iter=1000, tol=1e-6):
    """Generic gradient descent optimizer."""
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    
    for i in range(n_iter):
        g = grad_fn(x)
        x_new = x - learning_rate * g
        
        if np.linalg.norm(x_new - x) < tol:
            print(f"Converged at iteration {i+1}")
            break
        x = x_new
        history.append(x.copy())
    
    return x, np.array(history)

# Minimize f(x, y) = x^2 + 2y^2 - xy
def grad_f(x):
    gx = 2*x[0] - x[1]
    gy = 4*x[1] - x[0]
    return np.array([gx, gy])

x_opt, hist = gradient_descent(grad_f, x0=[5.0, 5.0], learning_rate=0.1)
print(f"Optimum: x={x_opt[0]:.4f}, y={x_opt[1]:.4f}")
```

### 12.3 Adam Optimizer

```python
import numpy as np

def adam(grad_fn, x0, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, n_iter=1000):
    """Adam optimizer implementation."""
    x = np.array(x0, dtype=float)
    m = np.zeros_like(x)  # first moment
    v = np.zeros_like(x)  # second moment
    
    for t in range(1, n_iter + 1):
        g = grad_fn(x)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        x -= lr * m_hat / (np.sqrt(v_hat) + eps)
    
    return x

x_opt = adam(grad_f, x0=[5.0, 5.0])
print(f"Adam optimum: {x_opt}")
```

---

## 13. QUICK REFERENCE

### FFT Key Facts

| Property               | Value / Formula                         |
|------------------------|-----------------------------------------|
| Complexity             | O(N log N)                              |
| Frequency resolution   | 1/(N × Δt)                              |
| Nyquist frequency      | 1/(2Δt)                                 |
| DC component           | X[0] = sum(x) = N × mean(x)            |
| Parseval's theorem     | sum(|x|²) = (1/N) sum(|X|²)            |
| Real signal symmetry   | X[N-k] = conj(X[k])                    |

### Optimization Algorithm Selection

| Algorithm    | Convergence | Per Step Cost | Best For                        |
|--------------|-------------|---------------|---------------------------------|
| GD (batch)   | O(1/T)      | O(N)          | Small datasets, convex          |
| SGD          | O(1/√T)     | O(1)          | Large datasets                  |
| Momentum SGD | O(1/T)      | O(1)          | Non-smooth landscapes           |
| Adam         | O(1/√T)     | O(d)          | Deep learning, sparse grads     |
| L-BFGS       | Superlinear  | O(d)          | Smooth, moderate scale          |
| Newton       | Quadratic   | O(d³)         | Small problems, near optimum    |

### Lagrange Multiplier Summary

| Situation               | Method         | Conditions                          |
|-------------------------|----------------|-------------------------------------|
| Equality constraints    | Lagrange       | ∇L = 0                              |
| Inequality constraints  | KKT            | Stationarity, feasibility, CS       |
| Linear objectives       | LP / Simplex   | Strong duality                      |
| Convex objectives       | Interior point | Global optimum guaranteed           |

### Key Python Libraries

| Library             | Purpose                                    |
|---------------------|--------------------------------------------|
| numpy.fft           | FFT, RFFT, IFFT                            |
| scipy.fft           | FFT with more control, backends            |
| scipy.signal        | Welch PSD, Savitzky-Golay, filters         |
| scipy.optimize      | minimize, minimize_scalar, root            |
| scipy.integrate     | solve_ivp (ODE solver)                     |
| torch.optim         | Adam, SGD, L-BFGS for deep learning        |
| statsmodels         | ARIMA (gradient-based MLE fitting)         |

---
*End of FOURIER_CALCULUS_KB.md*
*Sources: Bookdown (Peng "Time Series Analysis"), numberanalytics.com Fourier guide,*
*Wikipedia (Gradient Descent, Lagrange Multipliers), IBM Think (Gradient Descent),*
*scipy documentation, Hestenes & Stiefel (1952) conjugate gradient.*

---

## Knowledge Update — 2026-03-06

### Survey: Advanced Fourier-Type Integral Transforms
**Source:** scisimple.com summary of "A mathematical survey on Fourier type integral transforms and their offshoots" (Aug 2025)
**URL:** https://scisimple.com/en/articles/2025-08-26-understanding-fourier-transforms-in-signal-processing--ak4ql4w

Comprehensive taxonomy of transforms beyond the standard FFT:

| Transform | Key Property | Best Use Case |
|---|---|---|
| STFT (Windowed Fourier) | Fixed time-frequency resolution | Stationary or near-stationary signals |
| Wavelet Transform | Adaptive resolution (multiresolution) | Non-stationary signals; transients |
| Stockwell Transform (S-transform) | Phase-preserving STFT with frequency-dependent window | Power systems, seismic, biomedical |
| Wavelet Packet Transform | Full decomposition tree (not just low-frequency) | High-frequency fault signatures |

**Resolution tradeoff (Heisenberg-Gabor limit):** No transform escapes the fundamental uncertainty Δt · Δf ≥ 1/(4π). The choice of transform is about *where you allocate* the time-frequency resolution budget, not whether you can exceed it.

### S-Transform for Time-Frequency Analysis in Process Monitoring
**Source:** MDPI Sensors, Vol. 25(23):7318 — December 2025
**URL:** https://www.mdpi.com/1424-8220/25/23/7318

The **S-transform** provides adaptive resolution and phase information that STFT lacks:
- Frequency-dependent Gaussian window: wider window at low frequencies (more time averaging), narrower at high frequencies (better time resolution for fast transients)
- Demonstrated superior performance for partial discharge (PD) signal analysis in power systems vs. standard STFT
- Combined approach: wavelet packet + generalized morphological filters → frequency-domain analysis + noise suppression

**Supply chain relevance:** Vibration analysis for predictive maintenance. Equipment faults (bearing wear, imbalance, cavitation) produce characteristic frequency signatures. The S-transform's adaptive resolution is better suited to detecting these than standard FFT when fault frequencies are mixed with low-frequency process noise.

### Computational Fourier Analysis — 2025 State
**Source:** JAEAS (rjsaonline.org), November 2025

- Real-time Fourier analysis is now computationally feasible at IoT edge hardware scale (FPGA, microcontroller with DSP extensions)
- Large-signal processing (millions of samples) handled via blocked FFT and streaming computation frameworks
- Emerging applications: frequency-domain SPC (monitoring spectral shift as a process quality indicator), not just time-domain control charts

*Sources: scisimple.com (2025-08), MDPI Sensors 25(23):7318 (2025-12), rjsaonline.org JAEAS (2025-11)*

---

## Knowledge Update — 2026-03-07

### Real-Time Fourier Analysis at IoT Edge Scale (2025)
**Source:** JAEAS (rjsaonline.org) Vol. 1 No. 4 — November 2025; JAEAS article view/148

Key computational trend: FFT is no longer a batch, offline operation.

- **FPGA and DSP-extended microcontrollers** now execute FFT on streaming sensor data in real time (< 1ms latency for 1024-point FFT)
- **Blocked FFT and streaming frameworks** enable continuous spectral monitoring of signals longer than available memory
- **Applications emerging in industrial IoT:** frequency-domain process monitoring, where the shape of the power spectral density (PSD) is the process quality indicator — not time-domain mean/variance
- Connection to SPC: **spectral SPC** — control charts on FFT power at key frequencies, rather than (or in addition to) time-domain Shewhart/EWMA. A shift in spectral energy at a characteristic frequency (e.g., bearing defect frequency) triggers an alarm before the time-domain signal crosses limits

**Supply chain / maintenance relevance:** Vibration signatures for equipment health monitoring are now feasible on low-cost edge hardware without data offloading. The monitoring loop is: sensor → embedded FFT → spectral SPC → threshold alert → maintenance trigger. No cloud dependency required.

### Fourier Analysis Curriculum Anchor — JHU Engineering
**Source:** JHU Engineering Programs — January 2026

JHU 625.710 (Fourier Analysis with Applications) covers:
- Sampling theorem and aliasing — critical for IoT sensor design (ensure sample rate > 2× highest frequency of interest)
- Convolution theorems — time-domain convolution = frequency-domain multiplication; used for efficient filter design
- Orthogonal function theory — Fourier series as a special case of orthogonal decomposition; connects to wavelet theory and non-Fourier basis sets (Legendre, Chebyshev polynomials)
- Spectral analysis — power spectral density estimation, windowing effects (Hann, Hamming windows to reduce spectral leakage)

*Sources: rjsaonline.org JAEAS Vol.1 No.4 (2025-11), JHU EP Online 625.710 (2026-01)*

---

## Knowledge Update — 2026-03-08

### Fourier Analysis Networks (FAN): Deep Learning Integration (arXiv, December 2025)
**Source:** arXiv:2512.14873 — December 2025 (39 citations as of Dec 2025)
**URL:** https://arxiv.org/html/2512.14873

FAN (Fourier Analysis Network) integrates Fourier components directly into neural network activation functions, enabling neural networks to learn periodic and quasi-periodic patterns without preprocessing:

- **Mechanism:** FAN uses a dual-activation layer: Fourier basis functions (sin/cos at learned frequencies) combined with nonlinear activation (GELU or ReLU). Network learns both frequency and amplitude of periodic components end-to-end
- **CFAN extension (Jeong et al., 2025):** Convolutional Fourier Analysis Network — extends FAN to convolutional architectures for spatial/image data with periodic texture
- **Performance:** Multiple follow-up studies report consistent improvements in time series tasks with periodic structure (seasonal demand, vibration monitoring, power signals)
- **39 citations within ~3 months** — indicates rapid adoption in the research community

**Supply chain / predictive maintenance relevance:** For demand time series with strong seasonal patterns (weekly, monthly, annual cycles), FAN-based models can outperform standard LSTM/Transformer because the Fourier basis explicitly parameterizes periodicity rather than learning it implicitly from long sequences.

### Adaptive Fourier Series for Equipment Failure Prediction (Scientific Reports, 2025)
**Source:** Nature/Scientific Reports s41598-025-24497-4 — November 19, 2025
**URL:** https://www.nature.com/articles/s41598-025-24497-4

Comparative study of deep learning vs. Fourier series models for predictive maintenance:

- **Finding:** Adaptive Fourier series enhances prediction power of both ARIMA and ANN models for equipment failure prediction
- **Adaptive Fourier series:** Fit a Fourier series to residuals of a baseline model; adaptive means the number of harmonics and their frequencies are selected by AIC/BIC rather than fixed a priori
- **Hybrid workflow:**
  1. ARIMA or exponential smoothing for trend/level
  2. Fourier series on residuals for cyclical components
  3. ANN for remaining non-linear residuals
  Result: each component handles what it's structurally suited for; Fourier handles the periodic, ANN handles the nonlinear aperiodic

**Practical implication:** When equipment failure patterns have cyclical signatures (maintenance intervals, seasonal load variation), adding adaptive Fourier features to a deep learning model is a disciplined improvement — not overfitting, because the frequency selection is penalized.

### Real-Time FFT on Edge Hardware: Spectral SPC (2025-2026 Trend)
**Source:** MDPI Sensors 25/23/7318 (December 2025); rjsaonline.org JAEAS (November 2025)

Confirmation of the trend identified 2026-03-07 (streaming FFT on embedded hardware) with additional detail:

- **DWT + HHT hybrid:** Discrete Wavelet Transform (DWT) for initial denoising → Hilbert-Huang Transform (HHT) for deep feature extraction in partial discharge signal analysis. DWT removes broadband noise; HHT extracts instantaneous frequency (non-stationary signal, no Fourier stationarity assumption required)
- **HHT vs. FFT:** HHT is adaptive — it decomposes signals into intrinsic mode functions (IMFs) without a fixed basis. Better for non-stationary processes (machine aging, load transients). FFT assumes stationarity.
- **When to use which:**
  - FFT: stationary signals, frequency content stable over time (rotating machinery at steady state, periodic demand signals)
  - DWT: multi-scale transient detection (shocks, ramps)
  - HHT: non-stationary, nonlinear signals (degradation curves, wear signals)

*Sources: arXiv:2512.14873 (2025-12), Nature s41598-025-24497-4 (2025-11), MDPI Sensors 25/23/7318 (2025-12), JAEAS Vol.1 No.4 (2025-11)*

---

## [2026-03-09 Update] Frequency Transforms in Time Series — Comprehensive Survey (arXiv 2504.07099)

### Beyond the Time Domain: Fourier, Laplace, and Wavelet in Modern Time Series Analysis
**Source:** Yang et al. (HKU, UCLA, UMD, Aalborg, Westlake, UQ, Microsoft), arXiv:2504.07099v2 (April 2025, updated)

First comprehensive survey specifically covering Fourier, Laplace, and Wavelet transforms in deep-learning-era time series analysis:

**Key findings from the survey:**

- **Frequency-based representations significantly enhance feature separability:** Low-frequency components (trends, seasonals) cleanly isolated from high-frequency details (noise, anomalies) — impossible to do cleanly in time domain alone
- **Fourier Neural Operators (FNOs):** New class of architectures that learn operators in frequency space. Outperform convolutional approaches on PDE-governed physical systems and show strong performance on long-horizon time series forecasting
- **Wavelet-based CNNs:** Wavelet decomposition as a preprocessing stage before CNN — captures multi-resolution features simultaneously (trend at coarse scale + transient at fine scale)
- **Laplace transform in ML:** Re-emerging for systems with exponential decay dynamics (chemical processes, inventory depletion, supply chain response to demand shocks)

**Application domains covered:** Finance, molecular dynamics, weather forecasting (relevant: supply chain demand signals with weather correlation)

**The practical taxonomy from the survey:**

| Transform | Best for | Limitation |
|-----------|----------|-----------|
| FFT | Stationary periodic signals | Assumes stationarity |
| Wavelet (DWT/CWT) | Multi-scale transients, non-stationary | Basis choice is critical |
| Laplace | Exponential decay / growth dynamics | Less interpretable spectrum |
| FNO | Learning entire operators on gridded data | Computationally heavier |

**Supply chain implication:** Demand signals often have mixed character (periodic seasonals + non-stationary trend + sporadic spikes). Hybrid frequency-domain preprocessing before ARIMA or ML forecasting models is now well-validated.

*Source: arXiv:2504.07099v2 (2025-04/2025-07 revision); GitHub: curated repository for reproducibility*

---

## [2026-03-09 Update] Fourier Basis Mapping for Time Series Forecasting (arXiv 2507.09445)

**Source:** arXiv:2507.09445v1 (July 2025)

- **Method:** Reinterprets the Fourier transform from a basis-functions perspective: real/imaginary parts of frequency components are cosine/sine basis coefficients
- **Fourier Basis Mapping (FBM):** Maps time series into Fourier coefficient space, applies a learned linear or nonlinear transformation, then inverts back to time domain
- **Benefit:** Separates the "what frequencies exist" (Fourier) from "how those frequencies evolve over the forecast horizon" (learned mapping) — cleaner than end-to-end time-domain forecasters
- **Reported improvement:** Strong results on standard benchmarks (ETT, Weather, Traffic datasets) vs. transformer-based baselines

**Practical note:** FBM is essentially a principled version of seasonal decomposition — instead of estimating a fixed seasonal pattern, it learns the frequency-domain transformation. This is the right approach when seasonal patterns shift over time (e.g., post-COVID demand patterns).

*Source: arXiv:2507.09445v1*

---

## [2026-03-09 Update] Deep Learning + Classical Fourier Hybrid (arXiv 2601.00427)

**Source:** arXiv:2601.00427 (January 2026)

- **Problem:** Multi-frequency inverse source problem (recovering source from far-field measurements) — Helmholtz equation governing wave propagation
- **Method:** Hybrid framework: classical Fourier method for the well-posed low-frequency components + deep CNN for the ill-posed high-frequency components
- **Principle that generalizes:** When a problem has components that are well-understood analytically (and where Fourier methods excel) AND components that are data-driven (where ML excels), hybrid architectures outperform either alone
- **Supply chain analogy:** Use FFT for the deterministic seasonal + trend components of demand; use ML for the residual driven by unstructured external factors. This hybrid is now theoretically validated in hard inverse problems.

*Source: arXiv:2601.00427 (2026-01)*
