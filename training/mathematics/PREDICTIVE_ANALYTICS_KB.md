# PREDICTIVE_ANALYTICS_KB.md
# Knowledge Base: Predictive Analytics for Supply Chain & Operations
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

1. Introduction to Predictive Analytics
2. Time Series Fundamentals
3. ARIMA Models — Theory and Practice
4. Holt-Winters Exponential Smoothing
5. Demand Forecasting in Supply Chain
6. Forecast Accuracy Metrics (MAPE, MAE, RMSE, MASE)
7. Gradient Boosting for Forecasting
8. Cross-Validation for Time Series
9. Demand Sensing
10. Model Selection and Practical Guidance
11. Python Code Examples
12. Quick Reference

---

## 1. INTRODUCTION TO PREDICTIVE ANALYTICS

Predictive analytics uses historical data, statistical algorithms, and machine learning
techniques to forecast future outcomes. In supply chain and operations, predictive
analytics drives:

- Inventory optimization (avoid stockouts and overstock)
- Workforce planning (labor demand by shift/lane)
- Transportation capacity planning
- Procurement and supplier negotiations
- Revenue forecasting and financial planning

### 1.1 The Forecasting Hierarchy

Forecasts exist at multiple levels:
- **Strategic:** Annual/multi-year (budget, network design)
- **Tactical:** Monthly/quarterly (S&OP, inventory targets)
- **Operational:** Daily/weekly (replenishment, dispatch, routing)

The time horizon and granularity determine which models are appropriate.
Short-horizon operational forecasts (1–14 days) often benefit from demand sensing
and ML approaches; longer-horizon forecasts lean toward statistical methods.

### 1.2 Types of Forecasting Problems

| Problem Type         | Example                          | Recommended Approach     |
|----------------------|----------------------------------|--------------------------|
| Univariate TS        | Weekly widget shipments          | ARIMA, Holt-Winters      |
| Multivariate TS      | Demand + promotions + weather    | Regression, SARIMA, ML   |
| Intermittent demand  | Spare parts, low-volume SKUs     | Croston, SBA, bootstrap  |
| Hierarchical         | National → regional → store      | Reconciliation methods   |
| New product launch   | No history                       | Analogous product, Delphi|

---

## 2. TIME SERIES FUNDAMENTALS

A time series is a sequence of observations recorded at successive, equally-spaced
time intervals: {y_1, y_2, ..., y_T}.

### 2.1 Key Components

**Trend (T):** Long-term increase or decrease in the data level.
- Can be linear, exponential, or nonlinear.
- Detected via moving averages, regression, or HP filter.

**Seasonality (S):** Regular periodic fluctuations.
- Fixed frequency (weekly, monthly, annual).
- Example: Retail demand peaks in November–December.
- Additive: y = T + S + R  (when amplitude is stable)
- Multiplicative: y = T × S × R  (when amplitude grows with level)

**Cyclicality (C):** Irregular longer-term fluctuations (economic cycles).
- Unlike seasonality, cycles do not have fixed frequency.
- Typically 2–10 year periods aligned with business/economic cycles.

**Residual/Error (R):** Random noise after removing T, S, C.
- White noise: mean zero, constant variance, no autocorrelation.
- Structured residuals indicate model misspecification.

### 2.2 Stationarity

A stationary time series has:
1. Constant mean over time
2. Constant variance over time
3. Autocovariance that depends only on lag, not time

Why it matters: Most statistical forecasting models (ARIMA) assume stationarity.
Non-stationary series must be transformed.

**Tests for stationarity:**
- Augmented Dickey-Fuller (ADF): H0 = unit root exists (non-stationary)
- KPSS: H0 = stationary
- Best practice: use both; ADF confirms non-stationarity, KPSS confirms stationarity

**Achieving stationarity:**
- First differencing: Δy_t = y_t − y_{t−1}  (removes trend)
- Seasonal differencing: Δ_m y_t = y_t − y_{t−m}  (removes seasonality)
- Log transform: log(y_t)  (stabilizes variance)

### 2.3 Autocorrelation

**ACF (Autocorrelation Function):** Correlation between y_t and y_{t−k} for lags k.
Indicates how past values relate to current values directly.

**PACF (Partial Autocorrelation Function):** Correlation between y_t and y_{t−k}
after removing the effects of intermediate lags.

ACF and PACF plots are critical diagnostic tools for ARIMA order selection:
- AR(p) process: ACF decays gradually, PACF cuts off at lag p
- MA(q) process: ACF cuts off at lag q, PACF decays gradually
- ARMA: both decay gradually

---

## 3. ARIMA MODELS — THEORY AND PRACTICE

**ARIMA = AutoRegressive Integrated Moving Average**

Developed by Box and Jenkins (1970). One of the most widely used and well-understood
statistical forecasting methods. Suitable for univariate time series with trend
but without strong seasonality (use SARIMA for seasonal data).

### 3.1 Model Components

**AR(p) — AutoRegressive part:**
y_t = φ_1 y_{t-1} + φ_2 y_{t-2} + ... + φ_p y_{t-p} + ε_t

The current value is a linear function of p past values.
φ are AR coefficients. ε_t is white noise.

**I(d) — Integration / Differencing:**
The "d" represents the number of times the series is differenced to achieve stationarity.
- d=0: already stationary
- d=1: first difference (most common)
- d=2: second difference (rare; implies very strong trend)

**MA(q) — Moving Average part:**
y_t = ε_t + θ_1 ε_{t-1} + θ_2 ε_{t-2} + ... + θ_q ε_{t-q}

The current value depends on q past forecast errors.
θ are MA coefficients.

**Combined ARIMA(p, d, q):**
Δ^d y_t = φ_1 Δ^d y_{t-1} + ... + φ_p Δ^d y_{t-p} + ε_t + θ_1 ε_{t-1} + ... + θ_q ε_{t-q}

### 3.2 SARIMA — Seasonal ARIMA

**SARIMA(p, d, q)(P, D, Q)[m]**

Extends ARIMA with seasonal components:
- (P, D, Q): seasonal AR order, seasonal differencing, seasonal MA order
- [m]: seasonal period (e.g., 12 for monthly data with annual seasonality)

Example: SARIMA(1,1,1)(1,1,1)[12] for monthly retail sales.

### 3.3 Model Selection — Box-Jenkins Methodology

Step 1: **Visualize** — plot the series; look for trend, seasonality, outliers.

Step 2: **Stationarize** — apply differencing until ADF/KPSS tests confirm stationarity.
         Determine d (and D for seasonal).

Step 3: **Identify p and q** — examine ACF and PACF of the stationary series.

Step 4: **Fit candidate models** — try several (p,d,q) combinations.

Step 5: **Select best model** — use information criteria:
- AIC (Akaike): AIC = 2k − 2 ln(L)  (penalizes number of parameters k)
- BIC (Bayesian): BIC = k ln(n) − 2 ln(L)  (heavier penalty; prefers simpler models)
- Lower AIC/BIC = better fit-to-complexity trade-off

Step 6: **Diagnostic checking** — residuals should be white noise.
- Ljung-Box test: H0 = residuals are independently distributed
- Shapiro-Wilk test: H0 = residuals are normally distributed
- Plot ACF of residuals: should show no significant spikes

Step 7: **Forecast** — generate point forecasts and prediction intervals.

### 3.4 auto.arima / pmdarima

Manual order selection is tedious for large numbers of series.
**auto_arima** (pmdarima) automates the Box-Jenkins process:
- Performs unit root tests to select d and D
- Uses stepwise search over p, q combinations
- Selects by AIC (default) or BIC
- Optionally fits SARIMA, handles seasonal period automatically

```python
from pmdarima import auto_arima
import pandas as pd

# Fit model
model = auto_arima(train_series,
                   seasonal=True,
                   m=12,           # monthly seasonality
                   d=None,         # auto-select
                   D=None,         # auto-select seasonal differencing
                   information_criterion='aic',
                   stepwise=True,
                   suppress_warnings=True)

# Forecast
forecast, conf_int = model.predict(n_periods=12, return_conf_int=True)
```

### 3.5 ARIMA Limitations

- Assumes linear relationships
- Sensitive to outliers and structural breaks
- Requires long enough history (typically 50+ observations)
- Single-series only (no exogenous variables, unless using ARIMAX)
- Not ideal for very long forecast horizons
- Computationally expensive at scale (thousands of SKUs)

### 3.6 ARIMAX — ARIMA with Exogenous Variables

Extends ARIMA by incorporating external regressors (promotions, price, macroeconomic).

y_t = ARIMA terms + β_1 X_{1t} + β_2 X_{2t} + ε_t

In Python: use the `exog` parameter in statsmodels SARIMAX.

---

## 4. HOLT-WINTERS EXPONENTIAL SMOOTHING

Also known as "Triple Exponential Smoothing." A highly practical method for series
with trend and seasonality. Computationally efficient and interpretable.

### 4.1 Forms

**Simple Exponential Smoothing (SES):** No trend, no seasonality.
ŷ_{t+1} = α y_t + (1-α) ŷ_t       (0 < α < 1)
- α close to 1: emphasizes recent observations
- α close to 0: more weight on historical data

**Holt's Linear (Double) Exponential Smoothing:** With trend.
Level:   l_t = α y_t + (1-α)(l_{t-1} + b_{t-1})
Trend:   b_t = β(l_t - l_{t-1}) + (1-β)b_{t-1}
Forecast: ŷ_{t+h} = l_t + h × b_t

**Holt-Winters (Triple) Exponential Smoothing:** With trend and seasonality.

Additive seasonal variant:
Level:    l_t = α(y_t - s_{t-m}) + (1-α)(l_{t-1} + b_{t-1})
Trend:    b_t = β(l_t - l_{t-1}) + (1-β)b_{t-1}
Seasonal: s_t = γ(y_t - l_{t-1} - b_{t-1}) + (1-γ)s_{t-m}
Forecast: ŷ_{t+h} = l_t + h × b_t + s_{t+h-m}

Multiplicative seasonal variant (when seasonal amplitude grows with level):
Level:    l_t = α(y_t / s_{t-m}) + (1-α)(l_{t-1} + b_{t-1})
Trend:    b_t = β(l_t - l_{t-1}) + (1-β)b_{t-1}
Seasonal: s_t = γ(y_t / (l_{t-1} + b_{t-1})) + (1-γ)s_{t-m}
Forecast: ŷ_{t+h} = (l_t + h × b_t) × s_{t+h-m}

### 4.2 Parameter Selection

Parameters α, β, γ ∈ (0, 1) are estimated by minimizing SSE on training data.
Most implementations use L-BFGS-B or Nelder-Mead optimization.

### 4.3 ETS Framework

ETS (Error, Trend, Seasonal) provides a unified state-space framework for
exponential smoothing. Each component can be:
- Error: Additive (A) or Multiplicative (M)
- Trend: None (N), Additive (A), Additive Damped (Ad), Multiplicative (M)
- Seasonal: None (N), Additive (A), Multiplicative (M)

This gives 30 possible ETS models. Model selection via AIC.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    train_series,
    trend='add',
    seasonal='mul',
    seasonal_periods=12,
    damped_trend=True
)
fitted = model.fit(optimized=True)
forecast = fitted.forecast(steps=12)
```

### 4.4 Holt-Winters vs ARIMA

| Aspect             | Holt-Winters          | ARIMA                  |
|--------------------|-----------------------|------------------------|
| Interpretability   | High                  | Moderate               |
| Handles seasonality| Yes (built-in)        | Yes (SARIMA extension) |
| Robustness         | Moderate              | Moderate               |
| Data requirements  | ~2× seasonal cycles   | 50+ obs recommended    |
| Speed              | Very fast             | Slower (ADF tests)     |
| Prediction intervals| Via simulation       | Analytic              |
| Best for           | Stable seasonal series| General univariate TS  |

---

## 5. DEMAND FORECASTING IN SUPPLY CHAIN

### 5.1 What Is Demand Forecasting?

Demand forecasting estimates future customer demand for products or services
using statistical models, historical data, market trends, and other factors.

**Strategic value:**
- Aligns production, procurement, and distribution to anticipated demand
- Reduces inventory carrying costs and stockout risk
- Enables supplier relationship management
- Improves cash flow predictability

**Critical statistics:**
- 9 of 10 organizations achieved measurable value from data/analytics (NewVantage 2023)
- 70% of consumers switch brands after a single stockout (ECR Europe)
- 45% of supply chain pros lack visibility beyond tier-1 suppliers (McKinsey)

### 5.2 Forecasting Methods for Supply Chain

**Qualitative Methods:**
- Delphi method: structured expert consensus, iterative rounds
- Market research / consumer surveys: primary data collection
- Sales force composite: aggregation of field sales estimates
- Use when: new product launches, no historical data, market disruption

**Quantitative Methods:**

*Time Series:*
- Moving Average: simple, low-lag, but misses trend
- Exponential Smoothing (SES, Holt, Holt-Winters): fast, interpretable
- ARIMA/SARIMA: rigorous, handles complex patterns
- Decomposition (STL): separates trend, seasonal, residual

*Causal / Regression:*
- Linear regression on external drivers (GDP, price, promotions)
- ARIMAX: ARIMA + exogenous variables
- VAR (Vector Autoregression): multiple interdependent time series

*Machine Learning:*
- Gradient Boosting (XGBoost, LightGBM): handles nonlinear feature interactions
- Random Forest: ensemble, robust to outliers
- LSTM/GRU: deep learning for complex long-range patterns
- Prophet: Facebook's decomposable model, handles holidays and trend changes

*Collaborative Methods:*
- CPFR (Collaborative Planning, Forecasting, and Replenishment): shared data
  between retailers and suppliers for more accurate joint forecasts
- VMI (Vendor Managed Inventory): supplier manages replenishment using POS data
- POS data sharing: real-time demand signal from point of sale

### 5.3 Demand Sensing

Demand sensing is the practice of using near-real-time data to improve
short-horizon forecasts (1–14 days).

**Traditional forecasting** uses weekly/monthly historical aggregates.
**Demand sensing** ingests:
- Daily or intraday POS data
- Social media signals
- Search trends (Google Trends)
- Weather forecasts
- Competitor pricing and promotions

**Process:**
1. Collect high-frequency data signals
2. Apply statistical or ML models to translate signals into demand adjustments
3. Update forecast daily (vs. traditional weekly/monthly cycle)
4. Propagate updated forecast through supply planning

**Benefits:**
- Reduces forecast error in the 1–7 day horizon by 20–40%
- Improves service levels and reduces safety stock
- Enables better transportation and labor planning

**Demand sensing vs. demand shaping:**
- Sensing: better reading what demand will be
- Shaping: using pricing, promotion, allocation to influence demand

### 5.4 Intermittent Demand

Many supply chain SKUs have sparse, lumpy demand (zeros interspersed with
irregular spikes). Standard ARIMA and exponential smoothing perform poorly.

**Croston's Method:**
Separately estimates average demand size (when non-zero) and inter-demand interval.
Uses SES on each component. Provides unbiased demand rate estimate.

**SBA (Syntetos-Boylan Approximation):**
Improves Croston's by correcting a bias in Croston's original formulation.
Widely regarded as the best simple method for intermittent demand.

**Bootstrap methods:**
Resample historical demand patterns to generate empirical forecast distributions.
Useful for safety stock calculation under intermittent demand.

### 5.5 Forecast Horizons and Lead Time

The forecast horizon should align with decision-making lead time:
- **Replenishment lead time:** order cycle + supplier lead time
- **Manufacturing lead time:** raw materials + production + quality check
- **Transportation lead time:** transit days by mode

For safety stock, the relevant horizon is supplier lead time + review period.
Forecast accuracy degrades rapidly beyond ~3× the seasonal cycle.

### 5.6 Hierarchical Forecasting

Multi-level demand structure (e.g., national → regional → DC → store → SKU):

**Bottom-up:** Aggregate forecasts from lowest level.
Pros: captures local patterns. Cons: noisy at low levels.

**Top-down:** Disaggregate national forecast using historical proportions.
Pros: accurate at aggregate. Cons: ignores local patterns.

**Middle-out:** Forecast at middle level; aggregate up, disaggregate down.

**Reconciliation (MinT):** Optimally reconcile forecasts at all levels
simultaneously using regression. Minimizes total forecast error.

---

## 6. FORECAST ACCURACY METRICS

### 6.1 Error Definitions

Let y_t = actual value, ŷ_t = forecast value.
Error: e_t = y_t − ŷ_t

### 6.2 Scale-Dependent Metrics

**MAE — Mean Absolute Error:**
MAE = (1/n) Σ |e_t|

- Interpretable in original units
- Robust to outliers
- Cannot compare across series with different scales
- Use when: all series are on the same scale; outliers should not dominate

**MSE — Mean Squared Error:**
MSE = (1/n) Σ e_t²

- Penalizes large errors heavily (squared)
- Not in original units
- Sensitive to outliers

**RMSE — Root Mean Squared Error:**
RMSE = √[(1/n) Σ e_t²]

- Same units as original data
- Penalizes large errors more than MAE
- Standard metric in many competitions (M-competitions)
- Use when: large errors are especially costly (e.g., stockout risk)

**Comparison of MAE vs RMSE:**
RMSE ≥ MAE always. The ratio RMSE/MAE indicates presence of outliers.
If RMSE >> MAE, the model has occasional large errors.

### 6.3 Scale-Independent Metrics

**MAPE — Mean Absolute Percentage Error:**
MAPE = (100/n) Σ |e_t / y_t|

- Expressed as percentage; allows cross-series comparison
- Widely used in business and supply chain
- FATAL flaw: undefined when y_t = 0; biased toward under-forecasting
- Asymmetric: a forecast of 0 when actual is 100 → 100% error,
  but a forecast of 200 when actual is 100 → 100% error too
  (the denominator is always actual, so over-forecasts are capped at asymptotic)

**Typical MAPE benchmarks in supply chain:**
- <10%: Excellent forecasting
- 10–20%: Good
- 20–30%: Acceptable
- >30%: Needs improvement
- Note: benchmarks vary by industry, SKU volatility, and product lifecycle stage

**sMAPE — Symmetric MAPE:**
sMAPE = (200/n) Σ |y_t − ŷ_t| / (|y_t| + |ŷ_t|)

Addresses MAPE asymmetry. Bounded between 0% and 200%.
Still problematic when both actual and forecast are near zero.

**WMAPE — Weighted MAPE:**
WMAPE = Σ |e_t| / Σ |y_t|

Also called MAD/Mean. Preferred over MAPE when zeros are present.
Avoids division by zero by using total actuals as denominator.
Standard metric at many large retailers and CPGs.

**MASE — Mean Absolute Scaled Error:**
MASE = MAE / (1/(n-1) Σ |y_t − y_{t-1}|)

- Scales error by in-sample naive forecast MAE
- Scale-free, works with zero values
- MASE = 1: same accuracy as naive forecast
- MASE < 1: better than naive
- Recommended by Hyndman & Koehler (2006) as the best general accuracy metric

### 6.4 Bias Metrics

**ME — Mean Error (Bias):**
ME = (1/n) Σ e_t

- Positive: systematic under-forecasting
- Negative: systematic over-forecasting
- A model can have ME = 0 but still be inaccurate (large MAE)

**MPE — Mean Percentage Error:**
MPE = (100/n) Σ (e_t / y_t)

Measures directional bias as percentage.

**Tracking Signal:**
TS_t = (Σ e_t) / MAD

- |TS| < 4: forecast in control (typical threshold)
- |TS| > 4: forecast out of control; investigate bias cause
- Used in real-time monitoring of forecasting systems

### 6.5 Choosing the Right Metric

| Situation                           | Recommended Metric   |
|-------------------------------------|----------------------|
| Single series, no zeros             | RMSE or MAE          |
| Multiple series, same scale         | RMSE or MAE          |
| Multiple series, different scales   | MASE or WMAPE        |
| Business stakeholder reporting      | MAPE or WMAPE        |
| Intermittent demand (zeros present) | MASE or MAD/Mean     |
| When large errors are critical      | RMSE                 |
| Monitoring bias                     | ME + Tracking Signal |

---

## 7. GRADIENT BOOSTING FOR FORECASTING

Gradient boosting is an ensemble machine learning method that builds models
sequentially, with each new model correcting the errors of its predecessors.

### 7.1 How Gradient Boosting Works

1. Initialize with a simple model (often mean of target)
2. Compute residuals (pseudo-residuals = negative gradient of loss)
3. Fit a weak learner (typically decision tree) to residuals
4. Update model: F_{m+1}(x) = F_m(x) + η × h_m(x)
   where η = learning rate, h_m = new weak learner
5. Repeat for M iterations

**Key hyperparameters:**
- `n_estimators`: number of trees (more = lower bias, risk of overfitting)
- `learning_rate`: shrinkage factor η (lower = better generalization, needs more trees)
- `max_depth`: tree depth (controls model complexity)
- `min_samples_leaf`: minimum samples per leaf (regularization)
- `subsample`: fraction of samples per tree (stochastic GB)
- `colsample_bytree`: fraction of features per tree (XGBoost)

### 7.2 XGBoost

eXtreme Gradient Boosting by Chen & Guestrin (2016).
Dominant in Kaggle competitions; excellent for tabular data including time series.

Key improvements over vanilla gradient boosting:
- Second-order gradient approximation (Newton boosting)
- Regularization: L1 (alpha) and L2 (lambda) penalties on leaf weights
- Column and row subsampling
- Efficient tree-building via histogram approximation
- Handles missing values natively

### 7.3 LightGBM

Microsoft's LightGBM uses leaf-wise (best-first) tree growth vs. level-wise.
Typically 2–5× faster than XGBoost on large datasets.
Preferred when: millions of rows, high-dimensional features.

### 7.4 Adapting GB to Time Series

Gradient boosting is a supervised learning algorithm; it requires feature engineering
to capture temporal patterns.

**Feature engineering for time series:**
- Lag features: y_{t-1}, y_{t-2}, ..., y_{t-p}
- Rolling statistics: rolling mean, std, min, max (windows: 7, 14, 30 days)
- Expanding window statistics
- Calendar features: day of week, month, quarter, year, holiday flag
- Time-since features: days since last promotion, last stockout
- External regressors: price, promotion intensity, weather, economic indices

**Recursive multi-step forecasting:**
- Predict h=1, then use that prediction as a lag for h=2, etc.
- Error accumulates over horizon

**Direct multi-step forecasting:**
- Train a separate model for each horizon h
- Higher computational cost but no error accumulation

### 7.5 GB vs ARIMA

| Aspect                 | Gradient Boosting     | ARIMA                |
|------------------------|-----------------------|----------------------|
| Feature handling       | Excellent             | Limited (ARIMAX)     |
| Nonlinear patterns     | Yes                   | No                   |
| Seasonality            | Via features          | Via SARIMA           |
| Data requirements      | 500+ observations     | 50+ observations     |
| Interpretability       | Low-moderate (SHAP)   | High                 |
| Scalability (many SKU) | Batch-trainable       | One model per series |
| Prediction intervals   | Quantile regression   | Analytic             |

---

## 8. CROSS-VALIDATION FOR TIME SERIES

Standard k-fold cross-validation shuffles data randomly, which is invalid for
time series (data has temporal ordering; future cannot inform past).

### 8.1 Time Series Split (Walk-Forward Validation)

Also called "rolling origin" or "expanding window" validation.

```
Fold 1: Train [1..n₁]       Test [n₁+1..n₁+h]
Fold 2: Train [1..n₁+h]     Test [n₁+h+1..n₁+2h]
Fold 3: Train [1..n₁+2h]    Test [n₁+2h+1..n₁+3h]
...
```

Each fold expands the training window. The test window "walks forward."
This preserves temporal ordering and simulates real forecasting conditions.

### 8.2 Sliding Window CV

Same as walk-forward but training window is fixed size (not expanding).
Appropriate when distribution shifts over time (older data less relevant).

### 8.3 Implementation in Python

```python
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

tscv = TimeSeriesSplit(n_splits=5, test_size=12)  # 5 folds, 12-step test

mae_scores = []
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae_scores.append(np.mean(np.abs(y_test - y_pred)))

print(f"CV MAE: {np.mean(mae_scores):.2f} ± {np.std(mae_scores):.2f}")
```

### 8.4 Information Leakage

Common pitfalls that cause data leakage in time series:
- Using future data to create lag features (must use only data available at forecast time)
- Fitting scalers/normalizers on the full dataset before splitting
- Including future promotional information in the feature set

Best practice: build a pipeline that simulates the exact information available
at each forecast origin.

### 8.5 Backtesting

Backtesting is the retrospective evaluation of a forecasting model on historical data.
Distinguishes from CV in that it typically uses a fixed hold-out test set
representing a specific historical period.

Components of a robust backtest:
1. Define evaluation period (start/end date)
2. Replicate production forecasting process (including data pipeline)
3. Compute accuracy metrics over evaluation period
4. Compare multiple models / benchmarks
5. Statistical significance testing (Diebold-Mariano test)

---

## 9. DEMAND SENSING — DEEP DIVE

### 9.1 The Demand Signal Hierarchy

From weakest/lagging to strongest/leading:

1. **Shipment data** (weakest): reflects supply, not demand; lags actual consumption
2. **Orders received**: better, but includes order batching and speculation
3. **POS / scan data**: actual consumer purchases at retail; real demand
4. **Loyalty card / basket data**: consumer-level demand with demographics
5. **Search/social signals** (leading): intent data before purchase

### 9.2 Demand Sensing Architecture

```
Real-time data feeds:
  POS scanners → Daily demand by SKU/store
  Weather APIs → Temperature, precipitation forecast
  Promotion calendar → Active/upcoming promotions
  Google Trends → Search volume index
  
Statistical engine:
  Short-term model (1-7 day horizon)
  Signal weighting and integration
  Anomaly detection (outlier suppression)
  
Output:
  Adjusted daily forecast
  Confidence intervals
  Inventory replenishment recommendations
```

### 9.3 Weather-Adjusted Demand

Many categories show strong weather elasticity:
- Beverages: summer heat drives soft drink demand
- HVAC supplies: extreme temperatures drive unit sales
- Apparel: seasonal transitions
- Automotive: precipitation affects tire/accessory demand

**Modeling approach:**
1. Compute historical weather sensitivity (regression of demand on temperature deviation)
2. Obtain weather forecast (7–14 day horizon)
3. Adjust statistical baseline forecast by weather deviation × sensitivity coefficient

---

## 10. MODEL SELECTION AND PRACTICAL GUIDANCE

### 10.1 Forecast Selection Framework

```
1. Data availability:
   - < 2 years history? → Simple exponential smoothing, Croston, analogous
   - 2-5 years? → Holt-Winters, ARIMA
   - 5+ years? → Full model suite

2. Demand pattern:
   - Stable, seasonal? → Holt-Winters (best simplicity/accuracy tradeoff)
   - Complex, nonlinear? → Gradient boosting, neural networks
   - Intermittent/lumpy? → Croston, SBA, bootstrapping

3. Available exogenous variables:
   - Promotions, price, weather available? → ARIMAX or ML
   - No exogenous data? → ARIMA, Holt-Winters

4. Scale:
   - 1-100 series? → Manual Box-Jenkins or auto_arima
   - 100-10,000 series? → auto_arima, Holt-Winters with automation
   - 10,000+ series? → Gradient boosting (single global model), neural networks

5. Forecast horizon:
   - 1-7 days? → Demand sensing (ML on high-frequency data)
   - 1-4 weeks? → ARIMA, Holt-Winters, GB
   - 1-12 months? → ARIMA, Holt-Winters, regression
   - 1-5 years? → Trend extrapolation, economic models
```

### 10.2 Ensemble Forecasting

Combining forecasts from multiple models consistently outperforms individual models.
Recommended for high-value forecasting applications.

Simple average: ŷ_ensemble = (1/K) Σ ŷ_k
Weighted average: ŷ_ensemble = Σ w_k ŷ_k  where w_k based on past accuracy

In practice, even equal-weight combinations of 3-5 diverse models (ARIMA + Holt-Winters
+ GB) often beat the best individual model by 5-15%.

### 10.3 Forecast Governance

- **Forecast review cadence:** weekly for operational, monthly for tactical
- **Exception reporting:** flag items with forecast error > threshold
- **Bias monitoring:** track ME and tracking signal over time
- **Model refresh:** refit models quarterly or when structural breaks detected
- **Consensus forecasting:** align statistical forecast with commercial judgment

---

## 11. PYTHON CODE EXAMPLES

### 11.1 ARIMA Full Pipeline

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("demand.csv", parse_dates=["date"], index_col="date")
y = df["units"]

# Stationarity test
result = adfuller(y)
print(f"ADF p-value: {result[1]:.4f}")  # p < 0.05 → stationary

# Split train/test (last 12 periods as test)
train, test = y[:-12], y[-12:]

# Fit auto ARIMA
model = auto_arima(train, seasonal=True, m=12,
                   information_criterion="aic",
                   stepwise=True, suppress_warnings=True)
print(model.summary())

# Forecast
forecast, conf_int = model.predict(n_periods=12, return_conf_int=True)
forecast = pd.Series(forecast, index=test.index)

# Evaluate
mae = mean_absolute_error(test, forecast)
mape = np.mean(np.abs((test - forecast) / test)) * 100
print(f"MAE: {mae:.1f}, MAPE: {mape:.1f}%")

# Plot
plt.figure(figsize=(12,5))
plt.plot(train[-36:], label="Train")
plt.plot(test, label="Actual")
plt.plot(forecast, label="Forecast")
plt.fill_between(test.index, conf_int[:,0], conf_int[:,1], alpha=0.2)
plt.legend()
plt.title("ARIMA Demand Forecast")
plt.show()
```

### 11.2 Holt-Winters with Accuracy Metrics

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

def forecast_accuracy(actual, forecast):
    mae  = np.mean(np.abs(actual - forecast))
    rmse = np.sqrt(np.mean((actual - forecast)**2))
    mape = np.mean(np.abs((actual - forecast) / actual)) * 100
    wmape = np.sum(np.abs(actual - forecast)) / np.sum(actual) * 100
    bias = np.mean(forecast - actual)
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape, "WMAPE": wmape, "Bias": bias}

# Fit Holt-Winters
model = ExponentialSmoothing(train, trend="add", seasonal="mul",
                              seasonal_periods=12, damped_trend=True)
fitted = model.fit(optimized=True)
forecast_hw = fitted.forecast(12)

metrics = forecast_accuracy(test.values, forecast_hw.values)
for k, v in metrics.items():
    print(f"  {k}: {v:.2f}")
```

### 11.3 XGBoost Time Series Forecasting

```python
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

def create_lag_features(series, lags, windows):
    df = pd.DataFrame({"y": series})
    for lag in lags:
        df[f"lag_{lag}"] = df["y"].shift(lag)
    for w in windows:
        df[f"roll_mean_{w}"] = df["y"].shift(1).rolling(w).mean()
        df[f"roll_std_{w}"] = df["y"].shift(1).rolling(w).std()
    df["month"] = df.index.month
    df["dayofweek"] = df.index.dayofweek
    df["quarter"] = df.index.quarter
    return df.dropna()

# Create features
feature_df = create_lag_features(y, lags=[1,2,3,4,12,24,52], windows=[4,8,13,26])
X = feature_df.drop(columns=["y"])
y_feat = feature_df["y"]

# Walk-forward CV
tscv = TimeSeriesSplit(n_splits=5, test_size=12)
cv_maes = []

for train_idx, test_idx in tscv.split(X):
    model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05,
                               max_depth=5, subsample=0.8)
    model.fit(X.iloc[train_idx], y_feat.iloc[train_idx],
              eval_set=[(X.iloc[test_idx], y_feat.iloc[test_idx])],
              verbose=False)
    pred = model.predict(X.iloc[test_idx])
    cv_maes.append(np.mean(np.abs(y_feat.iloc[test_idx] - pred)))

print(f"XGB CV MAE: {np.mean(cv_maes):.2f} ± {np.std(cv_maes):.2f}")
```

---

## 12. QUICK REFERENCE

### ARIMA Parameter Summary
| Parameter | Meaning                   | How to choose            |
|-----------|---------------------------|--------------------------|
| p         | AR order                  | PACF cutoff              |
| d         | Differencing              | ADF test (usually 0-1)   |
| q         | MA order                  | ACF cutoff               |
| P         | Seasonal AR order         | Seasonal PACF            |
| D         | Seasonal differencing     | Seasonal ADF test        |
| Q         | Seasonal MA order         | Seasonal ACF             |
| m         | Seasonal period           | Data frequency (12, 52)  |

### Accuracy Metric Quick Reference
| Metric  | Formula                         | Scale-free | Handles zeros | Notes                  |
|---------|----------------------------------|------------|----------------|------------------------|
| MAE     | mean(|e|)                       | No         | Yes            | Robust, interpretable  |
| RMSE    | sqrt(mean(e²))                  | No         | Yes            | Penalizes large errors |
| MAPE    | mean(|e/y|)×100                 | Yes        | No             | Common in business     |
| WMAPE   | sum(|e|)/sum(y)×100             | Yes        | Yes            | Better than MAPE       |
| MASE    | MAE / naive_MAE                 | Yes        | Yes            | Best general metric    |
| Bias    | mean(e)                         | No         | Yes            | Directional error      |

### Demand Sensing Data Sources
| Source           | Latency  | Signal Strength | Cost       |
|------------------|----------|-----------------|------------|
| POS/Scan data    | Daily    | High            | Medium     |
| Order data       | Real-time| Medium          | Low        |
| Shipment data    | Daily    | Low (lagged)    | Low        |
| Google Trends    | Daily    | Medium (leading)| Free       |
| Social media     | Real-time| Variable        | Low-Medium |
| Weather forecast | Hourly   | Category-specific| Free      |

### Key Python Libraries
| Library        | Purpose                              |
|----------------|--------------------------------------|
| statsmodels    | ARIMA, SARIMA, ETS, Holt-Winters     |
| pmdarima       | auto_arima, Box-Jenkins automation   |
| scikit-learn   | ML models, TimeSeriesSplit, metrics  |
| xgboost        | Gradient boosting (XGB)              |
| lightgbm       | Gradient boosting (LGB, fast)        |
| prophet        | Facebook Prophet, holiday handling   |
| skforecast     | Sklearn wrappers for TS forecasting  |
| nixtla/statsforecast | Fast statistical forecasting   |

---
*End of PREDICTIVE_ANALYTICS_KB.md*
*Source: Compiled from DataCamp, machinelearningplus.com, Trinetix demand forecasting guide,*
*Hyndman & Athanasopoulos "Forecasting: Principles and Practice", and industry practice.*

---

## UPDATE: 2026-03-04 — Forecasting Methods & Supply Chain Intelligence

### Ensemble Forecasting as Standard Practice (2026)

Best-in-class demand forecasting has moved firmly to **ensemble methods** — single models are no longer competitive for supply chain use cases.

**Recommended ensemble pattern:**
- ARIMA (captures autocorrelation, trend, seasonality)
- XGBoost (nonlinear feature interactions, promotions, external regressors)
- Exponential smoothing (robust baseline, handles level shifts)
- Weighted combination outperforms any single model in backtesting

**Temporal Fusion Transformer (TFT):**
- Emerging as the high-performance architecture for multi-horizon supply chain forecasting
- Handles: internal sales history, economic indicators, weather data, social media sentiment indices
- Architecture: attention-based, explicitly models known future inputs (promotions, holidays) vs. unknown
- Implementation: `pytorch-forecasting` library

**AI frameworks for external shock handling (2026):**
- Static models fail on demand spikes from viral trends, geopolitical disruptions, tariff changes
- Deep learning architectures with unstructured data ingestion (news feeds, port congestion data) are being deployed at the enterprise level
- Key shift: moving from **pattern recognition** → **predictive intelligence** that incorporates causal signals

**Tariff uncertainty modeling (current):**
- PYMNTS (March 2026): 42% of North American firms now use predictive analytics to model tariff exposure and synchronize payables with receivables
- Monte Carlo simulation is the primary tool for tariff scenario analysis — run N simulations across tariff probability distributions, compute P10/P50/P90 cost outcomes

**Supply chain agility metric:**
- Forecast accuracy improvement of up to 40% cited when combining multi-source external data with TFT models (meta-intelligence.tech, 2026)
- Error metric of choice: MAPE for symmetric distributions; sMAPE or WRMSSE for intermittent/lumpy demand

---

## Knowledge Update — 2026-03-05

### Predictive Analytics in Supply Chain — 2026 Framework
**Source:** Datup.ai (Feb 2026) | **Market:** $18B+ in 2024, growing 25–28% annually

The four-tier analytics framework:
| Type | Question | Time | Example |
|---|---|---|---|
| Descriptive | What happened? | Past | "Sold 12,400 units of SKU X in March" |
| Diagnostic | Why? | Past | "Sales dropped 18% due to supplier delay + competitor promo" |
| **Predictive** | What will happen? | Future | "April forecast: 14,200 units, 85% confidence" |
| **Prescriptive** | What to do? | Future/Action | "Increase safety stock 1,100 units; advance PO by 1 week" |

**Key stat:** 40% of a demand planner's time is spent explaining why last month's forecast failed. Predictive analytics closes that loop.

**Technical components for supply chain predictive analytics:**
- Combines historical transactional data + machine learning + real-time signals (IoT, weather, tariff news)
- Outputs: safety stock by SKU/location/channel, reorder points, optimal batch sizes
- Integrates with ERP, WMS, TMS

**Latin America adoption signal:** 70% of SC professionals cite predictive + prescriptive analytics as their #1 technology priority for 2026 — a leading indicator of where North American mid-market is heading in 12–18 months.

### AI Adoption for Working Capital Management
**Source:** PYMNTS.com (Feb 2026)

- 42% of North American firms now use AI for working capital efficiency
- Applications: demand swing modeling, tariff exposure simulation, payables/receivables synchronization
- Implication: predictive analytics is crossing from supply chain operations into finance-side decision support — **integrated demand-to-cash forecasting** is the emerging model

### Monte Carlo + Real-Time KPI Dashboards (Manufacturing)
**Source:** Journal of Intelligence and Engineering Technology (2026)
**Citation:** Yin, M. (2026). *Integrating Real-Time KPI Dashboards with Monte Carlo Simulation for Optimizing Semiconductor Manufacturing Processes.* JIET, 1(1), 27–39.

Key integration pattern: Monte Carlo simulation outputs (probability distributions of process outcomes) fed directly into live KPI dashboards, enabling operators to see not just current state but **confidence intervals on future state** in real time.

**Supply chain relevance:** Applicable to distribution center throughput planning — run Monte Carlo on labor variability, inbound volume uncertainty, and equipment availability to generate P10/P50/P90 throughput projections displayed on shift dashboards.

*Sources: datup.ai (2026-02), thinksupplychain.co (2026-02), meta-intelligence.tech (2026-02), pymnts.com (2026-03-03)*

---

## Knowledge Update — 2026-03-06

### Supply Chain Forecast Accuracy Benchmarks — 2025/2026
**Sources:** IPEC Group / ASCM 2026 Benchmarking Study, datup.ai (2026-02), sranalytics.io (2025-10)

Updated quantitative benchmarks for predictive analytics in supply chain:

| Metric | Reported Improvement Range | Source |
|---|---|---|
| Forecast accuracy | 30–40% vs. baseline methods | datup.ai (2026) |
| Forecast accuracy | 20–50% (advanced models) | sranalytics.io (2025) |
| Forecast accuracy | 35% average | ASCM 2026 Benchmarking |
| Inventory cost reduction | 20–45% | ASCM 2026 |
| Order fulfillment rate | +15–25% | ASCM 2026 |
| Supply chain cost reduction | ~25% | sranalytics.io (2025) |
| ROI payback period | 6–12 months | sranalytics.io (2025) |

**Interpretation caution:** These are vendor/analyst ranges; variance is high. Use P50 values (30–35% accuracy improvement, 20% inventory reduction) as conservative planning benchmarks. The P90 figures (50%, 45%) require mature data infrastructure.

### Google DeepMind WeatherNext 2 — Implications for Supply Chain Forecasting
**Source:** PYMNTS.com (November 20, 2025)
**URL:** https://www.pymnts.com/supply-chain/2025/predictive-analytics-not-inventory-becomes-front-line-for-supply-chain-resilience

Key development: **WeatherNext 2** generates hundreds of probabilistic weather scenarios from a single starting point, at up to 1-hour resolution, in under 1 minute on a single TPU — 8× faster than previous generation.

**Supply chain implications:**
- High-fidelity probabilistic weather feeds are now accessible to non-scientific users
- Enables **weather-conditional demand forecasting**: attach weather ensemble scenarios to demand models as exogenous variables
- Particularly relevant for: agricultural inputs, cold chain, construction materials, seasonal retail, port logistics (storm delay probability)
- Integrates naturally with Monte Carlo simulation: weather scenario = one MC draw; run 500 weather scenarios × demand model = empirical distribution of outcomes

**Practical approach:** Use WeatherNext 2 outputs as stochastic exogenous inputs to ARIMAX or gradient boosted forecasting models, replacing static seasonal adjustment with probabilistic weather terms.

### Predictive Analytics as Supply Chain Resilience Layer
**Source:** PYMNTS.com (Nov 2025), GlobeNewswire (Jan 2026), ASCM 2026

The paradigm shift captured in the 2026 literature: **resilience = predictive capability, not inventory buffer.**

- 55% of supply chain leaders in 2025 are increasing technology investments specifically for operational resilience (ASCM 2026 Benchmarking Study)
- The model: predictive analytics absorbs uncertainty that was previously absorbed by safety stock
- Mathematical connection: **P(stockout) = f(forecast error distribution, σ_lead, safety stock)** — improving forecast accuracy shrinks σ_forecast, which has the same effect as carrying more safety stock without the capital cost

*Sources: ASCM 2026 Benchmarking Study (via IPEC Group), datup.ai (2026-02), PYMNTS.com (2025-11-20), sranalytics.io (2025-10), GlobeNewswire (2026-01-29)*

---

## Knowledge Update — 2026-03-07

### Predictive Analytics Market Adoption: 2026 Benchmarks
**Source:** GlobeNewswire (Jan 2026), ASCM 2026 Benchmarking Study, datup.ai (Feb 2026), sranalytics.io (Oct 2025)

Quantified outcomes from deployed predictive analytics in supply chain (2025 literature):

| Metric | Documented improvement range |
|---|---|
| Forecast accuracy | 30–50% improvement vs. baseline |
| Inventory cost reduction | 15–45% |
| Order fulfillment rate | +15–25% |
| ROI timeline | 6–12 months |

**Interpretation caution (DC tier note):** These figures come from vendor/consulting reports with selection bias toward successful implementations. They represent attainable outcomes, not median outcomes. Use as aspirational targets with appropriate uncertainty.

**Investment trend:** 55% of supply chain leaders in 2025 are increasing technology investment specifically for resilience — the strategic framing has shifted from "efficiency" to "resilience through prediction." The math behind this: carrying excess inventory is a fixed capital cost; predictive accuracy improvement has a variable cost that scales more favorably at high volume.

### Predictive Analytics as Safety Stock Substitute (Mathematical Formulation)
**Source:** datup.ai (2026-02), sranalytics.io (2025-10)

The economic argument for predictive analytics investment is rigorously grounded in safety stock theory:

**Standard safety stock formula:**
```
SS = z × σ_D × √L
```
where z = service level z-score, σ_D = demand std dev, L = lead time (normalized)

**With improved forecasting:**
```
SS_improved = z × σ_forecast_error × √L
```
If σ_forecast_error = (1 - improvement%) × σ_D, then:
- 35% forecast improvement → σ_forecast_error = 0.65 × σ_D → SS reduced by 35%
- This is a linear relationship: **every 1% forecast accuracy improvement ≈ 1% safety stock reduction**
- The capital cost avoided = (SS reduction) × (unit cost) × (carrying rate)

**ROI formula:**
```
ROI = [(SS_old - SS_new) × unit_cost × carry_rate] / analytics_investment_cost
```

This formulation makes the business case for predictive analytics directly computable and auditable — not a fuzzy "up to 40% improvement" claim.

*Sources: GlobeNewswire (2026-01-29), IPEC Group / ASCM 2026, datup.ai (2026-02), sranalytics.io (2025-10-28)*

---

## Knowledge Update — 2026-03-08

### Ensemble Forecasting in Supply Chain: Quantified Performance (2025-2026)
**Source:** dropoff.com / Forecasting Best Practices 2026 (citing 2025 study); IPEC Group / ASCM 2026 Benchmarking
**Published:** March 2026

Concrete benchmarks from production deployments:

- **2025 study of 73 retail implementations:** Ensemble forecasting models reduced forecast error by **23.9%** vs. single-model baselines
- **ASCM 2026 Benchmarking Study averages across AI-enabled forecasting deployments:**
  - Forecast accuracy improvement: **35%**
  - Inventory reduction: **20–45%**
  - Order fulfillment rate improvement: **15–25%**
- Gartner (2025): 50% of logistics companies using data analytics to optimize transportation networks

**Key design insight (ensemble construction):** The 23.9% error reduction figure aligns with the well-established ensemble bias-variance tradeoff theory — diverse models that err in different ways combine to cancel out individual model errors. Best practice: include at minimum (1) a statistical baseline (ARIMA/Holt-Winters), (2) an ML model (gradient boosting or LSTM), and (3) a domain-informed model (e.g., product lifecycle phase adjustment). Weighted combination via held-out validation outperforms simple averaging.

### Google DeepMind WeatherNext 2: Supply Chain Disruption Forecasting Step-Change (2025)
**Source:** PYMNTS.com — November 20, 2025
**URL:** https://www.pymnts.com/supply-chain/2025/predictive-analytics-not-inventory-becomes-front-line-for-supply-chain-resilience

A significant advance in the data feeds available for supply chain disruption prediction:

- **WeatherNext 2** (Google DeepMind, released November 2025): AI meteorology model generating hundreds of weather outcome scenarios from a single initialization point
- **Speed:** Forecasts generated 8× faster than prior generation; each forecast takes < 1 minute on a single TPU
- **Resolution:** Up to 1-hour temporal resolution (vs. 6-hour typical for operational NWP)
- **Supply chain implication:** High-fidelity probabilistic weather forecasting is now accessible to operations teams, not just energy/scientific users. Enables direct integration with supply chain disruption risk models — attach a probability-weighted weather scenario set to transportation lane risk assessment

**Strategic implication:** Organizations treating predictive analytics as the primary resilience mechanism (vs. holding buffer inventory) are achieving better cost-service tradeoffs. WeatherNext 2 makes weather-driven disruption scenarios tractable for probabilistic network models.

### Predictive Analytics Investment Trends (2026)
**Source:** GlobeNewswire — January 29, 2026

- 55% of supply chain leaders increasing tech/innovation investments in 2025-2026 for operational resilience
- Market for predictive analytics and maintenance in supply chain growing through 2031
- Primary investment areas: demand sensing, supplier risk monitoring, transportation optimization

*Sources: dropoff.com 2026-03-07, IPEC/ASCM 2026-02, PYMNTS 2025-11-20, GlobeNewswire 2026-01-29*

---

## [2026-03-08 Update] Rubric-Based Scoring Frameworks (RULERS + Autorubric)

### RULERS: Locked Rubrics + Evidence-Anchored Scoring (arXiv 2601.08654, Jan 2026)
**Problem:** LLM-as-Judge scoring fails due to rubric instability, unverifiable reasoning, and scale misalignment with human graders.

**Solution (three layers):**
1. **Locked rubrics** — compile natural language rubrics into versioned, immutable bundles; prevents prompt-sensitivity drift between scoring runs
2. **Evidence-anchored decoding** — each score assignment requires matching text evidence; creates auditable reasoning trail
3. **Wasserstein-based calibration** — aligns LLM output scale to human grading distribution without model fine-tuning

**Results:** Outperforms baselines on human agreement; smaller models rival larger proprietary judges with RULERS applied.
**Code:** https://github.com/LabRAI/Rulers.git

**Key insight for Dale's scoring systems:** The "locked rubric" concept is the right answer to rubric instability. Wasserstein calibration is the correct tool for scale alignment — it's a distribution-level alignment, not a point calibration.

### Autorubric: Unified Rubric Evaluation Framework (arXiv 2603.00077, Mar 2026)
Open-source Python framework unifying all known rubric-based LLM evaluation techniques.

**Capabilities:**
- Criterion types: binary, ordinal, nominal (with configurable weights)
- Aggregation modes: single judge, majority, weighted, unanimous, any-vote
- Calibration: few-shot with verdict-balanced sampling
- Bias mitigations: position bias (option shuffling), verbosity bias (length penalties), criterion conflation (per-criterion atomic evaluation)
- **Psychometric reliability metrics: Cohen's κ, weighted κ, Pearson/Spearman correlation, distribution-level tests**
- Production infrastructure: caching, checkpointing, rate limiting, cost tracking

**CHARM-100 dataset:** 100-sample benchmark with ground truth across binary + ordinal + nominal criteria. The first dataset for stress-testing heterogeneous rubric systems.

**Practical note:** The psychometric reliability metrics (Cohen's κ) are the mathematical proof that rubric scores are reproducible and valid — not just internally consistent. For presenting rubric systems to stakeholders, κ ≥ 0.61 (substantial agreement) is the defensibility threshold.

*Sources: arXiv:2601.08654, arXiv:2603.00077*

---

## [2026-03-09 Update] Predictive Analytics in Supply Chain — 2026 Benchmarks and Trends

### Quantified Performance Benchmarks (2025-2026 Industry Data)
**Sources:** IPEC Group / ASCM 2026 Benchmarking Study; sranalytics.io (October 2025); datup.ai (February 2026)

Consolidated benchmark ranges from multiple 2025-2026 industry studies:

| Metric | Improvement range | Notes |
|--------|-------------------|-------|
| Forecast accuracy | 20–50% improvement | vs. traditional methods; 35% average |
| Inventory cost reduction | 15–45% | Wider range reflects implementation maturity |
| Order fulfillment rate | 15–25% improvement | |
| ROI timeline | 6–12 months | For well-scoped implementations |

**55% of supply chain leaders** (ASCM 2026) increased investment in technology/innovation for operational resilience in 2025.

**Critical caveat:** These benchmarks are marketing-adjacent. The 35–50% accuracy improvement figures typically compare advanced ML against naive forecasting baselines, not against properly tuned ARIMA or exponential smoothing. For realistic expectations, compare against the current deployed method specifically.

---

### Google DeepMind WeatherNext 2 — High-Fidelity Weather Forecasting for Supply Chain
**Source:** PYMNTS.com (November 2025)

A step-change development with direct supply chain relevance:

- **Capability:** Generates hundreds of possible weather outcomes from a single starting point; forecasts 8× faster than prior models; resolution up to 1-hour intervals
- **Compute:** Each prediction < 1 minute on a single TPU
- **Implication:** Weather-correlated demand forecasting (retail, agriculture, energy, logistics) gains a dramatically improved exogenous variable. Weather disruption modeling in supply chains can now be probabilistic (ensemble forecasts) rather than deterministic (single forecast)
- **Access:** Expected to become available via Google Cloud APIs; watch for 2026 integration with supply chain planning platforms

**Modeling implication:** For products with weather-sensitive demand, incorporating WeatherNext 2 ensemble forecasts as probabilistic exogenous inputs to ARIMA or gradient-boosted models is now practically feasible. The uncertainty in the weather forecast propagates into demand forecast uncertainty bands — improving safety stock calculations.

---

### Predictive Analytics as Operational Resilience Infrastructure (2026 Shift)
**Source:** Multiple 2025-2026 industry sources (ASCM, Gartner-adjacent)

The fundamental framing shift underway:

- **Old model:** Predictive analytics as a capability layer (optional, applied to specific problems)
- **New model (2026):** Predictive analytics as front-line resilience infrastructure — replaces inventory buffers as the primary defense against supply chain disruption
- **Evidence:** Organizations reducing safety stock while maintaining service levels by substituting real-time demand signals + predictive models for static safety stock formulas
- **Risk note:** This substitution is only sound when model performance is continuously monitored (SPC on forecast errors) and fallback inventory protocols exist for model failures

**Mathematical implication:** Safety stock formula `z × σ_LTD × √(L + R)` gets modified: σ_LTD is now a model-predicted uncertainty (smaller when model is confident) rather than a fixed historical standard deviation. Tighter uncertainty estimates = lower safety stock = cost savings. But model confidence must be calibrated — overconfident models destroy service levels.

*Sources: globenewswire.com (2026-01), ipec-group.com (2026-02), pymnts.com (2025-11), sranalytics.io (2025-10)*

---

## [2026-03-10 Update] Future-Guided Learning (FGL) for Time Series Forecasting

**Source:** Nature Communications, s41467-025-63786-4 (September 30, 2025)

**Problem addressed:** Deep learning models capture nonlinear relationships but fail on long-term dependencies — especially under distribution shift, noise, and non-stationarity.

**Method — Future-Guided Learning (FGL):**
- Combines a *future-oriented* forecasting model (teacher) with a *past-oriented* forecasting model (student) in a Knowledge Distillation (KD) framework
- The teacher generates future predictions; student is continuously corrected by that feedback — a temporal interplay reminiscent of predictive coding in cognitive science
- Key differentiator from threshold-based drift detection (Page-Hinkley, DDM): FGL does not abruptly reset when drift is detected. It dynamically adjusts via continuous feedback, preserving long-term learned patterns rather than discarding them
- The student receives gradient signal from the teacher at every step — eliminates the "cold start" problem after drift detection

**vs. classical methods:**
| Method | Drift response | Long-term memory |
|--------|---------------|-----------------|
| ARIMA | N/A (static) | Limited |
| EWMA smoothing | Slow | Good |
| DDM/Page-Hinkley | Reset on detection | Lost after reset |
| FGL | Continuous correction | Preserved |

**Supply chain relevance:** Particularly strong for demand signals with gradual distributional shift — post-disruption recovery patterns, secular trend changes, channel mix shifts. FGL's continuous correction means you don't lose learned baseline when the market shifts.

**Implementation note:** Requires deep learning infrastructure. Not a drop-in replacement for ARIMA, but a serious candidate when you have enough data volume and a non-stationary environment.

*Source: Nature Communications, arXiv preprint. Authors: multiple. Published 2025-09-30.*

---

## [2026-03-10 Update] EEMD + LASSO + LSTM Hybrid for Demand Forecasting

**Source:** ScienceDirect / Computers & Industrial Engineering (July 2025), doi:10.1016/j.cie.2025....

**Method:** Three-stage hybrid:
1. **EEMD (Ensemble Empirical Mode Decomposition):** Decomposes demand into intrinsic mode functions (IMFs) — separates high-frequency noise from trend and seasonal components without assuming stationarity. Advantage over FFT: handles non-linear, non-stationary signals.
2. **LASSO regression:** Selects the most predictive IMFs and external features (price, promotions, weather). Provides automatic feature selection and prevents overfitting.
3. **LSTM (Long Short-Term Memory):** Learns sequence patterns in the selected IMFs; generates final forecast.

**Why EEMD over FFT or STL decomposition:**
- STL assumes additive structure with fixed periodicity — breaks on intermittent demand or changing seasonality
- FFT assumes stationarity — breaks on trend changes
- EEMD makes no periodicity or stationarity assumptions; decomposes the signal adaptively

**Reported performance:** Superior capture of irregular demand patterns (lumpy, intermittent, promotional spike) compared to ARIMA, ETS, and vanilla LSTM baselines.

**Supply chain fit:** High SKU-count environments where demand patterns vary by SKU and include promotional effects. EEMD+LASSO stage handles pattern heterogeneity; LSTM handles the learned temporal structure.

**Caution:** Computationally intensive at scale. For 10K+ SKUs, needs parallelization and a tiered approach (simple exponential smoothing for stable SKUs; EEMD+LASSO+LSTM for high-value volatile SKUs).

*Source: ScienceDirect, pii/S2667305325000663 (2025-07)*

---

## [2026-03-10 Update] TIME Benchmark — Pattern-Level Evaluation for TSFMs

**Source:** arXiv:2602.12147 — "Towards the Next Generation of Time Series Forecasting Benchmarks" (February 2026)

### What TIME Is

A next-generation benchmark for evaluating Time Series Foundation Models (TSFMs) in strict zero-shot conditions. 50 fresh datasets, 98 tasks; human-in-the-loop construction with LLM assistance for quality assurance. No data leakage.

Leaderboard: https://huggingface.co/spaces/Real-TSF/TIME-leaderboard

### Key Methodological Innovation: Pattern-Level Evaluation

Legacy benchmarks report average error per dataset (dataset-level). TIME introduces **pattern-level evaluation**:
- Characterize time series by structural features (trend strength, seasonality, autocorrelation, intermittency, volatility).
- Group datasets by pattern profile.
- Report model performance *per pattern group*.

**Why this matters:** A model can score well on average while failing on a specific pattern type (e.g., intermittent demand). Pattern-level evaluation reveals this. For supply chain, this means the question isn't "which model is best overall?" but "which model is best for this demand pattern?"

### Identified Limitations of Existing Benchmarks (directly applicable to our work)

| Limitation | Implication for SC Modeling |
|-----------|----------------------------|
| Reused legacy data (M4, ETT) | Our internal SC data may have different characteristics — don't assume M4 rankings transfer |
| Data leakage (TSFMs trained on public datasets) | Zero-shot claims need leakage-verified evaluation |
| Dataset-level averages mask pattern failure | Use pattern-level evaluation when comparing demand models |
| Misaligned task formulations | Evaluation horizon and frequency should match operational decision cadence |

### Practical Guidance

When benchmarking demand forecasting models internally:
1. Characterize each SKU's time series by structural pattern (trend, seasonal, intermittent, volatile).
2. Evaluate each model per pattern group, not just on overall MAPE/RMSE.
3. Use the pattern-group ranking to match models to SKU types in production.

*Source: arXiv:2602.12147, February 2026*

---

## [2026-03-10 Update] LLM Scoring Alignment — SFT + DPO + RAG Framework

**Source:** arXiv:2603.06424 — "From Prompting to Preference Optimization: A Comparative Study of LLM-based Automated Essay Scoring" (March 2026)

### Empirical Ranking of Scoring Architectures (IELTS Writing, F1-Score)

| Approach | F1-Score | Notes |
|---------|---------|-------|
| SFT + RAG | 93% | Best configuration overall |
| SFT + DPO + RAG | Near top | Best rubric alignment |
| Instruction tuning + RAG | Good | Solid baseline |
| Few-shot prompting | Moderate | No fine-tuning required |
| Encoder classification | Varies | Fast but brittle |

### Relevance to AI-in-the-Loop Scoring (Dale's Work)

**The key insight:** Pure prompting is convenient but leaves alignment to chance. When rubric conformance matters, SFT + RAG is the practical gold standard. DPO adds a preference alignment layer that closes the gap between model predictions and human rubric judgments.

**Implementation pathway for supply chain quality scoring:**
1. Collect interaction traces (Critic Rubrics approach, P28).
2. Fine-tune on rubric-labeled examples (SFT stage).
3. Use RAG to inject relevant rubric context at inference.
4. Apply DPO to align model outputs with human preference when divergence is detected.

*Source: arXiv:2603.06424 [cs.CL], March 2026*
