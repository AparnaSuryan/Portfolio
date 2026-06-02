SELECT 
    d.d_date AS date,
    d.d_day_name AS day_of_week,
    ROUND(SUM(ss.ss_net_paid), 2) AS total_revenue,
    COUNT(DISTINCT ss.ss_ticket_number) AS total_orders
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES ss
JOIN SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.DATE_DIM d
    ON ss.ss_sold_date_sk = d.d_date_sk
WHERE d.d_year = 2001
AND d.d_moy = 12
GROUP BY d.d_date, d.d_day_name
ORDER BY d.d_date;