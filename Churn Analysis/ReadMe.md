# Customer Churn Analysis & Prediction

A complete end-to-end data analytics project that identifies at-risk customers and predicts churn probability using machine learning — deployed as a live interactive dashboard.

---

## Business Problem

A telecom company is losing 1 in 4 customers. Every churned customer represents lost recurring revenue. This project answers three questions:

- **Who** is most likely to churn?
- **Why** are they leaving?
- **When** should the business intervene?

---

## Live Demo

Run the dashboard locally:

```bash
streamlit run app.py
```

**Dashboard pages:**
- **Overview** — KPI metrics, churn distribution, top drivers
- **Customer Segments** — Churn rates by contract, internet service, payment method, and more
- **Churn Predictor** — Enter any customer's details and get a live churn probability score with a retention recommendation

---

## Key Findings

| Insight | Detail |
|---|---|
| Overall churn rate | 26.5% — 1 in 4 customers leaving |
| Highest risk segment | Month-to-month fiber optic customers in first 12 months |
| Safest segment | Two-year contract customers (churn rate under 3%) |
| Top churn driver | `charges_per_tenure` — a custom engineered feature |
| Critical window | 80% of churners leave within the first 12 months |
| Payment risk | Electronic check users churn at 2x the rate of other methods |

---

## Model Performance

Two models were trained and compared:

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression (baseline) | 0.799 | 0.838 |
| Random Forest | 0.793 | 0.834 |

Logistic Regression marginally outperformed Random Forest — a reminder that simpler models can win on smaller, linear datasets. Both models significantly outperform random guessing (AUC 0.5).

---

## Feature Engineering

Three new features were created beyond the original dataset:

| Feature | Logic | Why it matters |
|---|---|---|
| `charges_per_tenure` | Monthly charges / (tenure + 1) | Captures customers paying a lot before building loyalty — the #1 churn predictor |
| `total_services` | Sum of all add-on services | More services = more embedded = less likely to leave |
| `high_spender` | Monthly charges above median | Flags premium customers with no loyalty perks |

---

## Project Structure

```
churn/
│
├── app.py                    # Streamlit dashboard
├── churn_eda.ipynb           # Exploratory data analysis
├── churn_features.ipynb      # Feature engineering
├── churn_model.ipynb         # Model training and evaluation
│
├── telco_churn_clean.csv     # Cleaned, engineered dataset
├── churn_model.pkl           # Trained Random Forest model
│
└── charts/
    ├── churn_distribution.png
    ├── churn_by_contract.png
    ├── tenure_churn.png
    ├── charges_churn.png
    ├── feature_importance.png
    ├── confusion_matrix.png
    └── roc_curve.png
```

---

## Tech Stack

All free and open source:

- **Python 3.8**
- **pandas** — data manipulation
- **matplotlib / seaborn** — visualization
- **scikit-learn** — machine learning
- **joblib** — model persistence
- **Streamlit** — interactive dashboard

---

## ⚙️ How to Run

**1 — Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/customer-churn-prediction
cd customer-churn-prediction
```

**2 — Install dependencies**
```bash
pip install pandas scikit-learn matplotlib seaborn streamlit joblib
```

**3 — Launch the dashboard**
```bash
streamlit run app.py
```

---

## Dataset

IBM Telco Customer Churn dataset — 7,032 customers, 21 features including contract type, payment method, tenure, monthly charges, and churn status.

Source: [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Business Recommendations

Based on the analysis, three actions would meaningfully reduce churn:

1. **Target new fiber optic customers in month 1–3** with a proactive outreach call and a contract upgrade incentive
2. **Bundle online security and tech support** into onboarding packages — customers with these services churn at half the rate
3. **Nudge electronic check users** toward auto-pay — this payment method is strongly correlated with churn and may indicate lower engagement

---

*Built as a portfolio project demonstrating end-to-end data analytics: EDA, feature engineering, machine learning, and dashboard deployment.*
