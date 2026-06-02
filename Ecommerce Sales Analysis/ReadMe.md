# E-Commerce Sales Analytics Dashboard

## Project Overview
End-to-end data analytics project using Snowflake and Data Studio to analyze e-commerce sales trends, seasonal patterns, and customer behaviour
across 2001-2002 on a dataset of 957M+ orders.

## Tools & Technologies
- **Snowflake** — Cloud data warehouse (SQL queries)
- **Data Studio** — Business Intelligence dashboard
- **SQL** — Data transformation and analysis

## Dashboard
https://datastudio.google.com/s/oC_iPOOHxLs

## Key Insights
- Holiday season (Nov-Dec) generates 2x more revenue than any other season
- Saturday and Monday are the highest revenue days in December
- Revenue remained stable YoY (2001 vs 2002) showing consistent business performance
- Top customer spent over $6M across 218 orders

## SQL Analyses
| File | Description |
|---|---|
| 01_monthly_revenue.sql | Monthly revenue and profit trend 2001-2002 |
| 02_revenue_by_store.sql | Revenue and profit breakdown by store |
| 03_top_customers.sql | Top 20 customers by total spend |
| 04_seasonal_analysis.sql | Revenue comparison across seasons |
| 05_daily_sales.sql | Daily sales performance in December 2001 |

## Dataset
Snowflake Sample Data — `TPCDS_SF10TCL`
Scale factor 10, simulating a large retail enterprise with billions of transactions.
