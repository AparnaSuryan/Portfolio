# Sales Forecasting & Demand Analysis (Airbnb Case Study)

## Project Overview
This project analyzes customer survey data and historical booking patterns to understand **demand behavior** and build **time series forecasting models**.  
The objective is to identify trends, seasonality, and provide **business-driven recommendations** using Python-based forecasting techniques.

---

## Data Sources
- **Survey Data:** Customer preferences, demographics, and usage behavior
- **Time Series Data:** Historical Airbnb booking data

---

## Survey Insights

### Key Findings
- The primary reasons customers choose Airbnb are:
  - Location
  - Cost
  - Comfort
  - Convenience
- Most respondents reported a **positive experience** using Airbnb.
- Airbnb is **more frequently preferred by females** than males.
- **Students** represent the largest group of Airbnb users compared to other occupants.

---

## Time Series Analysis

### Demand Behavior
- **Trend:** Gradual increase in bookings over time
- **Seasonality:**  
  - Higher bookings during **summer months**  
  - Lower bookings during **winter months**
- **Residuals:** No significant pattern observed

---

## Forecasting Models Evaluated

### Naïve Method
- Large deviation from actual values
- Underestimates peaks and overestimates troughs
- Ignores trend and seasonality

### Simple Average
- Produces a flat forecast
- Does not account for trend or seasonality

### Simple Moving Average (SMA)
- Follows trend more closely than the naïve method
- Smooths short-term fluctuations
- Does not explicitly model seasonality

### Simple Exponential Smoothing (SES)
- Identifies basic trend patterns
- Does not capture seasonality

### Holt-Winters Additive Model
- Captures trend and seasonality
- Minor deviations at peak and trough points
- Performs better than SES and SMA

### Holt-Winters Multiplicative Model
- Best-performing model
- Accurately captures both trend and seasonality
- Achieves the **lowest MAPE and RMSE values**

---

## Forecast Accuracy Comparison
- Holt-Winters Multiplicative model outperforms all other methods
- Provides the most reliable and realistic forecasts

---

## Business Recommendations
- Airbnb demand peaks during **summer**
- The company should:
  - Increase marketing and promotional campaigns during high-demand periods
  - Offer discounts and incentives during winter to reduce demand troughs
  - Diversify offerings to minimize the impact of seasonal fluctuations

---

## Tools & Techniques
- Python
- Time Series Analysis
- Holt-Winters Forecasting
- Error Metrics (MAPE, RMSE)
