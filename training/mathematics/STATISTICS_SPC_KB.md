# STATISTICS & STATISTICAL PROCESS CONTROL — Knowledge Base
# Agent: Pythagoras | Domain: Mathematics & Analytics
# Last updated: 2026-03-03 | Sources: ASQ, Wikipedia, Six Sigma Study Guide, 1Factory, NIST

---

## Pre-flight Checklist

Before selecting a statistical method or running analysis, answer these 5 questions:

1. **What type of data?** Continuous, ordinal, categorical, binary, count data?
2. **What is the sample size?** n < 30 triggers non-parametric or Bayesian considerations
3. **What distributional assumptions apply?** Normality? Independence? Homoscedasticity?
4. **What decision follows from this analysis?** If unclear, clarify scope before proceeding
5. **What is the acceptable error rate?** Alpha level, confidence interval width, Type I vs Type II tradeoff?

> Choosing the wrong method because assumptions weren't checked is correctable — but expensive.

---


## 1. STATISTICAL PROCESS CONTROL (SPC) — FOUNDATIONS

### 1.1 Overview and Purpose

Statistical Process Control (SPC) is a method of quality control that uses statistical methods to monitor and control a process. The goal is to ensure the process operates at its full potential to produce conforming product. SPC was pioneered by Walter A. Shewhart at Bell Labs in the 1920s and later championed by W. Edwards Deming.

**Core Distinction:**
- **Common cause variation** (also: chance, natural, random): Inherent to the process; always present; the process is "in control" but naturally varies. Reducing it requires changing the process itself.
- **Special cause variation** (also: assignable cause): Due to identifiable external factors (machine malfunction, wrong raw material, operator error). Signals process is "out of control."

**SPC Philosophy:**
- A process in statistical control is predictable.
- Reacting to common-cause variation as if it were special cause (tampering) increases total variation.
- Only special causes warrant investigation and correction.

Sources: Wikipedia (Control chart); Shewhart (1931) "Economic Control of Quality of Manufactured Product"

### 1.2 Common- vs. Special-Cause Decision Rules

| Signal Type | Action |
|-------------|--------|
| Common cause | Leave process alone; improve process if necessary |
| Special cause | Investigate, identify root cause, eliminate if harmful |

**Funnel Experiment (Deming):** Moving a funnel to compensate for each drop's error increases spread. Demonstrates that tampering with a stable process increases variability.

---

## 2. CONTROL CHARTS

### 2.1 Anatomy of a Control Chart

Every Shewhart control chart has:
1. **Center Line (CL):** Process mean or target
2. **Upper Control Limit (UCL):** CL + 3*sigma
3. **Lower Control Limit (LCL):** CL - 3*sigma
4. **Data points** plotted over time

Control limits are set at +/-3 standard deviations of the plotted statistic. This means ~99.73% of points from a normal, in-control process fall within the limits. A point outside is a signal (false alarm rate ~0.27%).

**Control limits != Specification limits.** Control limits come from the process; specification limits come from customers or engineering.

### 2.2 X-bar and R Chart (Variables Data — Subgroups)

Used when measurements are continuous and collected in rational subgroups of size n (typically 2-10).

**X-bar Chart (Subgroup Means):**
```
X-double-bar = Grand mean of all subgroup means
UCL_xbar = X-double-bar + A2 * R-bar
LCL_xbar = X-double-bar - A2 * R-bar
```

**R Chart (Subgroup Ranges):**
```
R-bar = Average range across all subgroups
UCL_R = D4 * R-bar
LCL_R = D3 * R-bar
```

Control chart constants (A2, D3, D4) depend on subgroup size n:

| n  | A2    | D3    | D4    |
|----|-------|-------|-------|
| 2  | 1.880 | 0     | 3.267 |
| 3  | 1.023 | 0     | 2.574 |
| 4  | 0.729 | 0     | 2.282 |
| 5  | 0.577 | 0     | 2.114 |
| 10 | 0.308 | 0.223 | 1.777 |

**When to use:** Subgroup size 2-10; monitoring mean and spread simultaneously.

**Pitfall:** Must verify R chart is in control before interpreting X-bar chart.

### 2.3 X-bar and S Chart (Variables Data — Larger Subgroups)

For subgroup sizes n > 10, use S (standard deviation) instead of R.

```
UCL_S = B4 * S-bar
LCL_S = B3 * S-bar
UCL_xbar = X-double-bar + A3 * S-bar
LCL_xbar = X-double-bar - A3 * S-bar
```

### 2.4 Individuals and Moving Range (I-MR / XmR) Chart

Used when subgroups of size 1 are collected (one measurement per time period). Common in chemical processes, batch production, slow processes.

```
Moving Range: MR_i = |X_i - X_{i-1}|
MR-bar = average of all moving ranges
sigma_estimate = MR-bar / d2   (d2 = 1.128 for n=2)

UCL_X = X-bar + 3 * MR-bar / d2 = X-bar + 2.66 * MR-bar
LCL_X = X-bar - 2.66 * MR-bar

UCL_MR = D4 * MR-bar = 3.267 * MR-bar
LCL_MR = 0 (by convention)
```

**Pitfall:** I-MR assumes approximately normal individual observations.

### 2.5 p Chart (Proportion Nonconforming — Attribute Data)

Used when data is the fraction defective from samples of varying size.

```
p-bar = total defectives / total inspected
sigma_p_i = sqrt(p-bar * (1 - p-bar) / n_i)

UCL_p = p-bar + 3 * sigma_p_i
LCL_p = p-bar - 3 * sigma_p_i
```

Note: Control limits vary with sample size n_i. For equal sample sizes, limits are constant.

**Pitfall:** Requires n large enough that both n*p-bar and n*(1-p-bar) > 5.

### 2.6 np Chart (Number Nonconforming)

Used when sample size n is constant. Tracks count, not proportion.

```
np-bar = n * p-bar
UCL_np = np-bar + 3 * sqrt(np-bar * (1 - p-bar))
LCL_np = np-bar - 3 * sqrt(np-bar * (1 - p-bar))
```

### 2.7 c Chart (Count of Defects per Unit — Constant Area)

Used when counting defects and the inspection area is constant. Assumes Poisson distribution.

```
c-bar = average count of defects per inspection unit
UCL_c = c-bar + 3 * sqrt(c-bar)
LCL_c = c-bar - 3 * sqrt(c-bar)
```

### 2.8 u Chart (Defects per Unit — Variable Area)

Used when the inspection area varies.

```
u_i = c_i / n_i     (defects per unit for sample i)
u-bar = total defects / total units inspected

UCL_u = u-bar + 3 * sqrt(u-bar / n_i)
LCL_u = u-bar - 3 * sqrt(u-bar / n_i)
```

### 2.9 CUSUM Chart (Cumulative Sum)

CUSUM accumulates deviations from target, making it more sensitive to small sustained shifts (0.5-2 sigma) than Shewhart charts.

**Two-sided CUSUM:**
```
C+_i = max(0, C+_{i-1} + (X_i - mu_0 - k))   # Upper CUSUM
C-_i = max(0, C-_{i-1} - (X_i - mu_0 + k))   # Lower CUSUM
```
Where:
- mu_0 = target mean
- k = reference value (allowable slack), typically k = delta/2 where delta = shift to detect in sigma units
- H = decision interval (threshold), typically H = 4 or 5 sigma units

**Signal:** C+_i > H or C-_i > H

**Advantage:** ARL to detect 1-sigma shift ~10 vs 43 for Shewhart.

**Pitfall:** Harder to interpret than Shewhart; needs careful k and H selection.

### 2.10 EWMA Chart (Exponentially Weighted Moving Average)

Also sensitive to small shifts. Weights recent observations more heavily.

```
Z_i = lambda * X_i + (1 - lambda) * Z_{i-1}
sigma_Z = sigma * sqrt(lambda / (2 - lambda))   (steady state)

UCL = mu_0 + L * sigma_Z
LCL = mu_0 - L * sigma_Z
```
Where:
- lambda = smoothing parameter, 0 < lambda <= 1 (typically 0.1-0.25 for small shift detection)
- L = control limit width (typically L = 3)

**Advantage:** Smooth, less affected by outliers; good for autocorrelated data.

### 2.11 Selecting the Right Control Chart

```
Data Type?
|-- Variables (continuous)
|   |-- Subgroup n=1 --> I-MR (XmR)
|   |-- Subgroup n=2-10 --> X-bar R
|   +-- Subgroup n>10 --> X-bar S
+-- Attributes (discrete)
    |-- Defectives (pass/fail)
    |   |-- Variable n --> p chart
    |   +-- Constant n --> np chart
    +-- Defects (count)
        |-- Constant area --> c chart
        +-- Variable area --> u chart
```

---

## 3. WESTERN ELECTRIC RULES

Western Electric Handbook (1956) defined 8 run rules to detect non-random patterns, even when all points remain within control limits.

### 3.1 Zone Definitions

- Zone A: Between 2-sigma and 3-sigma from centerline
- Zone B: Between 1-sigma and 2-sigma from centerline
- Zone C: Within 1-sigma of centerline

### 3.2 The Eight Rules

| Rule | Signal Condition |
|------|-----------------|
| 1 | 1 point beyond Zone A (outside +/-3-sigma) |
| 2 | 2 of 3 consecutive points in Zone A or beyond (same side) |
| 3 | 4 of 5 consecutive points in Zone B or beyond (same side) |
| 4 | 8 consecutive points on one side of centerline |
| 5 | 6 consecutive points steadily increasing or decreasing (trend) |
| 6 | 15 consecutive points in Zone C (above and below CL) — hugging |
| 7 | 14 consecutive points alternating up and down |
| 8 | 8 consecutive points on both sides, none in Zone C — mixture |

### 3.3 Interpretation

- **Rule 1:** Classic out-of-control signal; special cause
- **Rule 4 (run of 8):** Process mean has shifted
- **Rule 5 (trend):** Gradual process drift (tool wear, temperature drift)
- **Rule 6 (hugging):** Possible stratification; subgroups contain mixed populations
- **Rule 7 (alternating):** Systematic pattern; possibly two alternating processes
- **Rule 8 (mixture):** Two different processes mixed in data

### 3.4 Nelson Rules

Nelson (1984) published a similar but slightly different set. Most software (Minitab, JMP) implements both.

**Pitfall:** Applying all 8 rules increases false alarm rate substantially. Consider using only Rules 1-4 for general use.

### 3.5 Python SPC Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

def build_xbar_r_chart(data, subgroup_size=5):
    """Build X-bar and R control charts from data."""
    data = np.array(data)
    n = len(data) // subgroup_size
    subgroups = data[:n * subgroup_size].reshape(n, subgroup_size)
    
    means = subgroups.mean(axis=1)
    ranges = subgroups.ptp(axis=1)
    
    x_bar = means.mean()
    r_bar = ranges.mean()
    
    # Control chart constants
    A2 = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419,
          8: 0.373, 9: 0.337, 10: 0.308}
    D3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
    D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924,
          8: 1.864, 9: 1.816, 10: 1.777}
    
    k = subgroup_size
    ucl_x = x_bar + A2[k] * r_bar
    lcl_x = x_bar - A2[k] * r_bar
    ucl_r = D4[k] * r_bar
    lcl_r = D3[k] * r_bar
    
    return {
        'means': means, 'ranges': ranges,
        'x_bar': x_bar, 'r_bar': r_bar,
        'ucl_x': ucl_x, 'lcl_x': lcl_x,
        'ucl_r': ucl_r, 'lcl_r': lcl_r,
    }

def check_western_electric_rules(values, cl, ucl, lcl):
    """Check Western Electric rules 1-4 on a series of chart values."""
    sigma = (ucl - cl) / 3
    signals = []
    n = len(values)
    
    for i in range(n):
        v = values[i]
        # Rule 1: Beyond 3-sigma
        if v > ucl or v < lcl:
            signals.append((i, 'Rule 1: Beyond 3-sigma'))
        
        # Rule 4: 8 consecutive on one side
        if i >= 7:
            window = values[i-7:i+1]
            if all(w > cl for w in window) or all(w < cl for w in window):
                signals.append((i, 'Rule 4: 8 points one side'))
        
        # Rule 2: 2 of 3 in Zone A (same side)
        if i >= 2:
            window = values[i-2:i+1]
            above_A = sum(1 for w in window if w > cl + 2*sigma)
            below_A = sum(1 for w in window if w < cl - 2*sigma)
            if above_A >= 2 or below_A >= 2:
                signals.append((i, 'Rule 2: 2 of 3 in Zone A'))
        
        # Rule 3: 4 of 5 in Zone B or beyond (same side)
        if i >= 4:
            window = values[i-4:i+1]
            above_B = sum(1 for w in window if w > cl + sigma)
            below_B = sum(1 for w in window if w < cl - sigma)
            if above_B >= 4 or below_B >= 4:
                signals.append((i, 'Rule 3: 4 of 5 in Zone B+'))
    
    return signals

# Example usage
np.random.seed(42)
process_data = np.random.normal(10, 0.5, 150)
# Inject a shift at observation 100
process_data[100:] += 1.0

chart = build_xbar_r_chart(process_data, subgroup_size=5)
signals = check_western_electric_rules(
    chart['means'], chart['x_bar'], chart['ucl_x'], chart['lcl_x']
)
print(f"Signals detected: {len(signals)}")
for s in signals[:5]:
    print(f"  Subgroup {s[0]}: {s[1]}")
```

---

## 4. PROCESS CAPABILITY

### 4.1 Concepts

Process capability measures how well a process fits within specification limits. Assumes:
1. Process is in statistical control
2. Data is approximately normally distributed

**Specification limits (from customer/engineering):**
- USL = Upper Specification Limit
- LSL = Lower Specification Limit

### 4.2 Cp (Capability Ratio — Potential)

```
Cp = (USL - LSL) / (6 * sigma)
```

Where sigma = process standard deviation estimated from control chart (sigma = R-bar / d2).

Cp measures **spread** only — ignores centering.

| Cp value | Interpretation |
|----------|----------------|
| < 1.0 | Process wider than spec; producing defects |
| = 1.0 | Process exactly fits spec (0.27% defects) |
| = 1.33 | Minimum acceptable (automotive, medical) |
| = 1.67 | Target for critical characteristics |
| = 2.0 | Six Sigma target (0.0018 ppm centered) |

### 4.3 Cpk (Capability Index — Actual)

Cpk adjusts for process centering.

```
CPU = (USL - mu) / (3 * sigma)   # upper capability
CPL = (mu - LSL) / (3 * sigma)  # lower capability
Cpk = min(CPU, CPL)
```

**Relationship:**
- Cpk <= Cp always
- Cpk = Cp when process is perfectly centered
- Large gap between Cp and Cpk indicates centering problem

### 4.4 Pp and Ppk (Performance Indices)

Pp and Ppk use the overall sample standard deviation (long-term).

```
Pp = (USL - LSL) / (6 * s_overall)
Ppk = min[(USL - x-bar) / (3 * s_overall), (x-bar - LSL) / (3 * s_overall)]
```

**Distinction:**
- Cp/Cpk = short-term, within-subgroup variation (potential)
- Pp/Ppk = long-term, overall variation (actual performance)
- Cp > Pp indicates significant between-subgroup variation

### 4.5 Sigma Level and DPMO

| Cpk  | Sigma Level | DPMO (with 1.5-sigma shift) |
|------|-------------|------------------------------|
| 0.33 | 1           | 697,700                      |
| 0.67 | 2           | 308,537                      |
| 1.00 | 3           | 66,807                       |
| 1.33 | 4           | 6,210                        |
| 1.67 | 5           | 233                          |
| 2.00 | 6           | 3.4                          |

### 4.6 Python Implementation

```python
import numpy as np
from scipy import stats

def process_capability(data, USL, LSL, subgroup_size=5):
    data = np.array(data)
    n = len(data)
    mu = np.mean(data)
    s_overall = np.std(data, ddof=1)
    
    # Pp and Ppk (overall performance)
    Pp = (USL - LSL) / (6 * s_overall)
    Ppk = min((USL - mu) / (3 * s_overall), (mu - LSL) / (3 * s_overall))
    
    # Within-subgroup sigma estimate for Cp/Cpk
    n_subgroups = n // subgroup_size
    subgroups = data[:n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
    R_bar = np.mean(np.ptp(subgroups, axis=1))
    d2_table = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534,
                7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}
    d2 = d2_table.get(subgroup_size, 2.326)
    sigma_within = R_bar / d2
    
    Cp = (USL - LSL) / (6 * sigma_within)
    Cpk = min((USL - mu) / (3 * sigma_within), (mu - LSL) / (3 * sigma_within))
    
    return {
        'mean': mu,
        'std_overall': s_overall,
        'sigma_within': sigma_within,
        'Pp': round(Pp, 3),
        'Ppk': round(Ppk, 3),
        'Cp': round(Cp, 3),
        'Cpk': round(Cpk, 3),
        'sigma_level': round(Cpk * 3, 2),
        'ppm_theoretical': round(stats.norm.sf(3 * Cpk) * 1e6 * 2, 2)
    }

# Example
np.random.seed(42)
data = np.random.normal(loc=10.05, scale=0.15, size=100)
results = process_capability(data, USL=10.5, LSL=9.5, subgroup_size=5)
for k, v in results.items():
    print(f"{k:25s}: {v}")
```

---

## 5. MEASUREMENT SYSTEM ANALYSIS (MSA) — GAGE R&R

### 5.1 Purpose

Before trusting control chart data, validate the measurement system. Gage R&R quantifies measurement system error.

**Total Variation = Part Variation + Measurement System Variation**

**Measurement System Variation components:**
- **Repeatability (Equipment Variation, EV):** Same appraiser, same part, same gage — multiple readings. "Within-appraiser variation."
- **Reproducibility (Appraiser Variation, AV):** Different appraisers measuring same part. "Between-appraiser variation."

```
GRR = sqrt(EV^2 + AV^2)
```

### 5.2 Acceptance Criteria

```
%GRR = (GRR / Total Variation) * 100
   OR
%GRR = (GRR / Tolerance) * 100    (tolerance = USL - LSL)
```

| %GRR | Decision |
|------|----------|
| < 10% | Acceptable measurement system |
| 10-30% | May be acceptable depending on application |
| > 30% | Unacceptable; measurement system must be improved |

**Number of Distinct Categories (ndc):**
```
ndc = 1.41 * (Part Variation / GRR)
```
ndc >= 5 required for adequate discrimination.

### 5.3 ANOVA Method vs. Average and Range Method

**Average & Range Method:** Simpler; separates EV and AV but cannot separate interaction.
**ANOVA Method:** More powerful; can quantify Part x Appraiser interaction. Preferred in automotive (AIAG MSA Manual).

### 5.4 Bias, Linearity, Stability

- **Bias:** Difference between measurement average and reference (true) value. Systematic error.
- **Linearity:** Consistency of bias across measurement range. Plot bias vs. reference value; should be flat.
- **Stability:** Consistency of measurement over time. Monitor with control chart of repeated standard measurements.

### 5.5 Python Gage R&R

```python
import pandas as pd
import numpy as np

def gage_rr_avg_range(df, part_col='Part', appraiser_col='Appraiser',
                       measure_col='Measurement', trials=2, tolerance=None):
    """Basic Gage R&R using Average and Range method."""
    appraisers = df[appraiser_col].unique()
    parts = df[part_col].unique()
    n_appraisers = len(appraisers)
    n_parts = len(parts)
    
    # Range per part per appraiser
    ranges = df.groupby([part_col, appraiser_col])[measure_col].apply(
        lambda x: x.max() - x.min()
    )
    R_bar = ranges.mean()
    
    d2_table = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326}
    d2 = d2_table.get(trials, 1.128)
    EV = R_bar / d2  # Repeatability
    
    # Reproducibility
    appraiser_means = df.groupby(appraiser_col)[measure_col].mean()
    R_appraisers = appraiser_means.max() - appraiser_means.min()
    d2_a = d2_table.get(n_appraisers, 1.693)
    AV_raw = R_appraisers / d2_a
    AV = np.sqrt(max(AV_raw**2 - EV**2 / (n_parts * trials), 0))
    
    GRR = np.sqrt(EV**2 + AV**2)
    
    # Part variation
    part_means = df.groupby(part_col)[measure_col].mean()
    R_parts = part_means.max() - part_means.min()
    d2_p = d2_table.get(n_parts, 2.326)
    PV = R_parts / d2_p
    
    TV = np.sqrt(GRR**2 + PV**2)
    
    result = {
        'Repeatability (EV)': round(EV, 4),
        'Reproducibility (AV)': round(AV, 4),
        'GRR': round(GRR, 4),
        'Part Variation (PV)': round(PV, 4),
        'Total Variation (TV)': round(TV, 4),
        '%GRR (of TV)': round(GRR / TV * 100, 1),
        'ndc': int(1.41 * PV / GRR) if GRR > 0 else 'inf',
    }
    if tolerance:
        result['%GRR (of tolerance)'] = round(GRR / tolerance * 100, 1)
    return result
```

---

## 6. REGRESSION ANALYSIS

### 6.1 Simple Linear Regression

**Model:** Y = beta_0 + beta_1 * X + epsilon

Where:
- Y = response (dependent variable)
- X = predictor (independent variable)
- beta_0 = intercept
- beta_1 = slope
- epsilon ~ N(0, sigma^2) = error term

**Ordinary Least Squares (OLS) Estimates:**
```
beta_1 = Sum[(Xi - X-bar)(Yi - Y-bar)] / Sum[(Xi - X-bar)^2]
       = Sxy / Sxx

beta_0 = Y-bar - beta_1 * X-bar
```

**Key Metrics:**
```
SST = Sum(Yi - Y-bar)^2              # Total sum of squares
SSR = Sum(Y-hat_i - Y-bar)^2         # Regression sum of squares
SSE = Sum(Yi - Y-hat_i)^2            # Error sum of squares

R^2 = SSR / SST = 1 - SSE / SST     # Coefficient of determination
Adj-R^2 = 1 - (SSE/(n-p-1)) / (SST/(n-1))   # p = number of predictors
RMSE = sqrt(SSE / (n-2))             # Root mean square error
```

### 6.2 Multiple Linear Regression

**Model:** Y = beta_0 + beta_1*X1 + beta_2*X2 + ... + beta_p*Xp + epsilon

In matrix form: Y = X*beta + epsilon

**OLS Solution:** beta = (X'X)^(-1) * X'Y

**Assumptions (LINE):**
1. **L**inearity: Relationship is linear
2. **I**ndependence: Errors are independent
3. **N**ormality: Errors are normally distributed
4. **E**qual variance (Homoscedasticity): Constant error variance

**Diagnostics:**
- Residual vs. fitted plot (check linearity, homoscedasticity)
- Q-Q plot of residuals (check normality)
- Cook's distance (check influential points — Cook's D > 4/n is a flag)
- VIF (Variance Inflation Factor) — check multicollinearity; VIF > 10 problematic

**Supply Chain Applications:**
- Predict freight cost from weight, distance, carrier type
- Predict demand from promotions, price, seasonality
- Model lead time from order size, supplier, time of year

### 6.3 Logistic Regression

Used when Y is binary (0/1). Models probability of outcome.

**Model:**
```
log(p / (1-p)) = beta_0 + beta_1*X1 + ... + beta_p*Xp
p = 1 / (1 + exp(-(beta_0 + beta_1*X1 + ... + beta_p*Xp)))
```

**Interpretation:** A one-unit increase in Xi multiplies the odds by exp(beta_i).

**Supply Chain Applications:**
- Predict late delivery (yes/no) from carrier, distance, order size
- Predict stockout occurrence
- Classify supplier risk (high/low)

### 6.4 Python Regression

```python
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# --- OLS with statsmodels (preferred for inference and p-values) ---
np.random.seed(42)
n = 200
weight = np.random.uniform(10, 100, n)
distance = np.random.uniform(100, 2000, n)
cost = 50 + 1.2*weight + 0.08*distance + np.random.normal(0, 20, n)

X = sm.add_constant(np.column_stack([weight, distance]))
model = sm.OLS(cost, X).fit()
print(model.summary())
# Key outputs: coefficients, p-values, R^2, F-statistic

# Confidence intervals for coefficients
print(model.conf_int(alpha=0.05))

# --- sklearn for prediction pipelines ---
X_arr = np.column_stack([weight, distance])
X_train, X_test, y_train, y_test = train_test_split(
    X_arr, cost, test_size=0.2, random_state=42
)
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print(f"R^2:  {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"MAE:  {np.mean(np.abs(y_test - y_pred)):.2f}")

# --- Diagnostic plots ---
import matplotlib.pyplot as plt
residuals = cost - model.fittedvalues
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Residuals vs fitted
axes[0].scatter(model.fittedvalues, residuals, alpha=0.5)
axes[0].axhline(0, color='red', linestyle='--')
axes[0].set_xlabel('Fitted Values')
axes[0].set_ylabel('Residuals')
axes[0].set_title('Residuals vs Fitted')

# Q-Q plot
from scipy import stats
stats.probplot(residuals, plot=axes[1])
axes[1].set_title('Normal Q-Q Plot')
plt.tight_layout()
plt.savefig('regression_diagnostics.png')
```

---

## 7. HYPOTHESIS TESTING

### 7.1 Framework

1. State H0 (null hypothesis) and Ha (alternative hypothesis)
2. Choose significance level alpha (typically 0.05)
3. Select appropriate test statistic
4. Compute p-value
5. Decision: Reject H0 if p-value < alpha

**Type I Error (alpha):** Rejecting a true H0 (false positive)
**Type II Error (beta):** Failing to reject a false H0 (false negative)
**Power = 1 - beta:** Probability of correctly rejecting false H0

### 7.2 Common Tests

**One-sample t-test:** Test if mean equals a specified value
```
t = (X-bar - mu_0) / (s / sqrt(n))
df = n - 1
```

**Two-sample t-test (independent):** Test if two means are equal
```
t = (X1-bar - X2-bar) / sqrt(sp^2 * (1/n1 + 1/n2))
sp^2 = ((n1-1)*s1^2 + (n2-1)*s2^2) / (n1 + n2 - 2)
df = n1 + n2 - 2
```

**Paired t-test:** Differences before/after within same subject
```
d_i = X1_i - X2_i
t = d-bar / (sd / sqrt(n))
df = n - 1
```

**F-test for variances:**
```
F = s1^2 / s2^2
df1 = n1 - 1, df2 = n2 - 1
```

**Chi-square test for independence:**
```
chi^2 = Sum[(Observed - Expected)^2 / Expected]
df = (rows - 1) * (cols - 1)
```

### 7.3 Confidence Intervals

**95% CI for mean:**
```
X-bar +/- t(alpha/2, n-1) * s / sqrt(n)
```

**95% CI for proportion:**
```
p-hat +/- z(alpha/2) * sqrt(p-hat*(1-p-hat)/n)
```

**95% CI for Cpk (approximate):**
```
Cpk +/- z(alpha/2) * sqrt(1/(9*n*Cpk) + 1/(2*(n-1)))
```

### 7.4 Sample Size Calculation

For detecting a mean shift of delta with power 1-beta:
```
n ~= (z_alpha + z_beta)^2 * sigma^2 / delta^2
```

```python
from scipy import stats
import numpy as np

# One-sample t-test
data = [23.1, 24.2, 22.8, 23.5, 24.0, 23.7]
t_stat, p_value = stats.ttest_1samp(data, popmean=23.0)
print(f"t={t_stat:.4f}, p={p_value:.4f}")

# Two-sample t-test
group1 = np.random.normal(10, 2, 30)
group2 = np.random.normal(11, 2, 35)
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"t={t_stat:.4f}, p={p_value:.4f}")

# Sample size using statsmodels
from statsmodels.stats.power import TTestIndPower
analysis = TTestIndPower()
# effect_size = delta / sigma (Cohen's d)
n = analysis.solve_power(effect_size=0.5, power=0.8, alpha=0.05)
print(f"Required n per group: {n:.0f}")

# Proportion test sample size
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower
es = proportion_effectsize(0.10, 0.15)  # detect shift from 10% to 15%
n_prop = NormalIndPower().solve_power(effect_size=es, power=0.8, alpha=0.05)
print(f"Required n for proportion test: {n_prop:.0f}")
```

---

## 8. ANALYSIS OF VARIANCE (ANOVA)

### 8.1 One-Way ANOVA

Tests if means of k groups are equal.

**H0:** mu_1 = mu_2 = ... = mu_k
**Ha:** At least one pair differs

```
SST = Sum_i Sum_j (Yij - Y-double-bar)^2
SSB = Sum_i ni * (Yi-bar - Y-double-bar)^2    # Between groups
SSW = SST - SSB                                # Within groups (error)

F = (SSB / (k-1)) / (SSW / (N-k))
```

**Reject H0 if F > F_critical(k-1, N-k, alpha)**

**Post-hoc tests after significant ANOVA:**
- Tukey HSD: Controls family-wise error rate
- Bonferroni: Conservative; adjusts alpha by number of comparisons
- Scheffe: Most conservative; appropriate for all possible contrasts

### 8.2 Two-Way ANOVA

Tests effects of two factors and their interaction.

```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Two-way ANOVA example
data = pd.DataFrame({
    'yield': [85, 87, 88, 90, 91, 89, 83, 85, 84, 92, 94, 93],
    'fertilizer': ['A','A','A','B','B','B','A','A','A','B','B','B'],
    'irrigation': ['low','low','low','low','low','low',
                   'high','high','high','high','high','high']
})

model = ols('yield ~ C(fertilizer) + C(irrigation) + C(fertilizer):C(irrigation)',
            data=data).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
# Columns: sum_sq, df, F, PR(>F)
```

### 8.3 Repeated Measures ANOVA

Used when the same subjects are measured multiple times (e.g., before, during, after treatment).

```python
# Using pingouin library for repeated measures
import pingouin as pg

data_long = pd.DataFrame({
    'Subject': [1,2,3,4,5]*3,
    'Time': ['Pre','Pre','Pre','Pre','Pre',
              'Mid','Mid','Mid','Mid','Mid',
              'Post','Post','Post','Post','Post'],
    'Score': [10,12,11,13,10, 14,15,13,16,14, 18,19,17,20,18]
})
result = pg.rm_anova(data=data_long, dv='Score', within='Time', subject='Subject')
print(result)
```

---

## 9. NON-PARAMETRIC METHODS

Used when normality assumption is violated or data is ordinal.

| Parametric Test | Non-Parametric Alternative | Python Function |
|-----------------|---------------------------|-----------------|
| One-sample t-test | Wilcoxon signed-rank test | stats.wilcoxon |
| Two-sample t-test | Mann-Whitney U test | stats.mannwhitneyu |
| Paired t-test | Wilcoxon signed-rank test | stats.wilcoxon |
| One-way ANOVA | Kruskal-Wallis test | stats.kruskal |
| Two-way ANOVA | Friedman test | stats.friedmanchisquare |
| Pearson correlation | Spearman rank correlation | stats.spearmanr |

### 9.1 When to Use Non-Parametric Tests

- Small samples (n < 15) with unknown distribution
- Ordinal scale data
- Data with significant outliers
- Distribution known to be non-normal (e.g., defect counts, highly skewed)

### 9.2 Python Non-Parametric Tests

```python
from scipy import stats
import numpy as np

# Mann-Whitney U: two independent groups
group1 = np.random.exponential(2, 30)
group2 = np.random.exponential(3, 30)
stat, p = stats.mannwhitneyu(group1, group2, alternative='two-sided')
print(f"Mann-Whitney U: stat={stat:.2f}, p={p:.4f}")

# Kruskal-Wallis: k independent groups
g1 = np.random.normal(10, 2, 20)
g2 = np.random.normal(12, 2, 20)
g3 = np.random.normal(11, 3, 20)
stat, p = stats.kruskal(g1, g2, g3)
print(f"Kruskal-Wallis: stat={stat:.2f}, p={p:.4f}")

# Wilcoxon signed-rank: paired data
before = np.random.normal(10, 2, 25)
after = before + np.random.normal(1.5, 1, 25)
stat, p = stats.wilcoxon(before, after)
print(f"Wilcoxon: stat={stat:.2f}, p={p:.4f}")

# Spearman correlation
x = np.random.normal(0, 1, 50)
y = x**2 + np.random.normal(0, 0.5, 50)  # non-linear but monotone
rho, p = stats.spearmanr(x, y)
print(f"Spearman rho={rho:.4f}, p={p:.4f}")
```

---

## 10. SIX SIGMA STATISTICAL TOOLS

### 10.1 DMAIC Framework

- **D**efine: Project charter, VOC (Voice of Customer), CTQ (Critical-to-Quality) tree, SIPOC diagram
- **M**easure: MSA (Gage R&R), baseline Cpk, process map, data collection plan
- **A**nalyze: Hypothesis tests, regression, fishbone (Ishikawa), Pareto analysis, FMEA
- **I**mprove: DOE (Design of Experiments), solution selection matrix, piloting
- **C**ontrol: Control plan, SPC charts, FMEA update, response plan, handoff to operations

### 10.2 Design of Experiments (DOE)

**Full Factorial (2^k):** All 2^k combinations of k factors at 2 levels (low/high). Detects all main effects and interactions.

**Fractional Factorial (2^(k-p)):** Subset of full factorial (resolution III, IV, V). More efficient; some interactions confounded (aliased).

**Taguchi Methods:** Orthogonal arrays; robust design; minimize sensitivity to noise factors. L8, L9, L16, L18 designs common.

**Response Surface Methodology (RSM):**
- Central Composite Design (CCD): Fits quadratic model; finds optimum
- Box-Behnken Design: No corners; fewer extreme conditions needed
- Steepest ascent/descent: Sequential approach to optimum

```python
import numpy as np
from itertools import product

def full_factorial_2level(factors, low_vals, high_vals):
    """Generate a full 2^k factorial design."""
    levels = list(product([0, 1], repeat=len(factors)))
    runs = []
    for level in levels:
        run = {}
        for i, factor in enumerate(factors):
            run[factor] = low_vals[i] if level[i] == 0 else high_vals[i]
        runs.append(run)
    return runs

design = full_factorial_2level(
    factors=['Temperature', 'Pressure', 'Time'],
    low_vals=[150, 10, 30],
    high_vals=[200, 20, 60]
)
for i, run in enumerate(design):
    print(f"Run {i+1}: {run}")
```

### 10.3 Pareto Analysis (80/20 Rule)

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['Material defect', 'Machine jam', 'Wrong setup', 
              'Operator error', 'Environmental', 'Other']
counts = [120, 75, 45, 30, 15, 10]

# Sort descending
sorted_idx = np.argsort(counts)[::-1]
sorted_cats = [categories[i] for i in sorted_idx]
sorted_counts = [counts[i] for i in sorted_idx]
cumulative_pct = np.cumsum(sorted_counts) / sum(sorted_counts) * 100

fig, ax1 = plt.subplots(figsize=(10, 5))
bars = ax1.bar(sorted_cats, sorted_counts, color='steelblue')
ax1.set_ylabel('Defect Count')

ax2 = ax1.twinx()
ax2.plot(sorted_cats, cumulative_pct, 'r-o', linewidth=2)
ax2.axhline(y=80, color='r', linestyle='--', alpha=0.7)
ax2.set_ylabel('Cumulative %')
ax2.set_ylim(0, 110)

plt.title('Pareto Analysis — Defect Sources')
plt.tight_layout()
plt.savefig('pareto_chart.png', dpi=150)
```

### 10.4 FMEA (Failure Mode and Effects Analysis)

Risk Priority Number (RPN):
```
RPN = Severity (1-10) * Occurrence (1-10) * Detection (1-10)
```

**Severity scale:**
- 1-2: No effect or very minor
- 3-4: Minor effect, slight customer dissatisfaction
- 5-6: Moderate effect, some customer dissatisfaction
- 7-8: Significant effect, high customer dissatisfaction
- 9-10: Safety hazard or regulatory non-compliance

**Action priority:** High RPN (> 100-200) triggers corrective action. Also prioritize high Severity * high Occurrence combinations even if Detection is good.

### 10.5 Fishbone / Ishikawa Diagram

Cause-and-effect diagram. Main branches (6M):
1. **M**an (People): Training, fatigue, skill level
2. **M**achine: Maintenance, calibration, age
3. **M**ethod: SOPs, process settings, controls
4. **M**aterial: Supplier quality, incoming inspection
5. **M**easurement: Gage accuracy, measurement frequency
6. **E**nvironment (Milieu): Temperature, humidity, vibration

Used in Analyze phase to brainstorm root causes systematically before data collection.

### 10.6 Process Sigma Calculation (DPMO Method)

```python
from scipy import stats

def dpmo_to_sigma(dpmo):
    """Convert DPMO to process sigma level."""
    p_defect = dpmo / 1e6
    # With Motorola 1.5-sigma shift convention:
    sigma = stats.norm.ppf(1 - p_defect) + 1.5
    return sigma

def sigma_to_dpmo(sigma_level):
    """Convert sigma level to DPMO (with 1.5-sigma shift)."""
    p_defect = stats.norm.sf(sigma_level - 1.5)
    return p_defect * 1e6

# Examples
for sigma in [3, 4, 5, 6]:
    dpmo = sigma_to_dpmo(sigma)
    print(f"Sigma {sigma}: {dpmo:.1f} DPMO")

# From actual defect data
total_units = 5000
total_opportunities = 3  # opportunities per unit
defects_found = 45
dpmo = (defects_found / (total_units * total_opportunities)) * 1e6
sigma = dpmo_to_sigma(dpmo)
print(f"\nActual DPMO: {dpmo:.0f} --> Sigma Level: {sigma:.2f}")
```

---

## 11. COMMON PITFALLS AND BEST PRACTICES

### 11.1 SPC Pitfalls

1. **Using control limits as specification limits:** Fundamentally different concepts. Never draw spec limits on a control chart.
2. **Not validating the measurement system** before charting. Noisy gage = noisy chart.
3. **Using inappropriate chart type** for data (e.g., np chart with variable sample size).
4. **Applying too many run rules** increases false alarm rate significantly.
5. **Ignoring rational subgrouping:** Subgroup should capture within-group variation; between-group variation should reflect process shifts you want to detect.
6. **Starting SPC before achieving statistical control:** Establish control limits only from in-control data.
7. **Not updating control limits** after confirmed process improvement.
8. **Autocorrelated data:** Standard SPC assumes independence. For time series with autocorrelation, use EWMA or ARIMA-based residual charts.

### 11.2 Capability Pitfalls

1. **Computing capability for an out-of-control process** is meaningless.
2. **Using short-term sample** to estimate long-term performance without disclosing the limitation.
3. **Assuming normality without checking** — especially for one-sided specifications or highly skewed processes.
4. **Confusing Cpk and Ppk** — both needed for a complete picture.
5. **Ignoring non-normal distributions** — for highly skewed data, use Weibull or non-parametric capability analysis.

### 11.3 Regression Pitfalls

1. **Correlation does not imply causation.** Always apply domain knowledge.
2. **Extrapolation beyond data range** is dangerous and unreliable.
3. **Ignoring outliers or influential points** — Check Cook's D; investigate before removing.
4. **Multicollinearity** makes coefficient interpretation unreliable. VIF > 10 is a concern.
5. **Omitted variable bias** — missing confounders bias all coefficients.
6. **Overfitting** — a model with many predictors and few observations fits noise, not signal.

### 11.4 Hypothesis Testing Pitfalls

1. **p-value is not the probability H0 is true.** It's the probability of the data given H0 is true.
2. **Statistical significance != practical significance.** Always calculate effect size.
3. **Multiple comparisons inflate Type I error** — apply Bonferroni or FDR correction.
4. **Underpowered studies** miss real effects. Always calculate required sample size upfront.
5. **One-sided vs. two-sided tests** — know which you need before collecting data.

---

## 12. REFERENCE SUMMARY TABLE

| Concept | Key Formula | Benchmark/Rule |
|---------|-------------|----------------|
| Cpk | min[(USL-mu)/3sigma, (mu-LSL)/3sigma] | >= 1.33 acceptable |
| %GRR | GRR/TV * 100 | < 10% acceptable |
| Control Limits | CL +/- 3*sigma_statistic | 99.73% coverage |
| R^2 | SSR/SST | Closer to 1 is better |
| DPMO at 6-sigma | 3.4 | With 1.5-sigma shift |
| Type I Error | alpha | 0.05 conventional |
| Power | 1 - beta | >= 0.80 recommended |
| ndc (Gage R&R) | 1.41 * PV / GRR | >= 5 required |
| VIF (regression) | 1 / (1 - Ri^2) | < 10 acceptable |
| Effect size (Cohen's d) | (mu1 - mu2) / sigma | 0.2=small, 0.5=med, 0.8=large |

---

## SOURCES AND REFERENCES

- Shewhart, W.A. (1931). *Economic Control of Quality of Manufactured Product*. Van Nostrand.
- Deming, W.E. (1986). *Out of the Crisis*. MIT Press.
- Montgomery, D.C. (2012). *Introduction to Statistical Quality Control*, 7th ed. Wiley.
- AIAG (2010). *Measurement System Analysis Reference Manual*, 4th ed.
- Western Electric Co. (1956). *Statistical Quality Control Handbook*.
- Wheeler, D.J. & Chambers, D.S. (1992). *Understanding Statistical Process Control*. SPC Press.
- NIST/SEMATECH (2013). e-Handbook of Statistical Methods. https://www.itl.nist.gov/div898/handbook/
- ASQ. Control Charts. https://asq.org/quality-resources/control-chart
- Wikipedia. Control chart. https://en.wikipedia.org/wiki/Control_chart
- SixSigmaStudyGuide. Cp & Cpk. https://sixsigmastudyguide.com/process-capability-cp-cpk/
- 1Factory. Guide to Process Capability. https://www.1factory.com/quality-academy/guide-process-capability.html

---

## UPDATE: 2026-03-04 — SPC in Asset Health & Predictive Maintenance

### SPC as Predictive Maintenance Engine (2026)

A significant convergence is underway: SPC is being repositioned from a quality-assurance tool to the **mathematical core of predictive maintenance (PdM)** in manufacturing environments.

**Key evolution:**
- Traditional SPC: operators measure parts at intervals, plot manually
- Modern SPC (2026): IIoT sensors stream continuous data; control limits are computed dynamically by AI; work orders trigger automatically on special-cause detection
- Platforms applying this model (e.g., Factory AI / f7i.ai) claim ~70% reduction in unplanned downtime and ~25% reduction in maintenance costs

**Mechanism remains classical:**
- UCL / LCL still set at ±3σ from historical asset behavior baseline
- Common cause variation = background noise of normal operation
- Special cause variation = anomaly indicating developing fault (bearing wear, shaft misalignment, lubrication failure)
- X-bar and R-charts still dominate; EWMA charts gaining traction for slow-drift detection

**SPC data inputs for asset health:**
- Vibration (mm/s or g-force)
- Temperature (bearing, motor)
- Power draw / current
- Pressure differentials

**Supply chain relevance:** For DC and manufacturing operations, applying SPC to conveyor systems, HVAC, and material handling equipment enables condition-based maintenance schedules that reduce unplanned shutdowns affecting throughput.

**Recent research note:** ScienceDirect (2026) published work on SPC for real-time monitoring in clinical psychology using Shewhart and EWMA procedures — demonstrating the method's reach beyond manufacturing into any process with sequential measurement data.

---

## Knowledge Update — 2026-03-05

### SPC for Asset Health Management (Industrial IoT)
**Source:** Factory AI / f7i.ai (Feb 2026)

SPC has evolved from quality control into the mathematical backbone of **predictive maintenance (PdM)** and **asset health management**:
- Sensors stream vibration, temperature, and power data continuously; control limits are calculated dynamically using AI (not static ±3σ from historical batches)
- Common cause vs. special cause distinction applies directly: a pump fluctuating 2.1–2.4 mm/s vibration = common cause; a spike to 4.5 mm/s = special cause requiring action
- Reported outcomes for brownfield manufacturers: ~70% reduction in unplanned downtime, ~25% reduction in maintenance costs
- Key enabler: no-code SPC platforms (e.g., Factory AI for Maximo) allow deployment without data scientists

**Supply chain relevance:** DC and manufacturing operations can apply real-time SPC to conveyor systems, refrigeration units, lift equipment, and WMS infrastructure — shifting from schedule-based PM to condition-based maintenance.

### Adaptive Bayesian Control Chart for Poisson Processes
**Source:** Malaysian Journal of Fundamental and Applied Sciences (Mar 2026)
**URL:** https://mjfas.utm.my/index.php/mjfas/article/view/4713

New research introduces an **adaptive Bayesian c-chart** with flexible modeling and customized loss functions for monitoring count-type defects:
- Significantly outperforms classical and standard Bayesian c-charts for detecting **small and moderate process shifts**
- Validated on real-world aircraft defect monitoring data
- Key innovation: integrates prior process knowledge via Bayes with adaptive thresholds that adjust as new data arrives

**Supply chain relevance:** Applicable to supplier defect rate monitoring (PPM tracking), inbound inspection, and any count-based quality metric (damaged units, mispicks, label errors) where classical c-charts are slow to detect drift.

*Sources: f7i.ai (2026-02-18), ScienceDirect (2026), iiot-world.com (2026-02)*

---

## Knowledge Update — 2026-03-06

### ML-for-SPC: Systematic Review and Challenge-Centric Taxonomy
**Source:** MDPI Entropy, Vol. 28(2), Article 151 — Published January 29, 2026
**URL:** https://www.mdpi.com/1099-4300/28/2/151

A comprehensive systematic review of mathematical and algorithmic advances in ML-driven SPC, covering literature through December 2025. Key contribution: a **challenge-centric taxonomy** (rather than a technology-centric view) that classifies ML-SPC methods by the type of data complexity they address:

- **High-dimensional / multivariate data** — principal component-based control charts, deep learning feature extractors replacing T² statistics
- **Non-stationary processes** — adaptive and online learning methods that update control limits dynamically without full Phase I restarts
- **Imbalanced fault classes** — oversampling, cost-sensitive learning, and generative models (VAE, GAN) for rare-event detection
- **Complex correlation structures** — graph neural networks for monitoring processes with latent interaction effects

**Practical implication:** The taxonomy provides a diagnostic framework: identify *which type of data complexity* is present in your process, then select the ML-SPC approach matched to that complexity. Applying a GNN where the problem is simply multivariate Gaussian is overkill and adds fragility.

### Stable Shift Algorithm for Re-establishing SPC Control Limits
**Source:** BMJ Quality & Safety — Published December 1, 2025
**URL:** https://qualitysafety.bmj.com/content/early/2025/11/29/bmjqs-2025-019263

New algorithmic approach for identifying when a process has genuinely shifted to a new stable state and it is appropriate to re-baseline control limits:
- Addresses a common SPC error: **premature declaration of successful improvement** before the process has stabilized
- Algorithm can be pre-specified at protocol stage, improving comparability across studies and reducing analyst subjectivity
- Reduces time needed for SPC analysis in improvement initiatives

**Supply chain relevance:** After a Kaizen event or process redesign, the question "when can I reset my control limits?" has been largely judgment-based. This algorithm provides a quantitative gate — reducing the risk of reporting improvement before it has been sustained.

*Sources: MDPI Entropy (2026-01-29), BMJ Quality & Safety (2025-12-01)*
