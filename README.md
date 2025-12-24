# NASA CMAPSS Predictive Maintenance – Remaining Useful Life (RUL) Prediction

## Project Overview

This project develops an **end-to-end predictive maintenance pipeline** to estimate the **Remaining Useful Life (RUL)** of turbofan engines using the NASA CMAPSS dataset.

The goal is to demonstrate:
- Sound exploratory data analysis (EDA)
- Degradation-aware feature engineering
- Leakage-safe model evaluation
- Defensible model selection based on generalization and interpretability

The project uses the **FD001 subset**, which represents a single operating condition and a single fault mode.

---

## Objectives

- Understand engine degradation behavior from multivariate time-series sensor data
- Engineer features that capture progressive damage accumulation
- Compare linear and nonlinear regression models for RUL prediction
- Select a robust baseline model suitable for real-world maintenance decision-making
- Provide interpretable insights into model behavior

---

## Dataset

- **Source:** NASA CMAPSS (Commercial Modular Aero-Propulsion System Simulation)
- **Subset:** FD001
- **Engines:** 100 training engines, run-to-failure
- **Sensors:** 21 sensor measurements + operational settings
- **Target:** Remaining Useful Life (RUL), computed from run-to-failure trajectories

---

## Project Structure

```
NASA-CMAPSS-Predictive-Maintenance/
│
├── data/
│   ├── raw/                      # Original CMAPSS files
│   └── processed/                # Cleaned & engineered datasets
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_modeling.ipynb
│
├── src/
│   ├── features.py               # Reusable feature functions
│   ├── models.py
│   └── utils.py
│
├── results/
│   ├── figures/                  # Plots and visualizations
│   ├── metrics.csv               # Final model metrics
│   └── ridge_final.joblib        # Saved final model
│
├── requirements.txt
└── README.md
```

---

## 1. Exploratory Data Analysis (EDA)

**Notebook:** `01_eda.ipynb`

Key findings from EDA:

- Engine lifetimes vary significantly, requiring engine-specific modeling
- Several sensors exhibit monotonic degradation trends as failure approaches
- Multiple sensors show strong correlation with RUL
- A subset of sensors has near-zero variance and provides no predictive value
- Operational settings have minimal influence in FD001
- Degradation behavior is progressive rather than abrupt

These insights guided feature selection and engineering strategies.

---

## 2. Feature Engineering

**Notebook:** `02_feature_engineering.ipynb`

Feature engineering focuses on capturing **degradation dynamics** rather than raw sensor values.

Key feature groups:

- **Per-engine standardization** – Emphasizes relative degradation patterns instead of absolute sensor levels
- **Cumulative damage indicators** – Approximate irreversible wear accumulation over time
- **Rolling statistics & slopes** – Capture short-term variability and long-term degradation trends
- **Rate-of-change features** – Identify accelerating degradation behavior
- **Limited interaction terms** – Introduced only for highly correlated sensor pairs
- **Normalized lifecycle position (`cycle_norm`)** – Represents relative engine life progression

Feature selection is performed using **mutual information on engine endpoints** to avoid temporal leakage.

---

## 3. Modeling & Evaluation

**Notebook:** `03_modeling.ipynb`

### Modeling Strategy

Models are evaluated progressively:

1. **Ridge Regression (baseline)** – Linear model with L2 regularization, strong stability, high interpretability
2. **XGBoost** – Nonlinear, tree-based ensemble with high training capacity
3. **MLP (Neural Network)** – High-capacity nonlinear model

### Evaluation Protocol

- Train–validation split performed **by engine ID** (no leakage across cycles)
- Test evaluation uses **only the last cycle per engine**
- Metrics: RMSE, MAE, R²
- Test performance prioritized over training metrics

---

## Results Summary

| Model    | Test RMSE | Test MAE | Test R² |
|----------|-----------|----------|---------|
| Ridge    | **36.46** | **29.51** | **0.23** |
| XGBoost  | 79.82     | 69.69    | -2.69   |
| MLP      | 85.68     | 69.68    | -3.25   |

### Key Insight

While XGBoost and MLP achieve excellent training and validation performance, they **fail to generalize** to unseen test engines due to overfitting to engine-specific degradation trajectories.

**Ridge regression generalizes substantially better**, making it the most reliable model for deployment.

---

## Model Interpretability

SHAP (SHapley Additive exPlanations) is used to analyze feature contributions.

- **XGBoost SHAP** shows heavy reliance on lifecycle proxy features (e.g., normalized cycle position), explaining poor generalization
- **Ridge SHAP** reveals more evenly distributed, physically meaningful degradation features, supporting its robustness

---

## Maintenance-Oriented Evaluation

To assess real-world usefulness, RUL predictions are converted into a binary classification task using a **30-cycle threshold**.

**Ridge Regression Performance (Test Set):**
- Precision: **0.96**
- Recall: **0.92**
- F1-score: **0.94**

This demonstrates strong capability to identify engines approaching failure.

---

## Final Model Selection

**Ridge Regression** is selected as the final model due to:
- Superior test generalization
- Stability in high-dimensional feature space
- Interpretability of degradation drivers
- Practical maintenance decision performance

The trained model is saved for reproducibility and downstream use.

---

## Key Takeaways

- Simpler models can outperform complex models in low-sample, high-dimensional settings
- Engine-level data leakage prevention is critical for honest evaluation
- Degradation-aware features are more important than model complexity
- Interpretability is a strength, not a trade-off, in predictive maintenance

---

## Tools & Libraries

- Python, NumPy, Pandas
- Scikit-learn
- XGBoost
- TensorFlow / Keras
- SHAP
- Matplotlib, Seaborn

---

<div align="center">
This project demonstrates an end-to-end predictive maintenance workflow, emphasizing sound methodology, robust evaluation, and interpretable model selection in a real-world engineering context.
</div>