SELECT 
    d.d_year AS year,
    d.d_qoy AS quarter,
    CASE 
        WHEN d.d_moy IN (11, 12) THEN 'Holiday Season'
        WHEN d.d_moy IN (6, 7, 8) THEN 'Summer'
        WHEN d.d_moy IN (3, 4, 5) THEN 'Spring'
        ELSE 'Winter'
    END AS season,
    ROUND(SUM(ss.ss_net_paid), 2) AS total_revenue,
    COUNT(DISTINCT ss.ss_ticket_number) AS total_orders
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES ss
JOIN SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.DATE_DIM d
    ON ss.ss_sold_date_sk = d.d_date_sk
WHERE d.d_year IN (2001, 2002)
GROUP BY d.d_year, d.d_qoy, season
ORDER BY d.d_year, d.d_qoy;

