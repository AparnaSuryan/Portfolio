SELECT *
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES
LIMIT 10;



SELECT 
    d.d_year AS year,
    d.d_moy AS month,
    ROUND(SUM(ss.ss_net_paid), 2) AS total_revenue,
    ROUND(SUM(ss.ss_net_profit), 2) AS total_profit,
    COUNT(DISTINCT ss.ss_ticket_number) AS total_orders
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES ss
JOIN SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.DATE_DIM d
    ON ss.ss_sold_date_sk = d.d_date_sk
WHERE d.d_year IN (2001, 2002)
GROUP BY d.d_year, d.d_moy
ORDER BY d.d_year, d.d_moy;
