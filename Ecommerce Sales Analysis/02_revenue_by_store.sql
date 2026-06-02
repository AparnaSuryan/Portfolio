SELECT 
    ss_store_sk AS store,
    ROUND(SUM(ss_net_paid), 2) AS total_revenue,
    ROUND(SUM(ss_net_profit), 2) AS total_profit,
    COUNT(DISTINCT ss_ticket_number) AS total_orders
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES
GROUP BY ss_store_sk
ORDER BY total_revenue DESC
LIMIT 20;