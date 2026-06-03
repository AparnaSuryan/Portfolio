# Marketing Campaign Analytics Dashboard

## Project Overview
End-to-end data analytics project analyzing customer behavior and 
marketing campaign performance for 2,216 customers using Python, 
PostgreSQL, and Power BI.

## Data Pipeline

```
+------------------+
|  Raw CSV Data    |
|  2,216 customers |
+--------+---------+
         |
         v
+------------------+
|  Python + Pandas |
|  - Clean data    |
|  - Feature eng.  |
|  - Build schemas |
+--------+---------+
         |
         v
+------------------+
|   PostgreSQL     |
|  - Star Schema   |
|  - Snowflake     |
|    Schema        |
+--------+---------+
         |
         v
+------------------+
|  Power Query     |
|  - Age groups    |
|  - Income bands  |
|  - Channels      |
+--------+---------+
         |
         v
+------------------+
|  DAX Measures    |
|  - Revenue       |
|  - Response Rate |
|  - YoY Growth    |
+--------+---------+
         |
         v
+------------------+
|  Power BI        |
|  Dashboard       |
|  5 visuals +     |
|  2 slicers       |
+------------------+
```


## Tools & Technologies
- **Python** — Data cleaning, transformation, ETL pipeline
- **Pandas** — Data manipulation
- **PostgreSQL** — Cloud data warehouse, data modeling
- **SQLAlchemy** — Python to PostgreSQL connection
- **Power BI** — Dashboard and visualization
- **Power Query (M Language)** — Data transformation
- **DAX** — KPI measures and calculations

## Data Modeling
Built and compared two schema designs on the same dataset:

### Star Schema (4 tables)
- `fact_marketing` — Core metrics and measures
- `dim_customer` — Customer demographics
- `dim_date` — Date dimensions
- `dim_campaign` — Campaign reference data

### Snowflake Schema (9 tables)
- Normalized dim_customer into `snow_dim_education` 
and `snow_dim_marital`
- Normalized dim_date into `snow_dim_year` and `snow_dim_month`
- Normalized dim_campaign into `snow_dim_campaign_type`

### Star vs Snowflake Tradeoffs
| | Star Schema | Snowflake Schema |
|---|---|---|
| Tables | 4 | 9 |
| Query Speed | Faster | Slower |
| Storage | More redundancy | Less redundancy |
| Best For | Power BI / Reporting | Large data warehouses |

## DAX Measures
- **Total Revenue** — SUM of customer spending
- **Total Customers** — DISTINCTCOUNT of customers
- **Avg Order Value** — Revenue per customer
- **Response Rate** — % customers who responded to campaigns
- **YoY Revenue Growth** — Year over year comparison
- **High Value Customers** — Customers spending over $1,000

## Power Query Transformations
- Added `age_group` column (Young/Middle Age/Senior/Elderly)
- Added `income_band` column (Low/Medium/High/Very High)
- Added `spending_category` (Low/Medium/High/VIP Spender)
- Added `top_channel` (Store/Web/Catalog)
- Added `response_label` (Responded/Did Not Respond)

## Key Insights
- **Seniors** are the highest spending age group
- **Graduation** level customers generate most revenue
- **Store** channel dominates with 24K purchases vs 6K web
- **15% campaign response rate** — above industry average
- **Low spenders** form the largest customer segment

## Files
| File | Description |
|---|---|
| `01_clean_data.py` | Data cleaning and transformation |
| `02_star_schema.py` | Star schema creation |
| `03_load_to_postgres.py` | Load data to PostgreSQL |
| `04_snowflake_schema.py` | Snowflake schema creation |
| `marketing_analytics.pbix` | Power BI dashboard file |

## Dataset
IBM Marketing Campaign Dataset from Kaggle
- 2,216 customers
- 29 features
- Customer demographics, purchase history, campaign responses
